from flask import Flask, jsonify, request, render_template_string

app = Flask(__name__)

BOT_CONFIG = {
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

HTML_PAGE = """
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Lords Mobile Web Bot - Control Panel</title>
    <style>
        body { font-family: Arial, sans-serif; background: #0f172a; color: #fff; padding: 15px; margin: 0; }
        .container { max-width: 600px; margin: auto; background: #1e293b; padding: 20px; border-radius: 10px; }
        h1 { text-align: center; color: #38bdf8; font-size: 20px; }
        .status { background: #0f172a; padding: 10px; border-radius: 6px; border-left: 4px solid #22c55e; margin-bottom: 15px; font-family: monospace; font-size: 13px; }
        .btn { width: 100%; padding: 12px; border: none; border-radius: 6px; font-weight: bold; cursor: pointer; margin-bottom: 10px; font-size: 15px; }
        .btn-start { background: #22c55e; color: white; }
        .btn-stop { background: #ef4444; color: white; }
        .section { background: #334155; padding: 12px; border-radius: 6px; margin-top: 15px; }
        h3 { margin-top: 0; color: #cbd5e1; font-size: 15px; border-bottom: 1px solid #475569; padding-bottom: 5px; }
        label { display: block; margin-bottom: 8px; font-size: 13px; cursor: pointer; }
        input[type="text"], input[type="number"] { width: 100%; padding: 6px; background: #0f172a; border: 1px solid #475569; color: #fff; border-radius: 4px; margin-top: 4px; }
    </style>
</head>
<body>
    <div class="container">
        <h1>Lords Mobile Web Bot</h1>
        <div class="status">RUNNING | 21 Categories Active.</div>
        <button class="btn btn-start" onclick="alert('Bot is active 24/7!')">START BOT 24/7</button>
        <button class="btn btn-stop" onclick="alert('Bot stopped.')">STOP BOT</button>
        
        <div class="section">
            <h3>1. Protection Settings</h3>
            <label><input type="checkbox" id="always_open_shield" checked> Always Open Shield</label>
            <label><input type="checkbox" id="open_shield_under_attack" checked> Open Shield Under Attack</label>
        </div>

        <div class="section">
            <h3>7. Gather Settings</h3>
            <label><input type="checkbox" id="gather_enable" checked> Enable Resource Gathering</label>
            <label>Start Time: <input type="text" id="gather_start" value="12:01 PM"></label>
            <label>End Time: <input type="text" id="gather_end" value="11:00 PM"></label>
        </div>

        <div class="section">
            <h3>9. Monster Settings</h3>
            <label><input type="checkbox" id="auto_hunting" checked> Auto Hunting</label>
            <label>Energy Percentage: <input type="number" id="energy_percentage" value="90"></label>
        </div>

        <div class="section">
            <h3>21. Schedule Settings (IST)</h3>
            <label><input type="checkbox" id="enable_schedule" checked> Enable Schedule</label>
            <label>Offline Start: <input type="text" id="offline_start" value="02:00 AM"></label>
            <label>Offline End: <input type="text" id="offline_end" value="08:00 AM"></label>
        </div>
    </div>
</body>
</html>
"""

@app.route("/")
def home():
    return render_template_string(HTML_PAGE)

@app.route("/api/config", methods=["GET"])
def get_config():
    return jsonify(BOT_CONFIG)

@app.route("/api/config", methods=["POST"])
def update_config():
    global BOT_CONFIG
    new_data = request.json
    if new_data:
        BOT_CONFIG.update(new_data)
        return jsonify({"status": "success", "message": "Updated successfully!"})
    return jsonify({"status": "error"}), 400

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=True)
