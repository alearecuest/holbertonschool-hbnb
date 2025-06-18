#!/usr/bin/python3
"""
Flask application initialization and API configuration.
Date: 2025-06-18 03:38:24
Author: alearecuest
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
