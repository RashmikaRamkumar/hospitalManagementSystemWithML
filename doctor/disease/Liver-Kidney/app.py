from flask import Flask, render_template, request, flash, redirect, url_for
from tensorflow.keras.models import load_model
import numpy as np
import os

app = Flask(__name__, template_folder='template')

# Configurations
app.config['SECRET_KEY'] = '5791628bb0b13ce0c676dfde280ba245'
UPLOAD_FOLDER = 'uploads'
STATIC_FOLDER = 'static'
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

# Load models
model_kidney = load_model("model_kidney.h5")  # Kidney model
model_liver = load_model("model_liver.h5")  # Liver model

# Helper function for model predictions
def ValuePredictor(to_predict_list, size):
    to_predict = np.array(to_predict_list).reshape(1, size)
    
    if size == 12:  # Kidney
        loaded_model = model_kidney
    elif size == 10:  # Liver
        loaded_model = model_liver
    
    result = loaded_model.predict(to_predict)
    return result[0]

# Routes
@app.route("/")
@app.route("/home")
def home():
    return render_template("home.html")

@app.route("/liver")
def liver():
    return render_template("liver.html")

@app.route("/kidney")
def kidney():
    return render_template("kidney.html")

@app.route("/result", methods=["POST"])
def result():
    if request.method == 'POST':
        # Capture form data
        to_predict_list = request.form.to_dict()
        to_predict_list = list(to_predict_list.values())
        to_predict_list = list(map(float, to_predict_list))

        # Predict based on the length of input data (size corresponds to Liver or Kidney)
        if len(to_predict_list) == 12:  # Kidney
            result = ValuePredictor(to_predict_list, 12)
        elif len(to_predict_list) == 10:  # Liver
            result = ValuePredictor(to_predict_list, 10)
        
        # Determine the prediction result
        if int(result) == 1:
            prediction = 'Sorry! You are suffering.'
        else:
            prediction = 'Congrats! You are healthy.'
        
    return render_template("result.html", prediction=prediction)

if __name__ == "__main__":
    app.run(debug=True)
