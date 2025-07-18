#!/usr/bin/python3
"""
User API endpoints
"""
from flask import request
from flask_restx import Namespace, Resource, fields
from app.services import facade
from flask_jwt_extended import jwt_required, get_jwt_identity, get_jwt

api = Namespace('users', description='User operations')

user_model = api.model('User', {    
    'first_name': fields.String(required=True, description='First name of the user'),
    'last_name': fields.String(required=True, description='Last name of the user'),
    'email': fields.String(required=True, description='Email of the user'),
    'password': fields.String(required=True, description='password for user'),
    'is_admin': fields.Boolean(description='Admin status of the user')
})

user_response_model = api.model('UserResponse', {
    'id': fields.String(description='User ID'),
    'first_name': fields.String(description='First name of the user'),
    'last_name': fields.String(description='Last name of the user'),
    'email': fields.String(description='Email of the user'),
    'is_admin': fields.Boolean(description='Admin status of the user'),
    'created_at': fields.String(description='Creation timestamp'),
    'updated_at': fields.String(description='Update timestamp')
})

@api.route('/')
class UserList(Resource):
    @api.doc('create_user')
    @api.expect(user_model, validate=True)
    @api.response(201, 'User successfully created', user_response_model)
    @api.response(400, 'Email already registered')
    @api.response(400, 'Invalid input data')
    @api.marshal_with(user_response_model, code=201)
    @jwt_required()
    def post(self):
        """Register a new user""" #Modifique estas lineas
        claims = get_jwt()
        if not claims.get('is_admin', False):
            api.abort(403, "Admin privileges required to create users.")

        user_data = request.json

        existing_user = facade.get_user_by_email(user_data['email'])
        if existing_user:
            api.abort(400, "Email already registered")

        try:
            new_user = facade.create_user(user_data)
            return new_user.to_dict(), 201
        except ValueError as e:
            api.abort(400, str(e))

    @api.doc('list_users')
    @api.response(200, 'List of users retrieved successfully', [user_response_model])
    @api.marshal_list_with(user_response_model)
    def get(self):
        """Retrieve a list of all users"""
        users = facade.get_all_users()
        return [user.to_dict() for user in users]

@api.route('/<string:user_id>')
@api.param('user_id', 'The user identifier')
class UserResource(Resource):
    @api.doc('get_user')
    @api.response(200, 'User details retrieved successfully', user_response_model)
    @api.response(404, 'User not found')
    @api.marshal_with(user_response_model)
    @jwt_required()  # <-- PROTEGE GET
    def get(self, user_id):
        """Get user details by ID (admin or self only)"""
        claims = get_jwt()
        current_user = get_jwt_identity()
        # Solo admin o el propio usuario pueden ver los datos
        if not (claims.get('is_admin', False) or current_user == user_id):
            api.abort(403, "Unauthorized action")
        user = facade.get_user(user_id)
        if not user:
            api.abort(404, f"User with ID {user_id} not found")
        return user.to_dict()

    @api.doc('update_user')
    @api.expect(user_model)
    @api.response(200, 'User updated successfully', user_response_model)
    @api.response(404, 'User not found')
    @api.response(400, 'Invalid input data')
    @api.marshal_with(user_response_model)
    @api.response(401, 'Authentication required')
    @api.response(403, 'Unauthorized action')
    @jwt_required()  # <-- PROTEGE PUT
    def put(self, user_id):
        """Update a user's information (admin can update any user)"""
        claims = get_jwt()
        current_user = get_jwt_identity()
        user = facade.get_user(user_id)
        if not user:
            api.abort(404, f"User with ID {user_id} not found")
        data = request.json

        # Admin puede modificar cualquier campo, incluido email/password
        if claims.get('is_admin', False):
            if 'email' in data and data['email'] != user.email:
                existing_user = facade.get_user_by_email(data['email'])
                if existing_user and existing_user.id != user_id:
                    api.abort(400, "Email already registered")
            try:
                updated_user = facade.update_user(user_id, data)
                if not updated_user:
                    api.abort(404, f"Failed to update user with ID {user_id}")
                return updated_user.to_dict()
            except ValueError as e:
                api.abort(400, str(e))

        # Usuario normal: solo puede modificar a sí mismo, sin email ni password
        if current_user != user_id:
            api.abort(403, "Unauthorized action")
        if 'email' in data or 'password' in data:
            api.abort(400, "You cannot modify email or password through this endpoint")
        try:
            updated_user = facade.update_user(user_id, data)
            if not updated_user:
                api.abort(404, f"Failed to update user with ID {user_id}")
            return updated_user.to_dict()
        except ValueError as e:
            api.abort(400, str(e))
