import streamlit as st
import requests
import random

# --- 1. KI FUNKTION ---
def get_mistral_content(topic, mode, context=None):
    api_key = st.secrets["mistral_key"]
    url = "https://api.mistral.ai/v1/chat/completions"
    
    if mode == "detail":
        prompt = f"Erkläre den Hintergrund zu diesem Fakt über '{topic}' kurz und sachlich: '{context}'. Max. 3-4 Sätze."
    else:
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

# --- 2. ABSTRAKTE DENKAUFGABEN ---
def get_abstract_task():
    tasks = [
        "Zähle in 7er-Schritten von 100 rückwärts (100, 93, 86...).",
        "Berechne im Kopf: 18 mal 3 plus 16.",
        "Buchstabiere 'PHILOSOPHIE' rückwärts.",
        "Nenne 5 Hauptstädte in alphabetisch umgekehrter Reihenfolge.",
        "Wie viele Sekunden hat eine Stunde? Berechne es im Kopf.",
        "Nenne 4 chemische Elemente aus dem Periodensystem.",
        "Zähle alle Fenster in dem Raum, in dem du dich befindest, und multipliziere sie mit 7."
    ]
    return random.choice(tasks)

# --- 3. UI INITIALISIERUNG ---
st.set_page_config(page_title="FocusSwitch", page_icon="🛑")

if 'fact' not in st.session_state:
    st.session_state.fact = ""
if 'current_topic' not in st.session_state:
    st.session_state.current_topic = ""
if 'extra_content' not in st.session_state:
    st.session_state.extra_content = ""
if 'extra_type' not in st.session_state:
    st.session_state.extra_type = ""

# --- 4. APP INTERFACE ---
st.title("🛑 FocusSwitch")

user_topic = st.text_input("Interessengebiet:", placeholder="Zufall...")

if st.button("FOKUS-STOPP AUSLÖSEN", use_container_width=True):
    topic = user_topic if user_topic else random.choice(["Quantenphysik", "Antike", "Neurologie", "Weltraum", "Tiefsee"])
    st.session_state.current_topic = topic
    st.session_state.fact = get_mistral_content(topic, "fact")
    st.session_state.extra_content = "" 
    st.session_state.extra_type = ""

# Anzeige des Haupt-Fakts
if st.session_state.fact:
    st.divider()
    st.markdown(f"**🧠 Thema: {st.session_state.current_topic}**")
    st.info(st.session_state.fact)

    # 1. Erzähle mir mehr
    if not st.session_state.extra_content:
        if st.button("💬 Erzähle mir mehr", use_container_width=True):
            st.session_state.extra_content = get_mistral_content(st.session_state.current_topic, "detail", context
                                                                
