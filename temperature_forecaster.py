import streamlit as st
import pandas as pd
import numpy as np
from sklearn.preprocessing import MinMaxScaler
import joblib
import plotly.graph_objs as go
from plotly.subplots import make_subplots

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

st.title("Temperature Forecasting App")

st.write("Select countries and years to forecast future temperatures.")

# Prepare the dataset
df_country = historical_data.copy()
df = df_country.drop('Area', axis=1)
df_pivot = df.pivot_table(index='Date', columns='Country', values='Monthly_temperature', aggfunc='first')

# Scaling the data
scaler = MinMaxScaler()
scaled_data = scaler.fit_transform(df_pivot)

# Get a list of countries from the dataset
country_list = df_pivot.columns.tolist()

# Add country and year selectors
selected_countries = st.multiselect('Select countries to predict', country_list)
year_range = st.slider('Select the range of years for prediction', min_value=2023, max_value=2050, value=(2023, 2050))

start_year, end_year = year_range
#start_year = st.slider('Select start year for prediction', min_value=2023, max_value=2049, value=2023)
#end_year = st.slider('Select end year for prediction', min_value=start_year+1, max_value=2050, value=2050)

# Proceed only if countries are selected
if selected_countries:
    # Prepare the data for the selected range
    num_months = 12 * (end_year - start_year + 1)
    seq_length = 12  # Assuming a sequence length of 12 months (1 year)
    
    # Use the last known data to make predictions
    last_sequence = scaled_data[-seq_length:]  # The last 12 months of historical data
    
    # Generate predictions for the selected range
    future_scaled = predict_future(model, last_sequence, num_months, seq_length)
    future_temperatures = scaler.inverse_transform(future_scaled)
    
    # Create a DataFrame for future predictions
    future_dates = pd.date_range(start=f'{start_year}-01-01', periods=num_months, freq='M').strftime('%b-%Y')
    future_df = pd.DataFrame(np.round(future_temperatures, 2), index=future_dates, columns=df_pivot.columns)
    future_df.index.name = 'Year'
    
    # Display the forecasted temperature for selected countries
    st.write("Forecasted Temperature")
    st.write(future_df[selected_countries])
    
    # Plot historical and predicted data for the selected countries
    fig = make_subplots(rows=1, cols=1, subplot_titles=['Historical and Predicted Temperatures for Selected Countries'])
    
    for country in selected_countries:
        # Historical data plot
        fig.add_trace(go.Scatter(x=df_pivot.index, 
                                 y=df_pivot[country], 
                                 name=f'{country} (Historical)', 
                                 mode='lines'))
        
        # Predicted data plot
        fig.add_trace(go.Scatter(x=future_df.index, 
                                 y=future_df[country], 
                                 name=f'{country} (Predicted)', 
                                 mode='lines', 
                                 ))
        #line=dict(dash='dash')
    
    # Update layout for better visualization
    fig.update_layout(title='Historical and Predicted Temperatures for Selected Countries',
                      xaxis_title='Year', 
                      yaxis_title='Temperature (°C)', 
                      legend_title='Country',
                      xaxis=dict(type='category'))  # Ensure categorical x-axis for dates
    
    st.plotly_chart(fig)
#===========================================================================================================================================
st.write("Upload a CSV file with monthly temperature data for different countries to forecast 50-years temperatures.")

uploaded_file = st.file_uploader("Choose a CSV file", type="csv")

if uploaded_file:
    df = pd.read_csv(uploaded_file)
    df_country = df.copy()  # Assuming df_country is same as df
    df = df_country.drop('Area', axis=1)
    df_pivot = df.pivot_table(index='Date', columns='Country', values='Monthly_temperature', aggfunc='first')

    scaler = MinMaxScaler()
    scaled_data = scaler.fit_transform(df_pivot)

    seq_length = 12
    last_sequence = scaled_data[-seq_length:]
    num_months = 12 * (2050 - 2022)  # Number of months from 2023 to 2050
    future_scaled = predict_future(model, last_sequence, num_months,seq_length)
    future_temperatures = scaler.inverse_transform(future_scaled)

    future_dates = pd.date_range(start='2023-01-01', periods=num_months, freq='M').strftime('%b-%Y')
    future_df = pd.DataFrame(np.round(future_temperatures,2), index=future_dates, columns=df_pivot.columns)
    future_df.index.name = 'Year'
    st.write("Forecasted Temperature")
    st.write(future_df)

    # Year slicer
    #year_range = st.slider('Select year range', 1901, 2050, (1901, 2050))
    #start_year, end_year = year_range
    #mask = (pd.to_datetime(future_df.index).year >= start_year) & (pd.to_datetime(future_df.index).year <= end_year)
    #filtered_future_df = future_df[mask]

    selected_countries = st.multiselect('Select countries to plot', df_pivot.columns)
    
    if selected_countries:
        fig = make_subplots(rows=1, cols=1, subplot_titles=['Historical and Predicted Temperatures for Selected Countries'])
        for country in selected_countries:
            fig.add_trace(
            go.Scatter(x=pd.to_datetime(df_pivot.index).strftime('%b-%Y'), y=df_pivot[country], name=f'{country} (Historical)', mode='lines')
            )
            fig.add_trace(
                go.Scatter(x=future_df.index, y=future_df[country], name=f'{country} (Predicted)', mode='lines')
            )
        fig.update_layout(title='Historical and Predicted Temperatures for Selected Countries', xaxis_title='Year', yaxis_title='Temperature (°C)',            legend_title='Country',width=2500)
        
        st.plotly_chart(fig)
