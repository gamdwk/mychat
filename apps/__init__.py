from flask import Flask


def createapp(config):
    app = Flask(__name__)
    app.config.from_object(config)
    register_blueprint(app)
    register_ext(app)
    register_error(app)
    return app


def register_blueprint(app):
    from .user import test
    app.register_blueprint(test)
    pass


def register_ext(app):
    from .ext import socketio, api, cors, sess
    api.init_app(app)
    socketio.init_app(app)
    sess.init_app(app)
    cors.init_app(app)


def register_error(app):
    # 以下错误只会在flask触发，不在api和socket.io触发
    from .errors import not_found_error, not_allow_method_error, run_error, args_error, not_user_error
    app.register_error_handler(404, not_found_error)
    app.register_error_handler(403, not_allow_method_error)
    app.register_error_handler(500, run_error)
    app.register_error_handler(400, args_error)
    app.register_error_handler(401, not_user_error)


from . import chat, common, files, ext, user, rediscli, errors, fields, search
