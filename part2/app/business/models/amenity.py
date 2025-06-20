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

    def add_place(self, place):
        """
        Add a place to the amenity's places

        Args:
            place: The place to add
        """
        if place not in self.places:
            self.places.append(place)
