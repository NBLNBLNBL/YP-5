import streamlit as st
import streamlit.components.v1 as components

# Webhooks
DEFAULT_WEBHOOK = "https://your-default-webhook-url"
PREFIL_WEBHOOK = "https://nbjhhh.app.n8n.cloud/webhook/225784dc-80f4-4184-a0df-ae6eee1fb74c"

# Préfil mode (session)
if "prefil" not in st.session_state:
    st.session_state.prefil = False

# Style global
st.set_page_config(page_title="", page_icon="", layout="wide")
st.markdown("""
    <style>
    body, html {
        background: white;
        margin: 0;
        padding: 0;
        font-family: 'Avenir Next', sans-serif;
        font-weight: 200;
        font-size: 2rem;
        letter-spacing: .3rem;
        overflow-x: hidden;
        text-align: center;
    }
    input:focus, textarea:focus {
        outline: none !important;
        box-shadow: none !important;
        border: none !important;
    }
    #text-input {
        width: 100%;
        border: none;
        background: transparent;
        color: black;
        font-family: 'Avenir Next', sans-serif;
        font-weight: 200;
        font-size: 2.5rem;
        text-align: center;
        letter-spacing: .4rem;
    }
    .btn {
        font-family: 'Avenir Next', sans-serif;
        font-weight: 200;
        font-size: 1rem;
        text-transform: uppercase;
        border: none;
        background: none;
        cursor: pointer;
        margin: 20px auto;
        display: block;
    }
    </style>
""", unsafe_allow_html=True)

# Boutons Préfil
col1, col2 = st.columns(2)
with col1:
    if st.button("Activer Préfil"):
        st.session_state.prefil = True
with col2:
    if st.button("Désactiver Préfil"):
        st.session_state.prefil = False

# Zone HTML
webhook_url = PREFIL_WEBHOOK if st.session_state.prefil else DEFAULT_WEBHOOK
js = f"""
<script>
let buffer = "";
let timer = null;

function send(text) {{
    fetch("{webhook_url}", {{
        method: "POST",
        headers: {{ "Content-Type": "application/json" }},
        body: JSON.stringify({{ message: text }})
    }});
}}

document.addEventListener("keydown", function(e) {{
    buffer += e.key;
    document.getElementById("display").textContent = buffer;

    if (timer) clearTimeout(timer);

    // Envoi selon mode
    if ({'true' if st.session_state.prefil else 'false'}) {{
        if (buffer.length % 3 === 0) {{
            send(buffer);
        }}
    }} else {{
        timer = setTimeout(() => {{
            send(buffer);
        }}, 3500);
    }}
}});
</script>
"""

html = """
<div style="height:70vh;display:flex;align-items:center;justify-content:center;">
  <div id="display"></div>
</div>
""" + js

components.html(html, height=500)
