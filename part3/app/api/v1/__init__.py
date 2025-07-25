#!/usr/bin/python3
"""
API v1 package for the HBnB project
"""

from flask import Blueprint
from flask_restx import Api

from app.api.v1.auth import api as auth_ns
from app.api.v1.places import api as places_ns
from app.api.v1.amenities import api as amenities_ns

api_v1 = Blueprint('api_v1', __name__, url_prefix='/api/v1')

api = Api(
    api_v1,
    version='1.0',
    title='HBNB API',
    description='API for HBNB application'
)

api.add_namespace(auth_ns)
api.add_namespace(places_ns)
api.add_namespace(amenities_ns)
