from classes import execute
from database import db
from dotenv import load_dotenv
import os, sys
from flask_socketio import SocketIO
from handle_connection import attachListener
from flask_cors import CORS
from findmyself import app
from models.call_model import train
import logging

logging.basicConfig(level=logging.DEBUG, format='%(asctime)s %(levelname)s %(message)s', handlers=[logging.StreamHandler(sys.stdout)])

logger = logging.getLogger()
load_dotenv(override=True)

with app.app_context():
    db.reflect()

classes = execute()

# initialize socket io
socketio = SocketIO(app, async_handlers=True, logger=True, always_connect=True)
CORS(app, origins='*')
socketio.init_app(app, cors_allowed_origins="*")

if __name__ == '__main__':
    ml_dict = train()
    attachListener(socketio, ml_dict)
    socketio.run(app, debug=False, host='0.0.0.0', port=5001, allow_unsafe_werkzeug=True)