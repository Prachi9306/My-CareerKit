import streamlit as st
from gtts import gTTS
import io
import requests
import threading
from fpdf import FPDF
import speech_recognition as sr
import time  # For simulating delays if needed

# Note: speech_recognition requires microphone access, which may not work in all Streamlit deployments.
# For TTS, gTTS is used to generate audio on the fly.

# Initialization
st.set_page_config(page_title="My CareerKit AI Chatbot", layout="wide")

# Custom CSS for a clean, modern UI (light theme, no avatars, better spacing)
st.markdown("""
    <style>
    .stApp {
        background-color: #ffffff;  /* Light background */
        color: #000000;  /* Dark text */
    }
    .stChatFloatingInputContainer {
        padding-bottom: 6rem;
    }
    /* Hide avatars */
    [data-testid="avatar"] {
        display: none;
    }
    .chat-message {
        padding: 1.2rem;
        border-radius: 8px;
        margin-bottom: 1rem;
        max-width: 80%;
        font-size: 16px;
        line-height: 1.5;
    }
    .chat-message.user {
        background-color: #dcedff;  /* Soft blue for user */
        align-self: flex-end;
    }
    .chat-message.bot {
        background-color: #e6f7e6;  /* Soft green for bot */
        align-self: flex-start;
    }
    .stTextInput > div > div > input {
        border-radius: 8px;
        border: 1px solid #ced4da;
        padding: 0.75rem;
    }
    .stButton > button {
        border-radius: 8px;
    }
    </style>
""", unsafe_allow_html=True)

# Global context and emotion
if "context_history" not in st.session_state:
    st.session_state.context_history = []
if "emotion_state" not in st.session_state:
    st.session_state.emotion_state = "neutral"
if "messages" not in st.session_state:  # Use messages as per Streamlit best practice
    st.session_state.messages = []
if "processing" not in st.session_state:
    st.session_state.processing = False
if "stop_event" not in st.session_state:
    st.session_state.stop_event = threading.Event()

# Emotion detection
def detect_emotion(text):
    emotions = {
        "happy": ["happy", "great", "excited", "joy", "love"],
        "sad": ["sad", "upset", "unhappy", "depressed"],
        "angry": ["angry", "mad", "furious"],
        "confused": ["confused", "lost", "uncertain"]
    }
    for emotion, keywords in emotions.items():
        if any(word in text.lower() for word in keywords):
            return emotion
    return "neutral"

# Streamed response generator for Ollama
def ollama_response_generator(prompt, stop_event):
    url = "http://localhost:11434/api/generate"
    response = requests.post(url, json={
        "model": "llama3",
        "prompt": prompt,
        "stream": True
    }, stream=True)

    for line in response.iter_lines():
        if stop_event.is_set():
            break
        if line:
            data = line.decode('utf-8')
            if 'response' in data:
                chunk = data.split('"response":"')[-1].split('"')[0]
                yield chunk.replace("\\n", "\n").replace("**", "")
                time.sleep(0.05)  # Optional delay for typewriter effect

# PDF Export
class PDF(FPDF):
    def header(self):
        self.set_font("Arial", 'B', 14)
        self.cell(0, 10, 'My CareerKit AI Chatbot Conversation', ln=True, align='C')
        self.ln(10)

    def add_chat(self, chat):
        self.set_font("Arial", '', 12)
        for role, content in chat:
            if role == "user":
                self.set_text_color(0, 0, 255)
            else:
                self.set_text_color(0, 128, 0)
            self.multi_cell(0, 10, f"{role.capitalize()}: {content}\n")

# Sidebar options
with st.sidebar:
    st.header("🤖 My CareerKit")
    if st.button("🌐 Language"):
        st.info("Language switching coming soon!")
    # if st.button("🎯 Career Quiz"):
    #     st.info("Starting quiz...")
    #if st.button("📤 Export PDF"):
        if st.session_state.messages:
            pdf = PDF()
            pdf.add_page()
            pdf.add_chat([(m["role"], m["content"]) for m in st.session_state.messages])
            pdf_bytes = io.BytesIO()
            pdf.output(pdf_bytes)
            pdf_bytes.seek(0)
            st.download_button("Download PDF", pdf_bytes, file_name="chat_conversation.pdf", mime="application/pdf")
        else:
            st.warning("No conversation to export.")
    if st.button("📄 New Page"):
        st.session_state.context_history = []
        st.session_state.messages = []
        st.rerun()

# Chat display
st.title("My CareerKit AI Chatbot")
chat_container = st.container()
for message in st.session_state.messages:
    with chat_container:
        with st.chat_message(message["role"]):
            st.markdown(message["content"])
            col1, col2 = st.columns(2)
            with col1:
                if st.button("🔊 Speak", key=f"speak_{hash(message['content'])}"):
                    tts = gTTS(message["content"])
                    fp = io.BytesIO()
                    tts.write_to_fp(fp)
                    fp.seek(0)
                    st.audio(fp, format="audio/mp3")
            with col2:
                if st.button("📋 Copy", key=f"copy_{hash(message['content'])}"):
                    st.code(message["content"], language="text")
                    st.info("Copied to clipboard (simulate in browser).")

# Input form
with st.form(key="chat_form", clear_on_submit=True):
    cols = st.columns([6, 1, 1, 1])
    with cols[0]:
        user_msg = st.text_input("Type your message...", key="user_input")
    with cols[1]:
        submit_button = st.form_submit_button("📨 Send")
    with cols[2]:
        if st.form_submit_button("⛔ Stop"):
            st.session_state.stop_event.set()
            st.session_state.processing = False
    with cols[3]:
        #if st.form_submit_button("🎤 Mic"):
            try:
                r = sr.Recognizer()
                with sr.Microphone() as source:
                    audio = r.listen(source, timeout=5)
                    recognized_text = r.recognize_google(audio, language='en-IN')
                    # In Streamlit, we can't directly set input, but simulate
                    st.info(f"Recognized: {recognized_text}")
                    # To process, set session state and rerun
                    st.session_state.user_input = recognized_text
                    st.rerun()
            except Exception as e:
                st.warning(f"Microphone input failed: {str(e)}. Limited support in web.")

    if submit_button and user_msg and not st.session_state.processing:
        st.session_state.messages.append({"role": "user", "content": user_msg})
        st.session_state.context_history.append(user_msg)
        if len(st.session_state.context_history) > 10:
            st.session_state.context_history.pop(0)
        st.session_state.processing = True
        st.session_state.stop_event.clear()
        emotion = detect_emotion(user_msg)
        prompt = f"You are MyCareerKit, an empathetic career advisor chatbot. Respond with helpful, clear advice. Keep your response concise and straightforward, with a brief explanation relevant to the question.\nMood: {emotion}.\n\nUser: {user_msg}"
        
        with st.chat_message("assistant"):
            response = st.write_stream(ollama_response_generator(prompt, st.session_state.stop_event))
        if response:
            st.session_state.messages.append({"role": "assistant", "content": response})
        st.session_state.processing = False