#!/usr/bin/python3
"""
User module for the HBnB project
"""
from app.business.models.base_model import BaseModel


class User(BaseModel):
    """
    User class for representing users in the HBnB application
    """

    def __init__(self, *args, **kwargs):
        """
        Initialize a new User instance

        Args:
            *args: Variable length argument list
            **kwargs: Arbitrary keyword arguments
        """
        super().__init__(*args, **kwargs)
        self.email = kwargs.get("email", "")
        self.password = kwargs.get("password", "")
        self.first_name = kwargs.get("first_name", "")
        self.last_name = kwargs.get("last_name", "")
        self.places = []
        self.reviews = []

    def add_place(self, place):
        """
        Add a place to the user's places

        Args:
            place: The place to add
        """
        if place not in self.places:
            self.places.append(place)

    def add_review(self, review):
        """
        Add a review to the user's reviews

        Args:
            review: The review to add
        """
        if review not in self.reviews:
            self.reviews.append(review)
