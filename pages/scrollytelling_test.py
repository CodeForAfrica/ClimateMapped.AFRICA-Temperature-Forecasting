import streamlit as st

html_code = """
<!doctype html>
<html class="no-js" lang="">
<head>
  <meta charset="utf-8">
  <title>Data story with flourish</title>
  <meta http-equiv="X-UA-Compatible" content="IE=edge" />
  <meta name="description" content="how-to-make-a-story">
  <meta name="viewport" content="width=device-width, initial-scale=1">

  <link rel="stylesheet" href="https://cdn.jsdelivr.net/npm/bootstrap@4.6.0/dist/css/bootstrap.min.css">
  <link rel="preconnect" href="https://fonts.gstatic.com">
  <link href="https://fonts.googleapis.com/css2?family=Poppins:wght@300;400;500;600;700&display=swap" rel="stylesheet">
  <link href="https://fonts.googleapis.com/css2?family=Lora:wght@400;600;700&display=swap" rel="stylesheet">

  <style>
    body {
      font-family: 'Poppins', sans-serif;
      margin: 0;
      overflow-x: hidden;
    }

    .wrapper {
      padding: 96px 0;
    }

    .scrolly__section {
      position: relative;
      height: 100vh;
      width: 100vw;
      overflow-x: hidden;
    }

    .scrolly__chart {
      position: fixed;
      top: 0;
      left: 0;
      width: 100vw;
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
      z-index: 1;
      width: 100%;
      max-width: 700px;
      margin: 0 auto;
      padding-top: 100px;
    }

    .step {
      margin: 0 auto 3rem auto;
      padding: 2rem;
      background: rgba(255, 255, 255, 0.8);
      border-radius: 8px;
      box-shadow: 0 0 10px rgba(0, 0, 0, 0.1);
    }

    .text-block.is-active {
      background-color: goldenrod;
    }
  </style>
</head>

<body>
  <div class="wrapper">
    <div class="container py-5">
      <div class="row justify-content-center">
        <div class="col-lg-7 col-11">
          <p class="mb-5">
            Intro: Lorem ipsum dolor sit amet consectetur adipisicing elit. Reprehenderit dolorem iusto...
          </p>
          <img src="https://picsum.photos/640/280" class="mb-5 py-2" width="100%" />
          <h3 class="mb-3">Subtitle</h3>
          <div class="flourish-embed flourish-chart mt-3" data-src="visualisation/6262784"></div>
          <p class="text-center">caption: here is a flourish chart...</p>
        </div>
      </div>
    </div>

    <div id="scrolly" class="scrolly__section">
      <div class="scrolly__chart">
        <iframe src="https://flo.uri.sh/story/872914/embed#slide-0" scrolling="no"></iframe>
      </div>
      <div class="scrolly__content">
        <div class="step" data-step="1">
          <div class="text-block">
            <p>Step 1: Lorem ipsum dolor sit amet consectetur adipisicing elit.</p>
          </div>
        </div>
        <div class="step" data-step="2">
          <div class="text-block">
            <p>Step 2: Lorem ipsum dolor sit amet consectetur adipisicing elit.</p>
          </div>
        </div>
        <div class="step" data-step="3">
          <div class="text-block">
            <p>Step 3: Lorem ipsum dolor sit amet consectetur adipisicing elit.</p>
          </div>
        </div>
        <div class="step" data-step="4">
          <div class="text-block">
            <p>Step 4: Lorem ipsum dolor sit amet consectetur adipisicing elit.</p>
          </div>
        </div>
      </div>
    </div>
  </div>

  <script src="https://d3js.org/d3.v5.min.js"></script>
  <script src="https://unpkg.com/intersection-observer"></script>
  <script src="https://unpkg.com/scrollama"></script>
  <script src="https://public.flourish.studio/resources/embed.js"></script>

  <script>
    var scroller = scrollama();
    var stepSel = d3.selectAll(".step");

    function handleStepEnter(response) {
      stepSel.selectAll(".text-block")
        .classed("is-active", (d, i) => i === response.index);

      const slide = response.index;
      d3.select(".scrolly__chart iframe")
        .attr("src", `https://flo.uri.sh/story/872914/embed#slide-${slide}`);
    }

    function updateProgress(progress) {
      // progress en 0..100
      window.parent.postMessage({streamlitScrollProgress: progress}, '*');
    }
    
    // Par exemple dans handleStepEnter
    const totalSteps = step.size();
    const progressPercent = ((response.index + 1) / totalSteps) * 100;
    updateProgress(progressPercent);

    function handleResize() {
      var stepH = Math.floor(window.innerHeight * 0.8);
      stepSel.style("height", stepH + "px");
      scroller.resize();
    }

    function init() {
      handleResize();
      scroller.setup({
        step: ".step",
        offset: 0.5,
        debug: false
      }).onStepEnter(handleStepEnter);
      window.addEventListener("resize", handleResize);
    }

    init();
  </script>
</body>
</html>
"""

st.components.v1.html(html_code, height=3000, scrolling=True)
