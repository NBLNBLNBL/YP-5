# app.py
import streamlit as st
import streamlit.components.v1 as components

# CONFIG
WEBHOOK = "https://<TON_INSTANCE_N8N>/webhook/225784dc-80f4-4184-a0df-ae6eee1fb74c"

# INIT PAGE
st.set_page_config(layout="centered", page_title="", initial_sidebar_state="collapsed")

# STYLES
st.markdown("""
<style>
  #MainMenu, header, footer { visibility: hidden; }
  html, body {
    margin: 0; padding: 0;
    height: 100%; width: 100%;
    background: white;
    overflow: hidden;
  }
  body > div {
    display: flex !important;
    justify-content: center;
    align-items: center;
    height: 100vh;
  }

  .fakeInput {
    font-family: 'Avenir Next', sans-serif;
    font-weight: 200;
    font-size: 2rem;
    text-align: center;
    outline: none;
    border: none;
    background: transparent;
    color: black;
    caret-color: #007AFF;
    width: 80vw;
    max-width: 500px;
  }
</style>
<link href="https://fonts.googleapis.com/css2?family=Avenir+Next:wght@200&display=swap" rel="stylesheet">
""", unsafe_allow_html=True)

# HTML + JS avec div éditable (sans input HTML)
components.html(f"""
<div contenteditable="true" class="fakeInput" id="editZone" spellcheck="false" autofocus></div>

<script>
  const zone = document.getElementById('editZone');
  let timer;

  // Clean et recentrage
  function sendText(txt) {{
    if (!txt.trim()) return;
    fetch("{WEBHOOK}", {{
      method: "POST",
      headers: {{ "Content-Type": "application/json" }},
      body: JSON.stringify({{ body: txt }})
    }});
    zone.innerText = "";
  }}

  // Envoi auto 5s
  zone.addEventListener('input', () => {{
    clearTimeout(timer);
    timer = setTimeout(() => {{
      sendText(zone.innerText);
    }}, 5000);
  }});

  // Envoi Enter
  zone.addEventListener('keydown', (e) => {{
    if (e.key === 'Enter') {{
      e.preventDefault();
      clearTimeout(timer);
      sendText(zone.innerText);
    }}
  }});

  // Focus dès interaction
  window.addEventListener('keydown', () => {{
    zone.focus();
  }});
</script>
""", height=600)
