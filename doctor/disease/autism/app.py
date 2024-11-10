import os
import numpy as np
from flask import Flask, render_template, request, redirect, url_for
import pickle
import joblib
os.environ['TF_CPP_MIN_LOG_LEVEL'] = '2'


app = Flask(__name__)

# Load models
model_path = os.path.join(os.getcwd(), 'models')
ASD_model = joblib.load(os.path.join(model_path, 'ASD_model.joblib'))

encoder_path = os.path.join(os.getcwd(), 'encoders')
sex_encoder = pickle.load(open(os.path.join(encoder_path, 'sex_encoder.pkl'), 'rb'))
yes_no_encoder = pickle.load(open(os.path.join(encoder_path, 'yes_no_encoder.pkl'), 'rb'))
ethnicity_encoder = pickle.load(open(os.path.join(encoder_path, 'ethnicity_encoder.pkl'), 'rb'))

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/<age_group>', methods=['GET', 'POST'])
def predict_age_group(age_group):
    if request.method == 'POST':
        data = request.form.to_dict()
        features = [yes_no_encoder.transform([data[f'Q{i}']])[0] for i in range(1, 11)]
        if age_group == 'toddler':
            age_in_months = int(data['age'])
            age_in_years = age_in_months / 12  # Convert age from months to years
            features.append(age_in_years)
        else:
            features.append(int(data['age']))
        
        features.append(sex_encoder.transform([data['sex']])[0])

        features.append(ethnicity_encoder.transform([data['ethnicity']])[0])
        features.append(yes_no_encoder.transform([data['jaundice']])[0])
        features.append(yes_no_encoder.transform([data['family_asd']])[0])
        

        # Convert features to a numpy array
        features = np.array([features])

        # Make predictions using the H5 model
        prediction = ASD_model.predict(features)
        result = 'Positive' if prediction > 0.5 else 'Negative'

        return render_template('result.html', result=result)

    return render_template(f'{age_group}.html')

if __name__ == '__main__':
    app.run(debug=True)