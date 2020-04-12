from .ext import api
from flask_restful import reqparse, Resource, marshal_with, fields, marshal
from flask import session, abort
from collections import OrderedDict

UserDataFields = {
    'name': fields.String,
    'country': fields.String,
    'autograpgh': fields.String,
    'phone': fields.String,
    'email': fields.String,
    'icon': fields.String  # (default='/static/icon/default.jpg')
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
            if not session['user']['name']:
                abort(400)
        data = marshal(data=args, fields=UserDataFields)
        session['user'].update(data)
        return {
            'status': 0,
            'data': data
        }

    def delete(self):
        pass


api.add_resource(Users, '/user', endpoint='user')
