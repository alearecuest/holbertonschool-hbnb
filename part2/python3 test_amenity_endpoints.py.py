#!/usr/bin/python3
"""
Simple Flask application for amenity management
"""
from flask import Flask, jsonify, request
import uuid
from datetime import datetime

app = Flask(__name__)

class Amenity:
    def __init__(self, name, description=None, id=None, created_at=None, updated_at=None):
        self.id = id or str(uuid.uuid4())
        self.name = name
        self.description = description
        self.created_at = created_at or datetime.utcnow()
        self.updated_at = updated_at or self.created_at

    def update(self, data):
        for key, value in data.items():
            if key not in ['id', 'created_at']:
                setattr(self, key, value)
        self.updated_at = datetime.utcnow()

    def validate(self):
        if not self.name or not isinstance(self.name, str) or len(self.name) == 0:
            raise ValueError("Amenity name is required and must be a non-empty string")
        
        if self.description is not None and not isinstance(self.description, str):
            raise ValueError("Amenity description must be a string")

    def to_dict(self):
        return {
            'id': self.id,
            'name': self.name,
            'description': self.description,
            'created_at': self.created_at.isoformat(),
            'updated_at': self.updated_at.isoformat()
        }

# Repositorio en memoria
class InMemoryRepository:
    def __init__(self):
        self._storage = {}

    def add(self, obj):
        self._storage[obj.id] = obj
        return obj

    def get(self, obj_id):
        return self._storage.get(obj_id)

    def get_all(self):
        return list(self._storage.values())

    def update(self, obj):
        self._storage[obj.id] = obj
        return obj

    def delete(self, obj_id):
        if obj_id in self._storage:
            del self._storage[obj_id]
            return True
        return False

# Instancia del repositorio
amenity_repo = InMemoryRepository()

@app.route('/api/v1/amenities/', methods=['GET'])
def get_amenities():
    """Get all amenities"""
    amenities = amenity_repo.get_all()
    return jsonify([amenity.to_dict() for amenity in amenities])

@app.route('/api/v1/amenities/', methods=['POST'])
def create_amenity():
    """Create a new amenity"""
    data = request.json
    try:
        amenity = Amenity(**data)
        amenity.validate()
        amenity_repo.add(amenity)
        return jsonify(amenity.to_dict()), 201
    except ValueError as e:
        return jsonify({"error": str(e)}), 400

@app.route('/api/v1/amenities/<string:amenity_id>', methods=['GET'])
def get_amenity(amenity_id):
    """Get an amenity by ID"""
    amenity = amenity_repo.get(amenity_id)
    if not amenity:
        return jsonify({"error": f"Amenity with ID {amenity_id} not found"}), 404
    return jsonify(amenity.to_dict())

@app.route('/api/v1/amenities/<string:amenity_id>', methods=['PUT'])
def update_amenity(amenity_id):
    """Update an amenity"""
    data = request.json
    amenity = amenity_repo.get(amenity_id)
    if not amenity:
        return jsonify({"error": f"Amenity with ID {amenity_id} not found"}), 404
    
    try:
        amenity.update(data)
        amenity.validate()
        return jsonify(amenity.to_dict())
    except ValueError as e:
        return jsonify({"error": str(e)}), 400

@app.route('/api/v1/', methods=['GET'])
def api_root():
    """API root endpoint"""
    return jsonify({
        "message": "Welcome to the HBnB API",
        "version": "1.0",
        "endpoints": {
            "GET /api/v1/amenities/": "Get all amenities",
            "POST /api/v1/amenities/": "Create a new amenity",
            "GET /api/v1/amenities/<id>": "Get an amenity by ID",
            "PUT /api/v1/amenities/<id>": "Update an amenity"
        }
    })

@app.route('/', methods=['GET'])
def index():
    """Redirect to API documentation"""
    return """
    <html>
        <head>
            <title>HBnB API</title>
        </head>
        <body>
            <h1>HBnB API</h1>
            <p>Welcome to the HBnB API. Available endpoints:</p>
            <ul>
                <li><a href="/api/v1/">API Documentation</a></li>
                <li><a href="/api/v1/amenities/">GET /api/v1/amenities/</a> - List all amenities</li>
            </ul>
        </body>
    </html>
    """

if __name__ == '__main__':
    print("\n=== HBnB Amenity API ===")
    print("Author: alearecuest")
    print("Last updated: 2025-06-20 21:56:48")
    print("\nStarting server on http://localhost:5000/")
    print("API endpoints:")
    print("  GET /api/v1/ - API documentation")
    print("  GET /api/v1/amenities/ - Get all amenities")
    print("  POST /api/v1/amenities/ - Create a new amenity")
    print("  GET /api/v1/amenities/<id> - Get an amenity by ID")
    print("  PUT /api/v1/amenities/<id> - Update an amenity")
    app.run(debug=True, host='0.0.0.0', port=5000)
