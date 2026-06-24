import streamlit as st
import random

# --- PAGE SETUP ---
st.set_page_config(
    page_title="Rhythm Rascals! 🥁",
    page_icon="🎵",
    layout="centered"
)

# --- INITIALIZE GAME STATE ---
if "score" not in st.session_state:
    st.session_state.score = 0
if "level" not in st.session_state:
    st.session_state.level = 1
if "streak" not in st.session_state:
    st.session_state.streak = 0
if "current_q" not in st.session_state:
    st.session_state.current_q = None
if "options" not in st.session_state:
    st.session_state.options = []
if "feedback" not in st.session_state:
    st.session_state.feedback = None
if "answered" not in st.session_state:
    st.session_state.answered = False

# --- RHYTHM DICTIONARY (Questions) ---
QUESTIONS = [
    {
        "title": "The Steady March 🐻",
        "emojis": "🚶‍♂️  🚶‍♂️  🚶‍♂️  🚶‍♂️",
        "correct": "Ta - Ta - Ta - Ta",
        "wrong": ["Ta - Ti-Ti - Ta - Ta", "Ta - Ta - Rest - Ta"],
        "why": "Quarter notes ('Ta') are like taking steady walking steps. One sound for every beat!"
    },
    {
        "title": "The Running Rabbit 🐇",
        "emojis": "🐇 🐇  🚶‍♂️  🚶‍♂️  🚶‍♂️",
        "correct": "Ti-Ti - Ta - Ta - Ta",
        "wrong": ["Ta - Ta - Ti-Ti - Ta", "Ti-Ti - Rest - Ta - Ta"],
        "why": "Eighth notes ('Ti-Ti') move twice as fast! Two quick rabbit hops fit into one regular walking step."
    },
    {
        "title": "The Sleepy Koala 🐨",
        "emojis": "🚶‍♂️  🤫  🚶‍♂️  🤫",
        "correct": "Ta - Rest - Ta - Rest",
        "wrong": ["Ta - Ta - Ta - Rest", "Rest - Rest - Ti-Ti - Ta"],
        "why": "The '🤫' means a 'Rest'. In music, a rest means absolute silence—don't clap here!"
    },
    {
        "title": "The Kangaroo Dance 🦘",
        "emojis": "🦘 🦘  🤫  🦘 🦘  🚶‍♂️",
        "correct": "Ti-Ti - Rest - Ti-Ti - Ta",
        "wrong": ["Ta - Rest - Ti-Ti - Ta", "Ti-Ti - Ti-Ti - Rest - Rest"],
        "why": "Two quick hops ('Ti-Ti'), then a quiet pause ('Rest'), two more quick hops, and a steady landing step!"
    },
    {
        "title": "The Racecar Finish 🏎️",
        "emojis": "🐇 🐇  🐇 🐇  🐇 🐇  🐇 🐇",
        "correct": "Ti-Ti - Ti-Ti - Ti-Ti - Ti-Ti",
        "wrong": ["Ta - Ta - Ta - Ta", "Ti-Ti - Rest - Ti-Ti - Rest"],
        "why": "Pure speed! Four pairs of fast double-steps in a row make this pattern super fast."
    }
]

# --- GAME LOGIC FUNCTIONS ---
def generate_question():
    st.session_state.current_q = random.choice(QUESTIONS)
    all_opts = [st.session_state.current_q["correct"]] + st.session_state.current_q["wrong"]
    random.shuffle(all_opts)
    st.session_state.options = all_opts
    st.session_state.feedback = None
    st.session_state.answered = False

# Load first question on boot
if st.session_state.current_q is None:
    generate_question()

q = st.session_state.current_q

# --- COMPONENT: GAMEPLAY FRAGMENT ---
# st.fragment isolates re-renders so children can play fluidly without entire page flashing
@st.fragment
def play_game():
    st.markdown(f"### 🎵 Code Name: **{q['title']}**")
    st.write("Look at the creature steps below and figure out the rhythm code:")
    
    # Big kid-friendly visual box
    st.markdown(
        f"<div style='text-align: center; background-color: #f0f2f6; padding: 25px; border-radius: 20px; margin: 15px 0;'>"
        f"<h1 style='font-
