# Naruto AI Voice Assistant

An AI-powered voice assistant inspired by the spirit of Naruto — energetic, mission-driven, and always ready to help. Built with speech recognition and text-to-speech, it can answer questions, check the weather, play music, send emails, set timers, and more, all through voice commands.

## Features

- 🎙️ **Voice-controlled** — talk to it naturally using your microphone
- 🔥 **Wake word activation** — say "Naruto" before your command so it doesn't respond to background noise
- ⏰ **Non-blocking timers** — set a timer and keep giving commands while it counts down
- 📧 **Email sending** — dictate a recipient, subject, and message
- 🌦️ **Weather lookup** — opens live weather results for any city
- 🎵 **Music search** — finds and opens songs on YouTube
- 🔍 **Google search** — searches and reads back top results
- 😄 **Jokes** — a quick laugh, ninja-style
- 🕐 **Time & date** — quick spoken lookups

## Requirements

- Python 3.8+
- A working microphone
- The following Python packages:

```
pip install SpeechRecognition pyttsx3 pyjokes googlesearch-python python-dotenv pyaudio
```

> **Note:** `pyaudio` can be tricky to install on some systems.
> - **Windows:** `pip install pyaudio` usually works directly.
> - **macOS:** install `portaudio` first — `brew install portaudio`, then `pip install pyaudio`.
> - **Linux:** `sudo apt-get install python3-pyaudio` or install `portaudio19-dev` before pip installing.

## Setup

1. Clone or download this repository.
2. Install the dependencies above.
3. Create a `.env` file in the project's root directory (same folder as the script) with your email credentials:

   ```
   EMAIL_ADDRESS=your_email@gmail.com
   EMAIL_APP_PASSWORD=your_app_password
   ```

   > For Gmail, you'll need an **App Password**, not your regular password. Enable 2-Step Verification on your Google account, then generate an App Password under Google Account → Security → App Passwords.

4. Run the assistant:

   ```
   python naruto_ai_voice_assistant.py
   ```

## Usage

Once running, the assistant listens continuously. Say the wake word **"Naruto"** followed by your command:

| Say something like...                          | It will...                              |
|-------------------------------------------------|------------------------------------------|
| "Naruto, what time is it?"                       | Tell you the current time                |
| "Naruto, what's today's date?"                   | Tell you today's date                    |
| "Naruto, play music"                             | Ask for a song, then search it on YouTube|
| "Naruto, what's the weather?"                    | Ask for a city, then open weather results|
| "Naruto, open YouTube" / "open Google"           | Opens the site in your browser           |
| "Naruto, search for something"                   | Runs a Google search and reads results   |
| "Naruto, send an email"                          | Walks you through recipient, subject, body |
| "Naruto, set a timer"                            | Asks for seconds, then counts down       |
| "Naruto, tell me a joke"                         | Tells a joke                             |
| "Naruto, stop" / "exit" / "goodbye"              | Shuts down the assistant                 |

## Project Structure

```
.
├── naruto_ai_voice_assistant.py   # Main assistant script
├── .env                           # Your email credentials (not committed to git)
└── README.md                      # This file
```

## Security Notes

- Never commit your `.env` file to version control. Add it to `.gitignore`.
- The assistant validates email addresses with basic format checking before sending, but always double-check spoken input before confirming a send.
- Google's free speech recognition API (`recognize_google`) is rate-limited and unofficial — fine for personal projects, but not guaranteed for production use.

## Known Limitations

- Requires an active internet connection (speech recognition and search rely on Google's services).
- Voice recognition accuracy depends on your microphone quality and background noise.
- Currently supports English (India locale, `en-in`) — change the `language` parameter in `listen()` to adjust.

## Roadmap Ideas

- Add more ninja-themed easter egg responses
- Support offline speech recognition (e.g., Vosk or Whisper) for reliability
- Add calendar/reminder integration
- Add a simple GUI status indicator

## License

This project is provided as-is for personal and educational use.

---

*"Believe it!" — built in the ninja way.* 🍥
