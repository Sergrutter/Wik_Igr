from flask import Flask
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///mydatabase.db'
db = SQLAlchemy(app)


class Page(db.Model):
    """Таблица для хранения созданных страниц"""
    id = db.Column(db.Integer, primary_key = True)
    name = db.Column(db.String(100), nullable = False)
    creator = db.Column(db.String(100), nullable = False)
    url = db.Column(db.String(200), nullable = False)


class User(db.Model):
    """Таблица для хранения зарегистрировавшихся пользователей"""
    id = db.Column(db.Integer, primary_key = True)
    email = db.Column(db.String(100), nullable = False)
    name = db.Column(db.String(100), nullable = False)


db.create_all()
