from flask_socketio import SocketIO
from flask_restful import Api
from flask_session import Session
from flask_cors import CORS


socketio = SocketIO(binary=False, manage_session=False,logger=True,engineio_logger=True,cors_allowed_origins='*')
api = Api()
sess = Session()
cors = CORS(origins='*', supports_credentials=True)