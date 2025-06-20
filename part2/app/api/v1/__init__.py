#!/usr/bin/python3
"""
API v1 package for the HBnB project
"""
from flask import Blueprint
from flask_restx import Api

blueprint = Blueprint('api_v1', __name__, url_prefix='/api/v1')

api = Api(
    blueprint,
    version='1.0',
    title='HBnB API',
    description='Holberton BnB API',
    doc='/',
    validate=True
)

from app.api.v1.amenities import api as amenities_ns
api.add_namespace(amenities_ns, path='/amenities')
