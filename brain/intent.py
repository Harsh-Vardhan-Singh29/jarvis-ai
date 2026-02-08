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
