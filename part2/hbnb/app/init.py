#!/usr/bin/python3
"""
Flask application initialization and API configuration.
"""
from flask import Flask
from flask_restx import Api

def create_app():
    """Creates and configures the Flask application"""
    app = Flask(__name__)
    

    app.config.from_object('config.DevelopmentConfig')
    

    api = Api(
        app, 
        version='1.0', 
        title='HBnB API',
        description='API for the HBnB application (AirBnB clone)',
        doc='/api/docs'
    )
    
    return app
