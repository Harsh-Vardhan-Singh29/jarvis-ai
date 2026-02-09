import threading
from main import start_ai
from ui.tray import run_tray

def start_voice():
    start_ai()

if __name__ == "__main__":
    # 1️⃣ start voice assistant in background
    voice_thread = threading.Thread(
        target=start_voice,
        daemon=True
    )
    voice_thread.start()

    # 2️⃣ run tray app on MAIN THREAD (required)
    run_tray()



