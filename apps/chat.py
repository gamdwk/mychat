from apps.ext import socketio
from flask_socketio import Namespace, emit
from flask import Blueprint, render_template, request, session
from apps.ext import db
from apps.models import User

main = Blueprint("main", __name__)


@main.route('/')
def index():
    return render_template("test.html", async_mode=socketio.async_mode)


class ChatNamespace(Namespace):
    def on_connect(self):
        print("连接")

    def on_disconnect(self):
        print("断开连接")

    def on_my_event(self, data):
        emit('my_response')
        pass

    def on_create_room(self):
        pass

    def on_join_room(self,room):
        pass

    def on_leave_room(self, room):
        pass

    def on_break_room(self, room):
        pass

    def on_message(self, room):
        pass


socketio.on_namespace(ChatNamespace("/chat"))
