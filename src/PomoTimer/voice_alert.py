from __init__ import VOICE_ID
import pyttsx3

class VoiceAlert:
    def __init__(self):
        self.voice_engine = pyttsx3.init()
        self.voice_engine.setProperty('voice', VOICE_ID)

    def speak(self, text):
        self.voice_engine.say(text)
        self.voice_engine.runAndWait()


