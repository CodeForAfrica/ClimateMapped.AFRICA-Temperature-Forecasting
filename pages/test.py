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
    'EG': 'Egypt', 'GQ': 'Equatorial Guinea', 'ER': 'Eritrea', 'ET': 'Ethiopia',
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

# 1. OpenStreetMap showing city temperatures as fixed-size points
#st.subheader(f"Average Temperature 2025 ({latest_year})")
fig_map = px.scatter_mapbox(
    latest_data,
    lat="latitude",
    lon="lng",
    color="temperature",
    size_max=5,
    size=[5] * len(latest_data),
    hover_name="city",
    zoom=3,
    mapbox_style="open-street-map",
    color_continuous_scale="RdBu_r",
    title=f"Average Temperature in {latest_year}"
)
# Force marker size
fig_map.update_traces(marker=dict(size=6))
st.plotly_chart(fig_map, use_container_width=True)

# 2. Hierarchical filters: Country -> Cities
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
        <div class="subtitle">Temperature Trends</div>
""", unsafe_allow_html=True)

#st.subheader("Temperature trend over the years by city")

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
    "Select cities :", 
    available_cities, 
    default=available_cities[:1] if len(available_cities) > 1 else available_cities
)

if selected_cities:
    ## Filter data based on selected cities
    #filtered_df = df[df['city'].isin(selected_cities)]
    
    ## Plot line chart with dashed trend lines
    #fig_trend = px.line(
        #filtered_df,
        #x="year",
        #y="temperature",
        #color="city",  # Color by city for clarity
        #markers=True,
        #title="Temperature va by City"
    #)
    
    ## Make all lines dashed
    #fig_trend.update_traces(line=dict(dash="dash"))
    
    #st.plotly_chart(fig_trend, use_container_width=True)
    
    # 3. Climate Heatmap
    #st.subheader("Climate Heatmap")
    fig_heatmap = create_climate_heatmap(df, selected_cities)
    st.plotly_chart(fig_heatmap, use_container_width=True)
    
else:
    st.info("Please select at least one city to display the temperature trends and heatmap.")

# Display country-city information
#if selected_countries:
 #   st.subheader("Selected Countries and Cities")
 #   for country in selected_countries:
  #      cities_in_country = df[df['country'] == country]['city'].unique()
  #      st.write(f"**{country}**: {', '.join(sorted(cities_in_country))}")

# Footer
st.markdown("Data source: https://cds.climate.copernicus.eu/")
