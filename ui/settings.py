import tkinter as tk
from utils.autostart import (
    enable_autostart,
    disable_autostart,
    is_autostart_enabled,
)

def open_settings():
    root = tk.Tk()
    root.title("Jarvis Settings")
    root.geometry("300x150")
    root.resizable(False, False)

    autostart_var = tk.BooleanVar(value=is_autostart_enabled())

    def toggle_autostart():
        if autostart_var.get():
            enable_autostart()
        else:
            disable_autostart()

    cb = tk.Checkbutton(
        root,
        text="Start Jarvis on system startup",
        variable=autostart_var,
        command=toggle_autostart,
    )
    cb.pack(pady=30)

    root.mainloop()
