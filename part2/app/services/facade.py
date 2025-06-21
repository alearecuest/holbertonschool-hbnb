#!/usr/bin/python3
"""
Facade service for the HBnB application
"""
from app.repositories.in_memory_repository import InMemoryRepository
from app.models.user import User
from app.models.amenity import Amenity


class HBnBFacade:
    """Facade for handling business logic operations"""

    def __init__(self):
        """Initialize repositories for different entities"""
        self.user_repo = InMemoryRepository()
        self.amenity_repo = InMemoryRepository()

    def create_user(self, user_data):
        """
        Create a new user

        Args:
            user_data (dict): Data for the new user

        Returns:
            User: The created user
        """
        user = User(**user_data)
        return self.user_repo.add(user)

    def get_user(self, user_id):
        """
        Get a user by ID

        Args:
            user_id (str): ID of the user

        Returns:
            User: The found user or None
        """
        return self.user_repo.get(user_id)

    def get_all_users(self):
        """
        Get all users

        Returns:
            list: List of all users
        """
        return self.user_repo.get_all()

    def update_user(self, user_id, data):
        """
        Update a user

        Args:
            user_id (str): ID of the user
            data (dict): New data for the user

        Returns:
            User: The updated user or None
        """
        return self.user_repo.update(user_id, data)

    def get_user_by_email(self, email):
        """
        Get a user by email

        Args:
            email (str): Email of the user

        Returns:
            User: The found user or None
        """
        return self.user_repo.get_by_attribute('email', email)

    def create_amenity(self, data):
        """
        Create a new amenity

        Args:
            data (dict): Data for the new amenity

        Returns:
            Amenity: The created amenity
        """
        amenity = Amenity(**data)
        return self.amenity_repo.add(amenity)

    def get_amenity(self, amenity_id):
        """
        Get an amenity by ID

        Args:
            amenity_id (str): ID of the amenity

        Returns:
            Amenity: The found amenity or None
        """
        return self.amenity_repo.get(amenity_id)

    def get_all_amenities(self):
        """
        Get all amenities

        Returns:
            list: List of all amenities
        """
        return self.amenity_repo.get_all()

    def update_amenity(self, amenity_id, data):
        """
        Update an amenity

        Args:
            amenity_id (str): ID of the amenity
            data (dict): New data for the amenity

        Returns:
            Amenity: The updated amenity or None
        """
        return self.amenity_repo.update(amenity_id, data)


_facade = HBnBFacade()

def create_user(user_data):
    return _facade.create_user(user_data)

def get_user(user_id):
    return _facade.get_user(user_id)

def get_all_users():
    return _facade.get_all_users()

def update_user(user_id, data):
    return _facade.update_user(user_id, data)

def get_user_by_email(email):
    return _facade.get_user_by_email(email)

def create_amenity(data):
    return _facade.create_amenity(data)

def get_amenity(amenity_id):
    return _facade.get_amenity(amenity_id)

def get_all_amenities():
    return _facade.get_all_amenities()

def update_amenity(amenity_id, data):
    return _facade.update_amenity(amenity_id, data)
