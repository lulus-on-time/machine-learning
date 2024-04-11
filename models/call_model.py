import pickle 
from database import db
from sqlalchemy import text
from data.aps import access_points
from sklearn.calibration import CalibratedClassifierCV
from sklearn.neighbors import KNeighborsClassifier
from sklearn.model_selection import GridSearchCV
import pandas as pd
import numpy as np

model = None
with open("models/knn.pkl", "rb") as f:
        model = pickle.load(f)

# function to initialize ML model for the first time
# def first_use():      

def train_model():
    print("--- Training session started ---")

#     fill the database w/ dummy data
#     update the BSSID
#     transform rssi & bssid values -> digestible for the model
    result = db.session.execute(text('SELECT * FROM "Floor"'))

    # Extract column names from the cursor description
    columns = [col[0] for col in result.cursor.description]

    # Iterate over the result set and create a list of dictionaries
    rows = [dict(zip(columns, row)) for row in result]

    # Now 'rows' contains a list of dictionaries, each representing a row in the result set
    print(rows)

#     fit, hyperparameter tuning, wrap in calibration

    calibrated_knn = CalibratedClassifierCV(estimator = KNeighborsClassifier())
    tuned_params = [
        {
        'estimator__n_neighbors': [2,3,5,10,15],
        'estimator__weights': ['uniform', 'distance'],
        'estimator__algorithm': ['ball_tree', 'kd_tree','brute'],
        'estimator__metric': ['cityblock', 'euclidean'],
        }
    ]

    knn_tuned = GridSearchCV(
                      calibrated_knn,
                      tuned_params,
                      scoring='accuracy',
                      cv=10,
                      verbose = 3,
                      error_score='raise'
                    )

    knn_tuned.fit(X_train_scaled, y_train)

#     update the model
    with open("knn.pkl", "wb") as f:
        pickle.dump(knn_tuned, f)


def predict_model(data):
      prediction_probabilities = model.predict_proba(data)
      label_probabilities = []
      class_labels = model.classes_

      # Iterate over the predicted probabilities and corresponding class labels
      for probs in prediction_probabilities:
        for label, prob in zip(class_labels, probs):
          label_probabilities.append({"label": label, "probability": prob})

      # Sort the list based on probabilities in descending order
      label_probabilities.sort(key=lambda x: x["probability"], reverse=True)

      return label_probabilities[:3]