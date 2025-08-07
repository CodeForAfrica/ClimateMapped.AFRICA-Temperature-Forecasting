import streamlit as st

html_code = """
<!doctype html>
<html class="no-js" lang="">
<head>
  <meta charset="utf-8">
  <title>Data story with flourish</title>
  <meta name="viewport" content="width=device-width, initial-scale=1">

  <!-- Bootstrap + Fonts -->
  <link rel="stylesheet" href="https://cdn.jsdelivr.net/npm/bootstrap@4.6.0/dist/css/bootstrap.min.css">
  <link href="https://fonts.googleapis.com/css2?family=Poppins&family=Lora&display=swap" rel="stylesheet">

  <style>
    body {
      font-family: 'Poppins', sans-serif;
      color: #1d1d1d;
    }

    .wrapper {
      padding: 96px 0;
    }

    .scrolly-overlay {
      position: relative;
      width: 100%;
      height: 100vh;
      overflow: hidden;
    }

    .scrolly-overlay iframe {
      position: absolute;
      top: 0;
      left: 0;
      width: 100%;
      height: 100%;
      z-index: 0;
      border: none;
    }

    .steps-container {
      position: relative;
      z-index: 1;
      width: 100%;
      height: 100%;
      display: flex;
      flex-direction: column;
      justify-content: center;
      padding: 2rem;
    }

    .step {
      margin: 2rem auto;
      padding: 1.5rem;
      max-width: 600px;
      background: rgba(255, 255, 255, 0.85);
      border-left: 5px solid #104E8B;
      box-shadow: 0 0 10px rgba(0,0,0,0.1);
    }

    .step.is-active {
      background: goldenrod;
      color: #3b3b3b;
    }
  </style>
</head>

<body>
  <div class="wrapper">
    <div class="container py-5">
      <div class="row justify-content-center">
        <div class="col-lg-8 col-12">
          <p class="mb-4">
            Lorem ipsum dolor sit amet consectetur adipisicing elit. Reprehenderit dolorem iusto, vel, cum est architecto odit quia culpa sed ex ipsa praesentium alias ullam tempore numquam aliquid aspernatur, provident nesciunt!
          </p>
          <img src="https://picsum.photos/640/280" alt="placeholder" width=100% class="mb-4" />
        </div>
      </div>
    </div>

    <div class="scrolly-overlay">
      <iframe id="storyframe" src="https://flo.uri.sh/story/872914/embed#slide-0" scrolling="no"></iframe>

      <div class="steps-container" id="steps">
        <div class="step" data-step="0">Step 1: Lorem ipsum dolor sit amet.</div>
        <div class="step" data-step="1">Step 2: Consectetur adipiscing elit.</div>
        <div class="step" data-step="2">Step 3: Sed do eiusmod tempor incididunt.</div>
        <div class="step" data-step="3">Step 4: Ut labore et dolore magna aliqua.</div>
      </div>
    </div>
  </div>

  <!-- Scripts -->
  <script src="https://d3js.org/d3.v5.min.js"></script>
  <script src="https://unpkg.com/intersection-observer"></script>
  <script src="https://unpkg.com/scrollama"></script>

  <script>
    var scroller = scrollama();
    var steps = d3.selectAll(".step");

    function handleStepEnter(response) {
      steps.classed("is-active", (d, i) => i === response.index);
      var iframe = document.getElementById("storyframe");
      iframe.src = "https://flo.uri.sh/story/872914/embed#slide-" + response.index;
    }

    function handleResize() {
      scroller.resize();
    }

    scroller
      .setup({
        step: ".step",
        offset: 0.5,
        debug: false
      })
      .onStepEnter(handleStepEnter);

    window.addEventListener("resize", handleResize);
  </script>
</body>
</html>

"""

st.components.v1.html(html_code, height=3000, scrolling=True)
