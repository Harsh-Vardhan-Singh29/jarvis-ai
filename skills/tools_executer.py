import subprocess
import webbrowser

def execute_tool(tool_name):
    tool_name = tool_name.strip().lower()

    # 🧠 Normalize AI outputs & use subprocess so the AI doesn't freeze
    if "notepad" in tool_name:
        subprocess.Popen("notepad")
        return "Opening Notepad 📝"

    if "calculator" in tool_name or "calc" in tool_name:
        subprocess.Popen("calc")
        return "Opening Calculator 🧮"

    if "browser" in tool_name or "internet" in tool_name or "search" in tool_name:
        webbrowser.open("https://www.google.com")
        return "Opening browser 🌐"

    return "I don't know how to do that yet."