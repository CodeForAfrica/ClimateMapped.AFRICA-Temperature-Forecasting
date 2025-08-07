import streamlit as st

html_code  = """

<!DOCTYPE html>
<html lang="fr">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Scrollytelling Demo</title>
    <style>
        * {
            margin: 0;
            padding: 0;
            box-sizing: border-box;
        }

        body {
            font-family: 'Arial', sans-serif;
            line-height: 1.6;
            color: #333;
        }

        /* Section d'introduction */
        .hero {
            height: 100vh;
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            display: flex;
            align-items: center;
            justify-content: center;
            color: white;
            text-align: center;
        }

        .hero h1 {
            font-size: 3.5rem;
            margin-bottom: 1rem;
            opacity: 0;
            transform: translateY(50px);
            animation: fadeInUp 1s ease forwards;
        }

        .hero p {
            font-size: 1.3rem;
            opacity: 0;
            transform: translateY(50px);
            animation: fadeInUp 1s ease 0.3s forwards;
        }

        @keyframes fadeInUp {
            to {
                opacity: 1;
                transform: translateY(0);
            }
        }

        /* Container principal pour le scrollytelling */
        .scrolly-container {
            position: relative;
            min-height: 400vh;
        }

        /* Visualisation fixe */
        .sticky-viz {
            position: sticky;
            top: 0;
            height: 100vh;
            display: flex;
            align-items: center;
            justify-content: center;
            background: #f8f9fa;
            overflow: hidden;
        }

        /* Cercle animé */
        .circle {
            width: 200px;
            height: 200px;
            border-radius: 50%;
            background: linear-gradient(45deg, #ff6b6b, #ee5a24);
            transition: all 0.6s ease;
            display: flex;
            align-items: center;
            justify-content: center;
            color: white;
            font-size: 2rem;
            font-weight: bold;
        }

        /* Graphique en barres */
        .bar-chart {
            display: none;
            flex-direction: column;
            gap: 15px;
        }

        .bar {
            height: 30px;
            background: #3742fa;
            border-radius: 15px;
            display: flex;
            align-items: center;
            padding-left: 15px;
            color: white;
            font-weight: bold;
            transform: scaleX(0);
            transform-origin: left;
            transition: transform 0.8s ease;
        }

        .bar.animate {
            transform: scaleX(1);
        }

        .bar:nth-child(1) { width: 300px; }
        .bar:nth-child(2) { width: 250px; }
        .bar:nth-child(3) { width: 180px; }
        .bar:nth-child(4) { width: 320px; }

        /* Texte de narration */
        .narrative {
            position: absolute;
            top: 0;
            left: 0;
            width: 100%;
            pointer-events: none;
        }

        .step {
            height: 100vh;
            display: flex;
            align-items: center;
            padding: 0 50px;
        }

        .step-content {
            background: rgba(255, 255, 255, 0.95);
            padding: 40px;
            border-radius: 15px;
            max-width: 500px;
            box-shadow: 0 20px 40px rgba(0, 0, 0, 0.1);
            opacity: 0.3;
            transform: translateX(-50px);
            transition: all 0.6s ease;
        }

        .step.active .step-content {
            opacity: 1;
            transform: translateX(0);
        }

        .step-content h2 {
            color: #2c3e50;
            margin-bottom: 20px;
            font-size: 2rem;
        }

        .step-content p {
            font-size: 1.1rem;
            line-height: 1.8;
        }

        /* Indicateur de progression */
        .progress-indicator {
            position: fixed;
            top: 50%;
            right: 30px;
            transform: translateY(-50%);
            z-index: 100;
        }

        .progress-dot {
            width: 12px;
            height: 12px;
            border-radius: 50%;
            background: #bdc3c7;
            margin: 15px 0;
            transition: all 0.3s ease;
            cursor: pointer;
        }

        .progress-dot.active {
            background: #3742fa;
            transform: scale(1.3);
        }

        /* Section finale */
        .conclusion {
            height: 100vh;
            background: linear-gradient(135deg, #2c3e50 0%, #34495e 100%);
            display: flex;
            align-items: center;
            justify-content: center;
            color: white;
            text-align: center;
        }

        .conclusion h2 {
            font-size: 2.5rem;
            margin-bottom: 20px;
        }

        /* Responsive */
        @media (max-width: 768px) {
            .hero h1 { font-size: 2.5rem; }
            .step { padding: 0 20px; }
            .step-content { padding: 30px; max-width: 90%; }
            .progress-indicator { right: 15px; }
            .circle { width: 150px; height: 150px; font-size: 1.5rem; }
        }
    </style>
</head>
<body>
    <!-- Section héro -->
    <section class="hero">
        <div>
            <h1>L'Art du Scrollytelling</h1>
            <p>Une histoire racontée par le défilement</p>
        </div>
    </section>

    <!-- Container principal -->
    <div class="scrolly-container">
        <!-- Visualisation sticky -->
        <div class="sticky-viz">
            <!-- Cercle initial -->
            <div class="circle" id="mainViz">
                1
            </div>
            
            <!-- Graphique en barres -->
            <div class="bar-chart" id="barChart">
                <div class="bar">Données A</div>
                <div class="bar">Données B</div>
                <div class="bar">Données C</div>
                <div class="bar">Données D</div>
            </div>
        </div>

        <!-- Texte narratif -->
        <div class="narrative">
            <div class="step" data-step="0">
                <div class="step-content">
                    <h2>Le Début</h2>
                    <p>Tout commence par une simple forme. Cette première étape introduit notre histoire et capture l'attention du lecteur.</p>
                </div>
            </div>

            <div class="step" data-step="1">
                <div class="step-content">
                    <h2>La Transformation</h2>
                    <p>Observez comme notre forme évolue. Les couleurs changent, la taille grandit, créant un sentiment de progression.</p>
                </div>
            </div>

            <div class="step" data-step="2">
                <div class="step-content">
                    <h2>L'Évolution</h2>
                    <p>Notre cercle continue de se transformer, adoptant de nouvelles couleurs et une forme différente pour illustrer le changement.</p>
                </div>
            </div>

            <div class="step" data-step="3">
                <div class="step-content">
                    <h2>Les Données</h2>
                    <p>Maintenant, révélons les données cachées derrière cette histoire. Le graphique montre la progression réelle.</p>
                </div>
            </div>
        </div>
    </div>

    <!-- Indicateur de progression -->
    <div class="progress-indicator">
        <div class="progress-dot active" data-step="0"></div>
        <div class="progress-dot" data-step="1"></div>
        <div class="progress-dot" data-step="2"></div>
        <div class="progress-dot" data-step="3"></div>
    </div>

    <!-- Section finale -->
    <section class="conclusion">
        <div>
            <h2>Fin de l'Histoire</h2>
            <p>Le scrollytelling permet de créer des expériences narratives immersives et engageantes.</p>
        </div>
    </section>

    <script>
        // Configuration
        const steps = document.querySelectorAll('.step');
        const progressDots = document.querySelectorAll('.progress-dot');
        const mainViz = document.getElementById('mainViz');
        const barChart = document.getElementById('barChart');
        let currentStep = 0;

        // Configuration des étapes
        const stepConfigs = {
            0: {
                circle: { size: 200, color: 'linear-gradient(45deg, #ff6b6b, #ee5a24)', text: '1' },
                showChart: false
            },
            1: {
                circle: { size: 250, color: 'linear-gradient(45deg, #4834d4, #686de0)', text: '2' },
                showChart: false
            },
            2: {
                circle: { size: 300, color: 'linear-gradient(45deg, #00d2d3, #54a0ff)', text: '3' },
                showChart: false
            },
            3: {
                circle: { size: 0, color: '', text: '' },
                showChart: true
            }
        };

        // Fonction pour mettre à jour la visualisation
        function updateVisualization(stepIndex) {
            const config = stepConfigs[stepIndex];
            
            if (config.showChart) {
                mainViz.style.display = 'none';
                barChart.style.display = 'flex';
                
                // Animer les barres avec un délai
                setTimeout(() => {
                    document.querySelectorAll('.bar').forEach((bar, index) => {
                        setTimeout(() => {
                            bar.classList.add('animate');
                        }, index * 200);
                    });
                }, 300);
            } else {
                mainViz.style.display = 'flex';
                barChart.style.display = 'none';
                
                // Réinitialiser les barres
                document.querySelectorAll('.bar').forEach(bar => {
                    bar.classList.remove('animate');
                });
                
                // Mettre à jour le cercle
                mainViz.style.width = config.circle.size + 'px';
                mainViz.style.height = config.circle.size + 'px';
                mainViz.style.background = config.circle.color;
                mainViz.textContent = config.circle.text;
            }
        }

        // Fonction pour activer une étape
        function activateStep(stepIndex) {
            if (stepIndex === currentStep) return;
            
            // Désactiver l'étape actuelle
            steps[currentStep].classList.remove('active');
            progressDots[currentStep].classList.remove('active');
            
            // Activer la nouvelle étape
            currentStep = stepIndex;
            steps[currentStep].classList.add('active');
            progressDots[currentStep].classList.add('active');
            
            // Mettre à jour la visualisation
            updateVisualization(currentStep);
        }

        // Observer d'intersection pour détecter les étapes visibles
        const observerOptions = {
            root: null,
            rootMargin: '-40% 0px -40% 0px',
            threshold: 0
        };

        const observer = new IntersectionObserver((entries) => {
            entries.forEach(entry => {
                if (entry.isIntersecting) {
                    const stepIndex = parseInt(entry.target.dataset.step);
                    activateStep(stepIndex);
                }
            });
        }, observerOptions);

        // Observer chaque étape
        steps.forEach(step => {
            observer.observe(step);
        });

        // Gestion des clics sur les indicateurs de progression
        progressDots.forEach(dot => {
            dot.addEventListener('click', () => {
                const stepIndex = parseInt(dot.dataset.step);
                steps[stepIndex].scrollIntoView({
                    behavior: 'smooth',
                    block: 'center'
                });
            });
        });

        // Initialisation
        activateStep(0);

        // Animation de défilement fluide
        let ticking = false;
        
        function updateOnScroll() {
            // Ici vous pouvez ajouter d'autres animations basées sur le scroll
            ticking = false;
        }

        window.addEventListener('scroll', () => {
            if (!ticking) {
                requestAnimationFrame(updateOnScroll);
                ticking = true;
            }
        });
    </script>
</body>
</html>

"""

st.components.v1.html(html_code, height=3000, scrolling=True)
