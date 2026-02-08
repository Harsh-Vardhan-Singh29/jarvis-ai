import tkinter as tk
from utils.autostart import enable_autostart, disable_autostart

_window = None  # prevent multiple windows

def open_settings():
    global _window
    if _window:
        return  # already open

    _window = tk.Tk()
    _window.title("Jarvis Settings")
    _window.geometry("300x200")
    _window.resizable(False, False)

    # ----- UI ELEMENTS -----

    tk.Label(
        _window,
        text="Jarvis Settings",
        font=("Segoe UI", 12, "bold")
    ).pack(pady=10)

    autostart_var = tk.BooleanVar()

    def toggle_autostart():
        if autostart_var.get():
            enable_autostart()
        else:
            disable_autostart()

    tk.Checkbutton(
        _window,
        text="Start Jarvis on Windows boot",
        variable=autostart_var,
        command=toggle_autostart
    ).pack(pady=10)

    def on_close():
        global _window
        _window.destroy()
        _window = None

    tk.Button(
        _window,
        text="Close",
        command=on_close
    ).pack(pady=10)

    _window.protocol("WM_DELETE_WINDOW", on_close)
    _window.mainloop()
