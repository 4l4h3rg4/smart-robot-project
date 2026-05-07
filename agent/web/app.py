"""
FastAPI application factory para la plataforma web de monitoreo del robot.
"""

from pathlib import Path

from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles

from web.routes import api, dashboard, ws

# Resolver ruta a static/ — funciona tanto en dev como instalado
_base = Path(__file__).resolve().parent

app = FastAPI(
    title="Smart Robot Monitor",
    description="Plataforma de monitoreo y control para ELEGOO Smart Robot Car V4.0",
    version="1.0.0",
)

app.mount("/static", StaticFiles(directory=str(_base / "static")), name="static")

app.include_router(dashboard.router)
app.include_router(api.router)
app.include_router(ws.router)


@app.on_event("shutdown")
async def shutdown_event():
    from web.state_manager import state as s

    if s.connected:
        await s.disconnect()
