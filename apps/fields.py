from flask_restful import marshal
from flask_restful.fields import String, Raw, Integer, Nested
import json


class StaticFileUrl(Raw):
    def format(self, value):
        if value:
            return '/static/' + value[0] + '/' + value[1]
        else:
            return None


class RedisString(Raw):
    def format(self, value):
        if json.dumps(value):
            return str(value)
        else:
            return json.dumps(value)


class StringFromRedis(Raw):
    def format(self, value):
        if value:
            return str(value)
        else:
            return json.loads(value)


FileField = {
    'url': StaticFileUrl
}
FileResponseField = {
    'status': Integer,
    'data': Nested(FileField)
}

UserDataFields = {
    'name': String,
    'country': String,
    'autograpgh': String,
    'phone': String,
    'email': String,
    'icon': String  # (default='/static/icon/default.jpg')
}

UserResponseFields = {
    'status': Integer,
    'data': Nested(UserDataFields)
}

RoomToRedisFields = {
    "owner": RedisString,
    "name": RedisString,
    "icon": RedisString,
    "describe": RedisString,
    "topic": RedisString
}

RoomFromRedisFields = {
    "owner": StringFromRedis,
    "name": StringFromRedis,
    "icon": StringFromRedis,
    "describe": StringFromRedis,
    "topic": StringFromRedis
}

RoomRspField = {
    "status": Integer,
    "data": Nested(RoomFromRedisFields)
}

MessageField = {
    "message":String
}

AnnouncementField = {
    "status": Integer,
    "data": Nested(MessageField)
}