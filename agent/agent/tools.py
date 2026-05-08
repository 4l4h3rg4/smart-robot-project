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
    Mueve el robot físico. Para "forward" monitorea el sensor ultrasónico cada 0.3s
    durante TODO el movimiento y frena automáticamente si detecta obstáculo a < 25cm.

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
        result = ctrl.safe_forward(speed=speed, duration_s=duration_ms / 1000)
        if result.startswith("BLOQUEADO"):
            return result
        return f"Movimiento ejecutado: {direction} a velocidad {speed} durante {duration_ms}ms"

    direction_map = {
        "backward": ctrl.backward,
        "left": ctrl.turn_left,
        "right": ctrl.turn_right,
    }
    fn = direction_map.get(direction)
    if not fn:
        return f"ERROR: dirección desconocida '{direction}'. Usa: forward, backward, left, right"

    fn(speed=speed, duration_s=duration_ms / 1000)
    return f"Movimiento ejecutado: {direction} a velocidad {speed} durante {duration_ms}ms"


def move_distance(meters: float, speed: int = 120) -> str:
    """
    Avanza una distancia en metros, monitoreando obstáculos cada 0.3s.
    Se detiene automáticamente si detecta algo a menos de 25cm.
    Usar para órdenes como "avanza 2 metros" o "ve 1.5 metros adelante".

    Args:
        meters: distancia a avanzar en metros (ej: 2.0 = 2 metros)
        speed: velocidad 0-255 (default 120)

    Returns:
        "OK" si completó, o "BLOQUEADO a Xcm" si encontró obstáculo.
    """
    ctrl = get_controller()
    if not ctrl:
        return "ERROR: robot no conectado"
    distance_cm = int(meters * 100)
    return ctrl.forward_distance(distance_cm=distance_cm, speed=speed)


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


# ================================================================
#  Movimiento avanzado
# ================================================================

def move_diagonal(direction: str, speed: int = 120, duration_ms: int = 600) -> str:
    """
    Mueve el robot en diagonal usando 8 direcciones (joystick mode).
    Para maniobras finas o posicionamiento preciso.

    Args:
        direction: "left_forward", "right_forward", "left_backward", "right_backward"
        speed: velocidad 0-255
        duration_ms: duración en milisegundos

    Returns:
        Descripción de la acción ejecutada.
    """
    ctrl = get_controller()
    if not ctrl:
        return "ERROR: robot no conectado"
    try:
        ctrl.joystick_move(direction, speed)
        time.sleep(duration_ms / 1000)
        ctrl.stop()
        return f"Movimiento diagonal ejecutado: {direction} a velocidad {speed} durante {duration_ms}ms"
    except ValueError as e:
        return f"ERROR: {e}"


def arc_turn(direction: str, tightness: str = "medium", speed: int = 120,
             duration_ms: int = 800) -> str:
    """
    Giro en arco (curva suave) en vez de giro brusco sobre el eje.
    Más natural para navegación en espacios abiertos.

    Args:
        direction: "left" o "right"
        tightness: "tight" (cerrado), "medium", "wide" (amplio)
        speed: velocidad base
        duration_ms: duración en milisegundos

    Returns:
        Descripción de la acción ejecutada.
    """
    ctrl = get_controller()
    if not ctrl:
        return "ERROR: robot no conectado"
    radius_map = {"tight": 0.3, "medium": 0.6, "wide": 0.85}
    radius = radius_map.get(tightness, 0.6)
    ctrl.arc_turn(direction, radius, speed, duration_ms / 1000)
    return f"Giro en arco: {direction} ({tightness}) a velocidad {speed}"


# ================================================================
#  Sensores y seguridad
# ================================================================

def is_robot_lifted() -> dict:
    """
    Detecta si el robot fue levantado del suelo.
    Si es True, detener todo inmediatamente por seguridad.

    Returns:
        Dict con 'lifted' (bool) y mensaje descriptivo.
    """
    ctrl = get_controller()
    if not ctrl:
        return {"error": "robot no conectado"}
    lifted = ctrl.is_lifted()
    return {
        "lifted": lifted,
        "message": "ROBOT LEVANTADO DEL SUELO" if lifted else "Robot en el suelo",
    }


def set_line_tracking_sensitivity(threshold: int) -> str:
    """
    Ajusta la sensibilidad de seguimiento de línea para el modo tracking.
    Valores bajos = más sensible a líneas tenues.

    Args:
        threshold: 50 (muy sensible) a 1000 (poco sensible)

    Returns:
        Confirmación del ajuste.
    """
    ctrl = get_controller()
    if not ctrl:
        return "ERROR: robot no conectado"
    ctrl.set_tracking_sensitivity(threshold)
    return f"Sensibilidad de tracking ajustada a {threshold}"


def activate_autonomous_mode(mode: str) -> str:
    """
    Activa modos autónomos del firmware del robot.
    El robot ejecuta el modo por sí solo hasta que se le ordene parar.

    Args:
        mode: "tracking" (seguir línea negra), "obstacle" (evitar obstáculos),
              "follow" (seguir objeto/persona)

    Returns:
        Confirmación del modo activado.
    """
    ctrl = get_controller()
    if not ctrl:
        return "ERROR: robot no conectado"
    mode_map = {
        "tracking": ctrl.set_tracking_mode,
        "obstacle": ctrl.set_obstacle_mode,
        "follow": ctrl.set_follow_mode,
    }
    fn = mode_map.get(mode)
    if not fn:
        return f"ERROR: modo '{mode}' desconocido. Usa: tracking, obstacle, follow"
    fn()
    return f"Modo autónomo activado: {mode}"


# ================================================================
#  Cámara y visión
# ================================================================

def enable_face_detection(enabled: bool = True) -> str:
    """
    Activa o desactiva la detección de rostros integrada en la cámara ESP32.
    Cuando está activo, la cámara marca rectángulos en los rostros detectados.

    Args:
        enabled: True para activar, False para desactivar

    Returns:
        Confirmación del cambio.
    """
    from robot.camera import set_face_detect
    ok = set_face_detect(enabled)
    if ok:
        return f"Detección de rostros {'activada' if enabled else 'desactivada'}"
    return "ERROR: no se pudo cambiar la detección de rostros"


def toggle_camera_led(intensity: int = 0) -> str:
    """
    Controla el LED de la cámara. 0 = apagado, 255 = máximo brillo.
    Útil para exploración en baja luz o ahorro de batería.

    Args:
        intensity: 0-255

    Returns:
        Confirmación.
    """
    from robot.camera import set_led_intensity
    ok = set_led_intensity(intensity)
    return f"LED de cámara ajustado a {intensity}" if ok else "ERROR ajustando LED"


def set_camera_settings(quality: int = -1, brightness: int = 0,
                        contrast: int = 0) -> str:
    """
    Ajusta parámetros de la cámara para optimizar la visión.

    Args:
        quality: calidad JPEG 0-63 (-1 = no cambiar). Menor = mejor calidad.
        brightness: brillo -2 a 2
        contrast: contraste -2 a 2

    Returns:
        Resumen de cambios aplicados.
    """
    from robot.camera import set_camera_quality, set_camera_brightness, set_camera_contrast
    changes = []
    if quality >= 0:
        set_camera_quality(quality)
        changes.append(f"quality={quality}")
    if brightness != 0:
        set_camera_brightness(brightness)
        changes.append(f"brightness={brightness}")
    if contrast != 0:
        set_camera_contrast(contrast)
        changes.append(f"contrast={contrast}")
    return f"Cámara ajustada: {', '.join(changes)}" if changes else "Sin cambios"


def scan_and_analyze(question: str) -> dict:
    """
    Escanea el entorno rotando la cámara en 5 posiciones (0°→180°),
    capturando un frame en cada una. Devuelve frames codificados
    para que la IA los analice visualmente.

    Args:
        question: qué buscar o analizar en las imágenes

    Returns:
        Dict con lista de frames base64, sus ángulos pan, y la pregunta.
    """
    ctrl = get_controller()
    if not ctrl:
        return {"error": "robot no conectado"}

    frames = []
    for pan in [0, 45, 90, 135, 180]:
        ctrl.set_pan(pan)
        time.sleep(0.5)
        frame = capture_frame()
        b64 = base64.b64encode(frame_to_bytes(frame, format="JPEG")).decode()
        frames.append({"pan": pan, "image_base64": b64})

    ctrl.set_pan(90)
    return {"frames": frames, "question": question}


# ================================================================
#  Estado del robot
# ================================================================

def get_robot_status() -> dict:
    """
    Obtiene el estado completo del robot: batería estimada, sensores,
    cámara y estado de seguridad.

    Usar al inicio de cualquier tarea para verificar condiciones,
    o cuando el usuario pregunta "¿cómo está el robot?".

    Returns:
        Dict con todos los indicadores de estado.
    """
    ctrl = get_controller()
    if not ctrl:
        return {"error": "robot no conectado"}

    distance = ctrl.get_distance_cm()
    ir = ctrl.get_ir_sensors()
    battery = ctrl.estimate_battery_pct()
    lifted = ctrl.is_lifted()

    from robot.camera import get_camera_status
    cam_status = get_camera_status()

    return {
        "distance_cm": distance,
        "ir_sensors": ir,
        "battery": battery,
        "is_lifted": lifted,
        "camera": {
            "face_detect": cam_status.get("face_detect", 0) == 1,
            "quality": cam_status.get("quality", "?"),
            "led_intensity": cam_status.get("led_intensity", 0),
            "framesize": cam_status.get("framesize", "?"),
        },
    }
