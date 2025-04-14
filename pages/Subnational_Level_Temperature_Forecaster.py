import streamlit as st
import pandas as pd
import numpy as np
import tensorflow as tf
import keras
from sklearn.preprocessing import MinMaxScaler
import joblib
import plotly.graph_objs as go
from plotly.subplots import make_subplots

# Add logo
image = 'images/climatemap_logo.png'
st.image(image, width=200)

# Title
st.title("Regions Level Temperature Forecasting")
st.write('Curious about how temperature will vary in your region in the future? Select your country and region.')

# Load the model
model = joblib.load('models/subnational_temp_forecaster.pkl')

# Load and prepare data
df = pd.read_csv('data/subnational_monthly_temp_1990.csv')
df['Date'] = pd.to_datetime(df['Date'])

df_pivot = df.pivot_table(index='Date', columns=['Country', 'Area'], values='Monthly_temperature', aggfunc='first')
df_pivot.columns = ['_'.join(col).strip() for col in df_pivot.columns.values]
df_pivot = df_pivot.sort_index()

# --- filters ---
selected_country = st.selectbox('Select a country:', df['Country'].unique().tolist())
available_regions = df[df['Country'] == selected_country]['Area'].unique().tolist()
selected_regions = st.multiselect('Select regions to forecast:', available_regions)
year_range = st.slider("Select forecast range", 2023, 2050, (2023, 2030))
num_months = 12 * (year_range[1] - year_range[0] + 1)

# Define prediction function
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
        scaler = MinMaxScaler()
        scaled_data = scaler.fit_transform(df_pivot)
        seq_length = 12
        full_last_sequence = scaled_data[-seq_length:]

        future_scaled_all = predict_future(model, full_last_sequence, num_months, seq_length)
        future_all = scaler.inverse_transform(future_scaled_all)
        
        #future_dates = pd.date_range(start=f'{year_range[0]}-01-01', periods=num_months, freq='M').strftime('%b-%Y')

        future_dates = pd.date_range(start=df_pivot.index[-1] + pd.DateOffset(months=1), periods=num_months, freq='MS')
        future_df_all = pd.DataFrame(np.round(future_all, 2), index=future_dates, columns=df_pivot.columns)
        #future_df_all.index.name = 'Date'

        selected_columns = [f"{selected_country}_{region}" for region in selected_regions]
        future_df = future_df_all[selected_columns]
        historical_df = df_pivot[selected_columns]

        # Show forecast table
        #st.subheader("Forecasted Monthly Temperatures")
        display_df = future_df.copy()
        display_df.index = display_df.index.strftime('%b-%Y')
        display_df.index.name = 'Date'
        st.dataframe(display_df)

        # CSV Download
        csv = display_df.to_csv()
        st.download_button("Download forecast data in CSV format", data=csv, file_name="subnational_forecast.csv", mime="text/csv")


        # Add download button for CSV
        #csv_data = future_df[selected_countries].to_csv()
        #st.download_button(label="Download forecasted data as CSV", data=csv_data, file_name='forecasted_temperature.csv', mime='text/csv')


        # Historical + Forecast Plot
        fig = make_subplots(rows=1, cols=1, subplot_titles=["Historical and Forecasted Temperatures"])

        for col in selected_columns:
            fig.add_trace(go.Scatter(x=pd.to_datetime(historical_df.index).strftime('%b-%Y'), y=historical_df[col], name=f"{col} (Historical)", mode='lines'))
            fig.add_trace(go.Scatter(x=pd.to_datetime(future_df.index).strftime('%b-%Y'), y=future_df[col], name=f"{col} (Forecast)", mode='lines'))

        fig.update_layout(
            title="Subnational Temperature Forecast",
            xaxis_title="Date",
            yaxis_title="Temperature (°C)",
            xaxis=dict(tickformat="%Y-%m", tickangle=-45)
        )
        st.plotly_chart(fig)

        # Heatmaps
        future_df['Year'] = future_df.index.year
        future_df['Month'] = future_df.index.month
        month_names = {
            1: 'January', 2: 'February', 3: 'March', 4: 'April', 5: 'May', 6: 'June',
            7: 'July', 8: 'August', 9: 'September', 10: 'October', 11: 'November', 12: 'December'
        }
        future_df['Month_Name'] = future_df['Month'].map(month_names)

        heatmap_data = future_df[
            (future_df['Year'] >= year_range[0]) &
            (future_df['Year'] <= year_range[1])
        ]

        for region_col in selected_columns:
            region_df = heatmap_data[[region_col, 'Year', 'Month']].copy()
            region_df = region_df.rename(columns={region_col: 'Temperature'})

            heatmap_pivot = region_df.pivot_table(index='Month', columns='Year', values='Temperature')

            sorted_months = sorted(heatmap_pivot.index)
            sorted_months = sorted_months[::-1]

            heatmap_fig = go.Figure(data=go.Heatmap(
                #z=heatmap_pivot.values,
                x=heatmap_pivot.columns,
                z=heatmap_pivot.loc[sorted_months].values,
                y=[month_names[m] for m in sorted_months],
                #y=[month_names[m] for m in heatmap_pivot.index],
                colorscale='RdBu',
                reversescale=True,
                colorbar=dict(title='Temperature (°C)'),
                hovertemplate='Year: %{x}<br>Month: %{y}<br>Temperature: %{z}°C<extra></extra>'
            ))

            heatmap_fig.update_layout(
                title=f"Monthly Temperature Heatmap for {region_col.replace('_', ', ')}",
                xaxis_title='Year',
                yaxis_title='Month',
                xaxis=dict(tickangle=-45)
            )
            st.plotly_chart(heatmap_fig)

    # CSV Download
        #csv = future_df.drop(columns=['Year', 'Month', 'Month_Name']).to_csv()
        #st.download_button("Download Forecast CSV", data=csv, file_name="subnational_forecast.csv", mime="text/csv")

        
else:
    st.warning("Please select at least one region to generate a forecast.")
