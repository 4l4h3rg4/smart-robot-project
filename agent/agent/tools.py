"""
Herramientas que el agente Gemini puede invocar para controlar el robot.

Cada función es un tool ADK: recibe parámetros simples (str/int/float),
ejecuta acciones en el robot, y devuelve un string descriptivo del resultado.
"""

import base64
import time

from robot.camera import capture_frame, frame_to_bytes

from .robot_state import get_controller

OBSTACLE_THRESHOLD_CM = 25


def move_robot(direction: str, speed: int = 120, duration_ms: int = 600) -> str:
    """
    Mueve el robot físico. Para movimientos hacia adelante verifica automáticamente
    que no haya obstáculos antes de moverse.

    Args:
        direction: "forward", "backward", "left" o "right"
        speed: velocidad 0-255 (recomendado 80-180)
        duration_ms: tiempo de movimiento en milisegundos

    Returns:
        Descripción de la acción ejecutada o motivo por el que no se movió.
    """
    ctrl = get_controller()
    if not ctrl:
        return "ERROR: robot no conectado"

    if direction == "forward":
        dist = ctrl.get_distance_cm()
        if dist < OBSTACLE_THRESHOLD_CM:
            return (
                f"BLOQUEADO: obstáculo a {dist}cm al frente (mínimo {OBSTACLE_THRESHOLD_CM}cm). "
                "No se ejecutó el movimiento."
            )

    direction_map = {
        "forward": ctrl.forward,
        "backward": ctrl.backward,
        "left": ctrl.turn_left,
        "right": ctrl.turn_right,
    }
    fn = direction_map.get(direction)
    if not fn:
        return f"ERROR: dirección desconocida '{direction}'. Usa: forward, backward, left, right"

    fn(speed=speed, duration_s=duration_ms / 1000)
    return f"Movimiento ejecutado: {direction} a velocidad {speed} durante {duration_ms}ms"


def stop_robot() -> str:
    """Para el robot inmediatamente. Usar solo en emergencia o al final de una secuencia larga."""
    ctrl = get_controller()
    if not ctrl:
        return "ERROR: robot no conectado"
    ctrl.stop()
    return "Robot detenido"


def rotate_robot(degrees: int, speed: int = 110) -> str:
    """
    Rota el robot en el lugar.

    Args:
        degrees: grados a rotar. Positivo = derecha, negativo = izquierda.
        speed: velocidad de rotación 0-255

    Returns:
        Descripción de la acción.
    """
    ctrl = get_controller()
    if not ctrl:
        return "ERROR: robot no conectado"
    ctrl.spin(degrees=degrees, speed=speed)
    return f"Rotación ejecutada: {degrees}° a velocidad {speed}"


def look_at(pan: int = 90, tilt: int = 90) -> str:
    """
    Mueve los servos de la cámara.

    Args:
        pan: ángulo horizontal 0-180 (0=izquierda, 90=centro, 180=derecha)
        tilt: ángulo vertical 0-180 (0=abajo, 90=centro, 180=arriba)

    Returns:
        Confirmación del movimiento.
    """
    ctrl = get_controller()
    if not ctrl:
        return "ERROR: robot no conectado"
    ctrl.set_pan(pan)
    time.sleep(0.3)
    ctrl.set_tilt(tilt)
    return f"Cámara posicionada: pan={pan}°, tilt={tilt}°"


def capture_and_describe(question: str) -> dict:
    """
    Captura un frame de la cámara y lo devuelve codificado en base64
    para que el agente pueda analizarlo visualmente.

    Args:
        question: pregunta o contexto para guiar el análisis (solo informativo)

    Returns:
        Dict con 'image_base64' (JPEG en base64) y 'question'.
    """
    frame = capture_frame()
    jpeg_bytes = frame_to_bytes(frame, format="JPEG")
    b64 = base64.b64encode(jpeg_bytes).decode()
    return {
        "image_base64": b64,
        "width": frame.width,
        "height": frame.height,
        "question": question,
    }


def check_obstacle() -> dict:
    """
    Lee el sensor ultrasónico y devuelve la distancia al obstáculo más cercano.
    Útil para consultar la distancia sin intentar moverse.

    Returns:
        Dict con 'distance_cm' y 'is_blocked' (True si < 25cm).
    """
    ctrl = get_controller()
    if not ctrl:
        return {"error": "robot no conectado"}
    dist = ctrl.get_distance_cm()
    return {
        "distance_cm": dist,
        "is_blocked": dist < OBSTACLE_THRESHOLD_CM,
    }


def read_ir_sensors() -> dict:
    """
    Lee los 3 sensores infrarrojo del robot (útil para detección de líneas o bordes).

    Returns:
        Dict con valores de los sensores 'left', 'mid', 'right'.
    """
    ctrl = get_controller()
    if not ctrl:
        return {"error": "robot no conectado"}
    return ctrl.get_ir_sensors()


def scan_environment() -> str:
    """
    Rota la cámara en 5 posiciones (0°, 45°, 90°, 135°, 180°) para reconocer el entorno.
    Usar al inicio de tareas de búsqueda o exploración.

    Returns:
        Mensaje indicando que el escaneo se completó.
    """
    ctrl = get_controller()
    if not ctrl:
        return "ERROR: robot no conectado"
    positions = [0, 45, 90, 135, 180]
    for pan in positions:
        ctrl.set_pan(pan)
        time.sleep(0.5)
    ctrl.set_pan(90)
    return f"Escaneo completado: {len(positions)} posiciones revisadas (pan 0°→180°→90°)"
