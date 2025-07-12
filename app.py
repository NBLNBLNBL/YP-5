# app.py
import streamlit as st
import streamlit.components.v1 as components

# ─── CONFIG ────────────────────────────────────────────────────────────────────
BASE_N8N_URL = "https://<TON_INSTANCE_N8N>"
WEBHOOK_SIMPLE = f"{BASE_N8N_URL}/webhook/225784dc-80f4-4184-a0df-ae6eee1fb74c"
WEBHOOK_PREFIL = f"{BASE_N8N_URL}/webhook/225784dc-80f4-4184-a0df-ae6eee1fb74c"  # identique ici mais pourrait différer

# ─── PAGE STREAMLIT ────────────────────────────────────────────────────────────
st.set_page_config(layout="centered", page_title="", initial_sidebar_state="collapsed")

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
    width: 100vw;
  }
  #editZone {
    font-family: 'Avenir Next', sans-serif;
    font-weight: 200;
    font-size: 2rem;
    line-height: 1.5;
    text-align: center;
    outline: none;
    border: none;
    background: transparent;
    color: black;
    width: 80vw;
    max-width: 600px;
    padding: 0;
    margin: 0;
    caret-color: #007AFF;
  }
  #editZone:focus {
    outline: none !important;
    border: none !important;
  }
</style>
<link href="https://fonts.googleapis.com/css2?family=Avenir+Next:wght@200&display=swap" rel="stylesheet">
""", unsafe_allow_html=True)

# ─── HTML + JS ─────────────────────────────────────────────────────────────────
components.html(f"""
<div contenteditable="true" id="editZone" spellcheck="false"></div>

<script>
  const zone = document.getElementById('editZone');
  let timer;
  let lastSent = '';
  let charCounter = 0;

  function sendTextToWebhook(url, payload) {{
    fetch(url, {{
      method: "POST",
      headers: {{ "Content-Type": "application/json" }},
      body: JSON.stringify(payload)
    }});
  }}

  // Envoi après 3.5s d'inactivité (webhook simple)
  zone.addEventListener('input', () => {{
    clearTimeout(timer);
    timer = setTimeout(() => {{
      sendTextToWebhook("{WEBHOOK_SIMPLE}", {{ body: zone.innerText.trim() }});
    }}, 3500);
  }});

  // Envoi Enter immédiat (webhook simple)
  zone.addEventListener('keydown', (e) => {{
    if (e.key === 'Enter') {{
      e.preventDefault();
      clearTimeout(timer);
      sendTextToWebhook("{WEBHOOK_SIMPLE}", {{ body: zone.innerText.trim() }});
      zone.innerText = "";
      charCounter = 0;
      lastSent = '';
    }}
  }});

  // Préfil — envoie tous les 3 caractères (webhook préfilé)
  zone.addEventListener('keyup', () => {{
    const current = zone.innerText.trim();
    const delta = current.length - lastSent.length;
    if (delta >= 3) {{
      sendTextToWebhook("{WEBHOOK_PREFIL}", {{ body: current }});
      lastSent = current;
    }}
  }});

  // Focus auto
  window.addEventListener('keydown', () => {{ zone.focus(); }});
</script>
""", height=600)
