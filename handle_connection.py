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
            
        elif data['command'] == 'Test!':
            build_df()

    @socketio.on('predict')
    def predict(data):
        threading.Thread(target=predict_model, args=(data, socketio)).start()
