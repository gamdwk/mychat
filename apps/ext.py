from flask_socketio import SocketIO
from flask_restful import Api
from flask_session import Session
from flask_cors import CORS

socketio = SocketIO(manage_session=False, cors_allowed_origins='*',engineio_logger=True,logger=True)
api = Api()
sess = Session()
cors = CORS(origins='*', supports_credentials=True)
