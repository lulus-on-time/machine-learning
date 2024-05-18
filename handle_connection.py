from models.call_model import predict_model, train_model, build_df

def attachListener(socketio):

    @socketio.on('connect')
    def handle_connect():
        print("Client connected")
    
    @socketio.on('disconnect')
    def handle_disconnect():
        print('Client disconnected')

    @socketio.on('train')
    def train(data):
        socketio.emit("message", "on training handler function")
        if data['command'] == 'Train!':
            train_model.delay()
            
        elif data['command'] == 'Test!':
            build_df()

    @socketio.on('predict')
    def predict(data):
        predict_model(data, socketio)