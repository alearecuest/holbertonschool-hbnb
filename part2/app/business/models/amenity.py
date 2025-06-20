#!/usr/bin/python3
"""
Amenity module for the HBnB project
"""
from app.business.models.base_model import BaseModel


class Amenity(BaseModel):
    """
    Amenity class for representing amenities in the HBnB application
    """

    def __init__(self, *args, **kwargs):
        """
        Initialize a new Amenity instance

        Args:
            *args: Variable length argument list
            **kwargs: Arbitrary keyword arguments
        """
        super().__init__(*args, **kwargs)
        self.name = kwargs.get("name", "")
        self.description = kwargs.get("description", "")
        self.places = []
        
        self.validate()

    def validate(self):
        """
        Validate amenity attributes
        
        Raises:
            ValueError: If any attribute is invalid
        """
        if not self.name:
            raise ValueError("Amenity name cannot be empty")

    def add_place(self, place):
        """
        Add a place to the amenity's places

        Args:
            place: The place to add
        """
        if place not in self.places:
            self.places.append(place)
            if hasattr(place, 'add_amenity'):
                place.add_amenity(self)

    def remove_place(self, place):
        """
        Remove a place from the amenity's places

        Args:
            place: The place to remove
            
        Returns:
            True if the place was removed, False otherwise
        """
        if place in self.places:
            self.places.remove(place)
            if hasattr(place, 'remove_amenity'):
                place.remove_amenity(self)
            return True
        return False
    
    def get_places(self):
        """
        Get all places that have this amenity
        
        Returns:
            List of places
        """
        return self.places