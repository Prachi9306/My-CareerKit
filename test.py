import streamlit as st
import base64
import pathlib
import subprocess

# ---------------------- PAGE CONFIG ----------------------
st.set_page_config(
    page_title="My Career Kit",
    layout="wide"
)

# ---------------------- BACKGROUND HELPER ----------------------
def _get_image_data_uri(path: str) -> str:
    p = pathlib.Path(path)
    if not p.exists():
        return "https://i.ibb.co/6vmrZ7y/career-bg.jpg"  # fallback URL

    suffix = p.suffix.lower()
    if suffix == ".png":
        mime = "png"
    elif suffix == ".webp":
        mime = "webp"
    elif suffix == ".gif":
        mime = "gif"
    else:
        mime = "jpeg"  # default for jpg/jpeg

    data = p.read_bytes()
    b64 = base64.b64encode(data).decode()
    return f"data:image/{mime};base64,{b64}"

bg_uri = _get_image_data_uri("assets/bg.jpg")

# ---------------------- GLOBAL CSS ----------------------
st.markdown(f"""
<style>
/* Background: fill full screen */
.stApp {{
    background-image: url("{bg_uri}");
    background-size: cover;   /* fills full screen */
    background-repeat: no-repeat;
    background-position: center center;
    background-attachment: fixed;
    color: white;
}}

/* Make Streamlit's block container a column flex so we can push the START button to the bottom */
.stApp .block-container {{
    display: flex;
    flex-direction: column;
    min-height: 100vh;
    padding-bottom: 24px; /* avoid overlap */
}}

/* Title + subtitle */
.title {{
    font-size: 120px;
    font-weight: 900;
    text-align: center;
    text-shadow: 3px 3px 10px black;
    margin-top: 6vh;
}}
.subtitle {{
    font-size: 36px;
    text-align: center;
    margin-bottom: 30px;
    font-weight: 600; /* Slightly bold to match title's prominence */
}}

/* General button styling */
div.stButton > button {{
    background-color: #2a9df4 !important;
    color: #ffffff !important;
    border: none !important;
    padding: 18px 24px !important;
    font-size: 18px !important;
    border-radius: 12px !important;
    width: 100% !important;
    height: 64px !important;
    box-shadow: 0 10px 0 rgba(11, 74, 122, 0.6) !important;
    transition: transform 0.15s ease, box-shadow 0.15s ease !important;
    text-align: center !important;
}}
div.stButton > button:hover {{
    transform: translateY(-6px) !important;
    box-shadow: 0 14px 12px rgba(11, 74, 122, 0.35) !important;
}}
div.stButton > button:active {{
    transform: translateY(6px) !important;
    box-shadow: 0 4px 0 rgba(11, 74, 122, 0.6) !important;
}}

/* Column gap */
[data-testid="column"] {{
    gap: 24px;
}}
</style>
""", unsafe_allow_html=True)

# ---------------------- SESSION NAV ----------------------
if "page" not in st.session_state:
    st.session_state.page = "home"

# ---------------------- HOME PAGE ----------------------
if st.session_state.page == "home":
    st.markdown('<p class="title">MY CAREER KIT</p>', unsafe_allow_html=True)
    st.markdown('<p class="subtitle">Discover your ideal career path through guided exploration.</p>', unsafe_allow_html=True)

    # START button at the bottom of the screen
    st.markdown("""
    <style>
    .start-btn-container {
        position: fixed;
        bottom: 20px;       /* closer to the bottom */
        left: 50%;          /* center horizontally */
        transform: translateX(-50%);
        width: 300px;       /* width of the button container */
        text-align: center;
        z-index: 999;       /* make sure it's on top */
    }
    </style>
""", unsafe_allow_html=True)
    st.markdown('<div class="start-btn-container">', unsafe_allow_html=True)
    if st.button("🚀 START", key="start_btn", use_container_width=True):
        st.session_state.page = "main"
        st.rerun()  # Force immediate rerun to switch pages on single click
    st.markdown('</div>', unsafe_allow_html=True)

# ---------------------- MAIN PAGE ----------------------
elif st.session_state.page == "main":
    st.title("🎓 Career Options")
    st.markdown("### Select an option below:")

    col1, col2 = st.columns(2)

    with col1:
        if st.button("🔍 Know your interested career", use_container_width=True):
            st.session_state.page = "career_quiz"
            st.rerun()  # Force immediate rerun
        if st.button("📊 Career Flowchart", use_container_width=True):
            st.session_state.page = "flowchart"
            st.rerun()  # Force immediate rerun

    with col2:
        if st.button("🛤 Roadmap for your desired career", use_container_width=True):
            st.session_state.page = "roadmap"
            st.rerun()  # Force immediate rerun
        if st.button("🏛 Govt Exams", use_container_width=True):
            st.session_state.page = "govt_exams"
            st.rerun()  # Force immediate rerun

    st.markdown("### 💬 Ask Your Doubt")
    if st.button("🤖 Open AI Chatbot", use_container_width=True):
        st.session_state.page = "chatbot"
        st.rerun()  # Force immediate rerun

    st.markdown("---")
    if st.button("⬅ Back to Home", use_container_width=True):
        st.session_state.page = "home"
        st.rerun()  # Force immediate rerun

# ---------------------- CONNECTED PAGES ----------------------
elif st.session_state.page == "career_quiz":
    try:
        subprocess.Popen(["streamlit", "run", "attempt_quiz.py"])
        st.write("Opened career quiz in a new tab.")
    except Exception as e:
        st.error(f"Could not load career quiz: {e}")

    if st.button("⬅ Back to Main Menu", use_container_width=True):
        st.session_state.page = "main"
        st.rerun()

elif st.session_state.page == "flowchart":
    try:
        subprocess.Popen(["streamlit", "run", "flowchart.py"])
        st.write("Opened flowchart in a new tab.")
    except Exception as e:
        st.error(f"Could not load flowchart: {e}")

    if st.button("⬅ Back to Main Menu", use_container_width=True):
        st.session_state.page = "main"
        st.rerun()

elif st.session_state.page == "roadmap":
    try:
        subprocess.Popen(["streamlit", "run", "roadmap.py"])
        st.write("Opened roadmap in a new tab.")
    except Exception as e:
        st.error(f"Could not load roadmap: {e}")

    if st.button("⬅ Back to Main Menu", use_container_width=True):
        st.session_state.page = "main"
        st.rerun()

elif st.session_state.page == "govt_exams":
    try:
        subprocess.Popen(["streamlit", "run", "govt_exam.py"])
        st.write("Opened govt exams in a new tab.")
    except Exception as e:
        st.error(f"Could not load govt exams: {e}")

    if st.button("⬅ Back to Main Menu", use_container_width=True):
        st.session_state.page = "main"
        st.rerun()

elif st.session_state.page == "chatbot":
    try:
        subprocess.Popen(["streamlit", "run", "chatbot.py"])
        st.write("Opened chatbot in a new tab.")
    except Exception as e:
        st.error(f"Could not load chatbot: {e}")

    if st.button("⬅ Back to Main Menu", use_container_width=True):
        st.session_state.page = "main"
        st.rerun()