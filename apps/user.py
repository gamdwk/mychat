from .ext import api
from flask_restful import reqparse, Resource, marshal_with, fields, marshal, abort
from flask import session, current_app, g, request
from collections import OrderedDict
from os import remove
from os.path import join
from .fields import UserDataFields, UserResponseFields
from .common import random_string
from .rediscli import set_user, get_user, check_user, init_user
from flask_socketio import emit, rooms


class Users(Resource):
    def __init__(self):
        self.reqparse = reqparse.RequestParser()
        self.reqparse.add_argument('name', type=str, location='form')
        self.reqparse.add_argument('country', type=str, location='form')
        self.reqparse.add_argument('autograpgh', type=str, location='form')
        self.reqparse.add_argument('email', type=str, location='form')
        self.reqparse.add_argument('phone', type=str, location='form')
        self.reqparse.add_argument('icon', type=str, location='form')

    @marshal_with(UserResponseFields)
    def get(self):
        if 'uid' not in session.keys():
            abort(403)
        if not check_user(session["uid"]):
            abort(403)
        user = get_user(session["uid"])
        return {
            'status': 0,
            'data': user
        }

    def post(self):
        if 'uid' in session.keys():
            pass
        else:
            session['uid'] = random_string()
            init_user(session['uid'])
        return {"status": 0, "data": {"uid": session["uid"]}}

    @marshal_with(UserResponseFields)
    def put(self):
        args = self.reqparse.parse_args()
        print(args)
        if 'uid' not in session.keys():
            abort(403)
        data = set_user(session["uid"], args)
        data = marshal(data=data, fields=UserDataFields)

        return {
            'status': 0,
            'data': data
        }

    def delete(self):
        pass


api.add_resource(Users, '/user', endpoint='user')
