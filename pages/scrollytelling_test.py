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

    /* Chart + text container */
    #scrolly__section {
      position: relative;
      max-width: 900px;
      margin: 0 auto;
      height: 100vh;
    }

    /* Fixed chart on the right */
    .scrolly__chart {
      position: fixed;
      top: 0;
      right: 0;
      width: 60vw;
      height: 100vh;
      z-index: 1;
      background: #fff;
      box-shadow: -5px 0 15px rgba(0,0,0,0.1);
    }

    iframe {
      width: 100%;
      height: 100%;
      border: none;
    }

    /* Scrollable text content */
    .scrolly__content {
        max-width: 100vw;
        margin-left: 0;
        height: auto;
        overflow-y: visible;
        padding: 1rem;
      }
      .step {
        min-height: auto;
      }
    }
    /* Active step */
    .step.is-active {
      background-color: transparent !important;
      box-shadow: none !important;
      filter: none !important;
      backdrop-filter: none !important;
      border-color: goldenrod;
      color: #3b3b3b;
    }

    /* Scrollbar style for scrollable text */
    .scrolly__content::-webkit-scrollbar {
      width: 8px;
    }
    .scrolly__content::-webkit-scrollbar-thumb {
      background-color: rgba(16, 78, 139, 0.5);
      border-radius: 4px;
    }
    .scrolly__content::-webkit-scrollbar-track {
      background: transparent;
    }

    /* Responsive styles for mobile */
    @media (max-width: 768px) {
      .scrolly__chart {
        position: relative;
        width: 100vw;
        height: 50vh;
        box-shadow: none;
      }
    .scrolly__content {
        position: absolute;
        top: 0;
        left: 0;
        width: 100%;
        height: 100vh;
        z-index: 2;
        display: flex;
        align-items: flex-start;  /* top-aligned vertically */
        justify-content: center;  /* center horizontally */
        padding-top: 3rem;        /* space from top */
        box-sizing: border-box;
        pointer-events: none;     /* let clicks through except on steps */
      }
      
      .step {
        pointer-events: auto;     /* allow interaction */
      }
    }

    /* Header styling */
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

    /* Adds space between header and content */
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
          <h3>Premature deaths</h3>
          <p>89% of premature deaths occurred in low- and middle-income countries.</p>
        </div>
        <div class="step" data-step="1">
          <h3>Children deaths</h3>
          <p>Overlay: Over 237 000 deaths of children under the age of 5</p>
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
      // On mobile, steps can have auto height
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
        container: '#scroll-content' // Limit scrollama to scrollable content
      })
      .onStepEnter(handleStepEnter);

      window.addEventListener('resize', handleResize);
    }

    init();
  </script>

</body>
</html>
"""

# Render the HTML in Streamlit
st.components.v1.html(html_code, height=1000, scrolling=True)
