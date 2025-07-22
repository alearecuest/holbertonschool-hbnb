#!/usr/bin/python3
"""
Tablas de asociación para relaciones many-to-many
"""
from app.extensions import db

# Tabla de asociación para la relación many-to-many entre Place y Amenity
place_amenity = db.Table('place_amenity',
    db.Column('place_id', db.String(36), db.ForeignKey('places.id'), primary_key=True),
    db.Column('amenity_id', db.String(36), db.ForeignKey('amenities.id'), primary_key=True)
)
