import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
import numpy as np
from datetime import datetime
import calendar


st.set_page_config(layout="wide", page_title="Climate Map Africa", page_icon="🌍")

# Enhanced CSS styling with SDG colors and climate imagery

st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Poppins:wght@300;400;500;600;700&display=swap');
    html, body, [class*="st"] {
        font-family: 'Poppins', sans-serif;
    }
    </style>
""", unsafe_allow_html=True)

st.markdown("""
    <style>
    .stApp {
        background-image: url("https://climatemapped-africa.dev.codeforafrica.org/_next/static/media/bg-map-white.f3fbc71d.jpg");
        background-attachment: fixed;
        background-size: cover;
    }
        #.custom-container {
        #    background-image: 
        #    background-size: cover;  
        #    background-position: center; 
        #    background-repeat: no-repeat; 
        #    #background-color: #ffeaa7;
        #    padding: 20px;
        #    border-radius: 10px;
        #    box-shadow: 0 4px 15px rgba(0,0,0,0.1);
        }
    </style>
""", unsafe_allow_html=True)

st.markdown("""
    <style>
        .main-title {
            background-image: url("https://climatemapped-africa.dev.codeforafrica.org/media/sat-mtKenya-1_alt@2400x.jpg");
            background-size: cover;
            background-position: center;
            #background: linear-gradient(135deg, #0000FF 0%, #0000FF 100%);
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

        @keyframes gradientShift {
            0% { background-position: 0% 50%; }
            50% { background-position: 100% 50%; }
            100% { background-position: 0% 50%; }
        }
        
        .sdg-header {
            background: linear-gradient(90deg, #FF0000, #007aff, #45B7D1, #0000FF, #0000FF);
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
            #background: linear-gradient(135deg, #007aff 0%, #007aff 100%);
            #background: linear-gradient(135deg, rgba(0,0,255,0.6) 0%, rgba(0,0,255,0.6) 100%);
            background: transparent;
            padding: 15px;
            border-radius: 8px;
            color: black;
            margin: 15px 0;
            box-shadow: 0 4px 15px rgba(78,205,196,0.3);
        }
        .climate-info h4 {
        color: black; 
        }
        .climate-info p {
        color: black;
        }
        
    
        .climate-good {
            #background: transparent;
            background: linear-gradient(135deg, #56ab2f 0%, #a8e6cf 100%);
            padding: 15px;
            border-radius: 8px;
            color: white;
            margin: 15px 0;
            box-shadow: 0 4px 15px rgba(86,171,47,0.3);
        }
        
        .subtitle {
            background-image: url("https://climatemapped-africa.dev.codeforafrica.org/media/sat-mtKenya-1_alt@2400x.jpg");
            background-size: cover;
            background-position: center;
            #background: linear-gradient(135deg, #0000FF 0%, #0000FF 100%);
            padding: 15px;
            border-radius: 10px;
            text-align: center;
            color: white;
            font-size: 22px;
            font-weight: bold;
            margin: 20px 0;
            #box-shadow: 0 4px 15px rgba(102,126,234,0.3);
            box-shadow: 0 4px 15px rgba(78,205,196,0.3);
        }
        
        .sdg-card {
            background: transparent;
            #background: linear-gradient(135deg, #f093fb 0%, #f5576c 100%);
            padding: 20px;
            border-radius: 12px;
            color: black;
            margin: 15px 0;
            #box-shadow: 0 6px 20px rgba(240,147,251,0.3);
            box-shadow: 0 4px 15px rgba(78,205,196,0.3);
        }

        }
        .sdg-card h4 {
        color: black; 
        }
        .sdg-card p {
        color: black;
        }
        
        .stats-card-1 {
            #background: linear-gradient(135deg, #4facfe 0%, #4facfe 100%);
            background: #0000CD; 
            padding: 20px;
            border-radius: 12px;
            color: white;
            text-align: center;
            margin: 10px 0;
            #box-shadow: 0 4px 15px rgba(79,172,254,0.3); 
            box-shadow: 0 4px 15px rgba(78,205,196,0.3);
            }
        .stats-card-1, 
        .stats-card-1 * {
            color: white ;
        }
            

        .stats-card-1:hover {
            transform: translateY(-3px);
            box-shadow: 0 12px 40px rgba(79, 172, 254, 0.5);
        }

        .stats-card-2 {
            #background: linear-gradient(135deg, #7B68EE 0%, #7B68EE 100%);
            background: #1E90FF;
            padding: 20px;
            border-radius: 12px;
            color: white;
            text-align: center;
            margin: 10px 0;
            #box-shadow: 0 4px 15px rgba(67,233,123,0.3);
            box-shadow: 0 4px 15px rgba(78,205,196,0.3);
        }

        .stats-card-2, 
        .stats-card-2 * {
            color: white ;
        }

        .stats-card-2:hover {
            transform: translateY(-3px);
            box-shadow: 0 12px 40px rgba(79, 172, 254, 0.5);
        }
        
        .stats-card-3 {
            #background: linear-gradient(135deg, #1E90FF 0%, #1E90FF 100%);
            background:#0000FF; 
            padding: 20px;
            border-radius: 12px;
            color: white;
            text-align: center;
            margin: 10px 0;
            #box-shadow: 0 4px 15px rgba(240,147,251,0.3);
            box-shadow: 0 4px 15px rgba(78,205,196,0.3);
        }

        .stats-card-3, 
        .stats-card-3 * {
            color: white ;
        }
        
        .stats-card-3:hover {
            transform: translateY(-3px);
            box-shadow: 0 12px 40px rgba(79, 172, 254, 0.5);
        }
        
        .stats-card-4 {
            #background: linear-gradient(135deg, #00BFFF 0%, #00BFFF 100%);
            background: #00BFFF;
            padding: 20px;
            border-radius: 12px;
            color: white;
            text-align: center;
            margin: 10px 0;
            #box-shadow: 0 4px 15px rgba(255,154,158,0.3);
            box-shadow: 0 4px 15px rgba(78,205,196,0.3);
        }

        .stats-card-4, 
        .stats-card-4 * {
            color: white ;
        }
        .stats-card-4:hover {
            transform: translateY(-3px);
            box-shadow: 0 12px 40px rgba(79, 172, 254, 0.5);
        }

        
        .footer {
            background: linear-gradient(135deg, #2c3e50 0%, #34495e 100%);
            padding: 20px;
            border-radius: 10px;
            color: white;
            text-align: center;
            margin-top: 30px;
        }
        
        .click-instruction {
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            padding: 15px;
            border-radius: 8px;
            color: white;
            text-align: center;
            margin: 15px 0;
            box-shadow: 0 4px 15px rgba(102,126,234,0.3);
            font-size: 18px;
            font-weight: bold;
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
# Load and prepare the dataset
@st.cache_data
def load_data():
    # Load historical data
    df1 = pd.read_csv("data/sample_temp_1950-2025_1.csv")
    df2 = pd.read_csv("data/sample_temp_1950-2025_2.csv")
    df = pd.concat([df1, df2], axis=0).reset_index(drop=True)
    df.fillna("NA", inplace=True)
    df.columns = df.columns.str.lower()

    if 'latitude' not in df.columns:
        df['latitude'] = df['lat']
    if 'lng' not in df.columns and 'longitude' in df.columns:
        df['lng'] = df['longitude']

    df['country_name'] = df['country'].map(country_mapping)
    
    # Load prediction data
    df_pred = pd.read_csv("data/monthly_pred_temp_2025-2029.csv")
    df_pred.columns = df_pred.columns.str.lower()

    # Parse the date column (mm-year format like "Jul-2025")
    df_pred['date_parsed'] = pd.to_datetime(df_pred['date'], format='%b-%Y')
    df_pred['year'] = df_pred['date_parsed'].dt.year
    df_pred['month'] = df_pred['date_parsed'].dt.month
    df_pred['month_name'] = df_pred['date_parsed'].dt.strftime('%b')

    if 'latitude' not in df_pred.columns:
        df_pred['latitude'] = df_pred['lat']
    if 'lng' not in df_pred.columns and 'longitude' in df_pred.columns:
        df_pred['lng'] = df_pred['longitude']

    df_pred['country_name'] = df_pred['country'].map(country_mapping)
    
    return df, df_pred

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

def calculate_prediction_anomaly(df_pred, baseline_temps):
    """Calculate temperature anomaly for prediction data using historical baseline"""
    anomaly_df = df_pred.copy()
    
    # Merge with baseline temperatures
    anomaly_df = anomaly_df.merge(baseline_temps, on='city', how='left')
    
    # Calculate anomaly
    anomaly_df['temperature_anomaly'] = anomaly_df['temperature'] - anomaly_df['baseline_temp']
    
    return anomaly_df

def generate_climate_narrative(city_data, city_name, country_name):
    """Generate dynamic climate narrative based on 1980s trend and baseline comparison"""
    if city_data.empty:
        return ""
    
    # Calculate trends and anomalies
    recent_years = city_data[city_data['year'] >= 2015]
    early_years = city_data[city_data['year'] <= 1980]
    
    if recent_years.empty or early_years.empty:
        return ""
    
    # Temperature change since 1980s
    recent_avg = recent_years['temperature'].mean()
    early_avg = early_years['temperature'].mean()
    temp_change = recent_avg - early_avg
    
    # Latest year and baseline comparison
    latest_year = city_data['year'].max()
    latest_temp = city_data.loc[city_data['year'] == latest_year, 'temperature'].mean()
    baseline_temp = city_data['baseline_temp'].iloc[0]
    latest_anomaly = city_data.loc[city_data['year'] == latest_year, 'temperature_anomaly'].iloc[0]
    
    # Determine trend relative to baseline
    baseline_diff = latest_temp - baseline_temp
    if baseline_diff > 0.2:
        baseline_trend = "increased"
    elif baseline_diff < -0.2:
        baseline_trend = "decreased"
    else:
        baseline_trend = "remained relatively constant"
    
    # Select narrative class
    if temp_change > 2.0:
        narrative_class = "climate-warning"
        emoji = "🔥"
        title = "CRITICAL TEMPERATURE RISE DETECTED"
        message = f"""
        <div class="{narrative_class}">
            <h3>{emoji} {title} {emoji}</h3>
            <p><strong>{city_name}, {country_name}</strong> has experienced a significant temperature increase of 
            <strong>{temp_change:.1f}°C</strong> since the 1980s!</p>
            <p>Current anomaly: In <strong>{latest_year}</strong>, the recored average temperature 
            (<strong>{latest_temp:.1f}°C</strong>) has <strong>{baseline_trend}</strong> by 
            <strong>{baseline_diff:+.1f}°C</strong> compared to the 1961–1990 baseline 
            (<strong>{baseline_temp:.1f}°C</strong>).</p>
            <p> This aligns with <strong>SDG 13: Climate Action</strong> - urgent action needed!</p>
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
            <p>Current anomaly: In <strong>{latest_year}</strong>, the recored average temperature 
            (<strong>{latest_temp:.1f}°C</strong>) has <strong>{baseline_trend}</strong> by 
            <strong>{baseline_diff:+.1f}°C</strong> compared to the 1961–1990 baseline 
            (<strong>{baseline_temp:.1f}°C</strong>).</p>
            <p>This relates to <strong>SDG 13: Climate Action</strong> and 
            <strong>SDG 11: Sustainable Cities</strong>.</p>
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
            <p>Current anomaly: In <strong>{latest_year}</strong>, the recored average temperature 
            (<strong>{latest_temp:.1f}°C</strong>) has <strong>{baseline_trend}</strong> by 
            <strong>{baseline_diff:+.1f}°C</strong> compared to the 1961–1990 baseline 
            (<strong>{baseline_temp:.1f}°C</strong>).</p>
            <p>🌱 Continue supporting <strong>SDG 13: Climate Action</strong> to maintain stability!</p>
        </div>
        """
    
    return message

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
        showscale=False,
        hovertemplate='<b>%{y}</b><br>' +
                      'Year: %{x}<br>' +
                      'Anomaly: %{z:.2f}°C<br>' +
                      '<extra></extra>'
    ))
    
    fig.update_layout(
        title=f"Historical Heatmap Temperature Anomalies for {selected_city}",
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

def create_yearly_monthly_trend_chart(df_pred, selected_city, selected_year):
    """Create a line chart showing monthly predicted temperature trends for a specific year"""
    if not selected_city or not selected_year:
        return None
    
    city_data = df_pred[(df_pred['city'] == selected_city) & (df_pred['year'] == selected_year)].copy()
    
    if city_data.empty:
        return None
    
    # Sort by month to ensure proper order
    city_data = city_data.sort_values('month')
    
    fig = go.Figure()
    
    # Add predicted temperature line
    fig.add_trace(go.Scatter(
        x=city_data['month_name'],
        y=city_data['temperature'],
        mode='lines+markers',
        name=f'Predicted Temperature {selected_year}',
        line=dict(color='#FF8C00', width=3),
        marker=dict(size=8, color='#FF8C00'),
        hovertemplate='Month: %{x}<br>Predicted Temperature: %{y:.1f}°C<extra></extra>'
    ))
    
    # Add trend line across months
    x_numeric = np.arange(len(city_data))
    z = np.polyfit(x_numeric, city_data['temperature'], 1)
    p = np.poly1d(z)
    fig.add_trace(go.Scatter(
        x=city_data['month_name'],
        y=p(x_numeric),
        mode='lines',
        name=f'Monthly Trend {selected_year}',
        line=dict(color='#DC143C', width=3, dash='dash'),
        hovertemplate='Month: %{x}<br>Trend: %{y:.1f}°C<extra></extra>'
    ))
    
    fig.update_layout(
        title=f"Monthly Temperature Predictions for {selected_city} - {selected_year}",
        plot_bgcolor='rgba(255,255,255,0.9)',
        paper_bgcolor='rgba(255,255,255,0.95)',
        margin=dict(l=40, r=40, t=60, b=40),
        xaxis_title="Month",
        yaxis_title="Temperature (°C)",
        height=400,
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

def create_yearly_monthly_heatmap(df_pred, selected_city, selected_year):
    """Create a monthly heatmap for a specific year showing temperature anomalies"""
    if not selected_city or not selected_year:
        return None
    
    # Filter data for selected city and year
    city_data = df_pred[(df_pred['city'] == selected_city) & (df_pred['year'] == selected_year)]
    
    if city_data.empty:
        return None
    
    # Sort by month
    city_data = city_data.sort_values('month')
    
    # Create heatmap with months on x-axis and single row
    fig = go.Figure(data=go.Heatmap(
        z=[city_data['temperature_anomaly'].values],
        x=city_data['month_name'].values,
        y=[selected_city],
        zmin=-3,
        zmax=3,
        colorscale='RdBu_r',
        showscale=True,
        colorbar=dict(title="Anomaly (°C)"),
        hovertemplate='<b>%{y}</b><br>' +
                      'Month: %{x}<br>' +
                      'Predicted Anomaly: %{z:.2f}°C<br>' +
                      '<extra></extra>'
    ))
    
    fig.update_layout(
        title=f"Heatmap Monthly Temperature Anomalies for {selected_city} - {selected_year}",
        paper_bgcolor='rgba(255,255,255,0.95)',
        margin=dict(l=40, r=40, t=60, b=40),
        xaxis_title="Month",
        yaxis=dict(showticklabels=False, gridcolor='rgba(0,0,0,0.1)'),
        height=400,
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
        name='Historical Temperature',
        line=dict(color='#4B9CD3', width=3),
        marker=dict(size=6, color='#4B9CD3'),
        hovertemplate='Year: %{x}<br>Temperature: %{y:.1f}°C<extra></extra>'
    ))
    
    # Add trend line
    z = np.polyfit(city_data['year'], city_data['temperature'], 1)
    p = np.poly1d(z)
    fig.add_trace(go.Scatter(
        x=city_data['year'],
        y=p(city_data['year']),
        mode='lines',
        name='Historical Trend',
        line=dict(color='#FF0000', width=4, dash='dash'),
        hovertemplate='Year: %{x}<br>Trend: %{y:.1f}°C<extra></extra>'
    ))
    
    fig.update_layout(
        title=f"Historical Temperature Trend for {selected_city}",
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

# Load data and calculate anomalies
df, df_pred = load_data()
df = calculate_temperature_anomaly(df)

# Calculate baseline temperatures for predictions
baseline_data = df[(df['year'] >= 1961) & (df['year'] <= 1990)]
baseline_temps = baseline_data.groupby('city')['temperature'].mean().reset_index()
baseline_temps.columns = ['city', 'baseline_temp']

# Calculate anomalies for prediction data
df_pred = calculate_prediction_anomaly(df_pred, baseline_temps)

# Display key statistics
latest_year = df['year'].max()
latest_data = df[df['year'] == latest_year]

with st.container():
    col1, col2, col3, col4 = st.columns(4)
    with col1:
        st.markdown(f"""
            <div class="stats-card-1">
                <h5>Cities and Towns Monitored</h5>
                <h2>{len(df['city'].unique())}</h2>
            </div>
        """, unsafe_allow_html=True)
    with col2:
        st.markdown(f"""
            <div class="stats-card-2">
                <h5>Countries Covered</h5>
                <h2>{len(df['country_name'].unique())}</h2>
            </div>
        """, unsafe_allow_html=True)
    with col3:
        avg_temp = latest_data['temperature'].mean()
        st.markdown(f"""
            <div class="stats-card-3">
                <h5>Average Temperature {latest_year}</h5>
                <h2>{avg_temp:.1f}°C</h2>
            </div>
        """, unsafe_allow_html=True)
    with col4:
        avg_anomaly = latest_data['temperature_anomaly'].mean()
        st.markdown(f"""
            <div class="stats-card-4">
                <h5>Average Anomaly {latest_year}</h5>
                <h2>{avg_anomaly:+.1f}°C</h2>
            </div>
        """, unsafe_allow_html=True)

st.markdown("""
        <div class="climate-info">
            <h4>🎯 Get Started:</h4>
            <p>Use the country and city selection boxes below to choose specific locations for analysis.</p>
            <p>Or click on any city point on the map above to begin your climate analysis journey!</p>
            <p>Explore how temperatures have changed over time and discover the impacts of climate change in Africa.</p>
        </div>
    """, unsafe_allow_html=True)

# Country and city selection (appears first for better UX)
countries = sorted(df['country_name'].dropna().unique())

# Create two columns for aligned filters
col1, col2 = st.columns(2)

with col1:
    selected_countries = st.multiselect(
        "Select countries to analyze:", 
        countries, 
        default=[],
        help="Choose one or more African countries to examine their climate data"
    )

# Filter cities based on selected countries
available_cities = df[df['country_name'].isin(selected_countries)]['city'].sort_values().unique() if selected_countries else []

with col2:
    selected_cities = st.multiselect(
        "Select cities for detailed analysis:", 
        available_cities, 
        default=[],
        help="Choose specific cities to analyze temperature trends and anomalies"
    )

# Default center and zoom
map_center = {"lat": 0, "lon": 20}
map_zoom = 2

# If only one city is selected, zoom into it
if len(selected_cities) == 1:
    city_info = df[df['city'] == selected_cities[0]].iloc[0]
    map_center = {"lat": city_info["latitude"], "lon": city_info["lng"]}
    map_zoom = 12

fig_map = px.scatter_mapbox(
    latest_data,
    lat="latitude",
    lon="lng",
    color="temperature",
    hover_name="city",
    hover_data={"temperature": ":.1f", "country_name": True},
    center=map_center,
    zoom=map_zoom,
    #mapbox_style="open-street-map",
    mapbox_style="carto-positron",
    color_continuous_scale="RdBu_r",
)

# Set marker size after creation
fig_map.update_traces(marker=dict(size=13))
fig_map.update_layout(height=700, width=1500, margin=dict(l=0, r=0, t=30, b=0))
fig_map.update_layout(
    coloraxis_colorbar=dict(
        title="Average Temperature(°C) 2025",
        title_side='top',
        title_font=dict(
            color='black',        
            size=14              
        ),
        tickfont=dict(
            color='black',     
            size=12            
        ),
        x=0.70,                 
        y=0.05,                 
        xanchor='left',
        yanchor='bottom',
        orientation='h',        
        len=0.3,                
        thickness=15            
    )
)
fig_map.update_layout(
    margin=dict(l=0, r=0, t=0, b=0),
    paper_bgcolor="rgba(0,0,0,0)",
    plot_bgcolor="rgba(0,0,0,0)",
)

# Display the map and capture click events
map_click = st.plotly_chart(fig_map, use_container_width=True, on_select="rerun")

# Handle map click events
if map_click and map_click.selection and map_click.selection.points:
    # Get the clicked point
    clicked_point = map_click.selection.points[0]
    
    # Find the city based on the clicked point's hover_name
    if 'hovertext' in clicked_point:
        clicked_city = clicked_point['hovertext']
        st.session_state.selected_city = clicked_city
    elif 'customdata' in clicked_point:
        # Alternative method to get city name
        point_index = clicked_point['point_index']
        if point_index < len(latest_data):
            clicked_city = latest_data.iloc[point_index]['city']
            st.session_state.selected_city = clicked_city

# Function to display city analysis
def display_city_analysis(city, df, df_pred):
    """Display complete analysis for a single city"""
    city_data = df[df['city'] == city]
    city_pred_data = df_pred[df_pred['city'] == city]
    
    if city_data.empty:
        return

    country_name = city_data['country_name'].iloc[0]

    st.markdown(f"""
        <div class="subtitle">
            Detailed Climate Analysis for {city}, {country_name}
        </div>
    """, unsafe_allow_html=True)

    # Historical Analysis Section
    st.markdown("### Historical Analysis (1950-2025)")
    col1, col2 = st.columns(2)

    with col1:
        trend_chart = create_temperature_trend_chart(df, city)
        if trend_chart:
            st.plotly_chart(trend_chart, use_container_width=True)

    with col2:
        heatmap = create_climate_heatmap(df, city)
        if heatmap:
            st.plotly_chart(heatmap, use_container_width=True)

    # Display narrative
    narrative = generate_climate_narrative(city_data, city, country_name)
    if narrative:
        st.markdown(narrative, unsafe_allow_html=True)
    
    # Prediction Analysis Section
    if not city_pred_data.empty:
        st.markdown("### Future Predictions (2025-2029)")
        
        # Year selection dropdown
        available_years = sorted(city_pred_data['year'].unique())
        
        col_year, col_space = st.columns([1, 3])
        with col_year:
            selected_year = st.selectbox(
                f"Select year for {city}:",
                available_years,
                index=0,
                key=f"year_selector_{city}"
            )
        
        if selected_year:
            # Display monthly analysis for selected year
            col3, col4 = st.columns(2)
            
            with col3:
                # Monthly trend chart
                monthly_trend_chart = create_yearly_monthly_trend_chart(df_pred, city, selected_year)
                if monthly_trend_chart:
                    st.plotly_chart(monthly_trend_chart, use_container_width=True)
            
            with col4:
                # Monthly heatmap
                monthly_heatmap = create_yearly_monthly_heatmap(df_pred, city, selected_year)
                if monthly_heatmap:
                    st.plotly_chart(monthly_heatmap, use_container_width=True)
            
            # Year summary statistics
            year_data = city_pred_data[city_pred_data['year'] == selected_year]
            if not year_data.empty:
                avg_temp = year_data['temperature'].mean()
                avg_anomaly = year_data['temperature_anomaly'].mean()
                hottest_month = year_data.loc[year_data['temperature'].idxmax(), 'month_name']
                hottest_temp = year_data['temperature'].max()
                coolest_month = year_data.loc[year_data['temperature'].idxmin(), 'month_name']
                coolest_temp = year_data['temperature'].min()
                
                st.markdown(f"""
                    <div class="climate-info">
                        <h4> {selected_year} Summary for {city}</h4>
                        <p><strong>Average Temperature:</strong> {avg_temp:.1f}°C</p>
                        <p><strong>Average Anomaly:</strong> {avg_anomaly:+.1f}°C above 1961-1990 baseline</p>
                        <p><strong>Hottest Month:</strong> {hottest_month} ({hottest_temp:.1f}°C)</p>
                        <p><strong>Coolest Month:</strong> {coolest_month} ({coolest_temp:.1f}°C)</p>
                        <p><strong>Temperature Range:</strong> {hottest_temp - coolest_temp:.1f}°C</p>
                    </div>
                """, unsafe_allow_html=True)

# Display analysis for selected city from map click (only if actually clicked)
if st.session_state.selected_city is not None:
    selected_city = st.session_state.selected_city
    display_city_analysis(selected_city, df, df_pred)
    
    # Add button to clear selection
    if st.button("Clear Selection", key="clear_selection_map"):
        st.session_state.selected_city = None
        st.rerun()

# Display analysis for cities selected from multiselect (only if cities are selected)
if selected_cities:
    for city in selected_cities:
        display_city_analysis(city, df, df_pred)

# Footer information
st.markdown("---")
st.markdown("""
    <div class="climate-info">
        <h4> About this analysis</h4>
        <p><strong>Historical Data:</strong> Temperature records from 1950-2025 showing long-term climate trends</p>
        <p><strong>Prediction Data:</strong> Monthly forecasts from 2025-2029 using advanced climate modeling</p>
        <p><strong>Temperature Anomalies:</strong> Calculated relative to 1961-1990 baseline period (WMO standard)</p>
        <p><strong>Color Scale:</strong> Blue indicates cooler than average, red indicates warmer than average</p>
        <p>This tool supports <strong>SDG 13: Climate Action</strong> by providing accessible climate data for decision-making.</p>
    </div>
""", unsafe_allow_html=True)

st.info("""
**ℹ️ Monthly Anomaly Note**  
Monthly anomalies are calculated relative to the historical **annual** baseline due to lack of monthly historical data.  
These anomalies indicate **overall warming trends** but may not capture **seasonal variations** precisely.
""")

# SDG Information Section
with st.container():
    st.markdown("""
    <div class="sdg-header" style="text-align:center;">
        🎯 Supporting UN Sustainable Development Goals 🎯 
    </div>
""", unsafe_allow_html=True)


    col1, col2, col3 = st.columns(3)
    with col1:
        st.markdown("""
            <div class="sdg-card">
                <h4>🌍 SDG 13: Climate Action</h4>
                <p>Take urgent action to combat climate change and its impacts through monitoring trends and promoting awareness.</p>
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
        <h3 style="color: black;">🌱 Take Climate Action Today!</h3>
        <p>Support renewable energy, reduce carbon footprint, and advocate for climate policies. Small and smart choices to mitigate increasing temperatures:</p>
        <ul style="color: black;">
          <li>Create green spaces like parks, urban forests, rooftop gardens, community gardens, and green roofs or walls.</li>
          <li>Plant native species to promote biodiversity.</li>
          <li>Use renewable energy sources and improve energy efficiency.</li>
          <li>Walk, bike, or take public transport to reduce greenhouse gas emissions.</li>
          <li>Reduce, reuse, repair, and recycle to lower your carbon footprint.</li>
          <li>Advocate for change: speak up and encourage others to take action.</li>
        </ul>

    </div>

""", unsafe_allow_html=True)

st.markdown("---")

# Footer
st.markdown("""
    <div class="footer">
        <h4 style="color: white;" >🌍 Climate Map Africa Dashboard</h4>
        <p>Data source: <a href="https://cds.climate.copernicus.eu/" target="_blank" style="color: #4ECDC4;">Copernicus Climate Data Store</a></p>
        <p>Supporting UN SDGs: Climate Action (13) • Sustainable Cities (11) • Partnerships (17)</p>
        <p>🤝 Together, we can build a sustainable future for Africa and the world!</p>
    </div>
""", unsafe_allow_html=True)
