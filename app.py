import streamlit as st
import streamlit.components.v1 as components
import requests

st.set_page_config(
    layout="centered",
    initial_sidebar_state="collapsed",
    page_title="",
    page_icon="",
)

# Webhook URLs
WEBHOOK_PREFIL = "https://nbjhhh.app.n8n.cloud/webhook/225784dc-80f4-4184-a0df-ae6eee1fb74c"
WEBHOOK_SIMPLE = "https://nbjhhh.app.n8n.cloud/webhook/225784dc-80f4-4184-a0df-ae6eee1fb74c"

# Mode de pré-remplissage (toggle)
prefil_mode = st.button("📤 Préfil")

# Interface personnalisée
st.markdown(
    """
    <style>
    #MainMenu, header, footer { visibility: hidden; }
    html, body {
        margin: 0;
        padding: 0;
        height: 100%;
        background: white;
        font-family: 'Avenir Next', sans-serif;
    }
    input[type="text"] {
        font-family: 'Avenir Next', sans-serif;
        font-weight: 100;
        font-size: 2.5rem;
        border: none;
        outline: none;
        background: transparent;
        text-align: center;
        width: 100%;
        letter-spacing: .1rem;
    }
    input[type="text"]:focus {
        outline: none;
    }
    </style>
    <link href="https://fonts.googleapis.com/css2?family=Avenir+Next:wght@100&display=swap" rel="stylesheet">
    """,
    unsafe_allow_html=True,
)

# HTML input + JS webhook logic
html = f"""
<div style="display:flex;justify-content:center;align-items:center;height:70vh">
  <input id="inp" type="text" placeholder="..." autofocus />
</div>
<script>
  const inp = document.getElementById('inp');
  let timer = null;
  let previous = "";

  function send(value) {{
    const body = {{ body: value }};
    fetch("{WEBHOOK_SIMPLE}", {{
      method: "POST",
      headers: {{ "Content-Type": "application/json" }},
      body: JSON.stringify(body)
    }});
  }}

  function sendPrefil(value) {{
    const body = {{ data: [{{ companyName: value }}] }};
    fetch("{WEBHOOK_PREFIL}", {{
      method: "POST",
      headers: {{ "Content-Type": "application/json" }},
      body: JSON.stringify(body)
    }});
  }}

  inp.addEventListener("input", () => {{
    clearTimeout(timer);
    const val = inp.value;
    timer = setTimeout(() => {{
      if ({str(prefil_mode).lower()}) {{
        if (val.length >= 3 && val !== previous) {{
          sendPrefil(val);
          previous = val;
        }}
      }} else {{
        send(val);
      }}
    }}, 3500);
  }});
</script>
"""

components.html(html, height=600)
