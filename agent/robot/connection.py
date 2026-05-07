"""
TCP client para el robot ELEGOO Smart Robot Car V4.0.

El ESP32 del robot escucha en el puerto 100. Los comandos son JSON
encerrado entre { }. El robot requiere un heartbeat cada ~1s o se detiene.
"""

import json
import socket
import threading
import time
from typing import Optional


ROBOT_IP = "192.168.4.1"
ROBOT_PORT = 100
HEARTBEAT_INTERVAL = 0.8  # segundos — por debajo del límite de 1s del robot


class RobotConnection:
    def __init__(self, ip: str = ROBOT_IP, port: int = ROBOT_PORT):
        self.ip = ip
        self.port = port
        self._sock: Optional[socket.socket] = None
        self._lock = threading.Lock()
        self._heartbeat_thread: Optional[threading.Thread] = None
        self._running = False

    def connect(self, retries: int = 3, retry_delay: float = 2.0) -> None:
        last_err: Exception = RuntimeError("No se intentó conectar")
        for attempt in range(1, retries + 1):
            try:
                self._sock = socket.create_connection((self.ip, self.port), timeout=5)
                self._sock.settimeout(0.3)
                self._running = True
                self._heartbeat_thread = threading.Thread(
                    target=self._heartbeat_loop, daemon=True
                )
                self._heartbeat_thread.start()
                return
            except (OSError, socket.timeout) as e:
                last_err = e
                print(f"[WARN] Intento {attempt}/{retries} fallido: {e}")
                if attempt < retries:
                    time.sleep(retry_delay)
        raise ConnectionError(
            f"No se pudo conectar a {self.ip}:{self.port} tras {retries} intentos. "
            f"¿Está el robot encendido y conectado por WiFi? Último error: {last_err}"
        )

    def disconnect(self) -> None:
        self._running = False
        if self._sock:
            try:
                self._sock.close()
            except OSError:
                pass
            self._sock = None

    @staticmethod
    def _encode(cmd: dict) -> bytes:
        return json.dumps(cmd, separators=(",", ":")).encode()

    def fire(self, cmd: dict) -> None:
        """Envía un comando JSON sin esperar respuesta (movimiento, servos, stop)."""
        payload = self._encode(cmd)
        print(f"[DEBUG send ] {payload}", flush=True)
        with self._lock:
            if not self._sock:
                raise RuntimeError("No hay conexión con el robot")
            self._sock.send(payload)

    def send(self, cmd: dict) -> Optional[str]:
        """Envía un comando JSON y espera respuesta (solo para consultas de sensores).
        Descarta los {Heartbeat} que el robot envía periódicamente."""
        payload = self._encode(cmd)
        print(f"[DEBUG send ] {payload}", flush=True)
        with self._lock:
            if not self._sock:
                raise RuntimeError("No hay conexión con el robot")
            self._sock.send(payload)
            try:
                while True:
                    resp = self._sock.recv(256)
                    decoded = resp.decode(errors="replace").strip()
                    if "{Heartbeat}" in decoded:
                        cleaned = decoded.replace("{Heartbeat}", "").strip()
                        if cleaned:
                            print(f"[DEBUG recv ] {cleaned!r}", flush=True)
                            return cleaned
                        # solo heartbeats, seguir leyendo
                        continue
                    print(f"[DEBUG recv ] {decoded!r}", flush=True)
                    return decoded
            except socket.timeout:
                print("[DEBUG recv ] timeout — sin respuesta", flush=True)
                return None

    def send_raw(self, raw: bytes) -> None:
        with self._lock:
            if self._sock:
                self._sock.send(raw)

    def _heartbeat_loop(self) -> None:
        while self._running:
            try:
                self.send_raw(b"{Heartbeat}")
            except Exception:
                pass
            time.sleep(HEARTBEAT_INTERVAL)

    def __enter__(self):
        self.connect()
        return self

    def __exit__(self, *_):
        self.disconnect()
