# app.py
import streamlit as st
import streamlit.components.v1 as components

st.set_page_config(layout="centered")

# HTML/CSS/JS pour une zone de texte invisible, centrée et responsive
components.html("""
  <style>
    #editor {
      position: absolute;
      top: 50%;
      left: 50%;
      transform: translate(-50%, -50%);
      width: 80%;
      outline: none;
      border: none;
      background: transparent;
      font-family: 'Polysavion', sans-serif;
      font-weight: 100;
      letter-spacing: 0.2em;
      text-align: center;
      white-space: pre-wrap;
      margin: 0;
      padding: 0;
    }
  </style>
  <div id="editor" contenteditable="true"></div>
  <script>
    window.onload = function() {
      const ed = document.getElementById('editor');
      ed.focus();  // focus automatique, pas besoin de cliquer
      // la saisie positionne le curseur où il faut
      ed.addEventListener('keydown', function(e) {
        // rien d’autre à ajouter — contenteditable gère le retour à la ligne
      });
    };
  </script>
""", height=600)
