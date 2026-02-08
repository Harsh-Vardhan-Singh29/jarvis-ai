import speech_recognition as sr

recognizer = sr.Recognizer()
microphone = sr.Microphone()

recognizer.energy_threshold = 300
recognizer.pause_threshold = 0.8

def init_mic():
    with microphone as source:
        recognizer.adjust_for_ambient_noise(source, duration=0.6)

def listen_command():
    with microphone as source:
        print("🎤 Listening...")
        try:
            audio = recognizer.listen(source, timeout=5, phrase_time_limit=5)
        except sr.WaitTimeoutError:
            return ""

    try:
        text = recognizer.recognize_google(audio)
        print("You:", text)
        return text.lower()
    except:
        return ""
