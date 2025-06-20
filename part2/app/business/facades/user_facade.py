#!/usr/bin/python3
"""
User facade for the HBnB project
"""
from app.business.facades.base_facade import BaseFacade
from app.business.models.user import User


class UserFacade(BaseFacade):
    """
    User facade class that provides a simplified interface to user operations
    """

    def __init__(self, repository):
        """
        Initialize a new UserFacade instance

        Args:
            repository: The repository to use for persistence
        """
        super().__init__(repository)

    def create(self, data):
        """
        Create a new user

        Args:
            data: Dictionary of user attributes

        Returns:
            The created user
        """
        user = User(**data)
        return self.repository.save(user)

    def update(self, user_id, data):
        """
        Update a user

        Args:
            user_id: The ID of the user to update
            data: Dictionary of attributes to update

        Returns:
            The updated user if successful, None otherwise
        """
        user = self.repository.get(user_id)
        if not user:
            return None

        for key, value in data.items():
            if key not in ['id', 'created_at', 'updated_at']:
                setattr(user, key, value)
        
        try:
            user.validate()
        except ValueError as e:
            # Re-raise the validation error
            raise ValueError(f"Validation error: {str(e)}")
        
        user.save()
        return self.repository.update(user)

    def get_all_users(self):
        """
        Get all users

        Returns:
            A list of all users
        """
        return self.repository.all()
