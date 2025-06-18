#!/usr/bin/python3
"""
User model class representing a user in the business logic layer.
"""
from datetime import datetime

class User:
    """User model for business logic"""
    
    def __init__(self, id=None, email=None, password=None, first_name="", 
                 last_name="", created_at=None, updated_at=None):
        """Initialize a new user"""
        self.id = id
        self.email = email
        self.password = password
        self.first_name = first_name
        self.last_name = last_name
        self.created_at = created_at or datetime.now()
        self.updated_at = updated_at or datetime.now()
    
    def to_dict(self):
        """Convert the user to a dictionary"""
        return {
            'id': self.id,
            'email': self.email,
            'first_name': self.first_name,
            'last_name': self.last_name,
            'created_at': self.created_at.isoformat(),
            'updated_at': self.updated_at.isoformat()
        }
    
    def __str__(self):
        """String representation of the user"""
        return f"User(id={self.id}, email={self.email}, name={self.first_name} {self.last_name})"
