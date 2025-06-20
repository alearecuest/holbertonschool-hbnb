#!/usr/bin/python3
"""
Initialize Flask application and register API
"""
from flask import Flask
from flask_restx import Api

def create_app():
    """Create and configure the Flask application"""
    app = Flask(__name__)

    from app.api.v1 import blueprint as api_v1

    app.register_blueprint(api_v1)
    
    return app
