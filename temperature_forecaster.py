import streamlit as st
import pandas as pd
import numpy as np
from sklearn.preprocessing import MinMaxScaler
import joblib
import plotly.graph_objs as go
from plotly.subplots import make_subplots
import plotly.express as px

# Page config
st.set_page_config(layout="wide", page_title="Temperature Forecasting App")

# Add logo
st.image('climate_map_Africa_logo.png', width=200)  # Adjust the width as needed

# Title
st.title("Temperature Forecasting App")
st.write("Select countries and years to forecast future temperatures.")

# Load the pre-trained model
model = joblib.load('temperature_forecaster.pkl')

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
        
historical_data = pd.read_csv('Monthly_Temperature_Data_2010.csv')
#historical_data = historical_data[historical_data.Date>='2010']

df_country = historical_data.copy()
df_pivot = df_country.pivot_table(index='Date', columns='Country', values='Monthly_temperature', aggfunc='first')
df_pivot.index = pd.to_datetime(df_pivot.index)
df_pivot = df_pivot.sort_index()
all_countries = df_pivot.columns.tolist()

# -----------------------------
# Country Selector with "All Countries" Option
# -----------------------------
all_option = "All Countries"
selected_options = st.multiselect(
    "Select countries for plotting (choose 'All Countries' to display everything)",
    options=[all_option] + all_countries,
    default=[all_option]
)

if all_option in selected_options:
    selected_countries = all_countries
else:
    selected_countries = selected_options

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

    # Plot historical and predicted data (line chart)
    fig = make_subplots(rows=1, cols=1, subplot_titles=['Historical and predicted temperatures for selected countries'])
    for country in selected_countries:
        fig.add_trace(go.Scatter(x=pd.to_datetime(df_pivot.index).strftime('%b-%Y'), y=df_pivot[country], name=f'{country} (Historical)', mode='lines'))
        fig.add_trace(go.Scatter(x=future_df.index, y=future_df[country], name=f'{country} (Predicted)', mode='lines'))

    # Update layout for better visualization
    fig.update_layout(title='Historical and predicted temperatures for selected countries',
                      xaxis_title='Year', 
                      yaxis_title='Temperature (°C)', 
                      legend_title='Country',
                      xaxis=dict(type='category', title_font=dict(size=18)),
                      yaxis=dict(title_font=dict(size=18)),
                      title_font=dict(size=22),
                      legend=dict(font=dict(size=16)))

    st.plotly_chart(fig)

    # Create a heatmap for the forecasted data
   
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
        title='Monthly temperature heatmap by year',
        xaxis_title='Year',        # Now just shows Year
        yaxis_title='Month',       # Months are on the y-axis
        title_font=dict(size=22),
        xaxis_title_font=dict(size=18),
        yaxis_title_font=dict(size=18),
        xaxis=dict(tickangle=-45), # Rotate x-axis labels for better readability
    )
    
    # Display the heatmap
    st.plotly_chart(heatmap_fig)

    st.markdown("#### Africa temperature maps")
    
    # Historical map -> choose a historical date
    hist_date = st.selectbox(
        "Select a historical date for the map",
        options=sorted(df_pivot.index),
        format_func=lambda d: pd.to_datetime(d).strftime('%b-%Y')
    )
    hist_date = get_nearest_date(hist_date, df_pivot.index)
    hist_temp_all = df_pivot.loc[hist_date, all_countries]
    hist_map_df = pd.DataFrame({
        'Country': hist_temp_all.index,
        'Temperature': hist_temp_all.values
    })
    
    # Predicted map -> choose a predicted date
    pred_date = st.selectbox(
        "Select a predicted date for the map",
        options=sorted(future_df.index),
        format_func=lambda d: pd.to_datetime(d).strftime('%b-%Y')

    )
    pred_date = get_nearest_date(pred_date, future_df.index)
    pred_temp_all = future_df.loc[pred_date, all_countries]
    pred_map_df = pd.DataFrame({
        'Country': pred_temp_all.index,
        'Temperature': pd.to_numeric(pred_temp_all.values)
    })
    
    # Display maps side by side
    col1, col2 = st.columns(2)
    with col1:
        st.markdown(f"Historical temperatures on {pd.to_datetime(hist_date).strftime('%b-%Y')}")
        fig_hist_map = px.choropleth(
            hist_map_df,
            locations='Country',
            locationmode='country names',
            color='Temperature',
            scope='africa',
            color_continuous_scale='RdBu_r',
            title=f'Historical ({pd.to_datetime(hist_date).strftime("%b-%Y")})'
        )
        st.plotly_chart(fig_hist_map)
        
    with col2:
        st.markdown(f"Predicted temperatures on {pd.to_datetime(pred_date).strftime('%b-%Y')}")
        fig_pred_map = px.choropleth(
            pred_map_df,
            locations='Country',
            locationmode='country names',
            color='Temperature',
            scope='africa',
            color_continuous_scale='RdBu_r',
            title=f'Predicted ({pd.to_datetime(pred_date).strftime("%b-%Y")})'
        )
        st.plotly_chart(fig_pred_map)

st.markdown("---")
st.subheader("Upload your own data for prediction")

# File uploader for custom data
uploaded_file = st.file_uploader("Upload a CSV file with monthly temperature data", type=["csv"])

# Load the pre-trained scaler
scaler = joblib.load('scaler.pkl')  # Ensure scaler.pkl is available in the directory

# Function to rename uploaded data columns to match expected names
import pandas as pd

def process_uploaded_data(user_df, reference_df):
    expected_columns = reference_df.columns.tolist()
    
    matching_columns = [col for col in user_df.columns if col in expected_columns]
    
    if not matching_columns:
        raise ValueError("No columns in the uploaded data match the historical data columns.")

    user_df = user_df[matching_columns]
    
    rename_map = {col: col for col in matching_columns if col in expected_columns}
    user_df = user_df.rename(columns=rename_map)
    
    missing_columns = [col for col in expected_columns if col not in user_df.columns]
    for col in missing_columns:
        user_df[col] = pd.NA  # Fill missing columns with NaN

    # Reorder columns to match the historical data
    user_df = user_df[expected_columns]
    
    return user_df

# If a file is uploaded
if uploaded_file:
    user_data = pd.read_csv(uploaded_file)
    
    # Ensure the uploaded data matches expected structure
    if len(user_data.columns) == len(df_pivot.columns):  # Check column count matches
        user_data = process_uploaded_data(user_data, df_pivot.columns)  # Rename to match expected columns
        st.write("Uploaded Data (after renaming columns):")
        st.write(user_data.head())

        # Scale user data
        user_data_scaled = scaler.transform(user_data)
        
        # Define sequence length and prepare the last sequence for prediction
        seq_length = 12  # Adjust as needed
        last_sequence = user_data_scaled[-seq_length:]

        # Number of prediction steps
        num_months = st.slider('Number of months to predict', min_value=1, max_value=120, value=12)

        # Generate predictions
        with st.spinner('Generating forecast for uploaded data...'):
            future_scaled = predict_future(model, last_sequence, num_months, seq_length)
            future_temperatures = scaler.inverse_transform(future_scaled)

        # Create a DataFrame for the forecasted data
        start_date = pd.to_datetime(user_data['Date'].iloc[-1]) + pd.DateOffset(months=1)
        future_dates = pd.date_range(start=start_date, periods=num_months, freq='M')
        future_df = pd.DataFrame(np.round(future_temperatures, 2), index=future_dates, columns=df_pivot.columns)

        # Display the forecasted data
        st.write("Forecasted Temperature Data")
        st.write(future_df)

        # Add a download button for the forecasted data
        csv_data = future_df.to_csv()
        st.download_button(label="Download Forecasted Data as CSV", data=csv_data, file_name='forecasted_temperature.csv', mime='text/csv')

        # Plot both the original uploaded and predicted data
        fig = make_subplots(rows=1, cols=1, subplot_titles=['Uploaded and Predicted Temperatures'])
        for column in df_pivot.columns:
            fig.add_trace(go.Scatter(x=user_data['Date'], y=user_data[column], name=f'{column} (Uploaded)', mode='lines'))
            fig.add_trace(go.Scatter(x=future_df.index, y=future_df[column], name=f'{column} (Predicted)', mode='lines'))

        # Customize plot layout
        fig.update_layout(
            title='Uploaded and Predicted Temperatures',
            xaxis_title='Date',
            yaxis_title='Temperature (°C)',
            legend_title='Country/Region'
        )
        st.plotly_chart(fig)
    else:
        st.error("The uploaded file does not match the expected format. Please upload a file with the correct structure.")

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
