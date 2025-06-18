#!/usr/bin/python3
"""
In-memory implementation of the User repository.
"""
import uuid
from datetime import datetime
from app.business.models.user import User
from app.persistence.repositories.interfaces.user_repository_interface import UserRepositoryInterface

class InMemoryUserRepository(UserRepositoryInterface):
    """In-memory repository for users"""
    
    def __init__(self):
        self.users = {}
    
    def create(self, user_data):
        """Create a new user"""
        # Generate unique ID
        user_id = str(uuid.uuid4())
        

        user = User(
            id=user_id,
            email=user_data.get('email'),
            password=user_data.get('password'),
            first_name=user_data.get('first_name', ''),
            last_name=user_data.get('last_name', ''),
            created_at=datetime.now(),
            updated_at=datetime.now()
        )
        

        self.users[user_id] = user
        return user
    
    def get_by_id(self, user_id):
        """Get a user by ID"""
        return self.users.get(user_id)
    
    def get_all(self):
        """Get all users"""
        return list(self.users.values())
    
    def update(self, user_id, user_data):
        """Update an existing user"""
        user = self.get_by_id(user_id)
        if not user:
            return None
        

        for key, value in user_data.items():
            if hasattr(user, key) and key not in ('id', 'created_at'):
                setattr(user, key, value)
        
        user.updated_at = datetime.now()
        return user
    
    def delete(self, user_id):
        """Delete a user"""
        if user_id in self.users:
            del self.users[user_id]
            return True
        return False
    
    def get_by_email(self, email):
        """Get a user by email"""
        for user in self.users.values():
            if user.email == email:
                return user
        return None