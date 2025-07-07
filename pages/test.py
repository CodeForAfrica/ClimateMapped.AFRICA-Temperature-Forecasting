import streamlit as st
import pandas as pd
import plotly.express as px

# Load and prepare the dataset
@st.cache_data
def load_data():
    df = pd.read_csv("africa_temperatures.csv")
    df.columns = df.columns.str.lower()

    # Ensure latitude and longitude columns exist
    if 'latitude' not in df.columns:
        df['latitude'] = df['lat']
    if 'lng' not in df.columns and 'longitude' in df.columns:
        df['lng'] = df['longitude']
    
    return df

df = load_data()

st.title("Africa Temperature 2025")

# Get latest year in the dataset
latest_year = df['year'].max()
latest_data = df[df['year'] == latest_year]

# 1. OpenStreetMap showing city temperatures as fixed-size points
st.subheader(f"Temperature map of african cities ({latest_year})")

fig_map = px.scatter_mapbox(
    latest_data,
    lat="latitude",
    lon="lng",
    color="temperature",
    size_max=5,
    size=[5] * len(latest_data),  # fixed point size
    hover_name="city",
    zoom=3,
    mapbox_style="open-street-map",
    color_continuous_scale="RdBu_r",  # Climate strip style: blue to red
    title=f"Temperatures in African Cities ({latest_year})"
)

# Force marker size
fig_map.update_traces(marker=dict(size=6))
st.plotly_chart(fig_map, use_container_width=True)

# 2. Temperature trend line chart with city filter
st.subheader("Temperature trend over the years by city")

# City selection
cities = df['city'].sort_values().unique()
selected_cities = st.multiselect("Select cities to display:", cities, default=cities[:5])

# Filter data based on selected cities
filtered_df = df[df['city'].isin(selected_cities)]

# Plot line chart
fig_trend = px.line(
    filtered_df,
    x="year",
    y="temperature",
    color="city",  # Color by city for clarity
    markers=True,
    title="Temperature Evolution by City"
)

st.plotly_chart(fig_trend, use_container_width=True)

# Footer
st.markdown("Data source: `africa_temperatures.csv`")
