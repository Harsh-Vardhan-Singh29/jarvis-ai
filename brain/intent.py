from memory.personal_brain import track_app_usage


def detect_intent(command: str):
    command = command.lower()

    FAST_KEYWORDS = [
        "open", "close", "start",
        "search", "google",
        "time", "date",
        "exit", "stop"
    ]

    for word in FAST_KEYWORDS:
        if word in command:
            return "FAST"

    return "THINK"

def detect_intent(command):
    command = command.lower()

    if "open whatsapp" in command:
        track_app_usage("whatsApp")
        return "OPEN_WHATSAPP"

    if "send message" in command or command.startswith("message"):
        track_app_usage("whatsApp")
        return "SEND_WHATSAPP"

    return "CHAT"
