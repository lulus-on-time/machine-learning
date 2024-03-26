import json
from flask_socketio import send

def attachListener(socketio):

    @socketio.on('connect')
    def handleConnection():
        print("Client connected")

    @socketio.on('predict')
    def handle_websocket_message(message):
        # Convert the message to a JSON object

        # Handle JSON
        print("hello")
        send("Message received")
