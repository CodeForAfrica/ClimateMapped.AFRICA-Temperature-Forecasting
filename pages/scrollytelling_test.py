import streamlit as st

html_code = """
<!doctype html>
<html lang="fr">
<head>
  <meta charset="utf-8">
  <title>Data story with Flourish</title>
  <meta name="viewport" content="width=device-width, initial-scale=1">

  <!-- CSS + Bootstrap + Fonts -->
  <link rel="stylesheet" href="https://cdn.jsdelivr.net/npm/bootstrap@4.6.0/dist/css/bootstrap.min.css">
  <link href="https://fonts.googleapis.com/css2?family=Poppins:wght@300;400;600&family=Lora:wght@400;700&display=swap" rel="stylesheet">

  <style>
    body {
      font-family: 'Poppins', sans-serif;
      margin: 0;
      padding: 0;
    }

    .wrapper {
      padding: 96px 0;
    }

    .text-block.is-active {
      background-color: rgba(255, 223, 100, 0.95);
    }

    /* Section Scrollytelling */
    #scrolly__section {
      position: relative;
      width: 100%;
      height: 100vh;
      overflow-x: hidden;
    }

    .scrolly__chart {
      position: fixed;
      top: 0;
      left: 0;
      width: 100%;
      height: 100vh;
      z-index: 0;
    }

    .scrolly__chart iframe {
      width: 100%;
      height: 100%;
      border: none;
    }

    .scrolly__content {
      position: relative;
      z-index: 10;
      width: 100%;
    }

    .step {
      height: 100vh;
      display: flex;
      align-items: center;
      justify-content: center;
      padding: 2rem;
    }

    .text-block {
      background-color: rgba(255, 255, 255, 0.9);
      padding: 2rem;
      max-width: 700px;
      text-align: center;
      border-radius: 12px;
      box-shadow: 0 0 20px rgba(0,0,0,0.15);
    }

    /* Responsive tweaks */
    @media (max-width: 768px) {
      .text-block {
        padding: 1.5rem;
      }
    }
  </style>
</head>

<body>
  <div class="wrapper">
    <div class="container py-5">
      <div class="row justify-content-center">
        <div class="col-lg-7 col-11">
          <p class="mb-5">
            Lorem ipsum dolor sit amet consectetur adipisicing elit. Reprehenderit dolorem iusto, vel, cum est architecto odit quia culpa sed ex ipsa praesentium alias ullam tempore numquam aliquid aspernatur, provident nesciunt!
          </p>

          <img src="https://picsum.photos/640/280" alt="placeholder" width="100%" class="mb-5 py-2" />

          <h3 class="mb-3">Sous-titre ici</h3>

          <div class="flourish-embed flourish-chart mt-3" data-src="visualisation/6262784"></div>
          <p class="text-center">caption: voici un graphique Flourish intégré via embed.</p>

          <p class="mb-4">
            Lorem ipsum dolor sit amet consectetur adipisicing elit. Facilis aut, cum reprehenderit obcaecati minima eius aperiam dolorem laboriosam ullam facere eaque earum voluptatibus, doloremque officiis quibusdam quae impedit ipsa sunt.
          </p>

          <hr class="my-5" />
          <p class="blockquote font-italic text-center">“Block quote example”</p>
          <hr class="my-5" />

          <p class="mb-5">
            Lorem ipsum dolor sit amet consectetur adipisicing elit. Ullam architecto obcaecati alias delectus, illo non nam ad, accusamus magnam <em>italique ici</em> <a href="#" target="_blank">lien ici</a> ipsa accusantium ratione praesentium dolores nesciunt ab officia quisquam excepturi sunt?
          </p>

          <img src="https://picsum.photos/640/280" alt="placeholder" width="100%" class="mb-5 py-2" />

          <h3 class="mb-3">Sous-titre ici</h3>

          <p class="mb-4">
            Lorem, ipsum dolor sit amet consectetur adipisicing elit. Error dolor, quos aut repellendus quia porro temporibus magni unde, rerum quasi aperiam, eligendi ducimus aliquam fugiat quas autem labore id consectetur.
          </p>
        </div>
      </div>
    </div>
  </div>

  <!-- ✅ SCROLLYTELLING SECTION -->
  <div id="scrolly__section">
    <div class="scrolly__chart">
      <iframe scrolling="no" src="https://flo.uri.sh/story/872914/embed#slide-0"></iframe>
    </div>

    <div class="scrolly__content">
      <div class="step" data-step="0">
        <div class="text-block">
          <h3>Slide 1</h3>
          <p>Introduction au graphique. Ce que vous voyez ici est le début de l'histoire.</p>
        </div>
      </div>
      <div class="step" data-step="1">
        <div class="text-block">
          <h3>Slide 2</h3>
          <p>Un deuxième fait important illustré par cette slide du graphique.</p>
        </div>
      </div>
      <div class="step" data-step="2">
        <div class="text-block">
          <h3>Slide 3</h3>
          <p>Une troisième partie du récit, toujours synchronisée avec le graphique.</p>
        </div>
      </div>
      <div class="step" data-step="3">
        <div class="text-block">
          <h3>Slide 4</h3>
          <p>Dernière partie de l'analyse. Synthèse ou appel à l'action.</p>
        </div>
      </div>
    </div>
  </div>

  <!-- JS: Scrollama + Flourish -->
  <script src="https://unpkg.com/d3@5.9.1/dist/d3.min.js"></script>
  <script src="https://unpkg.com/scrollama"></script>
  <script src="https://public.flourish.studio/resources/embed.js"></script>

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
      step.selectAll(".text-block")
          .classed("is-active", (d, i) => i === response.index);

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
