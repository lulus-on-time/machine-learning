import pickle 
from database import db
from sqlalchemy import text
from sklearn.calibration import CalibratedClassifierCV
from sklearn.neighbors import KNeighborsClassifier
from sklearn.model_selection import GridSearchCV
from sklearn.preprocessing import StandardScaler
import pandas as pd
import numpy as np

access_points = {}
def init_model():
    with open("models/knn.pkl", "rb") as f:
        model = pickle.load(f)
    return model

model = init_model()

def transform_rssi(rssi_dbm):
    # convert dbm to mw
    # Define the conversion function
    return 10 ** (rssi_dbm / 10)

def build_df():
    data = fetch_data()
    access_point_df = pd.DataFrame(data["access_point"].fetchall(), columns=data["access_point"].keys())
    fingerprint_df = pd.DataFrame(data["fingerprint"].fetchall(), columns=data["fingerprint"].keys())
    fingerprint_detail_df = pd.DataFrame(data["fingerprint_detail"].fetchall(), columns=data["fingerprint_detail"].keys())

    # transform rssi & bssid values -> digestible for the model -> turn into dataframe
    merged_df = pd.merge(fingerprint_df, fingerprint_detail_df, left_on='id', right_on='fingerprintId')
    merged_df = pd.merge(merged_df, access_point_df, on='bssid')
    df = merged_df.drop(['id_x','id_y','id','ssid','description','createdAt','coordinateId'], axis=1)
    print("IDWIEWIIWLDSD")
    print(df)

    # Apply the conversion function to the 'rssi' column
    df['rssi'] = df['rssi'].apply(transform_rssi)

    # Pivot dataframe
    df['location-fingerprintId'] = df['location'] + '-' + df['fingerprintId'].astype('str')
    df = df.pivot_table(index='location-fingerprintId',columns='bssid', values='rssi', fill_value=0).reset_index()
    df[['location', 'fingerprintId']] = df['location-fingerprintId'].str.split('-', expand=True)
    df.drop(columns=['fingerprintId','location-fingerprintId'], inplace=True)
    df.columns.name=None

    return df

def standardize(X):
    scaler = StandardScaler()
    # all data are used for training
    X_scaled = scaler.fit_transform(X) 
    return X_scaled

def fetch_data():
    access_point = db.session.execute(text('SELECT * FROM "AccessPoint"'))
    fingerprint = db.session.execute(text('SELECT * FROM "Fingerprint"'))
    fingerprint_detail = db.session.execute(text('SELECT * FROM "FingerprintDetail"'))

    return {
        "access_point" : access_point,
        "fingerprint" : fingerprint, 
        "fingerprint_detail" : fingerprint_detail
    }

def update_bssid():
    data = fetch_data()
    bssid = pd.DataFrame(data["access_point"].fetchall(), columns=data["access_point"].keys())['bssid'].to_list()
    updated_access_points = {}
    
    for index, bssid in enumerate(bssid):
        updated_access_points[bssid] = index

    return updated_access_points

def train_model():
    print("--- Training session started ---")
    # TODO: restructure database and its dummy data 
    #    -> wait for Sam's resturcturing confirmation

    df = build_df()
    X = standardize(df.drop(['location'], axis=1))
    y = df.location

    calibrated_knn = CalibratedClassifierCV(estimator = KNeighborsClassifier(), method='sigmoid')
    tuned_params = [
        {
            'estimator__n_neighbors': [2,3,5,10,15],
            'estimator__weights': ['uniform', 'distance'],
            'estimator__algorithm': ['ball_tree', 'kd_tree','brute'],
            'estimator__metric': ['cityblock', 'euclidean'],
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

def predict_model(data):
    model = init_model()
    access_points = update_bssid()
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

    prediction_probabilities = model.predict_proba(rssi_values_2d)
    label_probabilities = []
    class_labels = model.classes_

    # Iterate over the predicted probabilities and corresponding class labels
    for probs in prediction_probabilities:
        for label, prob in zip(class_labels, probs):
            label_probabilities.append({"label": label, "probability": prob})

        # Sort the list based on probabilities in descending order
        label_probabilities.sort(key=lambda x: x["probability"], reverse=True)
    
    return label_probabilities[:3]