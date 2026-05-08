"""
WebSocket — canal dúplex para comandos y streaming de estado en tiempo real.
"""

import json
import logging

from fastapi import APIRouter, WebSocket, WebSocketDisconnect

from web.state_manager import state

logger = logging.getLogger("web.ws")
router = APIRouter(prefix="/ws", tags=["websocket"])


@router.websocket("/")
async def ws_endpoint(ws: WebSocket):
    await ws.accept()
    await state.register_ws(ws)

    try:
        while True:
            raw = await ws.receive_text()
            try:
                msg = json.loads(raw)
            except json.JSONDecodeError:
                await ws.send_json({"type": "error", "data": {"message": "JSON inválido."}})
                continue

            msg_type = msg.get("type", "")
            data = msg.get("data", {})

            if msg_type == "command":
                text = data.get("text", "").strip()
                if text:
                    # Procesar en background para no bloquear el WS
                    import asyncio
                    asyncio.create_task(state.process_command(text))

            elif msg_type == "connect":
                ip = data.get("ip", "192.168.4.1")
                try:
                    result = await state.connect(ip)
                    await ws.send_json({"type": "connect_result", "data": {"ok": True, "message": result}})
                except Exception as e:
                    await ws.send_json({"type": "connect_result", "data": {"ok": False, "message": str(e)}})

            elif msg_type == "disconnect":
                result = await state.disconnect()
                await ws.send_json({"type": "disconnect_result", "data": {"ok": True, "message": result}})

            elif msg_type == "stop":
                result = await state.stop_robot()
                await ws.send_json({"type": "stop_result", "data": {"ok": True, "message": result}})

            elif msg_type == "poll_sensors":
                sensor_data = await state.poll_sensors()
                await ws.send_json({"type": "sensor_data", "data": sensor_data})

            elif msg_type == "ping":
                await ws.send_json({"type": "pong", "data": {}})

            elif msg_type == "face_detect":
                enabled = data.get("enabled", True)
                loop = asyncio.get_event_loop()
                ok = await loop.run_in_executor(None, state.toggle_face_detect, enabled)
                await ws.send_json({"type": "face_detect_result", "data": {"ok": ok, "enabled": enabled}})

            elif msg_type == "cam_led":
                intensity = data.get("intensity", 0)
                loop = asyncio.get_event_loop()
                ok = await loop.run_in_executor(None, state.set_cam_led, intensity)
                await ws.send_json({"type": "cam_led_result", "data": {"ok": ok, "intensity": intensity}})

            else:
                await ws.send_json({"type": "error", "data": {"message": f"Tipo desconocido: {msg_type}"}})

    except WebSocketDisconnect:
        pass
    except Exception as e:
        logger.warning(f"WS error: {e}")
    finally:
        await state.unregister_ws(ws)
