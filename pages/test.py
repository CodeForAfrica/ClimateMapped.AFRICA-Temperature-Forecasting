import streamlit as st
import pandas as pd
import geopandas as gpd
import plotly.express as px
from shapely.geometry import Point

# Load Data
@st.cache_data
def load_data():
    df = pd.read_csv("data/sample_temp_1950-2025.csv")
    df.columns = df.columns.str.lower()
    if 'latitude' not in df.columns:
        df['latitude'] = df['lat']
    return df

df = load_data()

st.title("🌡️ Choropleth Temperature Map of African Cities")

# Sidebar filter
st.sidebar.header("Filters")
year_selected = st.sidebar.slider("Select Year", int(df['year'].min()), int(df['year'].max()), step=1)

# Filter data
df_year = df[df['year'] == year_selected].copy()

# Convert to GeoDataFrame
gdf = gpd.GeoDataFrame(
    df_year,
    geometry=gpd.points_from_xy(df_year['lng'], df_year['latitude']),
    crs="EPSG:4326"
)

# Project to meters (for buffer calculation)
gdf = gdf.to_crs(epsg=3857)
gdf['geometry'] = gdf.buffer(50000)  # 50 km buffer
gdf = gdf.to_crs(epsg=4326)

# Convert to GeoJSON-like structure
gjson = gdf.__geo_interface__

# Plot as a true choropleth using Plotly
fig = px.choropleth_mapbox(
    gdf,
    geojson=gjson,
    locations=gdf.index,
    color='temperature',
    hover_name='city',
    color_continuous_scale='RdBu_r',  # Climate stripes style
    mapbox_style='carto-positron',
    zoom=2.5,
    center={"lat": 0, "lon": 20},
    opacity=0.7
)

fig.update_layout(margin={"r":0,"t":0,"l":0,"b":0})
st.plotly_chart(fig, use_container_width=True)

# Footer
st.markdown("🧭 This map shows each city as a 50 km zone colored by its average temperature.")
st.markdown("📊 Data source: `sample_temp_1950-2025.csv`")
