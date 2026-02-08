from brain.decision import decide
from voice.listen import listen_command
from voice.speak import speak
from voice.interrupt import start_interrupt_listener
from core.state import state
import time
from voice.listen import init_mic

AUTO_SLEEP_SECONDS = 20  # auto-sleep after inactivity

def start_ai():
    init_mic() 
    print("JARVIS AI Activated 🎙️")
    speak("Jarvis online. Say hey Jarvis.")

    start_interrupt_listener()

    last_active_time = time.time()

    while state["running"]:
        command = listen_command()
        now = time.time()

        # 💤 auto-sleep check
        if state["awake"] and (now - last_active_time) > AUTO_SLEEP_SECONDS:
            state["awake"] = False
            print("DEBUG: auto-sleep triggered")
            speak("Going to sleep.")
            continue

        if not command:
            continue

        print("DEBUG: heard ->", command)
        last_active_time = now  # reset timer on ANY speech

        # 🚪 EXIT ANYTIME
        if "exit" in command or "quit" in command:
            speak("Shutting down. Goodbye Harsh")
            state["running"] = False
            break

        # 💤 MANUAL SLEEP
        if "go to sleep" in command or "sleep jarvis" in command:
            state["awake"] = False
            speak("Going to sleep.")
            continue

        # 🔔 WAKE WORD
        if not state["awake"]:
            if "hey jarvis" in command or "hey jar" in command or "hey buddy" in command:
                state["awake"] = True
                last_active_time = time.time()
                speak("Yes?")
            continue

        # 🧠 PROCESS COMMAND
        response = decide(command)
        if response:
            speak(response)

if __name__ == "__main__":
    start_ai()
