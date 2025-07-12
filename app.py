import streamlit as st
import streamlit.components.v1 as components

# Webhooks
WEBHOOK_URL_TEXT = "https://nbjhhh.app.n8n.cloud/webhook/default-text"  # <-- remplace si besoin
WEBHOOK_URL_PREFIL = "https://nbjhhh.app.n8n.cloud/webhook/225784dc-80f4-4184-a0df-ae6eee1fb74c"

st.set_page_config(page_title="", layout="centered")

# Inject CSS + Google Font
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Avenir+Next:wght@100&display=swap');
html, body, [class*="css"] {
  font-family: 'Avenir Next', sans-serif !important;
  font-weight: 100;
}
input:focus, textarea:focus, select:focus {
  outline: none !important;
  box-shadow: none !important;
  border: none !important;
}
button {
  border: none;
  background: none;
  font-size: 14px;
  font-family: 'Avenir Next', sans-serif;
  font-weight: 100;
  letter-spacing: 0.15em;
  text-transform: uppercase;
  cursor: pointer;
  margin: 8px auto;
  display: block;
}
</style>
""", unsafe_allow_html=True)

# Toggle Prefil mode
if 'prefil' not in st.session_state:
    st.session_state.prefil = False

col1, col2 = st.columns(2)
with col1:
    if st.button("Activer Préfil"):
        st.session_state.prefil = True
with col2:
    if st.button("Désactiver Préfil"):
        st.session_state.prefil = False

# Choisir le webhook selon le mode
current_webhook = WEBHOOK_URL_PREFIL if st.session_state.prefil else WEBHOOK_URL_TEXT

# HTML INPUT invisible mais actif
components.html(f"""
<div style="display:flex;align-items:center;justify-content:center;height:50vh">
  <input id="input" 
         autofocus 
         style="
           font-size: 2rem;
           font-family: 'Avenir Next', sans-serif;
           font-weight: 100;
           letter-spacing: .5rem;
           background: transparent;
           border: none;
           text-align: center;
           width: 60vw;
         "
         placeholder=""/>
</div>
<script>
  const inp = document.getElementById('input');
  let timer;
  let lastSent = "";
  let prefil = {str(st.session_state.prefil).lower()};

  document.body.addEventListener('keydown', () => {{ inp.focus(); }});

  function send(val) {{
    if (!val.trim()) return;
    fetch("{current_webhook}", {{
      method: "POST",
      headers: {{ 'Content-Type': 'application/json' }},
      body: JSON.stringify({{ value: val }})
    }});
  }}

  inp.addEventListener('input', () => {{
    clearTimeout(timer);
    const val = inp.value;
    if (!prefil) {{
      timer = setTimeout(() => send(val), 3500);
    }} else {{
      if (val.length % 3 === 0 && val !== lastSent) {{
        send(val);
        lastSent = val;
      }}
    }}
  }});
</script>
""", height=400)
