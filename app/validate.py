#!/usr/bin/python3


def validate_data(data):
    """
    validates useer data and returns a list of error messages
    """
    errors = []

    if not data.get("name"):
        errors.append("Name is required.")
    if not data.get("email"):
        errors.append("Email is required.")
    elif "@" not in data["email"] or "." not in data["email"]:
        errors.append("Invalid email format.")
    if not isinstance(data.get("age"), int) or data["age"] <= 0:
        errors.append("Age must be a positive integer.")
    return errors
