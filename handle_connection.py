from data.aps import access_points
import pickle 
import numpy as np
from flask_socketio import send
import logging
from flask_socketio import SocketIO
from sklearn.calibration import CalibratedClassifierCV
from sklearn.metrics import make_scorer, accuracy_score
from models.call_model import model, predict_model, train_model
from classes import execute

'''
TODOS:
    - [DONE] Load the model (pickle.load) as the global variable so it can be accessed
        by 'predict' when it's prediction time and 'train' when it's model replacing time.
        The time required to load a model is very long. Hence, the loading process should be
        done outside of any event.
    - for train & retrain purposes:
        o [NOT DONE] fill the db with dummy data to simulate data fetching.
            - fill 'Room' -> 'Coordinate' -> 'AccessPoint' -> 'Fingerprint' -> 'FingerprintDetail'
            - syntax:
                INSERT INTO "AccessPoint" VALUES (0,'as:we:4r:56:56','hotspot ui','',0);
        o [NOT DONE] How to access the database models in this file from 'classes' variable that was called in app.py?
'''

# access_point = classes['AccessPoint']
# print(access_point)

def attachListener(socketio):

    @socketio.on('connect')
    def handle_connect():
        print("Client connected")
    
    @socketio.on('disconnect')
    def handle_disconnect():
        print('Client disconnected')

    @socketio.on('train')
    def train(data):
        if data['command'] == 'Train!':
            train_model()

    @socketio.on('predict')
    def predict(data):
        print(str(data))
        print()

        # Initialize an array filled with zeros
        num_bssids = len(access_points)
        rssi_values = np.zeros(num_bssids)

        # Populate the array according to the mapping from the access_points dictionary
        for entry in data["data"]:
            bssid = entry["bssid"]
            if bssid in access_points:
                index = access_points[bssid]
                rssi_values[index] = entry["rssi"]

        # Reshape the array into a 2D array with a single row
        rssi_values_2d = rssi_values.reshape(1, -1)
        predict_values = predict_model(rssi_values_2d)

        result = {
            "prediction": predict_values
        }

        print(result)
        send(result)
    
