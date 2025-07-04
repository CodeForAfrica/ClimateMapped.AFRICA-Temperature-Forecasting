import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px

# Load Data
@st.cache_data
def load_data():
    path = "data/sample_temp_1950-2025.csv"
    df = pd.read_csv(path)
    df.columns = df.columns.str.lower()
    if 'latitude' not in df.columns:
        df['latitude'] = df['lat']
    return df

df = load_data()

st.title("🌡️ Global Temperature Dashboard (African Data)")

# Sidebar filters
st.sidebar.header("Filters")
year_selected = st.sidebar.slider("Select Year", int(df['year'].min()), int(df['year'].max()), step=1)

# 1. Global Map with Climate Stripes Coloring (Simulated Choropleth)
st.subheader("Temperature Map (Simulated Choropleth View)")

df_year = df[df['year'] == year_selected]

fig_map = px.scatter_geo(
    df_year,
    lat='latitude',
    lon='lng',
    color='temperature',
    hover_name='city',
    color_continuous_scale='RdBu_r',
    projection="natural earth",
    size=np.full(len(df_year), 20),  # Uniform size for choropleth effect
)

fig_map.update_geos(
    showcoastlines=True,
    showland=True,
    landcolor="white",
    oceancolor="lightblue",
    bgcolor="white",
    fitbounds="locations"
)

fig_map.update_traces(marker=dict(line=dict(width=0)))  # No marker borders

st.plotly_chart(fig_map, use_container_width=True)

# 2. Heatmap (City vs Year)
st.subheader("Temperature Heatmap Over Years")

pivot = df.pivot_table(index='city', columns='year', values='temperature')
fig_heatmap = px.imshow(
    pivot,
    labels=dict(x="Year", y="City", color="Temperature"),
    aspect="auto",
    color_continuous_scale='RdBu_r'
)

st.plotly_chart(fig_heatmap, use_container_width=True)

# 3. Line Chart: Temperature Anomaly by Decade
st.subheader("Average Temperature Anomaly by Decade")

df['decade'] = (df['year'] // 10) * 10
decade_anomaly = df.groupby('decade')['temperature_anomaly'].mean().reset_index()

fig_line = px.line(
    decade_anomaly,
    x='decade',
    y='temperature_anomaly',
    markers=True,
    title="Average Temperature Anomaly by Decade"
)

fig_line.update_traces(line_color='crimson')
st.plotly_chart(fig_line, use_container_width=True)

# Footer
st.markdown("📊 Data Source: `sample_temp_1950-2025.csv`")
st.markdown("💡 Map styled with white land, light blue oceans, and climate stripes color scale (blue = cold, red = warm).")
