#!/usr/bin/python3
"""
Initialize Flask application and register API
"""
from flask import Flask
from flask_restx import Api

api = Api(
    version='1.0',
    title='HBnB API',
    description='Holberton BnB API',
    doc='/',
    prefix='/api/v1'
)

def create_app():
    """Create and configure the Flask application"""
    app = Flask(__name__)

    api.init_app(app)

    from app.api.v1.amenities import api as amenities_ns

    api.add_namespace(amenities_ns, path='/amenities')

    return app
