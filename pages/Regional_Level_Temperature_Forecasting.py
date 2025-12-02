import streamlit as st
import pandas as pd
import numpy as np
import plotly.graph_objs as go
from mlforecast import MLForecast
import joblib

# Streamlit Configuration
# ---------------------------
st.set_page_config(layout="wide", page_title="Regions Level Temperature Forecasting")

st.image("images/climatemap_logo.png", width=200)
st.title("Regions Level Temperature Forecasting")
st.write("Select your country and region to explore historical and future temperature trends.")


# Load model + data
# ---------------------------
model = joblib.load("nixtla_forecast.pkl")

# ensure no static features
model.static_features = []

df = pd.read_csv("data/monthly_temp_2015-2025.csv")
df.fillna("NA", inplace=True)
df = df[df.date <= "2024-12-01"].copy()



# Country Mapping
# ---------------------------
country_mapping = {
    'DZ': 'Algeria', 'AO': 'Angola', 'BJ': 'Benin', 'BW': 'Botswana',
    'BF': 'Burkina Faso', 'BI': 'Burundi', 'CM': 'Cameroon', 'CV': 'Cape Verde',
    'CF': 'Central African Republic', 'TD': 'Chad', 'KM': 'Comoros', 'CG': 'Congo',
    'CD': 'Democratic Republic of Congo', 'CI': "Côte d'Ivoire", 'DJ': 'Djibouti',
    'EG': 'Egypt', 'EH': 'Western Sahara', 'GQ': 'Equatorial Guinea', 'ER': 'Eritrea',
    'ET': 'Ethiopia', 'GA': 'Gabon', 'GM': 'Gambia', 'GH': 'Ghana',
    'GN': 'Guinea', 'GW': 'Guinea-Bissau', 'KE': 'Kenya', 'LS': 'Lesotho',
    'LR': 'Liberia', 'LY': 'Libya', 'MG': 'Madagascar', 'MW': 'Malawi',
    'ML': 'Mali', 'MR': 'Mauritania', 'MU': 'Mauritius', 'MA': 'Morocco',
    'MZ': 'Mozambique', 'NA': 'Namibia', 'NE': 'Niger', 'NG': 'Nigeria',
    'RW': 'Rwanda', 'ST': 'São Tomé and Príncipe', 'SN': 'Senegal',
    'SC': 'Seychelles', 'SL': 'Sierra Leone', 'SO': 'Somalia',
    'ZA': 'South Africa', 'SS': 'South Sudan', 'SD': 'Sudan', 'SZ': 'Eswatini',
    'TZ': 'Tanzania', 'TG': 'Togo', 'TN': 'Tunisia', 'UG': 'Uganda',
    'ZM': 'Zambia', 'ZW': 'Zimbabwe'
}

df["country_name"] = df["country"].map(country_mapping)


# Prepare Data
# ---------------------------
df = df.rename(columns={
    "temperature": "y",
    "date": "ds",
    "city": "unique_id"
})

df['y'] = df['y'].round(2)

df["ds"] = pd.to_datetime(df["ds"])
df = df.sort_values(["unique_id", "ds"])


# User Inputs
# ---------------------------
selected_country = st.selectbox("Select Country", sorted(df["country_name"].dropna().unique()))
cities = df[df["country_name"] == selected_country]["unique_id"].unique()
selected_city = st.selectbox("Select City/Region", sorted(cities))


# Filter Selected City
# ---------------------------
df_city = df[df["unique_id"] == selected_city]


#horizon = st.slider("Select number of future months to predict:", 1, 180, 36)
#st.info(f"Forecast horizon = **{horizon} months**")

last_date = df_city['ds'].max()

max_horizon = 12 * ((12 - last_date.month) + 10*12) 

horizon = st.slider(
    "Select number of future months to predict:",
    min_value=12,
    max_value=max_horizon,
    value=12,     
    step=12
)

years_equivalent = horizon // 12

# Display short message to the user
st.info(f"Forecast horizon selected: {horizon} months ({years_equivalent} year{'s' if years_equivalent > 1 else ''})")

# Model Forecast
# ---------------------------
# Keep only model-required columns
df_model = df[["unique_id", "ds", "y"]]

model.fit(df_model)
future = model.predict(h=horizon)
future["ds"] = future["ds"].dt.to_period("M").dt.to_timestamp()

future_city = future[future["unique_id"] == selected_city]

future_city = future_city.rename(columns={'LinearRegression': 'y'})

future_city['y'] = future_city['y'].round(2)


# Plot Line Chart 
# ---------------------------
combined = pd.concat([df_city, future_city])

combined['year_float'] = combined['ds'].dt.year + (combined['ds'].dt.month - 1) / 12

z = np.polyfit(combined['year_float'], combined['y'], 1)
p = np.poly1d(z)
combined['trend'] = p(combined['year_float'])

y_min = 4
y_max = 45


st.subheader("Historical vs Predicted Temperature")

fig = go.Figure()

# Historical data
fig.add_trace(go.Scatter(
    x=df_city["ds"], 
    y=df_city["y"], 
    mode="lines",
    name="Historical",
    line=dict(color="blue")
))

# Forecast
fig.add_trace(go.Scatter(
    x=future_city["ds"], 
    y=future_city["y"], 
    mode="lines",
    name="Forecast",
    line=dict(color="red", dash='dot')
))

# Trend line (continue sur tout, style interrompu sur forecast)
fig.add_trace(go.Scatter(
    x=combined["ds"],
    y=combined["trend"],
    mode="lines",
    name="Trend",
    line=dict(color="green", width=3, dash='dash'),
    hovertemplate='Date: %{x|%b %Y}<br>Trend: %{y:.2f}°C<extra></extra>'
))

fig.update_yaxes(range=[23, max(combined['y'].max(), combined['trend'].max()) + 1])

# Layout
fig.update_layout(
    xaxis_title="Date",
    yaxis_title="Temperature (°C)",
    height=500,
    template="plotly_white",
    legend=dict(orientation="h", y=1.1)
)
fig.update_yaxes(
    range=[y_min, y_max], 
    title_text="Temperature (°C)"
)

st.plotly_chart(fig, use_container_width=True)


# HEATMAP
# ---------------------------
st.subheader("Predicted Monthly Temperature Heatmap")


future_city = future_city[future_city['ds'] > "2025-12-01"]
future_city['Year'] = future_city['ds'].dt.year.astype(int)
future_city['Month'] = future_city['ds'].dt.strftime("%b")

# Pivot table: rows = months, columns = years

pivot = future_city.pivot_table(index='Month', columns='Year', values='y')

# Ensure months are in chronological order
months_order = ["Jan","Feb","Mar","Apr","May","Jun","Jul","Aug","Sep","Oct","Nov","Dec"]
pivot = pivot.reindex(months_order)

# Reverse months for Plotly (Jan at top, Dec at bottom)
pivot = pivot[::-1]


# Round the temperatures
pivot = pivot.round(2)

# Convert years to strings for Plotly X-axis
x_years = pivot.columns.astype(int).astype(str)  

# Plotly heatmap
heatmap_fig = go.Figure(
    data=go.Heatmap(
        z=pivot.values,
        x=x_years,     
        y=pivot.index,  # Months
        colorscale="RdBu",
        reversescale=True,
        colorbar=dict(title="Temp (°C)"),
        zmin=pivot.values.min(),
        zmax=pivot.values.max()
    )
)

heatmap_fig.update_layout(
    xaxis_title="Year",
    yaxis_title="Month",
    height=600,
    template="plotly_white"
)

st.plotly_chart(heatmap_fig, use_container_width=True)
