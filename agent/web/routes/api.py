"""
API REST — endpoints síncronos y asíncronos para control del robot.
"""

import logging

from fastapi import APIRouter, HTTPException
from fastapi.responses import StreamingResponse

from web.state_manager import state

logger = logging.getLogger("web.api")
router = APIRouter(prefix="/api", tags=["api"])


# ------------------------------------------------------------
#  Conexión
# ------------------------------------------------------------

@router.post("/connect")
async def connect(ip: str = "192.168.4.1"):
    try:
        msg = await state.connect(ip)
        return {"ok": True, "message": msg}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.post("/disconnect")
async def disconnect():
    msg = await state.disconnect()
    return {"ok": True, "message": msg}


# ------------------------------------------------------------
#  Estado
# ------------------------------------------------------------

@router.get("/status")
def status():
    return state._build_state_payload()


@router.get("/activity")
def activity(limit: int = 50):
    log = state.activity_log[-limit:]
    return {"activity": log}


# ------------------------------------------------------------
#  Comandos
# ------------------------------------------------------------

@router.post("/command")
async def send_command(text: str):
    if not text.strip():
        raise HTTPException(status_code=400, detail="Texto vacío.")
    try:
        await state.process_command(text.strip())
        return {"ok": True, "message": "Comando procesado."}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.post("/stop")
async def stop():
    msg = await state.stop_robot()
    return {"ok": True, "message": msg}


# ------------------------------------------------------------
#  Cámara
# ------------------------------------------------------------

@router.get("/camera/snapshot")
def camera_snapshot():
    jpeg = state.capture_frame()
    if jpeg is None:
        raise HTTPException(status_code=503, detail="Cámara no disponible.")
    return StreamingResponse(
        iter([jpeg]),
        media_type="image/jpeg",
        headers={"Content-Disposition": "inline; filename=snapshot.jpg"},
    )


@router.get("/camera/stream")
async def camera_stream():
    import httpx

    if not state.connected:
        raise HTTPException(status_code=503, detail="Robot no conectado.")

    stream_url = f"http://{state.robot_ip}:81/stream"

    async def generate():
        async with httpx.AsyncClient(timeout=httpx.Timeout(30.0, connect=5.0)) as client:
            try:
                async with client.stream("GET", stream_url) as resp:
                    async for chunk in resp.aiter_bytes(chunk_size=8192):
                        yield chunk
            except Exception as e:
                logger.warning(f"Stream MJPEG caído: {e}")

    return StreamingResponse(
        generate(),
        media_type="multipart/x-mixed-replace; boundary=123456789000000000000987654321",
    )


# ------------------------------------------------------------
#  Sensores (poll manual)
# ------------------------------------------------------------

@router.get("/sensors")
async def sensors():
    if not state.connected:
        raise HTTPException(status_code=503, detail="Robot no conectado.")
    data = await state.poll_sensors()
    return {"ok": True, "data": data}
