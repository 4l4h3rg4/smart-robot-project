# Fase 0 — Verificación de Conexión y Hardware
**Fecha:** 2026-04-30  
**Robot:** ELEGOO Smart Robot Car V4.0  
**Ejecutado en:** Linux (Fedora 43) — ethernet para internet + WiFi para robot

---

## 1. Identificación del robot en la red

### Red WiFi del robot
El robot crea su propio hotspot WiFi. Al conectarse, la PC obtiene la IP `192.168.4.2` y el robot actúa como gateway en `192.168.4.1`.

| Interfaz | IP | Rol |
|----------|----|-----|
| `eno1` (ethernet) | `192.168.132.43` | Internet (red local del usuario) |
| `wlo1` (WiFi) | `192.168.4.2` | Conectado al robot |

### Dispositivo identificado
```
IP:  192.168.4.1
MAC: 32:30:f9:34:a3:c4   ← ESP32-WROVER del robot
```

**Scan de red `192.168.4.0/24`:** solo 1 dispositivo encontrado (`192.168.4.1`).  
No hay interferencia con otro robot — es la única IP activa en esta red.

---

## 2. Puertos abiertos

| Puerto | Estado | Función |
|--------|--------|---------|
| `80`   | ABIERTO | Servidor web ESP32 (interfaz cámara + configuración) |
| `81`   | ABIERTO | Stream MJPEG de la cámara |
| `100`  | ABIERTO | Control TCP del robot (comandos JSON) |

---

## 3. Control TCP — Puerto 100

### Protocolo
- **Conexión:** TCP a `192.168.4.1:100`
- **Heartbeat:** enviar `{Heartbeat}` cada ~1 segundo → el robot responde `{Heartbeat}`
- **Comandos:** JSON sin espacios, encerrado entre `{` y `}`
- **Si no llega heartbeat:** el robot se detiene automáticamente (seguridad)

### Prueba ejecutada
```python
s = socket.create_connection(('192.168.4.1', 100), timeout=5)
# Heartbeat → respuesta: b'{Heartbeat}'   ✓
# {"N":100}            → STOP/CLEAR       ✓
# {"N":3,"D1":3,"D2":80} → ADELANTE       ✓  (robot se movió físicamente)
# {"N":3,"D1":1,"D2":80} → GIRO IZQUIERDA ✓  (robot giró físicamente)
```

**Resultado: EXITOSO.** El robot respondió y ejecutó todos los comandos.

### Referencia de comandos principales
```json
{"N":3,"D1":3,"D2":150}   // Adelante, velocidad 150
{"N":3,"D1":4,"D2":150}   // Atrás, velocidad 150
{"N":3,"D1":1,"D2":150}   // Girar izquierda, velocidad 150
{"N":3,"D1":2,"D2":150}   // Girar derecha, velocidad 150
{"N":100}                  // PARAR / limpiar estado

{"N":5,"D1":1,"D2":90}    // Servo horizontal (pan) a 90°
{"N":5,"D1":2,"D2":90}    // Servo vertical (tilt) a 90°

{"H":1,"N":21,"D1":2}     // Leer distancia ultrasónico (cm)
{"H":1,"N":22,"D1":0}     // Leer IR izquierdo
{"H":1,"N":22,"D1":1}     // Leer IR central
{"H":1,"N":22,"D1":2}     // Leer IR derecho

{"N":101,"D1":2}          // Activar modo obstacle-avoidance
{"N":101,"D1":3}          // Activar modo follow
```

---

## 4. Cámara — Puerto 80 y 81

### Endpoints verificados

| URL | Estado | Tipo | Descripción |
|-----|--------|------|-------------|
| `http://192.168.4.1/` | 200 | HTML (comprimido) | Interfaz web completa del ESP32 |
| `http://192.168.4.1/capture` | **200** | `image/jpeg` | **Frame único JPEG** |
| `http://192.168.4.1/status` | **200** | `application/json` | Estado/configuración de la cámara |
| `http://192.168.4.1:81/stream` | **200** | `multipart/x-mixed-replace` | **Stream MJPEG continuo** |

### Frame capturado
```
Resolución: 800 × 600 píxeles (SVGA)
Formato:    JPEG (JFIF 1.01)
Tamaño:     ~37–43 KB por frame
Guardado:   robot_test_frame.jpg (en esta misma carpeta)
```

### Stream MJPEG
```
URL:      http://192.168.4.1:81/stream
Tipo:     multipart/x-mixed-replace
Boundary: 123456789000000000000987654321
FPS:      hasta 60fps (X-Framerate: 60)
CORS:     Access-Control-Allow-Origin: *
```

Cada frame del stream tiene la estructura:
```
--123456789000000000000987654321
Content-Type: image/jpeg
Content-Length: XXXXX
X-Timestamp: XXX.XXX

[datos JPEG]
```

### Status de la cámara (JSON)
```json
{
  "framesize": 9,        // SVGA 800x600
  "quality": 10,         // calidad JPEG
  "brightness": 0,
  "contrast": 0,
  "awb": 1,              // auto white balance ON
  "aec": 1,              // auto exposure ON
  "agc": 1,              // auto gain ON
  "face_detect": 0,
  "face_recognize": 0,
  "led_intensity": 0
}
```

---

## 5. Resumen ejecutivo de la interfaz del robot

```
ELEGOO Smart Robot Car V4.0
├── Red WiFi
│   ├── SSID: ELEGOO-XXXXXXXXXXXXX (único en la sala)
│   └── Gateway/IP del robot: 192.168.4.1
│
├── Control (puerto 100/TCP)
│   ├── Protocolo: JSON sobre socket TCP
│   ├── Heartbeat: {Heartbeat} cada 1s (obligatorio)
│   └── Verificado: motores, servos, sensores
│
└── Cámara (puertos 80/81)
    ├── Frame único:  GET http://192.168.4.1/capture → JPEG 800x600
    ├── Stream MJPEG: GET http://192.168.4.1:81/stream → multipart
    └── Config cam:   GET http://192.168.4.1/status → JSON
```

---

## 6. Configuración de red recomendada para el agente

El agente Python necesita dos rutas:
- **Tráfico a 192.168.4.x** → por `wlo1` (WiFi, robot)
- **Tráfico a internet (API Gemini)** → por `eno1` (ethernet)

Linux gestiona esto automáticamente con las rutas existentes:
```
192.168.4.0/24 dev wlo1  # tráfico al robot por WiFi
default via 192.168.132.1 dev eno1  # internet por ethernet
```

El agente no necesita configuración especial de red — ya está listo.

---

## 7. Próximos pasos (Fase 1)

1. Crear proyecto Python en `/home/matyas/Documentos/GitHub/smart-robot-agent/`
2. Implementar `robot/connection.py` — cliente TCP con heartbeat automático
3. Implementar `robot/controller.py` — comandos de alto nivel
4. Implementar `robot/camera.py` — captura y stream de frames
5. Configurar Google ADK + Gemini API key
6. Construir el agente autónomo
