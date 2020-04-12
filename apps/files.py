from apps.ext import api
from flask_restful import Resource, reqparse, marshal_with, marshal, fields
from werkzeug.datastructures import FileStorage
from werkzeug.utils import secure_filename
from flask import current_app, abort
import os
from .common import random_string
from urllib.parse import urljoin


class StaticFileUrl(fields.Raw):
    def format(self, value):
        if value:
            return '/static/' + value[0]+'/'+value[1]
        else:
            return None


FileField ={
    'url': StaticFileUrl
}
FileResponseField = {
    'status': fields.Integer,
    'data': fields.Nested(FileField)
}
suffixes = {
    'image': ['jpg', 'jepg', 'gif', "exr"]
}


def check_filename(folder, filename):
    suffix = filename.split(".")[-1].lower()
    if folder in ['icon', 'pic']:
        if suffix in suffixes['image']:
            return True
        return False
    elif folder is 'files':
        return True
    return False


class Files(Resource):
    def __init__(self):
        self.reqparse = reqparse.RequestParser()
        self.reqparse.add_argument('folder', type=str, location='form')
        self.reqparse.add_argument('filename', type=str, location='form')
        self.reqparse.add_argument('file', type=FileStorage, location=['files', 'form'])

    @marshal_with(FileResponseField)
    def get(self, folder, filename):
        return

    @marshal_with(FileResponseField)
    def post(self):
        args = self.reqparse.parse_args()
        folder = args['folder']
        file = args['file']
        if not file:
            abort(100)
        if not folder:
            abort(323)
        path = os.path.join(current_app.root_path, current_app.static_folder)
        suffix = file.filename.split(".")[-1].lower()
        filename = random_string() + '.'+suffix
        if not check_filename(folder, filename):
            abort(403)
        path = os.path.join(path, folder, filename)
        file.save(path)
        file.close()
        return {'status': 0, 'data': {'url': (folder, filename)}}, 200


api.add_resource(Files, '/api/files', '/api/files/<string:folder>/<string:filename>/', endpoint='files')
