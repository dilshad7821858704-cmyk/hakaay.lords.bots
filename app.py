import os
import time
import threading
import subprocess
from flask import Flask, render_template_string, request, jsonify

app = Flask(__name__)

# Bot State & Settings
bot_state = {
    "running": False,
    "auto_help": False,
    "auto_shield": False,
    "auto_mystery_box": False,
    "last_action": "Bot is idle. Waiting for command...",
    "shield_interval_hours": 24,
    "last_shield_time": 0
}

# Standard 1280x720 Android Screen Coordinates for Lords Mobile
COORDS = {
    "help_button": (1190, 560),      # Bottom-right Guild Help icon
    "mystery_box": (1110, 620),      # Bottom-right Mystery Box icon
    "turf_boosts": (1220, 210),      # Right-side Turf Boost button
    "shield_tab": (900, 200),        # Shield category inside Turf Boost
    "use_shield": (1050, 380),       # "Use" button on 24h Shield
    "confirm_btn": (640, 450)        # Confirm popup button
}

def adb_tap(x, y, label=""):
    """Sends a screen tap command to the Android game container."""
    try:
        subprocess.run(["adb", "shell", "input", "tap", str(x), str(y)], check=False)
        bot_state["last_action"] = f"Tapped {label} at ({x}, {y}) - {time.strftime('%H:%M:%S')}"
    except Exception:
        bot_state["last_action"] = f"[Simulated Tap] {label} at ({x}, {y}) - {time.strftime('%H:%M:%S')}"

def bot_worker():
    """24/7 Background loop that runs while the bot is turned ON."""
    while True:
        if bot_state["running"]:
            now = time.time()

            # 1. Auto Guild Help
            if bot_state["auto_help"]:
                x, y = COORDS["help_button"]
                adb_tap(x, y, "Guild Help")
                time.sleep(2)

            # 2. Auto Mystery Box
            if bot_state["auto_mystery_box"]:
                x, y = COORDS["mystery_box"]
                adb_tap(x, y, "Mystery Box")
                time.sleep(2)

            # 3. Auto Shield Timer Check
            if bot_state["auto_shield"]:
                hours_passed = (now - bot_state["last_shield_time"]) / 3600
                if hours_passed >= (bot_state["shield_interval_hours"] - 0.2):
                    adb_tap(*COORDS["turf_boosts"], "Open Turf Boosts")
                    time.sleep(2)
                    adb_tap(*COORDS["shield_tab"], "Select Shield Tab")
                    time.sleep(2)
                    adb_tap(*COORDS["use_shield"], "Use Shield")
                    time.sleep(2)
                    adb_tap(*COORDS["confirm_btn"], "Confirm Overwrite Shield")
                    bot_state["last_shield_time"] = now

        time.sleep(5)

# Start background thread
threading.Thread(target=bot_worker, daemon=True).start()

# Webpage HTML Template
HTML_PAGE = """
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Lords Mobile Cloud Bot Panel</title>
    <style>
        body { font-family: Arial, sans-serif; background: #0f172a; color: #f8fafc; margin: 0; padding: 15px; }
        .card { background: #1e293b; border-radius: 12px; padding: 16px; margin-bottom: 15px; box-shadow: 0 4px 6px rgba(0,0,0,0.3); }
        h2 { margin-top: 0; color: #38bdf8; font-size: 20px; }
        .status-box { background: #0f172a; padding: 12px; border-radius: 8px; font-family: monospace; color: #4ade80; margin-bottom: 12px; font-size: 13px; }
        .btn { width: 100%; padding: 12px; border: none; border-radius: 8px; font-weight: bold; font-size: 15px; margin-top: 8px; cursor: pointer; }
        .btn-start { background: #22c55e; color: #fff; }
        .btn-stop { background: #ef4444; color: #fff; }
        .btn-action { background: #3b82f6; color: #fff; }
        .toggle-row { display: flex; justify-content: space-between; align-items: center; padding: 10px 0; border-bottom: 1px solid #334155; }
        input[type="number"], input[type="text"] { width: 100%; padding: 10px; margin-top: 6px; border-radius: 6px; border: 1px solid #475569; background: #0f172a; color: white; box-sizing: border-box; }
    </style>
</head>
<body>

    <div class="card">
        <h2>⚔️ Lords Mobile Web Bot</h2>
        <div class="status-box" id="statusText">Loading status...</div>
        <button class="btn btn-start" onclick="toggleBot(true)">▶ START BOT 24/7</button>
        <button class="btn btn-stop" onclick="toggleBot(false)">⏹ STOP BOT</button>
    </div>

    <div class="card">
        <h2>⚙️ Auto Features</h2>
        <div class="toggle-row">
            <span>Auto Guild Help</span>
            <input type="checkbox" id="auto_help" onchange="saveSettings()">
        </div>
        <div class="toggle-row">
            <span>Auto Mystery Box</span>
            <input type="checkbox" id="auto_mystery_box" onchange="saveSettings()">
        </div>
        <div class="toggle-row">
            <span>Auto 24h Shield Renewal</span>
            <input type="checkbox" id="auto_shield" onchange="saveSettings()">
        </div>
        <button class="btn btn-action" onclick="instantShield()">🛡️ Trigger Shield Right Now</button>
    </div>

    <div class="card">
        <h2>🎯 Custom Screen Tap / Coordinate Test</h2>
        <input type="number" id="tapX" placeholder="Screen X (e.g. 1190)">
        <input type="number" id="tapY" placeholder="Screen Y (e.g. 560)">
        <button class="btn btn-action" onclick="customTap()">Tap Screen Coordinate</button>
    </div>

    <script>
