import pickle 
from database import db
from sqlalchemy import text
from sklearn.calibration import CalibratedClassifierCV
from sklearn.neighbors import KNeighborsClassifier
from sklearn.model_selection import GridSearchCV
from sklearn.preprocessing import StandardScaler
import pandas as pd
import numpy as np
from findmyself import app
import gevent
from celery import Celery
import time
import logging

global access_points
access_points = {}
def init_model():
    try:
        with open("models/knn.pkl", "rb") as f:
            model = pickle.load(f)
        return model
    except Exception: 
        print("knn.pkl not available in models folder")
        return None

def get_features():
    try:
        with open("models/features.pkl", "rb") as f:
            features = pickle.load(f)
        return features
    except Exception:
        print("features.pkl not available in models folder")
        return []

model = init_model()
features = get_features()
flag = False

def build_df():
    data = fetch_data()
    network_df = pd.DataFrame(data["network"].fetchall(), columns=data["network"].keys())
    fingerprint_df = pd.DataFrame(data["fingerprint"].fetchall(), columns=data["fingerprint"].keys())
    fingerprint_detail_df = pd.DataFrame(data["fingerprint_detail"].fetchall(), columns=data["fingerprint_detail"].keys())

    # transform rssi & bssid values -> digestible for the model -> turn into dataframe
    merged_df = pd.merge(fingerprint_df, fingerprint_detail_df, left_on='id', right_on='fingerprintId')
    merged_df = pd.merge(merged_df, network_df, on='bssid')

    df = merged_df.drop(['id_x','id_y','createdAt','apId', 'ssid'], axis=1)

    # Pivot dataframe
    df['locationId-fingerprintId'] = df['locationId'].astype('str') + '-' + df['fingerprintId'].astype('str')
    
    df = df.pivot_table(index='locationId-fingerprintId',columns='bssid', values='rssi', fill_value=0).reset_index()
    df[['locationId', 'fingerprintId']] = df['locationId-fingerprintId'].str.extract(r'^(.*)-(\d+)$')

    df.drop(columns=['fingerprintId','locationId-fingerprintId'], inplace=True)
    df.columns.name=None
    return df

def standardize(X):
    scaler = StandardScaler()
    # all data are used for training
    X_scaled = scaler.fit_transform(X) 
    return X_scaled

def standardize_predict(X):
    # Reshape the input array to a 2D array with a single column
    X_2d = X.reshape(-1, 1)

    # Initialize the StandardScaler
    scaler = StandardScaler()

    # Fit the scaler to the data and transform the X
    X_2d_scaled = scaler.fit_transform(X_2d)

    # Flatten the 2D array to get the standardized X
    X_scaled = X_2d_scaled.flatten()

    return X_scaled

def fetch_data():
    network = db.session.execute(text('SELECT * FROM "Network"'))
    access_point = db.session.execute(text('SELECT * FROM "AccessPoint"'))
    fingerprint = db.session.execute(text('SELECT * FROM "Fingerprint"'))
    fingerprint_detail = db.session.execute(text('SELECT * FROM "FingerprintDetail"'))

    return {
        "access_point" : access_point,
        "fingerprint" : fingerprint, 
        "fingerprint_detail" : fingerprint_detail,
        "network": network
    }

def update_bssid(features):
    # bssid = pd.DataFrame(data["network"].fetchall(), columns=data["network"].keys())['bssid'].to_list()
    # print(features)
    updated_access_points = {}
    
    count = 0
    for feature in features:
        updated_access_points[feature] = count
        count = count + 1

    return updated_access_points

# @celery.task
def train_model():
    
    print("--- Training session started ---")
    with app.app_context():
        df = build_df()
        X = standardize(df.drop(['locationId'], axis=1))
        columns = df.columns.to_list()
        columns.remove('locationId')
        y = df.locationId

        calibrated_knn = CalibratedClassifierCV(estimator = KNeighborsClassifier(), method='sigmoid')
        tuned_params = [
            {
                'estimator__n_neighbors': [2],

                 'estimator__weights': ['distance'],
                'estimator__algorithm': ['brute'],
                'estimator__metric': ['cityblock'],
            }
        ]

        knn_tuned = GridSearchCV (
            calibrated_knn,
            tuned_params,
            scoring="accuracy",
            cv=10,
            verbose = 3,
            error_score='raise'
        )

        knn_tuned.fit(X, y)

        with open("models/knn.pkl", "wb") as f:
            pickle.dump(knn_tuned, f)

        with open("models/features.pkl", "wb") as f:
            pickle.dump(columns, f)

        global model
        global features
        model = init_model()
        features = get_features()
        
        print("--- Training session completed ---")

def predict_model(data, socketio):
    with app.app_context():
        print("--- Prediction session started ---")
        if (model == None) or (len(features) < 1 ):
            train_model()
        
        access_points = update_bssid(features)
        num_bssids = len(access_points)
        rssi_values = np.zeros(num_bssids)

        # Populate the array according to the mapping from the access_points dictionary
        for entry in data["data"]:
            bssid = entry["bssid"]
            if bssid in access_points:
                index = access_points[bssid]
                rssi_values[index] = entry["rssi"]

        rssi_values = standardize_predict(rssi_values)
        # Reshape the array into a 2D array with a single row
        rssi_values_2d = rssi_values.reshape(1, -1)

        prediction_probabilities = model.predict_proba(rssi_values_2d)
        label_probabilities = []
        class_labels = model.classes_

        # Iterate over the predicted probabilities and corresponding class labels
        for probs in prediction_probabilities:
            for label, prob in zip(class_labels, probs):
                label = int(label)
                label_probabilities.append({"locationId": label, "probability": prob})

            # Sort the list based on probabilities in descending order
            label_probabilities.sort(key=lambda x: x["probability"], reverse=True)
        
        print("--- Prediction session completed ---")
        # socketio.emit("message", label_probabilities[:3])
        socketio.emit("predict_%s" % data['clientId'], label_probabilities[:3])