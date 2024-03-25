from app import app
from flask_socketio import SocketIO

socketio = SocketIO(app)

@socketio.on('connect')
def handle_connect():
    print('Connected to WebSocket server')

@socketio.on('disconnect')
def handle_disconnect():
    print('Disconnected from WebSocket server')

# if __name__ == '__main__':
#     socketio.run(app)