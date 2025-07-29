#!/usr/bin/python3
"""
Initialize Flask application, register API and serve HTML templates.
"""
from flask import Flask, redirect, jsonify, render_template
from flask_restx import Api
from flask_cors import CORS

from app.extensions import init_app
from app.api.v1.auth      import api as auth_ns
from app.api.v1.users     import api as users_ns
from app.api.v1.amenities import api as amenities_ns
from app.api.v1.places    import api as places_ns
from app.api.v1.reviews   import api as reviews_ns

authorizations = {
    'Bearer Auth': {
        'type': 'apiKey',
        'in': 'header',
        'name': 'Authorization',
        'description': 'Agregar token con formato: Bearer {token}'
    }
}

def create_app(config_class="config.DevelopmentConfig"):
    app = Flask(__name__)
    app.url_map.strict_slashes = False
    app.config.from_object(config_class)

    CORS(app, resources={r"/api/*": {"origins": "*"}})

    init_app(app)

    api = Api(
        app,
        version='1.0',
        title='HBnB API',
        description='Holberton BnB API',
        prefix='/api/v1',
        doc='/api/v1',
        authorizations=authorizations,
        security='Bearer Auth'
    )
    api.add_namespace(auth_ns,      path="/auth")
    api.add_namespace(users_ns,     path="/users")
    api.add_namespace(amenities_ns, path="/amenities")
    api.add_namespace(places_ns,    path="/places")
    api.add_namespace(reviews_ns,   path="/reviews")

    @app.route('/info')
    def info():
        return jsonify({
            "name": "HBnB API",
            "version": "1.0",
            "author": "HolbertonG4MVD",
            "last_updated": "2025-07-24 14:29:05",
            "documentation": "/api/v1",
            "endpoints": {
                "users": "/api/v1/users",
                "amenities": "/api/v1/amenities",
                "places": "/api/v1/places",
                "reviews": "/api/v1/reviews",
                "auth": "/api/v1/auth"
            }
        })

    @app.route('/', methods=['GET'])
    def render_index():
        return render_template('index.html')

    @app.route('/login', methods=['GET'])
    def render_login():
        return render_template('login.html')

    @app.route('/place', methods=['GET'])
    def render_place():
        return render_template('place.html')

    @app.route('/add_review', methods=['GET'])
    def render_add_review():
        return render_template('add_review.html')

    return app
