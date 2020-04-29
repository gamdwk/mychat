from redis import StrictRedis, ConnectionPool
from flask_restful import marshal, fields
from flask_restful.fields import String
import json
from flask import current_app
from .common import random_string
from .fields import RoomFromRedisFields, RoomToRedisFields, SendMessageField, UserDataFields
from datetime import datetime
from os import remove
from os.path import join

File_Folder = '/www/wwwroot/mychat/apps'
# pool = ConnectionPool(host='localhost',  port=6379)
redisClient = StrictRedis(host='localhost', port=6379, db=0, decode_responses=True)


def check_user(uid):
    name = "user" + uid
    if redisClient.exists(name):
        return True
    return False


def set_user(uid, data):
    name = "user" + uid
    marshal(data, UserDataFields)
    if data['icon']:
        if redisClient.hexists(name, 'icon'):
            old_icon = redisClient.hget(name, 'icon')
            if old_icon != '/static/icon/default.jpg':
                path = File_Folder+old_icon
                try:
                    remove(path)
                except:
                    print(path)

    for k, v in data.items():
        if v is None:
            continue
        redisClient.hset(name, k, v)
    return redisClient.hgetall(name)


def get_user(uid):
    name = "user" + uid
    if redisClient.exists(name):
        return redisClient.hgetall(name)
    else:
        return None


def create_room(rid, data):
    data["rid"] = rid
    u = "user_in" + rid
    me = data["owner"]
    redisClient.sadd(u, me)
    new_data = marshal(data, RoomToRedisFields)
    if not new_data["name"]:
        new_data["name"] = rid
    if not new_data['icon']:
        new_data['icon'] = "/static/roomIcon/default.jpg"
    rid = "room" + rid
    for key in new_data.keys():
        # key = json.dumps(key)
        val = new_data[key]
        if val:
            redisClient.hset(rid, key, val)
    return redisClient.hgetall(rid)


def update_room(rid, data):
    data["rid"] = rid
    new_data = marshal(data, RoomToRedisFields)
    rid = "room" + rid
    print(redisClient.hgetall(rid))
    if new_data['icon']:
        if redisClient.hexists(rid, 'icon'):
            icon = redisClient.hget(rid, 'icon')
            if icon != '/static/roomIcon/default.jpg':
                try:
                    remove(File_Folder+ icon)
                except:
                    print(icon)
    else:
        if not redisClient.hexists(rid, 'icon'):
            redisClient.hset(rid, 'icon', '/static/roomIcon/default.jpg')

    for key in new_data.keys():
        # key=json.dumps(key)
        val = new_data[key]
        if val:
            redisClient.hset(rid, key, val)
    return redisClient.hgetall(rid)


def get_room_information(rid):
    rid = "room" + rid
    return redisClient.hgetall(rid)


def check_is_owner(rid, sid):
    rid = "room" + rid
    user = redisClient.hget(rid, "owner")
    if user == sid:
        return True
    else:
        return False


def check_room(rid):
    rid = "room" + rid
    if redisClient.exists(rid):
        return True
    return False


def delete_room(rid):
    room = "room" + rid
    icon = redisClient.hget(room, "icon")
    if icon != '/static/roomIcon/default.jpg':
        try:
            remove(join(File_Folder, icon))
        except:
            print(join(File_Folder, icon) + "不存在")
    redisClient.delete(room)
    mid = "message" + rid
    redisClient.delete(mid)
    u = "user_in" + rid
    redisClient.delete(u)
    folders = ['static/files/', 'static/pic/']
    for folder in folders:
        path = join(File_Folder,  folder + rid)
        try:
            remove(path)
        except:
            print(path)


def save_message(room, sid, data):
    mid = "message" + room
    data["uid"] = sid
    time = datetime.now().timestamp()
    data["time"] = time
    if not redisClient.exists(mid):
        data["index"] = 0
    else:
        m = redisClient.lindex(mid, -1)
        data["index"] = json.loads(m)["index"] + 1
    message = marshal(data, SendMessageField)
    redis_message = json.dumps(message)
    redisClient.rpush(mid, redis_message)
    message = redisClient.lindex(mid, -1)
    message = json.loads(message)
    return message


def get_message_list(room, rindex):
    mid = "message" + room
    if redisClient.llen(mid) <= 10:
        lindex = 0
    elif rindex > 11:
        lindex = rindex - 11
    elif rindex == -1:
        lindex = -10
        rindex = 0
    else:
        lindex = 0
    message_list = redisClient.lrange(mid, lindex, rindex - 1)
    m_list = list()
    for x in message_list:
        y = marshal(json.loads(x), SendMessageField)
        m_list.append(y)
    return m_list


def get_room_people_num(room):
    u = "user_in" + room
    return redisClient.scard(u)


def check_user_in(uid, rid):
    u = "user_in" + rid
    if redisClient.sismember(u, uid):
        return True
    else:
        return False


def in_room(uid, rid):
    u = "user_in" + rid
    if redisClient.exists(u):
        redisClient.sadd(u, uid)
        return True
    else:
        return False


def out_room(uid, rid):
    u = "user_in" + rid
    if redisClient.exists(u) and check_user_in(uid, rid):
        redisClient.srem(u, uid)
        return True
    else:
        return False


def init_user(uid):
    u = "user" + uid
    redisClient.hset(u, 'icon', '/static/icon/default.jpg')
    return True

