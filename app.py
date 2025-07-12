# app.py
import streamlit as st
import streamlit.components.v1 as components
import requests

# ─── CONFIG ───────────────────────────────────────────────────────────────────
# Remplacez <VOTRE_BASE_URL_N8N> par l'URL racine de votre instance n8n
WEBHOOK_URL = "https://<VOTRE_BASE_URL_N8N>/webhook/225784dc-80f4-4184-a0df-ae6eee1fb74c"

# ─── PAGE STREAMLIT ────────────────────────────────────────────────────────────
st.set_page_config(layout="centered", initial_sidebar_state="collapsed", 
                   page_title="", page_icon="")

# Masque le header/menu/footer pour une toile blanche pure
st.markdown(
    """
    <style>
      #MainMenu, header, footer { visibility: hidden; }
      html, body { margin: 0; padding: 0; height: 100%; }
    </style>
    """,
    unsafe_allow_html=True,
)

# ─── COMPOSANT HTML/CSS/JS ─────────────────────────────────────────────────────
components.html(f"""
<!DOCTYPE html>
<html>
<head>
  <meta charset="utf-8"/>
  <link href="https://fonts.googleapis.com/css2?family=Avenir+Next:wght@200&display=swap" rel="stylesheet">
  <style>
    body {{
      margin: 0; padding: 0;
      height: 100vh;
      display: flex;
      justify-content: center;
      align-items: center;
      background: #fff;
    }}
    input {{
      font-family: 'Avenir Next', sans-serif;
      font-weight: 200;
      font-size: 2rem;
      border: none;
      outline: none;
      background: transparent;
      text-align: center;
      letter-spacing: 1rem;
    }}
  </style>
</head>
<body>
  <input id="minimalInput" type="text" placeholder=". . ." autofocus />
  <script>
    const inp = document.getElementById('minimalInput');
    let tm;
    function send() {{
      const txt = inp.value.trim();
      if (!txt) return;
      fetch("{WEBHOOK_URL}", {{
        method: "POST",
        headers: {{ "Content-Type": "application/json" }},
        body: JSON.stringify({{ body: txt }})
      }});
      inp.value = "";
    }}
    inp.addEventListener('keyup', e => {{
      clearTimeout(tm);
      if (e.key === 'Enter') {{
        send();
      }} else {{
        tm = setTimeout(send, 3000);
      }}
    }});
  </script>
</body>
</html>
""", height=600)
