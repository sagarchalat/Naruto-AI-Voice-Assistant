import speech_recognition as sr
import pyttsx3
import smtplib
import pyjokes
import time
import os
import random
import webbrowser
from datetime import datetime
from email.message import EmailMessage
from googlesearch import search

# Initialize the speech engine
engine = pyttsx3.init()

# Function to convert text to speech
def speak_text(command):
    engine.say(command)
    engine.runAndWait()

# Function to listen to user commands
def listen_command():
    recognizer = sr.Recognizer()
    with sr.Microphone() as source:
        print("Listening...")
        recognizer.pause_threshold = 1
        audio = recognizer.listen(source)

    try:
        print("Recognizing...")
        query = recognizer.recognize_google(audio, language='en-in')
        print(f"User said: {query}")
    except Exception as e:
        print("Sorry, I didn't catch that. Please say that again.")
        return "None"
    
    return query.lower()

# Send Email
def send_email(to_address, subject, body):
    email = EmailMessage()
    email['From'] = 'your_email@gmail.com'
    email['To'] = to_address
    email['Subject'] = subject
    email.set_content(body)

    with smtplib.SMTP_SSL('smtp.gmail.com', 465) as smtp:
        smtp.login('your_email@gmail.com', 'your_app_password')
        smtp.send_message(email)
    speak_text("Email has been sent successfully!")

# Search Weather Online
def get_weather(city):
    speak_text(f"Searching for the weather in {city}.")
    search_query = f"weather in {city}"
    webbrowser.open(f"https://www.google.com/search?q={search_query}")

# Search Music Online (YouTube)
def play_music(song_name):
    speak_text(f"Searching for {song_name} on YouTube.")
    search_query = f"{song_name} song"
    webbrowser.open(f"https://www.youtube.com/results?search_query={search_query}")

# Open Websites
def open_youtube():
    speak_text("Opening YouTube for you!")
    webbrowser.open('https://www.youtube.com')

def open_google():
    speak_text("Opening Google for you!")
    webbrowser.open('https://www.google.com')

# Set Timer
def set_timer(seconds):
    speak_text(f"Setting a timer for {seconds} seconds.")
    time.sleep(seconds)
    speak_text("Time's up!")

# Google Search
def search_google(query):
    speak_text(f"Searching Google for {query}")
    for url in search(query, stop=5):
        print(url)
        speak_text(url)

# Tell a Joke
def tell_joke():
    joke = pyjokes.get_joke()
    speak_text(joke)

# Get Time
def get_time():
    now = datetime.now()
    current_time = now.strftime("%H:%M:%S")
    speak_text(f"The current time is {current_time}")

# Get Date
def get_date():
    today = datetime.now().strftime("%A, %B %d, %Y")
    speak_text(f"Today is {today}")

# Main Program Loop
def main():
    while True:
        command = listen_command()

        if 'play music' in command:
            speak_text('What song would you like to listen to?')
            song_name = listen_command()
            play_music(song_name)

        elif 'weather' in command:
            speak_text('Which city would you like the weather for?')
            city = listen_command()
            get_weather(city)

        elif 'time' in command:
            get_time()

        elif 'date' in command:
            get_date()

        elif 'google' in command:
            open_google()

        elif 'youtube' in command:
            open_youtube()

        elif 'email' in command:
            speak_text('To whom would you like to send an email?')
            to_address = listen_command()
            speak_text('What is the subject?')
            subject = listen_command()
            speak_text('What should the body of the email say?')
            body = listen_command()
            send_email(to_address, subject, body)

        elif 'search' in command:
            speak_text('What would you like to search for?')
            query = listen_command()
            search_google(query)

        elif 'joke' in command:
            tell_joke()

        elif 'timer' in command:
            speak_text('How many seconds?')
            seconds = int(listen_command())
            set_timer(seconds)

        elif 'stop' in command or 'exit' in command:
            speak_text("Goodbye!")
            break

if __name__ == "__main__":
    main()
