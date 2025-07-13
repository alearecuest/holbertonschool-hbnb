#!/usr/bin/python3
"""
Script para inicializar la base de datos
"""
from app import create_app
from app.extensiones import db

# Crear la aplicación
app = create_app()

# Usar el contexto de la aplicación
with app.app_context():
    # Crear todas las tablas
    db.create_all()
    print("¡Base de datos inicializada correctamente!")
