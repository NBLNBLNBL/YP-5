# app.py
import streamlit as st
import streamlit.components.v1 as components
import requests
import os
from pytube import YouTube
from bs4 import BeautifulSoup
from urllib.parse import urljoin, urlparse

# ─── CONFIG ────────────────────────────────────────────────────────────────────
WEBHOOK_URL = ""  # TODO : remplacez par votre URL de webhook

DOWNLOAD_DIR = "downloads"
os.makedirs(DOWNLOAD_DIR, exist_ok=True)

# ─── FONCTIONS DE TÉLÉCHARGEMENT ────────────────────────────────────────────────
def download_youtube(url):
    """Télécharge la meilleure résolution MP4 d'une vidéo YouTube."""
    yt = YouTube(url)
    stream = yt.streams.filter(progressive=True, file_extension="mp4") \
                       .order_by("resolution").desc().first()
    stream.download(output_path=DOWNLOAD_DIR)

def download_site(url, visited=None):
    """Crawl basique du domaine et téléchargement des assets (images, scripts, CSS…)."""
    if visited is None:
        visited = set()
    domain = urlparse(url).netloc
    if url in visited:
        return
    visited.add(url)

    try:
        r = requests.get(url)
        r.raise_for_status()
    except Exception:
        return

    soup = BeautifulSoup(r.text, "html.parser")

    # Assets à télécharger
    for tag in soup.find_all(("img", "script", "link")):
        attr = "src" if tag.name in ("img", "script") else "href"
        src = tag.get(attr)
        if not src:
            continue
        file_url = urljoin(url, src)
        if urlparse(file_url).netloc != domain:
            continue
        try:
            res = requests.get(file_url)
            res.raise_for_status()
            filename = os.path.join(DOWNLOAD_DIR, os.path.basename(file_url))
            with open(filename, "wb") as f:
                f.write(res.content)
        except Exception:
            pass

    # Crawl des liens internes
    for a in soup.find_all("a", href=True):
        link = urljoin(url, a["href"])
        if urlparse(link).netloc == domain:
            download_site(link, visited)

# ─── CONFIGURATION DE LA PAGE ───────────────────────────────────────────────────
st.set_page_config(page_title="Minimalist Streamlit App", layout="wide")

# ─── STYLES CSS ────────────────────────────────────────────────────────────────
st.markdown(
    """
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Avenir+Next:wght@200;400&display=swap');
    html, body, [class*="css"] { font-family: 'Avenir Next', sans-serif; }
    .container {
        background: white;
        border-radius: 24px;
        padding: 16px;
    }
    #customInput {
        width: 100%;
        padding: 20px;
        font-size: 2rem;
        font-weight: 200;
        border: none;
        outline: none;
        background: white;
        color: black;
    }
    ::placeholder { letter-spacing: 1rem; color: #888; }
    .btn-text {
        text-transform: uppercase;
        font-size: 0.8rem;
        font-weight: 200;
        background: rgba(255,255,255,0.3);
        backdrop-filter: blur(10px);
        border-radius: 12px;
        border: none;
        padding: 6px 12px;
        margin: 4px;
        cursor: pointer;
    }
    </style>
    """,
    unsafe_allow_html=True,
)

# ─── HTML + JS EMBEDDÉ ────────────────────────────────────────────────────────
html = f"""
<div class="container">
  <input type="text" id="customInput" placeholder=". . ." autofocus />
  <div style="margin-top:12px;">
    <span class="btn-text" onclick="sendText('ACTION1')">Action1</span>
    <span class="btn-text" onclick="sendText('ACTION2')">Action2</span>
  </div>
</div>
<script>
let timer;
const input = document.getElementById("customInput");

function sendText(text) {{
    const payload = {{ text }};
    if ("{WEBHOOK_URL}") {{
        fetch("{WEBHOOK_URL}", {{
            method: "POST",
            headers: {{ "Content-Type": "application/json" }},
            body: JSON.stringify(payload)
        }});
    }} else {{
        console.log("Ready to send:", payload);
    }}
}}

input.addEventListener("keyup", (e) => {{
    clearTimeout(timer);
    if (e.key === "Enter") {{
        sendText(input.value);
        input.value = "";
    }} else {{
        timer = setTimeout(() => {{
            sendText(input.value);
            input.value = "";
        }}, 3000);
    }}
}});
</script>
"""
components.html(html, height=160)

st.write("🎥 Entrez une URL YouTube ou l’URL d’un site web ci-dessous pour lancer le téléchargement :")

url = st.text_input("URL à télécharger", "")
if url:
    st.write(f"Tentative de traitement de : {url}")
    if "youtube.com" in url or "youtu.be" in url:
        download_youtube(url)
        st.success("Vidéo YouTube téléchargée !")
    else:
        download_site(url)
        st.success("Site web téléchargé ! (assets et pages internes)")
