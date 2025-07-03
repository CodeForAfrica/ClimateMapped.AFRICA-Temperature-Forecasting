import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px

# Load Data
@st.cache_data
def load_data():
    path = "data/annual_temp_1950-2025 (1).csv"
    df = pd.read_csv(path)
    # Ensure consistent column names
    df.columns = df.columns.str.lower()
    if 'latitude' not in df.columns:
        df['latitude'] = df['lat']
    return df

df = load_data()

st.title("African Cities Temperature Dashboard")

# Sidebar
st.sidebar.header("Filters")
year_selected = st.sidebar.slider("Select Year", int(df['year'].min()), int(df['year'].max()), step=1)

# 1. Choropleth Map of Temperatures
st.subheader("African Cities Temperature Map")

df_year = df[df['year'] == year_selected]

fig_map = px.scatter_geo(
    df_year,
    lat='latitude',
    lon='lng',
    color='temperature',
    hover_name='city',
    color_continuous_scale='thermal',
    projection="natural earth",
    title=f"Temperature Map for African Cities in {year_selected}"
)

fig_map.update_geos(fitbounds="locations", visible=False)
st.plotly_chart(fig_map, use_container_width=True)

# 2. Heatmap of Temperature over Years
st.subheader("Temperature Heatmap Over Years")

pivot = df.pivot_table(index='city', columns='year', values='temperature')
fig_heatmap = px.imshow(
    pivot,
    labels=dict(x="Year", y="City", color="Temperature"),
    aspect="auto",
    color_continuous_scale="YlOrRd"
)

st.plotly_chart(fig_heatmap, use_container_width=True)

# 3. Line Chart: Temperature Anomaly by Decade
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

st.plotly_chart(fig_line, use_container_width=True)

# Footer
st.markdown("Data source: Your dataset file `annual_temp_1950-2025 (1).csv`")


