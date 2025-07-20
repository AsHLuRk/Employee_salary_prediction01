import streamlit as st
import pandas as pd
import joblib

# Load model
model = joblib.load('salary_prediction_model.joblib')

# Page configuration
st.set_page_config(page_title="💼 Salary Predictor", page_icon="💰", layout="centered")

# Page styling
st.markdown("""
    <style>
        .stButton>button {
            background-color: #4CAF50;
            color: white;
            padding: 0.5em 2em;
            font-size: 1.1em;
            border-radius: 8px;
        }
        .stTextInput, .stNumberInput, .stSelectbox, .stSlider {
            padding: 0.3em;
        }
        .main {
            background-color: #f0f2f6;
            padding: 20px;
            border-radius: 12px;
        }
    </style>
""", unsafe_allow_html=True)

# Title and Header
st.title("💼 Employee Salary Category Predictor")
st.markdown("Predict whether an employee earns more than **$50K/year** based on their demographics and job attributes.")

st.markdown("---")

# Input Form
with st.form("salary_form"):
    st.subheader("📋 Input Employee Details")

    col1, col2 = st.columns(2)

    with col1:
        age = st.slider("Age", 18, 65, 30)
        fnlwgt = st.number_input("FNLWGT (final weight)", 10000, 1000000, 200000)
        education_num = st.slider("Educational Number", 1, 16, 10)
        capital_gain = st.number_input("Capital Gain", 0, 100000, 0)
        capital_loss = st.number_input("Capital Loss", 0, 5000, 0)
        hours_per_week = st.slider("Hours per Week", 1, 100, 40)

    with col2:
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
            'United-States', 'India', 'Mexico', 'Philippines', 'Germany',
            'Canada', 'Other'
        ])

    submitted = st.form_submit_button("🔮 Predict Salary")

if submitted:
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

    st.markdown("---")
    st.success(f"🎯 **Predicted Salary Category**: `{result}`")
    st.balloons()
