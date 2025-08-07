// --- Global Variables ---
const chatLog = document.getElementById('chat-log');
const chatInput = document.getElementById('chat-input');
const muteButton = document.getElementById('mute-button');
const speakerOnIcon = document.getElementById('speaker-on-icon');
const speakerOffIcon = document.getElementById('speaker-off-icon');
const RASA_SERVER_URL = 'http://localhost:5005/webhooks/rest/webhook';
const SENDER_ID = 'user';

let isTyping = false;
let japaneseVoice = null;
let isMuted = true;

// --- Master Audio Visualizer ---
let audioContext, analyser, visualizerCanvas, vizCtx;
let visualizerInitialized = false;

function initMasterVisualizer() {
    if (visualizerInitialized) return;
    
    const container = document.createElement('div');
    container.id = 'visualizer-container';
    visualizerCanvas = document.createElement('canvas');
    visualizerCanvas.id = 'chat-visualizer-canvas';
    container.appendChild(visualizerCanvas);
    chatLog.appendChild(container);
    vizCtx = visualizerCanvas.getContext('2d');

    const audioEl = document.getElementById('tts-audio');
    // AudioContext is created on first unmute click
    analyser = audioContext.createAnalyser();
    analyser.fftSize = 256;
    
    const ttsSource = audioContext.createMediaElementSource(audioEl);
    ttsSource.connect(analyser);
    analyser.connect(audioContext.destination);
    
    visualizerInitialized = true;
    animateVisualizer();
}

function animateVisualizer() {
    requestAnimationFrame(animateVisualizer);
    
    const bufferLength = analyser.frequencyBinCount;
    const dataArray = new Uint8Array(bufferLength);
    analyser.getByteFrequencyData(dataArray);

    vizCtx.fillStyle = 'rgba(13, 2, 8, 1)';
    vizCtx.fillRect(0, 0, visualizerCanvas.width, visualizerCanvas.height);
    
    const centerX = visualizerCanvas.width / 2;
    const centerY = visualizerCanvas.height / 2;
    const radius = 100;
    const barWidth = 3;
    
    for (let i = 0; i < bufferLength; i++) {
        const barHeight = dataArray[i] / 2;
        const angle = (i / bufferLength) * 2 * Math.PI;

        const x = centerX + Math.cos(angle) * radius;
        const y = centerY + Math.sin(angle) * radius;
        const x2 = centerX + Math.cos(angle) * (radius + barHeight);
        const y2 = centerY + Math.sin(angle) * (radius + barHeight);

        const gradient = vizCtx.createLinearGradient(x, y, x2, y2);
        gradient.addColorStop(0, '#a855f7');
        gradient.addColorStop(1, '#f472b6');

        vizCtx.strokeStyle = gradient;
        vizCtx.lineWidth = barWidth;
        vizCtx.beginPath();
        vizCtx.moveTo(x, y);
        vizCtx.lineTo(x2, y2);
        vizCtx.stroke();
    }
}

// --- Mute Button & Mode Switching Logic ---
function enterTextMode() {
    if (isMuted) return;
    isMuted = true;
    window.speechSynthesis.cancel();
    speakerOnIcon.style.display = 'none';
    speakerOffIcon.style.display = 'block';
    muteButton.title = "Unmute Mai";
    chatLog.classList.remove('voice-mode');
    const visualizerContainer = document.getElementById('visualizer-container');
    if (visualizerContainer) {
        visualizerContainer.style.opacity = '0';
        setTimeout(() => visualizerContainer.style.display = 'none', 300);
    }
}

function enterVoiceMode() {
    if (!isMuted) return;
    isMuted = false;
    // Create AudioContext on the first user click to unmute
    if (!audioContext) {
        audioContext = new (window.AudioContext || window.webkitAudioContext)();
    }
    if (!visualizerInitialized) initMasterVisualizer();
    
    speakerOnIcon.style.display = 'block';
    speakerOffIcon.style.display = 'none';
    muteButton.title = "Mute Mai";
    chatLog.classList.add('voice-mode');
    const visualizerContainer = document.getElementById('visualizer-container');
    if (visualizerContainer) {
        visualizerContainer.style.display = 'flex';
        setTimeout(() => visualizerContainer.style.opacity = '1', 10);
    }
}

muteButton.addEventListener('click', () => {
    if (isMuted) {
        enterVoiceMode();
    } else {
        enterTextMode();
    }
});

chatInput.addEventListener('click', enterTextMode);

// --- Text-to-Speech Functionality ---
function loadVoices() { const voices = window.speechSynthesis.getVoices(); japaneseVoice = voices.find(voice => voice.lang.startsWith('ja')); }

function speak(text) {
    if (isMuted) return;
    const audioEl = document.getElementById('tts-audio');
    const gttsUrl = `https://translate.google.com/translate_tts?ie=UTF-8&q=${encodeURIComponent(text)}&tl=ja&client=tw-ob`;
    audioEl.src = gttsUrl;
    audioEl.crossOrigin = "anonymous";
    audioEl.play().catch(e => console.error("Audio play failed:", e));
}

window.speechSynthesis.onvoiceschanged = loadVoices;
loadVoices();

// --- Chat Logic ---
function typeText(element, text, callback) { isTyping = true; let i = 0; element.innerHTML = ""; const interval = setInterval(() => { if (i < text.length) { element.innerHTML += text.charAt(i); i++; chatLog.scrollTop = chatLog.scrollHeight; } else { clearInterval(interval); isTyping = false; if (callback) callback(); } }, 30); }
function addLine(text, isUser = false) { const newLine = document.createElement('div'); newLine.classList.add('line'); if (isUser) { newLine.classList.add('user-line'); newLine.style.color = "#e0e0e0"; } else { speak(text); } chatLog.appendChild(newLine); typeText(newLine, text); }
async function sendMessageToRasa(message) { try { const response = await fetch(RASA_SERVER_URL, { method: 'POST', headers: { 'Content-Type': 'application/json' }, body: JSON.stringify({ sender: SENDER_ID, message: message }) }); if (!response.ok) throw new Error(`HTTP error! status: ${response.status}`); const botResponses = await response.json(); if (botResponses && botResponses.length > 0) { botResponses.forEach(res => addLine(res.text)); } else { addLine("Sumimasen, I don't have a response for that yet."); } } catch (error) { console.error("Error connecting to Rasa:", error); addLine("Error: Could not connect to Mai's brain. Is the Rasa server running?"); } }

chatInput.addEventListener('keypress', (e) => {
    if (e.key === 'Enter' && !isTyping) {
        const message = chatInput.value.trim();
        if (message) {
            addLine(message, true);
            chatInput.value = '';
            sendMessageToRasa(message);
        }
    }
});

function startUp() {
    const initialText = "Konnichiwa, boss-sama! I am Mai. System online.";
    addLine(initialText, false);
    // Start background animation
    const bgCanvas = document.getElementById('background-canvas');
    const bgCtx = bgCanvas.getContext('2d');
    let petals = [];
    const PETAL_COUNT = 50;
    function resizeBgCanvas() { bgCanvas.width = window.innerWidth; bgCanvas.height = window.innerHeight; }
    class Petal { constructor() { this.x = Math.random() * bgCanvas.width; this.y = Math.random() * bgCanvas.height * 2 - bgCanvas.height; this.size = Math.random() * 2 + 1; this.speed = Math.random() * 1 + 0.5; this.spin = Math.random() * 0.2 - 0.1; this.angle = Math.random() * Math.PI * 2; } update() { this.y += this.speed; this.x += Math.sin(this.angle) * 0.5; this.angle += this.spin; if (this.y > bgCanvas.height) { this.y = -this.size; this.x = Math.random() * bgCanvas.width; } } draw() { bgCtx.save(); bgCtx.translate(this.x, this.y); bgCtx.rotate(this.angle); bgCtx.fillStyle = `rgba(0, 255, 255, ${Math.random() * 0.5 + 0.3})`; bgCtx.shadowColor = '#00ffff'; bgCtx.shadowBlur = 10; bgCtx.fillRect(-this.size / 2, -this.size / 2, this.size, this.size); bgCtx.restore(); } }
    function initPetals() { petals = []; for (let i = 0; i < PETAL_COUNT; i++) { petals.push(new Petal()); } }
    function drawKanji() { const centerX = bgCanvas.width / 2; const centerY = bgCanvas.height / 2; const kanji = '侍'; bgCtx.font = '200px "Courier Prime"'; bgCtx.fillStyle = 'rgba(244, 114, 182, 0.1)'; bgCtx.textAlign = 'center'; bgCtx.textBaseline = 'middle'; bgCtx.shadowColor = '#f472b6'; bgCtx.shadowBlur = 20; bgCtx.fillText(kanji, centerX, centerY); bgCtx.shadowBlur = 0; }
    function animateBg() { bgCtx.fillStyle = 'rgba(10, 5, 16, 0.1)'; bgCtx.fillRect(0, 0, bgCanvas.width, bgCanvas.height); drawKanji(); petals.forEach(p => { p.update(); p.draw(); }); requestAnimationFrame(animateBg); }
    function startSamuraiAnimation() { resizeBgCanvas(); initPetals(); animateBg(); window.addEventListener('resize', () => { resizeBgCanvas(); initPetals(); }); }
    startSamuraiAnimation();
}

startUp();
