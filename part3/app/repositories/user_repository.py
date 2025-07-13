#!/usr/bin/python3
"""
User repository for database operations
"""
from app.repositories.sqlalchemy_repository import SQLAlchemyRepository
from app.models.user import User

class UserRepository(SQLAlchemyRepository):
    """Repository for User entity operations"""
    
    def __init__(self):
        """Initialize repository with User model"""
        super().__init__(User)
    
    def get_user_by_email(self, email):
        """
        Get user by email
        
        Args:
            email (str): User's email
            
        Returns:
            User: User object if found, None otherwise
        """
        return User.query.filter_by(email=email).first()
    
    def email_exists(self, email):
        """
        Check if email exists
        
        Args:
            email (str): Email to check
            
        Returns:
            bool: True if exists, False otherwise
        """
        return User.query.filter_by(email=email).count() > 0
