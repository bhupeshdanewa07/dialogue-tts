<div align="center">
  <h1>🎙️ Studio Voice Synthesizer</h1>
  <p><strong>Bring your scripts to life with AI-powered multi-voice synthesis using Sarvam AI.</strong></p>
</div>

<br />

## 🌟 Overview

The **Studio Voice Synthesizer** is a cinematic, dynamic Text-to-Speech (TTS) web application built with [Streamlit](https://streamlit.io/). Powered by the cutting-edge [Sarvam AI API](https://www.sarvam.ai/) (`bulbul:v3` model), it allows you to input multi-character dialogue and effortlessly generate a fully voiced, contiguous audio file.

Say goodbye to monotonous, single-voice robotic text-to-speech. Instantly cast distinct Indian voices for each character in your script and let the AI perform it for you!

---

## ✨ Features

- **🎭 Automatic Character Detection**: Just type your script in `Name: Dialogue` format, and the app will instantly detect all the characters.
- **🗣️ Rich Voice Library**: Cast your characters using **20 premium studio voices** (10 Male, 10 Female).
- **🎨 Interactive Aesthetic UI**: A beautifully designed, cinematic user interface that automatically filters voices based on gender selection.
- **✂️ Seamless Audio Stitching**: The app dynamically generates audio segments and seamlessly stitches them together into one high-quality `.wav` file.
- **💾 One-Click Download**: Instantly preview your generated dialogue and download it locally for your video, podcast, or presentation.

---

## 🛠️ Installation

### 1. Clone the repository
```bash
git clone https://github.com/bhupeshdanewa07/dialogue-tts.git
cd dialogue-tts
```

### 2. Install dependencies
Ensure you have Python installed, then run:
```bash
pip install -r requirements.txt
```

### 3. Set up your API Key
You will need a Sarvam AI API key.
1. Create a `.env` file in the root directory.
2. Add your API key like so:
```env
SARVAM_API_KEY=your_api_key_here
```

---

## 🚀 Usage

Run the application locally using Streamlit:
```bash
streamlit run main.py
```

### 📝 How to Write a Script
Format your text by placing the character's name followed by a colon `:` and their dialogue.

**Example:**
> **John:** Have you finished the API integration yet?
> **Sarah:** Almost done. I just need to fix a small routing bug in FastAPI.
> **John:** Awesome. Let me know when it's pushed to GitHub.

---

## 💻 Tech Stack
- **Frontend**: [Streamlit](https://streamlit.io/)
- **AI Model**: [Sarvam AI](https://www.sarvam.ai/) (`bulbul:v3` TTS API)
- **Audio Processing**: Native Python `wave` and `io` modules
- **Environment**: `python-dotenv`

---

<div align="center">
  <i>Built with ❤️ for dynamic audio generation.</i>
</div>
