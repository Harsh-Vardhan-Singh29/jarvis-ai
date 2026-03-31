import threading
import subprocess
import signal

from voice.audio_stream import start_audio_stream
from core.driver_monitor import start_driver_monitor
from main import start_ai
from ui.tray import run_tray

signal.signal(signal.SIGINT, signal.SIG_IGN)

# start ollama quietly
try:
    subprocess.Popen(
        ["ollama", "serve"],
        stdout=subprocess.DEVNULL,
        stderr=subprocess.DEVNULL,
        
        creationflags=subprocess.CREATE_NO_WINDOW
    )
except:
    pass

# start driver health monitor
start_driver_monitor()


def start_voice():
    start_ai()


# audio stream thread
threading.Thread(
    target=start_audio_stream,
    daemon=True
).start()


if __name__ == "__main__":

    # voice assistant thread
    voice_thread = threading.Thread(
        target=start_voice,
        daemon=True
    )
    voice_thread.start()

    # tray must run on main thread
    run_tray()