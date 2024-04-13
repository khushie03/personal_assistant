import streamlit as st
from streamlit_option_menu import option_menu
import wikipedia
from transformers import pipeline

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
    max_length = st.number_input("Enter the word limit:", min_value=10, max_value=10000, step=20)

    def get_wikipedia_content(topic):
        try:
            page_content = wikipedia.page(topic).content
            return page_content
        except wikipedia.exceptions.PageError:
            return "Page not found"

    text = get_wikipedia_content(input_name)
    st.write(text)

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
        outputs = translator(input_text, clean_up_tokenization_spaces=True, min_length=100)
        translated_text = outputs[0]['translation_text']
        st.subheader("Translated Text:")
        st.write(translated_text)

elif selected_page == "WEB SCROLL":
    st.header("Web Scroll")
    st.write("Input the URL of the webpage you want to scroll")
    # Implement webpage scrolling functionality
