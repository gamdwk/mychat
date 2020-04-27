from datetime import timedelta
from apps.rediscli import redisClient
from redis import StrictRedis

# File_Folder = '/www/wwwroot/mychat/apps'
File_Folder = 'F:\再战西二\python\第五轮\mychat\\apps'


class Config(object):
    DEBUG = True

    SECRET_KEY = "fcb0813083644071b18f6cb9f24b740c"
    # CSRF_ENABLED = True  # 激活跨站点请求伪造保护

    # 配置json
    JSON_AS_ASCII = False
    JSON_SORT_KEYS = False

    # 配置flask-session
    SESSION_TYPE = 'redis'
    SESSION_REDIS = StrictRedis(host='localhost',  port=6379, db=0)
    # SESSION_PERMANENT = True  # 如果设置为True，则关闭浏览器session就失效。
    SESSION_USE_SIGNER = True  # 是否对发送到浏览器上session的cookie值进行加密
    SESSION_KEY_PREFIX = 'session'  # 保存到session中的值的前缀

    # PERMANENT_SESSION_LIFETIME = timedelta(days=7)

