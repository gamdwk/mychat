class FlaskOverallError(object):
    def __init__(self, error_code, error_message):
        self.error_code = error_code
        self.error_message = error_message

    def resp(self):
        return {
                   "status": self.error_code,
                   "message": self.error_message
               }, self.error_code


def args_error(error):
    return FlaskOverallError(400, "请求无效").resp()


def not_user_error(error):
    return FlaskOverallError(401, "用户没有相关权限")


def not_found_error(error):
    return FlaskOverallError(404, "url不存在").resp()


def not_allow_method_error(error):
    return FlaskOverallError(403, '资源不允许访问 ').resp()


def run_error(error):
    return FlaskOverallError(500, '服务器运行错误').resp()


from .ext import api, socketio


@socketio.on_error('/chat')
def chat_error(e):
    print(e)


