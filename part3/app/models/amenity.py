#!/usr/bin/python3
"""
Amenity model for the HBnB project
"""
from app.models.base_model import BaseModel
from app.extensiones import db
from datetime import datetime

class Amenity(BaseModel):
    """Amenity class for storing amenity information"""
    __tablename__ = 'amenities'
    
    name = db.Column(db.String(50), nullable=False, unique=True)
    description = db.Column(db.Text, nullable=True)
    
    def __init__(self, **kwargs):
        """Initialize a new Amenity instance"""
        super().__init__(**kwargs)
        self.name = kwargs.get('name', '')
        self.description = kwargs.get('description', '')
        self.validate()

    def validate(self):
        """
        Validate amenity attributes

        Raises:
            ValueError: If validation fails
        """
        if not self.name or not isinstance(self.name, str):
            raise ValueError("Amenity must have a valid name")
        
        if self.description and not isinstance(self.description, str):
            raise ValueError("Description must be a string")
        
    def update(self, data):
        """
        Update amenity attributes
        
        Args:
            data (dict): New data for the amenity
            
        Returns:
            self: The updated amenity instance
        
        Raises:
            ValueError: If the updated data is invalid
        """
        if 'name' in data:
            self.name = data['name']
        if 'description' in data:
            self.description = data['description']
        
        self.updated_at = datetime.utcnow()
        
        self.validate()
        return self
