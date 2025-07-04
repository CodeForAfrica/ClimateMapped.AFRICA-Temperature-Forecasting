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

st.title("Global Temperature Dashboard (African Data)")

# Sidebar filters
st.sidebar.header("Filters")
year_selected = st.sidebar.slider("Select Year", int(df['year'].min()), int(df['year'].max()), step=1)

# 1. Global Map (scatter) with climate stripes colors
st.subheader("Temperature Map (Cities Across the Globe)")

df_year = df[df['year'] == year_selected]

fig_map = px.scatter_geo(
    df_year,
    lat='latitude',
    lon='lng',
    color='temperature',
    hover_name='city',
    color_continuous_scale='RdBu_r',  # Blue to red (cool to warm)
    projection="natural earth",
    title=f"Temperature Map for Cities in {year_selected}",
    range_color=[df['temperature'].min(), df['temperature'].max()]
)

fig_map.update_geos(showcoastlines=True, showland=True, fitbounds="locations")
st.plotly_chart(fig_map, use_container_width=True)

# 2. Heatmap (City vs Year)
st.subheader("Temperature Heatmap Over Years")

pivot = df.pivot_table(index='city', columns='year', values='temperature')
fig_heatmap = px.imshow(
    pivot,
    labels=dict(x="Year", y="City", color="Temperature"),
    aspect="auto",
    color_continuous_scale='RdBu_r'  # Use climate stripes coloring
)

st.plotly_chart(fig_heatmap, use_container_width=True)

# 3. Line chart: Decadal Anomaly
st.subheader("Temperature Anomaly by Decade")

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
st.markdown("🌍 This dashboard shows temperature trends using African city data on a global map.\
 Data source: `sample_temp_1950-2025.csv`")
