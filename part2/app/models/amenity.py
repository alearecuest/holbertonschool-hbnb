#!/usr/bin/python3
"""
Amenity model for the HBnB project
"""
import uuid
from datetime import datetime


class Amenity:
    """
    Amenity class for representing amenities in the HBnB application
    """

    def __init__(self, name, description=None, id=None, created_at=None, updated_at=None):
        """
        Initialize a new Amenity instance

        Args:
            name (str): The name of the amenity
            description (str, optional): The description of the amenity
            id (str, optional): The ID of the amenity. Defaults to a new UUID.
            created_at (datetime, optional): The creation timestamp. Defaults to now.
            updated_at (datetime, optional): The update timestamp. Defaults to now.
        """
        self.id = id or str(uuid.uuid4())
        self.name = name
        self.description = description
        self.created_at = created_at or datetime.utcnow()
        self.updated_at = updated_at or self.created_at

    def update(self, data):
        """
        Update the amenity with new data

        Args:
            data (dict): The data to update the amenity with
        """
        for key, value in data.items():
            if key not in ['id', 'created_at']:
                setattr(self, key, value)
        self.updated_at = datetime.utcnow()

    def validate(self):
        """
        Validate the amenity

        Raises:
            ValueError: If any required fields are missing or invalid
        """
        if not self.name or not isinstance(self.name, str) or len(self.name) == 0:
            raise ValueError("Amenity name is required and must be a non-empty string")
        
        if self.description is not None and not isinstance(self.description, str):
            raise ValueError("Amenity description must be a string")

    def to_dict(self):
        """
        Convert the amenity to a dictionary

        Returns:
            dict: A dictionary representation of the amenity
        """
        return {
            'id': self.id,
            'name': self.name,
            'description': self.description,
            'created_at': self.created_at.isoformat(),
            'updated_at': self.updated_at.isoformat()
        }

    def __str__(self):
        """
        Get a string representation of the amenity

        Returns:
            str: A string representation of the amenity
        """
        return "[Amenity] ({}) {}".format(self.id, self.__dict__)