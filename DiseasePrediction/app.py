import pickle
import streamlit as st
import numpy as np
from pymongo import MongoClient

# Load the trained model
model_loaded = pickle.load(open('C:\\Users\\Ritansh\\Desktop\\DiseasePrediction\\heart_disease_data.sav', 'rb'))

# MongoDB connection settings
client = MongoClient('mongodb+srv://RitanshBagal:Aventador$26.@cluster0.cvfpwsz.mongodb.net/?retryWrites=true&w=majority&appName=Cluster0')

db_name = "db1"
collection_name = "mycollection"

# Connecting to MongoDB
db = client[db_name]
collection = db[collection_name]

# Streamlit UI
st.title('Heart Disease Prediction')

# Introduction
st.write("""
This app predicts the presence of heart disease based on various factors.
Please fill in the following details and click the 'Predict' button.
""")

# Input form
st.sidebar.header('User Input')

with st.form(key='user_input_form'):
    col1, col2, col3 = st.columns([1,1,1])

    # Input fields
    with col1:
        age = st.number_input('Age', min_value=0, max_value=120)
        sex = st.selectbox('Sex', options=['Male', 'Female'])
        cp = st.selectbox('Chest Pain Type', options=['Typical Angina', 'Atypical Angina', 'Non-anginal Pain', 'Asymptomatic'])
        trestbps = st.number_input('Resting Blood Pressure (mm Hg)', min_value=0, max_value=300)
        chol = st.number_input('Serum Cholesterol (mg/dl)', min_value=0, max_value=600)
    
    with col2:
        fbs = st.selectbox('Fasting Blood Sugar > 120 mg/dl', options=['True', 'False'])
        restecg = st.selectbox('Resting Electrocardiographic Results', options=['Normal', 'ST-T wave abnormality', 'Probable or definite left ventricular hypertrophy'])
        thalach = st.number_input('Maximum Heart Rate Achieved', min_value=0, max_value=300)
        exang = st.selectbox('Exercise Induced Angina', options=['Yes', 'No'])
        oldpeak = st.number_input('ST Depression Induced by Exercise Relative to Rest', min_value=0.0, max_value=10.0)

    with col3:
        slope = st.selectbox('Slope of the Peak Exercise ST Segment', options=['Upsloping', 'Flat', 'Downsloping'])
        ca = st.number_input('Number of Major Vessels (0-3) Colored by Flourosopy', min_value=0, max_value=3)
        thal = st.selectbox('Thalassemia', options=['Normal', 'Fixed Defect', 'Reversible Defect'])
    
    submit_button = st.form_submit_button(label='Predict')

# Button to trigger prediction
if submit_button:
    # Process input data
    sex = 0 if sex == 'Male' else 1
    cp_mapping = {'Typical Angina': 0, 'Atypical Angina': 1, 'Non-anginal Pain': 2, 'Asymptomatic': 3}
    cp = cp_mapping[cp]
    fbs = 1 if fbs == 'True' else 0
    restecg_mapping = {'Normal': 0, 'ST-T wave abnormality': 1, 'Probable or definite left ventricular hypertrophy': 2}
    restecg = restecg_mapping[restecg]
    exang = 1 if exang == 'Yes' else 0
    slope_mapping = {'Upsloping': 0, 'Flat': 1, 'Downsloping': 2}
    slope = slope_mapping[slope]
    thal_mapping = {'Normal': 1, 'Fixed Defect': 2, 'Reversible Defect': 3}
    thal = thal_mapping[thal]
    
    # Make prediction
    input_data = np.asarray([age, sex, cp, trestbps, chol, fbs, restecg, thalach, exang, oldpeak, slope, ca, thal])
    input_data_reshaped = input_data.reshape(1, -1)
    prediction = model_loaded.predict(input_data_reshaped)
    
    # Display prediction result
    if age == 0:
        st.write('Enter Age!')
    else:
        if prediction[0] == 0:
            st.write('The person may not have heart disease.')
        else:
            st.write('The person might have heart disease.')

    # Save input data and prediction to MongoDB
    document = {
        "age": age,
        "sex": sex,
        "cp": cp,
        "trestbps": trestbps,
        "chol": chol,
        "fbs": fbs,
        "restecg": restecg,
        "thalach": thalach,
        "exang": exang,
        "oldpeak": oldpeak,
        "slope": slope,
        "ca": ca,
        "thal": thal,
        "prediction": int(prediction[0])
    }

    collection.insert_one(document)
    client.close()
