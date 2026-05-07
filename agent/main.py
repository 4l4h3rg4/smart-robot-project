"""
Modo interactivo del agente de robot.

Uso:
    cd agent/
    source .venv/bin/activate
    python main.py

Escribe comandos en lenguaje natural. Ejemplos:
    > ve adelante
    > gira a la izquierda
    > avanza 2 segundos y luego gira a la derecha
    > para
    > salir   ← cierra el programa
"""

import asyncio
import os
import warnings

warnings.filterwarnings("ignore")

from dotenv import load_dotenv
from google.adk.runners import Runner
from google.adk.sessions import InMemorySessionService
from google.genai import types as genai_types

from agent.agent import root_agent
from agent.robot_state import init_robot, shutdown_robot

load_dotenv()

EXIT_WORDS = {"salir", "exit", "quit", "q", "bye"}

BANNER = """
╔══════════════════════════════════════════╗
║   ELEGOO Smart Robot — Agente Gemini    ║
║   Escribe un comando o 'salir' para     ║
║   terminar.                             ║
╚══════════════════════════════════════════╝
"""


async def run_agent_turn(runner: Runner, session_id: str, text: str) -> None:
    content = genai_types.Content(
        role="user",
        parts=[genai_types.Part(text=text)],
    )
    async for event in runner.run_async(
        user_id="user",
        session_id=session_id,
        new_message=content,
    ):
        if event.content and event.content.parts:
            for part in event.content.parts:
                if hasattr(part, "text") and part.text:
                    print(f"\n[Robot] {part.text}\n")


async def main() -> None:
    robot_ip = os.getenv("ROBOT_IP", "192.168.4.1")

    print(BANNER)
    print(f"Conectando al robot en {robot_ip}...", end=" ", flush=True)
    try:
        init_robot(ip=robot_ip)
    except ConnectionError as e:
        print(f"\n\n✗ No se pudo conectar al robot:\n  {e}")
        print("\n⚠️  Pasos para solucionar:")
        print("   1. Verificar que el robot esté encendido")
        print("   2. Conectar la PC a la red WiFi 'ELEGOO-XXXXXXXXXXXXX'")
        print("   3. Verificar con: ping 192.168.4.1")
        print("   4. Volver a ejecutar: python main.py")
        return
    print("OK ✓\n")

    session_service = InMemorySessionService()
    runner = Runner(
        agent=root_agent,
        app_name="smart-robot-agent",
        session_service=session_service,
    )
    session = await session_service.create_session(
        app_name="smart-robot-agent",
        user_id="user",
    )

    try:
        while True:
            try:
                command = await asyncio.get_event_loop().run_in_executor(
                    None, lambda: input("Tú > ").strip()
                )
            except (EOFError, KeyboardInterrupt):
                print()
                break

            if not command:
                continue

            if command.lower() in EXIT_WORDS:
                break

            await run_agent_turn(runner, session.id, command)

    finally:
        print("Deteniendo robot y cerrando conexión...")
        shutdown_robot()
        print("Listo.")


if __name__ == "__main__":
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        pass  # salida limpia — el finally de main() ya hizo el shutdown
