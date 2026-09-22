"""
Naruto AI Voice Assistant
--------------------------
A voice assistant themed around the spirit of Naruto: ninja missions,
jutsu-style commands, and a determined, energetic personality.

Setup:
    pip install SpeechRecognition pyttsx3 pyjokes googlesearch-python python-dotenv pyaudio

    Create a `.env` file next to this script with:
        EMAIL_ADDRESS=your_email@gmail.com
        EMAIL_APP_PASSWORD=your_app_password

Say the wake word "Naruto" before a command, e.g. "Naruto, what time is it?"
"""

import os
import re
import time
import random
import logging
import threading
import webbrowser
from datetime import datetime
from email.message import EmailMessage
import smtplib

import speech_recognition as sr
import pyttsx3
import pyjokes
from googlesearch import search
from dotenv import load_dotenv

# ------------------------------------------------------------------
# Setup
# ------------------------------------------------------------------
load_dotenv()

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(message)s",
)
log = logging.getLogger("naruto-assistant")

EMAIL_ADDRESS = os.environ.get("EMAIL_ADDRESS")
EMAIL_APP_PASSWORD = os.environ.get("EMAIL_APP_PASSWORD")

WAKE_WORD = "naruto"

engine = pyttsx3.init()
engine.setProperty("rate", 180)

GREETINGS = [
    "Alright, I'm on the mission! Believe it!",
    "You called? Let's get this done!",
    "Ready for action, dattebayo!",
]

SIGN_OFFS = [
    "Mission complete!",
    "Jutsu executed successfully!",
    "That's my ninja way!",
]

NINJA_JOKES_INTRO = [
    "Here's a laugh, straight from the Hidden Leaf Village:",
    "Even Kakashi-sensei would chuckle at this one:",
]


# ------------------------------------------------------------------
# Core speech I/O
# ------------------------------------------------------------------
def speak(text: str) -> None:
    """Speak text aloud and print it for visibility/debugging."""
    print(f"Naruto-AI: {text}")
    try:
        engine.say(text)
        engine.runAndWait()
    except Exception as e:
        log.error(f"TTS failed: {e}")


def listen(prompt: str = None) -> str:
    """Listen to the microphone and return recognized text (lowercase),
    or an empty string if nothing usable was heard."""
    if prompt:
        speak(prompt)

    recognizer = sr.Recognizer()
    try:
        with sr.Microphone() as source:
            print("Listening...")
            recognizer.pause_threshold = 1
            recognizer.adjust_for_ambient_noise(source, duration=0.5)
            audio = recognizer.listen(source, timeout=8, phrase_time_limit=10)
    except sr.WaitTimeoutError:
        log.info("No speech detected in time.")
        return ""
    except Exception as e:
        log.error(f"Microphone error: {e}")
        return ""

    try:
        query = recognizer.recognize_google(audio, language="en-in")
        print(f"You said: {query}")
        return query.lower().strip()
    except sr.UnknownValueError:
        speak("Sorry, I didn't catch that. Say it again, believe it!")
        return ""
    except sr.RequestError as e:
        log.error(f"Speech recognition service error: {e}")
        speak("My ninja senses are offline right now — speech service isn't responding.")
        return ""


# ------------------------------------------------------------------
# Feature: Jutsu (commands)
# ------------------------------------------------------------------
def send_email(to_address: str, subject: str, body: str) -> None:
    if not EMAIL_ADDRESS or not EMAIL_APP_PASSWORD:
        speak("I can't send scrolls yet — email credentials aren't configured.")
        return

    if not re.match(r"[^@]+@[^@]+\.[^@]+", to_address):
        speak(f"That doesn't look like a valid address: {to_address}. Mission aborted.")
        return

    email = EmailMessage()
    email["From"] = EMAIL_ADDRESS
    email["To"] = to_address
    email["Subject"] = subject
    email.set_content(body)

    try:
        with smtplib.SMTP_SSL("smtp.gmail.com", 465) as smtp:
            smtp.login(EMAIL_ADDRESS, EMAIL_APP_PASSWORD)
            smtp.send_message(email)
        speak("Scroll delivered! Email sent successfully.")
    except Exception as e:
        log.error(f"Email send failed: {e}")
        speak("My message scroll got lost on the way. The email failed to send.")


def get_weather(city: str) -> None:
    speak(f"Scouting the weather conditions in {city}.")
    webbrowser.open(f"https://www.google.com/search?q=weather+in+{city}")


def play_music(song_name: str) -> None:
    speak(f"Summoning {song_name} on YouTube!")
    webbrowser.open(f"https://www.youtube.com/results?search_query={song_name}+song")


def open_youtube() -> None:
    speak("Opening YouTube — dattebayo!")
    webbrowser.open("https://www.youtube.com")


def open_google() -> None:
    speak("Opening Google for you!")
    webbrowser.open("https://www.google.com")


def search_google(query: str) -> None:
    speak(f"Searching the ninja archives for {query}.")
    try:
        results = list(search(query, num_results=5))
        if not results:
            speak("No scrolls found on that topic.")
            return
        for url in results:
            print(url)
        speak(f"I found {len(results)} results — check your screen.")
    except Exception as e:
        log.error(f"Search failed: {e}")
        speak("The search jutsu failed. Try again in a moment.")


def tell_joke() -> None:
    speak(random.choice(NINJA_JOKES_INTRO))
    speak(pyjokes.get_joke())


def get_time() -> None:
    now = datetime.now().strftime("%H:%M:%S")
    speak(f"The current time is {now}.")


def get_date() -> None:
    today = datetime.now().strftime("%A, %B %d, %Y")
    speak(f"Today is {today}.")


def set_timer(seconds: int) -> None:
    """Non-blocking timer so the assistant can keep listening."""
    speak(f"Setting a {seconds}-second timer. I'll alert you when it's up!")

    def alert():
        speak("Time's up! Your jutsu has finished charging!")

    threading.Timer(seconds, alert).start()


def parse_seconds(text: str) -> int:
    """Extract the first integer found in spoken text; raises ValueError if none."""
    match = re.search(r"\d+", text)
    if not match:
        raise ValueError("no number found")
    return int(match.group())


# ------------------------------------------------------------------
# Command dispatch table
# ------------------------------------------------------------------
def handle_music():
    song = listen("What song would you like to hear?")
    if song:
        play_music(song)


def handle_weather():
    city = listen("Which city's weather would you like?")
    if city:
        get_weather(city)


def handle_email():
    to_address = listen("Who should I send this scroll to? Please say the email address.")
    subject = listen("What's the subject?")
    body = listen("What should the message say?")
    if to_address and subject and body:
        send_email(to_address, subject, body)
    else:
        speak("Missing info — email mission aborted.")


def handle_search():
    query = listen("What would you like to search for?")
    if query:
        search_google(query)


def handle_timer():
    raw = listen("How many seconds should the timer run for?")
    try:
        seconds = parse_seconds(raw)
        set_timer(seconds)
    except ValueError:
        speak("I couldn't hear a number there. Timer jutsu failed.")


COMMANDS = {
    "play music": handle_music,
    "weather": handle_weather,
    "time": get_time,
    "date": get_date,
    "google": open_google,
    "youtube": open_youtube,
    "email": handle_email,
    "search": handle_search,
    "joke": tell_joke,
    "timer": handle_timer,
}

# Order matters: check more specific / longer phrases before shorter
# substrings that might be contained within them (e.g. "timer" vs "time").
COMMAND_ORDER = [
    "play music",
    "timer",
    "weather",
    "email",
    "search",
    "youtube",
    "google",
    "joke",
    "date",
    "time",
]


def dispatch(command: str) -> bool:
    """Match command text against known keywords in priority order.
    Returns True if handled, False otherwise."""
    for keyword in COMMAND_ORDER:
        if keyword in command:
            COMMANDS[keyword]()
            return True
    return False


# ------------------------------------------------------------------
# Main loop
# ------------------------------------------------------------------
def main():
    speak("Naruto AI Assistant activated. Say 'Naruto' followed by your command!")

    while True:
        try:
            heard = listen()
            if not heard:
                continue

            if WAKE_WORD not in heard:
                continue

            command = heard.replace(WAKE_WORD, "", 1).strip(" ,.")

            if not command:
                speak(random.choice(GREETINGS))
                command = listen("Go ahead, I'm listening!")

            if any(word in command for word in ("stop", "exit", "goodbye")):
                speak("See you next time — believe it!")
                break

            handled = dispatch(command)
            if not handled:
                speak("I don't know that jutsu yet. Try another command!")
            else:
                print(f"({random.choice(SIGN_OFFS)})")

        except KeyboardInterrupt:
            speak("Shutting down. Catch you later!")
            break
        except Exception as e:
            log.error(f"Unexpected error: {e}")
            speak("Something went wrong on my end, but I'm still here!")


if __name__ == "__main__":
    main()
