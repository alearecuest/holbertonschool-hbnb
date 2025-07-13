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
    
    def get_places_by_owner(self, owner_id):
        """
        Get places owned by a user
        
        Args:
            owner_id (str): User ID
            
        Returns:
            list: List of places owned by the user
        """
        return Place.query.filter_by(owner_id=owner_id).all()
    
    def add_amenity_to_place(self, place_id, amenity):
        """
        Add an amenity to a place
        
        Args:
            place_id (str): Place ID
            amenity: Amenity to add
            
        Returns:
            Place: Updated place if successful, None otherwise
        """
        place = self.get(place_id)
        if place and amenity not in place.amenities:
            place.amenities.append(amenity)
            self.session.commit()
            return place
        return None
