import os
import speech_recognition as sr
import pyttsx3
import openai
import webbrowser
from dotenv import load_dotenv
import time

# 🔑 Load environment variables (like your OpenAI API key)
load_dotenv()
openai.api_key = os.getenv("OPENAI_API_KEY")

# 🎙️ Initialize text-to-speech engine
engine = pyttsx3.init()
engine.setProperty('rate', 160)  # Set voice speed (words per minute)


# 🗣️ Function to speak text aloud + print it in console
def speak(text):
    print("GENXO:", text)
    engine.say(text)
    engine.runAndWait()


# 👂 Function to listen to microphone input and convert speech → text
def listen():
    recognizer = sr.Recognizer()
    with sr.Microphone() as source:
        print("🎤 Listening...")
        audio = recognizer.listen(source)  # Capture audio from mic
    
    try:
        # Try to recognize speech using Google Speech Recognition
        command = recognizer.recognize_google(audio)
        print("You said:", command)
        return command.lower()
    except sr.UnknownValueError:
        # If nothing is recognized, return empty string
        return ""


# 🤖 Function to ask OpenAI (GENXO personality) for a response
def ask_genxo(prompt):
    response = openai.chat.completions.create(
        model="gpt-4",   # Model used (you could swap with "gpt-5" when supported)
        messages=[
            {"role": "system", "content": "You are GENXO, a chill AI assistant."},
            {"role": "user", "content": prompt}
        ]
    )
    return response.choices[0].message.content


# 🚀 Main loop: constantly listens for commands
while True:
    command = listen()  # Wait for user voice input

    # 🎬 If user says "hello open youtube"
    if "hello open youtube" in command:
        speak("Yo bro! Opening YouTube for you. What do you wanna watch?")
        webbrowser.open("https://www.youtube.com")  # Open YouTube homepage
        time.sleep(4)  # Give it a few seconds to load

        # 🎯 Listen again for search query
        search_command = listen()
        if search_command:
            speak(f"Searching YouTube for {search_command}")
            query = search_command.replace(" ", "+")
            search_url = f"https://www.youtube.com/results?search_query={query}"
            webbrowser.open(search_url)  # Open YouTube search results
    
    # 💬 If user says something else, ask GENXO (ChatGPT)
    elif command:
        reply = ask_genxo(command)
        speak(reply)
