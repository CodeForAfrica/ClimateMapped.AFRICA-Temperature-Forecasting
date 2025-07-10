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
        
        .stats-card-1 {
            background: linear-gradient(135deg, #4facfe 0%, #00f2fe 100%);
            padding: 20px;
            border-radius: 12px;
            color: white;
            text-align: center;
            margin: 10px 0;
            box-shadow: 0 4px 15px rgba(79,172,254,0.3); 
            }
        .stats-card-2 {
            background: linear-gradient(135deg, #43e97b 0%, #38f9d7 100%);
            padding: 20px;
            border-radius: 12px;
            color: white;
            text-align: center;
            margin: 10px 0;
            box-shadow: 0 4px 15px rgba(67,233,123,0.3); 
        }
        .stats-card-3 {
            background: linear-gradient(135deg, #f093fb 0%, #f5576c 100%);
            padding: 20px;
            border-radius: 12px;
            color: white;
            text-align: center;
            margin: 10px 0;
            box-shadow: 0 4px 15px rgba(240,147,251,0.3); 
        }
        .stats-card-4 {
            background: linear-gradient(135deg, #ff9a9e 0%, #fad0c4 100%);
            padding: 20px;
            border-radius: 12px;
            color: white;
            text-align: center;
            margin: 10px 0;
            box-shadow: 0 4px 15px rgba(255,154,158,0.3); 
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
    anomaly_df = df.copy()
    baseline_data = df[(df['year'] >= baseline_start) & (df['year'] <= baseline_end)]
    baseline_temps = baseline_data.groupby('city')['temperature'].mean().reset_index()
    baseline_temps.columns = ['city', 'baseline_temp']
    anomaly_df = anomaly_df.merge(baseline_temps, on='city', how='left')
    anomaly_df['temperature_anomaly'] = anomaly_df['temperature'] - anomaly_df['baseline_temp']
    return anomaly_df

def generate_climate_narrative(city_data, city_name, country_name):
    if city_data.empty:
        return ""
    recent_years = city_data[city_data['year'] >= 2015]
    early_years = city_data[city_data['year'] <= 1980]
    if not recent_years.empty and not early_years.empty:
        recent_avg = recent_years['temperature'].mean()
        early_avg = early_years['temperature'].mean()
        temp_change = recent_avg - early_avg
        latest_anomaly = city_data[city_data['year'] == city_data['year'].max()]['temperature_anomaly'].iloc[0]
        if temp_change > 2.0:
            return f"""<div class="climate-warning"><h3>🔥 CRITICAL TEMPERATURE RISE DETECTED 🔥</h3>
                    <p><strong>{city_name}, {country_name}</strong> has experienced a significant increase of 
                    <strong>{temp_change:.1f}°C</strong> since the 1980s!</p>
                    <p>Current anomaly: <strong>{latest_anomaly:+.1f}°C</strong> above the 1961-1990 baseline</p>
                    <p>This aligns with <strong>SDG 13: Climate Action</strong> - urgent action needed!</p></div>"""
        elif temp_change > 1.0:
            return f"""<div class="climate-info"><h3>⚠️ MODERATE WARMING TREND ⚠️</h3>
                    <p><strong>{city_name}, {country_name}</strong> shows moderate warming of 
                    <strong>{temp_change:.1f}°C</strong> since the 1980s.</p>
                    <p>Current anomaly: <strong>{latest_anomaly:+.1f}°C</strong></p></div>"""
        else:
            return f"""<div class="climate-good"><h3>✅ STABLE TEMPERATURE PATTERN ✅</h3>
                    <p><strong>{city_name}, {country_name}</strong> shows a change of <strong>{temp_change:.1f}°C</strong>.</p>
                    <p>Anomaly: <strong>{latest_anomaly:+.1f}°C</strong></p></div>"""
    return ""

def create_climate_heatmap(df, selected_city):
    city_data = df[df['city'] == selected_city].sort_values('year')
    if city_data.empty:
        return go.Figure()
    fig = go.Figure(data=go.Heatmap(
        z=[city_data['temperature_anomaly'].values],
        x=city_data['year'].values,
        y=[selected_city],
        zmin=-3, zmax=3,
        colorscale='RdBu_r',
        showscale=True,
        colorbar=dict(title="Anomaly (°C)")
    ))
    fig.update_layout(title=f"Temperature Anomalies for {selected_city}", yaxis=dict(showticklabels=False))
    return fig

def create_temperature_trend_chart(df, selected_city):
    city_data = df[df['city'] == selected_city].sort_values('year')
    if city_data.empty:
        return go.Figure()
    fig = go.Figure()
    fig.add_trace(go.Scatter(
        x=city_data['year'], y=city_data['temperature'],
        mode='lines+markers', name='Temperature',
        line=dict(color='#FF6B6B')))
    z = np.polyfit(city_data['year'], city_data['temperature'], 1)
    p = np.poly1d(z)
    fig.add_trace(go.Scatter(
        x=city_data['year'], y=p(city_data['year']),
        mode='lines', name='Trend', line=dict(color='#4ECDC4', dash='dash')))
    fig.update_layout(title=f"Temperature Trend for {selected_city}", yaxis_title="Temperature (°C)")
    return fig

# Load data
df = load_data()
df = calculate_temperature_anomaly(df)
latest_year = df['year'].max()
latest_data = df[df['year'] == latest_year]

# Session state init
if 'selected_city' not in st.session_state:
    st.session_state.selected_city = None

# Title
st.markdown("<h1>Climate Map Africa</h1>", unsafe_allow_html=True)

# Stats
col1, col2, col3, col4 = st.columns(4)
with col1:
    st.metric("Cities Monitored", len(df['city'].unique()))
with col2:
    st.metric("Countries Covered", len(df['country_name'].unique()))
with col3:
    st.metric(f"Avg Temp {latest_year}", f"{latest_data['temperature'].mean():.1f}°C")
with col4:
    st.metric(f"Avg Anomaly {latest_year}", f"{latest_data['temperature_anomaly'].mean():+.1f}°C")

# Map
st.subheader("Interactive Climate Map of Africa")
fig_map = px.scatter_mapbox(
    latest_data,
    lat="latitude", lon="lng", color="temperature",
    hover_name="city", hover_data={"temperature": True, "country_name": True},
    center={"lat": 0, "lon": 20}, zoom=2,
    mapbox_style="open-street-map", color_continuous_scale="RdBu_r"
)
fig_map.update_traces(marker=dict(size=10))
fig_map.update_layout(height=700)

selected_points = plotly_events(fig_map, click_event=True, key="map")
if selected_points:
    index = selected_points[0]["pointIndex"]
    city_clicked = latest_data.iloc[index]['city']
    st.session_state.selected_city = city_clicked

# City View
if st.session_state.selected_city:
    selected_city = st.session_state.selected_city
    city_data = df[df['city'] == selected_city]
    if not city_data.empty:
        country_name = city_data['country_name'].iloc[0]
        st.subheader(f"Detailed Climate Analysis for {selected_city}, {country_name}")
        col1, col2 = st.columns(2)
        with col1:
            st.plotly_chart(create_temperature_trend_chart(df, selected_city), use_container_width=True)
        with col2:
            st.plotly_chart(create_climate_heatmap(df, selected_city), use_container_width=True)
        st.markdown(generate_climate_narrative(city_data, selected_city, country_name), unsafe_allow_html=True)
    else:
    st.info("Click a city on the map to explore its climate trend.")

else:
    st.markdown("""
        <div class="climate-info">
            <h4>🎯 Get Started:</h4>
            <p>Please select at least one country and city to begin your climate analysis journey!</p>
            <p>Explore how temperatures have changed over time and discover the impacts of climate change in Africa.</p>
        </div>
    """, unsafe_allow_html=True)

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

# Call to Action
st.markdown("""
    <div class="sdg-card">
        <h3>🌱 Take Climate Action Today!</h3>
        <p><strong>Individual Actions:</strong> Reduce energy consumption, use renewable energy, support sustainable transportation</p>
        <p><strong>Community Actions:</strong> Advocate for climate policies, support local environmental initiatives, educate others</p>
        <p><strong>Global Actions:</strong> Support international climate agreements, sustainable development projects, and climate research</p>
    </div>
""", unsafe_allow_html=True)

# Footer
st.markdown("""
    <div class="footer">
        <h4 style="color: white;" >🌍 Climate Map Africa Dashboard</h4>
        <p>Data source: <a href="https://cds.climate.copernicus.eu/" target="_blank" style="color: #4ECDC4;">Copernicus Climate Data Store</a></p>
        <p>Supporting UN SDGs: Climate Action (13) • Sustainable Cities (11) • Partnerships (17)</p>
        <p>🤝 Together, we can build a sustainable future for Africa and the world!</p>
    </div>
""", unsafe_allow_html=True)
