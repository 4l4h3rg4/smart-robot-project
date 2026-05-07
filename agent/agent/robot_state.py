"""
Estado global de la conexión al robot.

Separado de tools.py para que init/shutdown sean importables desde main.py
sin arrastrar las dependencias de los tools del agente.
"""

from robot.connection import RobotConnection
from robot.controller import RobotController

_conn: RobotConnection | None = None
_ctrl: RobotController | None = None


def init_robot(ip: str = "192.168.4.1") -> None:
    global _conn, _ctrl
    _conn = RobotConnection(ip=ip)
    _conn.connect()
    _ctrl = RobotController(_conn)
    _ctrl.center_camera()


def shutdown_robot() -> None:
    global _conn, _ctrl
    if _ctrl:
        _ctrl.stop()
    if _conn:
        _conn.disconnect()
    _conn = None
    _ctrl = None


def get_controller() -> RobotController | None:
    return _ctrl
