#!/usr/bin/python3
"""
In-memory repository implementation for the HBnB project
"""


class MemoryRepository:
    """
    In-memory repository that stores entities in a dictionary
    """

    def __init__(self):
        """
        Initialize a new MemoryRepository instance
        """
        self.entities = {}

    def all(self):
        """
        Get all entities

        Returns:
            A list of all entities
        """
        return list(self.entities.values())

    def get(self, entity_id):
        """
        Get an entity by ID

        Args:
            entity_id: The ID of the entity to get

        Returns:
            The entity if found, None otherwise
        """
        return self.entities.get(entity_id)

    def save(self, entity):
        """
        Save an entity

        Args:
            entity: The entity to save

        Returns:
            The saved entity
        """
        self.entities[entity.id] = entity
        return entity

    def update(self, entity):
        """
        Update an entity

        Args:
            entity: The entity to update

        Returns:
            The updated entity
        """
        self.entities[entity.id] = entity
        return entity

    def delete(self, entity_id):
        """
        Delete an entity

        Args:
            entity_id: The ID of the entity to delete

        Returns:
            True if successful, False otherwise
        """
        if entity_id in self.entities:
            del self.entities[entity_id]
            return True
        return False
