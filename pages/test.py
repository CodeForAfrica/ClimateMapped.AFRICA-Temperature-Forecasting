import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
import numpy as np

# Country code to country name mapping for African countries
COUNTRY_MAPPING = {
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
    
    # Ensure latitude and longitude columns exist
    if 'latitude' not in df.columns:
        df['latitude'] = df['lat']
    if 'lng' not in df.columns and 'longitude' in df.columns:
        df['lng'] = df['longitude']
    
    # Add country names based on country codes
    if 'country_code' in df.columns:
        df['country'] = df['country_code'].map(COUNTRY_MAPPING)
        # Fill any missing country names with the country code
        df['country'] = df['country'].fillna(df['country_code'])
    elif 'country' not in df.columns:
        # If no country info, create a default
        df['country'] = 'Unknown'
    
    # Remove rows where country is still a code (unmapped codes)
    df = df[df['country'].isin(COUNTRY_MAPPING.values()) | (df['country'] == 'Unknown')]
    
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
    
    # Create heatmap with climate stripes colors
    fig = go.Figure(data=go.Heatmap(
        z=pivot_df.values,
        x=pivot_df.columns,
        y=pivot_df.index,
        colorscale='RdBu_r',  # Climate stripes: blue (cold) to red (hot)
        showscale=True,
        colorbar=dict(title="Temperature (°C)"),
        hovertemplate='<b>%{y}</b><br>' +
                      'Year: %{x}<br>' +
                      'Temperature: %{z:.1f}°C<br>' +
                      '<extra></extra>'
    ))
    
    fig.update_layout(
        title="Temperature by city and year",
        xaxis_title="Year",
        yaxis_title="City",
        height=max(300, len(selected_cities) * 40)  # Adjust height based on number of cities
    )
    
    return fig

# Load data
df = load_data()

st.title("Africa Temperature 2025")

# Get latest year in the dataset
latest_year = df['year'].max()
latest_data = df[df['year'] == latest_year]

# 1. OpenStreetMap showing city temperatures as fixed-size points
st.subheader(f"Temperature map of african cities ({latest_year})")

# Check if we have data to display
if len(latest_data) > 0:
    fig_map = px.scatter_mapbox(
        latest_data,
        lat="latitude",
        lon="lng",
        color="temperature",
        size_max=10,
        hover_name="city",
        hover_data={"temperature": ":.1f", "country": True, "latitude": False, "lng": False},
        zoom=3,
        mapbox_style="open-street-map",
        color_continuous_scale="RdBu_r",  
        title=f"Temperatures in African Cities ({latest_year})"
    )
    # Force marker size to be consistent
    fig_map.update_traces(marker=dict(size=8))
    st.plotly_chart(fig_map, use_container_width=True)
else:
    st.warning("No temperature data available for the map display.")

# 2. Hierarchical filters: Country -> Cities (Side by side alignment)
st.subheader("Temperature trend over the years by city")

# Create two columns for side-by-side filters
col1, col2 = st.columns(2)

with col1:
    # Country selection - only show mapped country names
    available_countries = [country for country in df['country'].unique() if country in COUNTRY_MAPPING.values()]
    countries = sorted(available_countries) if available_countries else ['No countries available']
    
    selected_countries = st.multiselect(
        "Select countries:", 
        countries, 
        default=countries[:3] if len(countries) > 3 and countries[0] != 'No countries available' else (countries[:1] if countries[0] != 'No countries available' else [])
    )

with col2:
    # Filter cities based on selected countries
    if selected_countries and 'No countries available' not in selected_countries:
        available_cities = df[df['country'].isin(selected_countries)]['city'].sort_values().unique()
    else:
        available_cities = []
    
    # City selection (multiselect within selected countries)
    selected_cities = st.multiselect(
        "Select cities to display:", 
        available_cities, 
        default=available_cities[:5] if len(available_cities) > 5 else list(available_cities)
    )

if selected_cities:
    # Filter data based on selected cities
    filtered_df = df[df['city'].isin(selected_cities)]
    
    # Plot line chart with dashed trend lines
    fig_trend = px.line(
        filtered_df,
        x="year",
        y="temperature",
        color="city",  # Color by city for clarity
        markers=True,
        title="Temperature Evolution by City"
    )
    
    # Make all lines dashed
    fig_trend.update_traces(line=dict(dash="dash"))
    
    st.plotly_chart(fig_trend, use_container_width=True)
    
    # 3. Climate Heatmap
    st.subheader("Climate Heatmap")
    fig_heatmap = create_climate_heatmap(df, selected_cities)
    st.plotly_chart(fig_heatmap, use_container_width=True)
    
else:
    st.info("Please select at least one city to display the temperature trends and heatmap.")

# Display country-city information
if selected_countries and 'No countries available' not in selected_countries:
    st.subheader("Selected Countries and Cities")
    for country in selected_countries:
        cities_in_country = df[df['country'] == country]['city'].unique()
        if len(cities_in_country) > 0:
            st.write(f"**{country}**: {', '.join(sorted(cities_in_country))}")
        else:
            st.write(f"**{country}**: No cities found")

# Footer
st.markdown("Data source: https://cds.climate.copernicus.eu/")
