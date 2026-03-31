from threading import Lock

# global state lock for thread safety
state_lock = Lock()

state = {
    "running": True,
    "awake": False,
    "speaking": False,

    # WhatsApp automation
    "whatsapp_pending": False,
    "whatsapp_contact": None,
    "last_contact": None,

    # YouTube control
    "youtube_active": False,
}