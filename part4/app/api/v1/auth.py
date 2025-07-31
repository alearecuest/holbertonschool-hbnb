#!/usr/bin/python3
"""
Authentication API endpoints
"""
from flask import request, jsonify
from flask_restx import Namespace, Resource, fields
from flask_jwt_extended import (
    create_access_token,
    create_refresh_token,
    jwt_required,
    get_jwt_identity
)
from app.services.facade import get_user_by_email
from app.extensions import bcrypt

api = Namespace('auth', description='Authentication operations')

login_model = api.model('Login', {
    'email':    fields.String(required=True, description='User email'),
    'password': fields.String(required=True, description='User password')
})

register_model = api.model('Register', {
    'email':      fields.String(required=True, description='User email'),
    'password':   fields.String(required=True, description='User password'),
    'first_name': fields.String(required=True, description='User first name'),
    'last_name':  fields.String(required=True, description='User last name'),
    'is_admin':   fields.Boolean(description='Is admin user', required=False)
})

@api.route('/register')
class Register(Resource):
    @api.expect(register_model, validate=True)
    @api.response(201, 'User registered successfully')
    @api.response(409, 'Email already exists')
    @api.response(400, 'Invalid data')
    def post(self):
        user_data = request.get_json() or {}
        user_data['is_admin'] = user_data.get('is_admin', False)

        if get_user_by_email(user_data.get('email')):
            return {'msg': 'Email already registered'}, 409

        try:
            from app.services.facade import create_user
            new_user = create_user(user_data)
            result = new_user.to_dict()
            return result, 201
        except Exception as e:
            return {'msg': str(e)}, 400

@api.route('/login')
class Login(Resource):
    @api.expect(login_model, validate=True)
    @api.response(200, 'Login successful')
    @api.response(400, 'Validation error')
    @api.response(401, 'Invalid credentials')
    def post(self):
        creds = request.get_json() or {}
        email = creds.get('email')
        password = creds.get('password')

        if not email or not password:
            return {'msg': 'Email and password are required'}, 400

        user = get_user_by_email(email)
        if not user or not bcrypt.check_password_hash(user._password, password):
            return {'msg': 'Invalid email or password'}, 401

        access_token = create_access_token(
            identity=str(user.id),
            additional_claims={'is_admin': user.is_admin}
        )
        refresh_token = create_refresh_token(identity=str(user.id))

        return {'access_token': access_token, 'refresh_token': refresh_token}, 200

@api.route('/refresh')
class TokenRefresh(Resource):
    @api.response(200, 'Token refreshed successfully')
    @api.response(401, 'Invalid or missing refresh token')
    @jwt_required(refresh=True)
    def post(self):
        current_user = get_jwt_identity()
        new_token = create_access_token(identity=current_user)
        return {'access_token': new_token}, 200