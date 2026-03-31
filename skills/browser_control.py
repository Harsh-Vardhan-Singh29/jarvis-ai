from core.browser import get_driver
from core.tab_manager import get_tab, list_tabs, remove_tab


# =========================
# SWITCH TAB
# =========================
def switch_tab(name):
    driver = get_driver()

    handle = get_tab(name)

    # tab no longer exists
    if handle and handle not in driver.window_handles:
        remove_tab(name)
        return f"{name} tab was closed."

    if handle:
        driver.switch_to.window(handle)
        return f"Switched to {name}."

    return f"{name} tab not found."


# =========================
# CLOSE SPECIFIC TAB
# =========================
def close_tab(name):
    driver = get_driver()

    handle = get_tab(name)

    if handle and handle in driver.window_handles:
        driver.switch_to.window(handle)
        driver.close()

        remove_tab(name)

        # switch to another tab if available
        if driver.window_handles:
            driver.switch_to.window(driver.window_handles[-1])

        return f"{name} tab closed."

    return f"{name} tab not found."


# =========================
# CLOSE CURRENT TAB
# =========================
def close_current_tab():
    driver = get_driver()

    if not driver.window_handles:
        return "No browser tabs open."

    current = driver.current_window_handle

    driver.close()

    # remove tab from registry
    for name, handle in list_tabs().items():
        if handle == current:
            remove_tab(name)

    if driver.window_handles:
        driver.switch_to.window(driver.window_handles[-1])

    return "Tab closed."


# =========================
# CLOSE ENTIRE BROWSER
# =========================
def close_browser():
    driver = get_driver()

    try:
        driver.quit()
    except:
        pass

    # clear tab registry
    for name in list(list_tabs().keys()):
        remove_tab(name)

    return "Browser closed."


# =========================
# SHOW OPEN TABS
# =========================
def show_tabs():
    tabs = list_tabs()

    if not tabs:
        return "No browser tabs registered."

    return "Open tabs are: " + ", ".join(tabs.keys())