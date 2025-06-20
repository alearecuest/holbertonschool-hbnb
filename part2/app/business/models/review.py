#!/usr/bin/python3
"""
Review module for the HBnB project
"""
from app.business.models.base_model import BaseModel


class Review(BaseModel):
    """
    Review class for representing reviews in the HBnB application
    """

    def __init__(self, *args, **kwargs):
        """
        Initialize a new Review instance

        Args:
            *args: Variable length argument list
            **kwargs: Arbitrary keyword arguments
        """
        super().__init__(*args, **kwargs)
        self.text = kwargs.get("text", "")
        self.user_id = kwargs.get("user_id", "")
        self.place_id = kwargs.get("place_id", "")
        self.rating = kwargs.get("rating", 0)
        
        try:
            self.rating = int(self.rating)
        except (ValueError, TypeError):
            self.rating = 0
            
        self.validate()

    def validate(self):
        """
        Validate review attributes
        
        Raises:
            ValueError: If any attribute is invalid
        """
        if not self.text:
            raise ValueError("Review text cannot be empty")
        
        if not self.user_id:
            raise ValueError("Review must be associated with a user")
        
        if not self.place_id:
            raise ValueError("Review must be associated with a place")
        
        if not 0 <= self.rating <= 5:
            raise ValueError("Rating must be between 0 and 5")
