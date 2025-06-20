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
