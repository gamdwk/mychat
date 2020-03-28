from flask import Blueprint
from flask_socketio import emit
user_bp = Blueprint("user", __name__)

from apps.ext import socketio

@socketio.on('json')
def handel_json(json):
    print('received json: ' + str(json))


@user_bp.route('/user')
def user():
    return "hello"


@socketio.on('connect', namespace='/test')
def test_connect():
    emit('my response', {'data': 'Connected'})


@socketio.on('disconnect', namespace='/test')
def test_disconnect():
    print('Client disconnected')