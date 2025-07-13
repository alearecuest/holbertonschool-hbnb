#!/usr/bin/python3
"""
Amenity repository for database operations
"""
from app.repositories.sqlalchemy_repository import SQLAlchemyRepository
from app.models.amenity import Amenity

class AmenityRepository(SQLAlchemyRepository):
    """Repository for Amenity entity operations"""
    
    def __init__(self):
        """Initialize repository with Amenity model"""
        super().__init__(Amenity)
    
    def get_amenity_by_name(self, name):
        """
        Get amenity by name
        
        Args:
            name (str): Amenity name
            
        Returns:
            Amenity: Amenity object if found, None otherwise
        """
        return Amenity.query.filter_by(name=name).first()
