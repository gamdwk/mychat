from flask_sqlalchemy import SQLAlchemy
from flask_socketio import SocketIO
from flask_restful import Api

db = SQLAlchemy()
socketio = SocketIO()
api = Api()
