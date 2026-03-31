from skills.system import shutdown_system, restart_system
from skills.whatsapp import open_whatsapp
from skills.apps import open_notepad, open_calculator
from skills.web import web_commands

def run_automation(intent, command):
    if intent == "OPEN_WHATSAPP":
        return open_whatsapp()

    # NOTE: SEND_WHATSAPP was removed here because decision.py 
    # handles both 1-step and 2-step WhatsApp messaging flawlessly.

    # App actions
    if intent == "open_notepad":
        return open_notepad()

    if intent == "open_calculator":
        return open_calculator()

    # Web actions
    web_result = web_commands(command)
    if web_result:
        return web_result

    # Power actions
    if intent == "shutdown":
        return shutdown_system()

    if intent == "restart":
        return restart_system()

    return None