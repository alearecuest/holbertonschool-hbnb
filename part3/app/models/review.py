#!/usr/bin/python3
"""
Review model for the HBnB project
"""
from app.models.base_model import BaseModel
from app.extensiones import db

class Review(BaseModel):
    """Review class for representing reviews in the HBnB application"""
    __tablename__ = 'reviews'
    
    text = db.Column(db.Text, nullable=False)
    rating = db.Column(db.Integer, nullable=False)
    
    place_id = db.Column(db.String(36), db.ForeignKey('places.id'), nullable=False)
    user_id = db.Column(db.String(36), db.ForeignKey('users.id'), nullable=False)
    
    def __init__(self, text, rating, place, user, **kwargs):
        """
        Initialize a new Review instance

        Args:
            text (str): Content of the review
            rating (int): Rating given to the place (1-5)
            place (Place): The place being reviewed
            user (User): The user writing the review
            **kwargs: Additional attributes to set
        """
        super().__init__(**kwargs)
        self.text = text
        self.rating = rating
        self.place = place  # SQLAlchemy manejará el place_id automáticamente
        self.user = user    # SQLAlchemy manejará el user_id automáticamente
        self.validate()
        
        if hasattr(self.place, 'add_review'):
            self.place.add_review(self)

    def validate(self):
        """
        Validate review attributes

        Raises:
            ValueError: If any validation fails
        """
        if not self.text or not isinstance(self.text, str):
            raise ValueError("Review text is required and must be a string")

        if not isinstance(self.rating, int):
            raise ValueError("Rating must be an integer")
        if self.rating < 1 or self.rating > 5:
            raise ValueError("Rating must be between 1 and 5")

        from app.models.place import Place
        if not isinstance(self.place, Place):
            raise ValueError("Place must be a Place instance")

        from app.models.user import User
        if not isinstance(self.user, User):
            raise ValueError("User must be a User instance")
