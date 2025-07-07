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
    
    return df

def create_climate_stripes_heatmap(df, selected_cities):
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
        title="Climate Stripes Heatmap - Temperature by City and Year",
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
st.info("💡 Use the city selector below the map to choose cities, or select cities directly from the filters!")

fig_map = px.scatter_mapbox(
    latest_data,
    lat="latitude",
    lon="lng",
    color="temperature",
    size_max=5,
    size=[5] * len(latest_data),  # fixed point size
    hover_name="city",
    hover_data={"temperature": ":.1f", "country": True, "latitude": False, "lng": False},
    zoom=3,
    mapbox_style="open-street-map",
    color_continuous_scale="RdBu_r",  # Climate strip style: blue to red
    title=f"Temperatures in African Cities ({latest_year})"
)
# Force marker size and improve hover
fig_map.update_traces(marker=dict(size=8))
fig_map.update_layout(height=500)
st.plotly_chart(fig_map, use_container_width=True)

# Quick city selection from map data
st.subheader("Quick City Selection")
col1, col2 = st.columns([3, 1])

with col1:
    # Create a searchable selectbox for cities
    city_options = sorted(latest_data['city'].unique())
    quick_selected = st.multiselect(
        "🎯 Quickly select cities from the map:",
        city_options,
        help="Start typing to search for cities",
        key="quick_city_select"
    )

with col2:
    if st.button("🔄 Use Quick Selection", disabled=not quick_selected):
        st.session_state.use_quick_selection = True
        st.session_state.quick_cities = quick_selected
        st.rerun()

# Initialize session state
if 'use_quick_selection' not in st.session_state:
    st.session_state.use_quick_selection = False
if 'quick_cities' not in st.session_state:
    st.session_state.quick_cities = []

# 2. Hierarchical filters: Country -> Cities OR Quick Selection
st.subheader("Temperature trend over the years by city")

# Create tabs for different selection methods
tab1, tab2 = st.tabs(["🌍 Filter by Country", "⚡ Quick Selection"])

with tab1:
    # Country selection
    countries = sorted(df['country'].unique())
    selected_countries = st.multiselect(
        "Select countries:", 
        countries, 
        default=countries[:3] if len(countries) > 3 else countries,
        key="country_filter"
    )
    
    # Filter cities based on selected countries
    available_cities = df[df['country'].isin(selected_countries)]['city'].sort_values().unique()
    
    # City selection (multiselect within selected countries)
    filter_selected_cities = st.multiselect(
        "Select cities to display:", 
        available_cities, 
        default=available_cities[:5] if len(available_cities) > 5 else available_cities,
        key="city_filter"
    )

with tab2:
    if st.session_state.use_quick_selection and st.session_state.quick_cities:
        st.success(f"Using quick selection: {', '.join(st.session_state.quick_cities)}")
        if st.button("Clear Quick Selection"):
            st.session_state.use_quick_selection = False
            st.session_state.quick_cities = []
            st.rerun()
    else:
        st.info("Use the 'Quick City Selection' section above to select cities from the map!")

# Determine which cities to display (prioritize quick selection if available)
if st.session_state.use_quick_selection and st.session_state.quick_cities:
    selected_cities = st.session_state.quick_cities
    selection_method = "Quick Selection"
else:
    selected_cities = filter_selected_cities
    selection_method = "Filter Selection"

# Display current selection method
if selected_cities:
    st.info(f"Currently showing: **{selection_method}** ({len(selected_cities)} cities)")
else:
    st.info("No cities selected. Use either the country filters or quick city selection above.")

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
    
    # 3. Climate Stripes Heatmap
    st.subheader("Climate Stripes Heatmap")
    fig_heatmap = create_climate_stripes_heatmap(df, selected_cities)
    st.plotly_chart(fig_heatmap, use_container_width=True)
    
else:
    st.info("Please select at least one city to display the temperature trends and heatmap.")

# Display country-city information
if st.session_state.use_quick_selection and st.session_state.quick_cities:
    st.subheader("Quick Selected Cities")
    # Group quick selected cities by country
    quick_cities_df = df[df['city'].isin(st.session_state.quick_cities)][['country', 'city']].drop_duplicates()
    for country in quick_cities_df['country'].unique():
        cities_in_country = quick_cities_df[quick_cities_df['country'] == country]['city'].unique()
        st.write(f"**{country}**: {', '.join(sorted(cities_in_country))}")
elif selected_countries:
    st.subheader("Selected Countries and Cities")
    for country in selected_countries:
        cities_in_country = df[df['country'] == country]['city'].unique()
        st.write(f"**{country}**: {', '.join(sorted(cities_in_country))}")

# Footer
st.markdown("Data source: `africa_temperatures.csv`")
