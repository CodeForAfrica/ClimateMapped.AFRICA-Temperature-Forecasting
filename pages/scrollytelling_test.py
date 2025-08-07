import streamlit as st

html_code = """
import streamlit as st

html_code = """
<!doctype html>
<html lang="en">
<head>
  <meta charset="utf-8" />
  <title>Scroll-driven Flourish Story</title>
  <meta name="viewport" content="width=device-width, initial-scale=1" />

  <link rel="stylesheet" href="https://cdn.jsdelivr.net/npm/bootstrap@4.6.0/dist/css/bootstrap.min.css" crossorigin="anonymous" />

  <style>
    body {
      font-family: 'Poppins', sans-serif;
      margin: 0; padding: 0;
      background: #fff;
      color: #1d1d1d;
    }

    #scrolly__section {
      display: flex;
      max-width: 900px;
      margin: 0 auto;
      padding: 2rem 1rem;
    }

    .scrolly__content {
      flex: 1 1 40%;
      margin-right: 2rem;
    }

    .step {
      margin-bottom: 2rem;
      padding: 1rem;
      border: 2px solid #104E8B;
      cursor: pointer;
      transition: background-color 0.3s, color 0.3s;
      min-height: 100vh; /* full viewport height */
      display: flex;
      flex-direction: column;
      justify-content: center;
    }

    .step.is-active {
      background-color: goldenrod;
      color: #3b3b3b;
    }

    .scrolly__chart {
      flex: 1 1 60%;
      position: sticky;
      top: 20px;
      height: 80vh;
    }

    iframe {
      width: 100%;
      height: 100%;
      border: none;
    }

    /* Responsive */
    @media (max-width: 768px) {
      #scrolly__section {
        flex-direction: column;
        padding: 1rem;
      }
      .scrolly__content, .scrolly__chart {
        flex: none;
        width: 100%;
        margin: 0 0 2rem 0;
      }
      .step {
        min-height: auto;
        margin-bottom: 1.5rem;
      }
      .scrolly__chart {
        height: 50vh;
        position: relative;
        top: auto;
      }
    }
  </style>
</head>
<body>

<div id="scrolly__section">
  <div class="scrolly__content">
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

  <div class="scrolly__chart">
    <iframe id="flourish-iframe" src="https://flo.uri.sh/story/872914/embed#slide-0" scrolling="no"></iframe>
  </div>
</div>

<script src="https://d3js.org/d3.v5.min.js"></script>
<script src="https://unpkg.com/scrollama"></script>

<script>
  // Initialize scrollama
  var scroller = scrollama();

  // Setup function to set step heights dynamically (full viewport height)
  function handleResize() {
    var stepHeight = window.innerHeight;
    d3.selectAll('.step').style('min-height', stepHeight + 'px');
    scroller.resize();
  }

  // When a step is entered, update active class and iframe src
  function handleStepEnter(response) {
    // Remove active class from all steps
    d3.selectAll('.step').classed('is-active', false);
    // Add active class to current step
    d3.select(response.element).classed('is-active', true);

    // Update iframe src based on step index
    var slideNum = response.index;
    var iframe = document.getElementById('flourish-iframe');
    iframe.src = 'https://flo.uri.sh/story/872914/embed#slide-' + slideNum;
  }

  // Setup scrollama
  function init() {
    handleResize();

    scroller.setup({
      step: '.step',
      offset: 0.7,
      debug: false,
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
