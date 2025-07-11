import streamlit as st

# Configuration de la page
st.set_page_config(page_title="WeFlow", layout="centered", initial_sidebar_state="collapsed")

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
    color: rgba(0, 0, 0, 0.05);
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
    letter-spacing: 0.1rem;
    margin: 0;
}
.plans {
    list-style: none;
    padding: 0;
    margin: 1rem 0;
    display: flex;
    justify-content: center;
    gap: 1.5rem;
    font-size: 0.9rem;
    color: rgba(0, 0, 0, 0.7);
}
.input-zone textarea {
    width: 90% !important;
    max-width: 500px;
    height: 80px !important;
    margin-top: 2rem;
    font-size: 1rem;
    border: none;
    border-radius: 8px;
    box-shadow: 0 2px 10px rgba(0, 128, 255, 0.15);
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
    background-color: transparent;
    border: 1px solid rgba(0, 0, 0, 0.2);
    border-radius: 4px;
    font-size: 0.8rem;
    letter-spacing: 0.1rem;
    cursor: pointer;
    transition: background-color 0.2s, color 0.2s;
    text-transform: uppercase;
}
.option-button.selected {
    background-color: rgba(0, 128, 255, 0.1);
    color: #0050b3;
}
.card {
    background-color: rgba(0, 128, 255, 0.05);
    border-radius: 8px;
    padding: 1rem;
    margin-top: 1rem;
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
    st.markdown(f'<div class="card">Mode : {display_mode}</div>', unsafe_allow_html=True)
    st.markdown(f'<div class="card">Texte reçu : {user_text}</div>', unsafe_allow_html=True)

st.markdown('</div>', unsafe_allow_html=True)
