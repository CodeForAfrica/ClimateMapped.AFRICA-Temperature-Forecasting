import streamlit as st
import pandas as pd
import numpy as np
from sklearn.preprocessing import MinMaxScaler
import joblib
import plotly.graph_objs as go
from plotly.subplots import make_subplots

# Add logo
col1, col2 = st.columns([1, 1])

with col1:
    st.image('path_to_left_logo.png', width=150)

with col2:
    st.image('path_to_right_logo.png', width=150)

# Title
st.title("Temperature Forecasting App")

st.write("Select countries and years to forecast future temperatures.")

# Load the pre-trained model
model = joblib.load('temperature_forecaster.pkl')
historical_data = pd.read_csv('Monthly_Temperature_Sample.csv')

# Function to create sequences
def create_sequences(data, seq_length):
    sequences = []
    labels = []
    for i in range(len(data) - seq_length):
        seq = data[i:i+seq_length]
        label = data[i+seq_length]
        sequences.append(seq)
        labels.append(label)
    return np.array(sequences), np.array(labels)

# Function to predict future values
def predict_future(model, last_sequence, num_steps, seq_length):
    future_predictions = []
    current_sequence = last_sequence.copy()
    for _ in range(num_steps):
        prediction = model.predict(current_sequence.reshape(1, seq_length, -1))[0]
        future_predictions.append(prediction)
        current_sequence = np.roll(current_sequence, -1, axis=0)
        current_sequence[-1] = prediction
    return np.array(future_predictions)

# Prepare the dataset
df_country = historical_data.copy()
df_pivot = df_country.pivot_table(index='Date', columns='Country', values='Monthly_temperature', aggfunc='first')

# Scaling the data
scaler = MinMaxScaler()
scaled_data = scaler.fit_transform(df_pivot)

# Get a list of countries from the dataset
country_list = df_pivot.columns.tolist()

# To add country and year selectors
selected_countries = st.multiselect('Select countries to predict', country_list)
year_range = st.slider('Select the range of years for prediction', min_value=2023, max_value=2050, value=(2023, 2050))

if selected_countries:
    num_months = 12 * (year_range[1] - year_range[0] + 1)
    seq_length = 12  # Sequence length (1 year)
    last_sequence = scaled_data[-seq_length:]

    with st.spinner('Generating forecast...'):
        # Generate predictions
        future_scaled = predict_future(model, last_sequence, num_months, seq_length)
        future_temperatures = scaler.inverse_transform(future_scaled)

    future_dates = pd.date_range(start=f'{year_range[0]}-01-01', periods=num_months, freq='M').strftime('%b-%Y')
    future_df = pd.DataFrame(np.round(future_temperatures, 2), index=future_dates, columns=df_pivot.columns)
    future_df.index.name = 'Date'

    # Display forecasted temperatures
    st.write("Forecasted Temperature")
    st.write(future_df[selected_countries])

    # Add download button for CSV
    csv_data = future_df[selected_countries].to_csv()
    st.download_button(label="Download Forecasted Data as CSV", data=csv_data, file_name='forecasted_temperature.csv', mime='text/csv')

    # Plot historical and predicted data
    fig = make_subplots(rows=1, cols=1, subplot_titles=['Historical and Predicted Temperatures for Selected Countries'])
    for country in selected_countries:
        fig.add_trace(go.Scatter(x=df_pivot.index, y=df_pivot[country], name=f'{country} (Historical)', mode='lines'))
        fig.add_trace(go.Scatter(x=future_df.index, y=future_df[country], name=f'{country} (Predicted)', mode='lines'))

    # Update layout for better visualization
    fig.update_layout(title='Historical and Predicted Temperatures for Selected Countries',
                      xaxis_title='Year', 
                      yaxis_title='Temperature (°C)', 
                      legend_title='Country',
                      xaxis=dict(type='category', title_font=dict(size=18)),
                      yaxis=dict(title_font=dict(size=18)),
                      title_font=dict(size=22),
                      legend=dict(font=dict(size=16)))

    st.plotly_chart(fig)
