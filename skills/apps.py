import os
import subprocess

def open_notepad():
    subprocess.Popen(["notepad.exe"])
    return "Opening Notepad."

def open_calculator():
    subprocess.Popen(["calc.exe"])
    return "Opening Calculator."
