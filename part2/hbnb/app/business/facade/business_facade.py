#!/usr/bin/python3
"""
BusinessFacade implements the Facade pattern to provide a simplified interface
to the business logic layer.
"""
from app.persistence.repositories.in_memory.user_repository import InMemoryUserRepository

class BusinessFacade:
    """Facade that provides access to business logic and repositories"""
    
    _instance = None
    
    def __new__(cls):
        if cls._instance is None:
            cls._instance = super(BusinessFacade, cls).__new__(cls)
            cls._instance._initialize_repositories()
        return cls._instance
    
    def _initialize_repositories(self):
        """Initialize in-memory repositories"""
        self.user_repository = InMemoryUserRepository()
    

    def create_user(self, user_data):
        """Create a new user"""
        return self.user_repository.create(user_data)
    
    def get_user(self, user_id):
        """Get a user by ID"""
        return self.user_repository.get_by_id(user_id)
    
    def get_all_users(self):
        """Get all users"""
        return self.user_repository.get_all()
    
    def update_user(self, user_id, user_data):
        """Update an existing user"""
        return self.user_repository.update(user_id, user_data)
    
    def delete_user(self, user_id):
        """Delete a user"""
        return self.user_repository.delete(user_id)
