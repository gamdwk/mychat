from apps.ext import api
from flask_restful import Resource, reqparse
from flask import request, send_from_directory
from werkzeug.datastructures import FileStorage
from werkzeug.utils import secure_filename
from flask import session


class Files(Resource):
    def __init__(self):
        self.reqparse = reqparse.RequestParser()
        self.reqparse.add_argument('folder', type=str)
        self.reqparse.add_argument('filename', type=str)
        self.reqparse.add_argument('file', type=FileStorage, location='files')


    def get(self, folder, filename):
        return


    def post(self):
        parse = reqparse.RequestParser()
        parse.add_argument('file', type=FileStorage)
        args = parse.parse_args()
        file = args['file']

        return {'status':0,'folder':"/icon",'name':file.name},200


api.add_resource(Files, '/api/files', '/api/files/<string:folder>/<string:filename>/', endpoint='files')