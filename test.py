from flask_socketio import SocketIOTestClient
from mychat.app import app
from mychat.apps.ext import socketio

flask_test_client = app.test_client(use_cookies=True)
flask_test_client = app.test_client(use_cookies=True)
myclient = SocketIOTestClient(app=app, socketio=socketio,
                              namespace='/chat', flask_test_client=flask_test_client)
client2 = SocketIOTestClient(app=app, socketio=socketio,
                              namespace='/chat', flask_test_client=flask_test_client)
print(myclient.get_received(namespace='/chat'))


while True:
    """jpg = join("F:\再战西二\python\第五轮\mychat\\apps\static\icon", "default.jpg")
    with open(jpg, mode='rb') as f:
        myclient.emit('create_room', f.read(), binary=True, callback=print())"""
    myclient.emit('create_room', {'name': 'dcd', 'skwos': 'jiw'}, namespace='/chat')
    uid = myclient.get_received()["get_uid"]
    myclient.disconnect()
    print(myclient.get_received(namespace='/chat',))
    myclient.connect(namespace='/chat')
    myclient.emit('create_room', {'name': 'dcd', 'skwos': 'jiw'}, namespace='/chat')
    break

print(myclient.get_received(namespace='/chat'))