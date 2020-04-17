from .ext import api
from flask_restful import reqparse, Resource, marshal_with, fields, marshal
from flask import session, abort, current_app
from collections import OrderedDict
from os import remove
from os.path import join
from .fields import UserDataFields, UserResponseFields


class Users(Resource):
    def __init__(self):
        self.reqparse = reqparse.RequestParser()
        self.reqparse.add_argument('name', type=str, location='form')
        self.reqparse.add_argument('country', type=str, location='form')
        self.reqparse.add_argument('autograpgh', type=str, location='form')
        self.reqparse.add_argument('email', type=str, location='form')
        self.reqparse.add_argument('phone', type=str, location='form')
        self.reqparse.add_argument('icon', type=str, location='form', default='/static/icon/default.jpg')

    @marshal_with(UserResponseFields)
    def get(self):
        if 'user' not in session.keys():
            abort(403)
        if not session['user']['name']:
            abort(403)
        user = session['user']
        return {
            'status': 0,
            'data': user
        }

    @marshal_with(UserResponseFields)
    def put(self):
        args = self.reqparse.parse_args()
        if 'user' not in session.keys():
            session['user'] = OrderedDict()
        if args['name'] is None:
            if "name" not in session['user']:
                abort(400)
            if session['user']['name'] is None:
                abort(400)
        data = marshal(data=args, fields=UserDataFields)
        update(session['user'], data)
        return {
            'status': 0,
            'data': session['user']
        }

    def delete(self):
        pass


api.add_resource(Users, '/user', endpoint='user')


def update(user, data):
    if data['icon']:
        old_icon = user['icon']
        if old_icon != '/static/icon/default.jpg':
            path = join(current_app.config["File_Folder"], old_icon)
            remove(path)
    for key in data.keys():
        if data[key] is None:
            continue
        else:
            user[key] = data[key]
