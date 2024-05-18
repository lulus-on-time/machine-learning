class Fake:
    def __init__(self):
        self.info = "Fake model to handle empty database."

    def predict_proba(self):
        return [
            {
                "locationId": -1000,
                "probability": 0
            }
        ]
