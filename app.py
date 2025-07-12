# app.py
import streamlit as st
import streamlit.components.v1 as components

# ─── CONFIGURATION ─────────────────────────────────────────────────────────────
# Remplacez par l'URL racine de votre instance n8n (sans slash final)
BASE_N8N_URL       = "https://<VOTRE_BASE_URL_N8N>"
MAIN_WEBHOOK_PATH = "webhook/225784dc-80f4-4184-a0df-ae6eee1fb74c"
# Webhooks complets
MAIN_WEBHOOK       = f"{BASE_N8N_URL}/{MAIN_WEBHOOK_PATH}"
RESPONSIVE_WEBHOOK = f"{BASE_N8N_URL}/{MAIN_WEBHOOK_PATH}"

# ─── INITIALISATION STREAMLIT ──────────────────────────────────────────────────
st.set_page_config(
    layout="centered",
    initial_sidebar_state="collapsed",
    page_title="",
    page_icon=""
)

# ─── CSS ULTRA-MINIMALISTE ─────────────────────────────────────────────────────
st.markdown(
    """
    <style>
      /* Masquer toute UI native Streamlit */
      #MainMenu, header, footer { visibility: hidden; }
      html, body { margin:0; padding:0; height:100%; width:100%; overflow:hidden; }

      /* Conteneur full-screen centré */
      body > div { 
        display: flex !important;
        justify-content: center;
        align-items: center;
        height: 100vh;
        width: 100vw;
        background: #fff;
      }

      /* Input “vide” */
      #voidInput {
        font-family: 'Avenir Next', sans-serif;
        font-weight: 200;
        font-size: 2rem;
        width: 80vw; max-width: 400px;
        border: none;
        outline: none;
        background: transparent;
        text-align: center;
        caret-color: #007AFF;
      }

      /* Bouton Préfil discrètement placé */
      #prefilBtn {
        position: absolute;
        top: 16px; right: 16px;
        font-family: 'Avenir Next', sans-serif;
        font-weight: 200;
        font-size: 0.75rem;
        text-transform: uppercase;
        background: transparent;
        border: none;
        color: rgba(0,0,0,0.3);
        cursor: pointer;
        transition: color 0.2s ease;
      }
      #prefilBtn:hover {
        color: rgba(0,0,0,0.6);
      }

      /* Toast éphémère */
      #toast {
        position: fixed;
        bottom: 10vh;
        left: 50%;
        transform: translateX(-50%);
        background: rgba(255,255,255,0.8);
        backdrop-filter: blur(10px);
        font-family: 'Avenir Next', sans-serif;
        font-weight: 200;
        font-size: 1rem;
        padding: 8px 16px;
        border-radius: 12px;
        opacity: 0;
        transition: opacity 0.3s ease;
      }
      #toast.show { opacity: 1; }
    </style>
    <link href="https://fonts.googleapis.com/css2?family=Avenir+Next:wght@200&display=swap" rel="stylesheet">
    """,
    unsafe_allow_html=True
)

# ─── COMPOSANT HTML / JS ───────────────────────────────────────────────────────
components.html(f"""
<!DOCTYPE html>
<html><head><meta charset="utf-8"/></head><body>

  <!-- Bouton Préfil -->
  <button id="prefilBtn">Préfil</button>

  <!-- Zone de saisie “vide” -->
  <input id="voidInput" type="text" autofocus />

  <!-- Toast éphémère -->
  <div id="toast">Mode pré-remplissage activé</div>

  <script>
    const inp      = document.getElementById('voidInput');
    const prefil   = document.getElementById('prefilBtn');
    const toast    = document.getElementById('toast');
    let timer, toastTimer;

    // Fonction générique d'envoi
    function postTo(url, payload) {{
      fetch(url, {{
        method: 'POST',
        headers: {{ 'Content-Type': 'application/json' }},
        body: JSON.stringify(payload)
      }});
    }}

    // 1) Envoyer le texte saisi (Enter ou 5s inactivité)
    function scheduleSend() {{
      clearTimeout(timer);
      timer = setTimeout(() => {{
        const t = inp.value.trim();
        if (!t) return;
        postTo("{MAIN_WEBHOOK}", {{ body: t }});
        inp.value = '';
      }}, 5000);
    }}

    inp.addEventListener('keydown', () => {{
      // focus auto dès que l'utilisateur commence à taper
      if (document.activeElement !== inp) inp.focus();
      scheduleSend();
    }});

    inp.addEventListener('keyup', (e) => {{
      if (e.key === 'Enter') {{
        clearTimeout(timer);
        const t = inp.value.trim();
        if (!t) return;
        postTo("{MAIN_WEBHOOK}", {{ body: t }});
        inp.value = '';
      }}
    }});

    // 2) Mode Préfil : envoi immédiat, toast 2s
    prefil.addEventListener('click', () => {{
      postTo("{RESPONSIVE_WEBHOOK}", {{ mode: 'prefil' }});
      toast.classList.add('show');
      clearTimeout(toastTimer);
      toastTimer = setTimeout(() => {{ toast.classList.remove('show'); }}, 2000);
    }});
  </script>

</body></html>
""", height=600)
