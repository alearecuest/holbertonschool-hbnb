#!/usr/bin/python3
"""
Base facade for the HBnB project
"""


class BaseFacade:
    """
    Base facade class that provides a simplified interface to repository operations
    """

    def __init__(self, repository):
        """
        Initialize a new BaseFacade instance

        Args:
            repository: The repository to use for persistence
        """
        self.repository = repository

    def get_by_id(self, entity_id):
        """
        Get an entity by ID

        Args:
            entity_id: The ID of the entity to get

        Returns:
            The entity if found, None otherwise
        """
        return self.repository.get(entity_id)

    def get_all(self):
        """
        Get all entities

        Returns:
            A list of all entities
        """
        return self.repository.all()

    def create(self, data):
        """
        Create a new entity

        Args:
            data: Dictionary of entity attributes

        Returns:
            The created entity
        """
        raise NotImplementedError("Subclasses must implement this method")

    def update(self, entity_id, data):
        """
        Update an entity

        Args:
            entity_id: The ID of the entity to update
            data: Dictionary of attributes to update

        Returns:
            The updated entity if successful, None otherwise
        """
        raise NotImplementedError("Subclasses must implement this method")

    def delete(self, entity_id):
        """
        Delete an entity

        Args:
            entity_id: The ID of the entity to delete

        Returns:
            True if successful, False otherwise
        """
        entity = self.repository.get(entity_id)
        if not entity:
            return False
        return self.repository.delete(entity_id)
