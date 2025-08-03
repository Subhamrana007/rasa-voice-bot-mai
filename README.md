Mai (舞) - A Rasa Powered Voice Assistant
Mai is a conversational AI assistant with a unique personality, built from the ground up using Python and the Rasa open-source framework. She is designed to be a helpful and engaging companion, capable of understanding spoken English and responding with a Japanese-accented voice.

This project was developed by Rana as a demonstration of skills in conversational AI, natural language understanding, and cross-platform Python application development.

✨ Features
Voice-Activated: Fully hands-free interaction. Mai listens for your commands and responds audibly.

Unique Personality: Mai is from Japan and her responses are tailored to reflect her origin, using Japanese honorifics and phrases.

Cross-Platform: Works on Linux, macOS, and Windows.

Fast & Responsive: Utilizes in-memory audio processing for quick response times.

🛠️ Technologies Used
Core Framework: Rasa Open Source

Speech-to-Text: SpeechRecognition

Text-to-Speech: gTTS

Audio Playback: pydub

Core Language: Python 3.10

🚀 Setup and Installation
To run Mai on your own machine, please follow the steps for your specific operating system.

1. Clone the Repository
First, clone the repository and navigate into the project folder. This is the same for all systems.

git clone https://github.com/your-username/rasa-voice-bot-mai.git
cd rasa-voice-bot-mai

2. System Prerequisites
Next, install the necessary system dependencies.

On Linux (Fedora)
sudo dnf install portaudio-devel python3.10-devel gcc ffmpeg

On macOS
You will need Homebrew.

brew install portaudio ffmpeg

On Windows
You will need Chocolatey to easily install the tools.

choco install ffmpeg

Note for Windows: PyAudio can be difficult to install. If the pip install command fails later, you may need to install it from a pre-compiled wheel file from a trusted source like Christoph Gohlke's page.

3. Set Up the Python Environment
Create a virtual environment:

python3.10 -m venv venv

Activate the virtual environment:

On Linux/macOS:

source venv/bin/activate

On Windows:

.\venv\Scripts\activate

Install the required Python packages:

pip install -r requirements.txt

4. Train the Rasa Model
This step is the same for all systems.

rasa train

▶️ How to Run Mai
You will need two terminals (or Command Prompts on Windows).

In your first terminal, start the Rasa server:

rasa run --enable-api --cors "*"

In your second terminal, start the voice interface:

python voice_interface.py

Mai will greet you, and you can start talking!

💬 How to Interact
Simply speak clearly after you see the "Listening..." message in the terminal.

You can try saying things like:

"Hello"

"How are you?"

"Who made you?"

"Teach me a Japanese word"

"Exit" (to shut her down)