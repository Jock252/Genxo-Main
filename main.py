import os
import speech_recognition as sr
import pyttsx3
import openai
import webbrowser
from dotenv import load_dotenv
import time


load_dotenv()
openai.api_key = os.getenv("OPENAI_API_KEY")


engine = pyttsx3.init()
engine.setProperty('rate', 160)

def speak(text):
    print("GENXO:", text)
    engine.say(text)
    engine.runAndWait()


def listen():
    recognizer = sr.Recognizer()
    with sr.Microphone() as source:
        print("🎤 Listening...")
        audio = recognizer.listen(source)
    try:
        command = recognizer.recognize_google(audio)
        print("You said:", command)
        return command.lower()
    except sr.UnknownValueError:
        return ""


def ask_genxo(prompt):
    response = openai.chat.completions.create(
        model="gpt-4",
        messages=[
            {"role": "system", "content": "You are GENXO, a chill AI assistant."},
            {"role": "user", "content": prompt}
        ]
    )
    return response.choices[0].message.content


        
while True:
    command = listen()

    
    if "hello open youtube" in command:
        speak("Yo bro! Opening YouTube for you. What do you wanna watch?")
        webbrowser.open("https://www.youtube.com")
        time.sleep(4)  

        
        search_command = listen()
        if search_command:
            speak(f"Searching YouTube for {search_command}")
            query = search_command.replace(" ", "+")
            search_url = f"https://www.youtube.com/results?search_query={query}"
            webbrowser.open(search_url)
    
    elif command:
        reply = ask_genxo(command)
        speak(reply)
