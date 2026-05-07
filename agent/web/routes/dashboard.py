"""
Rutas del dashboard — sirve la SPA y assets estáticos.
"""

from pathlib import Path

from fastapi import APIRouter, Request
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates

router = APIRouter(tags=["dashboard"])

_templates_dir = str(Path(__file__).resolve().parent.parent / "templates")
templates = Jinja2Templates(directory=_templates_dir)


@router.get("/", response_class=HTMLResponse)
async def dashboard(request: Request):
    return templates.TemplateResponse("index.html", {"request": request})
