import datetime
import os
import webbrowser

import pyttsx3
import speech_recognition as sr
from google import genai

GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")
if not GEMINI_API_KEY:
    raise SystemExit(
        "Set the GEMINI_API_KEY environment variable before starting JARVIS."
    )

client = genai.Client(api_key=GEMINI_API_KEY)

try:
    engine = pyttsx3.init("espeak")
except Exception:
    engine = pyttsx3.init()

engine.setProperty("rate", 170)


def speak(text: str) -> None:
    """Print a response and read it aloud."""
    print(f"JARVIS: {text}")
    engine.say(text)
    engine.runAndWait()


def ask_gemini(user_prompt: str) -> str:
    """Send a voice prompt to Gemini and return a concise response."""
    try:
        system_instruction = (
            "You are JARVIS, a concise voice assistant. "
            "Keep responses conversational and under three sentences."
        )
        response = client.models.generate_content(
            model="gemini-2.5-flash",
            contents=f"{system_instruction}\n\nUser says: {user_prompt}",
        )
        return response.text or "I did not receive a text response."
    except Exception:
        print("Gemini API request failed.")
        return "I could not connect to the AI service. Please try again."


def wish_me() -> None:
    """Greet the user according to the local time."""
    hour = datetime.datetime.now().hour
    if 0 <= hour < 12:
        speak("Good morning.")
    elif 12 <= hour < 18:
        speak("Good afternoon.")
    else:
        speak("Good evening.")
    speak("AI core is online. Ready for your command.")


def take_command() -> str:
    """Capture and transcribe microphone input."""
    recognizer = sr.Recognizer()
    try:
        with sr.Microphone() as source:
            print("\nListening...")
            recognizer.adjust_for_ambient_noise(source, duration=1)
            recognizer.pause_threshold = 1
            audio = recognizer.listen(source, timeout=8, phrase_time_limit=15)
    except (OSError, sr.WaitTimeoutError):
        speak("The microphone is unavailable or no speech was detected.")
        return ""

    try:
        print("Recognizing...")
        query = recognizer.recognize_google(audio, language="en-US")
        print(f"You said: {query}\n")
        return query.lower()
    except sr.UnknownValueError:
        return ""
    except sr.RequestError:
        speak("Network issue. Please check your internet connection.")
        return ""


def main() -> None:
    wish_me()
    while True:
        query = take_command()
        if not query:
            continue

        if "time" in query:
            current_time = datetime.datetime.now().strftime("%I:%M %p")
            speak(f"The current time is {current_time}")
        elif "open google" in query:
            speak("Opening Google.")
            webbrowser.open("https://www.google.com")
        elif "open youtube" in query:
            speak("Opening YouTube.")
            webbrowser.open("https://www.youtube.com")
        elif "offline" in query or "quit" in query or "goodbye" in query:
            speak("Shutting down. Goodbye.")
            break
        else:
            speak(ask_gemini(query))


if __name__ == "__main__":
    main()
