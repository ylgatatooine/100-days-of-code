import pyttsx3

engine = pyttsx3.init()
voices = engine.getProperty('voices')
rate = 180

# for voice in voices:
#    engine.setProperty('voice', voice.id)
#    print(voice.id)
#    engine.say( voice.id + 'The quick brown fox jumped over the lazy dog.')
engine.setProperty('voice', 'com.apple.voice.compact.en-GB.Daniel')
engine.setProperty('rate',rate)
engine.say('Why did the computer catch a cold?')
engine.setProperty('rate', rate)
engine.say('Because it left its windows open')
engine.runAndWait()

# engine = pyttsx3.init()
# voices = engine.getProperty('voices')
# engine.setProperty('rate',150)
# engine.setProperty('voice', voices[0].id) #changing index changes voices but ony 0 and 1 are working here
# engine.say('Hello World, Liang Gang')
# engine.runAndWait()