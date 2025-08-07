import streamlit as st

html_code = """
<!doctype html>
<html lang="en">
<head>
  <meta charset="utf-8" />
  <title>Scroll-driven Flourish Story - Text over Chart</title>
  <meta name="viewport" content="width=device-width, initial-scale=1" />

  <link rel="stylesheet" href="https://cdn.jsdelivr.net/npm/bootstrap@4.6.0/dist/css/bootstrap.min.css" crossorigin="anonymous" />

  <style>
    body {
      font-family: 'Poppins', sans-serif;
      margin: 0;
      padding: 0;
      background: #fff;
      color: #1d1d1d;
      overflow-x: hidden;
    }

    #scrolly__section {
      position: relative;
      max-width: 100vw;
      margin: 0 auto;
      height: 100vh;
    }

    .scrolly__chart {
      position: fixed;
      top: 0;
      left: 0;
      width: 100vw;
      height: 100vh;
      z-index: 1;
      background: #fff;
    }

    iframe {
      width: 100%;
      height: 100%;
      border: none;
    }

    .scrolly__content {
      position: absolute;
      top: 0;
      left: 0;
      width: 100%;
      height: 100vh;
      z-index: 2;
      display: flex;
      align-items: flex-start;
      justify-content: center;
      padding-top: 3rem;
      pointer-events: none;
      box-sizing: border-box;
    }

    .step {
      pointer-events: auto;
      max-width: 40vw;
      margin-bottom: 3rem;
      padding: 1rem;
      border: 2px solid #104E8B;
      background: transparent !important;
      cursor: pointer;
      transition: background-color 0.3s, color 0.3s;
      min-height: 70vh;
      display: flex;
      flex-direction: column;
      justify-content: center;
      box-sizing: border-box;
      border-radius: 6px;
      box-shadow: none !important;
      filter: none !important;
      backdrop-filter: none !important;
    }

    .step.is-active {
      border-color: goldenrod;
      color: #3b3b3b;
    }

    @media (max-width: 768px) {
      .scrolly__chart {
        position: relative;
        width: 100vw;
        height: 50vh;
        box-shadow: none;
      }
      .scrolly__content {
        max-width: 100vw;
        margin-left: 0;
        height: auto;
        overflow-y: visible;
        padding: 1rem;
        display: block;
        position: relative;
        pointer-events: auto;
      }
      .step {
        min-height: auto;
        max-width: 100%;
      }
    }

    .app-header {
      background-color: #104E8B;
      color: white;
      font-family: 'Poppins', sans-serif;
      text-align: center;
      padding: 2rem 0;
      margin: 0;
      width: 100vw;
      box-sizing: border-box;
      position: relative;
      z-index: 1000;
      box-shadow: 0 4px 8px rgba(16, 78, 139, 0.3);
    }

    .app-header h1 {
      font-weight: 700;
      font-size: 2.8rem;
      margin-bottom: 0.3rem;
      font-family: 'Lora', serif;
    }

    .app-header h2 {
      font-weight: 400;
      font-size: 1.4rem;
      margin-top: 0;
      margin-bottom: 1rem;
      font-style: italic;
    }

    .app-header hr {
      border: 0;
      height: 1px;
      background: white;
      width: 40%;
      margin: 0 auto 1.5rem auto;
      opacity: 0.7;
    }

    .app-header .intro-text {
      font-size: 1rem;
      font-style: italic;
      max-width: 600px;
      margin: 0 auto;
      line-height: 1.4;
    }

    .wrapper {
      padding-top: 4rem;
    }
  </style>
</head>
<body>

  <header class="app-header">
    <div class="container">
      <h1>Data Scrollytelling</h1>
      <h2>Interactive analysis with Scrollama and Flourish</h2>
      <hr />
      <p class="intro-text">Discover how text and graphics interact harmoniously to tell your story.</p>
    </div>
  </header>

  <div class="wrapper">
    <div id="scrolly__section">

      <div class="scrolly__chart">
        <iframe id="flourish-iframe" src="https://flo.uri.sh/story/872914/embed#slide-0" scrolling="no"></iframe>
      </div>

      <div class="scrolly__content" id="scroll-content">
        <div class="step is-active" data-step="0">
          <h3>Step 1 Title</h3>
          <p>In 2019, 99% of the world’s population was living in places where the WHO air quality guidelines levels were not met. Sadly, women and children bear the greatest health burden, with air pollution being one of the greatest environmental risks to child health.</p>
        </div>
        <div class="step" data-step="1">
          <h3>Step 2 Title</h3>
          <p>Aliquam erat volutpat. Nullam id dolor id nibh ultricies vehicula ut id elit.</p>
        </div>
        <div class="step" data-step="2">
          <h3>Step 3 Title</h3>
          <p>Donec ullamcorper nulla non metus auctor fringilla.</p>
        </div>
        <div class="step" data-step="3">
          <h3>Step 4 Title</h3>
          <p>Maecenas sed diam eget risus varius blandit sit amet non magna.</p>
        </div>
      </div>

    </div>
  </div>

  <script src="https://d3js.org/d3.v5.min.js"></script>
  <script src="https://unpkg.com/scrollama"></script>

  <script>
    var scroller = scrollama();

    function handleResize() {
      var isMobile = window.matchMedia("(max-width: 768px)").matches;
      d3.selectAll('.step')
        .style('min-height', isMobile ? null : window.innerHeight * 0.7 + 'px');
      scroller.resize();
    }

    function handleStepEnter(response) {
      d3.selectAll('.step').classed('is-active', false);
      d3.select(response.element).classed('is-active', true);
      var slideNum = response.index;
      var iframe = document.getElementById('flourish-iframe');
      iframe.src = 'https://flo.uri.sh/story/872914/embed#slide-' + slideNum;
    }

    function init() {
      handleResize();
      scroller.setup({
        step: '.step',
        offset: 0.7,
        debug: false,
        container: '#scroll-content'
      })
      .onStepEnter(handleStepEnter);
      window.addEventListener('resize', handleResize);
    }

    init();
  </script>

</body>
</html>
"""

st.components.v1.html(html_code, height=1000, scrolling=True)
