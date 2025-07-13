#!/usr/bin/python3
"""
SQLAlchemy repository for database operations
"""
from app.extensiones import db
from datetime import datetime

class SQLAlchemyRepository:
    """Repository using SQLAlchemy for database operations"""
    
    def __init__(self, model):
        """Initialize with model class"""
        self.model = model
    
    def add(self, obj):
        """Add object to database"""
        db.session.add(obj)
        db.session.commit()
        return obj
    
    def get(self, obj_id):
        """Get object by ID"""
        return self.model.query.get(obj_id)
    
    def get_all(self):
        """Get all objects"""
        return self.model.query.all()
    
    def update(self, obj_id, data):
        """Update object attributes"""
        obj = self.get(obj_id)
        if obj:
            for key, value in data.items():
                if key not in ['id', 'created_at']:
                    setattr(obj, key, value)
            obj.updated_at = datetime.utcnow()
            db.session.commit()
            return obj
        return None
    
    def delete(self, obj_id):
        """Delete object by ID"""
        obj = self.get(obj_id)
        if obj:
            db.session.delete(obj)
            db.session.commit()
            return True
        return False
        
    def get_by_attribute(self, attr_name, attr_value):
        """Get object by attribute value"""
        filter_kwargs = {attr_name: attr_value}
        return self.model.query.filter_by(**filter_kwargs).first()
