#!/usr/bin/python3
"""
Place model for the HBnB project
"""
from app.models.base_model import BaseModel
from app.extensiones import db
from app.models.user import User
from app.models.associations import place_amenity

class Place(BaseModel):
    """Place class for representing rental properties in the HBnB application"""
    __tablename__ = 'places'
    
    title = db.Column(db.String(100), nullable=False)
    description = db.Column(db.Text, nullable=True)
    price = db.Column(db.Float, nullable=False)
    latitude = db.Column(db.Float, nullable=False)
    longitude = db.Column(db.Float, nullable=False)
    
    # Foreign key para la relación con User
    owner_id = db.Column(db.String(36), db.ForeignKey('users.id'), nullable=False)
    
    # Relaciones con otras entidades
    reviews = db.relationship('Review', backref='place', lazy=True, 
                           cascade="all, delete-orphan")
    
    # Relación many-to-many con Amenity
    amenities = db.relationship('Amenity', secondary=place_amenity, 
                             lazy='subquery', backref=db.backref('places', lazy=True))

    def __init__(self, title, description, price, latitude, longitude, owner, **kwargs):
        """
        Initialize a new Place instance

        Args:
            title (str): Title of the place
            description (str): Description of the place
            price (float): Price per night
            latitude (float): Latitude coordinate
            longitude (float): Longitude coordinate
            owner (User): User who owns the place
            **kwargs: Additional attributes to set
        """
        super().__init__(**kwargs)
        self.title = title
        self.description = description
        self.price = price
        self.latitude = latitude
        self.longitude = longitude
        self.owner = owner  # SQLAlchemy manejará el owner_id automáticamente
        self.validate()

    def validate(self):
        """
        Validate place attributes

        Raises:
            ValueError: If any validation fails
        """
        if not self.title or not isinstance(self.title, str):
            raise ValueError("Title is required and must be a string")
        if len(self.title) > 100:
            raise ValueError("Title must be at most 100 characters")

        if self.description is not None and not isinstance(self.description, str):
            raise ValueError("Description must be a string")

        if not isinstance(self.price, (int, float)):
            raise ValueError("Price must be a number")
        if self.price <= 0:
            raise ValueError("Price must be positive")

        if not isinstance(self.latitude, (int, float)):
            raise ValueError("Latitude must be a number")
        if self.latitude < -90.0 or self.latitude > 90.0:
            raise ValueError("Latitude must be between -90.0 and 90.0")

        if not isinstance(self.longitude, (int, float)):
            raise ValueError("Longitude must be a number")
        if self.longitude < -180.0 or self.longitude > 180.0:
            raise ValueError("Longitude must be between -180.0 and 180.0")

        if not isinstance(self.owner, User):
            raise ValueError("Owner must be a User instance")

    def add_review(self, review):
        """
        Add a review to the place

        Args:
            review: The review to add
        """
        if review not in self.reviews:
            self.reviews.append(review)

    def add_amenity(self, amenity):
        """
        Add an amenity to the place

        Args:
            amenity: The amenity to add
        """
        if amenity not in self.amenities:
            self.amenities.append(amenity)

    def get_reviews(self):
        """
        Get all reviews for the place

        Returns:
            list: List of reviews
        """
        return self.reviews

    def get_amenities(self):
        """
        Get all amenities for the place

        Returns:
            list: List of amenities
        """
        return self.amenities
