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
#st.set_page_config(layout="wide", page_title="Temperature Forecasting App")

# Add logo
image = 'images/climatemap_logo.png'
st.image(image, width=200)  # Adjust the width as needed

# Title
st.title("Regions Level Temperature Forecasting App")
st.write('Curious about how temperature will vary in your region in the future? Select your country and region.')

# Load the pre-trained model
#model_path = 'models/subnational_temp_forecaster.pkl'
#model = joblib.load(model_path)

path = 'data/subnational_monthly_temp_1990.csv'
historical_data = pd.read_csv(path)

df = historical_data.copy()
df_pivot = df.pivot_table(index='Date', columns=['Country','Area'], values='Monthly_temperature', aggfunc='first')
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

