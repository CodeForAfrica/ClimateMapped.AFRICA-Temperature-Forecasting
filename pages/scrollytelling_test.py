import streamlit as st

html_code = """

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
            overflow-x: hidden;
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
            position: relative;
        }

        .hero-content {
            transform: translateY(100px);
            opacity: 0;
            animation: heroFadeIn 1.5s ease forwards;
        }

        .hero h1 {
            font-size: 3.5rem;
            margin-bottom: 1rem;
            transform: translateY(50px);
            opacity: 0;
            animation: slideInUp 1s ease 0.5s forwards;
        }

        .hero p {
            font-size: 1.3rem;
            transform: translateY(30px);
            opacity: 0;
            animation: slideInUp 1s ease 1s forwards;
        }

        .scroll-indicator {
            position: absolute;
            bottom: 30px;
            left: 50%;
            transform: translateX(-50%);
            color: white;
            animation: bounce 2s infinite;
        }

        @keyframes heroFadeIn {
            to { transform: translateY(0); opacity: 1; }
        }

        @keyframes slideInUp {
            to { opacity: 1; transform: translateY(0); }
        }

        @keyframes bounce {
            0%, 20%, 50%, 80%, 100% { transform: translateX(-50%) translateY(0); }
            40% { transform: translateX(-50%) translateY(-10px); }
            60% { transform: translateX(-50%) translateY(-5px); }
        }

        /* Container principal pour le scrollytelling */
        .scrolly-container {
            position: relative;
            min-height: 500vh;
        }

        /* Visualisation fixe */
        .sticky-viz {
            position: sticky;
            top: 0;
            height: 100vh;
            display: flex;
            align-items: center;
            justify-content: center;
            background: linear-gradient(45deg, #f8f9fa, #e9ecef);
            overflow: hidden;
            z-index: 1;
        }

        /* Cercle animé amélioré */
        .circle {
            width: 200px;
            height: 200px;
            border-radius: 50%;
            background: linear-gradient(45deg, #ff6b6b, #ee5a24);
            transition: all 0.8s cubic-bezier(0.4, 0, 0.2, 1);
            display: flex;
            align-items: center;
            justify-content: center;
            color: white;
            font-size: 2rem;
            font-weight: bold;
            box-shadow: 0 10px 30px rgba(0,0,0,0.2);
            position: relative;
        }

        .circle::before {
            content: '';
            position: absolute;
            width: 100%;
            height: 100%;
            border-radius: 50%;
            background: inherit;
            opacity: 0.3;
            transform: scale(1.2);
            animation: pulse 2s infinite;
        }

        @keyframes pulse {
            0% { transform: scale(1.2); opacity: 0.3; }
            50% { transform: scale(1.4); opacity: 0.1; }
            100% { transform: scale(1.2); opacity: 0.3; }
        }

        /* Graphique en barres amélioré */
        .bar-chart {
            display: none;
            flex-direction: column;
            gap: 20px;
            padding: 40px;
            background: white;
            border-radius: 20px;
            box-shadow: 0 20px 40px rgba(0,0,0,0.1);
        }

        .bar {
            height: 40px;
            background: linear-gradient(90deg, #3742fa, #5352ed);
            border-radius: 20px;
            display: flex;
            align-items: center;
            padding-left: 20px;
            color: white;
            font-weight: bold;
            transform: scaleX(0);
            transform-origin: left;
            transition: transform 1.2s cubic-bezier(0.4, 0, 0.2, 1);
            position: relative;
            overflow: hidden;
        }

        .bar::before {
            content: '';
            position: absolute;
            top: 0;
            left: -100%;
            width: 100%;
            height: 100%;
            background: linear-gradient(90deg, transparent, rgba(255,255,255,0.3), transparent);
            transition: left 0.8s;
        }

        .bar.animate {
            transform: scaleX(1);
        }

        .bar.animate::before {
            left: 100%;
        }

        .bar:nth-child(1) { width: 350px; transition-delay: 0s; }
        .bar:nth-child(2) { width: 280px; transition-delay: 0.2s; }
        .bar:nth-child(3) { width: 220px; transition-delay: 0.4s; }
        .bar:nth-child(4) { width: 400px; transition-delay: 0.6s; }

        /* Texte de narration amélioré */
        .narrative {
            position: absolute;
            top: 0;
            left: 0;
            width: 100%;
            pointer-events: none;
            z-index: 10;
        }

        .step {
            height: 120vh;
            display: flex;
            align-items: center;
            padding: 0 50px;
        }

        .step-content {
            background: rgba(255, 255, 255, 0.98);
            padding: 50px;
            border-radius: 20px;
            max-width: 550px;
            box-shadow: 0 30px 60px rgba(0, 0, 0, 0.15);
            opacity: 0;
            transform: translateX(-100px) scale(0.9);
            transition: all 0.8s cubic-bezier(0.4, 0, 0.2, 1);
            backdrop-filter: blur(10px);
            border: 1px solid rgba(255, 255, 255, 0.2);
        }

        .step.active .step-content {
            opacity: 1;
            transform: translateX(0) scale(1);
        }

        .step-content h2 {
            color: #2c3e50;
            margin-bottom: 25px;
            font-size: 2.2rem;
            transform: translateY(20px);
            opacity: 0;
            transition: all 0.6s ease 0.3s;
        }

        .step.active .step-content h2 {
            transform: translateY(0);
            opacity: 1;
        }

        .step-content p {
            font-size: 1.2rem;
            line-height: 1.8;
            color: #555;
            transform: translateY(20px);
            opacity: 0;
            transition: all 0.6s ease 0.5s;
        }

        .step.active .step-content p {
            transform: translateY(0);
            opacity: 1;
        }

        /* Effet de typing pour le texte */
        .typing-effect {
            overflow: hidden;
            white-space: nowrap;
            border-right: 2px solid #3742fa;
            animation: typing 2s steps(40) 1s forwards, blink 1s infinite;
        }

        @keyframes typing {
            from { width: 0; }
            to { width: 100%; }
        }

        @keyframes blink {
            0%, 50% { border-color: #3742fa; }
            51%, 100% { border-color: transparent; }
        }

        /* Indicateur de progression amélioré */
        .progress-indicator {
            position: fixed;
            top: 50%;
            right: 40px;
            transform: translateY(-50%);
            z-index: 100;
            background: rgba(255, 255, 255, 0.9);
            padding: 20px 10px;
            border-radius: 25px;
            box-shadow: 0 10px 30px rgba(0,0,0,0.1);
            backdrop-filter: blur(10px);
        }

        .progress-dot {
            width: 14px;
            height: 14px;
            border-radius: 50%;
            background: #bdc3c7;
            margin: 20px 0;
            transition: all 0.4s cubic-bezier(0.4, 0, 0.2, 1);
            cursor: pointer;
            position: relative;
        }

        .progress-dot::before {
            content: '';
            position: absolute;
            width: 30px;
            height: 30px;
            border-radius: 50%;
            background: rgba(55, 66, 250, 0.2);
            top: 50%;
            left: 50%;
            transform: translate(-50%, -50%) scale(0);
            transition: transform 0.3s ease;
        }

        .progress-dot:hover::before {
            transform: translate(-50%, -50%) scale(1);
        }

        .progress-dot.active {
            background: #3742fa;
            transform: scale(1.4);
            box-shadow: 0 0 20px rgba(55, 66, 250, 0.5);
        }

        /* Section finale améliorée */
        .conclusion {
            height: 100vh;
            background: linear-gradient(135deg, #2c3e50 0%, #34495e 100%);
            display: flex;
            align-items: center;
            justify-content: center;
            color: white;
            text-align: center;
            position: relative;
        }

        .conclusion-content {
            transform: translateY(50px);
            opacity: 0;
            animation: fadeInUp 1s ease forwards;
        }

        .conclusion h2 {
            font-size: 3rem;
            margin-bottom: 30px;
            background: linear-gradient(45deg, #ff6b6b, #4ecdc4);
            -webkit-background-clip: text;
            -webkit-text-fill-color: transparent;
            background-clip: text;
        }

        .conclusion p {
            font-size: 1.4rem;
            opacity: 0.9;
        }

        @keyframes fadeInUp {
            to { transform: translateY(0); opacity: 1; }
        }

        /* Particules flottantes */
        .floating-particles {
            position: absolute;
            width: 100%;
            height: 100%;
            overflow: hidden;
            z-index: 0;
        }

        .particle {
            position: absolute;
            width: 4px;
            height: 4px;
            background: rgba(55, 66, 250, 0.6);
            border-radius: 50%;
            animation: float 6s infinite linear;
        }

        @keyframes float {
            0% { transform: translateY(100vh) rotate(0deg); opacity: 0; }
            10% { opacity: 1; }
            90% { opacity: 1; }
            100% { transform: translateY(-100px) rotate(360deg); opacity: 0; }
        }

        /* Responsive amélioré */
        @media (max-width: 768px) {
            .hero h1 { font-size: 2.8rem; }
            .step { padding: 0 25px; }
            .step-content { 
                padding: 35px; 
                max-width: 95%; 
                margin: 0 auto;
            }
            .progress-indicator { right: 20px; }
            .circle { width: 160px; height: 160px; font-size: 1.6rem; }
            .bar-chart { padding: 30px 20px; }
            .conclusion h2 { font-size: 2.2rem; }
        }
    </style>
</head>
<body>
    <!-- Section héro -->
    <section class="hero">
        <div class="hero-content">
            <h1>L'Art du Scrollytelling</h1>
            <p>Une histoire racontée par le défilement</p>
        </div>
        <div class="scroll-indicator">
            <div>↓ Faites défiler pour découvrir l'histoire</div>
        </div>
    </section>

    <!-- Container principal -->
    <div class="scrolly-container">
        <!-- Particules flottantes -->
        <div class="floating-particles" id="particles"></div>
        
        <!-- Visualisation sticky -->
        <div class="sticky-viz">
            <!-- Cercle initial -->
            <div class="circle" id="mainViz">
                1
            </div>
            
            <!-- Graphique en barres -->
            <div class="bar-chart" id="barChart">
                <div class="bar">Croissance 2024: +180%</div>
                <div class="bar">Nouveaux clients: +145%</div>
                <div class="bar">Satisfaction: +95%</div>
                <div class="bar">Revenue global: +220%</div>
            </div>
        </div>

        <!-- Texte narratif -->
        <div class="narrative">
            <div class="step" data-step="0">
                <div class="step-content">
                    <h2>Le Commencement</h2>
                    <p>Tout commence par une vision simple mais puissante. Cette première étape marque le début d'une transformation remarquable qui va bouleverser notre compréhension des données.</p>
                </div>
            </div>

            <div class="step" data-step="1">
                <div class="step-content">
                    <h2>La Métamorphose</h2>
                    <p>Observez attentivement cette évolution spectaculaire. Les couleurs se transforment, la forme grandit, symbolisant une croissance organique et naturelle qui dépasse toutes nos attentes initiales.</p>
                </div>
            </div>

            <div class="step" data-step="2">
                <div class="step-content">
                    <h2>L'Épanouissement</h2>
                    <p>Notre cercle continue sa mutation fascinante, adoptant de nouvelles teintes vibrantes et une dimension impressionnante. Cette phase illustre parfaitement l'accélération du processus de changement.</p>
                </div>
            </div>

            <div class="step" data-step="3">
                <div class="step-content">
                    <h2>La Révélation</h2>
                    <p>Et voici le moment tant attendu ! Les données cachées se dévoilent enfin à travers ce graphique dynamique, révélant la véritable ampleur de cette transformation extraordinaire.</p>
                </div>
            </div>
        </div>
    </div>

    <!-- Indicateur de progression -->
    <div class="progress-indicator">
        <div class="progress-dot active" data-step="0" title="Le Commencement"></div>
        <div class="progress-dot" data-step="1" title="La Métamorphose"></div>
        <div class="progress-dot" data-step="2" title="L'Épanouissement"></div>
        <div class="progress-dot" data-step="3" title="La Révélation"></div>
    </div>

    <!-- Section finale -->
    <section class="conclusion">
        <div class="conclusion-content">
            <h2>Fin de l'Aventure</h2>
            <p>Le scrollytelling révèle la magie de la narration interactive, transformant de simples données en expériences mémorables et engageantes.</p>
        </div>
    </section>

    <script>
        // Configuration
        const steps = document.querySelectorAll('.step');
        const progressDots = document.querySelectorAll('.progress-dot');
        const mainViz = document.getElementById('mainViz');
        const barChart = document.getElementById('barChart');
        let currentStep = -1;

        // Configuration des étapes avec plus de variété
        const stepConfigs = {
            0: {
                circle: { 
                    size: 200, 
                    color: 'linear-gradient(45deg, #ff6b6b, #ee5a24)', 
                    text: '1' 
                },
                showChart: false
            },
            1: {
                circle: { 
                    size: 280, 
                    color: 'linear-gradient(45deg, #4834d4, #686de0)', 
                    text: '2' 
                },
                showChart: false
            },
            2: {
                circle: { 
                    size: 360, 
                    color: 'linear-gradient(45deg, #00d2d3, #54a0ff)', 
                    text: '3' 
                },
                showChart: false
            },
            3: {
                circle: { size: 0, color: '', text: '' },
                showChart: true
            }
        };

        // Créer des particules flottantes
        function createParticles() {
            const particlesContainer = document.getElementById('particles');
            const particleCount = 15;

            for (let i = 0; i < particleCount; i++) {
                const particle = document.createElement('div');
                particle.className = 'particle';
                particle.style.left = Math.random() * 100 + '%';
                particle.style.animationDelay = Math.random() * 6 + 's';
                particle.style.animationDuration = (4 + Math.random() * 4) + 's';
                particlesContainer.appendChild(particle);
            }
        }

        // Fonction pour mettre à jour la visualisation avec animations fluides
        function updateVisualization(stepIndex) {
            const config = stepConfigs[stepIndex];
            
            if (config.showChart) {
                // Animation de sortie du cercle
                mainViz.style.transform = 'scale(0) rotate(180deg)';
                mainViz.style.opacity = '0';
                
                setTimeout(() => {
                    mainViz.style.display = 'none';
                    barChart.style.display = 'flex';
                    barChart.style.transform = 'scale(0)';
                    barChart.style.opacity = '0';
                    
                    // Animation d'entrée du graphique
                    setTimeout(() => {
                        barChart.style.transform = 'scale(1)';
                        barChart.style.opacity = '1';
                        barChart.style.transition = 'all 0.8s cubic-bezier(0.4, 0, 0.2, 1)';
                        
                        // Animer les barres avec des délais progressifs
                        setTimeout(() => {
                            document.querySelectorAll('.bar').forEach((bar, index) => {
                                setTimeout(() => {
                                    bar.classList.add('animate');
                                }, index * 300);
                            });
                        }, 500);
                    }, 100);
                }, 400);
                
            } else {
                // Réinitialiser le graphique
                barChart.style.transform = 'scale(0)';
                barChart.style.opacity = '0';
                
                setTimeout(() => {
                    barChart.style.display = 'none';
                    document.querySelectorAll('.bar').forEach(bar => {
                        bar.classList.remove('animate');
                    });
                    
                    // Afficher et animer le cercle
                    mainViz.style.display = 'flex';
                    mainViz.style.transform = 'scale(0) rotate(-180deg)';
                    mainViz.style.opacity = '0';
                    
                    setTimeout(() => {
                        mainViz.style.width = config.circle.size + 'px';
                        mainViz.style.height = config.circle.size + 'px';
                        mainViz.style.background = config.circle.color;
                        mainViz.textContent = config.circle.text;
                        mainViz.style.transform = 'scale(1) rotate(0deg)';
                        mainViz.style.opacity = '1';
                        mainViz.style.transition = 'all 0.8s cubic-bezier(0.4, 0, 0.2, 1)';
                    }, 100);
                }, 300);
            }
        }

        // Fonction pour activer une étape avec animations améliorées
        function activateStep(stepIndex) {
            if (stepIndex === currentStep) return;
            
            // Désactiver l'étape actuelle
            if (currentStep >= 0) {
                steps[currentStep].classList.remove('active');
                progressDots[currentStep].classList.remove('active');
            }
            
            // Activer la nouvelle étape avec délai pour l'effet
            currentStep = stepIndex;
            
            setTimeout(() => {
                steps[currentStep].classList.add('active');
                progressDots[currentStep].classList.add('active');
            }, 200);
            
            // Mettre à jour la visualisation
            updateVisualization(currentStep);
        }

        // Observer d'intersection amélioré
        const observerOptions = {
            root: null,
            rootMargin: '-30% 0px -50% 0px',
            threshold: [0, 0.5, 1]
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

        // Gestion améliorée des clics sur les indicateurs
        progressDots.forEach((dot, index) => {
            dot.addEventListener('click', (e) => {
                e.preventDefault();
                const stepIndex = parseInt(dot.dataset.step);
                steps[stepIndex].scrollIntoView({
                    behavior: 'smooth',
                    block: 'center'
                });
            });
            
            // Ajouter des tooltips
            dot.addEventListener('mouseenter', function() {
                const tooltip = this.getAttribute('title');
                // Logique tooltip si nécessaire
            });
        });

        // Animation de scroll fluide avec parallax subtil
        let ticking = false;
        
        function updateOnScroll() {
            const scrollPercent = window.pageYOffset / (document.documentElement.scrollHeight - window.innerHeight);
            
            // Effet parallax léger sur les particules
            const particles = document.querySelectorAll('.particle');
            particles.forEach((particle, index) => {
                const speed = 0.5 + (index % 3) * 0.2;
                particle.style.transform = `translateY(${scrollPercent * 100 * speed}px)`;
            });
            
            ticking = false;
        }

        window.addEventListener('scroll', () => {
            if (!ticking) {
                requestAnimationFrame(updateOnScroll);
                ticking = true;
            }
        });

        // Initialisation
        document.addEventListener('DOMContentLoaded', () => {
            createParticles();
            
            // Animation initiale retardée
            setTimeout(() => {
                if (steps.length > 0) {
                    activateStep(0);
                }
            }, 1000);
        });

        // Gestion du redimensionnement
        window.addEventListener('resize', () => {
            // Réajuster si nécessaire
        });
    </script>
</body>
</html>

"""

st.components.v1.html(html_code, height=3000, scrolling=True)
