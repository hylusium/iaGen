import streamlit as st
import requests
import pandas as pd

# Load the dataset to get unique regions and years
data = pd.read_csv("avocado.csv")
regions = data['region'].unique()
years = data['year'].unique()

# Streamlit app
st.title('Avocado Price Prediction')

# User inputs
date = st.date_input('Date')
quality1 = st.number_input('Quality1', min_value=0)
quality2 = st.number_input('Quality2', min_value=0)
quality3 = st.number_input('Quality3', min_value=0)
small_bags = st.number_input('Small Bags', min_value=0)
large_bags = st.number_input('Large Bags', min_value=0)
xlarge_bags = st.number_input('XLarge Bags', min_value=0)
type_ = st.selectbox('Type', ['conventional', 'organic'])
year = st.selectbox('Year', years)
region = st.selectbox('Region', regions)

# Prepare the input data
input_data = {
    'Date': date.strftime('%Y-%m-%d'),
    'Quality1': quality1,
    'Quality2': quality2,
    'Quality3': quality3,
    'Small Bags': small_bags,
    'Large Bags': large_bags,
    'XLarge Bags': xlarge_bags,
    'type': type_,
    'year': year,
    'region': region
}

# Button to get prediction
if st.button('Predict'):
    # Send a POST request to the Flask backend
    response = requests.post('http://127.0.0.1:5000/predict', json=input_data)
    
    if response.status_code == 200:
        prediction = response.json()['prediction']
        st.success(f'The predicted price of the avocado is ${prediction:.2f}')
    else:
        st.error('Error in prediction : ' + response.json()['error'])