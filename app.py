from flask import Flask, request, jsonify
import pandas as pd
import joblib
from sklearn.preprocessing import StandardScaler

app = Flask(__name__)

# Load the trained models and scaler
try:
    model  = joblib.load('models/rf_model.pkl')      
    scaler = joblib.load('models/scaler.pkl')
    feature_names = ['Respondent_SeqNo', 'Sex',	'Age',	'Race_Or_Ethnicity',	'Income_Min',	
                      'Income_Max',	'On Insulin or Diabetes Meds',		'Weight_Kg',	
                      'Height_cm',	'BMI',	'Upper_Leg_Length_cm',	'Upper_Arm_Length_cm',	
                      'Arm_Circumference_cm',	'Waist_Circumference_cm',	'Triceps_Skinfold_mm',	
                      'Subscapular_Skinfold_mm',		'Albumin_g/dL',	'Blood_urea_nitrogen_mg/dl',
                      'Creatinine_mg/dl' ]
    #, 'diabetes','gh'

  # Example feature names
except Exception as e:
    print(f"Error loading models or scaler: {e}")

@app.route('/')
def home():
    return "Welcome to the Diabetes Prediction API! 2"

@app.route('/predict', methods=['POST'])
def predict():

    global model
    global scaler

    # Check if the model and scaler are loaded
    if model is None or scaler is None:
        return jsonify({"error": "Model or scaler not loaded"}), 500

    if 'file' not in request.files:
        return jsonify({"error": "No file part in the request"}), 400

    file = request.files['file']

    if file.filename == '':
        return jsonify({"error": "No selected file"}), 400    

    try:
        file = request.files.get('file')
        if file:
            data = pd.read_csv(file)

            # Ensure columns match the expected feature names
            if set(data.columns) != set(feature_names):
                return f"Feature names mismatch. Expected: {feature_names}, but got: {list(data.columns)}", 400

            # Ensure the order of columns is correct
            data = data[feature_names]
            
            # Scale the data
            data_scaled = scaler.transform(data)
            
            # Predict using each model
            results = {}
            for name, model in {
                'Random Forest': model
            }.items():
                predictions = model.predict(data_scaled).tolist()
                results[name] = predictions
            
            return jsonify(results)
        else:
            return "No file uploaded", 400
    except Exception as e:
        return str(e), 500

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=80)
