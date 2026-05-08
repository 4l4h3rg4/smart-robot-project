"""
Acceso a la cámara del ESP32-WROVER del robot.

Modos:
- capture_frame(): GET /capture → JPEG único
- MjpegStream: stream MJPEG continuo (:81/stream)
- Control: face_detect, quality, led_intensity vía /control
- Status: estado completo de la cámara vía /status
"""

import io
import logging
import os
import threading
import time
from typing import Optional

import requests
from PIL import Image


logger = logging.getLogger("robot.camera")
ROBOT_IP = os.getenv("ROBOT_IP", "192.168.4.1")
CAPTURE_URL = f"http://{ROBOT_IP}/capture"
STREAM_URL = f"http://{ROBOT_IP}:81/stream"
CONTROL_URL = f"http://{ROBOT_IP}/control"
STATUS_URL = f"http://{ROBOT_IP}/status"
STREAM_BOUNDARY = b"123456789000000000000987654321"


def capture_frame(ip: str = ROBOT_IP, timeout: float = 5.0) -> Image.Image:
    """Captura un frame único de la cámara. Devuelve un objeto PIL.Image."""
    url = f"http://{ip}/capture"
    resp = requests.get(url, timeout=timeout)
    resp.raise_for_status()
    return Image.open(io.BytesIO(resp.content))


def frame_to_bytes(frame: Image.Image, format: str = "JPEG") -> bytes:
    buf = io.BytesIO()
    frame.save(buf, format=format)
    return buf.getvalue()


class MjpegStream:
    """
    Lee el stream MJPEG del robot en un thread de fondo.
    El frame más reciente siempre está disponible en `.latest_frame`.
    """

    def __init__(self, ip: str = ROBOT_IP):
        self.url = f"http://{ip}:81/stream"
        self.latest_frame: Optional[Image.Image] = None
        self._running = False
        self._thread: Optional[threading.Thread] = None

    def start(self) -> None:
        self._running = True
        self._thread = threading.Thread(target=self._read_loop, daemon=True)
        self._thread.start()

    def stop(self) -> None:
        self._running = False

    def get_frame(self) -> Optional[Image.Image]:
        return self.latest_frame

    def _read_loop(self) -> None:
        while self._running:
            try:
                with requests.get(self.url, stream=True, timeout=10) as resp:
                    resp.raise_for_status()
                    buffer = b""
                    for chunk in resp.iter_content(chunk_size=4096):
                        if not self._running:
                            break
                        buffer += chunk
                        # Buscar inicio y fin de frame JPEG
                        start = buffer.find(b"\xff\xd8")
                        end = buffer.find(b"\xff\xd9")
                        if start != -1 and end != -1 and end > start:
                            jpeg = buffer[start : end + 2]
                            buffer = buffer[end + 2 :]
                            try:
                                self.latest_frame = Image.open(io.BytesIO(jpeg))
                                self.latest_frame.load()
                            except Exception:
                                pass
            except Exception:
                if self._running:
                    time.sleep(1)


# ------------------------------------------------------------
#  Control de cámara (ESP32 /control endpoint)
# ------------------------------------------------------------

def _camera_control(var: str, val: int, ip: str = ROBOT_IP) -> bool:
    """Envía un comando de control a la cámara del ESP32."""
    try:
        url = f"http://{ip}/control"
        resp = requests.get(url, params={"var": var, "val": val}, timeout=3)
        return resp.status_code == 200
    except Exception as e:
        logger.warning(f"Camera control '{var}={val}' falló: {e}")
        return False


def set_face_detect(enabled: bool = True, ip: str = ROBOT_IP) -> bool:
    """Activa/desactiva detección de rostros en el ESP32."""
    return _camera_control("face_detect", 1 if enabled else 0, ip)


def set_face_recognize(enabled: bool = True, ip: str = ROBOT_IP) -> bool:
    """Activa/desactiva reconocimiento facial en el ESP32."""
    return _camera_control("face_recognize", 1 if enabled else 0, ip)


def set_camera_quality(quality: int, ip: str = ROBOT_IP) -> bool:
    """Ajusta calidad JPEG (0-63, menor = mejor calidad)."""
    quality = max(0, min(63, quality))
    return _camera_control("quality", quality, ip)


def set_camera_brightness(brightness: int, ip: str = ROBOT_IP) -> bool:
    """Ajusta brillo de cámara (-2 a 2)."""
    brightness = max(-2, min(2, brightness))
    return _camera_control("brightness", brightness, ip)


def set_camera_contrast(contrast: int, ip: str = ROBOT_IP) -> bool:
    """Ajusta contraste de cámara (-2 a 2)."""
    contrast = max(-2, min(2, contrast))
    return _camera_control("contrast", contrast, ip)


def set_camera_framesize(framesize: int, ip: str = ROBOT_IP) -> bool:
    """Ajusta resolución. 9=SVGA(800x600), 10=XGA(1024x768), etc."""
    return _camera_control("framesize", framesize, ip)


def set_led_intensity(intensity: int, ip: str = ROBOT_IP) -> bool:
    """Controla intensidad del LED de flash (0-255)."""
    intensity = max(0, min(255, intensity))
    return _camera_control("led_intensity", intensity, ip)


def get_camera_status(ip: str = ROBOT_IP) -> dict:
    """Obtiene estado completo de la cámara (face_detect, quality, etc.)."""
    try:
        resp = requests.get(f"http://{ip}/status", timeout=3)
        resp.raise_for_status()
        return resp.json()
    except Exception as e:
        logger.warning(f"Error obteniendo status de cámara: {e}")
        return {}
