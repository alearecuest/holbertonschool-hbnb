#!/usr/bin/python3
"""
User API controller for the HBnB project
"""
from flask import request
from flask_restx import Resource

from app.presentation.dto.user_dto import UserDTO
from app.business.facades.user_facade import UserFacade
from app.persistence.repositories.memory_repository import MemoryRepository


api = UserDTO.api
_user_create = UserDTO.user_create
_user_update = UserDTO.user_update
_user = UserDTO.user

# Initialize the repository and facade
user_repository = MemoryRepository()
user_facade = UserFacade(user_repository)


@api.route('/')
class UserList(Resource):
    """User list resource"""

    @api.doc('list_users')
    @api.marshal_list_with(_user)
    def get(self):
        """List all users"""
        users = user_facade.get_all_users()
        return users

    @api.doc('create_user')
    @api.expect(_user_create)
    @api.marshal_with(_user, code=201)
    @api.response(400, 'Validation Error')
    def post(self):
        """Create a new user"""
        data = request.json
        try:
            user = user_facade.create(data)
            return user, 201
        except ValueError as e:
            api.abort(400, str(e))


@api.route('/<string:user_id>')
@api.param('user_id', 'The user identifier')
@api.response(404, 'User not found')
class UserResource(Resource):
    """User resource"""

    @api.doc('get_user')
    @api.marshal_with(_user)
    def get(self, user_id):
        """Get a user by ID"""
        user = user_facade.get_by_id(user_id)
        if not user:
            api.abort(404, f"User with ID {user_id} not found")
        return user

    @api.doc('update_user')
    @api.expect(_user_update)
    @api.marshal_with(_user)
    @api.response(400, 'Validation Error')
    def put(self, user_id):
        """Update a user"""
        data = request.json
        try:
            user = user_facade.update(user_id, data)
            if not user:
                api.abort(404, f"User with ID {user_id} not found")
            return user
        except ValueError as e:
            api.abort(400, str(e))
