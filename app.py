# app.py
import streamlit as st
import streamlit.components.v1 as components

# ─── CONFIG ────────────────────────────────────────────────────────────────────
RESPONSIVE_WEBHOOK = "https://<VOTRE_BASE_URL_N8N>/webhook/225784dc-80f4-4184-a0df-ae6eee1fb74c"
MAIN_WEBHOOK       = "https://<VOTRE_BASE_URL_N8N>/webhook/225784dc-80f4-4184-a0df-ae6eee1fb74c"

# ─── PAGE STREAMLIT ────────────────────────────────────────────────────────────
st.set_page_config(layout="centered", initial_sidebar_state="collapsed",
                   page_title="", page_icon="")

# Masquer tout chrome Streamlit
st.markdown("""
  <style>
    #MainMenu, header, footer { visibility: hidden; }
    html, body { margin:0; padding:0; height:100%; width:100%; overflow:hidden; }
    body > div { display:flex!important; justify-content:center; align-items:center;
                 height:100vh; width:100vw; background:#fff; }
    input {
      font-family:'Avenir Next',sans-serif;
      font-weight:200;
      font-size:2rem;
      width:80vw; max-width:400px;
      border:none; outline:none;
      background:transparent;
      text-align:center;
      caret-color:#007AFF;
    }
  </style>
  <link href="https://fonts.googleapis.com/css2?family=Avenir+Next:wght@200&display=swap" rel="stylesheet">
""", unsafe_allow_html=True)

# ─── HTML/JS MINIMALISTE ──────────────────────────────────────────────────────
components.html(f"""
<!DOCTYPE html>
<html><head><meta charset="utf-8"/></head><body>

  <input id="voidInput" type="text" autofocus />

  <script>
    const inp = document.getElementById('voidInput');
    let timer;

    // à chaque frappe, on recentre et on relance le timer
    function resetTimer() {{
      clearTimeout(timer);
      timer = setTimeout(() => send(inp.value), 5000);
    }}

    // écoute n’importe quelle touche pour focus
    document.addEventListener('keydown', (e) => {{
      if (document.activeElement !== inp) inp.focus();
      resetTimer();
    }});

    // Enter envoie direct
    inp.addEventListener('keyup', (e) => {{
      if (e.key === 'Enter') send(inp.value);
    }});

    function send(text) {{
      const t = text.trim();
      if (!t) return;
      fetch("{MAIN_WEBHOOK}", {{
        method: "POST",
        headers: {{ "Content-Type": "application/json" }},
        body: JSON.stringify({{ body: t }})
      }});
      inp.value = "";
    }}
  </script>

</body></html>
""", height=600)
