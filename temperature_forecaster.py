import streamlit as st
import pandas as pd
import numpy as np
from sklearn.preprocessing import MinMaxScaler
import joblib
import plotly.graph_objs as go
from plotly.subplots import make_subplots

# Page config
st.set_page_config(layout="wide", page_title="Temperature Forecasting App")

# Add logo
st.image('climate_map_Africa_logo.png', width=200)  # Adjust the width as needed

# Title
st.title("Temperature Forecasting App")
st.write("Select countries and years to forecast future temperatures.")

# Load the pre-trained model
model = joblib.load('temperature_forecaster.pkl')
historical_data = pd.read_csv('Monthly_Temperature_Data_2010.csv')
#historical_data = historical_data[historical_data.Date>='2010']

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

    future_df['Year'] = pd.to_datetime(future_df.index).year
    future_df['Month'] = pd.to_datetime(future_df.index).month

    # Display forecasted temperatures
    st.write("Forecasted Temperature")
    st.write(future_df[selected_countries])

    # Add download button for CSV
    csv_data = future_df[selected_countries].to_csv()
    st.download_button(label="Download Forecasted Data as CSV", data=csv_data, file_name='forecasted_temperature.csv', mime='text/csv')

    # Plot historical and predicted data (Line Chart)
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

    # Now, create a heatmap for the forecasted data
    #st.write("Forecasted Temperatures Heatmap")

    # Monthly temperature heatmap
#st.write("Monthly Temperature Heatmap")

# Prepare the data for the heatmap, filter for the selected year range
#future_df['Year'] = pd.to_datetime(future_df.index).year
#future_df['Month'] = pd.to_datetime(future_df.index).month
    heatmap_data = future_df[(future_df['Year'] >= year_range[0]) & (future_df['Year'] <= year_range[1])][selected_countries + ['Year', 'Month']]

    # Create a mapping of month numbers to month names
    month_names = {1: 'January', 2: 'February', 3: 'March', 4: 'April', 5: 'May', 6: 'June', 
                   7: 'July', 8: 'August', 9: 'September', 10: 'October', 11: 'November', 12: 'December'}
    future_df['Month_Name'] = future_df['Month'].map(month_names)
    
    heatmap_data_melted = heatmap_data.melt(id_vars=['Year', 'Month'], var_name='Country', value_name='Temperature')
    
    heatmap_pivot = heatmap_data_melted.pivot_table(index='Month', columns=['Year'], values='Temperature')
    
    heatmap_fig = go.Figure(data=go.Heatmap(
        z=heatmap_pivot.values,
        x=heatmap_pivot.columns,   # Years on the x-axis
        y=[month_names[month] for month in heatmap_pivot.index],  # Month names on the y-axis
        colorscale='RdBu',         # Color scale from blue (cold) to red (hot)
        colorbar=dict(title='Temperature (°C)'),
        reversescale=True,         # Reverse the scale so blue is cold and red is hot
        hovertemplate='Year: %{x}<br>Month: %{y}<br>Temperature: %{z}°C<extra></extra>' # Custom hover template
    ))
    
    
    heatmap_fig.update_layout(
        title='Monthly Temperature Heatmap by Year',
        xaxis_title='Year',        # Now just shows Year
        yaxis_title='Month',       # Months are on the y-axis
        title_font=dict(size=22),
        xaxis_title_font=dict(size=18),
        yaxis_title_font=dict(size=18),
        xaxis=dict(tickangle=-45), # Rotate x-axis labels for better readability
    )
    
    # Display the heatmap
    st.plotly_chart(heatmap_fig)

# Footer section for Methodology
st.markdown("---")
with st.expander("View Methodology"):
    st.write("""
    ### Methodology
    The temperature forecasting model uses historical monthly temperature data from 1901. The data used in this study consists of national and subnational level annual average temperature for a period of 121 years (1901-2022) in all the 54 African countries except Western Sahara (there is no available data from this country). The data was collected from the [Climate Change Knowledge Portal](https://climateknowledgeportal.worldbank.org/).
    Compared to other models, CNN-LSTM offers a unique advantage by capturing both spatial and temporal features, which is particularly important for temperature forecasting. Temperature data is not only a sequential time series but also can exhibit spatial dependencies, especially when considering large-scale climate patterns or regional temperature grids. Traditional time series models like ARIMA or purely LSTM-based approaches focus mainly on temporal dependencies but fail to capture the spatial relationships present in the data. Combining CNNs with LSTM models has proven to be highly effective for time series forecasting, delivering accurate results in temperature predictions [Selmy et al. 3](https://link.springer.com/article/10.1007/s00521-023-09398-9).
    The model employs a Convolutional Neural Networks (CNNs) and Long Short-Term Memory (LSTM) architecture for time series prediction, using a sequence length of 12 months.
    Model performance was evaluated using Mean Squared Error (MSE), showing good predictive accuracy in capturing temperature trends, though some discrepancies emerged during rapid changes. The approach proved effective for temperature forecasting, with further tuning potentially improving results. 
    For more information about the whole methodology please go this website: https://climatemapped-africa.dev.codeforafrica.org/
    """)
