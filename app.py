# app.py
import streamlit as st
import streamlit.components.v1 as components

# —— CONFIG WEBHOOKS ——
WEBHOOK_TEXT = "https://nbjhhh.app.n8n.cloud/webhook/225784dc-80f4-4184-a0df-ae6eee1fb74c"
WEBHOOK_PREFIL = "https://nbjhhh.app.n8n.cloud/webhook/225784dc-80f4-4184-a0df-ae6eee1fb74c"

# —— PAGE STREAMLIT ——
st.set_page_config(layout="centered", initial_sidebar_state="collapsed", page_title="", page_icon="")

# Inject Avenir Next font from Google Fonts
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Avenir+Next:wght@200&display=swap');

html, body, [class*="css"]  {
    font-family: 'Avenir Next', sans-serif;
    background-color: white;
}
input:focus {{ outline: none !important; }}
</style>
""", unsafe_allow_html=True)

# —— ZONE DE SAISIE HTML/CSS/JS ——
html = f'''
<div style="display: flex; justify-content: center; align-items: center; height: 70vh;">
  <input id="inp" type="text" placeholder="..."
         style="
           font-family: 'Avenir Next', sans-serif;
           font-weight: 200;
           font-size: 2.5rem;
           border: none;
           background: transparent;
           text-align: center;
           letter-spacing: 0.3rem;
           width: 60%;
         " autofocus>
</div>
<script>
  const inp = document.getElementById('inp');
  let timer = null;
  let prefilMode = false;
  let previousLength = 0;

  function send(text, url) {{
    fetch(url, {{
      method: 'POST',
      headers: {{ 'Content-Type': 'application/json' }},
      body: JSON.stringify({{ body: text }})
    }});
  }}

  function checkInput() {{
    const value = inp.value;
    if (prefilMode && value.length % 3 === 0 && value.length !== previousLength) {{
      previousLength = value.length;
      send(value, '{WEBHOOK_PREFIL}');
    }}
  }}

  inp.addEventListener('input', () => {{
    checkInput();
    clearTimeout(timer);
    timer = setTimeout(() => send(inp.value, '{WEBHOOK_TEXT}'), 3500);
  }});

  document.addEventListener("keydown", () => {{ inp.focus(); }});

  window.activatePrefil = function() {{
    prefilMode = true;
    previousLength = 0;
  }}
  window.deactivatePrefil = function() {{
    prefilMode = false;
  }}
</script>
'''
components.html(html, height=500)

# —— SWITCH MODE PRÉFIL ——
col1, col2 = st.columns([1, 1])
with col1:
    if st.button("Activer Préfil"):
        components.html("<script>window.activatePrefil();</script>", height=0)
with col2:
    if st.button("Désactiver Préfil"):
        components.html("<script>window.deactivatePrefil();</script>", height=0)
