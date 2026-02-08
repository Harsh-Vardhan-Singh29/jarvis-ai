from brain.decision import decide
from voice.listen import listen_command
from voice.speak import speak
awake = False

def start_ai():
    print("JARVIS AI Activated 🎙️")
    speak("JARVIS activated. How can I help you, Harsh?")

    while True:
        print("DEBUG: before listen_command")
        command = listen_command()

        if not command:
            continue

        global awake

        if not awake:
            if "hey jarvis" in command:
                awake = True
                speak("Yes?")
            continue
        print("DEBUG: listen_command returned ->", repr(command))

        if not command:
            continue

        if "exit" in command or "stop" in command:
            speak("Shutting down. Goodbye Harsh")
            break

        print("DEBUG: calling decide()")
        response = decide(command)
        print("DEBUG: decide() returned ->", repr(response))

        if response:
            print("DEBUG: speaking response")
            speak(response)
awake = False

if __name__ == "__main__":
    start_ai()
