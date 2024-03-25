
@socketio.on('connect')
def handle_connect():
    print('Connected to WebSocket server')

@socketio.on('disconnect')
def handle_disconnect():
    print('Disconnected from WebSocket server')