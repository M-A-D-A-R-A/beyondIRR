from datetime import datetime
from flask import current_app, jsonify
import json
from passlib.hash import sha256_crypt

from extension import db

class User(db.Model):
    """
    This model holds information about a user registered
    """
    __tablename__ = "user"

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(80), nullable=False)
    username = db.Column(db.String(80), unique=True, nullable=False,)
    password = db.Column(db.String(128))
    email = db.Column(db.String(100), nullable=False, unique=True)

    def __init__(self, name, username, email, password=None):
        """
        Initializes the user instance
        """
        self.name = name
        self.username = username
        self.email = email
        if password:
            self.password = User.generate_password_hash(password)

    def __repr__(self):
        """
        Returns the object reprensentation of user
        """
        return "<User %r>" % self.name

    @staticmethod
    def generate_password_hash(password):
        """
        Returns hash of password
        """
        return sha256_crypt.hash(password)

    def verify_password(self, password):
        """
        Verify the password
        """
        return sha256_crypt.verify(self.password, password)
       
