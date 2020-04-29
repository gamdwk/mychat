from .rediscli import redisClient, check_user_in
from .ext import api
from flask_restful import Resource, reqparse
from flask import session, abort, request
import re
import json


class SearchApi(Resource):
    def __init__(self):
        self.reqparse = reqparse.RequestParser()
        self.reqparse.add_argument('args', type=str, location=['values', 'args', 'json', 'form'])
        self.reqparse.add_argument('rid', type=str, location=['values', 'args', 'json', 'form'])

    def get(self):
        args = self.reqparse.parse_args()
        ars = args['args']
        if ars is None:
            abort(400)
        if args['rid'] is None:
            abort(400)
        if 'uid' not in session:
            abort(403)
        elif not check_user_in(session['uid'], args['rid']):
            abort(403)
        else:
            messages = search(ars, args['rid'])
            ms = list()
            for message in messages:
                message = json.loads(message)
                uid = message['uid']
                name = redisClient.hget('user'+uid, 'name')
                message['name'] = name
                del message['uid']
                ms.append(message)
            return {
                "status": 0,
                "messages": ms
            }


def search(args, rid):
    mid = "message" + rid
    messages = redisClient.lrange(mid, 0, -1)
    args = args.split()

    def has_args(message):
        message = json.loads(message)
        if 'content' not in message:
            return False
        content = message['content']
        for arg in args:
            if content.find(arg) != -1:
                return True
        return False

    return list(filter(has_args, messages))


api.add_resource(SearchApi, '/search', endpoint='search')
