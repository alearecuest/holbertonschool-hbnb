#!/usr/bin/python3
"""
Facade service for the HBnB project
"""
from app.persistence.repository import InMemoryRepository
from app.models.amenity import Amenity


class HBnBFacade:
    """
    HBnB facade class that provides a simplified interface to business logic operations
    """

    def __init__(self):
        """
        Initialize a new HBnBFacade instance
        """
        self.user_repo = InMemoryRepository()
        self.place_repo = InMemoryRepository()
        self.review_repo = InMemoryRepository()
        self.amenity_repo = InMemoryRepository()

    def create_user(self, user_data):
        """
        Create a new user (placeholder)
        """
        pass

    def get_user(self, user_id):
        """
        Get a user by ID (placeholder)
        """
        pass

    def get_all_users(self):
        """
        Get all users (placeholder)
        """
        pass

    def update_user(self, user_id, user_data):
        """
        Update a user (placeholder)
        """
        pass

    def create_amenity(self, amenity_data):
        """
        Create a new amenity

        Args:
            amenity_data: Dictionary of amenity attributes

        Returns:
            The created amenity
        """
        amenity = Amenity(**amenity_data)
        amenity.validate()
        self.amenity_repo.add(amenity)
        return amenity

    def get_amenity(self, amenity_id):
        """
        Get an amenity by ID

        Args:
            amenity_id: The ID of the amenity to get

        Returns:
            The amenity if found, None otherwise
        """
        return self.amenity_repo.get(amenity_id)

    def get_all_amenities(self):
        """
        Get all amenities

        Returns:
            A list of all amenities
        """
        return self.amenity_repo.get_all()

    def update_amenity(self, amenity_id, amenity_data):
        """
        Update an amenity

        Args:
            amenity_id: The ID of the amenity to update
            amenity_data: Dictionary of attributes to update

        Returns:
            The updated amenity if successful, None otherwise
        """
        amenity = self.amenity_repo.get(amenity_id)
        if not amenity:
            return None

        amenity.update(amenity_data)

        try:
            amenity.validate()
        except ValueError as e:
            raise ValueError(f"Validation error: {str(e)}")
        
        return amenity
