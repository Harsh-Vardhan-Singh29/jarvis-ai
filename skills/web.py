# skills/web.py
import webbrowser

def web_commands(command):
    if "search" in command:
        query = command.replace("search", "").strip()
        webbrowser.open(f"https://www.google.com/search?q={query}")
        return f"Searching for {query} 🔍"

    return "Web command not recognized."
