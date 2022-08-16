import numpy as np
import pandas as pd
import streamlit as st
import pickle
from sklearn.preprocessing import OneHotEncoder

st.header("Predicting Used Car Prices in the UK")
st.write("""
Created by Giovanni Ceretti
""")
st.write("""
""")
st.write("""
This is a Streamlit web app created so users can generate a prediction for the price of a used car. The model is based off August 2022 used car listing data from the British online car reseller, Cazoo.
""")
st.write("""
""")
st.write("""
Please use the input boxes below to input the desired feature characteristics; input values for all features.
""")

# Creating the categorical variable input list
car_make_list = pickle.load(open('./model/car_make_list.pkl','rb'))
model_list = pickle.load(open('./model/model_list.pkl','rb'))
transmission_list = pickle.load(open('./model/transmission_list.pkl','rb'))
trim_list = pickle.load(open('./model/trim_list.pkl','rb'))
color_list = pickle.load(open('./model/color_list.pkl','rb'))

# Creating the input feature boxes

car_make = st.selectbox(
    'Car Make',
['<Select Make>'] + car_make_list
)

car_model = st.selectbox(
    'Car Model',
    ['<Select Model>'] + model_list
)

trim = st.selectbox(
    'What trim is on the car?',
    ['<Select Trim>'] + trim_list
)

reg_date = st.selectbox(
    'Car Registration Year',
    [2022, 2021, 2020, 2019, 2018, 2017, 2016, 2015, 2014]
)

car_age = 2022 - reg_date
if car_age == 0:
        car_age = 0.5
car_age = car_age ** 0.5


mileage = st.number_input(
    'Car Mileage',
    step=1000
)

transmission = st.selectbox(
    'Manual or Automatic',
    ['<Select Transmission>'] + transmission_list
)

color = st.selectbox(
    'What color is the car?',
    ['<Select Color>'] + color_list
)


# Load pickled encoder
encoder = pickle.load(open('./model/input_encoder.pkl','rb'))
# Identify and group different feature types
numeric_input = np.array([mileage,car_age])
categorical_input = np.array([
    car_model, trim, transmission, color, car_make]).reshape(1,-1)[0]
# Encode categorical features using the pickled encoder
categorical_input = encoder.transform(categorical_input.reshape(1,-1))[0]
# Concatenate numeric and dummified categorical inputs
user_input = np.hstack([numeric_input,categorical_input])

# Load pickled predictive model
model = pickle.load(open('./model/cazoo_streamlit.pkl','rb'))

predictions = model.predict(user_input.reshape(1,-1))
predictions_gbp = "£{:,.2f}".format(float(np.exp(predictions)))

if st.button('Predict Car Price'):
    st.write(predictions_gbp)
