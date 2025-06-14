#!/usr/bin/python3
import bcrypt
import json
import redis
from flask import request, jsonify, Blueprint
from flask_jwt_extended import create_access_token, jwt_required, get_jwt_identity
from app.models import User, db
from app.validate import validate_data


r = redis.Redis(host='localhost', port=6379, db=0, decode_responses=True)


user = Blueprint('user', __name__)


@user.route('/register', methods=['POST'])
def register():
    """
    user registration
    """
    data = request.get_json()  # parse incoming JSON data from the request body
    errors = validate_data(data)
    if errors:
        return jsonify({"errors": errors}), 400

    if User.query.filter_by(email=data['email']).first():  # check for duplicates
        return jsonify({"error": "Email already exists"}), 400

    user = User(
        name=data["name"],
        email=data["email"],
        age=data["age"]
    )
    user.set_password(data["password"])
    db.session.add(user)
    db.session.commit()
    return jsonify({"message": "User successfully registered"}), 201

@user.route('/register-admin', methods=['POST'])
@jwt_required()
def register_admin():
    current_user = json.loads(get_jwt_identity())
    if current_user['role'] != 'admin':
        return jsonify({"error": "Access denied - admin only"}), 403

    data = request.get_json()
    errors = validate_data(data)
    if errors:
        return jsonify({"errors": errors}), 400

    if User.query.filter_by(email=data['email']).first():
        return jsonify({"error": "Email already registered"}), 400
    admin = User(
        name=data['name'],
        email=data['email'],
        age=data['age'],
        role=data['role']
    )
    admin.set_password(data['password'])
    db.session.add(admin)
    db.session.commit()

    return jsonify({"message": "Admin successfully created"}), 201

@user.route('/login', methods=["POST"])
def login():
    """
    user authentication
    """
    data = request.get_json()

    user = User.query.filter_by(email=data.get("email")).first()
    if not user or not user.check_password(data.get("password")):
        return jsonify({"error": "Invalid credentials"}), 401

    # create JWToken, authenticated requests
    access_token = create_access_token(identity=json.dumps({"id": user.id, "role": user.role}))
    return jsonify({"token": access_token}), 200

@user.route("/users/<int:user_id>", methods=["GET"])
@jwt_required()
def get_single_user(user_id):
    """
    retrieve a single user's details, with authent and auth checks
    """
    identity = json.loads(get_jwt_identity())  # get JWT payload, set during login
    if identity["id"] != user_id and identity["role"] != "admin":
        return jsonify({"error": "Access forbidden"}), 403

    cached = r.get(f"user:{user_id}")
    if cached:
        return jsonify(json.loads(cached)), 200

    user = User.query.get(user_id)
    if not user:
        return jsonify({"error": "User not found"}), 404
    user_data = user.to_dict()
    r.setex(f"user:{user_id}", 60, json.dumps(user_data))

    return jsonify(user_data), 200

@user.route("/users", methods=["GET"])
@jwt_required()
def list_users():
    identity = json.loads(get_jwt_identity())
    if identity["role"] != "admin":
        return jsonify({"error": "Access forbidden"}), 403

    cached = r.get("all_users")
    if cached:
        return jsonify(json.loads(cached)), 200
    users = User.query.all()
    data = [user.to_dict() for user in users]
    r.setex("all_users", 60, json.dumps(data))

    return jsonify(data), 200

@user.route("/users/<int:user_id>", methods=["PUT"])
@jwt_required()
def modify_user(user_id):
    identity = json.loads(get_jwt_identity())

    if identity["id"] != user_id and identity["role"] != "admin":
        return jsonify({"error": "Access forbidden"}), 403

    data = request.get_json()
    errors = validate_data(data)
    if errors:
        return jsonify({"errors": errors}), 400

    user = User.query.get(user_id)
    if not user:
        return jsonify({"error": "User not found"}), 404
    user.name = data["name"]
    user.age = data["age"]
    user.email = data["email"]
    db.session.commit()

    r.delete(f"user:{user_id}")
    return jsonify(user.to_dict())


@user.route("/users/<user_id>", methods=["DELETE"])
@jwt_required()
def delete_user(user_id):
    identity = json.loads(get_jwt_identity())

    if identity["id"] != int(user_id) and identity["role"] != "admin":
        return jsonify({"error": "Access forbidden"}), 403

    user = User.query.get(user_id)
    if not user:
        return jsonify({"error": "User not found"}), 404

    db.session.delete(user)
    db.session.commit()

    r.delete(f"user:{user_id}")

    return jsonify({"message": "User successfully deleted"}), 200