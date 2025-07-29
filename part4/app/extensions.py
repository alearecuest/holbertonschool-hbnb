#!/usr/bin/python3
"""
Extensions for the HBnB application
"""
from flask import jsonify
from flask_jwt_extended import JWTManager
from flask_bcrypt import Bcrypt
from flask_sqlalchemy import SQLAlchemy

bcrypt = Bcrypt()
db     = SQLAlchemy()
jwt    = JWTManager()

def init_app(app):
    bcrypt.init_app(app)
    db.init_app(app)

    from app.models.user import User
    from app.models.review import Review
    from app.models.place import Place

    jwt.init_app(app)

    @jwt.unauthorized_loader
    def missing_header(err_msg):
        return jsonify(msg="Missing Authorization Header"), 401

    @jwt.expired_token_loader
    def expired_token(jwt_header, jwt_payload):
        return jsonify(msg="Token has expired"), 401

    @jwt.invalid_token_loader
    def invalid_token(err_msg):
        return jsonify(
            msg="Bad Authorization header. Expected 'Authorization: Bearer <JWT>'"
        ), 422
