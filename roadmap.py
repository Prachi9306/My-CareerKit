import streamlit as st
import subprocess
import pyttsx3
import speech_recognition as sr
from fpdf import FPDF
import base64
import io
import threading

# ---------------------- PAGE CONFIG ----------------------
st.set_page_config(page_title="Career Roadmap Generator", layout="wide")

# ---------------------- BACKGROUND ----------------------
def set_bg_from_local(image_file):
    with open(image_file, "rb") as file:
        encoded = base64.b64encode(file.read()).decode()
    bg_css = f"""
    <style>
    [data-testid="stAppViewContainer"] {{
        background-image: url("data:image/jpg;base64,{encoded}");
        background-size: cover;
        background-position: center;
        background-attachment: fixed;
    }}
    [data-testid="stHeader"], [data-testid="stToolbar"] {{
        background: rgba(0,0,0,0);
    }}
    div.stButton > button {{
        border-radius: 10px;
        padding: 0.6em 1.4em;
        font-weight: 600;
        border: 2px solid #00E5FF;
        color: white !important;
        background: rgba(0,0,0,0.6);
        transition: all 0.3s ease;
    }}
    div.stButton > button:hover {{
        background-color: #00E5FF;
        color: black !important;
        transform: scale(1.05);
    }}
    .main-content {{
        background: rgba(0,0,0,0.55);
        border-radius: 15px;
        padding: 25px 40px;
        box-shadow: 0 4px 20px rgba(0,0,0,0.5);
    }}
    h1, h2, p, label, div {{
        color: white !important;
    }}
    ::placeholder {{
        color: #B0BEC5 !important;
        opacity: 1;
    }}
    </style>
    """
    st.markdown(bg_css, unsafe_allow_html=True)

set_bg_from_local("bg.jpg")

# ---------------------- FUNCTIONS ----------------------
def query_ollama(career):
    prompt = f"""
Generate a detailed, visually appealing career roadmap for becoming a {career}. 
Include:
1. Educational pathway (Bachelor’s, Master’s, Ph.D. with durations)
2. Key skills (technical + soft)
3. Career progression steps with timelines
4. Alternate career options
5. Industry trends and future scope
6. Salary expectations and job market outlook
7. Tips to stay ahead (certifications, tools, networking)
Use *bold* section titles and bullet points.
"""
    try:
        result = subprocess.run(
            ["ollama", "run", "llama3", prompt],
            capture_output=True, text=True, check=True, encoding="utf-8"
        )
        return result.stdout.strip()
    except subprocess.CalledProcessError as e:
        return f"❌ Error generating roadmap: {e}"
    except FileNotFoundError:
        return "⚠️ Ollama not found. Please install Ollama and ensure `llama3` model is available."

def get_voice_input():
    recognizer = sr.Recognizer()
    with sr.Microphone() as source:
        with st.spinner("🎤 Listening... Please speak clearly"):
            recognizer.adjust_for_ambient_noise(source)
            try:
                audio = recognizer.listen(source, timeout=5)
                text = recognizer.recognize_google(audio)
                st.success(f"✅ Recognized: {text}")
                return text
            except sr.UnknownValueError:
                st.error("❌ Could not understand audio.")
            except sr.RequestError as e:
                st.error(f"⚠️ Error with speech recognition service: {e}")
            except sr.WaitTimeoutError:
                st.warning("⏰ No voice detected. Try again.")
    return ""

def read_aloud(text):
    engine = pyttsx3.init()
    engine.say(text)
    engine.runAndWait()

def save_as_pdf(content):
    pdf = FPDF()
    pdf.add_page()
    pdf.set_font("Arial", size=12)
    pdf.set_text_color(0, 0, 0)
    for line in content.split("\n"):
        pdf.multi_cell(0, 10, line)
    pdf_bytes = io.BytesIO()
    pdf.output(pdf_bytes)
    pdf_bytes.seek(0)
    return pdf_bytes

# ---------------------- MAIN UI ----------------------
st.markdown("<h1 style='text-align:center; color:#00E5FF;'>💼 Career Roadmap Generator</h1>", unsafe_allow_html=True)
st.markdown("<p style='text-align:center; font-size:18px; color:#E0F7FA;'>Your AI-powered career guide to education, skills, and success!</p>", unsafe_allow_html=True)
st.markdown("<br>", unsafe_allow_html=True)

# Main content box
with st.container():
    #st.markdown("<div class='main-content'>", unsafe_allow_html=True)

    # Input Section
    career_input = st.text_input("🎯 Enter your desired career", placeholder="e.g., Data Scientist", key="career_input", )

    # Button symmetry row
    col1, col2, col3 = st.columns([1, 1, 1])
    with col1:
        voice_btn = st.button("🎤 Voice Input")
    with col2:
        generate_btn = st.button("🚀 Generate Roadmap")
    with col3:
        clear_btn = st.button("🧹 Clear")

    # Voice Input
    if voice_btn:
        voice_text = get_voice_input()
        if voice_text:
            st.session_state.career_input = voice_text

    # State Init
    if "roadmap_text" not in st.session_state:
        st.session_state.roadmap_text = ""

    # Generate Roadmap
    if generate_btn:
        if not st.session_state.career_input:
            st.warning("⚠️ Please enter or say a career first.")
        else:
            with st.spinner("✨ Generating your personalized roadmap..."):
                roadmap_text = query_ollama(st.session_state.career_input)
                st.session_state.roadmap_text = roadmap_text

    # Clear Output
    if clear_btn:
        st.session_state.roadmap_text = ""
        st.session_state.career_input = ""

    # Output Section
    if st.session_state.roadmap_text:
        st.markdown(f"<h2 style='text-align:center; color:#80DEEA;'>📘 Career Roadmap for {st.session_state.career_input.title()}</h2>", unsafe_allow_html=True)
        st.markdown("---")

        st.markdown(
            f"<div style='background-color:rgba(0,0,0,0.7); padding:25px; border-radius:10px; color:white; font-size:16px; line-height:1.6;'>"
            f"{st.session_state.roadmap_text.replace('*', '**').replace('\n', '<br>')}"
            f"</div>", unsafe_allow_html=True
        )

        st.markdown("<br>", unsafe_allow_html=True)

        # Action buttons (aligned evenly)
        c1, c2, c3 = st.columns([1, 1, 1])
        with c1:
            if st.button("🔊 Read Aloud"):
                threading.Thread(target=read_aloud, args=(st.session_state.roadmap_text,)).start()
        with c2:
            pdf_bytes = save_as_pdf(st.session_state.roadmap_text)
            st.download_button("📄 Download PDF", pdf_bytes, file_name=f"{st.session_state.career_input}_roadmap.pdf")
        with c3:
            st.empty()

    st.markdown("</div>", unsafe_allow_html=True)

# Footer
st.markdown("<br><hr><p style='text-align:center; color:#B2EBF2;'>Made with ❤️ | AI Career Roadmap Generator</p>", unsafe_allow_html=True)
