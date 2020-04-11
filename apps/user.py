from .ext import api
from flask_restful import reqparse, Resource, marshal_with
from flask import session
from .models import User
from functools import wraps
from .redis import redisClient


@wraps
def login(f):
    if 'user' not in session:
        session['user'] = {}


class Users(Resource):
    def __init__(self):
        self.reqparse = reqparse.RequestParser()
        self.reqparse.add_argument('name', type=str)
        self.reqparse.add_argument('autograpgh', type=str)
        self.reqparse.add_argument('email', type=str)
        self.reqparse.add_argument('phone', type=str)
        self.reqparse.add_argument('icon', type=str)

    def get(self):
        uid = session['uid']
        u = User.query.get(uid)
        data = u.get()
        return {
            'status': 0,
            'data': data
        }

    def post(self):
        pass

    def put(self):
        args = self.reqparse.parse_args()
        u = User.query.get(session['uid'])
        u.set(args)
        pass

    def delete(self):
        pass


class Icon(Resource):
    def put(self):
        pass


api.add_resource(Users, '/user', endpoint='user')
api.add_resource(Icon, '/user/icon', endpoint='icon')