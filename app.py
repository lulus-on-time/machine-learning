from gevent import monkey; monkey.patch_all()
from classes import execute
from database import db
from dotenv import load_dotenv
import os, sys
from flask_socketio import SocketIO
from handle_connection import attachListener
from flask_cors import CORS
from findmyself import app
from models.call_model import train_model
import time
import logging
logging.basicConfig(level=logging.DEBUG, format='%(asctime)s %(levelname)s %(message)s', handlers=[logging.StreamHandler(sys.stdout)])

logger = logging.getLogger()
load_dotenv(override=True)

app.config['SOCKETIO_REDIS_URL'] = 'redis://34.101.77.142:6379/0'

with app.app_context():
    db.reflect()

classes = execute()

# initialize socket io
socketio = SocketIO(app, async_handlers=True, async_mode = 'gevent', logger=True, always_connect=True, message_queue=app.config['SOCKETIO_REDIS_URL'])
CORS(app, origins='*')
socketio.init_app(app, cors_allowed_origins="*")

time.sleep(7)
train_model.delay()
time.sleep(7)
train_model.delay()
time.sleep(7)
train_model.delay()
time.sleep(7)
train_model.delay()

if __name__ == '__main__':
    attachListener(socketio)
    socketio.run(app, debug=False, host='0.0.0.0', port=5000)