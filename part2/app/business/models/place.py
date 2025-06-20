#!/usr/bin/python3
"""
Place module for the HBnB project
"""
from app.business.models.base_model import BaseModel


class Place(BaseModel):
    """
    Place class for representing places in the HBnB application
    """

    def __init__(self, *args, **kwargs):
        """
        Initialize a new Place instance

        Args:
            *args: Variable length argument list
            **kwargs: Arbitrary keyword arguments
        """
        super().__init__(*args, **kwargs)
        self.user_id = kwargs.get("user_id", "")
        self.name = kwargs.get("name", "")
        self.description = kwargs.get("description", "")
        self.number_rooms = kwargs.get("number_rooms", 0)
        self.number_bathrooms = kwargs.get("number_bathrooms", 0)
        self.max_guest = kwargs.get("max_guest", 0)
        self.price_by_night = kwargs.get("price_by_night", 0)
        self.latitude = kwargs.get("latitude", 0.0)
        self.longitude = kwargs.get("longitude", 0.0)
        self.amenities = []
        self.reviews = []
        
        self._convert_numeric_attributes()
        
        self.validate()

    def _convert_numeric_attributes(self):
        """
        Convert string numeric values to their appropriate types
        """
        try:
            self.number_rooms = int(self.number_rooms)
            self.number_bathrooms = int(self.number_bathrooms)
            self.max_guest = int(self.max_guest)
            self.price_by_night = int(self.price_by_night)
            self.latitude = float(self.latitude)
            self.longitude = float(self.longitude)
        except (ValueError, TypeError):

            pass

    def validate(self):
        """
        Validate place attributes
        
        Raises:
            ValueError: If any attribute is invalid
        """
        if not self.name:
            raise ValueError("Place name cannot be empty")
        
        if not self.user_id:
            raise ValueError("Place must be associated with a user")
        
        if self.number_rooms < 0:
            raise ValueError("Number of rooms cannot be negative")
        
        if self.number_bathrooms < 0:
            raise ValueError("Number of bathrooms cannot be negative")
        
        if self.max_guest < 0:
            raise ValueError("Maximum number of guests cannot be negative")
        
        if self.price_by_night < 0:
            raise ValueError("Price by night cannot be negative")
        
        if not -90 <= self.latitude <= 90:
            raise ValueError("Latitude must be between -90 and 90")
        
        if not -180 <= self.longitude <= 180:
            raise ValueError("Longitude must be between -180 and 180")

    def add_amenity(self, amenity):
        """
        Add an amenity to the place

        Args:
            amenity: The amenity to add
        """
        if amenity not in self.amenities:
            self.amenities.append(amenity)

            if hasattr(amenity, 'add_place'):
                amenity.add_place(self)

    def remove_amenity(self, amenity):
        """
        Remove an amenity from the place

        Args:
            amenity: The amenity to remove
            
        Returns:
            True if the amenity was removed, False otherwise
        """
        if amenity in self.amenities:
            self.amenities.remove(amenity)

            if hasattr(amenity, 'remove_place'):
                amenity.remove_place(self)
            return True
        return False

    def add_review(self, review):
        """
        Add a review to the place

        Args:
            review: The review to add
        """
        if review not in self.reviews:
            self.reviews.append(review)
    
    def get_amenities(self):
        """
        Get all amenities of the place
        
        Returns:
            List of amenities
        """
        return self.amenities
    
    def get_reviews(self):
        """
        Get all reviews of the place
        
        Returns:
            List of reviews
        """
        return self.reviews
    
    def get_average_rating(self):
        """
        Calculate the average rating of the place
        
        Returns:
            Average rating as a float, or 0 if no reviews
        """
        if not self.reviews:
            return 0
        
        total_rating = sum(review.rating for review in self.reviews if hasattr(review, 'rating'))
        return total_rating / len(self.reviews) if self.reviews else 0