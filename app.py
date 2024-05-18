from gevent import monkey; monkey.patch_all()
from classes import execute
from database import db
from dotenv import load_dotenv
import os
from flask_socketio import SocketIO
from handle_connection import attachListener
from flask_cors import CORS
from findmyself import app
from models.call_model import train_model

load_dotenv(override=True)

app.config['SOCKETIO_REDIS_URL'] = 'redis://localhost:6379/0'

with app.app_context():
    db.reflect()

classes = execute()
train_model.delay()

# initialize socket io
socketio = SocketIO(app, async_handlers=True, async_mode = 'gevent', logger=True, always_connect=True, message_queue=app.config['SOCKETIO_REDIS_URL'])
CORS(app, origins='*')
socketio.init_app(app, cors_allowed_origins="*")

if __name__ == '__main__':
    attachListener(socketio)
    socketio.run(app, debug=True)