import streamlit as st
import base64
from gtts import gTTS
import io

# Function to get base64 of background image
def get_base64_of_bin_file(bin_file):
    with open(bin_file, 'rb') as f:
        data = f.read()
    return base64.b64encode(data).decode()

# Load background image
img_base64 = get_base64_of_bin_file("bg.jpg")

# Apply custom CSS for background and enhanced button styling
st.markdown(
    f"""
    <style>
    .stApp {{
        background-image: url("data:image/jpg;base64,{img_base64}");
        background-size: cover;
        background-position: center;
        background-repeat: no-repeat;
    }}
    .stButton > button {{
        width: 100%;
        height: 60px;
        font-size: 18px;
        font-weight: bold;
        border-radius: 10px;
        border: 2px solid white;
        color: white;
        background: linear-gradient(to right, navy, darkblue);
        box-shadow: 0 4px 8px rgba(0, 0, 0, 0.2);
        transition: all 0.3s ease;
    }}
    .stButton > button:hover {{
        background: linear-gradient(to right, darkblue, navy);
        color: yellow;
        box-shadow: 0 6px 12px rgba(0, 0, 0, 0.3);
        transform: translateY(-2px);
    }}
    .title {{
        text-align: center;
        color: white;
        background-color: white;
        padding: 15px;
        margin: 10px 0;
        border-radius: 10px;
        text-shadow: 2px 2px 4px rgba(0,0,0,0.5);
        box-shadow: 0 4px 8px rgba(0, 0, 0, 0.3);
    }}
    .exam-title {{
        color: white;
        text-align: center;
        font-weight: bold;
        text-shadow: 1px 1px 2px rgba(0,0,0,0.5);
    }}
    .exam-desc {{
        color: white;  /* Changed to white for better visibility */
        text-align: center;
        margin-bottom: 20px;
        text-shadow: 1px 1px 2px rgba(0,0,0,0.3);
    }}
    .read-aloud-button > button {{
        background: linear-gradient(to right, green, darkgreen);
        color: white;
    }}
    .read-aloud-button > button:hover {{
        background: linear-gradient(to right, darkgreen, green);
        color: yellow;
    }}
    .back-button > button {{
        background: linear-gradient(to right, orange, darkorange);
        color: white;
        box-shadow: 0 4px 8px rgba(255, 165, 0, 0.4);
    }}
    .back-button > button:hover {{
        background: linear-gradient(to right, darkorange, orange);
        color: white;
        box-shadow: 0 6px 12px rgba(255, 165, 0, 0.5);
        transform: translateY(-2px);
    }}
    .exit-button > button {{
        background: linear-gradient(to right, red, darkred);
        color: white;
    }}
    .exit-button > button:hover {{
        background: linear-gradient(to right, darkred, red);
        color: yellow;
    }}
    </style>
    """,
    unsafe_allow_html=True
)

# Exams data
exams = {
    "10th": [
        ("1. SSC MTS", "Entry-level positions in central government offices."),
        ("2. Indian Army Soldier", "Join the Indian Army as a soldier."),
        ("3. Railway Group D", "Jobs in Indian Railways for maintenance and support staff."),
        ("4. State Police Constable", "Recruitment for constable positions."),
        ("5. Indian Navy MR", "Entry-level positions in the Indian Navy."),
        ("6. Air Force Group Y", "Non-technical roles in the Indian Air Force."),
        ("7. Coast Guard Navik", "Entry-level positions in the Coast Guard."),
        ("8. DRDO CEPTAM", "Admin & Allied roles in DRDO."),
        ("9. BSF Constable", "Border Security Force jobs."),
        ("10. Post Office GDS", "Gramin Dak Sevak posts."),
        ("11. Forest Guard", "State forest departments."),
        ("12. Apprenticeship in PSUs", "BHEL, SAIL, etc."),
        ("13. Anganwadi Helper", "Rural child welfare programs."),
        ("14. Home Guard", "State-level home guard recruitment."),
        ("15. Peon/Clerk", "Clerical jobs in state and central government offices."),
    ],
    "12th": [
        ("1. SSC / CHSL", "Clerical and data entry jobs."),
        ("2. NDA", "Officer training in Indian Armed Forces."),
        ("3. Railway Clerk", "Clerical positions."),
        ("4. Sub-Inspector Exams", "State police recruitment."),
        ("5. Navy SSR", "Technical roles in the Navy."),
        ("6. Air Force Group X", "Technical roles."),
        ("7. LIC ADO", "LIC entry-level jobs."),
        ("8. IBPS/SBI Clerk", "Bank clerk positions."),
        ("9. Postman/Mail Guard", "Postal Department."),
        ("10. Revenue Dept Exams", "Patwari and clerical roles."),
        ("11. Forest Guard", "State forest departments."),
        ("12. Data Entry Operator", "Clerical jobs in various government departments."),
        ("13. Stenographer", "Stenography jobs in central and state government."),
        ("14. Indian Coast Guard Yantrik", "Technical roles in the Coast Guard."),
        ("15. Police Constable", "State-level police constable recruitment."),
    ],
    "Graduate": [
        ("1. UPSC Civil Services", "IAS, IPS, IFS roles."),
        ("2. SSC CGL", "Central Govt Group B/C posts."),
        ("3. IBPS/SBI PO", "Bank Officer positions."),
        ("4. RBI Grade B", "Reserve Bank roles."),
        ("5. CDS", "Defense officer entry."),
        ("6. ISRO/DRDO Scientist", "Research roles."),
        ("7. GATE", "Engineering & PSU jobs."),
        ("8. KVS/NVS Teachers", "Teaching jobs."),
        ("9. UGC/CSIR NET", "Research/lectureship."),
        ("10. Indian Forest Services", "Forest officer roles."),
        ("11. Assistant Professor", "Teaching jobs in universities and colleges."),
        ("12. Public Sector Banks", "Specialist Officer roles."),
        ("13. State PCS", "State-level administrative services."),
        ("14. Indian Railways", "Group A and B officer roles."),
        ("15. Judicial Services", "Entry-level judge positions for law graduates."),
    ],
}

# Use session state to manage views
if 'view' not in st.session_state:
    st.session_state.view = None

# Main view
if st.session_state.view is None:
    st.markdown("<h1 class='title'>Select Your Education Qualification</h1>", unsafe_allow_html=True)
    
    # Symmetric button layout with equal spacing
    st.markdown("<br>", unsafe_allow_html=True)
    col1, col2, col3 = st.columns(3)
    with col1:
        if st.button("10th"):
            st.session_state.view = "10th"
            st.rerun()
    with col2:
        if st.button("12th"):
            st.session_state.view = "12th"
            st.rerun()
    with col3:
        if st.button("Graduate"):
            st.session_state.view = "Graduate"
            st.rerun()
    
    # Centered Exit button with red color
    st.markdown("<br><br>", unsafe_allow_html=True)
    col_exit1, col_exit2, col_exit3 = st.columns(3)
    with col_exit2:
        st.markdown('<div class="exit-button">', unsafe_allow_html=True)
        st.button("Exit", key="main_exit")
        st.markdown('</div>', unsafe_allow_html=True)

# Exams view
else:
    qualification = st.session_state.view
    st.markdown(f"<h1 class='title'>Govt Exams after {qualification}</h1>", unsafe_allow_html=True)
    
    # Display exams in a styled, centered format
    for title, desc in exams.get(qualification, []):
        st.markdown(f"<div class='exam-title'>{title}</div>", unsafe_allow_html=True)
        st.markdown(f"<div class='exam-desc'>{desc}</div>", unsafe_allow_html=True)
    
    # Build full text for TTS
    full_text = ""
    for title, desc in exams.get(qualification, []):
        full_text += f"{title}. {desc}. "
    
    # Read Aloud and Back buttons
    col_read, col_back = st.columns(2)
    with col_read.container():
        st.markdown('<div class="read-aloud-button">', unsafe_allow_html=True)
        if st.button("Read Aloud", key="read_aloud"):
            tts = gTTS(full_text)
            fp = io.BytesIO()
            tts.write_to_fp(fp)
            fp.seek(0)
            audio_bytes = fp.read()
            base64_audio = base64.b64encode(audio_bytes).decode()
            st.markdown(f'<audio src="data:audio/mp3;base64,{base64_audio}" autoplay></audio>', unsafe_allow_html=True)
        st.markdown('</div>', unsafe_allow_html=True)
    
    with col_back.container():
        st.markdown('<div class="back-button">', unsafe_allow_html=True)
        if st.button("Back", key="back"):
            st.session_state.view = None
            st.rerun()
        st.markdown('</div>', unsafe_allow_html=True)