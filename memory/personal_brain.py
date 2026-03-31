import json
import os

MEMORY_FILE = "memory/brain_memory.json"


def load_memory():
    if not os.path.exists(MEMORY_FILE):
        return {}

    with open(MEMORY_FILE, "r") as f:
        return json.load(f)


def save_memory(data):
    with open(MEMORY_FILE, "w") as f:
        json.dump(data, f, indent=4)


# ================= USER =================

def set_user_name(name):

    data = load_memory()

    data["user"]["name"] = name

    save_memory(data)


def get_user_name():

    data = load_memory()

    return data["user"].get("name")


# ================= CONTACTS =================

def save_contact(alias, name):

    data = load_memory()

    data["contacts"][alias] = name

    save_memory(data)


def get_contact(alias):

    data = load_memory()

    return data["contacts"].get(alias)


# ================= FAVORITE APPS =================

def add_favorite_app(app):

    data = load_memory()

    if app not in data["favorite_apps"]:
        data["favorite_apps"].append(app)

    save_memory(data)


def get_favorite_apps():

    data = load_memory()

    return data["favorite_apps"]


# ================= PROJECTS =================

def save_project(name, description):

    data = load_memory()

    data["projects"][name] = description

    save_memory(data)


def get_projects():

    data = load_memory()

    return data["projects"]

# ================= HABIT LEARNING =================

def track_app_usage(app):

    data = load_memory()

    usage = data["work_habits"]["app_usage"]

    if app not in usage:
        usage[app] = 0

    usage[app] += 1

    save_memory(data)


def get_most_used_apps():

    data = load_memory()

    usage = data["work_habits"]["app_usage"]

    if not usage:
        return []

    sorted_apps = sorted(
        usage.items(),
        key=lambda x: x[1],
        reverse=True
    )

    return [app for app, count in sorted_apps[:3]]