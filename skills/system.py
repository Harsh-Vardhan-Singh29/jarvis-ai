import os
import ctypes
import subprocess
import pyautogui
pyautogui.FAILSAFE = False


# ---------------------------
# Low-level system actions
# ---------------------------

def open_notepad():
    subprocess.Popen(["notepad.exe"])
    return "Opening Notepad."

def open_calculator():
    subprocess.Popen(["calc.exe"])
    return "Opening Calculator."

def shutdown_system():
    os.system("shutdown /s /t 5")
    return "Shutting down the system."

def restart_system():
    os.system("shutdown /r /t 5")
    return "Restarting the system."


# ---------------------------
# Public router (IMPORTANT)
# ---------------------------

def system_commands(command: str):
    command = command.lower()

    # App launches
    if "notepad" in command:
        return open_notepad()

    if "calculator" in command or "calc" in command:
        return open_calculator()

    # Power commands
    if "shutdown" in command:
        return shutdown_system()

    if "restart" in command:
        return restart_system()

    return None

# =========================
# POWER CONTROLS
# =========================

def shutdown_pc():
    os.system("shutdown /s /t 1")
    return "Shutting down your PC."

def restart_pc():
    os.system("shutdown /r /t 1")
    return "Restarting your PC."

def sleep_pc():
    ctypes.windll.powrprof.SetSuspendState(0, 1, 0)
    return "Going to sleep."

def lock_pc():
    ctypes.windll.user32.LockWorkStation()
    return "Locking your PC."


# =========================
# VOLUME CONTROL
# =========================

def volume_up():
    subprocess.run(
        'powershell (New-Object -ComObject WScript.Shell).SendKeys([char]175)',
        shell=True
    )
    return "Volume up."

def volume_down():
    subprocess.run(
        'powershell (New-Object -ComObject WScript.Shell).SendKeys([char]174)',
        shell=True
    )
    return "Volume down."

def mute_volume():
    subprocess.run(
        'powershell (New-Object -ComObject WScript.Shell).SendKeys([char]173)',
        shell=True
    )
    return "Muted."


# =========================
# WINDOW CONTROL
# =========================

def switch_window():
    pyautogui.hotkey('alt', 'tab')
    return "Switching window."

def minimize_all():
    pyautogui.hotkey('win', 'd')
    return "Minimizing all windows."

def close_window():
    pyautogui.hotkey('alt', 'f4')
    return "Closing current window."

def show_task_view():
    pyautogui.hotkey('win', 'tab')
    return "Opening task view."

def open_start_menu():
    pyautogui.press('win')
    return "Opening start menu."

def open_settings():
    subprocess.Popen("start ms-settings:", shell=True)
    return "Opening settings."

# =========================
# MOUSE CONTROL
# =========================

def scroll_down():
    pyautogui.scroll(-500)
    return "Scrolling down."

def scroll_up():
    pyautogui.scroll(500)
    return "Scrolling up."

def click_mouse():
    pyautogui.click()
    return "Click."

# =========================
# MEDIA CONTROL
# =========================

def play_pause_media():
    pyautogui.press('playpause')
    return "Toggling media."

def next_track():
    pyautogui.press('nexttrack')
    return "Next track."

def previous_track():
    pyautogui.press('prevtrack')
    return "Previous track."
