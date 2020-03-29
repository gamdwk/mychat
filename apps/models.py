from apps.ext import db


class User(db.Model):
    __tablename__ = 'users'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(64))
    country = db.Column(db.String(64))
    autograpgh = db.Column(db.String(128))
    phone = db.Column(db.String(64))
    email = db.Column(db.String(64))
    upicfilename = db.Column(db.String(64))