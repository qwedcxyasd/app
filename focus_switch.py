import streamlit as st
import google.generativeai as genai
import random

# --- 1. KI KONFIGURATION ---
def get_working_model():
    try:
        genai.configure(api_key=st.secrets["gemini_key"])
        return genai.GenerativeModel('gemini-1.5-flash')
    except Exception as e:
        st.error(f"Fehler: {e}")
        return None

model = get_working_model()

# --- 2. LOGIK FUNKTION ---
def get_ai_response(topic, mode):
    if mode == "Info":
        prompt = f"Gib mir einen extrem faszinierenden wissenschaftlichen oder historischen Fakt über das Thema '{topic}'. Stil: Sachlich, kurz, fordernd."
    else:
        prompt = f"Gib mir eine schwierige logische Denkaufgabe oder eine Transferfrage zum Thema '{topic}', um jemanden aus einer Grübelschleife zu reißen. Der User muss aktiv nachdenken müssen."
    
    try:
        response = model.generate_content(prompt)
        return response.text
    except Exception as e:
        return f"Fehler bei der Generierung: {str(e)}"

# --- 3. UI & DESIGN ---
st.set_page_config(page_title="FocusSwitch Pro", page_icon="🛑")

st.markdown("""
    <style>
    .stButton>button {
        background-color: #CC0000; color: white; font-size: 30px;
        font-weight: bold; height: 150px; width: 100%;
        border-radius: 15px; border: 4px solid white;
        box-shadow: 0px 8px 15px rgba(0,0,0,0.3);
    }
    .main-box {
        background-color: #f8f9fa; padding: 20px; border-radius: 15px;
        border: 1px solid #dee2e6; margin-bottom: 20px;
    }
    </style>
    """, unsafe_allow_html=True)

# --- 4. APP ABLAUF ---
st.title("🛑 FocusSwitch Pro")

# Eingabebereich
with st.container():
    st.markdown("<div class='main-box'>", unsafe_allow_html=True)
    user_topic = st.text_input("Wunsch-Thema (leer lassen für Zufall):", placeholder="z.B. Zeitreisen, Biologie, Rom...")
    
    mode = st.radio(
        "Was brauchst du gerade?",
        ["Interessante Info", "Knifflige Denkaufgabe"],
        horizontal=True
    )
    st.markdown("</div>", unsafe_allow_html=True)

# Zufallsthemen falls Feld leer
RANDOM_TOPICS = ["Quantenphysik", "Stoische Philosophie", "Neurobiologie", "Astrophysik", "Spieltheorie", "Architektur"]

if st.button("FOKUS WECHSELN"):
    # Thema festlegen
    final_topic = user_topic if user_topic else random.choice(RANDOM_TOPICS)
    selected_mode = "Info" if mode == "Interessante Info" else "Task"
    
    with st.spinner(f'Generiere {mode} zu {final_topic}...'):
        content = get_ai_response(final_topic, selected_mode)
        st.session_state.active_content = content
        st.session_state.active_topic = final_topic
        st.session_state.show_result = True

# Ergebnisanzeige
if st.session_state.get('show_result'):
    st.divider()
    st.subheader(f"🧠 {st.session_state.active_topic}")
    st.info(st.session_state.active_content)
    
    if "Denkaufgabe" in mode:
        st.success("Tipp: Versuche die Lösung im Kopf zu formulieren, bevor du weitergehst.")

st.caption("Nutze dieses Tool als Notfall-Bremse für deine Gedanken.")
