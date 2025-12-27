import streamlit as st
import random
import datetime
import os
import base64

# --- KONFIGURATION ---
st.set_page_config(page_title="FocusSwitch Pro", page_icon="🛑", layout="centered")

# --- HILFSFUNKTIONEN ---
def get_stats():
    if not os.path.exists("stats.txt"):
        return 0
    with open("stats.txt", "r") as f:
        return int(f.read())

def increment_stats():
    count = get_stats() + 1
    with open("stats.txt", "w") as f:
        f.write(str(count))
    return count

def play_sound():
    # Ein kurzer, sauberer "Blip" Sound
    sound_html = """
        <audio autoplay>
            <source src="https://www.soundjay.com/buttons/sounds/button-16.mp3" type="audio/mpeg">
        </audio>
    """
    st.markdown(sound_html, unsafe_allow_html=True)

# --- CSS (STOPPSCHILD & STYLING) ---
st.markdown("""
    <style>
    .stButton>button {
        background-color: #CC0000; color: white; font-size: 50px;
        font-weight: bold; height: 220px; width: 220px;
        border-radius: 20%; border: 5px solid white;
        display: block; margin: auto; box-shadow: 0px 10px 20px rgba(0,0,0,0.3);
    }
    .stats-box {
        text-align: center; padding: 10px; background: #e1e4e8;
        border-radius: 10px; margin-top: 20px; font-weight: bold;
    }
    </style>
    """, unsafe_allow_html=True)

# --- APP LOGIK ---
st.title("🛑 FocusSwitch Pro")
st.write("Dein Werkzeug gegen Grübelschleifen.")

col1, col2, col3 = st.columns([1, 2, 1])

with col2:
    if st.button("STOPP"):
        play_sound()
        count = increment_stats()
        st.session_state.triggered = True
        st.session_state.count = count
        
        # KI-Interessen
        interests = ["Quantenphysik", "Stoische Philosophie", "Technik der Zukunft", "Römische Geschichte"]
        st.session_state.topic = random.choice(interests)
        
        # Hier die Platzhalter-Logik (oder dein API-Call)
        st.session_state.content = f"Interessanter Fakt über {st.session_state.topic}: [Hier generiert die KI einen tiefen Einblick...]"

# Ergebnisanzeige
if st.session_state.get('triggered'):
    st.markdown(f"### 🧠 Fokus-Wechsel: {st.session_state.topic}")
    st.info(st.session_state.content)
    
    st.markdown(f"""
        <div class='stats-box'>
            ✅ Du hast heute bereits {st.session_state.count} Mal aktiv deinen Fokus zurückgeholt!
        </div>
    """, unsafe_allow_html=True)
    
    st.text_area("Analysiere diesen Fakt kurz:", placeholder="Tippe hier, um dein Gehirn zu fordern...")

# --- ANLEITUNG ZUM DEPLOYMENT (PUNKT 3) ---
with st.expander("🚀 So bringst du die App auf dein Handy (Kostenlos)"):
    st.write("""
    1. Erstelle einen kostenlosen Account bei [GitHub](https://github.com).
    2. Lade diese Datei (`focus_switch.py`) dort in ein neues 'Repository' hoch.
    3. Gehe zu [streamlit.io/cloud](https://streamlit.io/cloud) und verbinde deinen GitHub-Account.
    4. Wähle dein Repository aus – Streamlit gibt dir eine URL (z.B. `deine-app.streamlit.app`).
    5. Öffne die URL am Handy im Browser und wähle im Menü 'Zum Startbildschirm hinzufügen'.
    """)