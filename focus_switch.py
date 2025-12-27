import streamlit as st
import requests
import random

# --- 1. KI FUNKTION (Fakten & Details) ---
def get_mistral_content(topic, mode, context=None):
    api_key = st.secrets["mistral_key"]
    url = "https://api.mistral.ai/v1/chat/completions"
    
    if mode == "detail":
        prompt = f"Erkläre den wissenschaftlichen Hintergrund zu diesem Fakt über '{topic}' kurz und sachlich: '{context}'. Max. 3-4 Sätze."
    else: # Normaler Fakt-Modus
        prompt = f"Nenne einen kurzen, faszinierenden wissenschaftlichen oder historischen Fakt über '{topic}'. Nur der Fakt, max. 2 Sätze, keine Einleitung."

    headers = {"Authorization": f"Bearer {api_key}"}
    data = {
        "model": "mistral-small-latest",
        "messages": [{"role": "user", "content": prompt}],
        "temperature": 0.7
    }

    try:
        response = requests.post(url, json=data, headers=headers)
        return response.json()['choices'][0]['message']['content']
    except:
        return "Verbindung fehlgeschlagen."

# --- 2. ABSTRAKTE DENKAUFGABEN (Ohne KI für 100% Stabilität) ---
def get_abstract_task():
    tasks = [
        "Zähle in 7er-Schritten von 100 rückwärts (100, 93, ...).",
        "Nenne 5 Gegenstände in deiner Umgebung, die blau sind, und buchstabiere sie rückwärts.",
        "Berechne im Kopf: 14 mal 6 minus 12.",
        "Nenne die letzten 5 Bundeskanzler (oder US-Präsidenten) in umgekehrter Reihenfolge.",
        "Überlege dir 5 Wörter, die auf '...ung' enden und nichts mit deinem aktuellen Zustand zu tun haben.",
        "Stelle dir eine analoge Uhr vor: Wie groß ist der Winkel zwischen dem Stunden- und Minutenzeiger um 15:15 Uhr?",
        "Zähle die Buchstaben deines vollständigen Namens und multipliziere sie mit 13."
    ]
    return random.choice(tasks)

# --- 3. UI INITIALISIERUNG ---
st.set_page_config(page_title="FocusSwitch Pro", page_icon="🛑")

if 'fact' not in st.session_state:
    st.session_state.fact = ""
if 'current_topic' not in st.session_state:
    st.session_state.current_topic = ""
if 'extra_content' not in st.session_state:
    st.session_state.extra_content = ""
if 'extra_type' not in st.session_state:
    st.session_state.extra_type = ""

# --- 4. APP INTERFACE ---
st.title("🛑 FocusSwitch Pro")

user_topic = st.text_input("Interessengebiet:", placeholder="Zufall...")

if st.button("FOKUS-STOPP AUSLÖSEN", use_container_width=True):
    topic = user_topic if user_topic else random.choice(["Astrophysik", "Antike", "Biologie", "Tiefsee", "Architektur"])
    st.session_state.current_topic = topic
    st.session_state.fact = get_mistral_content(topic, "fact")
    st.session_state.extra_content = "" 
    st.session_state.extra_type = ""

if st.session_state.fact:
    st.divider()
    st.markdown(f"**🧠 Fokus-Thema: {st.session_state.current_topic}**")
    st.info(st.session_state.fact)

    if st.session_state.extra_content:
        if st.session_state.extra_type == "detail":
            st.success(f"**Hintergrund-Wissen:**\n\n{st.session_state.extra_content}")
        else:
            st.warning(f"**Abstrakte Denkaufgabe:**\n\n{st.session_state.extra_content}")

    st.write("---")
    col1, col2, col3 = st.columns(3)
    
    with col1:
        if st.button("🧬 DETAILS", use_container_width=True):
            st.session_state.extra_content = get_mistral_content(st.session_state.current_topic, "detail", context=st.session_state.fact)
            st.session_state.extra_type = "detail"
            st.rerun()

    with col2:
        if st.button("🧩 AUFGABE", use_container_width=True):
            # Hier laden wir jetzt die abstrakte Aufgabe statt KI-Inhalt
            st.session_state.extra_content = get_abstract_task()
            st.session_state.extra_type = "task"
            st.rerun()

    with col3:
        if st.button("⏭️ WEITER", use_container_width=True):
            st.session_state.fact = get_mistral_content(st.session_state.current_topic, "fact")
            st.session_state.extra_content = ""
            st.session_state.extra_type = ""
            st.rerun()
