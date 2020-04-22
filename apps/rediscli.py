from redis import StrictRedis, ConnectionPool
from flask_restful import marshal, fields
from flask_restful.fields import String
import json
from flask import current_app
from .common import random_string
from .fields import RoomFromRedisFields, RoomToRedisFields, SendMessageField
from datetime import datetime

# pool = ConnectionPool(host='localhost',  port=6379)
redisClient = StrictRedis(host='localhost',  port=6379, db=0, decode_responses=True)


def creat_room(rid, data):
    data["rid"] = rid
    if not data["name"]:
        data["name"] = rid
    new_data = marshal(data, RoomToRedisFields)
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
    for key in new_data.keys():
        # key=json.dumps(key)
        val = new_data[key]
        if val:
            redisClient.hset(rid, key, val)
    return redisClient.hgetall(rid)


def get_room_message(rid):
    return redisClient.hgetall(rid)


def check_is_owner(rid, sid):
    rid = "room" + rid
    user = redisClient.hget(rid, "owner")
    if user == sid:
        print("是主人")
        return True
    else:
        print("不是主人")
        return False


def check_room(rid):
    rid = "room" + rid
    print(redisClient.exists(rid))
    if redisClient.exists(rid):
        return True
    return False


def delete_room(rid):
    room = "room" + rid
    redisClient.delete(room)


def save_message(room, sid, data):
    mid = "message" + room
    data["uid"] = sid
    time = datetime.utcnow().timestamp()
    data["time"] = time
    message = marshal(data, SendMessageField)
    redis_message = json.dumps(message)
    redisClient.rpush(mid, redis_message)
    message = redisClient.lindex(mid, -1)
    message = json.loads(message)
    return message


def get_message_list(room):
    mid = "message"+room


pubsub = redisClient.pubsub()
