from brain.decision import decide
from voice.listen import listen_command, init_mic
from voice.speak import speak
from voice.interrupt import start_interrupt_listener
from core.state import state
from memory.personal_brain import get_most_used_apps
from utils.logger import log
import time
from memory.context import get_context, clear, set_suggestion
from brain.suggestions import get_suggestion


WAKE_WORDS = [
    "hey jarvis",
    "hey jar",
    "hey service",
    "hey jervis",
    "jarvis",
    "hey buddy"
]

AUTO_SLEEP_SECONDS = 30


def detect_wake_word(text):
    return any(w in text for w in WAKE_WORDS)


def start_ai():
    init_mic()

    print("JARVIS AI Activated 🎙️")
    speak("Jarvis online. Say hey Jarvis.")

    start_interrupt_listener()

    last_active_time = time.time()

    while state["running"]:

        command = listen_command()
        now = time.time()

        # =========================
        # 🧠 CONTEXT TIMEOUT
        # =========================
        ctx = get_context()
        if ctx["timestamp"] and (now - ctx["timestamp"] > 15):
            clear()

        # =========================
        # 😴 AUTO SLEEP + SUGGESTIONS
        # =========================
        if state["awake"] and (now - last_active_time) > AUTO_SLEEP_SECONDS:

            suggestion = get_suggestion()

            # 🧠 If suggestion exists → speak and WAIT
            if suggestion:
                set_suggestion("open_app", "youtube")  # later make dynamic
                speak(suggestion)

                last_active_time = now   # ⏳ give time for YES/NO
                continue   # 🚨 do NOT sleep immediately

            # 💤 No suggestion → normal sleep
            apps = get_most_used_apps()

            if apps:
                speak(f"You often use {apps[0]}. Do you want me to open it?")

            if not state.get("whatsapp_pending") and not state.get("youtube_active"):
                state["awake"] = False
                log("Auto sleep triggered")
                speak("Going to sleep.")

            last_active_time = now
            continue

        # =========================
        # 🚫 IGNORE EMPTY INPUT
        # =========================
        if not command:
            continue

        # =========================
        # ❌ EXIT
        # =========================
        if any(x in command for x in ["exit", "quit", "goodbye"]):
            speak("Shutting down. Goodbye Harsh.")
            state["running"] = False
            break

        # =========================
        # 😴 MANUAL SLEEP
        # =========================
        if any(x in command for x in ["go to sleep", "sleep jarvis"]):
            state["awake"] = False
            clear()
            speak("Going to sleep.")
            continue

        # =========================
        # 🟢 WAKE SYSTEM
        # =========================
        if not state["awake"]:

            if detect_wake_word(command):
                state["awake"] = True
                last_active_time = now
                speak("Yes?")
                continue
            else:
                continue

        # =========================
        # 🧠 EXECUTE COMMAND
        # =========================
        response = decide(command)

        log(f"Decision returned: {repr(response)}")

        if response and response.strip():
            last_active_time = now   # ✅ only update on real interaction
            speak(response.strip())
        else:
            speak("I heard you, but I’m not sure how to respond yet.")


if __name__ == "__main__":
    start_ai()