# app.py
import streamlit as st
import streamlit.components.v1 as components

# ─── CONFIGURATION ─────────────────────────────────────────────────────────────
# Remplacez <BASE_URL_N8N> par l'URL de votre instance n8n (sans slash final)
BASE_N8N_URL = "https://<BASE_URL_N8N>"
WEBHOOK_PATH = "webhook/225784dc-80f4-4184-a0df-ae6eee1fb74c"
MAIN_WEBHOOK = f"{BASE_N8N_URL}/{WEBHOOK_PATH}"

# ─── INITIALISATION STREAMLIT ──────────────────────────────────────────────────
st.set_page_config(
    layout="centered",
    initial_sidebar_state="collapsed",
    page_title="",
    page_icon=""
)

# ─── CSS ULTRA MINIMALISTE ─────────────────────────────────────────────────────
st.markdown(
    """
    <style>
      /* Cacher tout chrome Streamlit */
      #MainMenu, header, footer { visibility: hidden; }
      html, body { margin:0; padding:0; height:100%; width:100%; overflow:hidden; }
      /* Conteneur full-screen centré */
      body > div {
        display: flex !important;
        justify-content: center;
        align-items: center;
        height: 100vh;
        width: 100vw;
        background: #fff;
      }
      /* Input « vide » sans cadre ni style par défaut */
      #voidInput {
        -webkit-appearance: none;
        appearance: none;
        font-family: 'Avenir Next', sans-serif;
        font-weight: 200;
        font-size: 2rem;
        width: 80vw;
        max-width: 400px;
        border: none !important;
        outline: none !important;
        background: transparent !important;
        text-align: center;
        caret-color: #007AFF;
        color: #000;
      }
    </style>
    <link href="https://fonts.googleapis.com/css2?family=Avenir+Next:wght@200&display=swap" rel="stylesheet">
    """,
    unsafe_allow_html=True
)

# ─── COMPOSANT HTML/JS ULTRA MINIMALISTE ───────────────────────────────────────
components.html(
    f"""
<!DOCTYPE html>
<html>
<head><meta charset=\"utf-8\"/></head>
<body>
  <input id=\"voidInput\" type=\"text\" autofocus />
  <script>
    const inp = document.getElementById('voidInput');
    let timer;
    // Focus auto et recentrage à chaque frappe
    document.addEventListener('keydown', () => {
      if (document.activeElement !== inp) inp.focus();
      clearTimeout(timer);
      timer = setTimeout(send, 5000);
    });
    // Envoi sur Enter
    inp.addEventListener('keyup', (e) => {
      if (e.key === 'Enter') {
        clearTimeout(timer);
        send();
      }
    });
    // Envoi de la valeur
    function send() {
      const text = inp.value.trim();
      if (!text) return;
      fetch("{MAIN_WEBHOOK}", {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ body: text })
      });
      inp.value = '';
    }
  </script>
</body>
</html>
""", 
    height=600
)
