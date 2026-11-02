from flask import Flask, jsonify, request, render_template_string
import threading
import time

app = Flask(__name__)

# Complete backend configuration structure tracking toggles and sub-settings
BOT_DATA = {
    "bot_running": False,
    "accounts": [{"igg_id": "123456789", "server": "1600", "status": "Connected"}],
    "config": {
        "protection": {"enabled": True, "always_open_shield": True, "open_shield_under_attack": True},
        "cargo": {"enabled": True, "allow_trading": True},
        "build": {"enabled": True, "max_build_level": 24},
        "research": {"enabled": False, "auto_research": False},
        "rally": {"enabled": True, "join_rallies": True},
        "realm_gather": {"enabled": True},
        "gather": {"enabled": True},
        "gear": {"enabled": True, "auto_switch_gear": True},
        "monster": {"enabled": True, "auto_hunting": True, "energy_percentage": 90},
        "hero_stage": {"enabled": True, "auto_attack_stages": True},
        "arena": {"enabled": True, "attack_arena": True, "collect_gems": True},
        "guild": {"enabled": True, "send_guild_help": True},
        "speed_up": {"enabled": True, "normal_speed_ups_for_building_only": True},
        "troop": {"enabled": True, "auto_train_troops": True},
        "supply": {"enabled": True, "player_to_send": "wow man 69"},
        "familiars_and_pacts": {"enabled": True, "enable_pact_merging": True},
        "guild_fest": {"enabled": True, "complete_missions": True},
        "extravaganza": {"enabled": True, "auto_item_select": True},
        "event_autoplay": {"enabled": True, "frost_commissions": True},
        "arena_and_battlefield": {"enabled": True, "max_nest_level": 60},
        "schedule": {"enabled": True, "enable_schedule": True}
    }
}

# Thread control event
stop_event = threading.Event()

def bot_worker_loop():
    """Background task simulator reading BOT_DATA config live."""
    print("[BOT ENGINE] Background Thread Started.")
    while not stop_event.is_set():
        if not BOT_DATA["bot_running"]:
            time.sleep(1)
            continue
            
        print("\n--- [BOT ENGINE] Running Automation Cycle ---")
        config = BOT_DATA["config"]
        
        # Check active status flags live from frontend variables
        if config["protection"]["enabled"] and config["protection"]["always_open_shield"]:
            print("[ACTION] Verification complete: Shield active.")
            
        if config["monster"]["enabled"] and config["monster"]["auto_hunting"]:
            thresh = config["monster"]["energy_percentage"]
            print(f"[ACTION] Searching monsters (Energy threshold target: >={thresh}%)")
            
        if config["build"]["enabled"]:
            max_lvl = config["build"]["max_build_level"]
            print(f"[ACTION] Upgrading production buildings up to Level {max_lvl}")
            
        if config["supply"]["enabled"]:
            target_player = config["supply"]["player_to_send"]
            print(f"[ACTION] Shipping resources to vault target account: {target_player}")

        # Sleep interval before repeating automation cycle
        time.sleep(5)
    print("[BOT ENGINE] Background Thread Safely Closed.")

HTML_PAGE = """
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Lords Mobile Web Bot - 21 Categories</title>
    <style>
        body { font-family: Arial, sans-serif; background: #0f172a; color: #fff; padding: 15px; margin: 0; }
        .container { max-width: 600px; margin: auto; background: #1e293b; padding: 20px; border-radius: 10px; }
        h1 { text-align: center; color: #38bdf8; font-size: 20px; }
        .status { background: #0f172a; padding: 10px; border-radius: 6px; border-left: 4px solid #ef4444; margin-bottom: 15px; font-family: monospace; font-size: 13px; transition: border 0.3s; }
        .btn { width: 100%; padding: 12px; border: none; border-radius: 6px; font-weight: bold; cursor: pointer; margin-bottom: 10px; font-size: 15px; }
        .btn-start { background: #22c55e; color: white; }
        .btn-stop { background: #ef4444; color: white; }
        .btn-save { background: #38bdf8; color: #0f172a; margin-top: 15px; }
        .section { background: #334155; padding: 12px; border-radius: 6px; margin-top: 15px; }
        h3 { margin-top: 0; color: #cbd5e1; font-size: 15px; border-bottom: 1px solid #475569; padding-bottom: 5px; }
        label { display: block; margin-bottom: 8px; font-size: 13px; cursor: pointer; }
        .sub-settings { background: #1e293b; padding: 10px; border-radius: 6px; margin-top: 5px; margin-bottom: 12px; padding-left: 15px; border-left: 2px solid #475569; }
        .sub-settings label { margin-bottom: 6px; color: #94a3b8; }
        input[type="text"], input[type="password"], input[type="number"] { width: 100%; padding: 6px; background: #0f172a; border: 1px solid #475569; color: #fff; border-radius: 4px; margin-top: 4px; margin-bottom: 10px; box-sizing: border-box; }
        .sub-settings input[type="text"], .sub-settings input[type="number"] { width: auto; display: inline-block; padding: 4px; margin-bottom: 0; margin-left: 5px; }
        .acc-card { background: #0f172a; padding: 10px; border-radius: 6px; margin-bottom: 8px; border-left: 3px solid #38bdf8; font-size: 13px; }
    </style>
</head>
<body>
    <div class="container">
        <h1>Lords Mobile Web Bot</h1>
        <div class="status" id="status-msg">STOPPED | Automated tasks offline.</div>
        
        <div class="section">
            <h3>Connect IGG Account</h3>
            <label>IGG ID / Username: <input type="text" id="igg_id" placeholder="Enter IGG ID"></label>
            <label>IGG Password / Token: <input type="password" id="igg_pass" placeholder="Enter password"></label>
            <label>Server / Kingdom: <input type="text" id="igg_server" placeholder="e.g. 1600"></label>
            <button class="btn btn-save" onclick="addAccount()">CONNECT ACCOUNT</button>
        </div>

        <div class="section">
            <h3>Connected Accounts</h3>
            <div id="acc-list">Loading...</div>
        </div>

        <div class="section">
            <h3>All 21 Categories Settings</h3>
            <form id="config-form">
                
                <label><input type="checkbox" name="protection.enabled"> 1. Protection</label>
                <div class="sub-settings">
                    <label><input type="checkbox" name="protection.always_open_shield"> Always Open Shield</label>
                    <label><input type="checkbox" name="protection.open_shield_under_attack"> Open Shield Under Attack</label>
                </div>

                <label><input type="checkbox" name="cargo.enabled"> 2. Cargo</label>
                <div class="sub-settings">
                    <label><input type="checkbox" name="cargo.allow_trading"> Allow Trading</label>
                </div>

                <label><input type="checkbox" name="build.enabled"> 3. Build</label>
                <div class="sub-settings">
                    <label>Max Build Level: <input type="number" name="build.max_build_level" min="1" max="25"></label>
                </div>

                <label><input type="checkbox" name="research.enabled"> 4. Research</label>
                <div class="sub-settings">
                    <label><input type="checkbox" name="research.auto_research"> Auto Research</label>
                </div>

                <label><input type="checkbox" name="rally.enabled"> 5. Rally</label>
                <div class="sub-settings">
                    <label><input type="checkbox" name="rally.join_rallies"> Join Rallies</label>
                </div>

                <label><input type="checkbox" name="realm_gather.enabled"> 6. Realm Gather</label>
                <label><input type="checkbox" name="gather.enabled"> 7. Gather</label>
                <label><input type="checkbox" name="gear.enabled"> 8. Gear</label>
                <div class="sub-settings">
                    <label><input type="checkbox" name="gear.auto_switch_gear"> Auto Switch Gear</label>
                </div>

                <label><input type="checkbox" name="monster.enabled"> 9. Monster Hunting</label>
                <div class="sub-settings">
                    <label><input type="checkbox" name="monster.auto_hunting"> Auto Hunting</label>
                    <label>Energy Threshold %: <input type="number" name="monster.energy_percentage" min="0" max="100"></label>
                </div>

                <label><input type="checkbox" name="hero_stage.enabled"> 10. Hero Stages</label>
                <div class="sub-settings">
                    <label><input type="checkbox" name="hero_stage.auto_attack_stages"> Auto Attack Stages</label>
                </div>

                <label><input type="checkbox" name="arena.enabled"> 11. Arena</label>
                <div class="sub-settings">
                    <label><input type="checkbox" name="arena.attack_arena"> Attack Arena</label>
                    <label><input type="checkbox" name="arena.collect_gems"> Collect Gems</label>
                </div>

                <label><input type="checkbox" name="guild.enabled"> 12. Guild Help</label>
                <div class="sub-settings">
                    <label><input type="checkbox" name="guild.send_guild_help"> Send Guild Help</label>
                </div>

                <label><input type="checkbox" name="speed_up.enabled"> 13. Speed Ups</label>
                <div class="sub-settings">
                    <label><input type="checkbox" name="speed_up.normal_speed_ups_for_building_only"> Building Only</label>
                </div>

                <label><input type="checkbox" name="troop.enabled"> 14. Troops</label>
                <div class="sub-settings">
