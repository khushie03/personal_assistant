import pyttsx3 as pt
import speech_recognition as sr
from streamlit_option_menu import option_menu
import wikipedia
from transformers import pipeline
import streamlit as st
from web_direct import InfoScraper, MusicPlayer
from news_extractor import fetch_news
import randfacts
from selenium.webdriver.common.by import By
from selenium import webdriver
from weather import weather_info
import keyboard
import time

st.set_page_config(
    page_title="Your Personal Assistant",
    page_icon=":robot_face:",
    layout="wide"
)

st.title("YOUR PERSONAL ASSISTANT")

selected_page = option_menu(
    menu_title=None,
    options=["INFORMATION", "Language Translator", "WEB SCROLL"],
    icons=["chair", "info-circle", "link"],
    orientation="horizontal",
)

st.sidebar.markdown("Interact with the web in a better way and retrieve information in seconds")

if selected_page == "INFORMATION":
    st.header("Retrieve Information")
    input_name = st.text_input("Enter the name of the person or topic:")
    

    def get_wikipedia_content(topic):
        try:
            if topic is None:
                st.write("Please enter your topic")
            page_content = wikipedia.page(topic).content
            return page_content
        except wikipedia.exceptions.PageError:
            return "Page not found"
        except wikipedia.exceptions.WikipediaException as e:
            return f"Wikipedia Exception: {e}"

    text = get_wikipedia_content(input_name)
    
    option = option_menu(menu_title=None,
                         options=["Question - Answering", "Summarizer"],
                         orientation="horizontal")
    if option == "Summarizer":
        st.write(text[:999])
    elif option == "Question - Answering":
        qna = pipeline("question-answering")
        input_question = st.text_input("Enter the question you want to ask : ")
        try:
            if input_question is None:
                st.write("Please write your question")
            else:
                outputs = qna(question=input_question, context=text)
                st.write(outputs["answer"])
        except ValueError as e:
            st.error(f"ValueError: {e}")

elif selected_page == "Language Translator":
    st.header("Language Translator")
    st.write("Input the text you want to translate")
    input_text = st.text_input("Enter the sentence")
    language_pairs = ["English to Russian", "English to Italian", "English to German", "Hindi to English"]
    selected_lang_option = option_menu(menu_title="Select translate: ",
                                       options=language_pairs,
                                       orientation="horizontal",
                                       )

    if selected_lang_option == "English to Russian":
        translator = pipeline("translation_en_to_ru", model="Helsinki-NLP/opus-mt-en-ru")
    elif selected_lang_option == "English to Italian":
        translator = pipeline("translation_en_to_it", model="Helsinki-NLP/opus-mt-en-it")
    elif selected_lang_option == "Hindi to English":
        translator = pipeline("translation_mt_to_hi", model="Helsinki-NLP/opus-mt-hi-en")
    elif selected_lang_option == "English to German":
        translator = pipeline("translation_en_to_de", model="Helsinki-NLP/opus-mt-en-de")

    if input_text:
        try:
            outputs = translator(input_text, clean_up_tokenization_spaces=True, min_length=100)
            translated_text = outputs[0]['translation_text']
            st.subheader("Translated Text:")
            st.write(translated_text)
        except Exception as e:
            st.error(f"Translation Error: {e}")
        
elif selected_page == "WEB SCROLL":
    st.header("Web Scroll")
    select_options = option_menu(
        menu_title="Choose ",menu_icon= ":robot_face:",
        options=["Talk with me", "Not right now"]
    )
    if select_options == "Talk with me":
        def speak(text):
            engine.say(text)
            engine.runAndWait()
        
        if st.button("Start Listening"):
            engine = pt.init()
            voices = engine.getProperty("voices")
            engine.setProperty("voice", voices[1].id)
            speak("Hello, I am your voice assistant. How are you?")
            r = sr.Recognizer()
            with sr.Microphone() as source:
                r.energy_threshold = 10000
                r.adjust_for_ambient_noise(source, 1.2)
                st.write("Listening.....")
                audio = r.listen(source)
                text = r.recognize_google(audio)
                st.write(text)
                
            if "what" in text and "about" in text:
                speak("I am having a great day too")
                #st.write("I am having a great day too")
                
            speak("What can I do for you")
            #st.write("What can I do for you")
            text2 = ""
            i = 0
            while i < 100:
                with sr.Microphone() as source:
                    r.energy_threshold = 10000
                    r.adjust_for_ambient_noise(source, 1.2)
                    st.write("Listening........")
                    audio = r.listen(source)
                    text2 = r.recognize_google(audio)
                    st.write(text2)
                    i = i +1
                
                if "nothing" in text2:
                    speak("Thankyou")
                    
                elif "information" in text2:
                    speak("Information related to which topic")
                    with sr.Microphone() as source:
                        r.energy_threshold = 10000
                        r.adjust_for_ambient_noise(source, 1.2)
                        st.write("Listening......")
                        audio = r.listen(source)
                        infer = r.recognize_google(audio)
                    st.write(infer)
                    speak("Searching {} on Wikipedia".format(infer))
                    assist = InfoScraper()
                    assist.get_info(infer)
                    
                elif "play" in text2 and "video" in text2:
                    speak("Which video would you like to play?")
                    with sr.Microphone() as source:
                        r.energy_threshold = 10000
                        r.adjust_for_ambient_noise(source, 1.2)
                        st.write("Listening...")
                        audio = r.listen(source)
                        video_name = r.recognize_google(audio)
                        st.write("Playing  "+video_name)
                    speak("Playing {} on YouTube".format(video_name))
                    player = MusicPlayer()
                    player.play_music(video_name)
                    
                elif "news" in text2:
                    speak("Here is the today news : ")
                    arr = fetch_news("ad8873e8f2e84c34a4cac06f8316a31d")
                    for i in range(len(arr)):
                        speak(arr[i])
                        print(arr[i])
                    
                        
                elif "fact" in text2 or "facts" in text2:
                    speak("Here are some interesting facts ")
                    x = randfacts.get_fact()
                    speak("Do you know that " + x)
                    st.empty()
                    print("Done")
                    
                elif "temperature" in text2:
                    speak("About which place you would like to know the temperature : ")
                    with sr.Microphone() as source:
                        r.energy_threshold = 10000
                        r.adjust_for_ambient_noise(source, 1.2)
                        st.write("Listening.....")
                        audio = r.listen(source)
                        location = r.recognize_google(audio)
                    speak("Sure")
                    temperature, description = weather_info(location)
                    speak("Today temperature of {} is {}".format(location, temperature))
                    speak("and the day is {}".format(description))
                    print("temperature")
            
                elif text2.lower() in ["exit" , "stop"]:
                    speak("Thankyou for your time")
                    break
                
                else:
                    st.write("Listening.....Redirecting you to Google")
                    query = text2
                    speak("Sure wait a second : ")
                    driver = webdriver.Chrome()
                    driver.get("https://www.google.com")
                    search_input = driver.find_element(By.XPATH, '//*[@id="APjFqb"]')
                    search_input.send_keys(query)
                    search_input.submit()
                    time.sleep(5)
                    print("Press 'Q' to exit the browser.")
                    while True:
                        if keyboard.is_pressed('q'):
                            driver.quit() 
                            speak("Browser closed.")
                            print("Browser closed.")
                            break
                
                  
            
            
                        
                
    if select_options == "Not right now":
        st.write("Never mind. Have a great day")
        
st.markdown("---")
st.write("© 2024 Your Personal Assistant")
