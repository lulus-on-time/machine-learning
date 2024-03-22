import pickle 
import numpy as np
import pandas as pd
from flask import Flask, request
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.orm import DeclarativeBase
from flask_socketio import SocketIO

# database connection
app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = "postgresql://postgres:ta@localhost:5431"
socketio = SocketIO(app)

class Base(DeclarativeBase):
  pass

db = SQLAlchemy(model_class=Base)
db.init_app(app)

with app.app_context():
    db.reflect()

#entities
# class AccessPoint(db.Model):
#     __tablename__ = 'AccessPoint'
#     id = db.Column(db.Integer, primary_key=True)
#     bssid = db.Column(db.String(), unique=True)
#     ssid = db.Column(db.String())
#     description = db.Column(db.String())
#     # fingerprints ?? listofFngerprintDetail
#     # coordinate Coordinate ?? add another class "Coordinate"? 
#     # coordinateId ?? same as above

#     def __repr__(self):
#         return f"<Car {self.bssid}>"

# class Fingerprint(db.Model):
#     __tablename__ = 'Fingerprint'
#     id = db.Column(db.Integer, primary_key=True)
#     createdAt = db.Column(db.DateTime, default=now())
#     # fingerprintDetails ?? listofFngerprintDetail
#     location = db.Column(db.String)

# class FingerprintDetail(db.Model):
#     __tablename__ = 'FingerprintDetail'
#     id = db.Column(db.Integer, primary_key=True)
#     # fp FP ?? add relation to another class FP, how syntax? 
#     fingerprintId = db.Column(db.Integer, unique=True)
#     # ap AcessPoint ?? add relation to another class AP, how syntax? 
#     bssid = db.Column(db.String)
#     rssi = db.Column(db.Float)

print(len(db.Model.metadata.tables.keys()))

class AccessPoint(db.Model):
    __table__ = db.Model.metadata.tables['AccessPoint']

    def __repr__(self):
        return self.id

class Coordinate(db.Model):
    __table__ = db.Model.metadata.tables['Coordinate']

    def __repr__(self):
        return self.id
    
class Fingerprint(db.Model):
    __table__ = db.Model.metadata.tables['Fingerprint']

    def __repr__(self):
        return self.id
    
class FingerprintDetail(db.Model):
    __table__ = db.Model.metadata.tables['FingerprintDetail']

    def __repr__(self):
        return self.id

class Floor(db.Model):
    __table__ = db.Model.metadata.tables['Floor']

    def __repr__(self):
        return self.id

class Room(db.Model):
    __table__ = db.Model.metadata.tables['Room']

    def __repr__(self):
        return self.id

# load model
# with open('models/model.pkl', "rb") as chosen_model:
#     model = pickle.load(chosen_model)

# features = db.findall()

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

@socketio.on('connect')
def handle_connect():
    print('Connected to WebSocket server')

@socketio.on('disconnect')
def handle_disconnect():
    print('Disconnected from WebSocket server')


# for development set to True
app.run(debug=True)

