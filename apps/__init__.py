from flask import Flask


def createapp(config):
    app = Flask(__name__)
    app.config.from_object(config)
    register_blueprint(app)
    register_ext(app)
    return app


def register_blueprint(app):
    from apps.chat import main
    app.register_blueprint(main)


def register_ext(app):
    from apps.ext import db, socketio, api,sess
    api.init_app(app)
    socketio.init_app(app)
    db.init_app(app)
    sess.init_app(app)
    db.create_all(app=app)


from apps import chat,common,files,ext,models,user
