#!/usr/bin/python3
"""
Initialize Flask application and register API namespaces
"""
from flask import Flask
from flask_restx import Api

from app.presentation.dto.user_dto import UserDTO
from app.presentation.api.user_controller import api as user_ns


def create_app():
    """Create and configure the Flask application"""
    app = Flask(__name__)
    
    api = Api(
        app,
        version='1.0',
        title='HBnB API',
        description='Holberton BnB API',
        prefix='/api/v1'
    )
    
    api.add_namespace(user_ns, path='/users')
    
    return app