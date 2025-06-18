#!/usr/bin/python3
"""
Interface defining the contract for User repository operations.
"""
from abc import ABC, abstractmethod

class UserRepositoryInterface(ABC):
    """Interface for User repository operations"""
    
    @abstractmethod
    def create(self, user_data):
        """Create a new user"""
        pass
    
    @abstractmethod
    def get_by_id(self, user_id):
        """Get a user by ID"""
        pass
    
    @abstractmethod
    def get_all(self):
        """Get all users"""
        pass
    
    @abstractmethod
    def update(self, user_id, user_data):
        """Update an existing user"""
        pass
    
    @abstractmethod
    def delete(self, user_id):
        """Delete a user"""
        pass
    
    @abstractmethod
    def get_by_email(self, email):
        """Get a user by email"""
        pass