from flask import Flask
import pickle 
import numpy as np
from flask_socketio import send, emit, SocketIO
import logging
from sklearn.metrics import make_scorer, accuracy_score
from models.call_model import model, predict_model, train_model, update_bssid, build_df
from classes import execute
import threading
import concurrent.futures
from celery.result import AsyncResult

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
            threading.Thread(target=train_model).start()
            # task = train_model.delay()
            # print(task.task_id)
            # res = AsyncResult("efd33b19-e944-4230-b8a4-f2e94b8a5579")
            # res.ready()
            
        elif data['command'] == 'Test!':
            build_df()

    @socketio.on('predict')
    def predict(data):
        threading.Thread(target=predict_model, args=(data, socketio)).start()
        # socketio.emit("message", "on predict handler function")
        # socketio.start_background_task(predict_model(data))
        # print("yohoo")

        # predict_values = predict_model(data)

        # result = {
        #     "prediction": predict_values
        # }
        # print(result)

        # emit('prediction_result', result)
        # with concurrent.futures.ThreadPoolExecutor() as executor:
        #     future = executor.submit(predict_model, data)
        #     result = future.result()  # Wait for the prediction task to complete
        #     # Emit the prediction result to the client
        #     socketio.emit('prediction_result', result)

        # predict_thread = threading.Thread(target=flask_context_thread, args=(lambda: predict_model(data),))
        # print(predict_thread)
        # predict_thread.start()

        # predict_thread.join()
        # print(predict_thread)
        # prediction_result = predict_thread.result() 