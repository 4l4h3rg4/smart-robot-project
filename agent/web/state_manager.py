"""
Gestor central del estado del robot para la plataforma web.

Singleton que maneja: conexión TCP, heartbeat, controlador, sensores,
broadcast WebSocket y procesamiento de comandos del agente.
"""

import asyncio
import logging
import os
import threading
import time
from typing import Optional

from dotenv import load_dotenv
from fastapi import WebSocket
from google.adk.runners import Runner
from google.adk.sessions import InMemorySessionService
from google.genai import types as genai_types

from agent.agent import root_agent
from robot.camera import capture_frame as camera_capture, frame_to_bytes
from robot.connection import RobotConnection
from robot.controller import RobotController

load_dotenv()

logger = logging.getLogger("web.state_manager")

ROBOT_IP = os.getenv("ROBOT_IP", "192.168.4.1")
SENSOR_POLL_INTERVAL = 2.5  # segundos


class RobotStateManager:
    _instance: Optional["RobotStateManager"] = None
    _lock = threading.Lock()

    def __new__(cls) -> "RobotStateManager":
        if cls._instance is None:
            with cls._lock:
                if cls._instance is None:
                    cls._instance = super().__new__(cls)
                    cls._instance._init()
        return cls._instance

    def _init(self) -> None:
        self.robot_ip = ROBOT_IP
        self.connected = False
        self._conn: Optional[RobotConnection] = None
        self._ctrl: Optional[RobotController] = None
        self._ws_clients: list[WebSocket] = []
        self._ws_lock = asyncio.Lock()

        # Estado actual del robot
        self.distance_cm: Optional[int] = None
        self.ir_left: Optional[int] = None
        self.ir_mid: Optional[int] = None
        self.ir_right: Optional[int] = None
        self.servo_pan = 90
        self.servo_tilt = 90

        # Actividad del agente
        self.activity_log: list[dict] = []
        self.max_activity = 100

        # Tareas de fondo
        self._sensor_task: Optional[asyncio.Task] = None
        self._command_lock = asyncio.Lock()

        # ADK
        self._session_service = InMemorySessionService()
        self._runner = Runner(
            agent=root_agent,
            app_name="smart-robot-web",
            session_service=self._session_service,
        )
        self._session_id: Optional[str] = None

    @property
    def ctrl(self) -> Optional[RobotController]:
        return self._ctrl

    @property
    def conn(self) -> Optional[RobotConnection]:
        return self._conn

    # ============================================================
    #  Conexión / Desconexión
    # ============================================================

    async def connect(self, ip: str = ROBOT_IP) -> str:
        if self.connected:
            return "Ya está conectado al robot."

        self.robot_ip = ip
        loop = asyncio.get_event_loop()
        try:
            await loop.run_in_executor(None, self._connect_sync, ip)
        except Exception as e:
            logger.error(f"Error conectando: {e}")
            raise

        self.connected = True
        self._start_sensor_polling()

        # Inicializar sesión ADK
        session = await self._session_service.create_session(
            app_name="smart-robot-web",
            user_id="web_user",
        )
        self._session_id = session.id

        self._add_activity("system", f"Conectado al robot en {ip}")
        await self._broadcast_state()
        return f"Conectado a {ip}"

    def _connect_sync(self, ip: str) -> None:
        self._conn = RobotConnection(ip=ip)
        self._conn.connect()
        self._ctrl = RobotController(self._conn)
        self._ctrl.center_camera()
        self.servo_pan = 90
        self.servo_tilt = 90

        # Sincronizar con agent.robot_state para que los tools del agente
        # (que usan get_controller()) encuentren la conexión
        import agent.robot_state as robot_state
        robot_state._conn = self._conn
        robot_state._ctrl = self._ctrl

    async def disconnect(self) -> str:
        if not self.connected:
            return "No hay conexión activa."

        self._stop_sensor_polling()
        self.connected = False

        loop = asyncio.get_event_loop()
        await loop.run_in_executor(None, self._disconnect_sync)

        self._add_activity("system", "Desconectado del robot")
        await self._broadcast_state()
        return "Desconectado."

    def _disconnect_sync(self) -> None:
        if self._ctrl:
            try:
                self._ctrl.stop()
            except Exception:
                pass
        if self._conn:
            try:
                self._conn.disconnect()
            except Exception:
                pass
        self._conn = None
        self._ctrl = None
        self.distance_cm = None
        self.ir_left = None
        self.ir_mid = None
        self.ir_right = None

        # Limpiar agent.robot_state
        import agent.robot_state as robot_state
        robot_state._conn = None
        robot_state._ctrl = None

    # ============================================================
    #  WebSocket
    # ============================================================

    async def register_ws(self, ws: WebSocket) -> None:
        async with self._ws_lock:
            self._ws_clients.append(ws)
        # Enviar estado actual al nuevo cliente
        try:
            await ws.send_json({
                "type": "robot_state",
                "data": self._build_state_payload(),
            })
        except Exception:
            await self.unregister_ws(ws)

    async def unregister_ws(self, ws: WebSocket) -> None:
        async with self._ws_lock:
            if ws in self._ws_clients:
                self._ws_clients.remove(ws)
        # Si no quedan clientes, detener polling
        if not self._ws_clients:
            self._stop_sensor_polling()

    async def _broadcast(self, payload: dict) -> None:
        async with self._ws_lock:
            dead: list[WebSocket] = []
            for ws in self._ws_clients:
                try:
                    await ws.send_json(payload)
                except Exception:
                    dead.append(ws)
            for ws in dead:
                self._ws_clients.remove(ws)

    async def _broadcast_state(self) -> None:
        await self._broadcast({
            "type": "robot_state",
            "data": self._build_state_payload(),
        })

    def _build_state_payload(self) -> dict:
        return {
            "connected": self.connected,
            "robot_ip": self.robot_ip,
            "distance_cm": self.distance_cm,
            "ir_left": self.ir_left,
            "ir_mid": self.ir_mid,
            "ir_right": self.ir_right,
            "servo_pan": self.servo_pan,
            "servo_tilt": self.servo_tilt,
        }

    # ============================================================
    #  Sensores
    # ============================================================

    async def poll_sensors(self) -> Optional[dict]:
        if not self.connected or not self._ctrl:
            return None

        loop = asyncio.get_event_loop()
        try:
            dist = await loop.run_in_executor(None, self._ctrl.get_distance_cm)
            self.distance_cm = dist
        except Exception as e:
            logger.warning(f"Error leyendo ultrasónico: {e}")

        try:
            ir = await loop.run_in_executor(None, self._ctrl.get_ir_sensors)
            if ir:
                self.ir_left = ir.get("left")
                self.ir_mid = ir.get("mid")
                self.ir_right = ir.get("right")
        except Exception as e:
            logger.warning(f"Error leyendo IR: {e}")

        await self._broadcast_state()
        return self._build_state_payload()

    def _start_sensor_polling(self) -> None:
        if self._sensor_task and not self._sensor_task.done():
            return
        self._sensor_task = asyncio.create_task(self._sensor_loop())

    def _stop_sensor_polling(self) -> None:
        if self._sensor_task and not self._sensor_task.done():
            self._sensor_task.cancel()
            self._sensor_task = None

    async def _sensor_loop(self) -> None:
        while self.connected:
            await asyncio.sleep(SENSOR_POLL_INTERVAL)
            if not self._ws_clients:
                continue
            # No pollear si hay un comando en curso
            if self._command_lock.locked():
                continue
            await self.poll_sensors()

    # ============================================================
    #  Procesamiento de comandos del agente
    # ============================================================

    async def process_command(self, text: str) -> None:
        if not self._session_id:
            await self._broadcast({
                "type": "agent_error",
                "data": {"message": "Conéctese al robot primero."},
            })
            return

        async with self._command_lock:
            self._add_activity("user", text)

            content = genai_types.Content(
                role="user",
                parts=[genai_types.Part(text=text)],
            )

            try:
                async for event in self._runner.run_async(
                    user_id="web_user",
                    session_id=self._session_id,
                    new_message=content,
                ):
                    if event.content and event.content.parts:
                        for part in event.content.parts:
                            # Respuesta de texto del agente
                            if hasattr(part, "text") and part.text:
                                self._add_activity("agent", part.text)
                                await self._broadcast({
                                    "type": "agent_text",
                                    "data": {"text": part.text},
                                })

                            # Llamada a herramienta
                            elif hasattr(part, "function_call") and part.function_call:
                                fc = part.function_call
                                tool_name = fc.name if hasattr(fc, "name") else str(fc)
                                tool_args = fc.args if hasattr(fc, "args") else {}
                                self._add_activity("tool_call", f"{tool_name}({tool_args})")
                                await self._broadcast({
                                    "type": "tool_call",
                                    "data": {"name": str(tool_name), "args": dict(tool_args) if hasattr(tool_args, "items") else str(tool_args)},
                                })

                            # Resultado de herramienta
                            elif hasattr(part, "function_response") and part.function_response:
                                fr = part.function_response
                                fr_name = fr.name if hasattr(fr, "name") else str(fr)
                                fr_result = str(fr.response) if hasattr(fr, "response") else str(fr)
                                self._add_activity("tool_result", f"{fr_name}: {fr_result}")
                                await self._broadcast({
                                    "type": "tool_result",
                                    "data": {"name": str(fr_name), "result": fr_result},
                                })

                # Después del comando, refrescar sensores
                if self.connected:
                    await self.poll_sensors()

                await self._broadcast({"type": "command_complete", "data": {}})

            except Exception as e:
                logger.error(f"Error procesando comando: {e}")
                await self._broadcast({
                    "type": "agent_error",
                    "data": {"message": str(e)},
                })

    async def stop_robot(self) -> str:
        if not self.connected or not self._ctrl:
            return "Robot no conectado."
        loop = asyncio.get_event_loop()
        await loop.run_in_executor(None, self._ctrl.stop)
        self._add_activity("system", "Robot detenido (manual)")
        return "Robot detenido."

    # ============================================================
    #  Cámara
    # ============================================================

    def capture_frame(self):
        if not self.connected:
            return None
        try:
            frame = camera_capture(ip=self.robot_ip)
            return frame_to_bytes(frame)
        except Exception as e:
            logger.warning(f"Error capturando frame: {e}")
            return None

    # ============================================================
    #  Log de actividad
    # ============================================================

    def _add_activity(self, kind: str, message: str) -> None:
        entry = {
            "kind": kind,
            "message": message,
            "timestamp": time.time(),
        }
        self.activity_log.append(entry)
        if len(self.activity_log) > self.max_activity:
            self.activity_log = self.activity_log[-self.max_activity:]


# Singleton accesible globalmente
state = RobotStateManager()
