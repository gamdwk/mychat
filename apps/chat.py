from .ext import socketio
from flask_socketio import Namespace, emit, join_room, leave_room, rooms, close_room, send, disconnect
from flask import Blueprint, render_template, abort, request, session, current_app, g
from os.path import join
from flask_restful import marshal
from .rediscli import create_room, update_room, get_message_list, check_user, get_room_people_num, \
    get_room_information, check_is_owner, check_room, delete_room, save_message, get_user, out_room, in_room
from .common import random_string
from .fields import RoomRspField, AnnouncementField, RoomFromRedisFields, \
    SendMessageField, UserDataFields, MessageListRspField


class ChatNamespace(Namespace):
    def on_connect(self):
        if 'uid' not in session.keys():
            disconnect()
        else:
            emit('get_uid', {"status": 0, "data": {"uid": session['uid']}})

    def on_disconnect(self):
        """for room in rooms():
            if room is request.sid:
                continue
            else:
                leave_room(room)
                out_room(session['uid'], room)"""
        pass

    def on_create_room(self, data):
        rid = random_string()
        data["owner"] = session["uid"]
        new_data = create_room(rid, data)
        resp = {"status": 0, "data": new_data}
        emit("owner_change", marshal(resp, RoomRspField))
        join_room(room=rid)
        in_room(session["uid"], rid)
        people = get_room_people_num(rid)
        emit("room_people", people, room=rid)

    def on_change_room_message(self, data):
        rid = data['rid']
        if "owner" in data.keys():
            del data["owner"]
        if check_is_owner(rid=rid, sid=session['uid']):
            data["owner"] = session['uid']
            d = update_room(rid, data)
            resp = {
                "status": 0,
                "data": d
            }
            room_data = marshal(resp, RoomRspField)
            emit('owner_change', room_data)
            emit("room_message", room_data, room=rid, include_self=False)
        else:
            emit("announcement", {"status": 401, "message": "你不是房间的主人"})

    def on_join_room(self, data):
        if 'rid' not in data:
            return
        rid = data["rid"]
        if not check_room(rid):
            emit("room_message", {"status": 404, "message": "房间不存在"})
        elif rid in rooms():
            pass
        else:
            join_room(room=rid)
            in_room(session["uid"], rid)
            user = get_user(session["uid"])
            d = get_room_information(rid)
            d["rid"] = rid
            resp = {"status": 0, "data": d}
            if "name" in user:
                name = user["name"]
            else:
                name = "匿名用户"
            resp2 = {"status": 0, "data": {"message": name + "加入群聊", "rid": rid}}
            emit("announcement", marshal(resp2, AnnouncementField), room=rid)
            people = get_room_people_num(rid)
            emit("room_people", people, room=rid)
            emit("room_message", marshal(resp, RoomRspField))

    def on_leave_room(self, data):
        rid = data['rid']
        if not check_room(rid):
            emit("announcement", {"status": 401, "message": "你不在房间"})
        elif rid in rooms():
            user = get_user(session["uid"])
            out_room(session["uid"], rid)
            if "name" in user:
                name = user["name"]
            else:
                name = "匿名用户"
            resp = {"status": 0, "data": {"message": name + "离开群聊", "rid": rid}}
            emit("announcement", marshal(resp, AnnouncementField), room=rid)
            leave_room(rid)
            people = get_room_people_num(rid)
            emit("room_people", people, room=rid)
        else:
            emit("announcement", {"status": 401, "message": "你不在房间"})

    def on_break_room(self, data):
        rid = data["rid"]
        if check_room(rid) and check_is_owner(rid, session['uid']):
            resp = {"status": 0, "data": {
                "message": "本房间已被解散",
                "rid": rid
            }}
            emit("announcement", marshal(resp, AnnouncementField), room=rid)
            emit("room_alive", {"status": 0, "data": {"rid": rid, "break": True}}, room=rid)
            close_room(rid)
            delete_room(rid)
        else:
            emit("announcement", {"status": 401, "message": "你不是房间的主人"})

    def on_message(self, data):
        room = data["rid"]
        if room in rooms():
            uid = session["uid"]
            message = save_message(room, uid, data)
            send(marshal(message, SendMessageField), room=room)
        else:
            emit("announcement", {"status": 401, "message": "你不是在房间"})

    def on_get_message_list(self, data):
        room = data["rid"]
        if room in rooms():
            l = get_message_list(room, data['index'])
            res = {
                "status": 0,
                "data": l
            }
            emit("message_list", res)
        else:
            emit("announcement", {"status": 401, "message": "你不是在房间"})

    def on_user_inform(self, data):
        uid = data["uid"]
        if not check_user(uid):
            emit("user_inform", {"status": 0, "data": {"message": "用户已注销", 'uid': uid}})
        else:
            data = get_user(uid)
            user = marshal(data, UserDataFields)
            user["uid"] = uid
            emit("user_inform", {"status": 0, "data": user})

    def on_flash_user(self):
        data = get_user(session["uid"])
        data = marshal(data=data, fields=UserDataFields)
        data['uid'] = session['uid']
        res = {
            'status': 0,
            'data': data
        }
        for room in rooms():
            emit('user_inform', res, room=room)


socketio.on_namespace(ChatNamespace("/chat"))
