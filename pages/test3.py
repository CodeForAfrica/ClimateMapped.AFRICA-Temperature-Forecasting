import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
import numpy as np
from datetime import datetime

st.set_page_config(layout="wide", page_title="Climate Map Africa", page_icon="🌍")

# Enhanced CSS styling with improved design and containers
st.markdown("""
    <style>
        /* Main app background */
        .main {
            background: linear-gradient(135deg, #667eea 0%, #764ba2 25%, #f093fb 50%, #f5576c 75%, #4facfe 100%);
            background-size: 400% 400%;
            animation: gradientShift 15s ease infinite;
            min-height: 100vh;
        }
        
        @keyframes gradientShift {
            0% { background-position: 0% 50%; }
            25% { background-position: 100% 50%; }
            50% { background-position: 50% 100%; }
            75% { background-position: 50% 0%; }
            100% { background-position: 0% 50%; }
        }
        
        /* Container styling - Reduced bottom margin */
        .custom-container {
            background: rgba(255, 255, 255, 0.95);
            backdrop-filter: blur(10px);
            padding: 25px;
            border-radius: 20px;
            box-shadow: 0 8px 32px rgba(0, 0, 0, 0.3);
            border: 1px solid rgba(255, 255, 255, 0.18);
            margin-bottom: 10px; /* Reduced from 20px */
        }
        
        .plot-container {
            background: rgba(255, 255, 255, 0.98);
            backdrop-filter: blur(15px);
            padding: 20px;
            border-radius: 15px;
            box-shadow: 0 10px 40px rgba(0, 0, 0, 0.2);
            border: 1px solid rgba(255, 255, 255, 0.3);
            margin: 10px 0; /* Reduced from 15px */
            overflow: hidden; /* Prevent content overflow */
        }
        
        .main-title {
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            padding: 40px;
            border-radius: 25px;
            text-align: center;
            color: white;
            font-size: 48px;
            font-weight: bold;
            margin-bottom: 20px; /* Reduced from 30px */
            box-shadow: 0 15px 50px rgba(102, 126, 234, 0.4);
            border: 3px solid rgba(255, 255, 255, 0.2);
            text-shadow: 2px 2px 4px rgba(0, 0, 0, 0.3);
        }
        
        .sdg-header {
            background: linear-gradient(135deg, #FF6B6B 0%, #4ECDC4 25%, #45B7D1 50%, #96CEB4 75%, #FFEAA7 100%);
            background-size: 300% 300%;
            animation: gradientShift 8s ease infinite;
            padding: 30px;
            border-radius: 20px;
            text-align: center;
            color: white;
            font-size: 28px;
            font-weight: bold;
            margin-bottom: 15px; /* Reduced from 25px */
            box-shadow: 0 12px 40px rgba(0, 0, 0, 0.3);
            border: 2px solid rgba(255, 255, 255, 0.2);
            text-shadow: 2px 2px 4px rgba(0, 0, 0, 0.3);
        }
        
        .climate-warning {
            background: linear-gradient(135deg, #FF4444 0%, #CC0000 100%);
            padding: 25px;
            border-radius: 15px;
            color: white;
            font-weight: bold;
            text-align: center;
            margin: 10px 0; /* Reduced from 20px */
            box-shadow: 0 10px 30px rgba(255, 68, 68, 0.4);
            border-left: 6px solid #FFD700;
            border: 2px solid rgba(255, 255, 255, 0.2);
        }
        
        .climate-info {
            background: linear-gradient(135deg, #4ECDC4 0%, #44A08D 100%);
            padding: 20px;
            border-radius: 15px;
            color: white;
            margin: 10px 0; /* Reduced from 20px */
            box-shadow: 0 8px 25px rgba(78, 205, 196, 0.4);
            border: 2px solid rgba(255, 255, 255, 0.2);
        }
        
        .climate-good {
            background: linear-gradient(135deg, #56ab2f 0%, #a8e6cf 100%);
            padding: 20px;
            border-radius: 15px;
            color: white;
            margin: 10px 0; /* Reduced from 20px */
            box-shadow: 0 8px 25px rgba(86, 171, 47, 0.4);
            border: 2px solid rgba(255, 255, 255, 0.2);
        }
        
        .subtitle {
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            padding: 20px;
            border-radius: 15px;
            text-align: center;
            color: white;
            font-size: 26px;
            font-weight: bold;
            margin: 15px 0; /* Reduced from 25px */
            box-shadow: 0 8px 30px rgba(102, 126, 234, 0.4);
            border: 2px solid rgba(255, 255, 255, 0.2);
            text-shadow: 1px 1px 2px rgba(0, 0, 0, 0.3);
        }
        
        .sdg-card {
            background: linear-gradient(135deg, #f093fb 0%, #f5576c 100%);
            padding: 25px;
            border-radius: 18px;
            color: white;
            margin: 10px 0; /* Reduced from 20px */
            box-shadow: 0 12px 35px rgba(240, 147, 251, 0.4);
            border: 2px solid rgba(255, 255, 255, 0.2);
            transition: transform 0.3s ease;
        }
        
        .sdg-card:hover {
            transform: translateY(-5px);
            box-shadow: 0 15px 45px rgba(240, 147, 251, 0.5);
        }
        
        .stats-card {
            background: linear-gradient(135deg, #4facfe 0%, #00f2fe 100%);
            padding: 25px;
            border-radius: 18px;
            color: white;
            text-align: center;
            margin: 10px 0; /* Reduced from 15px */
            box-shadow: 0 10px 30px rgba(79, 172, 254, 0.4);
            border: 2px solid rgba(255, 255, 255, 0.2);
            transition: transform 0.3s ease;
        }
        
        .stats-card:hover {
            transform: translateY(-3px);
            box-shadow: 0 12px 40px rgba(79, 172, 254, 0.5);
        }
        
        .footer {
            background: linear-gradient(135deg, #2c3e50 0%, #34495e 100%);
            padding: 30px;
            border-radius: 20px;
            color: white;
            text-align: center;
            margin-top: 30px; /* Reduced from 40px */
            box-shadow: 0 12px 40px rgba(44, 62, 80, 0.4);
            border: 2px solid rgba(255, 255, 255, 0.1);
        }
        
        .click-instruction {
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            padding: 20px;
            border-radius: 15px;
            color: white;
            text-align: center;
            margin: 10px 0; /* Reduced from 20px */
            box-shadow: 0 8px 25px rgba(102, 126, 234, 0.4);
            font-size: 18px;
            font-weight: bold;
            border: 2px solid rgba(255, 255, 255, 0.2);
        }
        
        /* Streamlit component styling - Fixed overflow */
        .stPlotlyChart {
            background: transparent;
            border-radius: 15px;
            overflow: hidden;
            width: 100% !important;
            max-width: 100% !important;
        }
        
        .stPlotlyChart > div {
            width: 100% !important;
            max-width: 100% !important;
        }
        
        /* Hide Streamlit branding */
        #MainMenu {visibility: hidden;}
        footer {visibility: hidden;}
        header {visibility: hidden;}
        
        /* Ensure proper responsive behavior */
        .element-container {
            width: 100% !important;
            max-width: 100% !important;
        }
        
        /* Fix for columns */
        .row-widget {
            width: 100% !important;
        }
        
        /* Additional spacing reductions for tighter layout */
        .block-container {
            padding-top: 1rem;
            padding-bottom: 1rem;
        }
        
        .element-container {
            margin-bottom: 0.5rem;
        }
    </style>
""", unsafe_allow_html=True)

# Country code to country name mapping for African countries
country_mapping = {
    'DZ': 'Algeria', 'AO': 'Angola', 'BJ': 'Benin', 'BW': 'Botswana',
    'BF': 'Burkina Faso', 'BI': 'Burundi', 'CM': 'Cameroon', 'CV': 'Cape Verde',
    'CF': 'Central African Republic', 'TD': 'Chad', 'KM': 'Comoros', 'CG': 'Congo',
    'CD': 'Democratic Republic of Congo', 'CI': 'Côte d\'Ivoire', 'DJ': 'Djibouti',
    'EG': 'Egypt', 'EH': 'Western Sahara', 'GQ': 'Equatorial Guinea', 'ER': 'Eritrea', 'ET': 'Ethiopia', 
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

    df['country_name'] = df['country'].map(country_mapping)
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
                <p>This aligns with <strong>SDG 13: Climate Action</strong> - urgent action needed to combat climate change!</p>
                <p><strong>Take Action:</strong> Support renewable energy, reduce carbon footprint, and advocate for climate policies.</p>
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
                <p>This relates to <strong>SDG 13: Climate Action</strong> and <strong>SDG 11: Sustainable Cities</strong></p>
                <p>Monitor trends closely and implement adaptation strategies.</p>
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

def create_climate_heatmap(df, selected_city):
    """Create an enhanced climate stripes style heatmap with anomaly data for a single city"""
    if not selected_city:
        return None
    
    # Filter data for selected city
    city_data = df[df['city'] == selected_city]
    
    if city_data.empty:
        return None
    
    # Sort by year
    city_data = city_data.sort_values('year')
    
    # Create heatmap with anomaly scale (single row for the city)
    fig = go.Figure(data=go.Heatmap(
        z=[city_data['temperature_anomaly'].values],
        x=city_data['year'].values,
        y=[selected_city],
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
        title=f"Temperature Anomalies for {selected_city}",
        #plot_bgcolor='rgba(255,255,255,0.9)',
        paper_bgcolor='rgba(255,255,255,0.95)',
        margin=dict(l=40, r=40, t=60, b=40),
        xaxis_title="Year",
        yaxis=dict(showticklabels=False, gridcolor='rgba(0,0,0,0.1)'),
        height=350,
        font=dict(size=12),
        title_font=dict(size=16, color='#2c3e50'),
        xaxis=dict(gridcolor='rgba(0,0,0,0.1)'),
        autosize=True
    )
    
    return fig

def create_temperature_trend_chart(df, selected_city):
    """Create a line chart showing temperature trends for the selected city"""
    if not selected_city:
        return None
    
    city_data = df[df['city'] == selected_city].sort_values('year')
    
    if city_data.empty:
        return None
    
    fig = go.Figure()
    
    # Add temperature line
    fig.add_trace(go.Scatter(
        x=city_data['year'],
        y=city_data['temperature'],
        mode='lines+markers',
        name='Temperature',
        line=dict(color='#FF6B6B', width=3),
        marker=dict(size=6, color='#FF6B6B'),
        hovertemplate='Year: %{x}<br>Temperature: %{y:.1f}°C<extra></extra>'
    ))
    
    # Add trend line
    z = np.polyfit(city_data['year'], city_data['temperature'], 1)
    p = np.poly1d(z)
    fig.add_trace(go.Scatter(
        x=city_data['year'],
        y=p(city_data['year']),
        mode='lines',
        name='Trend',
        line=dict(color='#4ECDC4', width=4, dash='dash'),
        hovertemplate='Year: %{x}<br>Trend: %{y:.1f}°C<extra></extra>'
    ))
    
    fig.update_layout(
        title=f"Temperature Trend for {selected_city}",
        plot_bgcolor='rgba(255,255,255,0.9)',
        paper_bgcolor='rgba(255,255,255,0.95)',
        margin=dict(l=40, r=40, t=60, b=40),
        xaxis_title="Year",
        yaxis_title="Temperature (°C)",
        height=350,
        font=dict(size=12),
        title_font=dict(size=16, color='#2c3e50'),
        xaxis=dict(gridcolor='rgba(0,0,0,0.1)'),
        yaxis=dict(gridcolor='rgba(0,0,0,0.1)'),
        legend=dict(
            bgcolor='rgba(255,255,255,0.8)',
            bordercolor='rgba(0,0,0,0.2)',
            borderwidth=1
        ),
        autosize=True
    )
    
    return fig

# Initialize session state for selected city
if 'selected_city' not in st.session_state:
    st.session_state.selected_city = None

# Main App
st.markdown("""
    <div class="main-title">
        Climate Map Africa
    </div>
""", unsafe_allow_html=True)

# SDG Information Section
st.markdown("""
    <div class="custom-container">
        <div class="sdg-header">
            🎯 Supporting UN Sustainable Development Goals 🎯 
        </div>
    </div>
""", unsafe_allow_html=True)

col1, col2, col3 = st.columns(3)
with col1:
    st.markdown("""
        <div class="custom-container">
            <div class="sdg-card">
                <h4>🌍 SDG 13: Climate Action</h4>
                <p>Take urgent action to combat climate change and its impacts through monitoring temperature trends and promoting awareness.</p>
            </div>
        </div>
    """, unsafe_allow_html=True)

with col2:
    st.markdown("""
        <div class="custom-container">
            <div class="sdg-card">
                <h4>🏙️ SDG 11: Sustainable Cities</h4>
                <p>Make cities and human settlements inclusive, safe, resilient and sustainable by understanding urban climate patterns.</p>
            </div>
        </div>
    """, unsafe_allow_html=True)

with col3:
    st.markdown("""
        <div class="custom-container">
            <div class="sdg-card">
                <h4>🤝 SDG 17: Partnerships</h4>
                <p>Strengthen global partnerships for sustainable development through open climate data and knowledge sharing.</p>
            </div>
        </div>
    """, unsafe_allow_html=True)

# Load data and calculate anomalies
df = load_data()
df = calculate_temperature_anomaly(df)

# Display key statistics
latest_year = df['year'].max()
latest_data = df[df['year'] == latest_year]

st.markdown('<div class="custom-container">', unsafe_allow_html=True)
col1, col2, col3, col4 = st.columns(4)
with col1:
    st.markdown(f"""
        <div class="stats-card">
            <h5>Cities and Towns Monitored</h5>
            <h4>{len(df['city'].unique())}</h4>
        </div>
    """, unsafe_allow_html=True)
with col2:
    st.markdown(f"""
        <div class="stats-card">
            <h5>Countries Covered</h5>
            <h4>{len(df['country_name'].unique())}</h4>
        </div>
    """, unsafe_allow_html=True)
with col3:
    avg_temp = latest_data['temperature'].mean()
    st.markdown(f"""
        <div class="stats-card">
            <h5>Average Temperature {latest_year}</h5>
            <h4>{avg_temp:.1f}°C</h4>
        </div>
    """, unsafe_allow_html=True)
with col4:
    avg_anomaly = latest_data['temperature_anomaly'].mean()
    st.markdown(f"""
        <div class="stats-card">
            <h5>Average Anomaly {latest_year}</h5>
            <h4>{avg_anomaly:+.1f}°C</h4>
        </div>
    """, unsafe_allow_html=True)
st.markdown('</div>', unsafe_allow_html=True)

# Interactive Map
st.markdown("""
    <div class="custom-container">
        <div class="subtitle">
            Interactive Climate Map of Africa <br>
            <span style="font-size:16px;"> Click on any city point on the map to see detailed climate analysis!</span>
        </div>
    </div>
""", unsafe_allow_html=True)

fig_map = px.scatter_mapbox(
    latest_data,
    lat="latitude",
    lon="lng",
    color="temperature",
    hover_name="city",
    hover_data={"temperature": ":.1f", "country_name": True},
    center={"lat": 0, "lon": 20},
    zoom=2,
    mapbox_style="open-street-map",
    color_continuous_scale="RdBu_r",
    title=f"Average Temperature in {latest_year}"
)

# Set marker size and layout
fig_map.update_traces(marker=dict(size=12))
fig_map.update_layout(
    height=600,
    plot_bgcolor='rgba(255,255,255,0.9)',
    paper_bgcolor='rgba(255,255,255,0.95)',
    title_font=dict(size=18, color='#2c3e50'),
    font=dict(size=12),
    margin=dict(l=0, r=0, t=40, b=0),
    autosize=True
)

# Display the map in a container
if "selected_cities" not in st.session_state:
    st.session_state.selected_cities = []

# --- Step 2: UI – Country & City Filters ---
countries = sorted(df['country_name'].unique())

col1, col2 = st.columns(2)

with col1:
    selected_countries = st.multiselect(
        "Select countries to analyze:", 
        countries,
        default=['Senegal'] if 'Senegal' in countries else countries[:1],
        help="Choose one or more African countries to examine their climate data"
    )

# Combine available cities from selected countries + any cities already selected (including map clicks)
filtered_df = df[df['country_name'].isin(selected_countries)]
dropdown_cities = sorted(filtered_df['city'].unique())

# Add any previously selected cities that may not be in current country filter
dropdown_cities = sorted(set(dropdown_cities) | set(st.session_state.selected_cities))

with col2:
    selected_cities = st.multiselect(
        "Select cities for detailed analysis:", 
        dropdown_cities, 
        default=st.session_state.selected_cities,
        help="Choose specific cities to analyze temperature trends and anomalies"
    )

# Update session state
st.session_state.selected_cities = selected_cities

# --- Step 3: Map Click Handling ---
map_click = st.plotly_chart(fig_map, use_container_width=True, on_select="rerun")

if map_click and map_click.selection and map_click.selection.points:
    clicked_point = map_click.selection.points[0]
    clicked_city = None

    if 'hovertext' in clicked_point:
        clicked_city = clicked_point['hovertext']
    elif 'customdata' in clicked_point:
        point_index = clicked_point['point_index']
        if point_index < len(latest_data):
            clicked_city = latest_data.iloc[point_index]['city']

    # If clicked city is valid and not already selected, add it and rerun
    if clicked_city and clicked_city not in st.session_state.selected_cities:
        st.session_state.selected_cities.append(clicked_city)
        st.experimental_rerun()

# --- Step 4: Display Analysis ---
if st.session_state.selected_cities:
    for city in st.session_state.selected_cities:
        city_data = df[df['city'] == city]
        if not city_data.empty:
            country_name = city_data['country_name'].iloc[0]

            st.markdown(f"""
                <div class="subtitle">
                    <strong>Detailed Climate Analysis for {city}, {country_name}</strong>
                </div>
            """, unsafe_allow_html=True)

            col1, col2 = st.columns(2)

            with col1:
                trend_chart = create_temperature_trend_chart(df, city)
                st.plotly_chart(trend_chart, use_container_width=True)

            with col2:
                heatmap = create_climate_heatmap(df, city)
                st.plotly_chart(heatmap, use_container_width=True)

            narrative = generate_climate_narrative(city_data, city, country_name)
            if narrative:
                st.markdown(narrative, unsafe_allow_html=True)

        # Additional insights
        st.markdown("""
            <div class="custom-container">
                <div class="climate-info">
                    <h4>📖 Understanding Temperature Anomalies:</h4>
                    <p>• <strong>Positive anomalies (red)</strong>: Temperatures above the 1961-1990 average</p>
                    <p>• <strong>Negative anomalies (blue)</strong>: Temperatures below the 1961-1990 average</p>
                    <p>• <strong>Baseline period</strong>: 1961-1990 is used as the reference period following WMO standards</p>
                    <p>• <strong>Climate stripes</strong>: Each column represents one year, showing long-term trends</p>
                </div>
            </div>
        """, unsafe_allow_html=True)
    
else:
    st.markdown("""
        <div class="custom-container">
            <div class="climate-info">
                <h4>🎯 Get Started:</h4>
                <p>Click on any city point on the map above to begin your climate analysis journey!</p>
                <p>Explore how temperatures have changed over time and discover the impacts of climate change in Africa.</p>
            </div>
        </div>
    """, unsafe_allow_html=True)

# Call to Action
st.markdown("""
    <div class="custom-container">
        <div class="sdg-card">
            <h3>🌱 Take Climate Action Today!</h3>
            <p><strong>Individual Actions:</strong> Reduce energy consumption, use renewable energy, support sustainable transportation</p>
            <p><strong>Community Actions:</strong> Advocate for climate policies, support local environmental initiatives, educate others</p>
            <p><strong>Global Actions:</strong> Support international climate agreements, sustainable development projects, and climate research</p>
        </div>
    </div>
""", unsafe_allow_html=True)

# Footer
st.markdown("""
    <div class="footer">
        <h4 style="color: white;">🌍 Climate Map Africa Dashboard</h4>
        <p>Data source: <a href="https://cds.climate.copernicus.eu/" target="_blank" style="color: #4ECDC4;">Copernicus Climate Data Store</a></p>
        <p>Supporting UN SDGs: Climate Action (13) • Sustainable Cities (11) • Partnerships (17)</p>
        <p>🤝 Together, we can build a sustainable future for Africa
    </div>
""", unsafe_allow_html=True)
