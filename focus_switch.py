import streamlit as st
import google.generativeai as genai
import random

# --- 1. KI KONFIGURATION ---
def init_gemini():
    try:
        genai.configure(api_key=st.secrets["gemini_key"])
        # Wir verzichten auf das Präfix 'models/' für maximale Kompatibilität
        return genai.GenerativeModel('gemini-1.5-flash')
    except Exception as e:
        st.error(f"Initialisierungsfehler: {e}")
        return None

model = init_gemini()

# --- 2. LOGIK FUNKTION ---
def get_ai_response(topic):
    prompt = f"""
    Unterbrich das Grübeln sofort mit einem faszinierenden wissenschaftlichen Fakt über {topic}.
    Stelle danach eine logische Transferfrage.
    Stil: Sachlich, keine Empathie-Floskeln.
    """
    try:
        # Wir nutzen den direkten Aufruf ohne v1beta-Erzwingung
        response = model.generate_content(prompt)
        return response.text
    except Exception as e:
        # Letzter Rettungsanker: Falls das Modell nicht gefunden wird
        return f"Konnte keine KI-Verbindung aufbauen. Nutze den manuellen Stopp: Zähle 10 blaue Dinge in deinem Raum auf. (Fehler: {str(e)})"

# --- 3. UI & CSS (GEKÜRZT FÜR ÜBERSICHT) ---
st.set_page_config(page_title="FocusSwitch", page_icon="🛑")
st.markdown("<style>.stButton>button {background-color: #CC0000; color: white; font-size: 40px; font-weight: bold; height: 220px; width: 220px; border-radius: 20%; border: 6px solid white; display: block; margin: auto;}</style>", unsafe_allow_html=True)

# --- 4. APP ABLAUF ---
st.title("🛑 FocusSwitch")

if 'total_stops' not in st.session_state:
    st.session_state.total_stops = 0

INTERESTS = ["Quantenmechanik", "Stoische Philosophie", "Neurobiologie", "Astrophysik", "Spieltheorie"]

col1, col2, col3 = st.columns([1, 2, 1])
with col2:
    if st.button("STOPP"):
        st.session_state.total_stops += 1
        topic = random.choice(INTERESTS)
        st.session_state.active_topic = topic
        with st.spinner('Fokus wird gewechselt...'):
            st.session_state.active_content = get_ai_response(topic)
        st.session_state.show_result = True

if st.session_state.get('show_result'):
    st.divider()
    st.markdown(f"### 🧠 Thema: {st.session_state.active_topic}")
    st.info(st.session_state.active_content)
    st.write(f"**Erfolgreiche Stopps heute:** {st.session_state.total_stops}")
