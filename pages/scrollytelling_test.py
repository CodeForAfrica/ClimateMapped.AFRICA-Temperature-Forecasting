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
      margin: 0; padding: 0;
      background: #fff;
      color: #1d1d1d;
      overflow-x: hidden;
    }

    #scrolly__section {
      position: relative;
      max-width: 900px;
      margin: 0 auto;
      height: 100vh;
    }

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

    .scrolly__content {
      position: relative;
      width: 100%;
      max-width: 40vw;
      margin-left: 2rem;
      padding-top: 2rem;
      z-index: 2;
      overflow-y: auto;
      height: 100vh;
    }

    .step {
      margin-bottom: 3rem;
      padding: 1rem;
      border: 2px solid #104E8B;
      background: rgba(255 255 255 / 0.85);
      cursor: pointer;
      transition: background-color 0.3s, color 0.3s;
      min-height: 70vh;
      display: flex;
      flex-direction: column;
      justify-content: center;
      box-sizing: border-box;
      border-radius: 6px;
      backdrop-filter: saturate(180%) blur(10px);
    }

    .step.is-active {
    background-color: transparent !important;
    box-shadow: none !important;
    filter: none !important;
    backdrop-filter: none !important;
    border-color: goldenrod;
    color: #3b3b3b;
    }

    /* Scrollbar styling for content */
    .scrolly__content::-webkit-scrollbar {
      width: 8px;
    }
    .scrolly__content::-webkit-scrollbar-thumb {
      background-color: rgba(16,78,139,0.5);
      border-radius: 4px;
    }
    .scrolly__content::-webkit-scrollbar-track {
      background: transparent;
    }

    /* Responsive */
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
      }
      .step {
        min-height: auto;
      }
    }
  </style>
</head>
<body>

<div id="scrolly__section">

  <div class="scrolly__chart">
    <iframe id="flourish-iframe" src="https://flo.uri.sh/story/872914/embed#slide-0" scrolling="no"></iframe>
  </div>

  <div class="scrolly__content" id="scroll-content">
    <div class="step is-active" data-step="0">
      <h3>Step 1 Title</h3>
      <p>Lorem ipsum dolor sit amet, consectetur adipiscing elit. Curabitur at suscipit sapien.</p>
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

<script src="https://d3js.org/d3.v5.min.js"></script>
<script src="https://unpkg.com/scrollama"></script>

<script>
  var scroller = scrollama();

  function handleResize() {
    // on mobile, let steps have auto height
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
      container: '#scroll-content'  // important: limit scrollama to the scroll container
    })
    .onStepEnter(handleStepEnter);

    window.addEventListener('resize', handleResize);
  }

  init();
</script>

</body>
</html>
"""

st.components.v1.html(html_code, height=900, scrolling=True)


st.components.v1.html(html_code, height=900, scrolling=True)
