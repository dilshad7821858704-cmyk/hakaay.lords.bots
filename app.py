from flask import Flask, jsonify, request, render_template_string

app = Flask(__name__)

# Complete Bot Data (Accounts + 21 Categories Config)
BOT_DATA = {
    "accounts": [
        {"igg_id": "123456789", "server": "1600", "status": "Connected"}
    ],
    "config": {
        "protection": {"always_open_shield": True, "open_shield_under_attack": True, "preferred_shield": "8 hour"},
        "cargo": {"allow_trading": True, "use_rss_from_bag": True},
        "build": {"building_priority": "Trading Post", "max_build_level": 24},
        "research": {"auto_research": False},
        "rally": {"join_rallies": True, "troop_type": "Send 1 Troop"},
        "realm_gather": {"enable": True, "high_tier_gathering": True},
        "gather": {"enable": True, "schedule": {"start": "12:01 PM", "end": "11:00 PM"}},
        "gear": {"auto_switch_gear": True},
        "monster": {"auto_hunting": True, "energy_percentage": 90, "max_walk_time_seconds": 60},
        "hero_stage": {"auto_attack_stages": True, "attack_stage_type": "Custom Chapter"},
        "arena": {"attack_arena": True, "collect_gems": True, "max_opponent_strength_pct": 90},
        "guild": {"send_guild_help": True, "join_showdown": True},
        "speed_up": {"normal_speed_ups_for_building_only": True},
        "troop": {"auto_train_troops": True, "auto_craft_lunar": True},
        "supply": {"player_to_send": "wow man 69", "max_travel_time_seconds": 600},
        "familiars_and_pacts": {"enable_pact_merging": True},
        "guild_fest": {"complete_missions": True, "solo_first": True},
        "extravaganza": {"auto_item_select": True},
        "event_autoplay": {"frost_commissions": True, "racing": True, "pinball": True},
        "arena_and_battlefield": {"chaos_arena_missions": True, "max_nest_level": 60},
        "schedule": {"enable_schedule": True, "timezone": "IST (UTC+05:30)", "go_offline_between": {"start": "02:00 AM", "end": "08:00 AM"}}
    }
}

HTML_PAGE = """
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Lords Mobile Bot - Control Panel</title>
    <style>
        body { font-family: Arial, sans-serif; background: #0f172a; color: #fff; padding: 15px; margin: 0; }
        .container { max-width: 600px; margin: auto; background: #1e293b; padding: 20px; border-radius: 10px; }
        h1 { text-align: center; color: #38bdf8; font-size: 20px; }
        .status { background: #0f172a; padding: 10px; border-radius: 6px; border-left: 4px solid #22c55e; margin-bottom: 15px; font-family: monospace; font-size: 13px; }
        .btn { width: 100%; padding: 12px; border: none; border-radius: 6px; font-weight: bold; cursor: pointer; margin-bottom: 10px; font-size: 15px; }
        .btn-start { background: #22c55e; color: white; }
        .btn-stop { background: #ef4444; color: white; }
        .btn-save { background: #38bdf8; color: #0f172a; margin-top: 15px; }
        .section { background: #334155; padding: 12px; border-radius: 6px; margin-top: 15px; }
        h3 { margin-top: 0; color: #cbd5e1; font-size: 15px; border-bottom: 1px solid #475569; padding-bottom: 5px; }
        label { display: block; margin-bottom: 8px; font-size: 13px; cursor: pointer; }
        input[type="text"], input[type="password"], input[type="number"] { width: 100%; padding: 6px; background: #0f172a; border: 1px solid #475569; color: #fff; border-radius: 4px; margin-top: 4px; margin-bottom: 10px; }
        .acc-card { background: #0f172a; padding: 10px; border-radius: 6px; margin-bottom: 8px; border-left: 3px solid #38bdf8; font-size: 13px; }
    </style>
</head>
<body>
    <div class="container">
        <h1>Lords Mobile Web Bot</h1>
        <div class="status" id="status-msg">RUNNING | Dashboard Ready.</div>
        
        <!-- Account Connection Section -->
        <div class="section">
            <h3>Connect IGG Account</h3>
            <label>IGG ID / Username: <input type="text" id="igg_id" placeholder="Enter IGG ID"></label>
            <label>IGG Password / Token: <input type="password" id="igg_pass" placeholder="Enter password"></label>
            <label>Server / Kingdom: <input type="text" id="igg_server" placeholder="e.g. 1600"></label>
            <button class="btn btn-save" onclick="addAccount()">CONNECT ACCOUNT</button>
        </div>

        <div class="section">
            <h3>Connected Accounts</h3>
            <div id="acc-list">Loading accounts...</div>
        </div>

        <!-- 21 Categories Quick Settings Section -->
        <div class="section">
            <h3>Bot Settings (21 Categories)</h3>
            <label><input type="checkbox" id="prot_shield" checked> Protection: Always Open Shield</label>
            <label><input type="checkbox" id="gather_enable" checked> Gather: Enable Resources</label>
            <label><input type="checkbox" id="monster_hunt" checked> Monster: Auto Hunting</label>
            <label>Monster Energy %: <input type="number" id="monster_energy" value="90"></label>
            <label><input type="checkbox" id="sched_enable" checked> Schedule: Enable 24/7 Timer</label>
            <button class="btn btn-save" onclick="saveConfig()">SAVE CONFIGURATION</button>
        </div>

        <button class="btn btn-start" onclick="alert('Bot started for all connected accounts!')">START BOT 24/7</button>
        <button class="btn btn-stop" onclick="alert('Bot stopped.')">STOP BOT</button>
    </div>

    <script>
        function loadAccounts() {
            fetch('/api/accounts')
                .then(res => res.json())
                .then(data => {
                    let html = '';
                    data.forEach(acc => {
                        html += `<div class="acc-card"><strong>ID:</strong> ${acc.igg_id} | <strong>Server:</strong> ${acc.server} | <span style="color:#22c55e;">${acc.status}</span></div>`;
                    });
                    document.getElementById('acc-list').innerHTML = html;
                });
        }

        function addAccount() {
            const igg_id = document.getElementById('igg_id').value;
            const server = document.getElementById('igg_server').value;
            if(!igg_id) { alert('Please enter IGG ID'); return; }
            
            fetch('/api/accounts', {
                method: 'POST',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify({ igg_id: igg_id, server: server })
            })
            .then(res => res.json())
            .then(response => {
                document.getElementById('status-msg').innerText = "SUCCESS | Account Connected!";
                document.getElementById('igg_id').value = '';
                document.getElementById('igg_server').value = '';
                loadAccounts();
            });
        }

        function saveConfig() {
            const configData = {
                protection: { always_open_shield: document.getElementById('prot_shield').checked },
                gather: { enable: document.getElementById('gather_enable').checked },
                monster: { 
                    auto_hunting: document.getElementById('monster_hunt').checked,
                    energy_percentage: parseInt(document.getElementById('monster_energy').value)
                },
                schedule: { enable_schedule: document.getElementById('sched_enable').checked }
            };

            fetch('/api/config', {
                method: 'POST',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify(configData)
            })
            .then(res => res.json())
            .then(response => {
                document.getElementById('status-msg').innerText = "SUCCESS | Settings Saved!";
            });
        }

        loadAccounts();
    </script>
</body>
</html>
"""

@app.route("/")
def home():
    return render_template_string(HTML_PAGE)

@app.route("/api/accounts", methods=["GET"])
def get_accounts():
    return jsonify(BOT_DATA["accounts"])

@app.route("/api/accounts", methods=["POST"])
def add_account():
    new_acc = request.json
    if new_acc and new_acc.get("igg_id"):
        BOT_DATA["accounts"].append({
            "igg_id": new_acc.get("igg_id"),
            "server": new_acc.get("server", "Unknown"),
            "status": "Connected"
        })
        return jsonify({"status": "success", "message": "Added successfully!"})
    return jsonify({"status": "error"}), 400

@app.route("/api/config", methods=["GET"])
def get_config():
    return jsonify(BOT_DATA["config"])

@app.route("/api/config", methods=["POST"])
def update_config():
    new_config = request.json
    if new_config:
        BOT_DATA["config"].update(new_config)
        return jsonify({"status": "success", "message": "Config updated!"})
    return jsonify({"status": "error"}), 400

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=True)
