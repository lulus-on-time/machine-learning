import pickle 
import numpy as np
import pandas as pd
from flask import Flask, request

app = Flask(__name__)

with open(models/model.pkl, "rb") as chosen_model:
    model = pickle.load(chosen_model)

@app.route('/')
def index():
    return{
        "status":"SUCCESS",
        "message":"Service is up"
    }, 200

@app.route('/predict')
def predict():

    return {}, 200

# app.run(debug=True)

