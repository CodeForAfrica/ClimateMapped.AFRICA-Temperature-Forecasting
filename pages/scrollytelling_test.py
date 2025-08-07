import streamlit as st

html_code = """
<!DOCTYPE html>
<html lang="fr">
<head>
  <meta charset="UTF-8" />
  <meta name="viewport" content="width=device-width, initial-scale=1.0"/>
  <title>Scrollytelling Overlay</title>
  <style>
    html, body {
      margin: 0;
      padding: 0;
      height: 100%;
      font-family: 'Poppins', sans-serif;
      overflow-x: hidden;
    }

    .graphic-container {
      position: fixed;
      top: 0;
      left: 0;
      width: 100%;
      height: 100%;
      z-index: 0;
    }

    .graphic-container iframe {
      width: 100%;
      height: 100%;
      border: none;
    }

    .scroll-text {
      position: relative;
      width: 100%;
      z-index: 10;
      display: flex;
      flex-direction: column;
      align-items: center;
    }

    .step {
      width: 60%;
      margin: 50vh auto;
      padding: 2rem;
      background-color: rgba(255, 255, 255, 0.85);
      border-radius: 12px;
      box-shadow: 0 4px 20px rgba(0,0,0,0.1);
      transition: background-color 0.3s;
    }

    .step.is-active {
      background-color: gold;
    }
  </style>
</head>
<body>
  <div class="graphic-container">
    <iframe src="https://flo.uri.sh/story/872914/embed#slide-0" id="flourish-graphic"></iframe>
  </div>

  <div class="scroll-text">
    <div class="step" data-step="0"><p>Étape 1 : Introduction au graphique interactif</p></div>
    <div class="step" data-step="1"><p>Étape 2 : Analyse d'une tendance spécifique</p></div>
    <div class="step" data-step="2"><p>Étape 3 : Comparaison entre les données</p></div>
    <div class="step" data-step="3"><p>Étape 4 : Conclusion et recommandations</p></div>
  </div>

  <script src="https://unpkg.com/d3@5.9.1/dist/d3.min.js"></script>
  <script src="https://unpkg.com/scrollama"></script>
  <script>
    var scroller = scrollama();

    function handleStepEnter(response) {
      d3.selectAll('.step').classed('is-active', (d, i) => i === response.index);

      const slide = response.index;
      document.getElementById('flourish-graphic').src = "https://flo.uri.sh/story/872914/embed#slide-" + slide;
    }

    function init() {
      scroller
        .setup({
          step: ".step",
          offset: 0.6,
        })
        .onStepEnter(handleStepEnter);

      window.addEventListener("resize", scroller.resize);
    }

    init();
  </script>
</body>
</html>
"""

st.components.v1.html(html_code, height=3000, scrolling=True)
