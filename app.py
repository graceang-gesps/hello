import streamlit as st
import random

# --- PAGE CONFIGURATION ---
st.set_page_config(
    page_title="Rhythm Rascals! 🥁",
    page_icon="🎵",
    layout="centered"
)

# --- INITIALIZE SESSION STATE ---
if "score" not in st.session_state:
    st.session_state.score = 0
if "level" not in st.session_state:
    st.session_state.level = 1
if "streak" not in st.session_state:
    st.session_state.streak = 0
if "current_q" not in st.session_state:
    st.session_state.current_q = None
if "feedback" not in st.session_state:
    st.session_state.feedback = None
if "selected_option" not in st.session_state:
    st.session_state.selected_option = None

# --- RHYTHM QUESTION BANK ---
# Designed specifically for 8-year-olds using standard elementary music syllables
QUESTIONS = [
    {
        "title": "The Walking Bear 🐻",
        "emojis": "🚶‍♂️ 🚶‍♂️ 🚶‍♂️ 🚶‍♂️",
        "correct": "Ta - Ta - Ta - Ta",
        "wrong": ["Ta - Ti-Ti - Ta - Ta", "Ta - Ta - Rest - Ta"],
        "why": "Quarter notes ('Ta') sound like taking big, steady walking steps. One count for each step!"
    },
    {
        "title": "The Running Rabbit 🐇",
        "emojis": "🐇 🐇 🚶‍♂️ 🚶‍♂️",
        "correct": "Ti-Ti - Ti-Ti - Ta - Ta",
        "wrong": ["Ta - Ta - Ti-Ti - Ti-Ti", "Ti-Ti - Rest - Ta - Ta"],
        "why": "Eighth notes ('Ti-Ti') move twice as fast! Two quick rabbit hops fit into one regular walking step."
    },
    {
        "title": "The Sleepy Koala 🐨",
        "emojis": "🚶‍♂️ 🤫 🚶‍♂️ 🤫",
        "correct": "Ta - Rest - Ta - Rest",
        "wrong": ["Ta - Ta - Ta - Rest", "Rest - Rest - Ti-Ti - Ta"],
        "why": "The zip-lip emoji '🤫' means a 'Rest'. In music, a rest is golden silence—don't clap on a rest!"
    },
    {
        "title": "The Kangaroo Dance 🦘",
        "emojis": "🦘 🤫 🦘 🚶‍♂️",
        "correct": "Ti-Ti - Rest - Ti-Ti - Ta",
        "wrong": ["Ta - Rest - Ti-Ti - Ta", "Ti-Ti - Ti-Ti - Rest - Rest"],
        "why": "This pattern starts with two quick hops ('Ti-Ti'), followed by a quiet pause ('Rest'), another quick hop, and a landing step!"
    },
    {
        "title": "The Speeding Racecar 🏎️",
        "emojis": "🐇 🐇 🐇 🐇",
        "correct": "Ti-Ti - Ti-Ti - Ti-Ti - Ti-Ti",
        "wrong": ["Ta - Ta - Ta - Ta", "Ti-Ti - Rest - Ti-Ti - Rest"],
        "why": "Nothing but speed! Four fast double-steps in a row make this pattern super energetic."
    }
]

# --- GAME FUNCTIONS ---
def generate_question():
    st.session_state.current_q = random.choice(QUESTIONS)
    # Combine correct and wrong answers, then shuffle them
    all_options = [st.session_state.current_q["correct"]] + st.session_state.current_q["wrong"]
    random.shuffle(all_options)
    st.session_state.options = all_options
    st.session_state.feedback = None
    st.session_state.selected_option = None

# Load first question if empty
if st.session_state.current_q is None:
    generate_question()

q = st.session_state.current_q

# --- MAIN UI DISPLAY ---
st.title("🥁 Rhythm Rascals Academy!")
st.subheader("Crack the musical emoji codes with your friends!")

# Scoreboard
col1, col2, col3 = st.columns(3)
with col1:
    st.metric(label="⭐ Total Score", value=st.session_state.score)
with col2:
    st.metric(label="🏆 Level", value=st.session_state.level)
with col3:
    st.metric(label="🔥 Win Streak", value=st.session_state.streak)

st.markdown("---")

# --- THE CHALLENGE PANEL ---
st.markdown(f"### 🎵 Target Pattern: **{q['title']}**")
st.write("Look at the creature steps below and figure out the matching rhythm pattern:")

# Giant visual centering for children
st.markdown(f"<div style='text-align: center; background-color: #f0f2f6; padding: 20px; border-radius: 15px; margin: 15px 0;'><h1 style='font-size: 70px; margin: 0;'>{q['emojis']}</h1></div>", unsafe_with_html=True)

# Interactive Sound Prompt (Fun fallback button)
if st.button("🔊 Tap to listen to the tempo heartbeat!", use_container_width=True):
    st.toast("Tick... Tock... Tick... Tock... Keep that steady beat in your head!", icon="⏱️")

st.write("#### Match the rhythm code:")

# Render choices cleanly as big button triggers using columns or a uniform radio list
for option in st.session_state.options:
    if st.button(f"🎵 {option}", use_container_width=True, key=f"btn_{option}"):
        st.session_state.selected_option = option
        if option == q["correct"]:
            st.session_state.feedback = "correct"
        else:
            st.session_state.feedback = "wrong"

# --- ACTIONABLE FEEDBACK ---
if st.session_state.feedback == "correct":
    st.balloons()
    st.success("🎉 **YOU GOT IT! You're a Rhythm Superstar!**")
    
    # Simple, interactive explanation block
    st.info(f"💡 **How it works:** {q['why']}")
    
    # Safe multi-step updating to prevent duplication on reruns
    if st.button("Next Rhythm Challenge ➡️", type="primary", use_container_width=True):
        st.session_state.score += 10
        st.session_state.streak += 1
        if st.session_state.score % 30 == 0:
            st.session_state.level += 1
        generate_question()
        st.rerun()

elif st.session_state.feedback == "wrong":
    st.error("😭 **Ooops! Not quite right, but don't give up!**")
    st.warning("🔍 **Hint:** Look at the pictures again. Every character makes a fast or slow sound, but the '🤫' always means a silent **Rest**!")
    
    if st.button("Try Another Pattern 🔄", use_container_width=True):
        st.session_state.streak = 0  # Reset streak
        generate_question()
        st.rerun()

# --- COOPERATIVE MULTIPLAYER DESIGN ---
st.markdown("---")
with st.expander("👥 How to play together (Co-op mode!):", expanded=True):
    st.markdown("""
    Streamlit runs in your browser, making it perfect to pass around or display on a smart TV! 
    
    * **Player 1 (The Composer):** Claps out the emoji code shown on screen using your hands or a toy drum! 
    * **Player 2 (The Listener):** Listens to Player 1's claps without looking at the screen, and shouts out the pattern!
    * **Take Turns:** Pass the mouse or tablet back and forth after every question. Can you work together to hit **Level 5**?
    """)
