#!/usr/bin/python3
from flask import Flask
from app.errors import handle_bad_request, handle_not_found
from app.routes import add_user, get_single_user, list_users
from app.routes import modify_user, delete_user


def create_app():
    app = Flask(__name__)

    from app.routes import user
    app.register_blueprint(user)

    return app