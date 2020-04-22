from flask import Flask


def createapp(config):
    app = Flask(__name__)
    app.config.from_object(config)
    register_blueprint(app)
    register_ext(app)
    return app


def register_blueprint(app):
    from .chat import main
    app.register_blueprint(main)


def register_ext(app):
    from .ext import socketio, api, sess, cors
    api.init_app(app)
    socketio.init_app(app)
    sess.init_app(app)
    cors.init_app(app)


from . import chat, common, files, ext, user, rediscli, errors, fields
