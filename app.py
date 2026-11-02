import os
import random
import time
from flask import Flask, render_template_string, jsonify, request

app = Flask(__name__)

# Mock backend runtime state
system_state = {
    "status": "IDLE",
    "focus": "food",
    "guild_quests": True,
    "logs": ["[System Initialization Complete. Awaiting User Command...]"]
}

# The HTML dashboard interface compiled right inside the web app
HTML_TEMPLATE = """
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <title>Game Simulation Web Dashboard</title>
    <style>
        body { font-family: 'Segoe UI', sans-serif; background: #1e1e24; color: #fff; margin: 20px; }
        .container { max-width: 800px; margin: 0 auto; background: #2a2a35; padding: 20px; border-radius: 8px; box-shadow: 0 4px 15px rgba(0,0,0,0.5); }
        .controls { display: flex; gap: 15px; align-items: center; margin-bottom: 20px; }
        button { padding: 10px 20px; font-weight: bold; border: none; border-radius: 4px; cursor: pointer; }
        .btn-start { background: #28a745; color: white; }
        .btn-stop { background: #dc3545; color: white; }
        .status-bar { font-size: 16px; margin-left: 10px; }
        .log-panel { background: #111; border: 1px solid #444; height: 250px; padding: 12px; font-family: monospace; overflow-y: auto; border-radius: 4px; color: #0f0; margin-top: 15px; }
        .log-entry { margin-bottom: 5px; font-size: 13px; }
        .config-section { background: #333344; padding: 15px; border-radius: 6px; margin-bottom: 20px; }
        .param-group { margin-bottom: 12px; display: flex; align-items: center; gap: 15px; }
        select { padding: 6px; border-radius: 4px; background: #444; color: white; border: 1px solid #666; }
    </style>
</head>
<body>
<div class="container">
    <h2>Simulation Dashboard Web Interface</h2>
    
    <div class="config-section">
        <h3>Configuration Parameters</h3>
        <div class="param-group">
            <label>Priority Production Focus:</label>
            <select id="upgradeFocus">
                <option value="food">Food Focus</option>
                <option value="stone">Stone Focus</option>
                <option value="wood">Wood Focus</option>
                <option value="ore">Ore Focus</option>
            </select>
        </div>
    </div>

    <div class="controls">
        <button class="btn-start" onclick="toggleSystem('START')">START SYSTEM</button>
        <button class="btn-stop" onclick="toggleSystem('STOP')">STOP SYSTEM</button>
        <div class="status-bar">Status: <span id="statusText" style="color: #dc3545; font-weight: bold;">IDLE</span></div>
    </div>

    <h3>Live Action Telemetry Log</h3>
    <div id="logPanel" class="log-panel"></div>
</div>

<script>
    function toggleSystem(action) {
        const focusVal = document.getElementById('upgradeFocus').value;
        fetch('/api/control', {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({ action: action, focus: focusVal })
        })
        .then(res => res.json())
        .then(data => updateUI(data));
    }

    function updateUI(data) {
        const statusText = document.getElementById('statusText');
        statusText.textContent = data.status;
        statusText.style.color = data.status === 'RUNNING' ? '#28a745' : '#dc3545';
        
        const logPanel = document.getElementById('logPanel');
        logPanel.innerHTML = '';
        data.logs.forEach(log => {
            const div = document.createElement('div');
            div.className = 'log-entry';
            div.textContent = log;
            logPanel.appendChild(div);
        });
        logPanel.scrollTop = logPanel.scrollHeight;
    }

    // Long poll to continuously get logs updates every 2 seconds
    setInterval(() => {
        fetch('/api/state')
        .then(res => res.json())
        .then(data => updateUI(data));
    }, 2000);
</script>
</body>
</html>
"""

@app.route('/')
def home():
    return render_template_string(HTML_TEMPLATE)

@app.route('/api/state', methods=['GET'])
def get_state():
    # If system is active, generate fake periodic process tasks
    if system_state["status"] == "RUNNING" and random.random() > 0.4:
        timestamp = time.strftime("%H:%M:%S")
        simulated_tasks = [
            f"Checking background tiles for {system_state['focus'].upper()} production optimization...",
            "Parsing simulation queue logs...",
            "Simulating secure heartbeats to internal platform endpoints...",
            "Verifying data integrity configurations..."
        ]
        system_state["logs"].append(f"[{timestamp}] {random.choice(simulated_tasks)}")
        if len(system_state["logs"]) > 30: # Prevent log overflow
            system_state["logs"].pop(1)
    return jsonify(system_state)

@app.route('/api/control', methods=['POST'])
def control_system():
    req = request.get_json()
    action = req.get("action")
    focus = req.get("focus", "food")
    
    timestamp = time.strftime("%H:%M:%S")
    if action == "START":
        system_state["status"] = "RUNNING"
        system_state["focus"] = focus
        system_state["logs"].append(f"[{timestamp}] SYSTEM STATE CHANGED -> RUNNING (Focus: {focus.upper()})")
    else:
        system_state["status"] = "IDLE"
        system_state["logs"].append(f"[{timestamp}] SYSTEM STATE CHANGED -> IDLE (Halted by user request)")
        
    return jsonify(system_state)

if __name__ == '__main__':
    # Dynamically bind port for cloud platforms like Render
    port = int(os.environ.get("PORT", 5000))
    app.run(host='0.0.0.0', port=port)
