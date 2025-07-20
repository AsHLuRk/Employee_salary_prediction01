from flask import Flask, request, render_template, jsonify
import joblib
import pandas as pd

app = Flask(__name__)

# Load the trained model
try:
    model = joblib.load('salary_prediction_model.joblib')
    print("✅ Model loaded successfully.")
except FileNotFoundError:
    print("❌ Model file not found. Please train the model first using main.py.")
    model = None

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/predict', methods=['POST'])
def predict():
    if model is None:
        return jsonify({'error': 'Model not loaded'}), 500

    try:
        # Collect form inputs and convert to proper types
        input_data = {
            'age': [int(request.form['age'])],
            'workclass': [request.form['workclass']],
            'fnlwgt': [int(request.form['fnlwgt'])],
            'education': [request.form['education']],
            'educational_num': [int(request.form['educational_num'])],
            'marital_status': [request.form['marital_status']],
            'occupation': [request.form['occupation']],
            'relationship': [request.form['relationship']],
            'race': [request.form['race']],
            'gender': [request.form['gender']],
            'capital_gain': [int(request.form['capital_gain'])],
            'capital_loss': [int(request.form['capital_loss'])],
            'hours_per_week': [int(request.form['hours_per_week'])],
            'native_country': [request.form['native_country']]
        }

        # Create DataFrame for prediction
        input_df = pd.DataFrame(input_data)
        print("\n🧾 Input DataFrame:")
        print(input_df)

        # Make prediction
        prediction = model.predict(input_df)
        print(f"🔮 Prediction result: {prediction}")

        result = 'Income > 50K' if prediction[0] == 1 else 'Income <= 50K'
        return jsonify({'salary_prediction': result})

    except Exception as e:
        print(f"❌ Error: {e}")
        return jsonify({'error': f'An error occurred: {str(e)}'}), 400

if __name__ == '__main__':
    app.run(debug=True)
