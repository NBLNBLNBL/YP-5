# app.py
import streamlit as st
import streamlit.components.v1 as components

# ─── CONFIG ────────────────────────────────────────────────────────────────────
WEBHOOK_BASE = "https://nbjhhh.app.n8n.cloud/webhook/225784dc-80f4-4184-a0df-ae6eee1fb74c"

# ─── STREAMLIT UI SETUP ────────────────────────────────────────────────────────
st.set_page_config(page_title="", layout="wide", initial_sidebar_state="collapsed")
st.markdown("""
<style>
/* GLOBAL RESET */
html, body, [class*="css"]  {
  margin: 0;
  padding: 0;
  background: white;
  font-family: 'Avenir Next', sans-serif;
  font-weight: 200;
  font-size: 2.4rem;
  letter-spacing: 0.2rem;
  text-align: center;
}

/* INPUT STYLING */
input:focus, input:active, input {
  outline: none !important;
  box-shadow: none !important;
  border: none !important;
  background: transparent !important;
  color: black;
}

/* Remove placeholder underline on focus */
input::placeholder {
  color: #ccc;
}

/* BUTTON STYLING */
button {
  all: unset;
  font-family: 'Avenir Next', sans-serif;
  font-weight: 200;
  text-transform: uppercase;
  font-size: 1.2rem;
  letter-spacing: 0.2rem;
  margin: 0.4rem 0;
  padding: 0.6rem 1.2rem;
  border: 1px solid black;
  cursor: pointer;
}

.button-wrapper {
  position: fixed;
  bottom: 2rem;
  left: 50%;
  transform: translateX(-50%);
  display: flex;
  flex-direction: column;
  gap: 1rem;
  align-items: center;
}
</style>
<link href="https://fonts.googleapis.com/css2?family=Avenir+Next:wght@200&display=swap" rel="stylesheet">
""", unsafe_allow_html=True)

# ─── MODE PRÉFILL ─────────────────────────────────────────────────────────────
states = st.session_state
if "prefill" not in states:
    states.prefill = False

# Boutons en HTML custom
components.html("""
<div class="button-wrapper">
  <button onclick="fetch('?prefill=1')">ACTIVER PRÉFILL</button>
  <button onclick="fetch('?prefill=0')">DÉSACTIVER PRÉFILL</button>
</div>
""", height=100)

query_params = st.experimental_get_query_params()
if "prefill" in query_params:
    states.prefill = query_params["prefill"][0] == "1"

webhook_url = WEBHOOK_BASE
mode = "Pré-remplissage activé" if states.prefill else "Mode simple"

# ─── INPUT HTML / JS ──────────────────────────────────────────────────────────
components.html(f"""
<div style="height:50vh;display:flex;justify-content:center;align-items:center">
  <input id='inp' type='text' placeholder='. . .' autofocus>
</div>
<script>
const inp = document.getElementById('inp');
inp.focus();

let timer = null;
let lastSent = "";

function sendPayload(t) {{
  fetch("{webhook_url}", {{
    method: "POST",
    headers: {{"Content-Type": "application/json"}},
    body: JSON.stringify({{ body: t }})
  }});
}}

inp.addEventListener('input', () => {{
  clearTimeout(timer);
  const val = inp.value.trim();

  if ({str(states.prefill).lower()} && val.length >= 3 && val.length % 3 === 0 && val !== lastSent) {{
    lastSent = val;
    sendPayload(val);
  }} else if (!{str(states.prefill).lower()}) {{
    timer = setTimeout(() => {{
      if (val && val !== lastSent) {{
        lastSent = val;
        sendPayload(val);
        inp.value = "";
      }}
    }}, 3500);
  }}
}});

// focus forcé global
window.addEventListener('keydown', () => {{
  if (document.activeElement !== inp) inp.focus();
}});
</script>
""", height=300)

st.markdown(f"<p style='text-align:center;font-size:1rem'>{mode}</p>", unsafe_allow_html=True)
