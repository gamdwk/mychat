from flask_socketio import SocketIOTestClient
from app import app
from apps.ext import socketio
import json
from werkzeug.datastructures import FileStorage
from io import BytesIO
from os.path import join
from time import sleep
import struct

flask_test_client = app.test_client()
myclient = SocketIOTestClient(app=app, socketio=socketio,
                              namespace='/chat', flask_test_client=flask_test_client)
myclient.connect('/chat')
while True:
    """jpg = join("F:\再战西二\python\第五轮\mychat\\apps\static\icon", "default.jpg")
    with open(jpg, mode='rb') as f:
        myclient.emit('create_room', f.read(), binary=True, callback=print())"""
    myclient.emit('name',)
    myclient.emit('create_room', {'name':'dcd','skwos':'jiw'})
    break

myclient.disconnect()

