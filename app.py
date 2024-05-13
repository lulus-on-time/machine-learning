from gevent import monkey; monkey.patch_all()
from flask import Flask
from classes import execute
from database import db
from dotenv import load_dotenv, find_dotenv
import os
from flask_socketio import SocketIO
from handle_connection import attachListener
from flask_cors import CORS
from gevent import pywsgi
from geventwebsocket.handler import WebSocketHandler
from sqlalchemy import text
from findmyself import app

load_dotenv(override=True)
# database connection
print(os.environ.get('DATABASE_URI', "postgresql://postgres:findmyself123@34.101.69.150:5432"))

# app.config['SQLALCHEMY_DATABASE_URI'] = os.environ.get('DATABASE_URI', "postgresql://postgres:findmyself123@34.101.69.150:5432")
app.config['SQLALCHEMY_ENGINE_OPTIONS'] = {"pool_pre_ping": True}  
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql+psycopg2://postgres:findmyself123@34.101.69.150:5432'

db.init_app(app)

with app.app_context():
    db.reflect()

classes = execute()

# initialize socket io
socketio = SocketIO(app, async_handlers=True, async_mode='threading', logger=True, always_connect=True)
CORS(app, origins='*')
socketio.init_app(app, cors_allowed_origins="*")

if __name__ == '__main__':
    attachListener(socketio)
    socketio.run(app, host='0.0.0.0', port=5000, debug=False, allow_unsafe_werkzeug=True)