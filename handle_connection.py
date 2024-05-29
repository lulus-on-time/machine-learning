from models.call_model import predict_sam, train as handle_train, build_df
from concurrent.futures import ProcessPoolExecutor
import multiprocessing
from flask_socketio import SocketIO
import time

predict_executor = ProcessPoolExecutor(mp_context=multiprocessing.get_context("fork"))
train_executor = ProcessPoolExecutor(mp_context=multiprocessing.get_context("fork"))

def attachListener(socketio: SocketIO, init_ml_dict):
    global ml_dict
    ml_dict = init_ml_dict

    # def init_predict(init_ml_dict, init_socketio):
    #     global ml_dict
    #     global socketio
    #     ml_dict = init_ml_dict
    #     socketio = init_socketio

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
            global train_executor
            train_job = train_executor.submit(handle_train, data)
            response = train_job.result()
            global ml_dict
            ml_dict = response
            # global predict_executor
            # delete_executor = predict_executor
            # predict_executor = ProcessPoolExecutor(mp_context=multiprocessing.get_context("fork"))
            # time.sleep(5)
            # delete_executor.shutdown()
        
        elif data['command'] == 'Test!':
            build_df()
        

    @socketio.on('predict')
    def predict(data):
        global ml_dict
        global predict_executor
        predict_job = predict_executor.submit(predict_sam, ml_dict['model'], ml_dict['features'], ml_dict['access_points'], data)
        result = predict_job.result()
        socketio.emit("predict_%s" % data['clientId'], result)

        