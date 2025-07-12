# app.py
import streamlit as st
import streamlit.components.v1 as components
import requests
from bs4 import BeautifulSoup
from urllib.parse import urljoin, urlparse

# ─── CONFIG ────────────────────────────────────────────────────────────────────
WEBHOOK_URL = "https://<VOTRE_BASE_URL_N8N>/webhook/225784dc-80f4-4184-a0df-ae6eee1fb74c"

# ─── PAGE STREAMLIT ────────────────────────────────────────────────────────────
st.set_page_config(layout="centered", initial_sidebar_state="collapsed",
                   page_title="", page_icon="")

st.markdown(
    """
    <style>
      /* toile blanche pure */
      #MainMenu, header, footer { visibility: hidden; }
      html, body { margin: 0; padding: 0; height: 100%; }

      /* style des vignettes Apple-style */
      .card {
        display: inline-block;
        width: 240px;
        height: 160px;
        margin: 8px;
        padding: 12px;
        border-radius: 24px;
        background: rgba(255,255,255,0.2);
        backdrop-filter: blur(20px);
        text-align: center;
        font-family: 'Avenir Next', sans-serif;
        font-weight: 200;
        font-size: 0.9rem;
        overflow: hidden;
        vertical-align: top;
      }
      .card a {
        color: inherit;
        text-decoration: none;
      }
    </style>
    <link href="https://fonts.googleapis.com/css2?family=Avenir+Next:wght@200&display=swap" rel="stylesheet">
    """,
    unsafe_allow_html=True,
)

# ─── ZONE MINIMALISTE × JS ENVOI WEBHOOK ────────────────────────────────────
html = f"""
<div style="display:flex;justify-content:center;align-items:center;height:40vh">
  <input id="inp" 
         style="
           font-family:'Avenir Next',sans-serif;
           font-weight:200;
           font-size:2rem;
           border:none;
           outline:none;
           background:transparent;
           text-align:center;
           letter-spacing:1rem;
         "
         type="text" placeholder=". . ." autofocus>
</div>
<script>
  const inp = document.getElementById('inp');
  let tm;
  function send(t) {{
    if (!t.trim()) return;
    fetch("{WEBHOOK_URL}", {{
      method: "POST",
      headers: {{ "Content-Type": "application/json" }},
      body: JSON.stringify({{ body: t }})
    }});
    inp.value = "";
  }}
  inp.addEventListener('keyup', e => {{
    clearTimeout(tm);
    if (e.key === 'Enter') send(inp.value);
    else tm = setTimeout(() => send(inp.value), 3000);
  }});
</script>
"""
components.html(html, height=300)

# ─── INPUT URL + BOUTON D’EXTRACTION ───────────────────────────────────────────
url = st.text_input("", value="", placeholder="https://…")
if st.button("EXTRAIRE PDF & AUDIO"):
    if not url.strip():
        st.warning("Merci de saisir une URL valide.")
    else:
        try:
            resp = requests.get(url, timeout=10)
            resp.raise_for_status()
            base = url
            parsed = urlparse(url)
            domain = f"{parsed.scheme}://{parsed.netloc}"
            soup = BeautifulSoup(resp.text, "html.parser")

            # collecte des liens .pdf et .mp3
            assets = set()
            for tag in soup.find_all(['a', 'source', 'link', 'audio']):
                for attr in ('href','src'):
                    link = tag.get(attr)
                    if link and (link.lower().endswith('.pdf') or link.lower().endswith('.mp3')):
                        full = urljoin(base, link)
                        assets.add(full)

            if not assets:
                st.info("Aucun PDF ni fichier audio trouvé dans le code source.")
            else:
                st.markdown("<div>", unsafe_allow_html=True)
                for asset in assets:
                    name = asset.split("/")[-1]
                    ext  = name.split('.')[-1].upper()
                    # vignette
                    st.markdown(f"""
                      <div class="card">
                        <div style="height:80px;line-height:80px;">
                          {ext}
                        </div>
                        <div style="font-size:0.8rem;overflow:hidden;text-overflow:ellipsis;">
                          <a href="{asset}" target="_blank">{name}</a>
                        </div>
                      </div>
                    """, unsafe_allow_html=True)

                    # lecteur audio si MP3
                    if asset.lower().endswith('.mp3'):
                        st.audio(asset)
                st.markdown("</div>", unsafe_allow_html=True)

        except Exception as e:
            st.error(f"Erreur lors de la récupération : {e}")
