import pickle 
import numpy as np
import pandas as pd
from flask import Flask, request
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.orm import DeclarativeBase
from models import execute
from database import db
from dotenv import load_dotenv
import os
from flask_socketio import SocketIO
from handle_connection import attachListener
from flask_cors import CORS

load_dotenv()

# database connection
app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = os.environ.get('DATABASE_URI', "postgresql://postgres:ta@localhost:5431")

db.init_app(app)

with app.app_context():
    db.reflect()

classes = execute()

# initialize socket io
socketio = SocketIO(app)
CORS(app, origins='*')
socketio.init_app(app, cors_allowed_origins="*")

attachListener(socketio)

if __name__ == '__main__':
    # Enable CORS for all origins
    socketio.run(app, debug=True)






# @app.route('/')
# def index():
#     return{
#         "status":"SUCCESS",
#         "message":"Service is up"
#     }, 200

# @app.route('/predict')
# def predict():
#     return {}, 200

# @app.route('/train')
# def train():

#     return {}, 200


# @app.route('/aps', methods=['GET'])
# def read_aps():
#     aps = AccessPoint.query.all()
#     results = [
#         {
#             "bssid": AccessPoint.bssid,
#             "ssid": AccessPoint.ssid,
#             "description": AccessPoint.description,
#         }
#     for ap in aps ] 

#     return {"count": len(results), "aps":results}

#         # is the code snippet above correct to read access point data?
#         # what about the other entities?

# # for development set to True
# # app.run(debug=True)

