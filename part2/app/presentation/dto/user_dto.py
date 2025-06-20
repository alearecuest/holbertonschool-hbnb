#!/usr/bin/python3
"""
Data Transfer Objects for User API
"""
from flask_restx import Namespace, fields


class UserDTO:
    """User Data Transfer Object"""

    api = Namespace('users', description='User operations')
    
    user_create = api.model('UserCreate', {
        'email': fields.String(required=True, description='User email'),
        'password': fields.String(required=True, description='User password'),
        'first_name': fields.String(description='User first name'),
        'last_name': fields.String(description='User last name')
    })
    
    user_update = api.model('UserUpdate', {
        'email': fields.String(description='User email'),
        'password': fields.String(description='User password'),
        'first_name': fields.String(description='User first name'),
        'last_name': fields.String(description='User last name')
    })
    
    user = api.model('User', {
        'id': fields.String(description='User ID'),
        'email': fields.String(description='User email'),
        'first_name': fields.String(description='User first name'),
        'last_name': fields.String(description='User last name'),
        'created_at': fields.DateTime(description='Creation timestamp'),
        'updated_at': fields.DateTime(description='Update timestamp')
    })
