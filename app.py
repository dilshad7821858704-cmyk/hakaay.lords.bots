from flask import Flask, jsonify, request

app = Flask(__name__)

# Aapki poori bot configuration jo screenshots se li gayi hai
BOT_CONFIG = {
    "protection": {
        "always_open_shield": True,
        "open_shield_under_attack": True,
        "open_shield_scouted": True,
        "open_shield_rallied": True,
        "always_anti_scout": True,
        "anti_scout_when_scouted": False,
        "preferred_shield": "8 hour",
        "dont_shield_with_prisoner": True,
        "auto_execute": False,
    },
    "cargo": {
        "allow_trading": True,
        "trade_resources": {"food": True, "stone": True, "wood": True, "ore": True, "gold": True},
        "ignore": {"food": False, "stone": False, "wood": False, "ore": False, "gold": False, "anima": False, "lunite": False, "speed_up": False},
        "exchange_rss_item_only": False,
        "use_rss_from_bag": True,
    },
    "build": {
        "auto_build": False,
        "auto_upgrade": False,
        "build_by_lowest_level": False,
        "ignore_spam_target": False,
        "auto_buy_second_queue": False,
        "second_queue_spam_only": False,
        "building_priority": "Trading Post",
        "max_build_level": 24,
    },
    "research": {
        "auto_research": False,
        "categories_priority": {
            "economy": False, "defense": False, "military": False, "monster_hunt": False,
            "upgrade_defense": False, "upgrade_military": False, "army_leadership": False,
            "military_command": False, "familiars": False, "sigils": False,
            "wonder_battles": False, "familiar_battles": False, "gear": False,
            "advance_wonder_battles": False, "mana_awakening": False, "guild_duel": True
        }
    },
    "rally": {
        "join_rallies": True,
        "no_t5_troops": True,
        "dont_join_if_lab_full": True,
        "dont_fill_rally": True,
        "no_siege_troops": True,
        "troop_type": "Send 1 Troop",
        "one_troop_type_only": False,
        "add_buffers": False,
        "levels_to_attack": [5, 6],
        "join_expedition_rallies": False,
    },
    "realm_gather": {
        "enable": True,
        "resources": {"food": False, "stone": False, "wood": False, "ore": False, "gold": False, "lunite": True},
        "high_tier_gathering": True,
        "leave_spare_army": False,
        "spare_army_amount": 1,
        "max_armies_to_send": 0,
    },
    "gather": {
        "enable": True,
        "use_high_tier_troops": False,
        "resources": {"food": False, "stone": False, "wood": False, "ore": False, "gold": False, "gems": True},
        "levels": [1, 2, 3, 4, 5, 6],
        "leave_spare_army": True,
        "recall_camps": False,
        "spare_army_amount": 1,
        "schedule": {"only_gather_between": True, "start": "12:01 PM", "end": "11:00 PM", "timezone": "IST (UTC+05:30)"},
        "auto_kvk": {"rival_kingdom": False, "go_back_after_return": False, "buy_random_relocator": False, "recall_minutes_before": 10},
        "troop_management": {"under_attack": True, "scouted": True, "on_conflict": True, "regather_wait_time_minutes": 5},
    },
    "gear": {
        "auto_switch_gear": True,
        "idle_gear_set": None,
    },
    "monster": {
        "auto_hunting": True,
        "combo_prediction": True,
        "allow_saberfang": False,
        "use_boots": False,
        "use_energy_from_bag": False,
        "avoid_conflict": False,
        "avoid_guild_conflict": False,
        "stop_after_1_kill": True,
        "energy_percentage": 90,
        "hunt_mode": "Any",
        "max_walk_time_seconds": 60,
        "daily_kill_target": 0,
        "hunt_levels": [2],
        "monsters_to_hunt": "all_selected",
        "hero_type": "Auto Selected",
    },
    "hero_stage": {
        "auto_hire_heroes": True,
        "auto_upgrade_heroes": True,
        "auto_enhance_heroes": True,
        "use_level_up_items": True,
        "revive_dead_leader": True,
        "auto_attack_stages": True,
        "priority_mode": True,
        "attack_stage_type": "Custom Chapter",
        "custom_chapter": {"chapter": "Chapter 6", "stage_type": "Elite", "stage": "6-3", "sweep": True, "x10_sweep": True},
        "heroic_saga": {"send_heroes": False, "free_refreshes": True, "compasses_to_refresh": False, "grade": 0, "keep_compasses": 0},
    },
    "arena": {
        "attack_arena": True,
        "collect_gems": True,
        "attack_guildmates": False,
        "hero_type": "Auto Selected",
        "auto_army_colloseum": {"auto_challenge": False, "deploy_best_teams": True, "max_opponent_strength_pct": 90},
        "max_list_refreshes": 3,
        "use_all_entries_before_reset_min": 60,
        "buy_entries_with_gems": False,
        "max_gems_per_purchase": 100,
        "max_purchases_per_day": 1,
    },
    "guild": {
        "send_guild_help": True,
        "help_check_delay": 30,
        "join_showdown": True,
        "recall_armies_before_registering": False,
        "update_lineup_minutes_before_close": 0,
        "showdown_gear_set": "Current gear",
    },
    "speed_up": {
        "use_speed_ups": False,
        "normal_speed_ups_for_building_only": True,
        "auto_speed_ups": {
            "building": False, "research": False, "training": False, "healing": False,
            "merging": False, "trap": False, "trap_repair": False, "lunar_gear": False,
            "gear": False, "wall": False
        }
    },
    "troop": {
        "auto_train_troops": True,
        "auto_heal_troops": False,
        "auto_heal_sanctuary": False,
        "auto_craft_lunar": True,
        "training_levels": {"infantry": [0]*4, "ranged": [0]*4, "cavalry": [0]*4, "siege": [0]*4},
    },
    "supply": {
        "enable_resource_sending": False,
        "player_to_send": "wow man 69",
        "use_speed_gear": False,
        "supply_speed": 3,
        "max_travel_time_seconds": 600,
        "resources": {
            "food": {"send": False, "reserved": 1000000, "min_to_send": 3000000},
            "stone": {"send": False, "reserved": 1000000, "min_to_send": 3000000},
            "wood": {"send": False, "reserved": 10000000, "min_to_send": 30000000},
            "ore": {"send": True, "reserved": 1000000, "min_to_send": 30000000},
            "gold": {"send": True, "reserved": 1000000, "min_to_send": 3000000},
        }
    },
    "familiars_and_pacts": {
        "merge_skill_stones": False,
        "skill_stones_type": "none",
        "skill_stones_limit": 0,
        "enable_pact_merging": True,
        "pact_types_allow_merge": {"pact_1a": False, "pact_1b": False, "pact_2a": False, "pact_2b": False, "pact_3": False, "pact_4": True},
        "active_familiars": ["Aquarius", "Bonehead", "Evil Weevil", "Gemming Gremlin", "Goblin", "Harpy", "Hell Drider", "Hoarder", "Saberfang", "SnowBeast", "Sorcerer", "Tempersite", "Territe", "Totempest", "Trickster"]
    },
    "guild_fest": {
        "complete_missions": True,
        "solo_first": True,
        "send_mail_after_task": False,
        "completed_missions_guild": {
            "gather_resources": {"enabled": True, "min_points": 150, "max_points": 356},
            "get_lv19_dark_essences": {"enabled": True, "min_points": 150, "max_points": 356},
        },
        "remove_missions": {
            "enable": True,
            "remove_duplicates": False,
            "remove_delay_seconds": 3,
            "guild_remove_all_selected": True,
            "min_points": 130,
            "max_points": 355
        }
    },
    "extravaganza": {
        "enable_exchange": False,
        "auto_item_select": True,
        "filter_mission": False,
        "mission_filter_settings": {"min_points": 1, "max_points": 255}
    },
    "event_autoplay": {
        "frost_commissions": {"play": True, "collect_rewards": True},
        "racing": {"play": True, "collect_rewards": True},
        "pinball": {"play": True, "collect_rewards": True},
        "hell_event": {
            "auto_hell_event": False,
            "target_phase": 3,
            "use_speed_ups": False,
            "medal_heroes": "none",
            "kinds_to_play": {"train": True, "research": True, "build": True, "pacts": True, "traps": False, "hunt": True}
        }
    },
    "arena_and_battlefield": {
        "chaos_arena": {"auto_enter": False, "auto_complete_missions": True},
        "solo_battlefield": {
            "auto_enter": False, "claim_rewards": False, "claim_achievements": False,
            "auto_alchemy": False, "skip_alchemy_when_overheated": True, "help_guild_alchemy": False,
            "auto_research": False, "research_mode": "Best for nests", "attack_insecticon_nests": False,
            "max_nest_level": 60, "max_wounded_pct": 30, "leave_at_wounded_pct": 0
        }
    },
    "schedule": {
        "enable_schedule": True,
        "timezone": "IST (UTC+05:30)",
        "go_offline_between": {"start": "02:00 AM", "end": "08:00 AM"},
        "recall_armies": True,
        "monitor_shield": True,
        "monitor_anti_scout": False,
        "monitor_shelter": False,
        "randomize_schedule": True,
        "random_max_minutes": 30,
    }
}

@app.route("/api/config", methods=["GET"])
def get_config():
    return jsonify(BOT_CONFIG)

@app.route("/api/config", methods=["POST"])
def update_config():
    global BOT_CONFIG
    new_data = request.json
    if new_data:
        BOT_CONFIG.update(new_data)
        return jsonify({"status": "success", "message": "Configuration updated successfully!"})
    return jsonify({"status": "error", "message": "No data provided"}), 400

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=True)
