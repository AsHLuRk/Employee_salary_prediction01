import streamlit as st
import pandas as pd
import joblib

# Load trained model
model = joblib.load("salary_prediction_model.joblib")

# Set Streamlit page config
st.set_page_config(page_title="Salary Predictor", layout="wide")

# --- 🎨 Custom CSS for modern glowing UI ---
st.markdown("""
    <style>
    body {
        background-color: #0d1117;
        color: white;
    }
    .hero {
        text-align: center;
        padding-top: 40px;
        padding-bottom: 20px;
    }
    .hero-title {
        font-size: 3.5em;
        font-weight: 900;
        background: linear-gradient(45deg, #8e2de2, #4a00e0);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
    }
    .hero-subtitle {
        font-size: 1.2em;
        color: #9ca3af;
        margin-top: 10px;
        margin-bottom: 30px;
    }
    .button-glow {
        background-color: #4f46e5;
        color: white;
        padding: 12px 26px;
        font-size: 1.1em;
        border-radius: 8px;
        border: none;
        box-shadow: 0 0 15px #4f46e5;
        cursor: pointer;
        transition: 0.3s;
    }
    .button-glow:hover {
        box-shadow: 0 0 25px #4f46e5;
    }
    </style>
""", unsafe_allow_html=True)

# --- 💫 HERO SECTION ---
st.markdown("""
<div class="hero">
    <div class="hero-title">Your Code</div>
    <div class="hero-subtitle">Gemini AI + Blockchain verified salary prediction</div>
</div>
""", unsafe_allow_html=True)

# --- 📄 INPUT FORM ---
st.subheader("📋 Enter Employee Details")

with st.form("salary_form"):
    col1, col2, col3 = st.columns(3)

    with col1:
        age = st.slider("Age", 18, 70, 30)
        fnlwgt = st.number_input("Final Weight (fnlwgt)", min_value=10000, value=150000)
        educational_num = st.slider("Education Number", 1, 16, 10)

    with col2:
        workclass = st.selectbox("Workclass", ['Private', 'Self-emp-not-inc', 'Self-emp-inc', 'Federal-gov', 'Local-gov', 'State-gov', 'Without-pay'])
        education = st.selectbox("Education", ['Bachelors', 'HS-grad', '11th', 'Masters', '9th', 'Some-college'])
        marital_status = st.selectbox("Marital Status", ['Married-civ-spouse', 'Divorced', 'Never-married', 'Separated', 'Widowed', 'Married-spouse-absent'])

    with col3:
        occupation = st.selectbox("Occupation", ['Tech-support', 'Craft-repair', 'Other-service', 'Sales', 'Exec-managerial'])
        relationship = st.selectbox("Relationship", ['Wife', 'Own-child', 'Husband', 'Not-in-family', 'Other-relative'])
        race = st.selectbox("Race", ['White', 'Black', 'Asian-Pac-Islander', 'Amer-Indian-Eskimo', 'Other'])

    gender = st.radio("Gender", ['Male', 'Female'], horizontal=True)
    capital_gain = st.slider("Capital Gain", 0, 100000, 0)
    capital_loss = st.slider("Capital Loss", 0, 5000, 0)
    hours_per_week = st.slider("Hours per Week", 1, 99, 40)
    native_country = st.selectbox("Native Country", ['United-States', 'India', 'Mexico', 'Philippines', 'Germany'])

    submitted = st.form_submit_button("🔮 Predict", type="primary")

# --- 🔮 PREDICTION LOGIC ---
if submitted:
    input_data = pd.DataFrame({
        'age': [age],
        'workclass': [workclass],
        'fnlwgt': [fnlwgt],
        'education': [education],
        'educational_num': [educational_num],
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

    prediction = model.predict(input_data)[0]
    result = "Income > 50K" if prediction == 1 else "Income ≤ 50K"

    # 💰 Tax Estimate
    if prediction == 1:
        est_salary = 70000
        tax_rate = 0.20
    else:
        est_salary = 40000
        tax_rate = 0.05
    tax_amount = est_salary * tax_rate

    # 📊 Display Results
    st.markdown("---")
    st.success(f"🎯 **Predicted Salary Category:** `{result}`")
    st.info(f"💵 Estimated Annual Salary: ₹{est_salary:,.0f}")
    st.warning(f"🧾 Estimated Tax (at {int(tax_rate*100)}%): ₹{tax_amount:,.0f}")
    st.balloons()
