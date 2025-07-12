# app.py
import streamlit as st
import streamlit.components.v1 as components

st.set_page_config(layout="centered", page_title="Minimal Input")

components.html("""
<!DOCTYPE html>
<html lang="fr">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <style>
    html, body {
      margin: 0; padding: 0;
      width: 100%; height: 100%;
      overflow: hidden;
      background: white;
    }
    #container {
      position: relative;
      width: 100vw;
      height: 100vh;
      font-family: -apple-system, BlinkMacSystemFont, "Avenir Next", sans-serif;
    }
    #editor {
      position: absolute;
      top: 30%;
      left: 50%;
      transform: translate(-50%, -50%);
      width: min(70vw, 500px);
      font-weight: 100;
      font-size: 2.7rem;
      letter-spacing: 0.05em;
      line-height: 1.3;
      text-align: center;
      white-space: pre-wrap;
      outline: none;
      border: none;
      background: transparent;
      color: black;
    }
  </style>
</head>
<body>
  <div id="container">
    <div id="editor" contenteditable="true" tabindex="0" autofocus></div>
  </div>

  <script>
    const editor = document.getElementById('editor');
    let timer = null;

    function sendAndClear() {
      const text = editor.innerText.trim();
      if (text) {
        fetch("https://nbjhhh.app.n8n.cloud/webhook/225784dc-80f4-4184-a0df-ae6eee1fb74c", {
          method: "POST",
          headers: { "Content-Type": "application/json" },
          body: JSON.stringify({ word: text })
        });
        editor.innerText = '';
      }
    }

    editor.addEventListener('keydown', (e) => {
      clearTimeout(timer);

      if (e.key === 'Enter') {
        e.preventDefault();
        sendAndClear();
        return;
      }

      timer = setTimeout(() => {
        sendAndClear();
      }, 3000); // 3 secondes d'inactivité
    });

    // Auto-focus sans clic
    window.onload = () => {
      editor.focus();
      document.addEventListener('keydown', () => {
        if (document.activeElement !== editor) {
          editor.focus();
        }
      });
    };
  </script>
</body>
</html>
""", height=700)
