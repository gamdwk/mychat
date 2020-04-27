from .ext import api
from flask_restful import Resource, reqparse, marshal_with, marshal, fields
from werkzeug.datastructures import FileStorage
from werkzeug.utils import secure_filename
from flask import current_app, abort, session
import os
from .common import random_string
from urllib.parse import urljoin
from .fields import FileResponseField, FileField
from flask_socketio import rooms
from os.path import exists
from .rediscli import check_user_in
from os import makedirs

folders = ['files', 'icon', 'roomIcon', 'user', 'pic']
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
    elif folder is 'userIcon':
        return True
    return False


def create_folder(path):
    if exists(path):
        return True
    try:
        makedirs(path)
        return True
    except:
        return False


class Files(Resource):
    def __init__(self):
        self.reqparse = reqparse.RequestParser()
        self.reqparse.add_argument('folder', type=str, location='form')
        self.reqparse.add_argument('filename', type=str, location='form')
        self.reqparse.add_argument('file', type=FileStorage, location=['files', 'form'])
        self.reqparse.add_argument('rid', type=str, location='form')

    @marshal_with(FileResponseField)
    def get(self, folder, filename):
        return

    @marshal_with(FileResponseField)
    def post(self):
        args = self.reqparse.parse_args()
        folder = args['folder']
        file = args['file']
        if not file:
            abort(400)
        if not folder:
            abort(400)
        if 'uid' not in session:
            abort(401)
        rid = args["rid"]
        path = os.path.join(current_app.root_path, current_app.static_folder)
        suffix = file.filename.split(".")[-1].lower()
        filename = random_string() + '.' + suffix
        if not check_filename(folder, filename):
            abort(400)
        if rid:
            folder = os.path.join(folder, rid)
            if not check_user_in(rid, session["uid"]):
                abort(403)
            else:
                path = os.path.join(current_app.root_path, rid)
                if create_folder(path):
                    path = os.path.join(path, filename)
                else:
                    abort(500)
        else:
            path = os.path.join(path, folder, filename)
        file.save(path)
        file.close()
        return {'status': 0, 'data': {'url': (folder, filename)}}, 200


api.add_resource(Files, '/api/files', '/api/files/<string:folder>/<string:filename>/', endpoint='files')
