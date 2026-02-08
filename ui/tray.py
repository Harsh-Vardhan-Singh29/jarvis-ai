import pystray
from pystray import MenuItem as item
from PIL import Image
from ui.settings import open_settings
import os
import threading
from core.state import state
from voice.speak import stop_speaking
import time

ICON = None   # 🔒 keep global reference

def create_image():
    # Guaranteed visible icon
    img = Image.new("RGB", (64, 64), "black")
    return img

def wake(icon, item):
    state["awake"] = True

def sleep(icon, item):
    state["awake"] = False

def stop(icon, item):
    stop_speaking()

def exit_app(icon, item):
    state["running"] = False
    icon.stop()

def run_tray():
    global ICON
    print("TRAY STARTED")

    menu = (
        item("Wake", wake),
        item("Sleep", sleep),
        item("Stop Speaking", stop),
        item("Settings", open_settings),
        item("Exit", exit_app),
        
    )

    ICON = pystray.Icon(
        "Jarvis",
        create_image(),
        "Jarvis — Sleeping",
        menu
    )

    def update_tooltip():
        while state["running"]:
            if state["speaking"]:
                ICON.title = "Jarvis — Speaking"
            elif state["awake"]:
                ICON.title = "Jarvis — Awake"
            else:
                ICON.title = "Jarvis — Sleeping"

            time.sleep(0.5)

    threading.Thread(
        target=update_tooltip,
        daemon=True
    ).start()

    ICON.run()