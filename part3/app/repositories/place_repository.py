#!/usr/bin/python3
"""
Place repository for database operations
"""
from app.repositories.sqlalchemy_repository import SQLAlchemyRepository
from app.models.place import Place

class PlaceRepository(SQLAlchemyRepository):
    """Repository for Place entity operations"""
    
    def __init__(self):
        """Initialize repository with Place model"""
        super().__init__(Place)
    
    def get_places_by_price_range(self, min_price, max_price):
        """
        Get places within a price range
        
        Args:
            min_price (float): Minimum price
            max_price (float): Maximum price
            
        Returns:
            list: List of places within the price range
        """
        return Place.query.filter(
            Place.price >= min_price,
            Place.price <= max_price
        ).all()
