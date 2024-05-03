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

# def run():
load_dotenv(override=True)
# database connection
print(os.environ.get('DATABASE_URI', "postgresql://postgres:ta@localhost:5431"))


app.config['SQLALCHEMY_DATABASE_URI'] = os.environ.get('DATABASE_URI', "postgresql://postgres:ta@localhost:5431")

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
    socketio.run(app, debug=True)
    # server = pywsgi.WSGIServer(("", 5000), app, handler_class=WebSocketHandler)
    
    # # Set the number of worker processes to 2
    # server.spawn = 6

    # # Start the server
    # server.serve_forever()

