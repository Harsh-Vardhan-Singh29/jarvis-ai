from skills.system import system_commands
from core.state import state
from skills.whatsapp import open_whatsapp, open_chat, send_message, close_whatsapp
from skills.web import web_commands
from skills.automation import run_automation
from memory.memory import Memory
from brain.intent import detect_intent
from ai.llm import ask_llm
from skills.tools_executer import execute_tool
from brain.cache import get_cached, save_cache
from skills.browser_control import switch_tab, show_tabs, close_tab, close_current_tab, close_browser
from utils.logger import log
from utils.timeout import run_with_timeout
from memory.personal_brain import *
from memory.context import get_context, set_context, update_context, clear
from skills.whatsapp import send_message
from memory.context import get_suggestion_context, clear_suggestion

memory = Memory()


QUESTION_WORDS = {
    "what","why","how","explain","define","tell",
    "who","when","where","which"
}


def safe_execute(func):
    try:
        return func()
    except Exception as e:
        log(f"SKILL ERROR: {e}")
        return "Something went wrong while executing that command."
    
# ======================================================
# 🧠 HUMAN LEVEL WHATSAPP PARSER
# ======================================================

def remember_contact(name):
    state["last_contact"] = name

def parse_whatsapp_command(command: str):
    command = command.lower().strip()
    trigger_words = ["send", "tell", "text", "message", "whatsapp", "ask"]

    if not any(w in command for w in trigger_words):
        return None, None

    # 1. HUMAN LEVEL PARSING (With "to" - e.g., "send hello to umang")
    if " to " in command:
        msg_part, contact = command.split(" to ", 1)
        msg_part = msg_part.replace("send", "").replace("tell", "").replace("message", "").replace("text", "").strip()
        contact = contact.strip().title()
        
        if msg_part:
            log(f"✅ DEBUG [Parse 1 - 'To']: Contact = '{contact}' | Message = '{msg_part}'")
            return contact, msg_part
        else:
            return None, None

    # 2. DIRECT PHRASING (Without "to" - e.g., "message saksham chai peene chalega")
    words = command.split()
    
    if len(words) >= 3 and words[0] in ["tell", "send", "text", "message", "whatsapp"]:
        contact = words[1].title()
        msg_part = " ".join(words[2:]).strip()
        
        if msg_part:
            log(f"✅ DEBUG [Parse 2 - Direct]: Contact = '{contact}' | Message = '{msg_part}'")
            return contact, msg_part

    # 3. PRO MEMORY MODE (Follow-up messages)
    if state.get("last_contact"):
        contact = state["last_contact"]
        msg_part = command.replace("send", "").replace("tell", "").replace("message", "").strip()
        
        if msg_part and msg_part != "message":
            log(f"✅ DEBUG [Parse 3 - Memory]: Contact = '{contact}' | Message = '{msg_part}'")
            return contact, msg_part

    return None, None


# ======================================================
# 🎯 MAIN DECISION ENGINE
# ======================================================

def decide(command: str):
    if not command:
        return "I didn’t quite catch that."

    command = command.strip().lower()
    
    # =========================
# 🤖 SUGGESTION HANDLING
# =========================
    sugg = get_suggestion_context()

    if sugg["intent"]:

        # ✅ YES
        if command in ["yes", "haan", "ha", "yup", "yeah"]:
            intent = sugg["intent"]
            data = sugg["data"]

            clear_suggestion()

            if intent == "open_app":
                return decide(f"open {data}")

        # ❌ NO
        if command in ["no", "nah", "nahi", "nope"]:
            clear_suggestion()
            return "Alright."
        
    
    ctx = get_context()

    if ctx["awaiting"]:

    # 🛑 1. CANCEL should ALWAYS break context
        if command in ["cancel", "stop", "leave it"]:
            clear()
            return "Okay, cancelled."

        # 🔁 2. NEW INTENT DETECTED → BREAK CONTEXT
        if any(x in command for x in [
            "play", "open", "search", "close", "switch", "youtube"
        ]):
            clear()
            return decide(command)

    # 🎵 SONG FLOW
        if ctx["intent"] == "play_song":
            song = command
            clear()
            return decide(f"play {song}")

        # 💬 MESSAGE FLOW
        if ctx["intent"] == "send_message":

            if ctx["awaiting"] == "contact":
                update_context("contact", command)

                # ✅ ONLY update awaiting, NOT reset context
                ctx["awaiting"] = "message"

                return "What message should I send?"

            elif ctx["awaiting"] == "message":
                contact = ctx["data"].get("contact")
                message = command
                clear()
                return decide(f"send {message} to {contact}")

    if "switch to youtube" in command:
        return run_with_timeout(lambda: safe_execute(lambda: switch_tab("youtube")))

    if "switch to whatsapp" in command:
        return run_with_timeout(lambda: safe_execute(lambda: switch_tab("whatsapp")))

    if "list tabs" in command:
        return run_with_timeout(lambda: safe_execute(show_tabs))

    if "close youtube" in command:
        return run_with_timeout(lambda: safe_execute(lambda: close_tab("youtube")))

    if "close whatsapp" in command:
        return run_with_timeout(lambda: safe_execute(lambda: close_tab("whatsapp")))

    if "close tab" in command:
        return run_with_timeout(lambda: safe_execute(close_current_tab))

    if "close browser" in command:
        return run_with_timeout(lambda: safe_execute(close_browser))

    # ======================================================
    # ===== WINDOW CONTROL =====
    # ======================================================

    if "change window" in command:
        from skills.system import switch_window
        return run_with_timeout(lambda: safe_execute(switch_window))

    if any(x in command for x in ["minimize all", "minimise all", "show desktop"]):
        from skills.system import minimize_all
        return run_with_timeout(lambda: safe_execute(minimize_all))

    if "close window" in command or "close app" in command:
        from skills.system import close_window
        return run_with_timeout(lambda: safe_execute(close_window))

    # ======================================================
    # ===== SYSTEM POWER =====
    # ======================================================

    if "shutdown pc" in command or "shutdown" in command or "shut down" in command:
        from skills.system import shutdown_pc
        return run_with_timeout(lambda: safe_execute(shutdown_pc))

    if "restart pc" in command:
        from skills.system import restart_pc
        return run_with_timeout(lambda: safe_execute(restart_pc))

    if "lock pc" in command or "lock screen" in command:
        from skills.system import lock_pc
        return run_with_timeout(lambda: safe_execute(lock_pc))

    if "sleep pc" in command:
        from skills.system import sleep_pc
        return run_with_timeout(lambda: safe_execute(sleep_pc))

    # ======================================================
    # ===== VOLUME CONTROL (SYSTEM ONLY) =====
    # ======================================================

    if "volume up" in command and "youtube" not in command:
        from skills.system import volume_up
        return run_with_timeout(lambda: safe_execute(volume_up))

    if "volume down" in command and "youtube" not in command:
        from skills.system import volume_down
        return run_with_timeout(lambda: safe_execute(volume_down))

    if "mute system" in command or "mute volume" in command:
        from skills.system import mute_volume
        return run_with_timeout(lambda: safe_execute(mute_volume))

    # ======================================================
    # ===== DESKTOP CONTROL =====
    # ======================================================

    if "task view" in command:
        from skills.system import show_task_view
        return run_with_timeout(lambda: safe_execute(show_task_view))

    if "open start menu" in command:
        from skills.system import open_start_menu
        return run_with_timeout(lambda: safe_execute(open_start_menu))

    if "open settings" in command:
        from skills.system import open_settings
        return run_with_timeout(lambda: safe_execute(open_settings))

    # ======================================================
    # ===== MOUSE =====
    # ======================================================

    if "scroll down" in command:
        from skills.system import scroll_down
        return run_with_timeout(lambda: safe_execute(scroll_down))

    if "scroll up" in command:
        from skills.system import scroll_up
        return run_with_timeout(lambda: safe_execute(scroll_up))

    if "click mouse" in command:
        from skills.system import click_mouse
        return run_with_timeout(lambda: safe_execute(click_mouse))

    # ======================================================
    # ===== MEDIA =====
    # ======================================================

    if "pause media" in command or "play media" in command:
        from skills.system import play_pause_media
        return run_with_timeout(lambda: safe_execute(play_pause_media))

    if "next track" in command:
        from skills.system import next_track
        return run_with_timeout(lambda: safe_execute(next_track))

    if "previous track" in command:
        from skills.system import previous_track
        return run_with_timeout(lambda: safe_execute(previous_track))
    

    # ======================================================
    # ========= YOUTUBE =========
    # ======================================================
    
    if "play a song" in command:
        set_context(intent="play_song", awaiting="song_name")
        return "Which song?"
    
    if "send message" in command:
        set_context(intent="send_message", awaiting="contact")
        return "To whom?"

    if "open youtube" in command:
        from skills.youtube import open_youtube
        add_favorite_app("youTube")
        track_app_usage("youTube")
        return run_with_timeout(lambda: safe_execute(open_youtube))

    if command.startswith("play"):
        from skills.youtube import play_video
        query = command.replace("play", "").strip()
        return run_with_timeout(lambda: safe_execute(lambda: play_video(query)))

    if any(x in command for x in [
        "pause",
        "pause video",
        "stop video"
    ]):
        from skills.youtube import pause_video
        return run_with_timeout(lambda: safe_execute(pause_video))
    
    if any(x in command for x in [
        "resume",
        "play video",
        "continue video"
    ]):
        from skills.youtube import pause_video
        return run_with_timeout(lambda: safe_execute(pause_video))

    # YouTube Fullscreen
    if any(x in command for x in [
        "fullscreen",
        "full screen",
        "go full screen",
        "make it full screen",
        "on screen"
    ]):
        from skills.youtube import fullscreen
        return run_with_timeout(lambda: safe_execute(fullscreen))

    if "next video" in command:
        from skills.youtube import next_video
        return run_with_timeout(lambda: safe_execute(next_video))

    # YOUTUBE volume (separate from system volume)
    if "youtube volume up" in command:
        from skills.youtube import volume_up as yt_up
        return run_with_timeout(lambda: safe_execute(yt_up))

    if "youtube volume down" in command:
        from skills.youtube import volume_down as yt_down
        return run_with_timeout(lambda: safe_execute(yt_down))

    # ======================================================
    # STEP MODE WHATSAPP (WAITING FOR MESSAGE)
    # ======================================================

    if state.get("whatsapp_pending"):
        contact = state.get("whatsapp_contact")

        safe_execute(lambda: send_message(command))
        remember_contact(contact)

        state["whatsapp_pending"] = False
        state["whatsapp_contact"] = None

        return f"Message sent to {contact}."

    # ======================================================
    # EXIT (HIGH PRIORITY)
    # ======================================================

    if "exit" in command or "stop" in command:
        return "exit"

    # ======================================================
    # CACHE
    # ======================================================

    cached = get_cached(command)
    if cached:
        return cached

    # ======================================================
    # MEMORY SAVE & RECALL
    # ======================================================

    if command.startswith("my name is"):
        name = command.replace("my name is", "").strip()
        memory.remember("user_name", name)
        return f"Got it. I will remember your name is {name}"

    if "what is my name" in command or "what's my name" in command:
        name = memory.recall("user_name")
        return f"Your name is {name}" if name else "I don't know your name yet."
    
    if command.startswith("remember project") and "is" in command:

        parts = command.replace("remember project", "").split("is")

        project = parts[0].strip()
        description = parts[1].strip()

        save_project(project, description)

        return f"I saved your project {project}"
    
    if "my projects" in command or "my project" in command or "list projects" in command:

        projects = get_projects()

        if not projects:
            return "You have no saved projects."

        result = ""

        for p, d in projects.items():
            result += f"{p} which is {d}. "

        return result
    
    if command.startswith("remember") and "is" in command:

        parts = command.replace("remember", "").split("is")

        real_contact = parts[0].strip().title()
        alias = parts[1].strip().lower()

        save_contact(alias, real_contact)

        return f"I will remember that {alias} means {real_contact}"
    
    if "favourite apps" in command:

        apps = get_favorite_apps()

        if not apps:
            return "I don't know your favorite apps yet."

        return "Your favorite apps are " + ", ".join(apps)
    
    if "most used apps" in command:

        apps = get_most_used_apps()

        if not apps:
            return "I haven't learned your habits yet."

        return "You usually use " + ", ".join(apps)
        
    

    # ======================================================
    # WHATSAPP (1-Step Smart Mode)
    # ======================================================

    contact, message = parse_whatsapp_command(command)

    if contact:
        alias = get_contact(contact.lower())
        if alias:
            contact = alias
    
    if contact:
        real_contact = get_contact(contact.lower())
        if real_contact:
            contact = real_contact

    if contact and message:
        safe_execute(open_whatsapp)
        add_favorite_app("whatsApp")
        track_app_usage("whatsApp")
        success = safe_execute(lambda: open_chat(contact))

        if success:
            remember_contact(contact)
            return safe_execute(lambda: send_message(message))

        return f"I couldn't find {contact}."

    # ======================================================
    # WHATSAPP (2-Step Mode)
    # ======================================================
    if contact:
        real_contact = get_contact(contact.lower())
        if real_contact:
            contact = real_contact
        
    if command.startswith("send message to") or command.startswith("text"):
        contact = command.replace("send message to", "").replace("text", "").strip().title()

        alias = get_contact(contact.lower())

        if alias:
            contact = alias

        safe_execute(open_whatsapp)
        add_favorite_app("whatsApp")
        track_app_usage("whatsApp")
        success = safe_execute(lambda: open_chat(contact))

        if success:
            remember_contact(contact)
            state["whatsapp_pending"] = True
            state["whatsapp_contact"] = contact
            return f"Okay. What should I send to {contact.lower()}?"

        return f"I couldn't find {contact}."

    # ======================================================
    # INTENT DETECTION
    # ======================================================

    intent = detect_intent(command)

    auto_response = run_automation(intent, command)
    if auto_response:
        return auto_response

    # ======================================================
    # INSTANT SHORTCUTS
    # ======================================================

    if any(p in command for p in ("write", "note", "type", "document")):
        return execute_tool("open_notepad")

    if any(p in command for p in ("calculate", "math")):
        return execute_tool("open_calculator")

    if any(p in command for p in ("browse", "internet", "website")):
        add_favorite_app("browser")
        track_app_usage("browser")
        return execute_tool("open_browser")

    # ======================================================
    # SYSTEM / WEB FAST MODE
    # ======================================================

    if intent == "FAST":
        if "open" in command or "close" in command:
            return system_commands(command)

        if "search" in command or "google" in command:
            return web_commands(command)

        if "time" in command:
            from datetime import datetime
            return datetime.now().strftime("The time is %I:%M %p")

        if "date" in command:
            from datetime import date
            return f"Today's date is {date.today()}"

    # ======================================================
    # AI SECTION (Lazy Import Safe)
    # ======================================================

    from ai.llm import ask_llm

    words = set(command.split())
    is_question = bool(words & QUESTION_WORDS)

    if is_question:
        user_name = memory.recall("user_name") or "User"
        context = f"The user's name is {user_name}."
        response = ask_llm(command, context)
    else:
        context = get_context()
        response = ask_llm(command, context)

    if response and response.strip():
        response = response.strip()
        save_cache(command, response)
        set_context("user", command)
        set_context("assistant", response)
        return response

    return "I didn’t quite catch that."




