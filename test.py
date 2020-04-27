from flask_socketio import SocketIOTestClient
from app import app
from apps.ext import socketio
from flask import url_for, session
from werkzeug.test import EnvironBuilder

app.testing = True
env = EnvironBuilder(base_url="localhost:5000/user")
flask_test_client = app.test_client(use_cookies=True)
flask_test_client2 = app.test_client(use_cookies=True)
myclient = SocketIOTestClient(app=app, socketio=socketio,
                              namespace='/chat', flask_test_client=flask_test_client)
client2 = SocketIOTestClient(app=app, socketio=socketio,
                             namespace='/chat', flask_test_client=flask_test_client2)
print(myclient.get_received(namespace='/chat'))
print(client2.get_received(namespace='/chat'))
print(myclient.sid)
myclient.emit()

a = input()
if int(a) is 1:
    b = myclient.emit("create_room", {"name":"de"}, namespace='/chat', callback = True)
    print(b)
print(myclient.get_received(namespace='/chat'))

