context = {
    "intent": None,
    "data": {},
    "awaiting": None,
    "timestamp": None
}


def set_context(intent=None, awaiting=None, data=None):
    import time
    context["intent"] = intent
    context["awaiting"] = awaiting
    context["data"] = data or {}
    context["timestamp"] = time.time()


def get_context():
    return context


def update_context(key, value):
    context["data"][key] = value


def clear():
    context["intent"] = None
    context["awaiting"] = None
    context["data"] = {}
    context["timestamp"] = None
    
suggestion_context = {
    "intent": None,
    "data": None,
    "timestamp": None
}


def set_suggestion(intent, data):
    import time
    suggestion_context["intent"] = intent
    suggestion_context["data"] = data
    suggestion_context["timestamp"] = time.time()


def get_suggestion_context():
    return suggestion_context


def clear_suggestion():
    suggestion_context["intent"] = None
    suggestion_context["data"] = None
    suggestion_context["timestamp"] = None