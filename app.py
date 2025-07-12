# app.py
import streamlit as st
import streamlit.components.v1 as components

# ───────────────────────────────────
# 1 CONFIG
# ───────────────────────────────────
BASE_N8N_URL = "https://<TON_INSTANCE_N8N>"          # ← remplace !
WEBHOOK_PATH = "webhook/225784dc-80f4-4184-a0df-ae6eee1fb74c"
MAIN_WEBHOOK = f"{BASE_N8N_URL}/{WEBHOOK_PATH}"

# ───────────────────────────────────
# 2 PAGE STREAMLIT
# ───────────────────────────────────
st.set_page_config(
    layout="centered",
    initial_sidebar_state="collapsed",
    page_title="",
    page_icon=""
)

# ───────────────────────────────────
# 3 CSS 100 % MINIMAL
# ───────────────────────────────────
st.markdown(
    """
    <style>
      #MainMenu, header, footer { visibility: hidden; }
      html, body { margin:0; padding:0; height:100%; width:100%; overflow:hidden; }
      body>div { display:flex !important; justify-content:center; align-items:center;
                 height:100vh; width:100vw; background:#fff; }

      /* Champ SANS bordure / ombre, même en focus */
      #voidInput, #voidInput:focus {
        -webkit-appearance:none; appearance:none;
        border:none !important; outline:none !important; box-shadow:none !important;
        background:transparent !important;

        font-family:'Avenir Next',sans-serif;
        font-weight:200;
        font-size:2rem;
        width:80vw; max-width:400px;
        text-align:center;
        caret-color:#007AFF;
        color:#000;
      }
    </style>
    <link href="https://fonts.googleapis.com/css2?family=Avenir+Next:wght@200&display=swap" rel="stylesheet">
    """,
    unsafe_allow_html=True
)

# ───────────────────────────────────
# 4 HTML + JS
# ───────────────────────────────────
html_code = (
    "<!DOCTYPE html><html><head><meta charset='utf-8'></head><body>"
    "  <input id='voidInput' type='text' autocomplete='off' autocorrect='off' spellcheck='false' autofocus>"
    "  <script>"
    "    const inp = document.getElementById('voidInput');"
    "    let timer;"
    "    document.addEventListener('keydown', () => { inp.focus(); clearTimeout(timer); timer = setTimeout(send, 5000); });"
    "    inp.addEventListener('keyup', e => { if (e.key === 'Enter') { clearTimeout(timer); send(); } });"
    "    function send() {"
    "      const txt = inp.value.trim();"
    "      if (!txt) return;"
    f"      fetch('{MAIN_WEBHOOK}', {{"
    "        method:'POST',"
    "        headers:{'Content-Type':'application/json'},"
    "        body: JSON.stringify({ body: txt })"
    "      }});"
    "      inp.value='';"
    "    }"
    "  </script>"
    "</body></html>"
)

components.html(html_code, height=600)
