import streamlit as st
import pandas as pd
import numpy as np
import tensorflow as tf
import keras
from sklearn.preprocessing import MinMaxScaler
import joblib
import plotly.graph_objs as go
from plotly.subplots import make_subplots
import plotly.express as px

# Page config
#st.set_page_config(layout="wide", page_title="Temperature Forecasting App")

# Add logo
image = 'images/climatemap_logo.png'
st.image(image, width=200)  # Adjust the width as needed

# Title
st.title("Regions Level Temperature Forecasting")
st.write('Curious about how temperature will vary in your region in the future? Select your country and region.')

# Load the pre-trained model
model_path = 'models/subnational_temp_forecaster.pkl'
model = joblib.load(model_path)

# Import the data
path = 'data/subnational_monthly_temp_1990.csv'
historical_data = pd.read_csv(path)
historical_data['Date'] = pd.to_datetime(historical_data['Date'])

df = historical_data.copy()
df_pivot = df.pivot_table(index='Date', columns=['Country','Area'], values='Monthly_temperature', aggfunc='first')
df_pivot.columns = ['_'.join(col).strip() for col in df_pivot.columns.values]  # flatten column names
df_pivot = df_pivot.sort_index()

# --- Select Country ---
available_countries = df['Country'].unique().tolist()
selected_country = st.selectbox('Select a country:', available_countries)

# --- Select Regions ---
available_regions = df[df['Country'] == selected_country]['Area'].unique().tolist()
selected_regions = st.multiselect('Select regions to forecast:', available_regions)

# --- Select Forecast Range ---
year_range = st.slider("Select forecast range (years)", 2023, 2050, (2023, 2030))
num_months = 12 * (year_range[1] - year_range[0] + 1)

# Normalize full data
scaler = MinMaxScaler()
scaled_data = scaler.fit_transform(df_pivot)
seq_length = 12
full_last_sequence = scaled_data[-seq_length:]  # shape: (12, num_regions)

# Define future prediction function
def predict_future(model, last_sequence, num_steps, seq_length):
    future_predictions = []
    current_sequence = last_sequence.copy()

    for _ in range(num_steps):
        pred = model.predict(current_sequence.reshape(1, seq_length, -1))[0]
        future_predictions.append(pred)
        current_sequence = np.roll(current_sequence, -1, axis=0)
        current_sequence[-1] = pred

    return np.array(future_predictions)
if selected_regions:
    with st.spinner('Generating forecast...'):
        # Predict for all regions once
        future_scaled_all = predict_future(model, full_last_sequence, num_months, seq_length)
        future_all = scaler.inverse_transform(future_scaled_all)

    # Create full future DataFrame
    last_date = df_pivot.index[-1]
    future_dates = pd.date_range(start=last_date + pd.DateOffset(months=1), periods=num_months, freq='MS')
    future_df_all = pd.DataFrame(np.round(future_all, 2), index=future_dates, columns=df_pivot.columns)
    future_df_all.index = future_df_all.index.strftime('%Y-%m-%d')
    
    # Filter relevant columns
    selected_columns = [f"{selected_country}_{region}" for region in selected_regions]
    future_df = future_df_all[selected_columns]
    historical_df = df_pivot[selected_columns]

else:
    st.warning("Please select at least one region to generate a forecast.")

# -------------------------------
# Display Forecast
# -------------------------------
#st.subheader("Forecasted Monthly Temperatures")
st.dataframe(future_df)

# Plot historical and forecast
fig = make_subplots(rows=1, cols=1, subplot_titles=["Historical and Forecasted Temperatures"])

for col in selected_columns:
    fig.add_trace(go.Scatter(x=historical_df.index, y=historical_df[col], name=f"{col} (Historical)", mode='lines'))
    fig.add_trace(go.Scatter(x=future_df.index, y=future_df[col], name=f"{col} (Forecast)", mode='lines'))

fig.update_layout(title="Subnational Temperature Forecast", xaxis_title="Date", yaxis_title="Temperature (°C)")
st.plotly_chart(fig)

#Create heatmap
# --- Extract Year and Month from index ---
future_df.index = pd.to_datetime(future_df.index, format='%Y-%m_%d', errors='coerce')
future_df['Year'] = future_df.index.year
future_df['Month'] = future_df.index.month

# --- Mapping of month numbers to names ---
month_names = {
    1: 'January', 2: 'February', 3: 'March', 4: 'April', 5: 'May', 6: 'June', 
    7: 'July', 8: 'August', 9: 'September', 10: 'October', 11: 'November', 12: 'December'
}
future_df['Month_Name'] = future_df['Month'].map(month_names)

# --- Melt data for plotting ---
heatmap_data = future_df[
    (future_df['Year'] >= year_range[0]) & 
    (future_df['Year'] <= year_range[1])
]

for region_col in selected_columns:
    region_df = heatmap_data[[region_col, 'Year', 'Month']].copy()
    region_df = region_df.rename(columns={region_col: 'Temperature'})
    
    heatmap_pivot = region_df.pivot_table(index='Month', columns='Year', values='Temperature')

    heatmap_fig = go.Figure(data=go.Heatmap(
        z=heatmap_pivot.values,
        x=heatmap_pivot.columns,
        y=[month_names[m] for m in heatmap_pivot.index],
        colorscale='RdBu',
        colorbar=dict(title='Temperature (°C)'),
        reversescale=True,
        hovertemplate='Year: %{x}<br>Month: %{y}<br>Temperature: %{z}°C<extra></extra>'
    ))

    heatmap_fig.update_layout(
        title=f"Monthly Temperature Heatmap for {region_col.replace('_', ', ')}",
        xaxis_title='Year',
        yaxis_title='Month',
        title_font=dict(size=22),
        xaxis_title_font=dict(size=18),
        yaxis_title_font=dict(size=18),
        xaxis=dict(tickangle=-45),
    )

    st.plotly_chart(heatmap_fig)


# CSV Download
csv = future_df.to_csv()
st.download_button("Download Forecast CSV", data=csv, file_name="subnational_forecast.csv", mime="text/csv")

# Footer section for Methodology
st.markdown("---")
with st.expander("View Methodology"):
    st.write("""
    ### Methodology
    The temperature forecasting model uses historical monthly temperature data from 1901. The data used in this study consists of national and subnational level annual average temperature for a period of 121 years (1901-2022) in all the 54 African countries except Western Sahara (there is no available data from this country). The data was collected from the [Climate Change Knowledge Portal](https://climateknowledgeportal.worldbank.org/).
    Compared to other models, CNN-LSTM offers a unique advantage by capturing both spatial and temporal features, which is particularly important for temperature forecasting. Temperature data is not only a sequential time series but also can exhibit spatial dependencies, especially when considering large-scale climate patterns or regional temperature grids. Traditional time series models like ARIMA or purely LSTM-based approaches focus mainly on temporal dependencies but fail to capture the spatial relationships present in the data. Combining CNNs with LSTM models has proven to be highly effective for time series forecasting, delivering accurate results in temperature predictions [Selmy et al. 3](https://link.springer.com/article/10.1007/s00521-023-09398-9).
    
    The model employs a Convolutional Neural Networks (CNNs) and Long Short-Term Memory (LSTM) architecture for time series prediction, using a sequence length of 12 months.
    Model performance was evaluated using Mean Squared Error (MSE), showing good predictive accuracy in capturing temperature trends, though some discrepancies emerged during rapid changes. The approach proved effective for temperature forecasting, with further tuning potentially improving results. 
    For more information about the whole methodology please go this website: [climatemapped.AFRICA](https://climatemapped-africa.dev.codeforafrica.org/about/Methodology)
    """)

