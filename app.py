from apps.ext import socketio
from apps import createapp
from config import Config

app = createapp(Config)

if __name__ == '__main__':
    socketio.run(app)
