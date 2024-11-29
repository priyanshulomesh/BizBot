from flask_sqlalchemy import SQLAlchemy
from flask import Flask

# app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///chatbot.db'


db = SQLAlchemy()
# If you want to keep an init_db function for manual DB initialization
def init_db(app: Flask):
    with app.app_context():
        db.create_all()

