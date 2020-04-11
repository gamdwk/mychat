from apps.ext import db
import os
from apps.common import random_string
from flask import request


class User(db.Model):
    __tablename__ = 'user'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(64))
    country = db.Column(db.String(64))
    autograpgh = db.Column(db.String(128))
    phone = db.Column(db.String(64))
    email = db.Column(db.String(64))
    icon = db.Column(db.String(64), default='default.jpg')

    def __repr__(self):
        return str(self.id)

    def set(self, data):
        self.name = data['name']
        self.autograpgh = data['autograpgh']
        self.country = data['country']
        self.email = data['email']
        self.phone = data['phone']
        self.icon = data['icon']

    def get(self):
        return {
            'name': self.name,
            'autograpgh': self.autograpgh,
            'country': self.country,
            'email': self.email,
            'phone': self.phone,
            'icon': self.icon
        }
