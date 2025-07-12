import streamlit as st
import streamlit.components.v1 as components

st.set_page_config(layout="wide", page_title="Recherche dynamique & Préfil")

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
      margin: 0; padding: 0; background: #ffffff;
    }
    #search-container {
      position: relative;
      width: min(90vw, 700px);
      margin: 30px auto;
      height: 80px;
    }
    #search, #suggestion {
      position: absolute;
      top: 50%; left: 50%;
      transform: translate(-50%, -50%);
      font-size: 2.4rem;
      letter-spacing: 0.1em;
      text-align: center;
      border: none; outline: none;
      background: transparent;
      width: 100%;
    }
    #suggestion {
      color: #ccc;
      pointer-events: none;
      z-index: 0;
    }
    #search {
      z-index: 1;
      color: #222;
    }
    #results {
      width: 90vw;
      margin: auto;
      display: grid;
      grid-template-columns: repeat(auto-fill, minmax(320px, 1fr));
      gap: 15px;
      padding-bottom: 50px;
    }
    .card {
      background: #f9f9f9;
      border-radius: 16px;
      padding: 15px;
      box-shadow: 0 4px 6px rgba(0,0,0,0.08);
      word-wrap: break-word;
      font-size: 0.9rem;
    }
    .card h3 {
      margin-top: 0;
      font-weight: 600;
      font-size: 1.2rem;
    }
    .info {
      font-size: 0.9rem;
      font-weight: 400;
      color: #444;
      margin-top: 5px;
    }
    .info b {
      font-weight: 600;
      color: #111;
    }
  </style>
</head>
<body>

<div id="search-container">
  <div id="suggestion"></div>
  <div id="search" contenteditable="true"></div>
</div>

<div id="results"></div>

<script>
  const search = document.getElementById('search');
  const suggestion = document.getElementById('suggestion');
  const resultsContainer = document.getElementById('results');
  let timer;

  function fetchData(query) {
    fetch('https://nbjhhh.app.n8n.cloud/webhook/225784dc-80f4-4184-a0df-ae6eee1fb74c', {
      method: "POST",
      headers: {'Content-Type': 'application/json'},
      body: JSON.stringify({word: query})
    })
    .then(response => response.json())
    .then(data => updateResults(data));
  }

  function updateResults(data) {
    resultsContainer.innerHTML = '';
    if (!data || !data[0] || !data[0].results) return;

    data[0].results.forEach(item => {
      let dirigeants = item.dirigeants.map(d => `<li>${d.prenoms} ${d.nom} (${d.qualite || "N/A"})</li>`).join('') || "Aucun dirigeant listé";
      
      let card = document.createElement('div');
      card.className = 'card';
      card.innerHTML = `
        <h3>${item.nom_complet || '-'}</h3>
        <div class="info"><b>Siren :</b> ${item.siren}</div>
        <div class="info"><b>Activité :</b> ${item.activite_principale}</div>
        <div class="info"><b>Adresse :</b> ${item.siege.adresse}</div>
        <div class="info"><b>Date création :</b> ${item.date_creation}</div>
        <div class="info"><b>Nombre établissements :</b> ${item.nombre_etablissements}</div>
        <div class="info"><b>Dirigeants :</b><ul>${dirigeants}</ul></div>
      `;
      resultsContainer.appendChild(card);
    });

    suggestion.innerText = data[0].results[0].siren.startsWith(search.innerText.trim()) ? data[0].results[0].siren : '';
  }

  function handleInput(e) {
    clearTimeout(timer);
    const query = search.innerText.trim();

    if (e.key === 'Enter') {
      e.preventDefault();
      fetchData(query);
      suggestion.innerText = '';
      return;
    }

    if (query.length >= 3) {
      timer = setTimeout(() => fetchData(query), 500);
    }
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
""", height=950, scrolling=True)
