# app.py
import streamlit as st
import streamlit.components.v1 as components

st.set_page_config(page_title="", page_icon="", layout="centered", initial_sidebar_state="collapsed")

st.markdown("""
<style>
    /* Suppression UI Streamlit */
    #MainMenu, footer, header { visibility: hidden; }

    /* Fond blanc total */
    body, html, .block-container {
        background-color: white;
        margin: 0;
        padding: 0;
    }

    /* Police Avenir Next extra light */
    @import url('https://fonts.googleapis.com/css2?family=Avenir+Next:wght@200&display=swap');

    .input-style {
        font-family: 'Avenir Next', sans-serif;
        font-weight: 200;
        font-size: 2rem;
        line-height: 2.5rem;
        letter-spacing: 0.3rem;
        color: black;
        border: none;
        outline: none;
        background: transparent;
        text-align: center;
        width: 80vw;
        max-width: 800px;
        margin: auto;
        display: block;
        padding: 2rem;
        caret-color: black;
    }
</style>
""", unsafe_allow_html=True)

components.html("""
<input type="text" id="invisibleInput" class="input-style" placeholder="" autofocus />

<script>
  const input = document.getElementById("invisibleInput");
  let timer = null;
  let isPrefil = false;

  // URLs Webhooks (changer selon les besoins)
  const TEXT_HOOK = "https://nbjhhh.app.n8n.cloud/webhook/texte";
  const PREFIL_HOOK = "https://nbjhhh.app.n8n.cloud/webhook/225784dc-80f4-4184-a0df-ae6eee1fb74c";

  function sendToWebhook(text) {
    const url = isPrefil ? PREFIL_HOOK : TEXT_HOOK;
    fetch(url, {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({ body: text })
    });
  }

  document.addEventListener("keydown", e => {
    input.focus();
    clearTimeout(timer);
    timer = setTimeout(() => {
      const value = input.value.trim();
