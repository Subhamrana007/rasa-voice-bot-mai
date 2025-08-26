
# Mai (舞) – Voice-Based Rasa AI Assistant

Mai isn’t your average bot—she’s a voice-powered AI assistant with a Japanese-inspired personality. Built with Python and Rasa Open Source, she listens in English, responds with gTTS (Japanese accent vibes included), and works across **Linux, macOS, and Windows**.

---

##  Features

- **Voice-Activated** – Speak commands, Mai listens and responds aloud  
- **Personality** – Uses Japanese honorifics and phrases to feel lively  
- **Cross-Platform** – Runs smoothly on Linux, macOS, and Windows  
- **Fast & Light** – In-memory audio processing keeps responsiveness on point  
- **Custom Startup** – Slick graphical loading screen for that polished touch  

---

##  Tech Stack

| Component            | Used Tools                          |
|----------------------|-------------------------------------|
| Core Framework       | Rasa Open Source                    |
| Speech-to-Text       | SpeechRecognition                   |
| Text-to-Speech       | gTTS (Google Text-to-Speech)        |
| Audio Playback       | pydub                               |
| Language             | Python 3.10                         |
| OS Support           | Linux, macOS, Windows               |

---

##  Setup & Run Instructions

### 1. Clone Repo
```bash
git clone https://github.com/Subhamrana007/rasa-voice-bot-mai.git
cd rasa-voice-bot-mai
````

### 2. Install System Dependencies

**Linux (Fedora)**

```bash
sudo dnf install portaudio-devel python3.10-devel gcc ffmpeg
```

**macOS** (via Homebrew)

```bash
brew install portaudio ffmpeg
```

**Windows**
Install `ffmpeg` via Chocolatey and prepare for potential PyAudio issues (use prebuilt wheel if needed).

### 3. Set Up Python Environment

```bash
python3.10 -m venv venv
source venv/bin/activate   # On Windows: .\venv\Scripts\activate
pip install -r requirements.txt
```

### 4. Train the Rasa Model

```bash
rasa train
```

### 5. Run the Assistant

Open **two terminals**:

**Terminal 1**

```bash
rasa run --enable-api --cors "*"
```

**Terminal 2**

```bash
python voice_interface.py
```

Mai will greet you—then you can speak things like “Hello,” “Tell me a Japanese word,” or “Exit” to shut her down.

---

## Ideas for Future Work

* Add more personality layers or regional accents
* Use faster ASR/TTS models (like Whisper or Silero)
* Build a GUI for visual interaction
* Dockerize the setup for easier deployment
* Add tests and CI workflow (looking at that Rasa train/test GitHub Action setup) ([DEV Community][1])

---

## License

MIT License – feel free to build on this or remix it.

---

## About

**Mai (舞)** is a personal project by **Shubham Rana** to flex my skills in conversational AI, voice-powered interactions, and cross-platform Python apps. Powered by Rasa and built with authenticity and personality. Feedback, collabs, or even memes—always welcome!

---

