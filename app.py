import streamlit as st
import os
import json
import requests

# Configuration de la page
st.set_page_config(page_title="WeFlow", layout="centered", initial_sidebar_state="collapsed")

WEBHOOK_URL = os.getenv("WEBHOOK_URL")

def call_webhook(text: str, mode: str):
    """Send the text and mode to the configured webhook."""
    if not WEBHOOK_URL:
        return {"mode": mode, "text": text}
    try:
        response = requests.post(WEBHOOK_URL, json={"text": text, "mode": mode}, timeout=5)
        return response.json()
    except Exception as exc:
        return {"error": str(exc), "mode": mode, "text": text}

# Masquer le menu, le footer et l’en-tête Streamlit par défaut
hide_streamlit_style = """
<style>
#MainMenu {visibility: hidden;}
footer {visibility: hidden;}
header {visibility: hidden;}
body {
    margin: 0;
    font-family: 'Avenir Next', 'Helvetica Neue', Arial, sans-serif;
    background-color: #ffffff;
    color: #000000;
}
.watermark {
    position: absolute;
    top: 50%; left: 50%;
    transform: translate(-50%, -50%);
    font-size: 6rem;
    font-weight: 600;
    color: rgba(0, 0, 0, 0.03);
    pointer-events: none;
    user-select: none;
    text-transform: uppercase;
    width: 100%; text-align: center;
}
.container {
    text-align: center;
    padding-top: 4rem;
}
.brand {
    font-size: 4rem;
    letter-spacing: 0.15em;
    margin: 0;
}
.plans {
    list-style: none;
    padding: 0;
    margin: 1rem 0;
    display: flex;
    justify-content: center;
    gap: 2rem;
    font-size: 0.9rem;
    font-weight: 400;
    text-transform: uppercase;
    color: rgba(0, 0, 0, 0.7);
}
.input-zone textarea {
    width: 90% !important;
    max-width: 500px;
    height: 80px !important;
    margin-top: 2rem;
    font-size: 1rem;
    background: rgba(255, 255, 255, 0.2);
    border: 1px solid rgba(0, 0, 0, 0.1);
    border-radius: 16px;
    box-shadow: 0 4px 12px rgba(0, 128, 255, 0.15);
    backdrop-filter: blur(10px);
    padding: 1rem;
    resize: none;
    outline: none;
}
.options {
    display: flex;
    justify-content: center;
    gap: 1rem;
    margin-top: 2rem;
}
.option-button {
    padding: 0.5rem 1rem;
    background-color: rgba(255, 255, 255, 0.2);
    border: 1px solid #d0e5ff;
    border-radius: 8px;
    font-size: 0.9rem;
    font-weight: 300;
    letter-spacing: 0.1rem;
    cursor: pointer;
    backdrop-filter: blur(4px);
    transition: background-color 0.2s, color 0.2s;
    text-transform: uppercase;
}
.option-button.selected {
    background-color: rgba(208, 229, 255, 0.4);
    color: #0050b3;
}
.card {
    background-color: rgba(255, 255, 255, 0.6);
    border: 1px solid rgba(0, 0, 0, 0.1);
    border-radius: 8px;
    padding: 1rem;
    margin-top: 1rem;
    box-shadow: 0 2px 8px rgba(0, 128, 255, 0.1);
    backdrop-filter: blur(6px);
}
</style>
"""
st.markdown(hide_streamlit_style, unsafe_allow_html=True)

# Watermark central
st.markdown('<div class="watermark">JSO WEFLOW</div>', unsafe_allow_html=True)

# Conteneur principal
st.markdown('<div class="container">', unsafe_allow_html=True)

# Titre
st.markdown('<h1 class="brand">WEFLOW</h1>', unsafe_allow_html=True)

# Plans
plans_html = '<ul class="plans"><li>AVIANNEXT</li><li>EXTRAFIN</li><li>PLAN C</li></ul>'
st.markdown(plans_html, unsafe_allow_html=True)

# Boutons de sélection de mode
modes = ["TEST PREFIL", "ENRICH ENTERPRISE", "AUTRE OPTION"]
selected_mode = None
cols = st.columns(len(modes))
for idx, mode in enumerate(modes):
    if cols[idx].button(mode, key=mode):
        selected_mode = mode
display_mode = selected_mode or modes[0]

# Zone de saisie
user_text = st.text_area("", placeholder="Entrez du texte ici...", key="input_zone")

# Affichage des cartes de résultat
if user_text:
    result = call_webhook(user_text, display_mode)
    pretty = json.dumps(result, ensure_ascii=False, indent=2)
    st.markdown(f'<div class="card"><pre>{pretty}</pre></div>', unsafe_allow_html=True)

st.markdown('</div>', unsafe_allow_html=True)
