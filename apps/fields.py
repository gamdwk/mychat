from flask_restful import marshal
from flask_restful.fields import String, Raw, Integer, Nested, Arbitrary, List
import json


class StaticFileUrl(Raw):
    def format(self, value):
        if value:
            return '/static/' + value[0] + '/' + value[1]
        else:
            return None


class RedisString(Raw):
    def format(self, value):
        return json.dumps(value)


class StringFromRedis(Raw):
    def format(self, value):
        return str(value)


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
    "rid": String,
    "owner": String,
    "name": String,
    "icon": String,
    "describe": String,
    "topic": String
}

RoomFromRedisFields = RoomToRedisFields

RoomRspField = {
    "status": Integer,
    "data": Nested(RoomFromRedisFields)
}

MessageField = {
    "message": String,
    "rid": String
}

AnnouncementField = {
    "status": Integer,
    "data": Nested(MessageField)
}

SendMessageField = {
    "rid": String,
    "uid": String,
    "index": Integer,
    "content": String,
    "url": String,
    "type": Integer,
    "time": Arbitrary
}

SendMessageRespField = {
    "status": Integer,
    "data": Nested(SendMessageField)
}


class MessageList(Raw):
    def format(self, value):
        return marshal(value, SendMessageField)


MessageListRspField = {
    "status": Integer,
    "data": List(MessageList)
}