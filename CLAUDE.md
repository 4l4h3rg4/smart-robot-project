# Smart Robot Project — Contexto para Claude

## Qué es esto

Agente de IA que controla un **ELEGOO Smart Robot Car V4.0** (ESP32-WROVER) mediante lenguaje natural.
El usuario escribe comandos en español → Gemini los interpreta → Python envía JSON al robot vía TCP.

## Stack

| Capa | Tecnología |
|------|-----------|
| LLM / agente | Google ADK + Gemini 2.5 Flash |
| Control del robot | Python 3.11+ (TCP sockets) |
| Hardware | ESP32-WROVER, motores DC, servo cámara, ultrasonido, IR |
| Comunicación | TCP puerto 100, JSON, WiFi local |

## Estructura del proyecto

```
agent/
  agent/
    agent.py        ← define root_agent (Google ADK Agent)
    tools.py        ← funciones que el agente puede llamar
    robot_state.py  ← estado global (_conn, _ctrl) + init/shutdown
  robot/
    connection.py   ← TCP client + heartbeat thread
    controller.py   ← comandos de alto nivel (move, servo, sensores)
    camera.py       ← captura JPEG y stream MJPEG
  main.py           ← punto de entrada interactivo
  pyproject.toml
```

## Protocolo TCP del robot

- **IP:** `192.168.4.1` (AP del ESP32)
- **Puerto:** `100`
- **Formato:** JSON sin espacios, sin salto de línea. Ej: `{"N":3,"D1":3,"D2":120}`
- **Heartbeat obligatorio:** enviar `{Heartbeat}` cada < 1s o el robot se detiene
- **Timeout socket:** 0.3s para lecturas de sensores

### Comandos principales

| N | Descripción | Params extra |
|---|-------------|-------------|
| 2 | Movimiento temporizado (robot para solo) | D1=dirección, D2=speed, T=ms |
| 3 | Movimiento continuo (requiere stop manual) | D1=dirección, D2=speed |
| 5 | Mover servo | D1=servo (1=pan, 2=tilt), D2=ángulo 0-180 |
| 21 | Leer ultrasónico | D1=2 → respuesta `{1_XXXX}` donde XXXX=cm |
| 22 | Leer sensor IR | D1=0(left)/1(mid)/2(right) → respuesta `{1_X}` |
| 100 | Stop inmediato | — |
| 101 | Modo autónomo | D1=1(tracking)/2(obstacle)/3(follow) |

### Direcciones de movimiento

| Valor D1 | Dirección |
|----------|-----------|
| 1 | LEFT |
| 2 | RIGHT |
| 3 | FORWARD |
| 4 | BACKWARD |

### Servos

| D1 | Servo | Rango | Centro |
|----|-------|-------|--------|
| 1 | Pan (horizontal) | 0-180° | 90° |
| 2 | Tilt (vertical) | 0-180° | 90° |

## Google ADK — patrones importantes

- **`Agent`**: recibe `model`, `name`, `instruction`, `tools=[]`
- **`tools`**: funciones Python normales con docstrings descriptivos; ADK genera el schema automáticamente
- **`Runner`**: ejecuta el agente turno a turno con `run_async()`
- **`InMemorySessionService`**: sesión en memoria, se pierde al reiniciar
- Los tools deben devolver `str` o `dict` serializable; ADK lo convierte a texto para el LLM
- Gemini ve los nombres y docstrings de los tools — son críticos para que el agente decida qué llamar

## Cómo correr el proyecto

```bash
cd agent/
source .venv/bin/activate

# Con robot físico conectado por WiFi (red: ELEGOO-XXXXX)
python main.py

# Diagnóstico de conexión
python diagnose.py
```

## Testing sin robot físico

Para testear sin conectar al robot, mockear `RobotConnection`:

```python
from unittest.mock import MagicMock, patch
with patch("robot.connection.RobotConnection") as mock:
    mock.return_value.connect.return_value = None
    mock.return_value.fire.return_value = None
    # ... prueba tools aquí
```

## Velocidades recomendadas

| Uso | Speed |
|-----|-------|
| Normal | 120 |
| Giro | 110 |
| Suave | 80 |
| Máximo recomendado | 180 |

## Gotchas comunes

- **No romper el heartbeat**: cualquier operación que bloquee > 1s el hilo de heartbeat detiene el robot
- **N:2 auto-para**: si se usa `T=ms`, el robot se detiene solo; no hace falta enviar N:100 después
- **Lock compartido**: `_lock` en `RobotConnection` es compartido por heartbeat y lecturas de sensor — no hacer operaciones lentas dentro del lock
- **IR sensors**: actualmente 3 TCP round-trips separados para leer left/mid/right
- **Calibración de spin**: `SECONDS_PER_DEGREE = 0.0055` en controller.py es aproximado, calibrar empíricamente
- **Cámara separada**: la cámara usa HTTP (`/capture` y `:81/stream`), no el socket TCP del control

## Variables de entorno (.env)

```
ROBOT_IP=192.168.4.1          # IP del robot (AP mode)
GOOGLE_API_KEY=...             # API key de Google AI Studio
GEMINI_MODEL=gemini-2.5-flash  # modelo a usar
```
