import os, time, threading, subprocess
from flask import Flask, render_template_string, request, jsonify

app = Flask(__name__)

bot_state = {
    "running": False,
    "auto_help": False,
    "auto_shield": False,
    "auto_mystery_box": False,
    "last_action": "Bot is idle. Waiting for command...",
    "last_shield_time": 0
}

COORDS = {
    "help": (1190, 560),
    "box": (1110, 620),
    "boosts": (1220, 210),
    "shield_tab": (900, 200),
    "use_shield": (1050, 380),
    "confirm": (640, 450)
}

def adb_tap(x, y, label=""):
    try:
        subprocess.run(["adb", "shell", "input", "tap", str(x), str(y)], check=False)
        bot_state["last_action"] = f"Tapped {label} ({x},{y}) at {time.strftime('%H:%M:%S')}"
    except Exception:
        bot_state["last_action"] = f"[Simulated] {label} ({x},{y}) at {time.strftime('%H:%M:%S')}"

def bot_worker():
    while True:
        if bot_state["running"]:
            now = time.time()
            if bot_state["auto_help"]:
                adb_tap(*COORDS["help"], "Guild Help")
                time.sleep(2)
            if bot_state["auto_mystery_box"]:
                adb_tap(*COORDS["box"], "Mystery Box")
                time.sleep(2)
            if bot_state["auto_shield"] and (now - bot_state["last_shield_time"]) >= 85600:
                adb_tap(*COORDS["boosts"], "Turf Boosts")
                time.sleep(2)
                adb_tap(*COORDS["shield_tab"], "Shield Tab")
                time.sleep(2)
                adb_tap(*COORDS["use_shield"], "Use 24h Shield")
                time.sleep(2)
                adb_tap(*COORDS["confirm"], "Confirm Shield")
                bot_state["last_shield_time"] = now
        time.sleep(5)

threading.Thread(target=bot_worker, daemon=True).start()

HTML_PAGE = '''<!DOCTYPE html>
<html>
<head>
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>Lords Web Bot</title>
<style>
body{font-family:sans-serif;background:#0f172a;color:#fff;padding:15px;margin:0}
.card{background:#1e293b;padding:15px;border-radius:10px;margin-bottom:15px}
.stat{background:#0f172a;padding:10px;border-radius:6px;color:#4ade80;font-family:monospace;margin-bottom:10px}
button{width:100%;padding:12px;border:none;border-radius:8px;font-weight:bold;color:#fff;margin-top:8px}
.on{background:#22c55e}.off{background:#ef4444}.act{background:#3b82f6}
.row{display:flex;justify-content:space-between;padding:8px 0;border-bottom:1px solid #334155}
input[type=number]{width:48%;padding:8px;background:#0f172a;color:#fff;border:1px solid #475569;border-radius:6px}
</style>
</head>
<body>
<div class="card">
<h3>Lords Mobile Web Bot</h3>
<div class="stat" id="st">Loading...</div>
<button class="on" onclick="up({running:true})">START BOT 24/7</button>
<button class="off" onclick="up({running:false})">STOP BOT</button>
</div>
<div class="card">
<div class="row"><span>Auto Guild Help</span><input type="checkbox" id="h" onchange="sv()"></div>
<div class="row"><span>Auto Mystery Box</span><input type="checkbox" id="m" onchange="sv()"></div>
<div class="row"><span>Auto 24h Shield</span><input type="checkbox" id="s" onchange="sv()"></div>
<button class="act" onclick="sh()">Trigger Shield Now</button>
</div>
<div class="card">
<input type="number" id="tx" placeholder="X (e.g. 1190)">
<input type="number" id="ty" placeholder="Y (e.g. 560)">
<button class="act" onclick="tp()">Tap Screen Coordinate</button>
</div>
<script>
async function load(){
let r=await fetch('/api/status'),d=await r.json();
document.getElementById('st').innerText=(d.running?"RUNNING | ":"STOPPED | ")+d.last_action;
document.getElementById('h').checked=d.auto_help;
document.getElementById('m').checked=d.auto_mystery_box;
document.getElementById('s').checked=d.auto_shield;
}
async function up(b){await fetch('/api/update',{method:'POST',headers:{'Content-Type':'application/json'},body:JSON.stringify(b)});load();}
function sv(){up({auto_help:document.getElementById('h').checked,auto_mystery_box:document.getElementById('m').checked,auto_shield:document.getElementById('s').checked});}
async function sh(){await fetch('/api/shield_now',{method:'POST'});load();}
async function tp(){await fetch('/api/tap',{method:'POST',headers:{'Content-Type':'application/json'},body:JSON.stringify({x:Number(document.getElementById('tx').value||640),y:Number(document.getElementById('ty').value||360)})});load();}
setInterval(load,3000);load();
</script>
</body>
</html>'''

@app.route("/")
def index():
    return render_template_string(HTML_PAGE)

@app.route("/api/status")
def status():
    return jsonify(bot_state)

@app.route("/api/update", methods=["POST"])
def update():
    data = request.json or {}
    for k in ["running", "auto_help", "auto_shield", "auto_mystery_box"]:
        if k in data:
            bot_state[k] = bool(data[k])
    return jsonify({"ok": True})

@app.route("/api/shield_now", methods=["POST"])
def shield_now():
    bot_state["last_shield_time"] = 0
    bot_state["auto_shield"] = True
    bot_state["running"] = True
    return jsonify({"ok": True})

@app.route("/api/tap", methods=["POST"])
def tap():
    data = request.json or {}
    adb_tap(data.get("x", 640), data.get("y", 360), "Custom Tap")
    return jsonify({"ok": True})

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=int(os.environ.get("PORT", 5000)))
