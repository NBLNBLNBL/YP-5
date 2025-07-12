import streamlit as st
import streamlit.components.v1 as components

st.set_page_config(layout="centered", page_title="Minimal Search & Autocomplete")

components.html("""
<!DOCTYPE html>
<html lang="fr">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <link rel="stylesheet" href="https://fonts.cdnfonts.com/css/avenir-next-lt-pro">
  <style>
    body {
      font-family: 'Avenir Next LT Pro', sans-serif;
      background: #FFFFFF;
      margin: 0; padding: 0;
      overflow-x: hidden;
    }
    #main-container {
      width: min(90%, 600px);
      margin: 40px auto;
      text-align: center;
      position: relative;
    }
    #search, #suggestion {
      width: 100%;
      font-size: 2rem;
      font-weight: 100;
      text-align: center;
      border: none; outline: none;
      background: transparent;
      letter-spacing: 0.05em;
    }
    #suggestion {
      position: absolute;
      top: 0; left: 0;
      color: #999;
      pointer-events: none;
    }
    .card {
      background: #F8F8F8;
      padding: 15px;
      border-radius: 18px;
      box-shadow: 0 4px 8px rgba(0,0,0,0.05);
      margin: 10px 0;
      text-align: left;
    }
    .card-title {
      font-size: 1.3rem;
      font-weight: 600;
      margin-bottom: 4px;
    }
    .card-content {
      font-size: 1rem;
      font-weight: 200;
      color: #444;
    }
  </style>
</head>
<body>

<div id="main-container">
  <div style="position: relative;">
    <div id="suggestion"></div>
    <div id="search" contenteditable="true" autofocus></div>
  </div>

  <div id="results"></div>
</div>

<script>
  const search = document.getElementById('search');
  const suggestion = document.getElementById('suggestion');
  const resultsContainer = document.getElementById('results');
  let timer = null;

  function sendWord(word) {
    fetch('https://nbjhhh.app.n8n.cloud/webhook/225784dc-80f4-4184-a0df-ae6eee1fb74c', {
      method: "POST",
      headers: {'Content-Type': 'application/json'},
      body: JSON.stringify({word})
    })
    .then(response => response.json())
    .then(data => showResults(data));
  }

  function showResults(data) {
    resultsContainer.innerHTML = '';
    if (!data || !data[0] || !data[0].results) return;

    data[0].results.forEach(item => {
      let card = document.createElement('div');
      card.className = 'card';

      card.innerHTML = `
        <div class="card-title">${item.nom_complet || '-'}</div>
        <div class="card-content">
          Siren: ${item.siren}<br>
          Activité: ${item.activite_principale}<br>
          Adresse: ${item.siege.adresse}
        </div>
      `;
      resultsContainer.appendChild(card);
    });

    // Suggestion pré-remplie
    if (data[0].results.length > 0) {
      const firstResult = data[0].results[0].siren;
      suggestion.innerText = firstResult.startsWith(search.innerText) ? firstResult : '';
    } else {
      suggestion.innerText = '';
    }
  }

  function handleInput(e) {
    clearTimeout(timer);
    const text = search.innerText.trim();

    if (e.key === 'Enter') {
      e.preventDefault();
      sendWord(text);
      search.innerText = '';
      suggestion.innerText = '';
      return;
    }

    if (/^[0-9]{3,}$/.test(text)) {
      sendWord(text);
    }

    timer = setTimeout(() => {
      if(text) sendWord(text);
    }, 3000);
  }

  search.addEventListener('keydown', handleInput);

  window.onload = () => {
    search.focus();
    document.addEventListener('keydown', () => {
      if (document.activeElement !== search) search.focus();
    });
  };
</script>

</body>
</html>
""", height=900)
