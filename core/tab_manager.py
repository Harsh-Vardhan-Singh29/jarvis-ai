tabs = {}

def register_tab(name, handle):
    tabs[name] = handle

def get_tab(name):
    return tabs.get(name)

def remove_tab(name):
    if name in tabs:
        del tabs[name]

def list_tabs():
    return tabs

def safe_switch(driver, name):
    handle = tabs.get(name)

    if handle and handle in driver.window_handles:
        driver.switch_to.window(handle)
        return True

    return False

def close_tab(driver, name):
    handle = get_tab(name)

    if handle not in driver.window_handles:
        remove_tab(name)
        return f"{name} tab not found."

    driver.switch_to.window(handle)