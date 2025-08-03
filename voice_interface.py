import speech_recognition as sr
import requests
import os
from gtts import gTTS
from pydub import AudioSegment
from pydub.playback import play
from io import BytesIO
import tkinter as tk
from PIL import Image, ImageTk
import threading
import time

# --- Settings ---
RASA_SERVER_URL = "http://localhost:5005/webhooks/rest/webhook"
BOT_NAME = "Mai"
USER_NAME = "boss"
MAI_IMAGE_URL = "https://i.imgur.com/p5A5i7g.png" # A friendly anime assistant image

def show_mai_graphic():
    """Creates a frameless pop-up window to display Mai. MUST RUN IN MAIN THREAD."""
    try:
        root = tk.Tk()
        root.attributes('-topmost', True)
        root.overrideredirect(True) 

        headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.3'}
        response = requests.get(MAI_IMAGE_URL, headers=headers)
        response.raise_for_status()
        
        img_data = response.content
        img = Image.open(BytesIO(img_data))
        img.thumbnail((400, 400))
        photo = ImageTk.PhotoImage(img)

        label = tk.Label(root, image=photo, bd=0)
        label.pack()

        root.update_idletasks()
        width = root.winfo_width()
        height = root.winfo_height()
        x = (root.winfo_screenwidth() // 2) - (width // 2)
        y = (root.winfo_screenheight() // 2) - (height // 2)
        root.geometry(f'{width}x{height}+{x}+{y}')
        
        root.after(4000, root.destroy)
        
        root.mainloop()

    except Exception as e:
        print(f"Could not display graphic. Make sure 'python3.10-tkinter' and 'Pillow' are installed. Error: {e}")

def speak(text):
    """Converts text to speech and plays it directly from memory."""
    try:
        print(f"{BOT_NAME}: {text}")
        mp3_fp = BytesIO()
        tts = gTTS(text=text, lang='ja', slow=False)
        tts.write_to_fp(mp3_fp)
        mp3_fp.seek(0)
        audio = AudioSegment.from_mp3(mp3_fp)
        play(audio)
    except Exception as e:
        print(f"Error in text-to-speech: {e}")

def listen():
    """Listens for user input from the microphone."""
    r = sr.Recognizer()
    with sr.Microphone() as source:
        print("Listening...")
        r.pause_threshold = 1
        r.adjust_for_ambient_noise(source)
        audio = r.listen(source)

    try:
        print("Recognizing...")
        query = r.recognize_google(audio, language='en-in')
        print(f"{USER_NAME}: {query}\n")
        return query.lower()
    except sr.UnknownValueError:
        speak("Gomen'nasai, I couldn't quite hear you.")
        return ""
    except sr.RequestError:
        speak("It seems I'm having trouble connecting to my recognition service.")
        return ""
    except Exception as e:
        print(f"An error occurred: {e}")
        return ""

def bot_logic_loop():
    """The main logic loop for the assistant (runs in a background thread)."""
    # Wait a moment for the graphic to appear before speaking
    time.sleep(1)
    speak(f"Konnichiwa, I'm {BOT_NAME}, your personal assistant.")
    
    while True:
        user_input = listen()

        if not user_input:
            continue

        if "exit" in user_input or "quit" in user_input:
            speak("Hai! Sayonara, boss!")
            break # This will end the loop and the thread will terminate

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
            break # Exit if we can't connect to Rasa

if __name__ == "__main__":
    # --- This is the new, more robust startup sequence ---

    # 1. Create a thread for the bot's logic (listening/speaking)
    bot_thread = threading.Thread(target=bot_logic_loop)
    bot_thread.daemon = True # Allows the main program to exit

    # 2. Start the bot logic in the background
    bot_thread.start()

    # 3. Run the GUI splash screen in the main thread (most reliable method)
    show_mai_graphic()

    # 4. Wait for the bot logic thread to finish. 
    # Since the loop inside only breaks when the user says "exit",
    # this will keep the program alive until then.
    bot_thread.join()

    print("--- Mai has shut down. ---")
