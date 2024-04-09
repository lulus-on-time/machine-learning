from flask import Flask
from models import execute
from database import db
from dotenv import load_dotenv
import os
from flask_socketio import SocketIO
from handle_connection import attachListener
from flask_cors import CORS
from gevent import pywsgi
from geventwebsocket.handler import WebSocketHandler

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
    # pywsgi.WSGIServer(("", 5000), app, handler_class=WebSocketHandler).serve_forever()
    socketio.run(app, debug=True)

@app.route('/train')
def train():
    ap = classes['AccessPoint']
    # ap.id
    print(ap.id)

    return {}, 200

@app.route('/aps', methods=['GET'])
def read_aps():
    aps = AccessPoint.query.all()
    results = [
        {
            "bssid": AccessPoint.bssid,
            "ssid": AccessPoint.ssid,
            "description": AccessPoint.description,
        }
    for ap in aps ] 
