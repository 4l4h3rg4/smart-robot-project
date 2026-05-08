/**
 * Smart Robot Monitor — Dashboard JS
 *
 * Gestiona WebSocket, UI reactiva, cámara y comandos.
 */

(function () {
  'use strict';

  // --- DOM refs ---
  const ipInput = document.getElementById('ip-input');
  const btnConnect = document.getElementById('btn-connect');
  const btnDisconnect = document.getElementById('btn-disconnect');
  const btnSend = document.getElementById('btn-send');
  const cmdInput = document.getElementById('command-input');
  const statusBadge = document.getElementById('connection-status');
  const cameraFeed = document.getElementById('camera-feed');
  const cameraPlaceholder = document.getElementById('camera-placeholder');
  const activityLog = document.getElementById('activity-log');
  const wsStatus = document.getElementById('ws-status');
  const lastUpdate = document.getElementById('last-update');

  // Sensor displays
  const sensorDistance = document.getElementById('sensor-distance');
  const sensorIrLeft = document.getElementById('sensor-ir-left');
  const sensorIrMid = document.getElementById('sensor-ir-mid');
  const sensorIrRight = document.getElementById('sensor-ir-right');
  const servoPan = document.getElementById('servo-pan');
  const servoTilt = document.getElementById('servo-tilt');

  // --- State ---
  let ws = null;
  let reconnectTimer = null;
  let connected = false;

  // ============================================================
  //  WebSocket
  // ============================================================
  function connectWS() {
    if (ws && ws.readyState !== WebSocket.CLOSED) return;

    const protocol = location.protocol === 'https:' ? 'wss:' : 'ws:';
    const url = `${protocol}//${location.host}/ws/`;

    ws = new WebSocket(url);

    ws.onopen = function () {
      setWsState(true);
      clearTimeout(reconnectTimer);
      // Solicitar estado inicial
      sendWS({ type: 'ping', data: {} });
    };

    ws.onclose = function () {
      setWsState(false);
      reconnectTimer = setTimeout(connectWS, 3000);
    };

    ws.onerror = function () {
      ws.close();
    };

    ws.onmessage = function (event) {
      let msg;
      try {
        msg = JSON.parse(event.data);
      } catch (e) {
        return;
      }
      handleMessage(msg);
    };
  }

  function sendWS(payload) {
    if (ws && ws.readyState === WebSocket.OPEN) {
      ws.send(JSON.stringify(payload));
    }
  }

  function setWsState(online) {
    wsStatus.className = online ? 'ws-on' : 'ws-off';
    wsStatus.textContent = online ? '●' : '●';
  }

  // ============================================================
  //  Message handler
  // ============================================================
  function handleMessage(msg) {
    const data = msg.data || {};
    updateTimestamp();

    switch (msg.type) {
      case 'robot_state':
        updateStateUI(data);
        break;

      case 'agent_text':
        addActivity('agent', data.text);
        break;

      case 'tool_call':
        addActivity('tool_call', `${data.name}(${JSON.stringify(data.args)})`);
        break;

      case 'tool_result':
        addActivity('tool_result', `${data.name}: ${data.result}`);
        break;

      case 'agent_error':
        addActivity('system', 'ERROR: ' + data.message);
        break;

      case 'command_complete':
        addActivity('system', 'Comando completado.');
        break;

      case 'connect_result':
        if (data.ok) {
          setConnected(true);
          addActivity('system', data.message);
        } else {
          addActivity('system', 'Error: ' + data.message);
        }
        break;

      case 'disconnect_result':
        setConnected(false);
        addActivity('system', data.message);
        break;

      case 'stop_result':
        addActivity('system', data.message);
        break;

      case 'sensor_data':
        updateSensorUI(data);
        break;

      case 'pong':
        break;

      case 'error':
        addActivity('system', 'Error: ' + (data.message || 'Desconocido'));
        break;
    }
  }

  // ============================================================
  //  UI updates
  // ============================================================
  function updateStateUI(data) {
    setConnected(data.connected);
    updateSensorUI(data);
    servoPan.textContent = data.servo_pan !== undefined ? data.servo_pan : '--';
    servoTilt.textContent = data.servo_tilt !== undefined ? data.servo_tilt : '--';
    updateBatteryUI(data);
    updateStatusBadges(data);
  }

  function updateBatteryUI(data) {
    const bar = document.getElementById('battery-bar');
    const text = document.getElementById('battery-text');
    if (data.battery_pct !== undefined && data.battery_pct !== null) {
      const pct = data.battery_pct;
      bar.style.width = pct + '%';
      text.textContent = pct + '%';
      if (data.battery_status === 'critical') {
        bar.style.background = '#ef4444';
        text.style.color = '#ef4444';
      } else if (data.battery_status === 'low') {
        bar.style.background = '#f59e0b';
        text.style.color = '#f59e0b';
      } else {
        bar.style.background = '#22c55e';
        text.style.color = '#22c55e';
      }
    } else {
      bar.style.width = '100%';
      bar.style.background = '#374151';
      text.textContent = '--';
      text.style.color = '#9ca3af';
    }
  }

  function updateStatusBadges(data) {
    const fdBadge = document.getElementById('face-detect-badge');
    if (data.face_detect_enabled) {
      fdBadge.className = 'badge on';
      fdBadge.textContent = '👤 Face: ON';
    } else {
      fdBadge.className = 'badge off';
      fdBadge.textContent = '👤 Face: OFF';
    }

    const groundBadge = document.getElementById('ground-badge');
    if (data.is_lifted) {
      groundBadge.className = 'badge danger';
      groundBadge.textContent = '⚠️ LEVANTADO';
    } else {
      groundBadge.className = 'badge ok';
      groundBadge.textContent = '📐 En suelo';
    }
  }

  function updateSensorUI(data) {
    if (data.distance_cm !== undefined && data.distance_cm !== null) {
      sensorDistance.textContent = data.distance_cm;
    } else {
      sensorDistance.textContent = '--';
    }
    sensorIrLeft.textContent = data.ir_left !== undefined && data.ir_left !== null ? data.ir_left : '--';
    sensorIrMid.textContent = data.ir_mid !== undefined && data.ir_mid !== null ? data.ir_mid : '--';
    sensorIrRight.textContent = data.ir_right !== undefined && data.ir_right !== null ? data.ir_right : '--';
  }

  function setConnected(state) {
    connected = state;
    btnConnect.disabled = state;
    btnDisconnect.disabled = !state;
    cmdInput.disabled = !state;
    btnSend.disabled = !state;

    if (state) {
      statusBadge.className = 'status-badge connected';
      statusBadge.querySelector('.label').textContent = 'Conectado';
      cameraFeed.src = '/api/camera/stream';
      cameraFeed.classList.remove('hidden');
      cameraPlaceholder.style.display = 'none';
    } else {
      statusBadge.className = 'status-badge disconnected';
      statusBadge.querySelector('.label').textContent = 'Desconectado';
      cameraFeed.src = '';
      cameraFeed.classList.add('hidden');
      cameraPlaceholder.style.display = 'flex';
      // Limpiar sensores
      sensorDistance.textContent = '--';
      sensorIrLeft.textContent = '--';
      sensorIrMid.textContent = '--';
      sensorIrRight.textContent = '--';
      servoPan.textContent = '--';
      servoTilt.textContent = '--';
    }
  }

  function addActivity(kind, message) {
    const div = document.createElement('div');
    div.className = 'activity-entry';

    const now = new Date();
    const time = now.toLocaleTimeString('es-ES', { hour: '2-digit', minute: '2-digit', second: '2-digit' });
    const timeSpan = document.createElement('span');
    timeSpan.className = 'activity-time';
    timeSpan.textContent = time;

    const kindSpan = document.createElement('span');
    kindSpan.className = 'activity-kind ' + kind;
    kindSpan.textContent = kind === 'tool_call' ? 'TOOL' : kind === 'tool_result' ? 'RESULT' : kind.toUpperCase();

    div.appendChild(timeSpan);
    div.appendChild(kindSpan);
    div.appendChild(document.createTextNode(message));

    // Eliminar placeholder si existe
    const empty = activityLog.querySelector('.activity-empty');
    if (empty) empty.remove();

    activityLog.appendChild(div);
    activityLog.scrollTop = activityLog.scrollHeight;

    // Limitar a 200 entradas
    while (activityLog.children.length > 200) {
      activityLog.firstChild.remove();
    }
  }

  function updateTimestamp() {
    const now = new Date();
    lastUpdate.textContent = now.toLocaleTimeString('es-ES');
  }

  // ============================================================
  //  Actions
  // ============================================================
  function doConnect() {
    const ip = ipInput.value.trim() || '192.168.4.1';
    sendWS({ type: 'connect', data: { ip } });
  }

  function doDisconnect() {
    sendWS({ type: 'disconnect', data: {} });
  }

  function doSendCommand() {
    const text = cmdInput.value.trim();
    if (!text) return;
    addActivity('user', text);
    sendWS({ type: 'command', data: { text } });
    cmdInput.value = '';
  }

  function doStop() {
    sendWS({ type: 'stop', data: {} });
  }

  // ============================================================
  //  Event listeners
  // ============================================================
  btnConnect.addEventListener('click', doConnect);
  btnDisconnect.addEventListener('click', doDisconnect);
  btnSend.addEventListener('click', doSendCommand);

  cmdInput.addEventListener('keydown', function (e) {
    if (e.key === 'Enter') {
      e.preventDefault();
      doSendCommand();
    }
  });

  // Quick action buttons
  document.querySelectorAll('.quick-btn').forEach(function (btn) {
    btn.addEventListener('click', function () {
      if (!connected) return;
      const cmd = this.dataset.cmd;
      if (cmd) {
        addActivity('user', cmd);
        sendWS({ type: 'command', data: { text: cmd } });
      }
    });
  });

  // Quick stop button
  document.querySelector('.quick-stop')?.addEventListener('click', function () {
    doStop();
  });

  // ============================================================
  //  Init
  // ============================================================
  connectWS();

  // Auto-conectar al cargar (intento rápido)
  setTimeout(function () {
    if (!connected && ws && ws.readyState === WebSocket.OPEN) {
      const ip = ipInput.value.trim() || '192.168.4.1';
      // No auto-conectar, esperar a que el usuario lo haga
    }
  }, 1000);
})();
