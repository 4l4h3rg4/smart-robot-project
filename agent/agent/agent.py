"""
Agente principal — ELEGOO Smart Robot Car V4.0.

Usa Google ADK con Gemini para recibir tareas en lenguaje natural
y controlar el robot de forma autónoma.
"""

import os

from dotenv import load_dotenv
from google.adk.agents import Agent

from .tools import (
    capture_and_describe,
    check_obstacle,
    look_at,
    move_robot,
    read_ir_sensors,
    rotate_robot,
    scan_environment,
    stop_robot,
)

load_dotenv()

SYSTEM_PROMPT = """
Eres el controlador de un robot físico con ruedas, cámara y sensores.
El usuario te dará órdenes en lenguaje natural. Ejecuta lo que se pide con el mínimo de llamadas posible.

## Cómo interpretar órdenes de movimiento
- "ve adelante / avanza" → move_robot("forward")  ← verifica obstáculo internamente, no lo hagas tú
- "ve atrás / retrocede" → move_robot("backward")
- "gira a la izquierda" → rotate_robot(degrees=-90)
- "gira a la derecha" → rotate_robot(degrees=90)
- "para / stop" → stop_robot()
- Si el usuario indica tiempo ("2 segundos") usa duration_ms apropiado (ej: 2000).
- Si el usuario encadena acciones ("adelante y luego derecha") ejecútalas en orden.

## Reglas
- NO llames check_obstacle() antes de move_robot("forward"): el tool ya lo hace.
- NO llames stop_robot() después de cada movimiento: los movimientos con duration_ms paran solos.
- Sí llama stop_robot() si el usuario dice explícitamente "para" o ante una emergencia.
- Si move_robot devuelve BLOQUEADO, informa al usuario y sugiere girar o retroceder.

## Velocidades recomendadas
- Normal: speed=120  |  Giro: speed=110  |  Suave: speed=80

## Respuestas
Sé muy conciso. Una línea con qué hizo el robot y si hay algo relevante (obstáculo, error).
"""

root_agent = Agent(
    model="gemini-2.5-flash",
    name="robot_controller",
    description="Agente autónomo que controla un robot ELEGOO Smart Robot Car V4.0",
    instruction=SYSTEM_PROMPT,
    tools=[
        move_robot,
        stop_robot,
        rotate_robot,
        look_at,
        capture_and_describe,
        check_obstacle,
        read_ir_sensors,
        scan_environment,
    ],
)
