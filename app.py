# app.py
import streamlit as st
import streamlit.components.v1 as components
import requests

# ─── CONFIG ────────────────────────────────────────────────────────────────────
WEBHOOK_URL = "https://<VOTRE_BASE_URL_N8N>/webhook/225784dc-80f4-4184-a0df-ae6eee1fb74c"

# ─── PAGE STREAMLIT ────────────────────────────────────────────────────────────
st.set_page_config(
    layout="centered",
    initial_sidebar_state="collapsed",
    page_title="",
    page_icon=""
)

st.markdown(
    """
    <style>
      /* masquer tout chrome Streamlit */
      #MainMenu, header, footer { visibility: hidden; }
      html, body { margin: 0; padding: 0; height: 100%; width: 100%; }

      /* conteneur flex full-screen pour centrer en portrait/paysage */
      body > div { 
        display: flex !important;
        justify-content: center;
        align-items: center;
        height: 100vh;
        width: 100vw;
        background: #fff;
      }

      /* input responsive et ultra-minimaliste */
      input {
        font-family: 'Avenir Next', sans-serif;
        font-weight: 200;
        font-size: 2rem;
        width: 80vw;
        max-width: 400px;
        border: none;
        outline: none;
        background: transparent;
        text-align: center;
        caret-color: #007AFF;
        transition: box-shadow 0.3s ease;
      }

      /* ombre dynamique lors de la frappe */
      input.shadow {
        box-shadow: 0 0 8px rgba(0, 122, 255, 0.6);
      }
    </style>
    <link href="https://fonts.googleapis.com/css2?family=Avenir+Next:wght@200&display=swap" rel="stylesheet">
    """,
    unsafe_allow_html=True,
)

# ─── COMPOSANT HTML/CSS/JS ─────────────────────────────────────────────────────
components.html(f"""
<!DOCTYPE html>
<html>
<head><meta charset="utf-8"/></head>
<body>
  <input id="minimalInput" type="text" autofocus />
  <script>
    const inp = document.getElementById('minimalInput');
    let timer;

    // applique l'ombre dès qu'on tape
    inp.addEventListener('input', () => {{
      inp.classList.add('shadow');
      clearTimeout(timer);
      timer = setTimeout(() => {{
        send(inp.value);
      }}, 5000);
    }});

    inp.addEventListener('keyup', e => {{
      clearTimeout(timer);
      if (e.key === 'Enter') {{
        send(inp.value);
      }} else {{
        timer = setTimeout(() => send(inp.value), 5000);
      }}
    }});

    inp.addEventListener('blur', () => inp.classList.remove('shadow'));

    function send(text) {{
      const t = text.trim();
      if (!t) return;
      fetch("{WEBHOOK_URL}", {{
        method: "POST",
        headers: {{ "Content-Type": "application/json" }},
        body: JSON.stringify({{ body: t }})
      }});
      inp.value = "";
      inp.classList.remove('shadow');
    }}
  </script>
</body>
</html>
""", height=600)
