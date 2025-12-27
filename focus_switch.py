import streamlit as st
import requests
import random

# --- 1. KI FUNKTION (Fokus auf Fakten) ---
def get_mistral_fact(topic, detail_mode=False):
    api_key = st.secrets["mistral_key"]
    url = "https://api.mistral.ai/v1/chat/completions"
    
    if detail_mode:
        prompt = f"Erkläre den Hintergrund zu diesem Fakt über '{topic}' etwas genauer, aber bleib sachlich und kompakt (max. 4-5 Sätze)."
    else:
        prompt = f"Nenne mir einen kurzen, extrem faszinierenden und wenig bekannten wissenschaftlichen oder historischen Fakt über '{topic}'. Nur der Fakt, max. 2 Sätze, keine Einleitung."

    headers = {"Authorization": f"Bearer {api_key}"}
    data = {
        "model": "mistral-small-latest",
        "messages": [{"role": "user", "content": prompt}]
    }

    try:
        response = requests.post(url, json=data, headers=headers)
        return response.json()['choices'][0]['message']['content']
    except:
        return "Verbindung fehlgeschlagen. Versuche es gleich noch einmal."

# --- 2. UI INITIALISIERUNG ---
st.set_page_config(page_title="FocusSwitch", page_icon="🛑")

if 'fact' not in st.session_state:
    st.session_state.fact = ""
if 'current_topic' not in st.session_state:
    st.session_state.current_topic = ""

# --- 3. APP INTERFACE ---
st.title("🛑 FocusSwitch")

user_topic = st.text_input("Thema eingeben (oder leer lassen):", placeholder="z.B. Astrophysik, Rom, Tiefsee...")

col_start, col_reset = st.columns(2)

with col_start:
    if st.button("FOKUS-FAKT GENERIEREN", use_container_width=True):
        topic = user_topic if user_topic else random.choice(["Quantenphysik", "Antike", "Biologie", "Neurologie"])
        st.session_state.current_topic = topic
        st.session_state.fact = get_mistral_fact(topic)

# Anzeige des Fakts
if st.session_state.fact:
    st.divider()
    st.markdown(f"**Thema: {st.session_state.current_topic}**")
    st.info(st.session_state.fact)

    # Die zwei gewünschten Buttons
    col1, col2 = st.columns(2)
    
    with col1:
        if st.button("🧬 MEHR DETAILS", use_container_width=True):
            detail = get_mistral_fact(st.session_state.current_topic, detail_mode=True)
            st.session_state.fact = f"{st.session_state.fact}\n\n---\n\n**Details:** {detail}"
            st.rerun()

    with col2:
        if st.button("⏭️ NÄCHSTER FAKT", use_container_width=True):
            st.session_state.fact = get_mistral_fact(st.session_state.current_topic)
            st.rerun()

st.write("---")
st.caption("Drücke 'Nächster Fakt', wenn dich das aktuelle Thema nicht genug ablenkt.")
