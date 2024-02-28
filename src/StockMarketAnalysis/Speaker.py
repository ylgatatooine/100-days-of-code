import pyttsx3
import datetime

engine = pyttsx3.init()
voices = engine.getProperty('voices')
rate = 180
engine.setProperty('voice', 'com.apple.voice.compact.en-GB.Daniel')
engine.setProperty('rate', rate)


def speak(audio):
    engine.say(audio)
    engine.runAndWait()


def wishme():
    hour = int(datetime.datetime.now().hour)

    if 0 <= hour < 12:
        speak("Good Morning! It is " + hour + "o'clock.")
    elif 12 <= hour < 18:
        speak("Good Afternoon! It is " + hour + "o'clock.")
    else:
        speak("Good Evening! It is " + hour + "o'clock.")


speak('Hello, this is your artificial intelligence assistant. Robert. ')

strTime = datetime.datetime.now().strftime("%H:%M:%S")
speak(f"Sir, the time is {strTime}")

# engine = pyttsx3.init()
# voices = engine.getProperty('voices')
# engine.setProperty('rate',150)
# engine.setProperty('voice', voices[0].id) #changing index changes voices but ony 0 and 1 are working here
# engine.say('Hello World, Liang Gang')
# engine.runAndWait()
