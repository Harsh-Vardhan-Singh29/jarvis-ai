import queue
import speech_recognition as sr
from utils.logger import log

audio_queue = queue.Queue()

recognizer = sr.Recognizer()
mic = sr.Microphone(sample_rate=16000)


def start_audio_stream():

    with mic as source:
        recognizer.adjust_for_ambient_noise(source, duration=2)

        while True:
            try:
                audio = recognizer.listen(
                    source,
                    timeout=2,
                    phrase_time_limit=5
                )

                audio_queue.put(audio)   # ✅ push audio to queue

            except sr.WaitTimeoutError:
                continue   # ✅ no speech → keep looping

            except Exception as e:
                log(f"AUDIO ERROR: {e}")
                continue


def get_audio():
    try:
        return audio_queue.get(timeout=1)  # ✅ don’t block forever
    except queue.Empty:
        return None