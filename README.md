
# 🌸 Mai (舞) — My AI Rasa Voice Bot  
**By Rana (a.k.a Boss 🤘)**  

Yo fam, welcome to **Mai** — your personal voice-based AI assistant with a whole lotta *personality*. She’s got the vibes of Japan, speaks with a Japanese accent, and talks back in real time. No typing, no clicking — just you, your mic, and a dope AI convo.  

This project was built from scratch using **Python** and **Rasa Open Source**, to help me level up in voice AI, NLP, and full-stack Python dev. Whether you’re here to learn or just vibe with an AI that actually feels alive, Mai’s got you.

## ✨ Features That Slap

- 🎤 **Voice-Activated**  
  Talk naturally — Mai listens and responds, no keyboard needed.

- 💃 **Full-On Personality**  
  She’s not just another boring bot. Think of her like your anime bestie — with casual Japanese phrases and a chill tone.

- 💻 **Cross-Platform**  
  Linux, Mac, Windows — doesn’t matter. She runs smooth everywhere.

- ⚡ **Instant Replies**  
  No annoying lag. All audio is processed in-memory, so she responds on the fly.

## 🧠 Tech Stack — What’s Under Mai’s Hood

| Component         | Tech Used              | Description |
|------------------|------------------------|-------------|
| 🤖 Bot Framework  | Rasa Open Source       | Handles the brainy part — NLP & dialogue management. |
| 🧏 Speech-to-Text | SpeechRecognition      | Converts your voice to text. |
| 🗣️ Text-to-Speech | gTTS (Google TTS)      | Converts her replies into voice. |
| 🔊 Audio Playback | pydub + ffmpeg         | Plays Mai’s responses in real time. |
| 🐍 Core Language   | Python 3.10            | Ties everything together. |

## 🚀 Setup — Run Mai on Your Own Machine

### 1. 📦 Clone the Repo
```bash
git clone https://github.com/your-username/rasa-voice-bot-mai.git
cd rasa-voice-bot-mai
```

### 2. 📋 Install the Prerequisites  

#### 🐧 Linux (Fedora/Ubuntu)
```bash
sudo dnf install portaudio-devel python3.10-devel gcc ffmpeg
```

#### 🍎 macOS (via Homebrew)
```bash
brew install portaudio ffmpeg
```

#### 🪟 Windows
- Install Chocolatey: https://chocolatey.org/install  
```bash
choco install ffmpeg
```
> **⚠️ Windows Note:**  
PyAudio might give you a hard time. If `pip install` fails, grab a pre-built `.whl` from [Gohlke’s unofficial Python libs](https://www.lfd.uci.edu/~gohlke/pythonlibs/#pyaudio).

### 3. 🐍 Python Environment

Set up a virtual environment:

```bash
python3.10 -m venv venv
```

Activate it:

- Linux/macOS:
  ```bash
  source venv/bin/activate
  ```
- Windows:
  ```bash
  .\venv\Scripts\activate
  ```

Then install all dependencies:

```bash
pip install -r requirements.txt
```

### 4. 🧠 Train the Bot (Give Her a Brain)
```bash
rasa train
```

## ▶️ Run Mai!

Open **two terminals**:

### Terminal 1 — Run the Rasa Server
```bash
rasa run --enable-api --cors "*"
```

### Terminal 2 — Fire Up the Voice Interface
```bash
python voice_interface.py
```

Mai will greet you with a “Konnichiwa~” and start listening 👂

## 💬 Try Talking To Her

Here’s some stuff you can say:

- "Hello"
- "How are you?"
- "Who made you?"
- "Teach me a Japanese word"
- "Exit" (to shut her down gracefully)

## 💡 Future Plans
- [ ] Add Whisper or faster ASR models for better STT  
- [ ] Switch from gTTS to local TTS (like Coqui or EdgeTTS)  
- [ ] Add hotword detection (like “Hey Mai”)  
- [ ] GUI front-end for desktop apps  
- [ ] Add emotion detection + sentiment-based replies

## 🙌 Credits & Shoutouts

- Inspired by the dream of building a real anime-style assistant ✨  
- Voice system powered by open-source tech — big thanks to Rasa, gTTS, and SpeechRecognition.

## 📫 Wanna Connect?

I’m **Shubham Rana (Rana)** — a full-stack dev with an AI addiction.  
You can reach out on GitHub or drop me a DM if you’re building something cool.
