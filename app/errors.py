#!/usr/bin/python3
from flask import jsonify


def handle_bad_request(error):
    return jsonify({"error": str(error)}), 400


def handle_not_found(error):
    return jsonify({"error": "User not found"})
