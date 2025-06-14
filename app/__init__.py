#!/usr/bin/python3
import os
import pymysql
from flask import Flask
from dotenv import load_dotenv
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_jwt_extended import JWTManager


pymysql.install_as_MySQLdb()
load_dotenv()
db = SQLAlchemy()
jwt = JWTManager()

def create_app():
    app = Flask(__name__)

    app.config.from_object('app.config.Config')
    db.init_app(app)
    jwt.init_app(app)

    app.config['SQLALCHEMY_DATABASE_URI'] = os.environ.get('DATABASE_URI')
    app.config['SECRET_KEY'] = os.getenv('SECRET_KEY')
    app.config['JWT_SECRET_KEY'] = os.getenv('JWT_SECRET_KEY')
    app.config['JWT_TOKEN_LOCATION'] = ['headers']

    migrate = Migrate(app, db)

    from app.routes import user

    app.register_blueprint(user)

    with app.app_context():
        from app.models import User
        db.create_all()

    return app