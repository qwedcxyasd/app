import streamlit as st
import requests
import random

# --- 1. KI FUNKTION (Mit Kontext-Übergabe) ---
def get_mistral_fact(topic, existing_fact=None):
    api_key = st.secrets["mistral_key"]
    url = "https://api.mistral.ai/v1/chat/completions"
    
    if existing_fact:
        # Hier zwingen wir die KI, sich auf den spezifischen Fakt zu beziehen
        prompt = f"Du hast gerade diesen Fakt genannt: '{existing_fact}'. Erkläre den wissenschaftlichen Hintergrund dazu genauer (max. 4 Sätze). Bleib sachlich."
    else:
        prompt = f"Nenne einen kurzen, faszinierenden wissenschaftlichen oder historischen Fakt über '{topic}'. Nur der Fakt, max. 2 Sätze, keine Einleitung."

    headers = {"Authorization": f"Bearer {api_key}"}
    data = {
        "model": "mistral-small-latest",
        "messages": [{"role": "user", "content": prompt}]
    }

    try:
        response = requests.post(url, json=data, headers=headers)
        return response.json()['choices'][0]['message']['content']
    except:
        return "Verbindung fehlgeschlagen."

# --- 2. UI INITIALISIERUNG ---
st.set_page_config(page_title="FocusSwitch", page_icon="🛑")

if 'fact' not in st.session_state:
    st.session_state.fact = ""
if 'current_topic' not in st.session_state:
    st.session_state.current_topic = ""
if 'detail_text' not in st.session_state:
    st.session_state.detail_text = ""

# --- 3. APP INTERFACE ---
st.title("🛑 FocusSwitch")

user_topic = st.text_input("Thema:", placeholder="z.B. Astrophysik, Rom, Tiefsee...")

if st.button("FOKUS-FAKT GENERIEREN", use_container_width=True):
    topic = user_topic if user_topic else random.choice(["Quantenphysik", "Antike", "Biologie", "Neurologie"])
    st.session_state.current_topic = topic
    st.session_state.fact = get_mistral_fact(topic)
    st.session_state.detail_text = "" # Reset Details bei neuem Fakt

if st.session_state.fact:
    st.divider()
    st.markdown(f"**Thema: {st.session_state.current_topic}**")
    st.info(st.session_state.fact)

    if st.session_state.detail_text:
        st.success(f"**Hintergrund:**\n\n{st.session_state.detail_text}")

    col1, col2 = st.columns(2)
    
    with col1:
        # Hier übergeben wir den aktuellen Fakt an die Funktion
        if st.button("🧬 MEHR DETAILS", use_container_width=True):
            st.session_state.detail_text = get_mistral_fact(st.session_state.current_topic, existing_fact=st.session_state.fact)
            st.rerun()

    with col2:
        if st.button("⏭️ NÄCHSTER FAKT", use_container_width=True):
            st.session_state.fact = get_mistral_fact(st.session_state.current_topic)
            st.session_state.detail_text = ""
            st.rerun()
