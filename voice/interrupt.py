from pynput import keyboard
from voice.speak import stop_speaking
from core.state import state

def start_interrupt_listener():
    def on_press(key):
        if key == keyboard.Key.esc and state["speaking"]:
            stop_speaking()

    listener = keyboard.Listener(on_press=on_press)
    listener.daemon = True
    listener.start()
