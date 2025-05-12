#!/usr/bin/python3
from uuid import uuid4


users = {}


def create_user(name, email, age):
    """
    create a new user and add them to the in-memory database
    """
    user_id = str(uuid4())
    users[user_id] = {"id": user_id, "name": name, "email": email, "age": age}
    return users[user_id]


def get_user(user_id):
    """
    get a user by their id
    """
    return users.get(user_id)


def get_all_users():
    """
    retrieve all users from the in-memory database
    """
    return list(users.values())


def update_user(user_id, name=None, email=None, age=None):
    """
    update an existing user's info
    """
    if user_id not in users:
        return None
    if name:
        users[user_id]["name"] = name
    if email:
        users[user_id]["email"] = email
    if age:
        users[user_id]["age"] = age
    return users[user_id]


def delete_user(user_id):
    """
    deletes a user from the system
    """
    if user_id in users:
        return users.pop(user_id)
    return None
