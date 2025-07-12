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
  <style>
    html, body {
      margin: 0; padding: 0;
      width: 100%; height: 100%;
      overflow: hidden;
      background: #fff;
    }
    #container {
      position: relative;
      width: 100vw;
      height: 100vh;
    }
    #editor {
      position: absolute;
      top: 45%;      /* légèrement plus haut */
      left: 50%;
      transform: translate(-50%, -50%);
      width: min(70vw, 500px);  /* zone plus petite */
      outline: none;
      border: none;
      background: transparent;
      font-family: 'aviaNext ExtraFine', sans-serif;  /* extra fin */
      font-weight: 100;
      font-size: 2.5rem;      /* un peu plus gros */
      letter-spacing: 0.1em;  /* espacement réduit */
      line-height: 1.3;
      text-align: center;
      white-space: pre-wrap;
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
    window.onload = () => {
      const ed = document.getElementById('editor');
      ed.focus();  // focus automatique
      document.addEventListener('keydown', () => {
        if (document.activeElement !== ed) {
          ed.focus();
        }
      });
    };
  </script>
</body>
</html>
""", height=700)
