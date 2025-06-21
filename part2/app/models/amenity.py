#!/usr/bin/python3
"""
Amenity model for the HBnB project

Author: alearecuest
Last updated: 2025-06-21 02:52:13
"""
from app.models.base_model import BaseModel


class Amenity(BaseModel):
    """Amenity class for representing amenities in the HBnB application"""

    def __init__(self, name, description=None, **kwargs):
        """
        Initialize a new Amenity instance

        Args:
            name (str): Name of the amenity
            description (str, optional): Description of the amenity
            **kwargs: Additional attributes to set
        """
        super().__init__(**kwargs)
        self.name = name
        self.description = description
        self.validate()

    def validate(self):
        """
        Validate amenity attributes

        Raises:
            ValueError: If any validation fails
        """
        if not self.name or not isinstance(self.name, str):
            raise ValueError("Amenity name is required and must be a string")
        if len(self.name) > 50:
            raise ValueError("Amenity name must be at most 50 characters")
            
        if self.description is not None and not isinstance(self.description, str):
            raise ValueError("Description must be a string")
