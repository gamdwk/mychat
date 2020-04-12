from .ext import api
from flask_restful import reqparse, Resource, marshal_with, fields, marshal
from flask import session
from collections import OrderedDict


UserDataFields = {
    'name': fields.String,
    'country': fields.String,
    'autograpgh': fields.String,
    'phone': fields.String,
    'email': fields.String,
    'icon': fields.String
}

UserResponseFields = {
    'status': fields.Integer,
    'data': fields.Nested(UserDataFields)
}


class Users(Resource):
    def __init__(self):
        self.reqparse = reqparse.RequestParser()
        self.reqparse.add_argument('name', type=str, location='form')
        self.reqparse.add_argument('autograpgh', type=str, location='form')
        self.reqparse.add_argument('email', type=str, location='form')
        self.reqparse.add_argument('phone', type=str, location='form')
        self.reqparse.add_argument('icon', type=str, location='form')

    @marshal_with(UserResponseFields)
    def get(self):
        if 'user' not in session.keys():
            session['user'] = OrderedDict()
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
        print(args)
        data = marshal(data=args, fields=UserDataFields)
        session['user'].update(data)
        return {
            'status': 0,
            'data': data
        }

    def delete(self):
        pass


class Icon(Resource):
    def put(self):
        pass


api.add_resource(Users, '/user', endpoint='user')
api.add_resource(Icon, '/user/icon', endpoint='icon')
