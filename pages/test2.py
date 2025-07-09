import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
import numpy as np
from datetime import datetime

st.set_page_config(layout="wide", page_title="Climate Map Africa", page_icon="🌍")

# Enhanced CSS styling with SDG colors and climate imagery
st.markdown("""
    <style>
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
            #border: 2px solid #FFD700;
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
        title="Temperature Anomalies by city and year",
        xaxis_title="Year",
        yaxis_title="City",
        height=max(400, len(selected_cities) * 50),
        font=dict(size=12)
    )
    
    return fig

# Main App
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

# Load data and calculate anomalies
df = load_data()
df = calculate_temperature_anomaly(df)

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

# Interactive Map
st.markdown("""
    <div class="subtitle">
        Interactive Climate Map of Africa
    </div>
""", unsafe_allow_html=True)

fig_map = px.scatter_mapbox(
    latest_data,
    lat="latitude",
    lon="lng",
    color="temperature",
    size_max=8,
    size=[8] * len(latest_data),
    hover_name="city",
    hover_data={"temperature": ":.1f", "temperature_anomaly": ":.2f"},
    zoom=3,
    mapbox_style="open-street-map",
    color_continuous_scale="RdBu_r",
    title=f"Average Temperature in {latest_year}"
)

fig_map.update_traces(marker=dict(size=8))
fig_map.update_layout(height=600)
st.plotly_chart(fig_map, use_container_width=True)

# Enhanced filtering section
st.markdown("""
    <div class="subtitle">
        Detailed Climate Analysis
    </div>
""", unsafe_allow_html=True)

#st.markdown("""
#   <div class="climate-info">
        #<h4>🔍 How to Use This Dashboard:</h4>
        #<p>1. Select countries from the dropdown below</p>
        #<p>2. Choose specific cities to analyze temperature trends</p>
        #<p>3. View the climate heatmap showing temperature anomalies over time</p>
       # <p>4. Read the climate narrative for insights and recommendations</p>
   # </div>
#""", unsafe_allow_html=True)

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

# Dynamic country selection feedback (moved under the filters)
 # if selected_countries:
   # st.markdown(f"""
       # <div class="climate-info">
       #     <p><strong>Selected Countries:</strong> {', '.join(selected_countries)}</p>
        #    <p><strong>Total Cities Available:</strong> {len(df[df['country_name'].isin(selected_countries)]['city'].unique())}</p>
       # </div>
    # """, unsafe_allow_html=True)

if selected_cities:
    # Generate climate narratives for each selected city
    for city in selected_cities:
        city_data = df[df['city'] == city]
        country_name = city_data['country_name'].iloc[0]
        narrative = generate_climate_narrative(city_data, city, country_name)
        if narrative:
            st.markdown(narrative, unsafe_allow_html=True)

    #st.markdown("""
      #  <div class="subtitle">
       #     Temperature Anomaly Heatmap
      #  </div>
   # """, unsafe_allow_html=True)
    
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
    
else:
    st.markdown("""
        <div class="climate-info">
            <h4>🎯 Get Started:</h4>
            <p>Please select at least one country and city to begin your climate analysis journey!</p>
            <p>Explore how temperatures have changed over time and discover the impacts of climate change in Africa.</p>
        </div>
    """, unsafe_allow_html=True)

# Call to Action
st.markdown("""
    <div class="sdg-card">
        <h3>🌱 Take Climate Action Today!</h3>
        <p><strong>Individual Actions:</strong> Reduce energy consumption, use renewable energy, support sustainable transportation</p>
        <p><strong>Community Actions:</strong> Advocate for climate policies, support local environmental initiatives, educate others</p>
        <p><strong>Global Actions:</strong> Support international climate agreements, sustainable development projects, and climate research</p>
    </div>
""", unsafe_allow_html=True)

# Enhanced Footer
st.markdown("""
    <div class="footer">
        <h4>🌍 Climate Action Africa Dashboard</h4>
        <p>Data source: <a href="https://cds.climate.copernicus.eu/" target="_blank" style="color: #4ECDC4;">Copernicus Climate Data Store</a></p>
        <p>Supporting UN SDGs: Climate Action (13) • Sustainable Cities (11) • Partnerships (17)</p>
        <p>🤝 Together, we can build a sustainable future for Africa and the world!</p>
    </div>
""", unsafe_allow_html=True)
