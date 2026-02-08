# skills/system.py
import os

def system_commands(command):
    if "open notepad" in command:
        os.system("notepad")
        return "Opening Notepad 📝"

    elif "open calculator" in command:
        os.system("calc")
        return "Opening Calculator 🧮"

    else:
        return "System command not recognized."
