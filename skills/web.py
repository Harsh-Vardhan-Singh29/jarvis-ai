import webbrowser

from memory.personal_brain import track_app_usage

def open_browser():
    track_app_usage("browser")
    webbrowser.open("https://www.google.com")
    return "Opening browser."

def search_google(command):
    query = command.replace("search", "").replace("google", "").strip()
    if not query:
        query = "something"
    url = f"https://www.google.com/search?q={query}"
    webbrowser.open(url)
    return f"Searching Google for {query}."

def web_commands(command):
    if "search" in command or "google" in command:
        track_app_usage("browser")
        return search_google(command)

    if "browser" in command or "internet" in command:
        track_app_usage("browser")
        return open_browser()

    return None
