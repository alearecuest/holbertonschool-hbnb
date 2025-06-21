#!/usr/bin/python3
"""
Initialize Flask application and register API
"""
from flask import Flask
from flask_restx import Api

def create_app():
    """Create and configure the Flask application"""
    app = Flask(__name__)
    
    api = Api(
        app,
        version='1.0',
        title='HBnB API',
        description='Holberton BnB API',
        prefix='/api/v1',
        doc='/api/v1'
    )
    
    from app.api.v1.amenities import api as amenities_ns
    
    api.add_namespace(amenities_ns, path='/amenities')
    
    return app
