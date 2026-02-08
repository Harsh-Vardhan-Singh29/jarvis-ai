import os
import sys

def enable_autostart(app_name="Jarvis"):
    startup_dir = os.path.join(
        os.environ["APPDATA"],
        "Microsoft\\Windows\\Start Menu\\Programs\\Startup"
    )

    exe_path = sys.executable
    shortcut_path = os.path.join(startup_dir, f"{app_name}.lnk")

    import win32com.client
    shell = win32com.client.Dispatch("WScript.Shell")
    shortcut = shell.CreateShortCut(shortcut_path)
    shortcut.Targetpath = exe_path
    shortcut.WorkingDirectory = os.path.dirname(exe_path)
    shortcut.save()

def disable_autostart(app_name="Jarvis"):
    startup_dir = os.path.join(
        os.environ["APPDATA"],
        "Microsoft\\Windows\\Start Menu\\Programs\\Startup"
    )
    shortcut_path = os.path.join(startup_dir, f"{app_name}.lnk")
    if os.path.exists(shortcut_path):
        os.remove(shortcut_path)
