import streamlit as st
import pandas as pd
import numpy as np
from sklearn.linear_model import LinearRegression
from mlforecast import MLForecast
from mlforecast.lag_transforms import ExpandingMean, RollingMean
from mlforecast.target_transforms import Differences
import joblib
import plotly.graph_objs as go
from plotly.subplots import make_subplots

# Page config
st.set_page_config(layout="wide", page_title="Regions Level Temperature Forecasting")

# Add logo
image = 'images/climatemap_logo.png'
st.image(image, width=200)

# Title
st.title("Regions Level Temperature Forecasting")
st.write('Curious about how temperature will vary in your region in the future? Select your country and region.')

# Load the model
model = joblib.load('models/subnational_temp_forecaster.pkl')
