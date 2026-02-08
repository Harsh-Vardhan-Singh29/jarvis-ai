from skills.system import system_commands
from skills.web import web_commands
from memory.memory import Memory
from brain.intent import detect_intent
from ai.llm import ask_llm
from skills.tools_executer import execute_tool
from brain.cache import get_cached, save_cache
from brain.context import ConversationContext


memory = Memory()
conversation = ConversationContext()


def decide(command: str):
    command = command.lower()

    # 0️⃣ CACHE (INSTANT)
    cached = get_cached(command)
    if cached:
        return cached

    # 1️⃣ EXIT
    if "exit" in command or "stop" in command:
        return "exit"

    # 2️⃣ QUESTION DETECTION (🔥 MUST COME EARLY)
    question_words = ["what", "why", "how", "explain", "define", "tell"]
    is_question = any(q in command.split() for q in question_words)

    if is_question:
        user_name = memory.recall("user_name") or "User"
        context = f"The user's name is {user_name}."
        response = ask_llm(command, context)
        save_cache(command, response)
        return response

    # 3️⃣ MEMORY SAVE
    if "my name is" in command:
        name = command.replace("my name is", "").strip()
        memory.remember("user_name", name)
        return f"Got it. I will remember your name is {name}"

    # 4️⃣ MEMORY RECALL
    if "what is my name" in command or "what's my name" in command:
        name = memory.recall("user_name")
        return f"Your name is {name}" if name else "I don't know your name yet"

    # 5️⃣ INSTANT SHORTCUTS (NO AI)
    if any(p in command for p in ["write", "note", "type", "document"]):
        return execute_tool("open_notepad")

    if any(p in command for p in ["calculate", "math"]):
        return execute_tool("open_calculator")

    if any(p in command for p in ["browse", "internet", "website"]):
        return execute_tool("open_browser")

    # 6️⃣ FAST INTENT
    intent = detect_intent(command)

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


    # 8️⃣ FALLBACK AI
    context = conversation.get_context()
    response = ask_llm(command, context)
    conversation.add(command, response)
    return response


