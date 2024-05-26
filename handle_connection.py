from models.call_model import predict_sam, train_sam, build_df
from concurrent.futures import ProcessPoolExecutor


def attachListener(socketio, init_model, init_features, init_access_points):

    global model
    global features
    global access_points

    model = init_model
    features = init_features
    access_points = init_access_points

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
            with ProcessPoolExecutor() as executor:
                train_job = executor.submit(train_sam)
                try:
                    response = train_job.result()
                    global model
                    global features
                    global access_points
                    model = response.get("model")
                    features = response.get("features")
                    access_points = response.get("access_points")
                except Exception as e:
                    print("Something went wrong in train.")
                    print(repr(e))

        
        elif data['command'] == 'Test!':
            build_df()

    @socketio.on('predict')
    def predict(data):
        with ProcessPoolExecutor() as executor:
            global model
            global features
            global access_points
            predict_job = executor.submit(predict_sam, model, features, access_points, data)
            try:
                result = predict_job.result()
                socketio.emit("predict_%s" % data['clientId'], result)
            except Exception as e:
                print("Something went wrong in predict")
                print(repr(e))

        