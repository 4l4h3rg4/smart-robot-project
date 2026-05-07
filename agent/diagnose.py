"""
Diagnóstico de conexión — ELEGOO Smart Robot Car V4.0
Uso: python diagnose.py [--ip 192.168.4.1]

Verifica 8 puntos antes de arrancar el agente.
"""

import importlib
import json
import os
import socket
import subprocess
import sys

from dotenv import load_dotenv

load_dotenv()


def check(n: int, total: int, label: str) -> None:
    print(f"[{n}/{total}] {label:<40}", end="", flush=True)


def ok(msg: str = "") -> None:
    print(f"✓  {msg}")


def fail(msg: str, hint: str = "") -> None:
    print(f"✗  {msg}")
    if hint:
        for line in hint.strip().splitlines():
            print(f"      → {line}")


TOTAL = 8


def main() -> int:
    ip = os.getenv("ROBOT_IP", "192.168.4.1")
    if len(sys.argv) >= 3 and sys.argv[1] == "--ip":
        ip = sys.argv[2]

    print("═" * 52)
    print("   ELEGOO Smart Robot — Diagnóstico de Conexión")
    print(f"   Robot IP: {ip}")
    print("═" * 52)

    errors = 0

    # 1. Variables de entorno
    check(1, TOTAL, "Variables de entorno (.env)...")
    api_key = os.getenv("GOOGLE_API_KEY", "")
    if not api_key:
        fail("GOOGLE_API_KEY no definida", "Agrégala en agent/.env")
        errors += 1
    else:
        masked = api_key[:8] + "..." + api_key[-4:]
        ok(f"GOOGLE_API_KEY={masked}, ROBOT_IP={ip}")

    # 2. Dependencias Python
    check(2, TOTAL, "Dependencias Python...")
    missing = []
    for pkg, import_name in [
        ("google-adk", "google.adk"),
        ("requests", "requests"),
        ("Pillow", "PIL"),
        ("python-dotenv", "dotenv"),
    ]:
        try:
            importlib.import_module(import_name)
        except ImportError:
            missing.append(pkg)
    if missing:
        fail(f"Faltan: {', '.join(missing)}", f"pip install {' '.join(missing)}")
        errors += 1
    else:
        ok("google-adk, requests, PIL, dotenv instalados")

    # 3. Ping al robot (informativo — ESP32 a veces no responde ICMP)
    check(3, TOTAL, f"Ping a {ip}...")
    try:
        result = subprocess.run(
            ["ping", "-c", "1", "-W", "2", ip],
            capture_output=True,
            timeout=5,
        )
        if result.returncode == 0:
            ok(f"{ip} responde")
        else:
            # No es error: muchos ESP32 no responden a ICMP pero sí a TCP
            print(f"⚠  {ip} no responde a ping (normal en algunos ESP32)")
    except Exception as e:
        print(f"⚠  Ping no disponible: {e}")

    # 4. Puerto TCP 100
    check(4, TOTAL, f"Puerto TCP {ip}:100...")
    sock = None
    try:
        sock = socket.create_connection((ip, 100), timeout=4)
        ok("Puerto 100 abierto")
    except Exception as e:
        fail(f"No se puede conectar al puerto 100: {e}", "Verifica que el robot esté encendido y en modo normal (no Upload)")
        errors += 1

    # 5. Heartbeat
    check(5, TOTAL, "Protocolo Heartbeat...")
    if sock:
        try:
            sock.settimeout(2)
            got_heartbeat = False
            for _ in range(3):
                sock.send(b"{Heartbeat}")
                try:
                    resp = sock.recv(256)
                    if b"Heartbeat" in resp:
                        got_heartbeat = True
                        break
                except socket.timeout:
                    pass
            if got_heartbeat:
                ok("Robot respondió {Heartbeat}")
            else:
                fail("Sin respuesta al Heartbeat tras 3 intentos",
                     "El robot podría estar en modo Upload (interruptor físico)\n"
                     "Pon el switch en posición 'Cam' y reinicia el robot")
                errors += 1
        except Exception as e:
            fail(f"Error: {e}")
            errors += 1
    else:
        fail("Saltado (sin conexión TCP)", "")
        errors += 1

    # 6. Comando STOP (seguro)
    check(6, TOTAL, "Comando STOP {N:100}...")
    if sock:
        try:
            cmd = json.dumps({"N": 100}, separators=(",", ":")).encode()
            sock.send(cmd)
            ok("Enviado sin error")
        except Exception as e:
            fail(f"Error al enviar: {e}")
            errors += 1
    else:
        fail("Saltado (sin conexión TCP)", "")
        errors += 1

    if sock:
        try:
            sock.close()
        except Exception:
            pass

    # 7. Puerto HTTP 80 (cámara)
    check(7, TOTAL, f"Puerto HTTP {ip}:80...")
    try:
        import requests as req
        r = req.get(f"http://{ip}/status", timeout=4)
        if r.status_code == 200:
            ok("Servidor web ESP32 activo")
        else:
            fail(f"Respuesta HTTP {r.status_code}")
            errors += 1
    except Exception as e:
        fail(f"No se puede alcanzar http://{ip}: {e}")
        errors += 1

    # 8. Endpoint /capture
    check(8, TOTAL, "Captura de cámara /capture...")
    try:
        import requests as req
        from PIL import Image
        import io
        r = req.get(f"http://{ip}/capture", timeout=5)
        if r.status_code == 200:
            img = Image.open(io.BytesIO(r.content))
            ok(f"Frame {img.width}×{img.height} recibido")
        else:
            fail(f"HTTP {r.status_code}")
            errors += 1
    except Exception as e:
        fail(f"Error: {e}")
        errors += 1

    # Resumen
    print("═" * 52)
    if errors == 0:
        print(" RESULTADO: TODO OK ✓  — puedes correr: python main.py")
    else:
        print(f" RESULTADO: {errors} problema(s) detectado(s). Corrige los ✗ arriba.")
    print("═" * 52)

    return errors


if __name__ == "__main__":
    sys.exit(main())
