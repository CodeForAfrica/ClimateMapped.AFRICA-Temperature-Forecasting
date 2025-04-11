import streamlit as st
import pandas as pd
import numpy as np
import tensorflow as tf
from sklearn.preprocessing import MinMaxScaler
import joblib
import plotly.graph_objs as go
from plotly.subplots import make_subplots
import plotly.express as px

# Page config
st.set_page_config(layout="wide", page_title="Temperature Forecasting App")

# Add logo
image = 'images/climatemap_logo.png'
st.image(image, width=200)  # Adjust the width as needed

# Title
st.title("Regions Level Temperature Forecasting App")
st.write('Curious about how temperature will vary in your region in the future? Select your country and region.')

# Load the pre-trained model
model_path = 'models/subnational_temp_forecaster.pkl'
model = joblib.load(model_path)

def get_nearest_date(selected_date, date_index):
    """
    Given a selected date (as a Timestamp) and a sorted date_index,
    return the nearest date from date_index.
    """
    # If the date is exactly in the index, return it
    if selected_date in date_index:
        return selected_date
    else:
        # Ensure the index is sorted
        sorted_index = date_index.sort_values()
        # Find the position of the nearest date using the 'nearest' method
        nearest_idx = sorted_index.get_indexer([selected_date], method='nearest')[0]
        return sorted_index[nearest_idx]

path = 'data/subnational_monthly_temp_1990.csv'
historical_data = pd.read_csv(path)

df_region = historical_data.copy()
df_pivot = df_region.pivot_table(index='Date', columns=['Country','Area'], values='Monthly_temperature', aggfunc='first')
df_pivot.index = pd.to_datetime(df_pivot.index)
df_pivot = df_pivot.sort_index()
all_regions = df_pivot.columns.tolist()

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
        current_sequence = np.roll(current_sequence, -1, axis=0)  # Shift sequence left
        current_sequence[-1] = prediction  # Replace last value with the new prediction

    return np.array(future_predictions)
    
# Prepare the dataset





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

