import speech_recognition as sr
import requests
import os
from gtts import gTTS
from pydub import AudioSegment
from pydub.playback import play
from io import BytesIO # <-- Import this for in-memory files

# --- Settings ---
RASA_SERVER_URL = "http://localhost:5005/webhooks/rest/webhook"
BOT_NAME = "Mai"
USER_NAME = "boss"

def speak(text):
    """Converts text to speech and plays it directly from memory for speed."""
    try:
        print(f"{BOT_NAME}: {text}")
        
        # --- THIS IS THE FASTER METHOD ---
        # 1. Create an in-memory file (a buffer)
        mp3_fp = BytesIO()
        
        # 2. Create the gTTS object and write the audio data directly to memory
        tts = gTTS(text=text, lang='ja', slow=False)
        tts.write_to_fp(mp3_fp)
        
        # 3. "Rewind" the in-memory file to the beginning
        mp3_fp.seek(0)
        
        # 4. Load the audio from memory and play it
        audio = AudioSegment.from_mp3(mp3_fp)
        play(audio)
        # No more saving or deleting files!

    except Exception as e:
        print(f"Error in text-to-speech: {e}")

def listen():
    """Listens for user input from the microphone and returns it as text."""
    r = sr.Recognizer()
    with sr.Microphone() as source:
        print("Listening...")
        r.pause_threshold = 1
        r.adjust_for_ambient_noise(source)
        audio = r.listen(source)

    try:
        print("Recognizing...")
        query = r.recognize_google(audio, language='en-in') # Listens for English
        print(f"{USER_NAME}: {query}\n")
        return query.lower()
    except sr.UnknownValueError:
        speak("Gomen'nasai, I couldn't quite hear you.")
        return ""
    except sr.RequestError as e:
        speak("It seems I'm having trouble connecting to my recognition service.")
        return ""
    except Exception as e:
        print(f"An error occurred: {e}")
        return ""

def main_loop():
    """The main loop to run the voice assistant."""
    speak(f"Konnichiwa, I'm {BOT_NAME}, your personal assistant.")
    
    while True:
        user_input = listen()

        if not user_input:
            continue

        if "exit" in user_input or "quit" in user_input:
            speak("Hai! Sayonara, boss!")
            break

        try:
            response = requests.post(
                RASA_SERVER_URL,
                json={"sender": USER_NAME, "message": user_input}
            )
            response.raise_for_status()
            
            bot_responses = response.json()
            if bot_responses:
                for r in bot_responses:
                    speak(r.get("text"))
            else:
                speak("Sumimasen, I don't have a response for that yet.")
        except requests.exceptions.RequestException as e:
            speak("I'm sorry, I can't seem to reach my brain right now. Please make sure the Rasa server is running.")
            print(f"Connection Error: {e}")


if __name__ == "__main__":
    main_loop()
