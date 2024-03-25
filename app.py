import pickle 
import numpy as np
import pandas as pd
from flask import Flask, request
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.orm import DeclarativeBase
from models import db, execute
# from database import db

# database connection
app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = "postgresql://postgres:ta@localhost:5431"

db.init_app(app)

with app.app_context():
    db.reflect()

# initialize classes in DB
classes = execute()
print(classes['AccessPoint'])

@app.route('/')
def index():
    return{
        "status":"SUCCESS",
        "message":"Service is up"
    }, 200

@app.route('/predict')
def predict():
    return {}, 200

@app.route('/train')
def train():

    return {}, 200


@app.route('/aps', methods=['GET'])
def read_aps():
    aps = AccessPoint.query.all()
    results = [
        {
            "bssid": AccessPoint.bssid,
            "ssid": AccessPoint.ssid,
            "description": AccessPoint.description,
        }
    for ap in aps ] 

    return {"count": len(results), "aps":results}

        # is the code snippet above correct to read access point data?
        # what about the other entities?

# for development set to True
app.run(debug=True)

