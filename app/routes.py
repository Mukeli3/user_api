#!/usr/bin/python3
from flask import request, jsonify, Blueprint
from app.models import *
from app.validate import validate_data


user = Blueprint('user', __name__)


@user.route('/users', methods=["POST"])
def add_user():
    data = request.get_json()
    errors = validate_data(data)
    if errors:
        return jsonify({"errors": errors}), 400
    user = create_user(data["name"], data["email"], data["age"])
    return jsonify(user), 201


@user.route("/users/<user_id>", methods=["GET"])
def get_single_user(user_id):
    user = get_user(user_id)
    if not user:
        return jsonify({"error": "User not found."}), 404
    return jsonify(user), 201


@user.route("/users", methods=["GET"])
def list_users():
    return jsonify(get_all_users())


@user.route("/users/<user_id>", methods=["PUT"])
def modify_user(user_id):
    data = request.get_json()
    user = update_user(user_id, **data)
    if not user:
        return jsonify({"error": "User not found"}), 404
    return jsonify(user), 201


@user.route("/users/<user_id>", methods=["DELETE"])
def delete_user(user_id):
    user = delete_user(user_id)
    if not user:
        return jsonify({"error": "User not found"}), 404
    return jsonify({"message": "User successfully deleted"}), 200
