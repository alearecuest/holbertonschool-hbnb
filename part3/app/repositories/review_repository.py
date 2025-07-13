#!/usr/bin/python3
"""
Review repository for database operations
"""
from app.repositories.sqlalchemy_repository import SQLAlchemyRepository
from app.models.review import Review

class ReviewRepository(SQLAlchemyRepository):
    """Repository for Review entity operations"""
    
    def __init__(self):
        """Initialize repository with Review model"""
        super().__init__(Review)
    
    def get_reviews_by_rating(self, min_rating):
        """
        Get reviews with rating greater than or equal to min_rating
        
        Args:
            min_rating (int): Minimum rating
            
        Returns:
            list: List of reviews with rating >= min_rating
        """
        return Review.query.filter(Review.rating >= min_rating).all()
