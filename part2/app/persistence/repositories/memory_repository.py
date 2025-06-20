#!/usr/bin/python3
"""
In-memory repository implementation for the HBnB project
"""


class MemoryRepository:
    """
    In-memory repository for storing and retrieving objects
    """

    def __init__(self):
        """
        Initialize a new MemoryRepository instance
        """
        self._objects = {}

    def save(self, obj):
        """
        Save an object to the repository

        Args:
            obj: The object to save
        """
        if not hasattr(obj, 'id'):
            raise ValueError("Object must have an 'id' attribute")
        
        self._objects[obj.id] = obj
        return obj

    def get(self, obj_id):
        """
        Get an object from the repository by ID

        Args:
            obj_id: The ID of the object to get

        Returns:
            The object if found, None otherwise
        """
        return self._objects.get(obj_id)

    def all(self):
        """
        Get all objects from the repository

        Returns:
            A list of all objects
        """
        return list(self._objects.values())

    def delete(self, obj_id):
        """
        Delete an object from the repository by ID

        Args:
            obj_id: The ID of the object to delete

        Returns:
            True if the object was deleted, False otherwise
        """
        if obj_id in self._objects:
            del self._objects[obj_id]
            return True
        return False

    def update(self, obj):
        """
        Update an object in the repository

        Args:
            obj: The object to update

        Returns:
            The updated object if successful, None otherwise
        """
        if not hasattr(obj, 'id') or obj.id not in self._objects:
            return None
        
        self._objects[obj.id] = obj
        return obj

    def find_by(self, attribute, value):
        """
        Find objects by attribute value

        Args:
            attribute: The attribute to search by
            value: The value to search for

        Returns:
            A list of objects matching the criteria
        """
        return [obj for obj in self._objects.values() 
                if hasattr(obj, attribute) and getattr(obj, attribute) == value]

    def clear(self):
        """
        Clear all objects from the repository
        """
        self._objects = {}
