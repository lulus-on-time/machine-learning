from data.aps import access_points
import pickle 
import numpy as np
from flask_socketio import send

def attachListener(socketio):

    @socketio.on('connect')
    def handleConnection():
        print("Client connected")

    @socketio.on('predict')
    def predict(data):
        data = {
            "data": [
                {
                    "bssid": '38:17:C3:18:00:68',
                    "rssi": 0.0000012
                },
                {
                    "bssid": '38:17:C3:18:00:69',
                    "rssi": 0.0000001
                },
                {
                    "bssid": '38:17:C3:18:00:70',
                    "rssi": 0.0000223
                },
                {
                    "bssid": '38:17:C3:18:00:71',
                    "rssi": 0.0000220
                },
                {
                    "bssid": '38:17:C3:18:00:72',
                    "rssi": 0.0000723
                },
                {
                    "bssid": '38:17:C3:18:00:73',
                    "rssi": 0.0000423
                },
                {
                    "bssid": '38:17:C3:18:00:74',
                    "rssi": 0.0000323
                },
                {
                    "bssid": '38:17:C3:18:00:75',
                    "rssi": 0.0000023
                },
                {
                    "bssid": '38:17:C3:18:00:76',
                    "rssi": 0.0000001
                },
                {
                    "bssid": '38:17:C3:18:00:77',
                    "rssi": 0.0000011
                },
                {
                    "bssid": '38:17:C3:18:00:78',
                    "rssi": 0.0000090
                },
                            {
                    "bssid": '38:17:C3:18:00:80',
                    "rssi": 0.0000030
                },
                {
                    "bssid": '38:17:C3:18:00:79',
                    "rssi": 0.0000065
                }
            ]
        }

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
        # print(rssi_values_2d)
        # print(sklearn.__version__)

        model = None
        with open("models/knn.pkl", "rb") as f:
            model = pickle.load(f)
        
        prediction = model.predict([[8.26342537e-04, 6.03064098e-04, 5.45072556e-04, 3.42770406e-04,
            3.04127748e-04, 4.17028041e-04, 6.81303953e-04, 8.75458087e-04,
            5.10427233e-04, 6.69317090e-04, 5.85940693e-04, 6.24907253e-04,
            6.74692304e-04, 8.42344014e-04, 8.32041564e-05, 7.63685205e-04,
            2.43673938e-04, 1.94231018e-04, 5.72461233e-04, 9.57215595e-05,
            8.85327973e-04, 6.27000000e-04, 8.26342537e-04, 6.03064098e-04, 5.45072556e-04, 3.42770406e-04,
            3.04127748e-04, 4.17028041e-04, 6.81303953e-04, 8.75458087e-04,
            5.10427233e-04, 6.69317090e-04, 5.85940693e-04, 6.24907253e-04,
            6.74692304e-04, 8.42344014e-04, 8.32041564e-05, 7.63685205e-04,
            2.43673938e-04, 1.94231018e-04, 5.72461233e-04, 9.57215595e-05,
            8.85327973e-04, 6.27000000e-04,  8.42344014e-04, 8.32041564e-05, 7.63685205e-04,
            2.43673938e-04, 1.94231018e-04, 5.72461233e-04, 9.57215595e-05]])
        print(prediction)
        send(prediction[0])

