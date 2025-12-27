import streamlit as st
import google.generativeai as genai
import random
import os

# --- 1. KI KONFIGURATION ---
try:
    genai.configure(api_key=st.secrets["gemini_key"])
    model = genai.GenerativeModel('gemini-1.5-flash')
except Exception as e:
    st.error("API Key fehlt oder ist ungültig. Bitte in den Streamlit Secrets hinterlegen.")

# --- 2. HILFSFUNKTIONEN ---
def get_stats():
    # Wir nutzen st.session_state für die Session-Statistik
    if 'total_stops' not in st.session_state:
        st.session_state.total_stops = 0
    return st.session_state.total_stops

def play_sound():
    # Kurzer akustischer Reiz zur Unterbrechung
    sound_html = """
        <audio autoplay>
            <source src="https://www.soundjay.com/buttons/sounds/button-16.mp3" type="audio/mpeg">
        </audio>
    """
    st.markdown(sound_html, unsafe_allow_html=True)

def get_ai_response(topic):
    prompt = f"""
    KONTEXT: Der User steckt in einer Grübelschleife (Trennungsschmerz). 
    AUFGABE: Unterbrich das Grübeln sofort mit einem faszinierenden, komplexen Fakt über {topic}.
    STIL: Wissenschaftlich, stoisch, intellektuell fordernd. Keine Esoterik, kein Mitleid.
    STRUKTUR: 
    1. Ein kurzer, krasser Fakt.
    2. Eine Transferaufgabe oder Logik-Frage, die aktives Denken erfordert.
    """
    try:
        response = model.generate_content(prompt)
        return response.text
    except:
        return "Fokus-Wechsel fehlgeschlagen. Zähle stattdessen die Primzahlen von 1 bis 20 rückwärts!"

# --- 3. UI & DESIGN ---
st.set_page_config(page_title="FocusSwitch", page_icon="🛑")

st.markdown("""
    <style>
    /* Das Stoppschild-Design */
    .stButton>button {
        background-color: #CC0000;
        color: white;
        font-size: 40px;
        font-weight: bold;
        height: 220px;
        width: 220px;
        border-radius: 20%; /* Achteck-Annäherung */
        border: 6px solid white;
        display: block;
        margin: auto;
        box-shadow: 0px 10px 25px rgba(0,0,0,0.4);
        transition: all 0.2s;
    }
    .stButton>button:hover {
        background-color: #FF0000;
        transform: scale(1.02);
        border-color: #eeeeee;
    }
    .stats-container {
        text-align: center;
        background-color: #f0f2f6;
        padding: 15px;
        border-radius: 15px;
        margin-top: 30px;
        border: 1px solid #d1d5db;
    }
    </style>
    """, unsafe_allow_html=True)

# --- 4. HAUPTSEITE ---
st.title("🛑 FocusSwitch")
st.write("Drücke den Button, sobald das Grübeln beginnt.")

# Interessen-Pool für die KI
INTERESTS = ["Quantenmechanik", "Stoische Philosophie", "Römische Strategie", "Neurobiologie", "Astrophysik", "Spieltheorie"]

# Initialisiere Session State Variablen, falls sie noch nicht existieren
if 'total_stops' not in st.session_state:
    st.session_state.total_stops = 0
if 'show_result' not in st.session_state:
    st.session_state.show_result = False

col1, col2, col3 = st.columns([1, 2, 1])

with col2:
    if st.button("STOPP"):
        play_sound()
        st.session_state.total_stops += 1
        topic = random.choice(INTERESTS)
        st.session_state.active_topic = topic
        
        with st.spinner('Extrahiere Fokus-Thema...'):
            # HIER wird jetzt die echte KI aufgerufen:
            st.session_state.active_content = get_ai_response(topic)
        
        st.session_state.show_result = True

# --- 5. ERGEBNIS-ANZEIGE ---
if st.session_state.show_result:
    st.divider()
    st.markdown(f"### 🧠 Neuer Fokus: {st.session_state.active_topic}")
    
    # Hier wird der echte Inhalt von Gemini angezeigt
    st.info(st.session_state.active_content)
    
    # Statistik Anzeige
    st.markdown(f"""
        <div class="stats-container">
            <b>Fortschritt heute:</b><br>
            Du hast bereits {st.session_state.total_stops} Mal erfolgreich die Reißleine gezogen.
        </div>
    """, unsafe_allow_html=True)
    
    # Kognitiver Anker (Input-Feld)
    st.text_area("Deine logische Schlussfolgerung (tippen aktiviert den Verstand):", 
                 key="logic_input_field",
                 placeholder="Schreibe hier kurz deinen Gedanken zum Thema auf...")
