import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
import numpy as np
from datetime import datetime

st.set_page_config(layout="wide", page_title="Climate Map Africa", page_icon="🌍")

# Custom CSS for full-screen map landing page
st.markdown("""
<style>
/* Hide Streamlit default elements for landing page */
.landing-mode .main > div {
    padding: 0 !important;
    margin: 0 !important;
}

/* Navigation bar styling */
.nav-bar {
    background: linear-gradient(135deg, #2c3e50 0%, #34495e 100%);
    padding: 15px 30px;
    position: fixed;
    top: 0;
    left: 0;
    right: 0;
    z-index: 1000;
    display: flex;
    justify-content: space-between;
    align-items: center;
    box-shadow: 0 2px 10px rgba(0,0,0,0.3);
}

.nav-title {
    color: white;
    font-size: 24px;
    font-weight: bold;
    margin: 0;
}

.nav-links {
    display: flex;
    gap: 30px;
}

.nav-link {
    color: white;
    text-decoration: none;
    font-size: 16px;
    padding: 8px 16px;
    border-radius: 5px;
    transition: background-color 0.3s;
}

.nav-link:hover {
    background-color: rgba(255,255,255,0.1);
}

.nav-link.active {
    background-color: #4ECDC4;
}

/* Search bar overlay */
.search-overlay {
    position: absolute;
    top: 100px;
    left: 50%;
    transform: translateX(-50%);
    z-index: 500;
    background: rgba(255,255,255,0.95);
    padding: 20px;
    border-radius: 10px;
    box-shadow: 0 4px 20px rgba(0,0,0,0.2);
    min-width: 400px;
}

/* Full-screen map container */
.map-container {
    height: 100vh;
    margin-top: 60px;
}

/* Color legend */
.temperature-legend {
    position: absolute;
    bottom: 30px;
    left: 30px;
    background: rgba(255,255,255,0.95);
    padding: 15px;
    border-radius: 8px;
    box-shadow: 0 2px 10px rgba(0,0,0,0.2);
    z-index: 500;
}

.legend-item {
    display: flex;
    align-items: center;
    margin: 5px 0;
}

.legend-color {
    width: 20px;
    height: 15px;
    margin-right: 10px;
    border-radius: 3px;
}

/* Enhanced existing styles */
.main-title {
    background: linear-gradient(135deg, #4ECDC4 0%, #4ECDC4 100%);
    padding: 30px;
    border-radius: 15px;
    text-align: center;
    color: white;
    font-size: 42px;
    font-weight: bold;
    margin-bottom: 30px;
    box-shadow: 0 8px 32px rgba(0,0,0,0.3);
}

.sdg-header {
    background: linear-gradient(90deg, #FF6B6B, #4ECDC4, #45B7D1, #96CEB4, #FFEAA7);
    background-size: 300% 300%;
    animation: gradientShift 3s ease infinite;
    padding: 20px;
    border-radius: 12px;
    text-align: center;
    color: white;
    font-size: 24px;
    font-weight: bold;
    margin-bottom: 20px;
    box-shadow: 0 4px 15px rgba(0,0,0,0.2);
}

@keyframes gradientShift {
    0% { background-position: 0% 50%; }
    50% { background-position: 100% 50%; }
    100% { background-position: 0% 50%; }
}

.climate-warning {
    background: linear-gradient(135deg, #FF4444 0%, #CC0000 100%);
    padding: 20px;
    border-radius: 10px;
    color: white;
    font-weight: bold;
    text-align: center;
    margin: 20px 0;
    box-shadow: 0 4px 15px rgba(255,68,68,0.3);
    border-left: 5px solid #FFD700;
}

.climate-info {
    background: linear-gradient(135deg, #4ECDC4 0%, #44A08D 100%);
    padding: 15px;
    border-radius: 8px;
    color: white;
    margin: 15px 0;
    box-shadow: 0 4px 15px rgba(78,205,196,0.3);
}

.climate-good {
    background: linear-gradient(135deg, #56ab2f 0%, #a8e6cf 100%);
    padding: 15px;
    border-radius: 8px;
    color: white;
    margin: 15px 0;
    box-shadow: 0 4px 15px rgba(86,171,47,0.3);
}

.subtitle {
    background: linear-gradient(135deg, #4ECDC4 0%, #4ECDC4 100%);
    padding: 15px;
    border-radius: 10px;
    text-align: center;
    color: white;
    font-size: 22px;
    font-weight: bold;
    margin: 20px 0;
    box-shadow: 0 4px 15px rgba(102,126,234,0.3);
}

.sdg-card {
    background: linear-gradient(135deg, #f093fb 0%, #f5576c 100%);
    padding: 20px;
    border-radius: 12px;
    color: white;
    margin: 15px 0;
    box-shadow: 0 6px 20px rgba(240,147,251,0.3);
}

.stats-card {
    background: linear-gradient(135deg, #4facfe 0%, #00f2fe 100%);
    padding: 20px;
    border-radius: 12px;
    color: white;
    text-align: center;
    margin: 10px 0;
    box-shadow: 0 4px 15px rgba(79,172,254,0.3);
}

.footer {
    background: linear-gradient(135deg, #2c3e50 0%, #34495e 100%);
    padding: 20px;
    border-radius: 10px;
    color: white;
    text-align: center;
    margin-top: 30px;
}

/* Mode toggle button */
.mode-toggle {
    position: fixed;
    top: 20px;
    right: 20px;
    z-index: 1001;
    background: #4ECDC4;
    color: white;
    border: none;
    padding: 10px 20px;
    border-radius: 25px;
    cursor: pointer;
    font-weight: bold;
    box-shadow: 0 4px 15px rgba(78,205,196,0.3);
}

.mode-toggle:hover {
    background: #44A08D;
}

/* Multiselect styling */
.stMultiSelect > div > div {
    background-color: #4ECDC4 !important;
}
</style>
""", unsafe_allow_html=True)

# Country code to country name mapping for African countries
country_mapping = {
    'DZ': 'Algeria', 'AO': 'Angola', 'BJ': 'Benin', 'BW': 'Botswana',
    'BF': 'Burkina Faso', 'BI': 'Burundi', 'CM': 'Cameroon', 'CV': 'Cape Verde',
    'CF': 'Central African Republic', 'TD': 'Chad', 'KM': 'Comoros', 'CG': 'Congo',
    'CD': 'Democratic Republic of Congo', 'CI': 'Côte d\'Ivoire', 'DJ': 'Djibouti',
    'EG': 'Egypt', 'GQ': 'Equatorial Guinea', 'ER': 'Eritrea', 'ET': 'Ethiopia',
    'GA': 'Gabon', 'GM': 'Gambia', 'GH': 'Ghana', 'GN': 'Guinea', 'GW': 'Guinea-Bissau',
    'KE': 'Kenya', 'LS': 'Lesotho', 'LR': 'Liberia', 'LY': 'Libya', 'MG': 'Madagascar',
    'MW': 'Malawi', 'ML': 'Mali', 'MR': 'Mauritania', 'MU': 'Mauritius',
    'MA': 'Morocco', 'MZ': 'Mozambique', 'NA': 'Namibia', 'NE': 'Niger',
    'NG': 'Nigeria', 'RW': 'Rwanda', 'ST': 'São Tomé and Príncipe', 'SN': 'Senegal',
    'SC': 'Seychelles', 'SL': 'Sierra Leone', 'SO': 'Somalia', 'ZA': 'South Africa',
    'SS': 'South Sudan', 'SD': 'Sudan', 'SZ': 'Eswatini', 'TZ': 'Tanzania',
    'TG': 'Togo', 'TN': 'Tunisia', 'UG': 'Uganda', 'ZM': 'Zambia', 'ZW': 'Zimbabwe'
}

# Load and prepare the dataset
@st.cache_data
def load_data():
    df = pd.read_csv("data/sample_temp_1950-2025.csv")
    df.columns = df.columns.str.lower()

    if 'latitude' not in df.columns:
        df['latitude'] = df['lat']
    if 'lng' not in df.columns and 'longitude' in df.columns:
        df['lng'] = df['longitude']

    df['country_name'] = df['country'].map(country_mapping).fillna(df['country'])
    return df

def calculate_temperature_anomaly(df, baseline_start=1961, baseline_end=1990):
    """Calculate temperature anomaly based on baseline period (1961-1990)"""
    anomaly_df = df.copy()
    
    # Calculate baseline temperature for each city
    baseline_data = df[(df['year'] >= baseline_start) & (df['year'] <= baseline_end)]
    baseline_temps = baseline_data.groupby('city')['temperature'].mean().reset_index()
    baseline_temps.columns = ['city', 'baseline_temp']
    
    # Merge with main dataframe
    anomaly_df = anomaly_df.merge(baseline_temps, on='city', how='left')
    
    # Calculate anomaly
    anomaly_df['temperature_anomaly'] = anomaly_df['temperature'] - anomaly_df['baseline_temp']
    
    return anomaly_df

def create_landing_page_map(df):
    """Create a full-screen landing page map similar to the European climate map"""
    latest_year = df['year'].max()
    latest_data = df[df['year'] == latest_year]
    
    # Create a more heat-map like visualization
    fig = px.scatter_mapbox(
        latest_data,
        lat="latitude",
        lon="lng",
        color="temperature_anomaly",
        size="temperature",
        size_max=15,
        hover_name="city",
        hover_data={
            "temperature": ":.1f°C",
            "temperature_anomaly": ":.2f°C",
            "country_name": True
        },
        zoom=3,
        center={"lat": 0, "lon": 20},
        mapbox_style="open-street-map",
        color_continuous_scale="RdBu_r",
        color_continuous_midpoint=0,
        title=f"Temperature Anomalies Across Africa ({latest_year})",
        labels={"temperature_anomaly": "Temperature Anomaly (°C)"}
    )
    
    # Update layout for full-screen effect
    fig.update_layout(
        height=800,
        margin=dict(l=0, r=0, t=60, b=0),
        showlegend=False,
        font=dict(size=14),
        title_font_size=20,
        title_x=0.5,
        coloraxis_colorbar=dict(
            title="Temperature Anomaly (°C)",
            titlefont_size=14,
            tickfont_size=12,
            len=0.7,
            thickness=15
        )
    )
    
    # Make markers more visible
    fig.update_traces(
        marker=dict(
            opacity=0.8,
            line=dict(width=1, color='rgba(0,0,0,0.3)')
        )
    )
    
    return fig

def generate_climate_narrative(city_data, city_name, country_name):
    """Generate dynamic climate narrative based on data"""
    if city_data.empty:
        return ""
    
    # Calculate trends and anomalies
    recent_years = city_data[city_data['year'] >= 2015]
    early_years = city_data[city_data['year'] <= 1980]
    
    if not recent_years.empty and not early_years.empty:
        recent_avg = recent_years['temperature'].mean()
        early_avg = early_years['temperature'].mean()
        temp_change = recent_avg - early_avg
        
        # Get latest anomaly
        latest_anomaly = city_data[city_data['year'] == city_data['year'].max()]['temperature_anomaly'].iloc[0]
        
        # Generate narrative based on temperature trends
        if temp_change > 2.0:
            narrative_class = "climate-warning"
            emoji = "🔥"
            title = "CRITICAL TEMPERATURE RISE DETECTED"
            message = f"""
            <div class="{narrative_class}">
                <h3>{emoji} {title} {emoji}</h3>
                <p><strong>{city_name}, {country_name}</strong> has experienced a significant temperature increase of 
                <strong>{temp_change:.1f}°C</strong> since the 1980s!</p>
                <p>Current anomaly: <strong>{latest_anomaly:+.1f}°C</strong> above the 1961-1990 baseline</p>
                <p>🌍 This aligns with <strong>SDG 13: Climate Action</strong> - urgent action needed to combat climate change!</p>
                <p>💡 <strong>Take Action:</strong> Support renewable energy, reduce carbon footprint, and advocate for climate policies.</p>
            </div>
            """
        elif temp_change > 1.0:
            narrative_class = "climate-info"
            emoji = "⚠️"
            title = "MODERATE WARMING TREND"
            message = f"""
            <div class="{narrative_class}">
                <h3>{emoji} {title} {emoji}</h3>
                <p><strong>{city_name}, {country_name}</strong> shows a moderate warming trend of 
                <strong>{temp_change:.1f}°C</strong> since the 1980s.</p>
                <p>Current anomaly: <strong>{latest_anomaly:+.1f}°C</strong> above the 1961-1990 baseline</p>
                <p>🎯 This relates to <strong>SDG 13: Climate Action</strong> and <strong>SDG 11: Sustainable Cities</strong></p>
                <p>📊 Monitor trends closely and implement adaptation strategies.</p>
            </div>
            """
        else:
            narrative_class = "climate-good"
            emoji = "✅"
            title = "STABLE TEMPERATURE PATTERN"
            message = f"""
            <div class="{narrative_class}">
                <h3>{emoji} {title} {emoji}</h3>
                <p><strong>{city_name}, {country_name}</strong> shows relatively stable temperatures with a change of 
                <strong>{temp_change:.1f}°C</strong> since the 1980s.</p>
                <p>Current anomaly: <strong>{latest_anomaly:+.1f}°C</strong> compared to the 1961-1990 baseline</p>
                <p>🌱 Continue supporting <strong>SDG 13: Climate Action</strong> to maintain stability!</p>
            </div>
            """
        
        return message
    
    return ""

def create_climate_heatmap(df, selected_cities):
    """Create an enhanced climate stripes style heatmap with anomaly data"""
    if not selected_cities:
        return go.Figure()
    
    # Filter data for selected cities
    filtered_df = df[df['city'].isin(selected_cities)]
    
    # Create pivot table for heatmap using anomaly data
    pivot_df = filtered_df.pivot_table(
        index='city', 
        columns='year', 
        values='temperature_anomaly',
        aggfunc='mean'
    )
    
    # Create heatmap with anomaly scale
    fig = go.Figure(data=go.Heatmap(
        z=pivot_df.values,
        x=pivot_df.columns,
        y=pivot_df.index,
        zmin=-3,
        zmax=3,
        colorscale='RdBu_r',
        showscale=True,
        colorbar=dict(title="Temperature Anomaly (°C)"),
        hovertemplate='<b>%{y}</b><br>' +
                      'Year: %{x}<br>' +
                      'Anomaly: %{z:.2f}°C<br>' +
                      '<extra></extra>'
    ))
    
    fig.update_layout(
        title="Temperature Anomalies by City and Year",
        xaxis_title="Year",
        yaxis_title="City",
        height=max(400, len(selected_cities) * 50),
        font=dict(size=12)
    )
    
    return fig

# Load data and calculate anomalies
df = load_data()
df = calculate_temperature_anomaly(df)

# Navigation/Mode Selection
st.markdown("""
    <div class="nav-bar">
        <div class="nav-title">🌍 Climate Action Africa</div>
        <div class="nav-links">
            <a href="#" class="nav-link active">🗺️ Browse the Map</a>
            <a href="#" class="nav-link">📊 Detailed Analysis</a>
            <a href="#" class="nav-link">ℹ️ About</a>
        </div>
    </div>
""", unsafe_allow_html=True)

# Initialize session state for view mode
if 'view_mode' not in st.session_state:
    st.session_state.view_mode = 'map'

# Mode toggle buttons
col1, col2, col3 = st.columns([1, 1, 1])
with col1:
    if st.button("🗺️ Map View", type="primary" if st.session_state.view_mode == 'map' else "secondary"):
        st.session_state.view_mode = 'map'
with col2:
    if st.button("📊 Analysis View", type="primary" if st.session_state.view_mode == 'analysis' else "secondary"):
        st.session_state.view_mode = 'analysis'
with col3:
    if st.button("ℹ️ About", type="primary" if st.session_state.view_mode == 'about' else "secondary"):
        st.session_state.view_mode = 'about'

# Landing Page Map View
if st.session_state.view_mode == 'map':
    st.markdown("""
        <div class="search-overlay">
            <h4>🔍 Search for a Place</h4>
            <p>Click on any city on the map to explore its climate data</p>
        </div>
    """, unsafe_allow_html=True)
    
    # Create and display the landing page map
    fig_landing = create_landing_page_map(df)
    st.plotly_chart(fig_landing, use_container_width=True)
    
    # Add temperature legend
    st.markdown("""
        <div class="temperature-legend">
            <h5>Temperature Anomaly Scale</h5>
            <div class="legend-item">
                <div class="legend-color" style="background: #67001f;"></div>
                <span>Much warmer (+2°C to +3°C)</span>
            </div>
            <div class="legend-item">
                <div class="legend-color" style="background: #b2182b;"></div>
                <span>Warmer (+1°C to +2°C)</span>
            </div>
            <div class="legend-item">
                <div class="legend-color" style="background: #d6604d;"></div>
                <span>Slightly warmer (+0.5°C to +1°C)</span>
            </div>
            <div class="legend-item">
                <div class="legend-color" style="background: #f4a582;"></div>
                <span>Near normal (-0.5°C to +0.5°C)</span>
            </div>
            <div class="legend-item">
                <div class="legend-color" style="background: #92c5de;"></div>
                <span>Slightly cooler (-1°C to -0.5°C)</span>
            </div>
            <div class="legend-item">
                <div class="legend-color" style="background: #4393c3;"></div>
                <span>Cooler (-2°C to -1°C)</span>
            </div>
            <div class="legend-item">
                <div class="legend-color" style="background: #053061;"></div>
                <span>Much cooler (-3°C to -2°C)</span>
            </div>
        </div>
    """, unsafe_allow_html=True)

# Analysis View (your existing dashboard)
elif st.session_state.view_mode == 'analysis':
    st.markdown("""
        <div class="main-title">
            🌍 Climate Action Africa Dashboard 🌍
        </div>
    """, unsafe_allow_html=True)

    # SDG Information Section
    st.markdown("""
        <div class="sdg-header">
            🎯 Supporting UN Sustainable Development Goals 🎯
        </div>
    """, unsafe_allow_html=True)

    col1, col2, col3 = st.columns(3)

    with col1:
        st.markdown("""
            <div class="sdg-card">
                <h4>🌍 SDG 13: Climate Action</h4>
                <p>Take urgent action to combat climate change and its impacts through monitoring temperature trends and promoting awareness.</p>
            </div>
        """, unsafe_allow_html=True)

    with col2:
        st.markdown("""
            <div class="sdg-card">
                <h4>🏙️ SDG 11: Sustainable Cities</h4>
                <p>Make cities and human settlements inclusive, safe, resilient and sustainable by understanding urban climate patterns.</p>
            </div>
        """, unsafe_allow_html=True)

    with col3:
        st.markdown("""
            <div class="sdg-card">
                <h4>🤝 SDG 17: Partnerships</h4>
                <p>Strengthen global partnerships for sustainable development through open climate data and knowledge sharing.</p>
            </div>
        """, unsafe_allow_html=True)

    # Display key statistics
    latest_year = df['year'].max()
    latest_data = df[df['year'] == latest_year]

    col1, col2, col3, col4 = st.columns(4)

    with col1:
        st.markdown(f"""
            <div class="stats-card">
                <h5>Cities and Towns Monitored</h5>
                <h2>{len(df['city'].unique())}</h2>
            </div>
        """, unsafe_allow_html=True)

    with col2:
        st.markdown(f"""
            <div class="stats-card">
                <h5>Countries Covered</h5>
                <h2>{len(df['country_name'].unique())}</h2>
            </div>
        """, unsafe_allow_html=True)

    with col3:
        avg_temp = latest_data['temperature'].mean()
        st.markdown(f"""
            <div class="stats-card">
                <h5>Average Temperature {latest_year}</h5>
                <h2>{avg_temp:.1f}°C</h2>
            </div>
        """, unsafe_allow_html=True)

    with col4:
        avg_anomaly = latest_data['temperature_anomaly'].mean()
        st.markdown(f"""
            <div class="stats-card">
                <h5>Average Anomaly {latest_year}</h5>
                <h2>{avg_anomaly:+.1f}°C</h2>
            </div>
        """, unsafe_allow_html=True)

    # Enhanced filtering section
    st.markdown("""
        <div class="subtitle">
            Detailed Climate Analysis
        </div>
    """, unsafe_allow_html=True)

    st.markdown("""
        <div class="climate-info">
            <h4>🔍 How to Use This Dashboard:</h4>
            <p>1. Select countries from the dropdown below</p>
            <p>2. Choose specific cities to analyze temperature trends</p>
            <p>3. View the climate heatmap showing temperature anomalies over time</p>
            <p>4. Read the climate narrative for insights and recommendations</p>
        </div>
    """, unsafe_allow_html=True)

    # Country and City selection
    countries = sorted(df['country_name'].unique())

    # Create two columns for aligned filters
    col1, col2 = st.columns(2)

    with col1:
        selected_countries = st.multiselect(
            "Select countries to analyze:", 
            countries, 
            default=['Senegal'] if 'Senegal' in countries else countries[:1],
            help="Choose one or more African countries to examine their climate data"
        )

    # Filter cities based on selected countries
    available_cities = df[df['country_name'].isin(selected_countries)]['city'].sort_values().unique()

    with col2:
        selected_cities = st.multiselect(
            "Select cities for detailed analysis:", 
            available_cities, 
            default=available_cities[:1] if len(available_cities) > 2 else available_cities,
            help="Choose specific cities to analyze temperature trends and anomalies"
        )

    # Dynamic country selection feedback
    if selected_countries:
        st.markdown(f"""
            <div class="climate-info">
                <p><strong>Selected Countries:</strong> {', '.join(selected_countries)}</p>
                <p><strong>Total Cities Available:</strong> {len(df[df['country_name'].isin(selected_countries)]['city'].unique())}</p>
            </div>
        """, unsafe_allow_html=True)

    if selected_cities:
        # Generate climate narratives for each selected city
        for city in selected_cities:
            city_data = df[df['city'] == city]
            country_name = city_data['country_name'].iloc[0]
            narrative = generate_climate_narrative(city_data, city, country_name)
            if narrative:
                st.markdown(narrative, unsafe_allow_html=True)

        fig_heatmap = create_climate_heatmap(df, selected_cities)
        st.plotly_chart(fig_heatmap, use_container_width=True)
        
        # Additional insights
        st.markdown("""
            <div class="climate-info">
                <h4>📖 Understanding Temperature Anomalies:</h4>
                <p>• <strong>Positive anomalies (red)</strong>: Temperatures above the 1961-1990 average</p>
                <p>• <strong>Negative anomalies (blue)</strong>: Temperatures below the 1961-1990 average</p>
                <p>• <strong>Baseline period</strong>: 1961-1990 is used as the reference period following WMO standards</p>
                <p>• <strong>Climate stripes</strong>: Each column represents one year, showing long-term trends</p>
            </div>
        """, unsafe_allow_html=True)

# About View
elif st.session_state.view_mode == 'about':
    st.markdown("""
        <div class="main-title">
            About Climate Action Africa
        </div>
    """, unsafe_allow_html=True)
    
    st.markdown("""
        <div class="climate-info">
            <h4>🌍 Our Mission</h4>
            <p>Climate Action Africa is dedicated to visualizing and understanding climate change impacts across the African continent. 
            We provide accessible climate data visualization tools to support informed decision-making and climate action.</p>
            
            <h4>📊 Data Sources</h4>
            <p>Our temperature data comes from the Copernicus Climate Data Store, providing comprehensive coverage of African cities 
            from 1950 to present. Temperature anomalies are calculated using the 1961-1990 baseline period following World Meteorological Organization standards.</p>
            
            <h4>🎯 Supporting UN SDGs</h4>
            <p>This dashboard directly supports:</p>
            <ul>
                <li><strong>SDG 13: Climate Action</strong> - Urgent action to combat climate change</li>
                <li><strong>SDG 11: Sustainable Cities</strong> - Making cities resilient and sustainable</li>
                <li><strong>SDG 17: Partnerships</strong> - Strengthening global partnerships for sustainable development</li>
            </ul>
        </div>
    """, unsafe_allow_html=True)

# Call to Action (appears in all views)
st.markdown("""
    <div class="sdg-card">
        <h3>🌱 Take Climate Action Today!</h3>
        <p><strong>Individual Actions:</strong> Reduce energy consumption, use renewable energy, support sustainable transportation</p>
        <p><strong>Community Actions:</strong> Advocate for climate policies, support local environmental initiatives, educate others</p>
        <p><strong>Global Actions:</strong> Support international climate agreements, sustainable development projects, and climate research</p>
    </div>
""", unsafe_allow_html)
