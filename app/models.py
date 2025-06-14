#!/usr/bin/activate
from app import db
from datetime import datetime
from werkzeug.security import generate_password_hash, check_password_hash


class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(120), nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    age = db.Column(db.Integer, nullable=False)
    password_hash = db.Column(db.String(200), nullable=False)
    role = db.Column(db.String(10), default='user')
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

    def set_password(self, password):
        """
        hash plain text password
        """
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        """
        check provided password matches hash, returns True or False
        """
        return check_password_hash(self.password_hash, password)

    def to_dict(self):
        """
        converts user object to dictionary, JSON response
        """
        return {
            "id": self.id,
            "name": self.name,
            "email": self.email,
            "age": self.age,
            "role": self.role,
            "created_at": self.created_at.isoformat()  # datetime JSON-serializable
        }