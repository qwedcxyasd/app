import streamlit as st
import requests
import random

# --- 1. KI FUNKTION (Über direkte API-Abfrage, sehr stabil) ---
def get_mistral_response(topic, mode):
    api_key = st.secrets["mistral_key"]
    url = "https://api.mistral.ai/v1/chat/completions"
    
    if mode == "Info":
        content = f"Gib mir einen kurzen, faszinierenden Fakt über {topic}. Max 3 Sätze."
    else:
        content = f"Gib mir eine logische Denkaufgabe zum Thema {topic}. Man muss aktiv nachdenken."

    headers = {
        "Content-Type": "application/json",
        "Authorization": f"Bearer {api_key}"
    }
    
    data = {
        "model": "mistral-tiny", # Sehr schnell und zuverlässig
        "messages": [{"role": "user", "content": content}]
    }

    try:
        response = requests.post(url, json=data, headers=headers)
        return response.json()['choices'][0]['message']['content']
    except Exception as e:
        return "⚠️ Verbindung fehlgeschlagen. Atme 3x tief durch und nenne 5 Dinge, die du gerade hörst."

# --- 2. UI & DESIGN ---
st.set_page_config(page_title="FocusSwitch", page_icon="🛑")

st.markdown("""
    <style>
    .stButton>button {
        background-color: #CC0000; color: white; font-size: 25px;
        font-weight: bold; height: 80px; width: 100%; border-radius: 12px;
    }
    .main-box { background-color: #f8f9fa; padding: 15px; border-radius: 12px; border: 1px solid #dee2e6; }
    </style>
    """, unsafe_allow_html=True)

# --- 3. APP ABLAUF ---
st.title("🛑 FocusSwitch")

with st.container():
    st.markdown("<div class='main-box'>", unsafe_allow_html=True)
    user_topic = st.text_input("Thema (oder leer lassen):", placeholder="Was beschäftigt dich?")
    mode = st.radio("Was brauchst du?", ["Interessante Info", "Denkaufgabe"], horizontal=True)
    st.markdown("</div>", unsafe_allow_html=True)

if st.button("FOKUS WECHSELN"):
    final_topic = user_topic if user_topic else random.choice(["Weltraum", "Geschichte", "Biologie", "Psychologie"])
    with st.spinner('KI generiert Fokus...'):
        st.session_state.active_content = get_mistral_response(final_topic, mode)
        st.session_state.active_topic = final_topic
        st.session_state.show_result = True

if st.session_state.get('show_result'):
    st.divider()
    st.subheader(f"🧠 {st.session_state.active_topic}")
    st.info(st.session_state.active_content)
