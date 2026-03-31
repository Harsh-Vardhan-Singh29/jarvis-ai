from memory.personal_brain import get_most_used_apps
from datetime import datetime


def get_suggestion():

    apps = get_most_used_apps()

    if not apps:
        return None

    current_hour = datetime.now().hour

    # 🕒 Time-based simple logic
    if 18 <= current_hour <= 23:
        if "youtube" in apps[0].lower():
            return "You usually watch YouTube now. Want me to open it?"

    if 9 <= current_hour <= 17:
        if "vscode" in apps[0].lower() or "code" in apps[0].lower():
            return "You usually code at this time. Should I open your setup?"

    return None