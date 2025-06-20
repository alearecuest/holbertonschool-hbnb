#!/usr/bin/python3
"""
Initialize Flask application and register API namespaces
"""
from flask import Flask
from flask_restx import Api

def create_app():
    """Create and configure the Flask application"""
    app = Flask(__name__)
    
    # Create API instance
    api = Api(
        app,
        version='1.0',
        title='HBnB API',
        description='Holberton BnB API',
        prefix='/api'
    )

    return app
