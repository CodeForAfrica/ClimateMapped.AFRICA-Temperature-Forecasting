import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
import numpy as np

st.set_page_config(layout="wide")

# Country code to country name mapping for African countries
country_mapping = { ... }  # (keep your existing dictionary)

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

    # Calculate baseline average (1961-1990)
    baseline = df[(df['year'] >= 1961) & (df['year'] <= 1990)]
    baseline_avg = baseline.groupby('city')['temperature'].mean().reset_index()
    baseline_avg.rename(columns={'temperature': 'baseline_temp'}, inplace=True)

    # Merge to main df to compute anomaly
    df = df.merge(baseline_avg, on='city', how='left')
    df['temp_anomaly'] = df['temperature'] - df['baseline_temp']

    return df

def create_climate_heatmap(df, selected_cities):
    if not selected_cities:
        return go.Figure()

    filtered_df = df[df['city'].isin(selected_cities)]
    pivot_df = filtered_df.pivot_table(index='city', columns='year', values='temperature', aggfunc='mean')
    global_min = df['temperature'].min()
    global_max = df['temperature'].max()

    fig = go.Figure(data=go.Heatmap(
        z=pivot_df.values,
        x=pivot_df.columns,
        y=pivot_df.index,
        zmin=global_min,
        zmax=global_max,
        colorscale='RdBu_r',
        showscale=True,
        colorbar=dict(title="Temperature (\u00b0C)"),
        hovertemplate='<b>%{y}</b><br>Year: %{x}<br>Temperature: %{z:.1f}\u00b0C<extra></extra>'
    ))

    fig.update_layout(
        title="Climate Stripes Heatmap",
        xaxis_title="Year",
        yaxis_title="City",
        height=max(300, len(selected_cities) * 40)
    )

    return fig

# Load data
df = load_data()

# Hero section
st.markdown("""
    <style>
        .main-title {
            background-color: #DFF0FF;
            padding: 20px;
            border-radius: 10px;
            text-align: center;
            color: #003366;
            font-size: 38px;
            font-weight: bold;
        }
    </style>
    <div class="main-title">Africa Climate Dashboard 🌍</div>
""", unsafe_allow_html=True)

st.markdown("""
Welcome to the Africa Climate Dashboard. This tool helps explore long-term temperature trends across African cities.
It integrates SDG 13 (Climate Action) and presents temperature anomalies relative to a 1961-1990 baseline.
""")

latest_year = df['year'].max()
latest_data = df[df['year'] == latest_year]

st.subheader(f"📍 Map of African Cities ({latest_year})")
fig_map = px.scatter_mapbox(
    latest_data,
    lat="latitude",
    lon="lng",
    color="temperature",
    size=[5] * len(latest_data),
    hover_name="city",
    zoom=3,
    mapbox_style="open-street-map",
    color_continuous_scale="RdBu_r",
    title=f"Average Temperature in {latest_year}"
)
fig_map.update_traces(marker=dict(size=6))
st.plotly_chart(fig_map, use_container_width=True, height=700)

st.markdown("""
---
### 🌡️ Explore Trends by Country and City
""")

countries = sorted(df['country_name'].unique())
selected_countries = st.multiselect("Select countries:", countries, default=countries[:1])
available_cities = df[df['country_name'].isin(selected_countries)]['city'].sort_values().unique()
selected_cities = st.multiselect("Select cities:", available_cities, default=available_cities[:1])

if selected_cities:
    filtered_df = df[df['city'].isin(selected_cities)]

    # Line chart for anomaly
    st.subheader("🔍 Temperature Trends and Anomalies")
    fig_line = go.Figure()
    warning_shown = False

    for city in selected_cities:
        city_data = filtered_df[filtered_df['city'] == city]
        fig_line.add_trace(go.Scatter(
            x=city_data['year'],
            y=city_data['temp_anomaly'],
            mode='lines+markers',
            name=city,
            line=dict(dash='dash')
        ))

        # Warning if anomaly > 1.5C in last 5 years
        recent_anomaly = city_data[city_data['year'] >= latest_year - 5]['temp_anomaly'].mean()
        if recent_anomaly >= 1.5:
            st.warning(f"Warning: Temperature anomaly in **{city}** over the last 5 years exceeds **1.5°C**! 🚨")
            warning_shown = True

    fig_line.update_layout(
        title="Temperature Anomalies (relative to 1961-1990 baseline)",
        xaxis_title="Year",
        yaxis_title="Temperature Anomaly (°C)",
        template="plotly_white"
    )

    st.plotly_chart(fig_line, use_container_width=True)

    # Heatmap
    st.subheader("🌌 Climate Stripes View")
    fig_heatmap = create_climate_heatmap(df, selected_cities)
    st.plotly_chart(fig_heatmap, use_container_width=True)

    if not warning_shown:
        st.success("No critical anomalies detected in selected cities. 🌿")

else:
    st.info("Please select at least one city to see trends and heatmaps.")

st.markdown("""
---
#### 🌍 Learn More
- [UN SDG 13 - Climate Action](https://sdgs.un.org/goals/goal13)
- [Copernicus Climate Data Store](https://cds.climate.copernicus.eu/)
""")
