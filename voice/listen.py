import speech_recognition as sr
from voice.audio_stream import get_audio
from utils.logger import log
import time

recognizer = sr.Recognizer()

recognizer.energy_threshold = 300
recognizer.dynamic_energy_threshold = True
recognizer.pause_threshold = 0.8
recognizer.phrase_threshold = 0.3
recognizer.non_speaking_duration = 0.5

microphone = None


def init_mic():
    global microphone

    try:
        time.sleep(1)

        microphone = sr.Microphone(
            device_index=1,
            sample_rate=16000
        )

        with microphone as source:
            recognizer.adjust_for_ambient_noise(source, duration=2)

        log("Microphone calibrated successfully.")

    except Exception as e:
        log(f"MIC INIT ERROR: {e}")
        microphone = None


def listen_command():

    try:
        audio = get_audio()

        command = recognizer.recognize_google(audio).lower().strip()

        if len(command) < 4:  # filter out short noises
            return ""

        log(f"Heard command: {command}")
        return command

    except sr.UnknownValueError:
        return ""
    
    except sr.WaitTimeoutError:
        return ""

    except OSError:
        log("Microphone stream closed. Reinitializing.")
        init_mic()
        return ""

    except Exception:
        return ""