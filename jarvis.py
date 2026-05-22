import datetime
import os
import speech_recognition as sr
import pyttsx3
import webbrowser
from google import genai

# Initialize Text-to-Speech Engine
try:
    engine = pyttsx3.init('espeak')
except Exception:
    engine = pyttsx3.init()

engine.setProperty('rate', 170)

# ─── PUT YOUR REAL GEMINI API KEY INSIDE THESE QUOTES ───
client = genai.Client(api_key="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") 

def speak(text):
    """Prints the response and uses native Linux text-to-speech."""
    print(f"JARVIS: {text}")
    engine.say(text)
    engine.runAndWait()

def ask_gemini(user_prompt):
    """Sends the voice prompt to Gemini and gets a concise response."""
    try:
        system_instruction = (
            "You are JARVIS, Tony Stark's sarcastic yet fiercely loyal AI assistant. "
            "Keep all responses very conversational, short, and brief (under 2-3 sentences) "
            "because your output is being read out loud via text-to-speech."
        )
        # CHANGED MODEL HERE TO 1.5-FLASH FOR HIGH STABILITY
        response = client.models.generate_content(
            model="gemini-1.5-flash", 
            contents=f"{system_instruction}\n\nUser says: {user_prompt}"
        )
        return response.text
    except Exception as e:
        print(f"API Error: {e}")
        return "I encountered an error connecting to my core brain, Boss."

def wish_me():
    """Greets you contextually based on the time."""
    hour = int(datetime.datetime.now().hour)
    if 0 <= hour < 12:
        speak("Good morning, Boss.")
    elif 12 <= hour < 18:
        speak("Good afternoon, Boss.")
    else:
        speak("Good evening, Boss.")
    speak("AI core is online. Ready for your command.")

def take_command():
    """Captures microphone input using Ubuntu's sound stream."""
    recognizer = sr.Recognizer()
    with sr.Microphone() as source:
        print("\nListening...")
        recognizer.adjust_for_ambient_noise(source, duration=1)
        recognizer.pause_threshold = 1 
        audio = recognizer.listen(source)

    try:
        print("Recognizing...")
        query = recognizer.recognize_google(audio, language='en-US')
        print(f"You said: {query}\n")
    except sr.UnknownValueError:
        return "none"
    except sr.RequestError:
        speak("Network issue. Please verify your internet connection.")
        return "none"
        
    return query.lower()

if __name__ == "__main__":
    wish_me()
    
    while True:
        query = take_command()

        if 'none' in query:
            continue

        # System Commands
        if 'time' in query:
            str_time = datetime.datetime.now().strftime("%I:%M %p")
            speak(f"The current time is {str_time}")

        elif 'open google' in query:
            speak("Opening Google.")
            webbrowser.open("https://google.com")

        elif 'open youtube' in query:
            speak("Opening Youtube.")
            webbrowser.open("https://youtube.com")

        elif 'open terminal' in query:
            speak("Opening a new terminal window.")
            os.system("gnome-terminal &")

        elif 'offline' in query or 'quit' in query or 'goodbye' in query:
            speak("Powering down systems. Goodbye, Boss.")
            break
            
        # AI Brain
        else:
            ai_response = ask_gemini(query)
            speak(ai_response)