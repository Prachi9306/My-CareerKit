import streamlit as st
from gtts import gTTS
import base64
import io

# -------------------- BACKGROUND IMAGE + CUSTOM STYLES --------------------
def get_base64(bin_file):
    with open(bin_file, "rb") as f:
        data = f.read()
    return base64.b64encode(data).decode()


def set_background_and_styles():
    bg_image = get_base64("assets/bg.jpg")
    st.markdown(
        f"""
        <style>
        .stApp {{
            background-image: url("data:image/jpg;base64,{bg_image}");
            background-size: cover;
            background-repeat: no-repeat;
            background-attachment: fixed;
            font-family: 'Poppins', sans-serif;
        }}
        .main-header {{
            color: navy;
            background-color: rgba(255,255,255,0.85);
            text-align: center;
            padding: 25px;
            border-radius: 15px;
            box-shadow: 0 6px 12px rgba(0,0,0,0.2);
            font-size: 42px;
            font-weight: 800;
            margin-bottom: 30px;
        }}
        .question-card {{
            background-color: rgba(255,255,255,0.92);
            padding: 25px;
            border-radius: 12px;
            box-shadow: 0 4px 10px rgba(0,0,0,0.15);
            margin-bottom: 30px;
        }}
        .question-text {{
            color: white;
            text-shadow: 2px 2px 4px rgba(0,0,0,0.5);
            text-align: center;
            font-size: 26px;
            font-weight: 700;
            margin-bottom: 20px;
        }}
        .stButton > button {{
            background-color: navy !important;
            color: white !important;
            font-size: 18px !important;
            font-weight: 600 !important;
            border-radius: 10px !important;
            padding: 12px 20px !important;
            width: 100% !important;
            white-space: normal !important;
            text-align: center !important;
            transition: all 0.3s ease !important;
            min-height: 60px;
            display: flex;
            align-items: center;
            justify-content: center;
        }}
        .stButton > button:hover {{
            background-color: #001f4d !important;
            transform: scale(1.04);
            box-shadow: 0 4px 8px rgba(0,0,0,0.3);
        }}
        .nav-btn {{
            background-color: #4682b4 !important;
        }}
        .nav-btn:hover {{
            background-color: #4169e1 !important;
        }}
        .exit-btn {{
            background-color: #b22222 !important;
        }}
        .exit-btn:hover {{
            background-color: #8b0000 !important;
        }}
        .result-card {{
            background-color: rgba(255,255,255,0.92);
            border-radius: 12px;
            padding: 20px;
            margin-top: 20px;
            box-shadow: 0 4px 10px rgba(0,0,0,0.15);
        }}
        .result-item {{
            background-color: navy;
            color: white;
            text-align: center;
            padding: 12px;
            border-radius: 8px;
            margin: 8px 0;
            font-size: 20px;
            font-weight: 600;
            transition: all 0.3s ease;
        }}
        .result-item:hover {{
            transform: scale(1.05);
            box-shadow: 0 4px 10px rgba(0,0,0,0.3);
        }}
        </style>
        """,
        unsafe_allow_html=True
    )

# -------------------- DATA DEFINITIONS --------------------
questions = [
    ("Which task sounds most exciting to you?",
     ["Coding an app", "Helping someone recover", "Shooting a short film", "Debating an issue",
      "Planting trees", "Teaching a class", "Launching a business", "Training athletes",
      "Planning a luxury trip", "Fixing a car"]),
    ("Which class would you enjoy the most?",
     ["Computer Science", "Biology", "Drama", "Political Science",
      "Environmental Studies", "Psychology", "Economics", "Physical Education",
      "Hotel Management", "Workshop/Shop class"]),
    ("Your dream work setting is:",
     ["Tech lab", "Clinic or hospital", "Film or studio", "Courtroom",
      "Nature or lab", "School", "Office or boardroom", "Gym or stadium",
      "Resort or cruise", "Garage or construction site"]),
    ("In your free time, you'd rather:",
     ["Tinker with tech", "Care for someone", "Draw or record", "Join a youth debate",
      "Volunteer for an eco cause", "Tutor someone", "Read business books", "Work out",
      "Travel or explore places", "Fix something mechanical"]),
    ("What motivates you the most?",
     ["Solving hard problems", "Making a difference in lives", "Creating something original", "Fighting for justice",
      "Protecting the Earth", "Helping others grow", "Succeeding in business", "Winning or competing",
      "Hosting and serving", "Using your hands and tools"]),
    ("Your ideal project is:",
     ["A machine that solves a problem", "A campaign for mental health", "A short film or art series",
      "A new law or policy", "A sustainable product", "An educational video series", "An online business",
      "A fitness program", "A hotel launch", "A new gadget"]),
    ("Which of these people do you admire most?",
     ["Elon Musk", "Doctors Without Borders volunteers", "Filmmakers or artists", "Supreme Court judges",
      "Greta Thunberg", "Teachers or professors", "Entrepreneurs", "Athletes",
      "Chefs", "Electricians or builders"]),
    ("How do you solve problems?",
     ["Logically with data", "Empathetically with care", "Creatively with design", "Critically with arguments",
      "Practically with eco-solutions", "Clearly with explanations", "Strategically with planning",
      "Physically with movement", "Service-first approach", "With tools and hands"]),
    ("What's your dream goal?",
     ["Invent new tech", "Heal or treat", "Inspire or express", "Uplift society",
      "Save the planet", "Educate the world", "Build a company", "Break sports records",
      "Travel the world", "Be a master craftsperson"]),
    ("What skill do you want to master?",
     ["AI or robotics", "Medical science", "Photography or acting", "Law or public speaking",
      "Climate science", "Mentoring", "Marketing or leadership", "Training routines",
      "Hospitality skills", "Electrical or carpentry work"])
]

categories = [
    "STEM", "Health & Medical", "Arts & Media", "Law & Government",
    "Environment & Sustainability", "Education & Training", "Business & Management",
    "Sports & Fitness", "Hospitality & Tourism", "Skilled Trades"
]

recommendations = {
    "STEM": [
        "Software Engineer", "AI Developer", "Data Analyst", "Robotics Engineer", 
        "Web Developer", "App Developer", "Product Designer", "Game Developer"
    ],
    "Health & Medical": [
        "Doctor", "Nurse", "Physiotherapist", "Psychologist", 
        "Public Health Expert", "Speech Therapist", "Medical Lab Technician"
    ],
    "Arts & Media": [
        "Graphic Designer", "Animator", "Content Creator", "Filmmaker", 
        "Actor", "Fashion Designer", "Illustrator", "Creative Director"
    ],
    "Law & Government": [
        "Lawyer", "Judge", "Civil Servant", "Human Rights Advocate", 
        "Policy Analyst", "Diplomat", "Legal Researcher"
    ],
    "Environment & Sustainability": [
        "Environmental Scientist", "Ecologist", "Sustainability Consultant", 
        "Renewable Energy Expert", "Climate Analyst", "Wildlife Biologist"
    ],
    "Education & Training": [
        "Teacher", "Professor", "Education Counselor", "Curriculum Developer", 
        "Corporate Trainer", "Special Ed Teacher", "Academic Researcher"
    ],
    "Business & Management": [
        "Entrepreneur", "Marketing Manager", "Business Analyst", "Project Manager", 
        "Sales Executive", "Product Manager", "Startup Founder"
    ],
    "Sports & Fitness": [
        "Athlete", "Coach", "Fitness Trainer", "Physiotherapist", 
        "Sports Nutritionist", "PE Teacher", "Recreational Therapist"
    ],
    "Hospitality & Tourism": [
        "Hotel Manager", "Chef", "Event Planner", "Travel Agent", 
        "Tour Guide", "Cruise Director", "Resort Manager"
    ],
    "Skilled Trades": [
        "Electrician", "Plumber", "Mechanic", "Carpenter", 
        "Welder", "Technician", "Construction Supervisor"
    ]
}

# Wrap the interactive UI inside a function so this module can be imported safely
def run_quiz():
    set_background_and_styles()

    # Small helper: allow returning to the main app from inside the quiz
    try:
        if st.button("⬅ Back to Main"):
            st.session_state.page = "main"
            st.rerun()
    except Exception:
        # If session_state isn't available yet, ignore gracefully
        pass

    # -------------------- SESSION STATE --------------------
    if "page" not in st.session_state:
        st.session_state.page = "welcome"
    if "current_q" not in st.session_state:
        st.session_state.current_q = 0
    if "answers" not in st.session_state:
        st.session_state.answers = []

    # -------------------- PAGE: WELCOME --------------------
    if st.session_state.page == "welcome":
        st.markdown('<div class="main-header">🎓 Welcome to the Career Interest Quiz</div>', unsafe_allow_html=True)
        _, col, _ = st.columns([1, 2, 1])
        with col:
            #st.markdown('<div class="question-card" style="text-align:center;">', unsafe_allow_html=True)
            st.markdown('<p style="color:#ffffff; text-align:center; font-weight:700; font-size:20px;">Take this quiz to discover careers that match your interests!</p>', unsafe_allow_html=True)
            if st.button("🚀 Start Quiz", use_container_width=True):
                st.session_state.page = "quiz"
                st.session_state.current_q = 0
                st.session_state.answers = []
                st.rerun()
            if st.button("❌ Exit", use_container_width=True):
                st.stop()
            st.markdown("</div>", unsafe_allow_html=True)

    # -------------------- PAGE: QUIZ --------------------
    elif st.session_state.page == "quiz":
        q_index = st.session_state.current_q
        if q_index >= len(questions):
            # Compute best fit
            counts = [0] * len(categories)
            for i, ans in enumerate(st.session_state.answers):
                cat_idx = questions[i][1].index(ans)
                counts[cat_idx] += 1
            best_fit = categories[counts.index(max(counts))]
            st.session_state.best_fit = best_fit
            st.session_state.page = "result"
            st.rerun()
        else:
            q_text, options = questions[q_index]
            st.markdown(f'<div class="question-text">{q_text}</div>', unsafe_allow_html=True)

            # Display options in a 2-column symmetric grid
            cols = st.columns(2)
            for i, opt in enumerate(options):
                with cols[i % 2]:
                    if st.button(opt, key=f"q{q_index}_opt{i}", use_container_width=True):
                        st.session_state.answers.append(opt)
                        st.session_state.current_q += 1
                        st.rerun()

            # Navigation buttons
            c1, c2, c3 = st.columns(3)
            with c1:
                if q_index > 0 and st.button("⬅️ Previous", key=f"prev_{q_index}", use_container_width=True):
                    st.session_state.answers.pop()
                    st.session_state.current_q -= 1
                    st.rerun()
            with c2:
                if st.button("🔊 Read Aloud", key=f"read_{q_index}", use_container_width=True):
                    text = f"{q_text}. The options are: {', '.join(options)}."
                    tts = gTTS(text)
                    fp = io.BytesIO()
                    tts.write_to_fp(fp)
                    fp.seek(0)
                    st.audio(fp, format="audio/mp3")
            with c3:
                if st.button("❌ Exit", key=f"exit_{q_index}", use_container_width=True):
                    st.session_state.page = "welcome"
                    st.rerun()

    # -------------------- PAGE: RESULT --------------------
    elif st.session_state.page == "result":
        best_fit = st.session_state.best_fit
        careers = recommendations[best_fit]
        st.markdown(f'<div class="main-header">{best_fit} Career Suggestions</div>', unsafe_allow_html=True)
        cols = st.columns(2)
        for i, c in enumerate(careers):
            with cols[i % 2]:
                st.markdown(f'<div class="result-item">• {c}</div>', unsafe_allow_html=True)

        st.markdown("</div>", unsafe_allow_html=True)

        c1, c2 = st.columns(2)
        with c1:
            if st.button("🔊 Read Aloud", use_container_width=True):
                text = f"{best_fit} Career Suggestions are: {'. '.join(careers)}."
                tts = gTTS(text)
                fp = io.BytesIO()
                tts.write_to_fp(fp)
                fp.seek(0)
                st.audio(fp, format="audio/mp3")
        with c2:
            if st.button("🏠 Restart", use_container_width=True):
                st.session_state.page = "welcome"
                st.rerun()


# Allow running attempt_quiz.py directly
if __name__ == "__main__":
    run_quiz()

def run_quiz():
    st.title("Career Interest Quiz")
    st.write("This is where your quiz questions appear.")    