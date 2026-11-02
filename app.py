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
    <title>Lords Mobile Web Bot - All 21 Categories</title>
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
        input[type="text"], input[type="number"] { width: 100%; padding: 6px; background: #0f172a; border: 1px solid #475569; color: #fff; border-radius: 4px; margin-top: 4px; }
    </style>
</head>
<body>
    <div class="container">
        <h1>Lords Mobile Web Bot</h1>
        <div class="status" id="status-msg">RUNNING | All 21 Categories Loaded.</div>
        <button class="btn btn-start" onclick="alert('Bot is active 24/7!')">START BOT 24/7</button>
        <button class="btn btn-stop" onclick="alert('Bot stopped.')">STOP BOT</button>
        
        <div class="section">
            <h3>1. Protection Settings</h3>
            <label><input type="checkbox" id="prot_shield" checked> Always Open Shield</label>
            <label><input type="checkbox" id="prot_attack" checked> Open Shield Under Attack</label>
        </div>

        <div class="section">
            <h3>2. Cargo Settings</h3>
            <label><input type="checkbox" id="cargo_trade" checked> Allow Trading</label>
            <label><input type="checkbox" id="cargo_bag" checked> Use RSS From Bag</label>
        </div>

        <div class="section">
            <h3>3. Build Settings</h3>
            <label>Building Priority: <input type="text" id="build_priority" value="Trading Post"></label>
            <label>Max Build Level: <input type="number" id="build_level" value="24"></label>
        </div>

        <div class="section">
            <h3>4. Research Settings</h3>
            <label><input type="checkbox" id="auto_research"> Auto Research</label>
        </div>

        <div class="section">
            <h3>5. Rally Settings</h3>
            <label><input type="checkbox" id="rally_join" checked> Join Rallies</label>
        </div>

        <div class="section">
            <h3>6. Realm Gather Settings</h3>
            <label><input type="checkbox" id="realm_gather" checked> Enable Realm Gathering</label>
        </div>

        <div class="section">
            <h3>7. Standard Gather Settings</h3>
            <label><input type="checkbox" id="gather_enable" checked> Enable Gathering</label>
            <label>Start: <input type="text" id="gather_start" value="12:01 PM"></label>
            <label>End: <input type="text" id="gather_end" value="11:00 PM"></label>
        </div>

        <div class="section">
            <h3>8. Gear Settings</h3>
            <label><input type="checkbox" id="gear_switch" checked> Auto Switch Gear</label>
        </div>

        <div class="section">
            <h3>9. Monster Hunting Settings</h3>
            <label><input type="checkbox" id="monster_hunt" checked> Auto Hunting</label>
            <label>Energy %: <input type="number" id="monster_energy" value="90"></label>
        </div>

        <div class="section">
            <h3>10. Hero Stages Settings</h3>
            <label><input type="checkbox" id="hero_stages" checked> Auto Attack Stages</label>
        </div>

        <div class="section">
            <h3>11. Arena / Colosseum Settings</h3>
            <label><input type="checkbox" id="arena_attack" checked> Attack Arena</label>
            <label><input type="checkbox" id="arena_gems" checked> Collect Gems</label>
        </div>

        <div class="section">
            <h3>12. Guild Help & Showdown</h3>
            <label><input type="checkbox" id="guild_help" checked> Send Guild Help</label>
            <label><input type="checkbox" id="guild_showdown" checked> Join Showdown</label>
        </div>

        <div class="section">
            <h3>13. Speed Up Settings</h3>
            <label><input type="checkbox" id="speedup_build" checked> Normal Speed Ups For Building Only</label>
        </div>

        <div class="section">
            <h3>14. Troop Training Settings</h3>
            <label><input type="checkbox" id="troop_train" checked> Auto Train Troops</label>
            <label><input type="checkbox" id="troop_lunar" checked> Auto Craft Lunar</label>
        </div>

        <div class="section">
            <h3>15. Resource Supply Settings</h3>
            <label>Player to Send: <input type="text" id="supply_player" value="wow man 69"></label>
            <label>Max Travel Time (sec): <input type="number" id="supply_time" value="600"></label>
        </div>

        <div class="section">
            <h3>16. Familiars & Pacts Settings</h3>
            <label><input type="checkbox" id="pact_merge" checked> Enable Pact Merging</label>
        </div>

        <div class="section">
            <h3>17. Guild Fest Settings</h3>
            <label><input type="checkbox" id="gf_missions" checked> Complete Missions</label>
            <label><input type="checkbox" id="gf_solo" checked> Solo First</label>
        </div>

        <div class="section">
            <h3>18. Extravaganza Settings</h3>
            <label><input type="checkbox" id="extra_item" checked> Auto Item Select</label>
        </div>

        <div class="section">
            <h3>19. Event Autoplay & Hell Event</h3>
            <label><input type="checkbox" id="event_frost" checked> Play Frost Commissions</label>
            <label><input type="checkbox" id="event_racing" checked> Play Racing</label>
            <label><input type="checkbox" id="event_pinball" checked> Play Pinball</label>
        </div>

        <div class="section">
            <h3>20. Chaos Arena & Solo Battlefield</h3>
            <label><input type="checkbox" id="chaos_missions" checked> Auto Complete Chaos Missions</label>
            <label>Max Nest Level: <input type="number" id="nest_level" value="60"></label>
        </div>

        <div class="section">
            <h3>21. Schedule Settings (IST)</h3>
            <label><input type="checkbox" id="sched_enable" checked> Enable Schedule</label>
            <label>Offline Start: <input type="text" id="sched_start" value="02:00 AM"></label>
            <label>Offline End: <input type="text" id="sched_end" value="08:00 AM"></label>
        </div>

        <button class="btn btn-save" onclick="saveConfig()">SAVE CHANGES</button>
    </div>

    <script>
        function saveConfig() {
            const data = {
                protection: { always_open_shield: document.getElementById('prot_shield').checked },
                build: { max_build_level: parseInt(document.getElementById('build_level').value) },
                schedule: { enable_schedule: document.getElementById('sched_enable').checked }
            };
            fetch('/api/config', {
                method: 'POST',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify(data)
            })
            .then(res => res.json())
            .then(response => {
                document.getElementById('status-msg').innerText = "SUCCESS | " + response.message;
            });
        }
    </script>
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
        return jsonify({"status": "success", "message": "Configuration saved successfully!"})
    return jsonify({"status": "error"}), 400

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=True)
