import streamlit as st
from PIL import Image
import base64

# ---------------- Helper Functions ----------------
def get_base64_image(image_path):
    with open(image_path, "rb") as img_file:
        return base64.b64encode(img_file.read()).decode('utf-8')

def set_background(image_path):
    base64_img = get_base64_image(image_path)
    st.markdown(f"""
        <style>
        .stApp {{
            background-image: url("data:image/jpg;base64,{base64_img}");
            background-size: cover;
            background-position: center;
            background-repeat: no-repeat;
        }}
        </style>
    """, unsafe_allow_html=True)

# ---------------- Page Config ----------------
st.set_page_config(
    page_title="Interested Domain",
    layout="wide",
    initial_sidebar_state="collapsed"
)
set_background("bg.jpg")

# ---------------- Custom CSS Styling ----------------
st.markdown("""
    <style>
    /* Main Titles */
    .title {
        text-align: center;
        font-size: 50px;
        font-weight: bold;
        color: #ffffff;
        text-shadow: 2px 2px 6px #000000;
        margin-top: 20px;
        margin-bottom: 40px;
    }
    .subtitle {
        text-align: center;
        font-size: 36px;
        font-weight: bold;
        color: #ffffff;
        text-shadow: 2px 2px 4px #000000;
        margin-bottom: 30px;
    }

    /* Option Cards */
    .option-card {
        background-color: rgba(255, 255, 255, 0.9);
        border-radius: 20px;
        text-align: center;
        padding: 25px;
        box-shadow: 0px 4px 20px rgba(0,0,0,0.3);
        transition: all 0.3s ease-in-out;
        cursor: pointer;
        border: 2px solid #0a3d62;
    }
    .option-card:hover {
        transform: scale(1.05);
        box-shadow: 0px 6px 25px rgba(0,0,0,0.4);
    }

    .option-title {
        font-size: 26px;
        font-weight: bold;
        color: #0a3d62;
        margin-top: 10px;
        margin-bottom: 5px;
    }

    .back-btn button {
        background-color: #0a3d62 !important;
        color: white !important;
        border-radius: 10px !important;
        font-weight: bold !important;
    }
    .back-btn button:hover {
        background-color: #1e5799 !important;
    }
    </style>
""", unsafe_allow_html=True)

# ---------------- Session States ----------------
if "exited" not in st.session_state:
    st.session_state.exited = False
if "selected_domain" not in st.session_state:
    st.session_state.selected_domain = None
if "selected_sub_domain" not in st.session_state:
    st.session_state.selected_sub_domain = None

# ---------------- Exit Check ----------------
if st.session_state.exited:
    st.markdown('<div class="title">Thank you for exploring!</div>', unsafe_allow_html=True)
    st.stop()

# ---------------- Title ----------------
st.markdown('<div class="title">Interested Domain</div>', unsafe_allow_html=True)

# ---------------- Domain Selection ----------------
if not st.session_state.selected_domain:
    cols = st.columns(3, gap="large")

    with cols[0]:
        st.markdown('<div class="option-card">', unsafe_allow_html=True)
        sci_img = Image.open("sci_img.png")
        st.image(sci_img, use_container_width=True)
        st.markdown('<div class="option-title">Science</div>', unsafe_allow_html=True)
        if st.button("Explore Science", use_container_width=True):
            st.session_state.selected_domain = "science"
        st.markdown("</div>", unsafe_allow_html=True)

    with cols[1]:
        st.markdown('<div class="option-card">', unsafe_allow_html=True)
        com_img = Image.open("com_img.png")
        st.image(com_img, use_container_width=True)
        st.markdown('<div class="option-title">Commerce</div>', unsafe_allow_html=True)
        if st.button("Explore Commerce", use_container_width=True):
            st.session_state.selected_domain = "commerce"
        st.markdown("</div>", unsafe_allow_html=True)

    with cols[2]:
        st.markdown('<div class="option-card">', unsafe_allow_html=True)
        art_img = Image.open("art_img.png")
        st.image(art_img, use_container_width=True)
        st.markdown('<div class="option-title">Arts / Humanities</div>', unsafe_allow_html=True)
        if st.button("Explore Arts", use_container_width=True):
            st.session_state.selected_domain = "arts"
        st.markdown("</div>", unsafe_allow_html=True)

# ---------------- Domain Details ----------------
else:
    st.markdown("---")
    if st.session_state.selected_domain == "science":
        st.markdown('<div class="subtitle">Science Streams</div>', unsafe_allow_html=True)

        sub_cols = st.columns(3, gap="large")
        with sub_cols[0]:
            st.markdown('<div class="option-card">', unsafe_allow_html=True)
            pcm_img = Image.open("pcm_img.png")
            st.image(pcm_img, use_container_width=True)
            st.markdown('<div class="option-title">PCM</div>', unsafe_allow_html=True)
            if st.button("View PCM Flowchart", use_container_width=True):
                st.session_state.selected_sub_domain = "pcm"
            st.markdown("</div>", unsafe_allow_html=True)

        with sub_cols[1]:
            st.markdown('<div class="option-card">', unsafe_allow_html=True)
            pcb_img = Image.open("pcb_img.png")
            st.image(pcb_img, use_container_width=True)
            st.markdown('<div class="option-title">PCB</div>', unsafe_allow_html=True)
            if st.button("View PCB Flowchart", use_container_width=True):
                st.session_state.selected_sub_domain = "pcb"
            st.markdown("</div>", unsafe_allow_html=True)

        with sub_cols[2]:
            st.markdown('<div class="option-card">', unsafe_allow_html=True)
            pcmb_img = Image.open("pcmb_img.png")
            st.image(pcmb_img, use_container_width=True)
            st.markdown('<div class="option-title">PCMB</div>', unsafe_allow_html=True)
            if st.button("View PCMB Flowchart", use_container_width=True):
                st.session_state.selected_sub_domain = "pcmb"
            st.markdown("</div>", unsafe_allow_html=True)

        st.markdown("---")
        st.markdown('<div class="back-btn">', unsafe_allow_html=True)
        if st.button("⬅ Back to Domains", use_container_width=True):
            st.session_state.selected_domain = None
        st.markdown('</div>', unsafe_allow_html=True)

        if st.session_state.selected_sub_domain:
            st.markdown("---")
            st.markdown(f"<h2 style='color:white;text-align:center;'>Flowchart for {st.session_state.selected_sub_domain.upper()}</h2>", unsafe_allow_html=True)
            st.image(f"{st.session_state.selected_sub_domain}_flowchart.jpg", use_container_width=True)
            st.markdown('<div class="back-btn">', unsafe_allow_html=True)
            if st.button("⬅ Back to Science Streams", use_container_width=True):
                st.session_state.selected_sub_domain = None
            st.markdown('</div>', unsafe_allow_html=True)
            st.markdown('<div class="back-btn">', unsafe_allow_html=True)
            if st.button("Exit", use_container_width=True):
                st.session_state.exited = True
            st.markdown('</div>', unsafe_allow_html=True)

    elif st.session_state.selected_domain == "commerce":
        st.markdown('<div class="subtitle">Commerce Flowchart</div>', unsafe_allow_html=True)
        st.image("Commerce_flowchart_image.jpg", use_container_width=True)
        st.markdown('<div class="back-btn">', unsafe_allow_html=True)
        if st.button("⬅ Back to Domains", use_container_width=True):
            st.session_state.selected_domain = None
        st.markdown('</div>', unsafe_allow_html=True)
        st.markdown('<div class="back-btn">', unsafe_allow_html=True)
        if st.button("Exit", use_container_width=True):
            st.session_state.exited = True
        st.markdown('</div>', unsafe_allow_html=True)

    elif st.session_state.selected_domain == "arts":
        st.markdown('<div class="subtitle">Arts / Humanities Flowchart</div>', unsafe_allow_html=True)
        st.image("Arts_flowchart_image.jpg", use_container_width=True)
        st.markdown('<div class="back-btn">', unsafe_allow_html=True)
        if st.button("⬅ Back to Domains", use_container_width=True):
            st.session_state.selected_domain = None
        st.markdown('</div>', unsafe_allow_html=True)
        st.markdown('<div class="back-btn">', unsafe_allow_html=True)
        if st.button("Exit", use_container_width=True):
            st.session_state.exited = True
        st.markdown('</div>', unsafe_allow_html=True)