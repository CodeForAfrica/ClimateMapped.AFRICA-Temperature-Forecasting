import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go

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

# Load data
df = load_data()

# Set full-page layout
st.set_page_config(layout="wide")

st.title("Africa Temperature 2025")

# Get latest year for the map
latest_year = df['year'].max()
latest_data = df[df['year'] == latest_year]

# === 1. Temperature Map ===
st.subheader(f"📍 Temperature Map of African Cities ({latest_year})")

fig_map = px.scatter_mapbox(
    latest_data,
    lat="latitude",
    lon="lng",
    color="temperature",
    size_max=5,
    size=[5] * len(latest_data),  # fixed-size points
    hover_name="city",
    zoom=3,
    mapbox_style="open-street-map",
    color_continuous_scale="RdBu_r",
    title=f"Temperatures in African Cities ({latest_year})"
)

fig_map.update_traces(marker=dict(size=6))

st.plotly_chart(fig_map, use_container_width=True, height=700)

# === 2. City selection ===
st.subheader("Temperature trend by city")

cities = df['city'].sort_values().unique()
selected_cities = st.multiselect("Select cities to display:", cities, default=cities[:5])

filtered_df = df[df['city'].isin(selected_cities)]

# === 3. Dashed Line Chart ===
fig_line = go.Figure()

for city in selected_cities:
    city_df = filtered_df[filtered_df['city'] == city]
    fig_line.add_trace(
        go.Scatter(
            x=city_df['year'],
            y=city_df['temperature'],
            mode='lines+markers',
            name=city,
            line=dict(dash='dash')
        )
    )

fig_line.update_layout(
    title="Dashed Temperature Trend by City",
    xaxis_title="Year",
    yaxis_title="Temperature (°C)",
    template="plotly_white"
)

st.plotly_chart(fig_line, use_container_width=True)

# === 4. Climate Stripes Heatmap ===
# Pivot table: rows=cities, columns=years, values=temperature
heatmap_data = filtered_df.pivot_table(
    index='city',
    columns='year',
    values='temperature',
    aggfunc='mean'
)

fig_heatmap = px.imshow(
    heatmap_data,
    aspect="auto",
    color_continuous_scale="RdBu_r",
    labels=dict(color="Temperature (°C)"),
    title="Climate Stripes Heatmap"
)

fig_heatmap.update_layout(
    xaxis_title="Year",
    yaxis_title="City"
)

st.plotly_chart(fig_heatmap, use_container_width=True)

# Footer
st.markdown("🗂Data source: `data/sample_temp_1950-2025.csv`")
