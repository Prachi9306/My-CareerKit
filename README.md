# My Career Kit

**My CareerKit** is an intelligent career counselling web application built using **Python** and **Streamlit**.  
It leverages **AI technology** to guide students in exploring, planning, and visualizing their career paths in an interactive and engaging way.

---

## Features
- Full-screen background (assets/bg.jpg) with layered styling
- Large, responsive title and subtitle
- Interactive career quiz (10 questions × 10 options)
- Category scoring and career recommendations
- Optional text-to-speech (gTTS) for questions/results
- Sidebar controls (upload background, navigation)
- Quiz implemented as a separate module (`attempt_quiz.py`) and integrated into the main app (`test.py`)

---

## Requirements
- Python 3.8+
- Streamlit
- Pillow (image handling)
- gTTS (optional — online TTS)
- (Optional) Speech recognition / microphone libs if you enable voice input

---

## Setup (PowerShell)
1. Open PowerShell and change to the project folder:
```powershell
Set-Location G:\MCK
```

2. (Recommended) Create a virtual environment:
```powershell
python -m venv .venv
.\.venv\Scripts\Activate.ps1
```

3. Install dependencies:
```powershell
.\.venv\Scripts\python -m pip install --upgrade pip
.\.venv\Scripts\python -m pip install streamlit pillow gTTS
# Optional for microphone support:
# pip install SpeechRecognition
# Use pipwin or wheels to install PyAudio on Windows
```

4. Add your background image:
- Place a file named `bg.jpg` or `bg_image.jpg` under `G:\MCK\assets\bg.jpg` (or update the script to point to your filename).

---

## Run the app
From the project folder (ensure venv active):
```powershell
.\.venv\Scripts\python -m streamlit run test.py --server.port 8501
```
Open the printed Local URL (usually `http://localhost:8501`) in your browser.

---

## How it works / Usage
- Home → Click `START` → `Main` page
- Click `🔍 Know your interested career` to open the quiz (this calls `attempt_quiz.run_quiz()` and renders the quiz inside the Streamlit app)
- Answer questions; at the end you get a recommended category and career list
- Use "Read Aloud" buttons to play TTS audio (requires internet for gTTS)
- Use the sidebar to upload/replace `assets/bg.jpg` if needed

---

## File structure (key files)
- test.py — Main Streamlit app, navigation, styling
- attempt_quiz.py — Quiz implementation (exposes `run_quiz()` for import)
- chatbot.py — AI chatbot (TTS/voice features optional)
- assets/ — place `bg.jpg` here
- README.md — this file

---

## Troubleshooting
- Syntax errors: run `python -m py_compile test.py` to see parse errors.
- Streamlit not found: ensure you installed packages into the active venv.
- PyAudio issues on Windows: use `pipwin install pyaudio` or download prebuilt wheel.
- TTS not working: gTTS requires network access; consider `pyttsx3` for offline TTS.
- UI styling conflicts: remove duplicate `.stApp` CSS blocks; only one global background rule should remain.

---

## Customization tips
- Change quiz questions / mappings in `attempt_quiz.py`.
- To keep the background image unzoomed while visually covering the screen, the app uses a layered CSS approach — change `background-size` between `contain` and `cover` as needed.
- Replace Streamlit radio options with custom button tiles for guaranteed styling across browsers.

---

## License
MIT

---
