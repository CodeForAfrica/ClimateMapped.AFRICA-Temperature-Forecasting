import streamlit as st

st.title('Methodology')

st.markdown("---")
#with st.expander("View Methodology"):
st.write("""
###
The temperature forecasting model uses historical monthly temperature data from 1901. The data used in this study consists of national and subnational level annual average temperature for a period of 121 years (1901-2022) in all the 54 African countries except Western Sahara (there is no available data from this country). The data was collected from the [Climate Change Knowledge Portal](https://climateknowledgeportal.worldbank.org/).
Compared to other models, CNN-LSTM offers a unique advantage by capturing both spatial and temporal features, which is particularly important for temperature forecasting. Temperature data is not only a sequential time series but also can exhibit spatial dependencies, especially when considering large-scale climate patterns or regional temperature grids. Traditional time series models like ARIMA or purely LSTM-based approaches focus mainly on temporal dependencies but fail to capture the spatial relationships present in the data. Combining CNNs with LSTM models has proven to be highly effective for time series forecasting, delivering accurate results in temperature predictions [Selmy et al. 3](https://link.springer.com/article/10.1007/s00521-023-09398-9).
    
The model employs a Convolutional Neural Networks (CNNs) and Long Short-Term Memory (LSTM) architecture for time series prediction, using a sequence length of 12 months.
Model performance was evaluated using Mean Squared Error (MSE), showing good predictive accuracy in capturing temperature trends, though some discrepancies emerged during rapid changes. The approach proved effective for temperature forecasting, with further tuning potentially improving results. 
For more information about the whole methodology please go this website: [climatemapped.AFRICA](https://climatemapped-africa.dev.codeforafrica.org/about/Methodology)
""")
