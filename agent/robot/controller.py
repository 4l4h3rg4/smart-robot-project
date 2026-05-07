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

    # Calibración de velocidad (cm/s a speed=120 — ajustar empíricamente)
    CM_PER_SECOND_120 = 33
    OBSTACLE_SAFE_CM = 25
    OBSTACLE_CHECK_INTERVAL_S = 0.3  # cada cuánto verifica obstáculo en safe_forward

    def __init__(self, connection: RobotConnection):
        self.conn = connection

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
