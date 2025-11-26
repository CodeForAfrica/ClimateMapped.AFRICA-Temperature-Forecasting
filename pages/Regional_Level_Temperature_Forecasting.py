import streamlit as st
import pandas as pd
import numpy as np
import plotly.graph_objs as go
from mlforecast import MLForecast
import joblib

# ---------------------------
# Streamlit Configuration
# ---------------------------
st.set_page_config(layout="wide", page_title="Regions Level Temperature Forecasting")

st.image("images/climatemap_logo.png", width=200)
st.title("Regions Level Temperature Forecasting")
st.write("Select your country and region to explore historical and future temperature trends.")

# ---------------------------
# Load model + data
# ---------------------------
model = joblib.load("models/nixtla_forecast.pkl")
df = pd.read_csv("data/monthly_temp_2015-2025.csv")

# ---------------------------
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

# ---------------------------
# Prepare Data
# ---------------------------
df = df.rename(columns={
    "temperature": "y",
    "date": "ds",
    "city": "unique_id"
})

df["ds"] = pd.to_datetime(df["ds"])
df = df.sort_values(["unique_id", "ds"])

# ---------------------------
# User Inputs
# ---------------------------
selected_country = st.selectbox("Select Country", sorted(df["country_name"].dropna().unique()))
cities = df[df["country_name"] == selected_country]["unique_id"].unique()
selected_city = st.selectbox("Select City/Region", sorted(cities))

forecast_type = st.radio("Forecast Based On:", ["Number of future months", "Target future year"])

if forecast_type == "Number of future months":
    horizon = st.slider("Select number of future months", 1, 120, 36)
else:
    target_year = st.slider("Select future year to predict up to:", 2025, 2050, 2030)
    last_date = df["ds"].max()
    horizon = (pd.Timestamp(f"{target_year}-12-01") - last_date).days // 30

st.info(f"Forecast horizon = **{horizon} months**")

# ---------------------------
# Filter Selected City
# ---------------------------
df_city = df[df["unique_id"] == selected_city]

# ---------------------------
# Model Forecast
# ---------------------------
model.fit(df)
future = model.predict(h=horizon)
future["ds"] = future["ds"].dt.to_period("M").dt.to_timestamp()

future_city = future[future["unique_id"] == selected_city]

# ---------------------------
# Plot Line Chart + Trend (PLOTLY)
# ---------------------------
st.subheader("Historical vs Predicted Temperature")

fig = go.Figure()

# Historical
fig.add_trace(go.Scatter(
    x=df_city["ds"], 
    y=df_city["y"], 
    mode="lines",
    name="Historical",
    line=dict(color="blue")
))

# Trend (Rolling Mean)
df_city["trend"] = df_city["y"].rolling(12).mean()
fig.add_trace(go.Scatter(
    x=df_city["ds"], 
    y=df_city["trend"], 
    mode="lines",
    name="Historical Trend (12-mo avg)",
    line=dict(color="orange", dash="dash")
))

# Forecast
fig.add_trace(go.Scatter(
    x=future_city["ds"], 
    y=future_city["y"], 
    mode="lines",
    name="Forecast",
    line=dict(color="red")
))

fig.update_layout(
    xaxis_title="Date",
    yaxis_title="Temperature (°C)",
    height=500,
    template="plotly_white",
    legend=dict(orientation="h", y=1.1)
)

st.plotly_chart(fig, use_container_width=True)

# ---------------------------
# HEATMAP
# ---------------------------
st.subheader("Monthly Temperature Heatmap (Historical + Forecast)")

heat_df = pd.concat([df_city[["ds", "y"]], future_city[["ds", "y"]]])
heat_df["Year"] = heat_df["ds"].dt.year
heat_df["Month"] = heat_df["ds"].dt.strftime("%b")

pivot = heat_df.pivot_table(index="Year", columns="Month", values="y")

# Ensure months appear in order
pivot = pivot.reindex(columns=["Jan","Feb","Mar","Apr","May","Jun","Jul","Aug","Sep","Oct","Nov","Dec"], fill_value=np.nan)

heatmap_fig = go.Figure(
    data=go.Heatmap(
        z=pivot.values,
        x=pivot.columns,
        y=pivot.index,
        colorscale="RdBu",
        reversescale=True,
        colorbar=dict(title="Temp (°C)")
    )
)

heatmap_fig.update_layout(
    xaxis_title="Month",
    yaxis_title="Year",
    height=600,
    template="plotly_white"
)

st.plotly_chart(heatmap_fig, use_container_width=True)

# ---------------------------
# Done
# ---------------------------
st.success("Forecasting complete.")
