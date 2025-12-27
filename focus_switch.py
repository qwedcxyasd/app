import streamlit as st
import google.generativeai as genai
import random

# --- 1. KI KONFIGURATION ---
try:
    genai.configure(api_key=st.secrets["gemini_key"])
    # Wir stellen sicher, dass wir das Modell korrekt ansprechen
    model = genai.GenerativeModel('models/gemini-1.5-flash') 
except Exception as e:
    st.error(f"Konfigurationsfehler: {str(e)}")

# --- 2. LOGIK FUNKTION ---
def get_ai_response(topic):
    prompt = f"""
    KONTEXT: Der User steckt in einer Grübelschleife. 
    AUFGABE: Unterbrich das Grübeln sofort mit einem faszinierenden Fakt über {topic}.
    STIL: Wissenschaftlich, fordernd. Keine Esoterik.
    STRUKTUR: Ein kurzer Fakt, gefolgt von einer Transferfrage.
    """
    try:
        # Falls v1beta nötig ist, wird das hier oft automatisch geregelt, 
        # aber wir nutzen den sichersten Aufruf:
        response = model.generate_content(prompt)
        return response.text
    except Exception as e:
        # Falls es immer noch ein Modell-Fehler ist, versuchen wir das 1.0 Pro Modell als Backup
        try:
            backup_model = genai.GenerativeModel('gemini-pro')
            response = backup_model.generate_content(prompt)
            return response.text
        except:
            return f"Technischer Fehler: {str(e)}. Bitte prüfe, ob dein API-Key im Google AI Studio Zugriff auf 'Gemini 1.5 Flash' hat."
# --- 3. UI & CSS ---
st.set_page_config(page_title="FocusSwitch", page_icon="🛑")

st.markdown("""
    <style>
    .stButton>button {
        background-color: #CC0000; color: white; font-size: 40px;
        font-weight: bold; height: 220px; width: 220px;
        border-radius: 20%; border: 6px solid white;
        display: block; margin: auto; box-shadow: 0px 10px 25px rgba(0,0,0,0.4);
    }
    .stats-container {
        text-align: center; background-color: #f0f2f6;
        padding: 15px; border-radius: 15px; margin-top: 30px;
    }
    </style>
    """, unsafe_allow_html=True)

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
        # HIER wird die KI-Funktion aufgerufen:
        with st.spinner('Fokus wird gewechselt...'):
            st.session_state.active_content = get_ai_response(topic)
        st.session_state.show_result = True

if st.session_state.get('show_result'):
    st.divider()
    st.markdown(f"### 🧠 Thema: {st.session_state.active_topic}")
    st.info(st.session_state.active_content)
    
    st.markdown(f"""
        <div class="stats-container">
            <b>Fortschritt:</b> Du hast heute {st.session_state.total_stops} Mal den Fokus zurückgeholt.
        </div>
    """, unsafe_allow_html=True)

