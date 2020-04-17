from apps.ext import socketio
from flask_socketio import Namespace, emit, join_room, leave_room, rooms, close_room
from flask import Blueprint, render_template, abort, request, session, current_app
from os.path import join
from flask_restful import marshal
from .rediscli import creat_room, update_room, \
    get_room_message, check_is_owner, check_room, delete_room
from .common import random_string
from .fields import RoomRspField, AnnouncementField

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

    def on_create_room(self, data):
        rid = random_string()
        join_room(room=rid)
        data["owner"] = session.sid
        new_data = creat_room(rid, data)
        resp = {"status": 0, "data": new_data}
        return marshal(resp, RoomRspField)

    def on_change_room_message(self, data):
        rid = data['rid']
        if "owner" in data.keys():
            del data["owner"]
        if check_is_owner(rid=rid, sid=session.sid):
            data["owner"] = session.sid
            resp = {
                "status": 0,
                "data": update_room(rid, data)
            }
            emit("room_message", marshal(resp, RoomRspField), room=rid)
        else:
            abort(403)

    def on_join_room(self, data):
        rid = data["rid"]
        if check_room(rid) is False:
            abort(403)
        join_room(room=rid)
        resp = {"status": 0, "data": {"rid": rid}}
        resp2 = {"status": 0, "data": {"message": session["user"]["name"] + "加入群聊"}}
        emit("announcement", marshal(resp2, AnnouncementField), room=rid)
        return marshal(resp, RoomRspField)

    def on_leave_room(self, data):
        rid = data['rid']
        if check_room(rid):
            abort(403)
        if rid in rooms(rid):
            leave_room(rid)

    def on_break_room(self, data):
        rid = data["rid"]
        resp = {"status": 0, "data": {
            "message": "本房间已被解散"
        }}
        emit("announcement", marshal(resp, AnnouncementField), room=rid)
        close_room(rid)
        delete_room(rid)

    def on_message(self, data):
        pass


socketio.on_namespace(ChatNamespace("/chat"))
