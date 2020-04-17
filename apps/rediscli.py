from redis import StrictRedis
from flask_restful import marshal, fields
from flask_restful.fields import String
import json
from flask import current_app
from .common import random_string
from .fields import RoomFromRedisFields, RoomToRedisFields

redisClient = StrictRedis(host='localhost', port=6379, db=0)


class User(object):
    def __init__(self, sid=None, name=None, country=None,
                 autograpgh=None, phone=None, email=None, icon='default.jpg'):
        self.data = {
            'sid': sid,
            'name': name,
            'country': country,
            'autograpgh': autograpgh,
            'phone': phone,
            'email': email,
            'icon': icon
        }

    def set_from_dict(self, data):
        return marshal(data, fields)

    """def get_data(self):
        data = dict()
        data['sid'] = self.sid
        data['name'] = self.name
        data['country'] = self.country
        data['autograpgh'] = self.autograpgh
        data['phone'] = self.phone
        data['email'] = self.email
        data['icon'] = self.icon
        return data"""


def creat_room(rid, data):
    if not data["name"]:
        data["name"] = rid
    new_data = marshal(data, RoomToRedisFields)
    rid = "room" + rid
    for key in new_data.keys():
        # key=json.dumps(key)
        val = new_data[key]
        redisClient.hset(rid, key, val)
    return redisClient.hgetall(rid)


def update_room(rid, data):
    new_data = marshal(data, RoomFromRedisFields)
    rid = "room" + rid
    for key in new_data.keys():
        # key=json.dumps(key)
        val = new_data[key]
        if json.loads(val):
            redisClient.hset(rid, key, val)
    return redisClient.hgetall(rid)


def get_room_message(rid):
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
    redisClient.delete(room)
