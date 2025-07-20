import streamlit as st
import pandas as pd
import joblib

# Load model
model = joblib.load('salary_prediction_model.joblib')

st.set_page_config(page_title="Salary Prediction", layout="centered")
st.title("💼 Employee Salary Prediction")

# Inputs
age = st.slider("Age", 18, 65, 30)
fnlwgt = st.number_input("FNLWGT", 10000, 1000000, 200000)
education_num = st.slider("Educational Number", 1, 16, 10)
capital_gain = st.number_input("Capital Gain", 0, 100000, 0)
capital_loss = st.number_input("Capital Loss", 0, 5000, 0)
hours_per_week = st.slider("Hours per Week", 1, 100, 40)

# Dropdowns
workclass = st.selectbox("Workclass", [
    'Private', 'Self-emp-not-inc', 'Self-emp-inc', 'Federal-gov',
    'Local-gov', 'State-gov', 'Without-pay', 'Never-worked'
])

education = st.selectbox("Education", [
    'Bachelors', 'Some-college', 'HS-grad', 'Masters', 'Assoc-acdm',
    'Assoc-voc', 'Doctorate', 'Prof-school', 'Other'
])

marital_status = st.selectbox("Marital Status", [
    'Married-civ-spouse', 'Never-married', 'Divorced', 'Separated', 'Widowed'
])

occupation = st.selectbox("Occupation", [
    'Tech-support', 'Craft-repair', 'Other-service', 'Sales', 'Exec-managerial',
    'Prof-specialty', 'Handlers-cleaners', 'Machine-op-inspct', 'Adm-clerical',
    'Farming-fishing', 'Transport-moving', 'Protective-serv'
])

relationship = st.selectbox("Relationship", [
    'Husband', 'Not-in-family', 'Own-child', 'Unmarried', 'Wife'
])

race = st.selectbox("Race", [
    'White', 'Black', 'Asian-Pac-Islander', 'Amer-Indian-Eskimo', 'Other'
])

gender = st.selectbox("Gender", ['Male', 'Female'])

native_country = st.selectbox("Native Country", [
    'United-States', 'India', 'Mexico', 'Philippines', 'Germany', 'Canada', 'Other'
])

# Predict
if st.button("🔮 Predict Salary"):
    input_df = pd.DataFrame({
        'age': [age],
        'workclass': [workclass],
        'fnlwgt': [fnlwgt],
        'education': [education],
        'educational_num': [education_num],
        'marital_status': [marital_status],
        'occupation': [occupation],
        'relationship': [relationship],
        'race': [race],
        'gender': [gender],
        'capital_gain': [capital_gain],
        'capital_loss': [capital_loss],
        'hours_per_week': [hours_per_week],
        'native_country': [native_country]
    })

    prediction = model.predict(input_df)[0]
    result = "Income > 50K" if prediction == 1 else "Income ≤ 50K"
    st.success(f"✅ Prediction: {result}")
