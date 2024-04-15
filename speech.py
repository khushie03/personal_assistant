import pyttsx3 as pt
import speech_recognition as sr
from web_direct import InfoScraper , MusicPlayer
from news_extractor import fetch_news
import randfacts
from weather import weather_info
engine = pt.init()
voices = engine.getProperty("voices")
engine.setProperty("voice" , voices[1].id)


def speak(text):
    engine.say(text)
    engine.runAndWait()
    

r = sr.Recognizer()
speak("Hello I am your voice assistant. How are you ")
with sr.Microphone() as source:
    r.energy_threshold = 10000
    r.adjust_for_ambient_noise(source , 1.2)
    print("Listening")
    audio = r.listen(source)
    text = r.recognize_google(audio)
    print(text)

if "what" and "about" and "you" in text:
    speak("I am having a great day")
speak("What can I do for you ")

with sr.Microphone() as source:
    r.energy_threshold = 10000
    r.adjust_for_ambient_noise(source , 1.2)
    print("Listening")
    audio = r.listen(source)
    text2 = r.recognize_google(audio)
    print(text2)

if "information" in text2:
    speak("Information related to which topic")
    with sr.Microphone() as source:
        r.energy_threshold = 10000
        r.adjust_for_ambient_noise(source , 1.2)
        print("Listening")
        audio = r.listen(source)
        infer = r.recognize_google(audio)
    speak("Searching {} on wikipedia".format(infer))
    assist = InfoScraper()
    assist.get_info(infer)
    
elif "play" in text2 and "video" in text2:
    speak("Which video would you like to play?")
    with sr.Microphone() as source:
        r.energy_threshold = 10000
        r.adjust_for_ambient_noise(source, 1.2)
        print("Listening...")
        audio = r.listen(source)
        video_name = r.recognize_google(audio)
        print(video_name)
    speak("Playing {} on YouTube".format(video_name))
    player = MusicPlayer()
    player.play_music(video_name)
    

elif "news" in text2:
    speak("Here is the today news : ")
    arr = fetch_news("your_api_key")
    for i in range(len(arr)):
        speak(arr[i])
        print(arr[i])
    
elif "fact" or "facts" in text2:
    speak("Here are some interesting facts ")
    x = randfacts.get_fact()
    speak("Do you know that"+x)
    
elif "temperature" in text2:
    speak("About which place you would like to know the temperature : ")
    with sr.Microphone() as source:
        r.energy_threshold = 10000
        r.adjust_for_ambient_noise(source , 1.2)
        print("Listening")
        audio = r.listen(source)
        location = r.recognize_google(audio)
    speak("Sure")
    temperature , description = weather_info(location)
    speak("Today temperature of {} is q{}".format(location , temperature))
    speak("and the day is {}".format(description))
