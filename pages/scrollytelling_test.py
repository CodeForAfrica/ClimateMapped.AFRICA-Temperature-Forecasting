import streamlit as st

html_code = """
<!doctype html>
<html lang="fr">
<head>
  <meta charset="utf-8">
  <title>Scrollytelling avec Flourish</title>
  <meta name="viewport" content="width=device-width, initial-scale=1">
  
  <!-- Scrollama & D3 -->
  <script src="https://unpkg.com/d3@5.9.1/dist/d3.min.js"></script>
  <script src="https://unpkg.com/intersection-observer"></script>
  <script src="https://unpkg.com/scrollama"></script>
  
  <!-- Flourish -->
  <script src="https://public.flourish.studio/resources/embed.js"></script>

  <style>
    body {
      margin: 0;
      font-family: 'Poppins', sans-serif;
    }

    #scrolly__section {
      position: relative;
      height: 100vh;
      width: 100%;
      overflow-x: hidden;
    }

    .scrolly__chart {
      position: fixed;
      top: 0;
      left: 0;
      height: 100vh;
      width: 100%;
      z-index: 0;
    }

    .scrolly__chart iframe {
      width: 100%;
      height: 100%;
      border: none;
    }

    .scrolly__content {
      position: relative;
      width: 100%;
      z-index: 2;
    }

    .step {
      height: 100vh;
      display: flex;
      align-items: center;
      justify-content: center;
    }

    .text-block {
      background: rgba(255, 255, 255, 0.85);
      padding: 2rem;
      max-width: 600px;
      text-align: center;
      border-radius: 12px;
      box-shadow: 0 10px 20px rgba(0,0,0,0.2);
      transition: background 0.3s ease;
    }

    .text-block.is-active {
      background-color: #ffe08a;
    }

    h3 {
      margin-top: 0;
      font-size: 1.5rem;
    }

    p {
      font-size: 1rem;
      line-height: 1.5;
    }
  </style>
</head>

<body>
  <div id="scrolly__section">
    <div class="scrolly__chart">
      <iframe scrolling="no" src="https://flo.uri.sh/story/872914/embed#slide-0"></iframe>
    </div>

    <div class="scrolly__content">
      <div class="step" data-step="0">
        <div class="text-block">
          <h3>Étape 1</h3>
          <p>Introduction au graphique : voici le début de notre histoire de données.</p>
        </div>
      </div>
      <div class="step" data-step="1">
        <div class="text-block">
          <h3>Étape 2</h3>
          <p>Deuxième point important de l'analyse illustrée par le graphique.</p>
        </div>
      </div>
      <div class="step" data-step="2">
        <div class="text-block">
          <h3>Étape 3</h3>
          <p>Troisième point clé. On commence à voir des tendances se dessiner.</p>
        </div>
      </div>
      <div class="step" data-step="3">
        <div class="text-block">
          <h3>Étape 4</h3>
          <p>Conclusion ou dernier point, résumé de l’histoire de données.</p>
        </div>
      </div>
    </div>
  </div>

  <script>
    var scrolly = d3.select("#scrolly__section");
    var chart = scrolly.select(".scrolly__chart");
    var content = scrolly.select(".scrolly__content");
    var step = content.selectAll(".step");

    var scroller = scrollama();

    function handleResize() {
      step.style("height", window.innerHeight + "px");
      scroller.resize();
    }

    function handleStepEnter(response) {
      step.select(".text-block").classed("is-active", function(d, i) {
        return i === response.index;
      });

      const linkHead = 'https://flo.uri.sh/story/872914/embed#slide-';
      const slide = response.index;

      d3.select('.scrolly__chart iframe')
        .attr('src', linkHead + slide);
    }

    function init() {
      handleResize();
      scroller
        .setup({
          step: "#scrolly__section .step",
          offset: 0.6,
          debug: false
        })
        .onStepEnter(handleStepEnter);

      window.addEventListener("resize", handleResize);
    }

    init();
  </script>
</body>
</html>
"""

st.components.v1.html(html_code, height=3000, scrolling=True)
