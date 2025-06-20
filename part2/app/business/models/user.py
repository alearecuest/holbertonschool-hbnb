#!/usr/bin/python3
"""
User module for the HBnB project
"""
from app.business.models.base_model import BaseModel
import re


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
        
        self.validate()

    def validate(self):
        """
        Validate user attributes
        
        Raises:
            ValueError: If any attribute is invalid
        """
        if self.email and not self._is_valid_email(self.email):
            raise ValueError("Invalid email format")
        
        if self.password and len(self.password) < 8:
            raise ValueError("Password must be at least 8 characters long")

    def _is_valid_email(self, email):
        """
        Check if the email has a valid format
        
        Args:
            email: The email to validate
            
        Returns:
            True if the email is valid, False otherwise
        """
        pattern = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
        return re.match(pattern, email) is not None

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
    
    def get_places(self):
        """
        Get all places owned by the user
        
        Returns:
            List of places
        """
        return self.places
    
    def get_reviews(self):
        """
        Get all reviews written by the user
        
        Returns:
            List of reviews
        """
        return self.reviews
        
    def to_dict(self):
        """
        Return a dictionary representation of the User instance
        """
        user_dict = super().to_dict()
        
        if "password" in user_dict:
            user_dict["password"] = "********"
            
        return user_dict
