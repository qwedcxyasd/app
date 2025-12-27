import streamlit as st
import google.generativeai as genai
import random

# --- 1. KI KONFIGURATION MIT AUTO-SCAN ---
def get_working_model():
    try:
        genai.configure(api_key=st.secrets["gemini_key"])
        
        # Wir listen alle verfügbaren Modelle auf, die Content generieren können
        available_models = [m.name for m in genai.list_models() if 'generateContent' in m.supported_generation_methods]
        
        # Wir suchen nach einem Flash oder Pro Modell
        for model_name in ["models/gemini-1.5-flash", "models/gemini-1.5-flash-latest", "models/gemini-pro"]:
            if model_name in available_models:
                return genai.GenerativeModel(model_name)
        
        # Falls keines der obigen in der Liste ist, nimm das erste verfügbare
        if available_models:
            return genai.GenerativeModel(available_models[0])
    except Exception as e:
        st.error(f"Kritischer Fehler beim Modell-Scan: {e}")
    return None

model = get_working_model()

# --- 2. LOGIK FUNKTION ---
def get_ai_response(topic):
    prompt = f"Gib mir einen extrem interessanten wissenschaftlichen Fakt über {topic}. Stelle danach eine schwierige Transferfrage. Stil: Sachlich, keine Empathie."
    if model is None:
        return "Modell konnte nicht initialisiert werden. Prüfe deine API-Berechtigungen."
    
    try:
        response = model.generate_content(prompt)
        return response.text
    except Exception as e:
        return f"Fehler bei der Generierung: {str(e)}"

# --- 3. UI & CSS ---
st.set_page_config(page_title="FocusSwitch", page_icon="🛑")
st.markdown("<style>.stButton>button {background-color: #CC0000; color: white; font-size: 40px; font-weight: bold; height: 220px; width: 220px; border-radius: 20%; border: 6px solid white; display: block; margin: auto; box-shadow: 0px 10px 25px rgba(0,0,0,0.4);}</style>", unsafe_allow_html=True)

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
        with st.spinner('Modelle werden gescannt und Fokus gewechselt...'):
            st.session_state.active_content = get_ai_response(topic)
        st.session_state.show_result = True

if st.session_state.get('show_result'):
    st.divider()
    st.markdown(f"### 🧠 Thema: {st.session_state.active_topic}")
    st.info(st.session_state.active_content)
    st.write(f"**Erfolgreiche Stopps heute:** {st.session_state.total_stops}")
