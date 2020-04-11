from redis import StrictRedis
from flask_restful import marshal, fields

redisClient = StrictRedis(host='localhost', port=6379, db=1, decode_responses=True, charset='utf-8')

userFields = {
    'sid': fields.String,
    'name': fields.String,
    'country': fields.String,
    'autograpgh': fields.String,
    'phone': fields.String,
    'email': fields.Url,
    'icon': fields.Url
}


class User(object):
    def __init__(self, sid=None, name=None, country=None,
                 autograpgh=None, phone=None, email=None, icon='default.jpg'):
        self.data = {
            'sid': sid,
            'name': name,
            'country': country,
            'autograpgh': autograpgh,
            'phone': phone,
            'email': email,
            'icon': icon
        }

    def set_from_dict(self, data):
        return marshal(data, fields)

    def get_data(self):
        data = dict()
        data['sid'] = self.sid
        data['name'] = self.name
        data['country'] = self.country
        data['autograpgh'] = self.autograpgh
        data['phone'] = self.phone
        data['email'] = self.email
        data['icon'] = self.icon
        return data
