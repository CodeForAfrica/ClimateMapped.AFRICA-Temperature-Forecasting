import streamlit as st
import pandas as pd
import numpy as np
from sklearn.preprocessing import MinMaxScaler
import joblib
import plotly.graph_objs as go

# Add logo
st.image('image.png', width=200)  # Adjust the width as needed

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

# Add country and year selectors
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

    # Create date range
    future_dates = pd.date_range(start=f'{year_range[0]}-01-01', periods=num_months, freq='M')
    future_df = pd.DataFrame(np.round(future_temperatures, 2), index=future_dates, columns=df_pivot.columns)
    future_df.index.name = 'Date'

    # Display forecasted temperatures
    st.write("Forecasted Temperature")
    st.write(future_df[selected_countries])

    # Add download button for CSV
    csv_data = future_df[selected_countries].to_csv()
    st.download_button(label="Download Forecasted Data as CSV", data=csv_data, file_name='forecasted_temperature.csv', mime='text/csv')

    # Prepare the data for heatmap plotting by year
    future_df['Year'] = future_df.index.year
    future_df['Month'] = future_df.index.strftime('%b')

    # Get unique years to plot the heatmaps separately for each year
    unique_years = future_df['Year'].unique()

    # Loop through each year to plot the heatmaps
    for year in unique_years:
        st.write(f"Heatmap for {year}")
        heatmap_data = future_df[future_df['Year'] == year][selected_countries + ['Month']]

        # Pivot the data so that the x-axis is the months and y-axis is the countries
        heatmap_pivot = heatmap_data.pivot_table(index='Country', columns='Month', values=selected_countries)

        # Create the heatmap with blue to red color scale
        heatmap_fig = go.Figure(data=go.Heatmap(
            z=heatmap_pivot.values,
            x=heatmap_pivot.columns,  # Months on the x-axis
            y=heatmap_pivot.index,    # Countries on the y-axis
            colorscale='RdBu',  # Color scale from blue (cold) to red (hot)
            colorbar=dict(title='Temperature (°C)'),
            reversescale=True  # Reverse the scale so blue is cold and red is hot
        ))

        # Update layout for the heatmap
        heatmap_fig.update_layout(
            title=f'Forecasted Temperatures Heatmap for {year}',
            xaxis_title='Month',
            yaxis_title='Country',
            title_font=dict(size=22),
            xaxis_title_font=dict(size=18),
            yaxis_title_font=dict(size=18),
            xaxis=dict(tickangle=-45),  # Rotate x-axis labels for better readability
        )

        # Display the heatmap for this year
        st.plotly_chart(heatmap_fig)
