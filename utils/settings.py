import json
import os
import sys

def _config_path():
    # Works in both .py and .exe
    base = os.path.dirname(sys.executable if getattr(sys, 'frozen', False) else __file__)
    return os.path.join(base, "config", "settings.json")

def load_settings():
    try:
        with open(_config_path(), "r") as f:
            return json.load(f)
    except:
        return {
            "autostart": False,
            "sleep_timeout": 25,
            "wake_word": True
        }

def save_settings(data):
    os.makedirs(os.path.dirname(_config_path()), exist_ok=True)
    with open(_config_path(), "w") as f:
        json.dump(data, f, indent=2)
