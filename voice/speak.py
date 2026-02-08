import win32com.client
import pythoncom
from core.state import state

speaker = None

SVSFlagsAsync = 1
SVSFPurgeBeforeSpeak = 2

def _init_sapi():
    global speaker
    if speaker is None:
        pythoncom.CoInitialize()
        speaker = win32com.client.Dispatch("SAPI.SpVoice")

def speak(text):
    _init_sapi()
    state["speaking"] = True
    speaker.Speak(text, SVSFlagsAsync)
    state["speaking"] = False

def stop_speaking():
    if speaker:
        speaker.Speak("", SVSFPurgeBeforeSpeak)
        state["speaking"] = False
