import streamlit as st
import plotly.graph_objects as go
import plotly.express as px
import pandas as pd
import time

# Configuration de la page
st.set_page_config(
    page_title="Scrollytelling avec Streamlit",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# CSS personnalisé pour améliorer l'apparence
st.markdown("""
<style>
    .main-header {
        text-align: center;
        padding: 50px 0;
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        color: white;
        margin: -1rem -1rem 2rem -1rem;
        border-radius: 0 0 20px 20px;
    }
    
    .step-section {
        padding: 40px 20px;
        margin: 30px 0;
        border-radius: 15px;
        background: #f8f9fa;
        border-left: 5px solid #3742fa;
    }
    
    .metric-card {
        background: white;
        padding: 20px;
        border-radius: 10px;
        box-shadow: 0 2px 10px rgba(0,0,0,0.1);
        text-align: center;
        margin: 10px;
    }
</style>
""", unsafe_allow_html=True)

# En-tête principal
st.markdown("""
<div class="main-header">
    <h1>L'Art du Scrollytelling</h1>
    <h3>Une histoire racontée avec Streamlit</h3>
</div>
""", unsafe_allow_html=True)

# Étape 1 : Introduction
st.markdown('<div class="step-section">', unsafe_allow_html=True)
col1, col2 = st.columns([1, 2])

with col1:
    st.markdown("## 🚀 Étape 1: Le Début")
    st.write("""
    Notre histoire commence par quelques données simples. 
    Observez ce premier graphique qui montre l'évolution 
    de nos métriques de base.
    """)

with col2:
    # Graphique simple - étape 1
    data1 = pd.DataFrame({
        'Mois': ['Jan', 'Fév', 'Mar', 'Avr'],
        'Ventes': [100, 120, 140, 180]
    })
    
    fig1 = px.bar(data1, x='Mois', y='Ventes', 
                  color='Ventes', 
                  color_continuous_scale='Blues',
                  title="Ventes par Mois - Phase 1")
    fig1.update_layout(showlegend=False, height=400)
    st.plotly_chart(fig1, use_container_width=True)

st.markdown('</div>', unsafe_allow_html=True)

# Séparateur visuel
st.markdown("---")

# Étape 2 : Évolution
st.markdown('<div class="step-section">', unsafe_allow_html=True)
col1, col2 = st.columns([2, 1])

with col1:
    # Graphique évolutif - étape 2
    data2 = pd.DataFrame({
        'Mois': ['Jan', 'Fév', 'Mar', 'Avr', 'Mai', 'Juin'],
        'Ventes': [100, 120, 140, 180, 220, 280],
        'Prévisions': [110, 125, 135, 170, 210, 250]
    })
    
    fig2 = go.Figure()
    fig2.add_trace(go.Scatter(x=data2['Mois'], y=data2['Ventes'], 
                             mode='lines+markers', name='Ventes Réelles',
                             line=dict(color='#3742fa', width=4)))
    fig2.add_trace(go.Scatter(x=data2['Mois'], y=data2['Prévisions'], 
                             mode='lines+markers', name='Prévisions',
                             line=dict(color='#ff6b6b', width=4, dash='dash')))
    
    fig2.update_layout(title="Évolution Complète - Réel vs Prévisions",
                      height=400)
    st.plotly_chart(fig2, use_container_width=True)

with col2:
    st.markdown("## 📈 Étape 2: La Croissance")
    st.write("""
    Maintenant nous voyons l'image complète ! 
    La croissance dépasse nos prévisions initiales.
    """)
    
    # Métriques interactives
    st.metric("Croissance totale", "180%", "50%")
    st.metric("Dépassement prévision", "+12%", "2%")

st.markdown('</div>', unsafe_allow_html=True)

# Séparateur
st.markdown("---")

# Étape 3 : Analyse détaillée
st.markdown('<div class="step-section">', unsafe_allow_html=True)
st.markdown("## 🔍 Étape 3: Analyse Approfondie")

# Navigation interactive
analysis_type = st.radio(
    "Choisissez votre analyse :",
    ["Vue d'ensemble", "Par région", "Par produit"],
    horizontal=True
)

if analysis_type == "Vue d'ensemble":
    col1, col2, col3 = st.columns(3)
    with col1:
        st.metric("Total Ventes", "1.2M€", "25%")
    with col2:
        st.metric("Nouveaux Clients", "450", "12%")
    with col3:
        st.metric("Satisfaction", "94%", "3%")

elif analysis_type == "Par région":
    regions_data = pd.DataFrame({
        'Région': ['Nord', 'Sud', 'Est', 'Ouest'],
        'Ventes': [300, 350, 280, 270],
        'Clients': [120, 140, 95, 95]
    })
    
    col1, col2 = st.columns(2)
    with col1:
        fig_regions = px.pie(regions_data, values='Ventes', names='Région',
                           title="Répartition des Ventes par Région")
        st.plotly_chart(fig_regions, use_container_width=True)
    
    with col2:
        fig_clients = px.bar(regions_data, x='Région', y='Clients',
                           color='Clients', color_continuous_scale='Viridis',
                           title="Nombre de Clients par Région")
        st.plotly_chart(fig_clients, use_container_width=True)

else:  # Par produit
    products_data = pd.DataFrame({
        'Produit': ['A', 'B', 'C', 'D'],
        'Ventes': [400, 300, 250, 350],
        'Marge': [20, 35, 30, 25]
    })
    
    fig_products = go.Figure()
    fig_products.add_trace(go.Bar(name='Ventes', x=products_data['Produit'], 
                                 y=products_data['Ventes'], yaxis='y', 
                                 marker_color='lightblue'))
    fig_products.add_trace(go.Scatter(name='Marge (%)', x=products_data['Produit'], 
                                    y=products_data['Marge'], yaxis='y2', 
                                    mode='lines+markers', marker_color='red'))
    
    fig_products.update_layout(
        title='Ventes et Marges par Produit',
        yaxis=dict(title='Ventes', side='left'),
        yaxis2=dict(title='Marge (%)', side='right', overlaying='y'),
        height=400
    )
    st.plotly_chart(fig_products, use_container_width=True)

st.markdown('</div>', unsafe_allow_html=True)

# Étape 4 : Conclusion interactive
st.markdown("---")
st.markdown("## 🎯 Conclusion Interactive")

# Slider pour explorer les données
year_range = st.slider("Explorez l'évolution dans le temps", 2020, 2024, (2022, 2024))

# Simulation de données temporelles
years = list(range(year_range[0], year_range[1] + 1))
values = [100 + (year - 2020) * 50 + (year - 2020)**2 * 10 for year in years]

final_data = pd.DataFrame({
    'Année': years,
    'Valeur': values
})

fig_final = px.line(final_data, x='Année', y='Valeur', 
                   markers=True, line_shape='spline',
                   title=f"Projection {year_range[0]}-{year_range[1]}")
fig_final.update_traces(line_color='#00d2d3', line_width=4, marker_size=10)
fig_final.update_layout(height=400)
st.plotly_chart(fig_final, use_container_width=True)

# Message final
st.success("""
🎉 **Félicitations !** Vous avez terminé cette expérience de scrollytelling avec Streamlit.
Cette approche permet de combiner narration et interactivité pour créer des histoires de données engageantes.
""")

# Footer
st.markdown("---")
st.markdown("""
<div style="text-align: center; color: #666; padding: 20px;">
    📊 Créé avec Streamlit • 🚀 Déployable en un clic
</div>
""", unsafe_allow_html=True)
