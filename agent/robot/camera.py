"""
Acceso a la cámara del ESP32-WROVER del robot.

Dos modos:
- capture_frame(): GET /capture → JPEG único (simple, bajo overhead)
- MjpegStream: lee el stream continuo de :81/stream
"""

import io
import os
import threading
import time
from typing import Optional

import requests
from PIL import Image


ROBOT_IP = os.getenv("ROBOT_IP", "192.168.4.1")
CAPTURE_URL = f"http://{ROBOT_IP}/capture"
STREAM_URL = f"http://{ROBOT_IP}:81/stream"
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
                    time.sleep(1)  # reconectar
