#!/usr/bin/python3
"""
Place module for the HBnB project
"""
from models.base_model import BaseModel


class Place(BaseModel):
    """
    Place class for representing places in the HBnB application
    """

    def __init__(self, *args, **kwargs):
        """
        Initialize a new Place instance

        Args:
            *args: Variable length argument list
            **kwargs: Arbitrary keyword arguments
        """
        super().__init__(*args, **kwargs)
        self.user_id = kwargs.get("user_id", "")
        self.name = kwargs.get("name", "")
        self.description = kwargs.get("description", "")
        self.number_rooms = kwargs.get("number_rooms", 0)
        self.number_bathrooms = kwargs.get("number_bathrooms", 0)
        self.max_guest = kwargs.get("max_guest", 0)
        self.price_by_night = kwargs.get("price_by_night", 0)
        self.latitude = kwargs.get("latitude", 0.0)
        self.longitude = kwargs.get("longitude", 0.0)
        self.amenities = []
        self.reviews = []

    def add_amenity(self, amenity):
        """
        Add an amenity to the place

        Args:
            amenity: The amenity to add
        """
        if amenity not in self.amenities:
            self.amenities.append(amenity)

    def add_review(self, review):
        """
        Add a review to the place

        Args:
            review: The review to add
        """
        if review not in self.reviews:
            self.reviews.append(review)
