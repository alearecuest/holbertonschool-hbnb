#!/usr/bin/python3
"""
Test script for HBnB business logic models
"""
import unittest
import sys
import os

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from app.business.models.base_model import BaseModel
from app.business.models.user import User
from app.business.models.place import Place
from app.business.models.review import Review
from app.business.models.amenity import Amenity



class TestBaseModel(unittest.TestCase):
    """Test cases for BaseModel class"""

    def test_init(self):
        """Test BaseModel initialization"""
        model = BaseModel()
        self.assertIsNotNone(model.id)
        self.assertIsNotNone(model.created_at)
        self.assertIsNotNone(model.updated_at)

    def test_to_dict(self):
        """Test to_dict method"""
        model = BaseModel()
        model_dict = model.to_dict()
        self.assertEqual(model_dict["__class__"], "BaseModel")
        self.assertIn("id", model_dict)
        self.assertIn("created_at", model_dict)
        self.assertIn("updated_at", model_dict)
        
    def test_from_dict(self):
        """Test from_dict method"""
        model = BaseModel()
        model_dict = model.to_dict()
        new_model = BaseModel.from_dict(model_dict)
        self.assertEqual(model.id, new_model.id)
        self.assertEqual(model.__class__.__name__, new_model.__class__.__name__)


class TestUser(unittest.TestCase):
    """Test cases for User class"""

    def test_init(self):
        """Test User initialization"""
        user = User(email="test@example.com", password="password123",
                    first_name="Test", last_name="User")
        self.assertEqual(user.email, "test@example.com")
        self.assertEqual(user.password, "password123")
        self.assertEqual(user.first_name, "Test")
        self.assertEqual(user.last_name, "User")
        self.assertEqual(len(user.places), 0)
        self.assertEqual(len(user.reviews), 0)
        
    def test_invalid_email(self):
        """Test User with invalid email"""
        with self.assertRaises(ValueError):
            User(email="invalid-email", password="password123")
            
    def test_short_password(self):
        """Test User with short password"""
        with self.assertRaises(ValueError):
            User(email="test@example.com", password="short")


class TestPlace(unittest.TestCase):
    """Test cases for Place class"""
    
    def test_init(self):
        """Test Place initialization"""
        place = Place(
            user_id="user123",
            name="Test Place",
            description="A test place",
            number_rooms=2,
            number_bathrooms=1,
            max_guest=4,
            price_by_night=100,
            latitude=40.0,
            longitude=-3.0
        )
        self.assertEqual(place.user_id, "user123")
        self.assertEqual(place.name, "Test Place")
        self.assertEqual(place.description, "A test place")
        self.assertEqual(place.number_rooms, 2)
        self.assertEqual(place.number_bathrooms, 1)
        self.assertEqual(place.max_guest, 4)
        self.assertEqual(place.price_by_night, 100)
        self.assertEqual(place.latitude, 40.0)
        self.assertEqual(place.longitude, -3.0)
        self.assertEqual(len(place.amenities), 0)
        self.assertEqual(len(place.reviews), 0)
        
    def test_empty_name(self):
        """Test Place with empty name"""
        with self.assertRaises(ValueError):
            Place(user_id="user123", name="")
            
    def test_invalid_latitude(self):
        """Test Place with invalid latitude"""
        with self.assertRaises(ValueError):
            Place(
                user_id="user123",
                name="Test Place",
                latitude=100.0,
                longitude=0.0
            )


class TestReview(unittest.TestCase):
    """Test cases for Review class"""
    
    def test_init(self):
        """Test Review initialization"""
        review = Review(
            text="Great place!",
            user_id="user123",
            place_id="place123",
            rating=5
        )
        self.assertEqual(review.text, "Great place!")
        self.assertEqual(review.user_id, "user123")
        self.assertEqual(review.place_id, "place123")
        self.assertEqual(review.rating, 5)
        
    def test_empty_text(self):
        """Test Review with empty text"""
        with self.assertRaises(ValueError):
            Review(
                text="",
                user_id="user123",
                place_id="place123",
                rating=5
            )
            
    def test_invalid_rating(self):
        """Test Review with invalid rating"""
        with self.assertRaises(ValueError):
            Review(
                text="Great place!",
                user_id="user123",
                place_id="place123",
                rating=6
            )


class TestAmenity(unittest.TestCase):
    """Test cases for Amenity class"""
    
    def test_init(self):
        """Test Amenity initialization"""
        amenity = Amenity(
            name="WiFi",
            description="High-speed internet"
        )
        self.assertEqual(amenity.name, "WiFi")
        self.assertEqual(amenity.description, "High-speed internet")
        self.assertEqual(len(amenity.places), 0)
        
    def test_empty_name(self):
        """Test Amenity with empty name"""
        with self.assertRaises(ValueError):
            Amenity(name="", description="Description")


if __name__ == "__main__":
    unittest.main()
