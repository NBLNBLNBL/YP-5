# app.py
import streamlit as st
import streamlit.components.v1 as components

st.set_page_config(layout="centered", page_title="Canvas Minimaliste")

components.html("""
  <!DOCTYPE html>
  <html lang="fr">
  <head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <!-- Polysavion extra fin depuis CDN -->
    <link href="https://fonts.cdnfonts.com/css/polysavion" rel="stylesheet">
    <style>
      html, body {
        margin: 0; padding: 0;
        width: 100%; height: 100%;
        overflow: hidden;
        background: #fff;
      }
      #container {
        display: flex;
        align-items: center;
        justify-content: center;
        width: 100vw;
        height: 100vh;
      }
      #editor {
        width: min(80vw, 600px);
        /* Taille adaptée à iPhone (~350px) et MacBook Air (~600px) */
        outline: none;
        border: none;
        background: transparent;
        font-family: 'Polysavion', sans-serif;
        font-weight: 100;
        letter-spacing: 0.3em;
        font-size: 2rem;       /* un peu plus gros */
        line-height: 1.5;      /* espacement plus large */
        text-align: center;    /* texte centré */
        white-space: pre-wrap; /* retours à la ligne auto */
        margin: 0;
        padding: 0;
      }
    </style>
  </head>
  <body>
    <div id="container">
      <div id="editor" contenteditable="true" tabindex="0"></div>
    </div>
    <script>
      window.onload = function() {
        const ed = document.getElementById('editor');
        ed.focus();  // focus automatique : on n'a pas besoin de cliquer
        // Si on tape ailleurs, on remet le focus
        document.addEventListener('keydown', function() {
          if (document.activeElement !== ed) {
            ed.focus();
          }
        });
      };
    </script>
  </body>
  </html>
""", height=800)
