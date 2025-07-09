import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
import numpy as np

st.set_page_config(layout="wide")

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

    df['country_name'] = df['country'].map(country_mapping).fillna(df['country'])
    return df
    

def create_climate_heatmap(df, selected_cities):
    """Create a climate stripes style heatmap for selected cities"""
    if not selected_cities:
        return go.Figure()
    
    # Filter data for selected cities
    filtered_df = df[df['city'].isin(selected_cities)]
    
    # Create pivot table for heatmap
    pivot_df = filtered_df.pivot_table(
        index='city', 
        columns='year', 
        values='temperature',
        aggfunc='mean'
    )
    
    # Determine global temperature range for color consistency
    global_min = df['temperature'].min()
    global_max = df['temperature'].max()
    
    # Create heatmap with global temperature scale
    fig = go.Figure(data=go.Heatmap(
        z=pivot_df.values,
        x=pivot_df.columns,
        y=pivot_df.index,
        zmin=global_min,
        zmax=global_max,
        colorscale='RdBu_r',
        showscale=True,
        colorbar=dict(title="Temperature (°C)"),
        hovertemplate='<b>%{y}</b><br>' +
                      'Year: %{x}<br>' +
                      'Temperature: %{z:.1f}°C<br>' +
                      '<extra></extra>'
    ))
    
    fig.update_layout(
        title="Temperature by City and Year (Standardized Scale)",
        xaxis_title="Year",
        yaxis_title="City",
        height=max(300, len(selected_cities) * 40)
    )
    
    return fig

# Initialize session state for selected city
if 'selected_city' not in st.session_state:
    st.session_state.selected_city = None
if 'selected_country' not in st.session_state:
    st.session_state.selected_country = None

# Load data
df = load_data()

st.markdown("""
    <style>
        .main-title {
            background-color: #ADD8E6;
            padding: 20px;
            border-radius: 10px;
            text-align: center;
            color: black;
            font-size: 36px;
            font-weight: bold;
            margin-bottom: 20px;
        }
    </style>
    <div class="main-title">Climate Map Africa</div>
""", unsafe_allow_html=True)

# Get latest year in the dataset
latest_year = df['year'].max()
latest_data = df[df['year'] == latest_year]

# 1. Interactive OpenStreetMap showing city temperatures
st.markdown("### 🌍 Interactive Temperature Map")
st.markdown("**Click on any city to see detailed climate analysis**")

fig_map = px.scatter_mapbox(
    latest_data,
    lat="latitude",
    lon="lng",
    color="temperature",
    hover_name="city",
    hover_data={
        "temperature": ":.1f",
        "country_name": True,
        "lat": False,
        "lng": False
    },
    center={"lat": 0, "lon": 20},
    zoom=2,
    mapbox_style="open-street-map",
    color_continuous_scale="RdBu_r",
    title=f"Average Temperature in {latest_year} - Click on a city for details"
)

# Force marker size and remove size from hover
fig_map.update_traces(marker=dict(size=8))

# Display the map and capture click events
clicked_data = st.plotly_chart(fig_map, use_container_width=True, on_select="rerun")

# Check if a point was clicked
if clicked_data and "selection" in clicked_data and clicked_data["selection"]["points"]:
    clicked_point = clicked_data["selection"]["points"][0]
    point_index = clicked_point["point_index"]
    
    # Get the city data for the clicked point
    st.session_state.selected_city = latest_data.iloc[point_index]['city']
    st.session_state.selected_country = latest_data.iloc[point_index]['country_name']

# Display detailed analysis if a city is selected
if st.session_state.selected_city:
    st.markdown("---")
    
    # Header for selected city
    col_header, col_clear = st.columns([4, 1])
    with col_header:
        st.markdown(f"## 📊 Climate Analysis: {st.session_state.selected_city}, {st.session_state.selected_country}")
    with col_clear:
        if st.button("🔄 Clear Selection", type="secondary"):
            st.session_state.selected_city = None
            st.session_state.selected_country = None
            st.rerun()
    
    # Filter data for the selected city
    city_data = df[df['city'] == st.session_state.selected_city].copy()
    
    # Calculate temperature statistics
    current_temp = city_data[city_data['year'] == latest_year]['temperature'].iloc[0] if not city_data[city_data['year'] == latest_year].empty else None
    avg_temp = city_data['temperature'].mean()
    max_temp = city_data['temperature'].max()
    min_temp = city_data['temperature'].min()
    
    # Display key metrics
    metric_col1, metric_col2, metric_col3, metric_col4 = st.columns(4)
    
    with metric_col1:
        st.metric("Current Temperature", f"{current_temp:.1f}°C" if current_temp else "N/A")
    with metric_col2:
        st.metric("Average Temperature", f"{avg_temp:.1f}°C")
    with metric_col3:
        st.metric("Highest Recorded", f"{max_temp:.1f}°C")
    with metric_col4:
        st.metric("Lowest Recorded", f"{min_temp:.1f}°C")
    
    # Create detailed plots
    plot_col1, plot_col2 = st.columns(2)
    
    with plot_col1:
        # Temperature trend over time
        fig_temp = px.line(
            city_data, 
            x='year', 
            y='temperature',
            title=f'Temperature Trend Over Time',
            labels={'temperature': 'Temperature (°C)', 'year': 'Year'},
            markers=True
        )
        fig_temp.update_traces(line=dict(color='#1f77b4', width=2))
        fig_temp.update_layout(height=400)
        st.plotly_chart(fig_temp, use_container_width=True)
    
    with plot_col2:
        # Temperature distribution
        fig_hist = px.histogram(
            city_data, 
            x='temperature',
            nbins=20,
            title=f'Temperature Distribution',
            labels={'temperature': 'Temperature (°C)', 'count': 'Frequency'},
            color_discrete_sequence=['#ff7f0e']
        )
        fig_hist.update_layout(height=400)
        st.plotly_chart(fig_hist, use_container_width=True)
    
    # Additional analysis
    plot_col3, plot_col4 = st.columns(2)
    
    with plot_col3:
        # Temperature by decade
        city_data['decade'] = (city_data['year'] // 10) * 10
        decade_avg = city_data.groupby('decade')['temperature'].mean().reset_index()
        
        fig_decade = px.bar(
            decade_avg, 
            x='decade', 
            y='temperature',
            title=f'Average Temperature by Decade',
            labels={'temperature': 'Temperature (°C)', 'decade': 'Decade'},
            color='temperature',
            color_continuous_scale='RdBu_r'
        )
        fig_decade.update_layout(height=400)
        st.plotly_chart(fig_decade, use_container_width=True)
    
    with plot_col4:
        # Temperature anomaly (if available)
        if 'temperature_anomaly' in city_data.columns:
            fig_anomaly = px.line(
                city_data, 
                x='year', 
                y='temperature_anomaly',
                title=f'Temperature Anomaly Over Time',
                labels={'temperature_anomaly': 'Temperature Anomaly (°C)', 'year': 'Year'},
                markers=True
            )
            fig_anomaly.update_traces(line=dict(color='red', width=2))
            fig_anomaly.add_hline(y=0, line_dash="dash", line_color="gray", annotation_text="Baseline")
            fig_anomaly.update_layout(height=400)
            st.plotly_chart(fig_anomaly, use_container_width=True)
        else:
            # Temperature change rate
            city_data_sorted = city_data.sort_values('year')
            city_data_sorted['temp_change'] = city_data_sorted['temperature'].diff()
            
            fig_change = px.bar(
                city_data_sorted[1:], 
                x='year', 
                y='temp_change',
                title=f'Year-over-Year Temperature Change',
                labels={'temp_change': 'Temperature Change (°C)', 'year': 'Year'},
                color='temp_change',
                color_continuous_scale='RdBu_r'
            )
            fig_change.update_layout(height=400)
            st.plotly_chart(fig_change, use_container_width=True)
    
    # Climate heatmap for the selected city
    st.markdown("### 🌡️ Temperature Timeline Heatmap")
    fig_city_heatmap = create_climate_heatmap(df, [st.session_state.selected_city])
    st.plotly_chart(fig_city_heatmap, use_container_width=True)

# 2. Multi-city comparison section
st.markdown("---")
st.markdown("""
        <style>
            .subtitle {
                background-color: #f0f0f0;
                padding: 10px;
                border-radius: 8px;
                text-align: center;
                color: #333333;
                font-size: 20px;
                font-weight: normal;
                margin-top: 10px;
                margin-bottom: 20px;
            }
        </style>
        <div class="subtitle">Multi-City Temperature Analysis</div>
""", unsafe_allow_html=True)

# Country selection
countries = sorted(df['country_name'].unique())
selected_countries = st.multiselect(
    "Select countries:", 
    countries, 
    default=countries[:1] if len(countries) > 1 else countries
)

# Filter cities based on selected countries
available_cities = df[df['country_name'].isin(selected_countries)]['city'].sort_values().unique()

# City selection (multiselect within selected countries)
selected_cities = st.multiselect(
    "Select cities:", 
    available_cities, 
    default=available_cities[:1] if len(available_cities) > 1 else available_cities
)

if selected_cities:
    # Climate Heatmap for multiple cities
    fig_heatmap = create_climate_heatmap(df, selected_cities)
    st.plotly_chart(fig_heatmap, use_container_width=True)
else:
    st.info("Please select at least one city to display the temperature trends and heatmap.")

# Footer
st.markdown("---")
st.markdown("""
    <div style="text-align: center; color: white;">
        <h4 style="color: white;">🌍 Climate Map Africa Dashboard</h4>
        <p>Data source: <a href="https://cds.climate.copernicus.eu/" target="_blank" style="color: #4ECDC4;">Copernicus Climate Data Store</a></p>
        <p>Supporting UN SDGs: Climate Action (13) • Sustainable Cities (11) • Partnerships (17)</p>
        <p>🤝 Together, we can build a sustainable future for Africa and the world!</p>
    </div>
""", unsafe_allow_html=True)
