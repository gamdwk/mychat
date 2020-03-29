from flask import Flask, Blueprint, render_template
from apps.ext import db, socketio, api


def createapp(config):
    app = Flask(__name__)
    app.config.from_object(config)
    register_blueprint(app)
    register_ext(app)
    return app


def register_blueprint(app):
    from apps.chat import main
    app.register_blueprint(main)
    pass


def register_ext(app):
    api.init_app(app)
    socketio.init_app(app)
    db.init_app(app)


from apps import chat
