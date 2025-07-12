# app.py
import streamlit as st
import streamlit.components.v1 as components

# ── WEBHOOKS ──────────────────────────────────────────────────────────────────
WEBHOOK_TEXT   = "https://nbjhhh.app.n8n.cloud/webhook/default-text"  # texte normal
WEBHOOK_PREFIL = "https://nbjhhh.app.n8n.cloud/webhook/225784dc-80f4-4184-a0df-ae6eee1fb74c"  # préfil (3 car.)

# ── PAGE ───────────────────────────────────────────────────────────────────────
st.set_page_config(layout="centered", page_title="")

st.markdown(
    """
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Avenir+Next:wght@100&display=swap');

    html, body, [class*="css"] { margin:0; padding:0; background:#fff; font-family:'Avenir Next',sans-serif; font-weight:100; }
    *:focus { outline:none !important; }

    /* zone éditable sans cadre */
    .zone { font-size:3rem; text-align:center; line-height:1.2; width:80vw; max-width:600px; margin:0 auto; border:none; }

    /* boutons custom */
    .btn { display:block; width:200px; margin:8px auto; background:transparent; border:none; cursor:pointer; font-size:0.9rem; letter-spacing:0.12em; text-transform:uppercase; font-family:'Avenir Next',sans-serif; font-weight:100; }
    </style>
    """,
    unsafe_allow_html=True,
)

# ── SESSION STATE ─────────────────────────────────────────────────────────────
if "prefil" not in st.session_state:
    st.session_state.prefil = False

# ── BOUTONS ────────────────────────────────────────────────────────────────────
col = st.columns(1)[0]
with col:
    if st.button("Activer Préfil", key="on", help="Mode envoi tous les 3 caractères", type="secondary"):
        st.session_state.prefil = True
    if st.button("Désactiver Préfil", key="off", help="Mode envoi après 3,5 s", type="secondary"):
        st.session_state.prefil = False

# ── HTML / JS ──────────────────────────────────────────────────────────────────
components.html(
    f"""
<div style='display:flex;justify-content:center;align-items:center;height:50vh;'>
  <div id='zone' class='zone' contenteditable='true' spellcheck='false'>&nbsp;</div>
</div>

<script>
  const zone = document.getElementById('zone');
  let timer; let last = ""; const prefilMode = {str(st.session_state.prefil).lower()};

  // focus global
  document.addEventListener('keydown', () => zone.focus());

  function send(url, txt) {{ fetch(url, {{method:'POST', headers:{{'Content-Type':'application/json'}}, body:JSON.stringify({{body:txt}})}}); }}

  zone.addEventListener('input', () => {{
      const txt = zone.innerText.replace(/\u00A0/g,' ').trim();
      clearTimeout(timer);

      if (prefilMode && txt.length >=3 && txt.length%3===0 && txt!==last) {{
          last = txt;
          send('{WEBHOOK_PREFIL}', txt);
      }}
      if (!prefilMode) {{
          timer = setTimeout(()=>{{ send('{WEBHOOK_TEXT}', txt); zone.innerText=''; last=''; }}, 3500);
      }}
  }});
</script>
""",
    height=450,
)
