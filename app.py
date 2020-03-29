from apps.ext import socketio
from apps import createapp
from config import Config

app = createapp(Config)

if __name__ == '__main__':
    socketio.run(app, host='0.0.0.0', port='8080')
