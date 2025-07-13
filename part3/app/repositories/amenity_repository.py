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
    
    def name_exists(self, name):
        """
        Check if amenity name exists
        
        Args:
            name (str): Amenity name
            
        Returns:
            bool: True if exists, False otherwise
        """
        return Amenity.query.filter_by(name=name).count() > 0
        
    def get_amenity_places(self, amenity_id):
        """
        Get places with this amenity
        
        Args:
            amenity_id (str): Amenity ID
            
        Returns:
            list: List of places with this amenity
        """
        amenity = self.get(amenity_id)
        if amenity:
            return amenity.places
        return []
