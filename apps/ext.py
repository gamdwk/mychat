from flask_sqlalchemy import SQLAlchemy
from flask_socketio import SocketIO
from flask_restful import Api
from flask_session import Session

db = SQLAlchemy()
socketio = SocketIO(manage_session=False,logger=True,engineio_logger=False,cors_allowed_origins='*')
api = Api()
sess = Session()
