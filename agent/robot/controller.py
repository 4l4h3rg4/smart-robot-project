"""
Comandos de alto nivel para el robot.

Todos los métodos son bloqueantes por la duración indicada y luego paran.
El heartbeat corre en segundo plano en RobotConnection.
"""

import time

from .connection import RobotConnection


class RobotController:
    # Direcciones según firmware ELEGOO (ApplicationFunctionSet_xxx0.cpp enum)
    FORWARD = 3
    BACKWARD = 4
    LEFT = 1
    RIGHT = 2

    # Servos
    SERVO_PAN = 1   # horizontal (izquierda/derecha)
    SERVO_TILT = 2  # vertical (arriba/abajo)

    # Joystick 8 direcciones (N:102)
    JOYSTICK = {
        "forward": 1,
        "backward": 2,
        "left": 3,
        "right": 4,
        "left_forward": 5,
        "left_backward": 6,
        "right_forward": 7,
        "right_backward": 8,
    }

    # Control individual de motor (N:1)
    MOTOR_ALL = 0
    MOTOR_LEFT = 1
    MOTOR_RIGHT = 2
    MOTOR_CLOCKWISE = 1
    MOTOR_COUNTERCLOCKWISE = 2

    # Rotación cámara suave (N:106)
    CAMERA_UP = 1
    CAMERA_DOWN = 2
    CAMERA_LEFT = 3
    CAMERA_RIGHT = 4

    # Calibración de velocidad (cm/s a speed=120 — ajustar empíricamente)
    CM_PER_SECOND_120 = 33
    OBSTACLE_SAFE_CM = 25
    OBSTACLE_CHECK_INTERVAL_S = 0.3

    # Batería — valores estimados (ajustar según mediciones reales)
    BATTERY_FULL_VOLTAGE = 8.4
    BATTERY_LOW_VOLTAGE = 6.8
    BATTERY_CRITICAL_VOLTAGE = 6.0
    MOTOR_CURRENT_AVG = 800
    IDLE_CURRENT = 200
    BATTERY_CAPACITY_MAH = 2200

    def __init__(self, connection: RobotConnection):
        self.conn = connection
        self._movement_seconds: float = 0.0
        self._init_time: float = time.monotonic()

    # --- Movimiento ---

    def stop(self) -> None:
        self.conn.fire({"N": 100})

    def move(self, direction: int, speed: int = 150, duration_s: float = 0) -> None:
        """Mueve el robot. Si duration_s > 0, usa modo N:2 (timed, Arduino maneja el stop).
        Si duration_s == 0, usa N:3 (continuo hasta recibir stop)."""
        if duration_s > 0:
            duration_ms = int(duration_s * 1000)
            self.conn.fire({"N": 2, "D1": direction, "D2": speed, "T": duration_ms})
        else:
            self.conn.fire({"N": 3, "D1": direction, "D2": speed})
        self.track_battery_usage(movement=True, seconds=duration_s)

    def forward(self, speed: int = 150, duration_s: float = 0) -> None:
        self.move(self.FORWARD, speed, duration_s)

    def backward(self, speed: int = 150, duration_s: float = 0) -> None:
        self.move(self.BACKWARD, speed, duration_s)

    def turn_left(self, speed: int = 150, duration_s: float = 0) -> None:
        self.move(self.LEFT, speed, duration_s)

    def turn_right(self, speed: int = 150, duration_s: float = 0) -> None:
        self.move(self.RIGHT, speed, duration_s)

    def spin(self, degrees: int, speed: int = 120) -> None:
        """Gira aproximadamente `degrees` grados en el lugar.
        Calibrado empíricamente: ~1 segundo ≈ 180° a speed=120.
        Ajustar SECONDS_PER_DEGREE según el robot real.
        """
        SECONDS_PER_DEGREE = 0.0055  # calibrar en pruebas
        duration_s = abs(degrees) * SECONDS_PER_DEGREE
        direction = self.RIGHT if degrees > 0 else self.LEFT
        self.move(direction, speed, duration_s)

    # --- Movimiento diferencial (N:4) ---

    def differential_drive(self, left_speed: int, right_speed: int) -> None:
        """Control independiente de ruedas. Curvas precisas y arcos suaves."""
        self.conn.fire({"N": 4, "D1": left_speed, "D2": right_speed})

    # --- Joystick 8 direcciones (N:102) ---

    def joystick_move(self, direction: str, speed: int = 150) -> None:
        """Movimiento en 8 direcciones."""
        d1 = self.JOYSTICK.get(direction)
        if d1 is None:
            raise ValueError(f"Dirección inválida: {direction}. Usa: {list(self.JOYSTICK.keys())}")
        self.conn.fire({"N": 102, "D1": d1, "D2": speed})

    # --- Control individual de motor (N:1) ---

    def set_motor(self, motor: int, speed: int, motor_direction: int) -> None:
        """Control granular de un solo motor."""
        self.conn.fire({"N": 1, "D1": motor, "D2": speed, "D3": motor_direction})

    # --- Giro en arco (wrapper sobre N:4) ---

    def arc_turn(self, direction: str, radius: float, speed: int = 120,
                 duration_s: float = 0) -> None:
        """Giro en arco. radius=0.0 = giro en el lugar, 1.0 = arco amplio."""
        inner_speed = int(speed * radius)
        outer_speed = speed
        if direction == "left":
            self.differential_drive(inner_speed, outer_speed)
        else:
            self.differential_drive(outer_speed, inner_speed)
        if duration_s > 0:
            time.sleep(duration_s)
            self.stop()

    # --- Movimiento seguro con monitoreo de obstáculos ---

    def safe_forward(self, speed: int = 120, duration_s: float = 0.6) -> str:
        """Avanza monitoreando el ultrasónico durante el movimiento.
        Divide el tiempo en tramos cortos. Si detecta obstáculo, frena
        inmediatamente y devuelve la distancia. Retorna 'OK' si completó."""
        interval = self.OBSTACLE_CHECK_INTERVAL_S
        remaining = duration_s

        while remaining > 0:
            dist = self.get_distance_cm()
            if dist < self.OBSTACLE_SAFE_CM:
                self.stop()
                return f"BLOQUEADO a {dist}cm"

            chunk = min(interval, remaining)
            self.move(self.FORWARD, speed, chunk)
            time.sleep(chunk)
            remaining -= chunk

        return "OK"

    def forward_distance(self, distance_cm: int, speed: int = 120) -> str:
        """Avanza una distancia aproximada en cm, monitoreando obstáculos.
        Convierte cm → tiempo usando CM_PER_SECOND_120 calibrado."""
        cm_per_s = self.CM_PER_SECOND_120 * (speed / 120)
        duration_s = distance_cm / cm_per_s
        return self.safe_forward(speed=speed, duration_s=duration_s)

    # --- Servo cámara ---

    def set_pan(self, angle: int) -> None:
        """Servo horizontal. 0=izquierda, 90=centro, 180=derecha."""
        angle = max(0, min(180, angle))
        self.conn.fire({"N": 5, "D1": self.SERVO_PAN, "D2": angle})

    def set_tilt(self, angle: int) -> None:
        """Servo vertical. 0=abajo, 90=centro, 180=arriba."""
        angle = max(0, min(180, angle))
        self.conn.fire({"N": 5, "D1": self.SERVO_TILT, "D2": angle})

    def center_camera(self) -> None:
        self.set_pan(90)
        self.set_tilt(90)

    # --- Sensores ---

    def get_distance_cm(self) -> int:
        """Distancia del ultrasónico en cm. Devuelve 999 si no hay respuesta."""
        resp = self.conn.send({"H": 1, "N": 21, "D1": 2})
        if resp and resp.startswith("{") and "}" in resp:
            # Respuesta típica: {1_XXXX} donde XXXX es la distancia
            try:
                value = resp.strip("{}").split("_")[-1]
                return int(value)
            except (ValueError, IndexError):
                pass
        return 999

    def get_ir_sensors(self) -> dict:
        """Lee los 3 sensores IR. Devuelve {'left': v, 'mid': v, 'right': v}."""
        result = {}
        for key, d1 in [("left", 0), ("mid", 1), ("right", 2)]:
            resp = self.conn.send({"H": 1, "N": 22, "D1": d1})
            try:
                value = resp.strip("{}").split("_")[-1] if resp else "0"
                result[key] = int(value)
            except (ValueError, AttributeError):
                result[key] = 0
        return result

    def is_obstacle_near(self, threshold_cm: int = 25) -> bool:
        return self.get_distance_cm() < threshold_cm

    # --- Seguridad y sensores adicionales ---

    def is_lifted(self) -> bool:
        """Detecta si el robot fue levantado del suelo (N:23)."""
        resp = self.conn.send({"H": 1, "N": 23})
        if resp and "true" in resp.lower():
            return True
        return False

    def set_tracking_sensitivity(self, threshold: int) -> None:
        """Ajusta sensibilidad de line-tracking (N:104). Rango 50-1000."""
        threshold = max(50, min(1000, threshold))
        self.conn.fire({"N": 104, "D1": threshold})

    # --- Cámara suave (N:106) ---

    def camera_rotate(self, direction: int) -> None:
        """Rotación continua de cámara. Usar CAMERA_UP/DOWN/LEFT/RIGHT."""
        self.conn.fire({"N": 106, "D1": direction})

    # --- Modo programación (N:110) ---

    def clear_programming_mode(self) -> None:
        """Limpia todos los estados. Más completo que N:100 (stop)."""
        self.conn.fire({"N": 110})

    # --- Batería (estimación por runtime) ---

    def track_battery_usage(self, movement: bool, seconds: float) -> None:
        """Registra consumo para estimación de batería.
        Solo se trackea movimiento explícitamente; idle se calcula como
        tiempo total transcurrido - tiempo de movimiento en estimate_battery_pct."""
        if movement:
            self._movement_seconds += seconds

    def estimate_battery_pct(self) -> dict:
        """Estima porcentaje de batería basado en tiempo de uso acumulado."""
        total_elapsed = time.monotonic() - self._init_time
        idle_s = max(0, total_elapsed - self._movement_seconds)
        mah_used = (
            (self.MOTOR_CURRENT_AVG * self._movement_seconds / 3600) +
            (self.IDLE_CURRENT * idle_s / 3600)
        )
        pct = max(0, 100 - (mah_used / self.BATTERY_CAPACITY_MAH * 100))
        if pct > 30:
            status = "ok"
        elif pct > 15:
            status = "low"
        else:
            status = "critical"
        return {
            "percentage": round(pct, 1),
            "status": status,
            "movement_minutes": round(self._movement_seconds / 60, 1),
            "idle_minutes": round(idle_s / 60, 1),
        }

    # --- Modos autónomos del firmware ---

    def set_obstacle_mode(self) -> None:
        """Activa el modo obstacle-avoidance del firmware del robot."""
        self.conn.fire({"N": 101, "D1": 2})

    def set_follow_mode(self) -> None:
        """Activa el modo follow del firmware del robot."""
        self.conn.fire({"N": 101, "D1": 3})

    def set_tracking_mode(self) -> None:
        """Activa el modo line-tracking del firmware del robot."""
        self.conn.fire({"N": 101, "D1": 1})
