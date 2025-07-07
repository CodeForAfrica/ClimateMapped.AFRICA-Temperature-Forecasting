import streamlit as st
import pandas as pd
import plotly.express as px

# Load and prepare the dataset
@st.cache_data
def load_data():
    df = pd.read_csv("data/sample_temp_1950-2025.csv")
    df.columns = df.columns.str.lower()
    
    # Ensure latitude and longitude columns exist
    if 'latitude' not in df.columns:
        df['latitude'] = df['lat']
    if 'lng' not in df.columns and 'longitude' in df.columns:
        df['lng'] = df['longitude']
        
    return df

df = load_data()

st.title("🌍 African Cities Temperature Dashboard")

# Find the most recent year in the dataset
latest_year = df['year'].max()

# Filter the data for the latest year
latest_data = df[df['year'] == latest_year]

# 1. OpenStreetMap showing temperatures by city
st.subheader(f"📍 City Temperatures in Africa ({latest_year})")

# Plotting city points on an OpenStreetMap using Plotly
fig_map = px.scatter_mapbox(
    latest_data,
    lat="latitude",
    lon="lng",
    color="temperature",
    size="temperature",
    hover_name="city",
    zoom=3,
    mapbox_style="open-street-map",
    color_continuous_scale="thermal",
    title=f"African Cities Temperature Map ({latest_year})"
)

st.plotly_chart(fig_map, use_container_width=True)

# 2. Temperature trend over the years
st.subheader("📈 Average Temperature Over the Years")

# Group by year and calculate average temperature
avg_temp_per_year = df.groupby('year')['temperature'].mean().reset_index()

# Line chart showing the temperature trend
fig_trend = px.line(
    avg_temp_per_year,
    x='year',
    y='temperature',
    markers=True,
    title="Average Temperature Trend Over the Years"
)

st.plotly_chart(fig_trend, use_container_width=True)

# Footer
st.markdown("Data source: `africa_temperatures.csv`")
