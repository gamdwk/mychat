# encoding: utf-8
# 仅用于数据库迁移
from flask_script import Manager
from flask_migrate import Migrate, MigrateCommand
from app import app
from apps.ext import db

manager = Manager(app)
migrate = Migrate(app, db)
manager.add_command('db', MigrateCommand)

if __name__ == '__main__':
    manager.run()
