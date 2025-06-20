#!/usr/bin/python3
"""
Test script for HBnB business logic models
"""
import unittest
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


class TestUser(unittest.TestCase):
    """Test cases for User class"""

    def test_init(self):
        """Test User initialization"""
        user = User(email="test@example.com", password="password",
                    first_name="Test", last_name="User")
        self.assertEqual(user.email, "test@example.com")
        self.assertEqual(user.password, "password")
        self.assertEqual(user.first_name, "Test")
        self.assertEqual(user.last_name, "User")
        self.assertEqual(len(user.places), 0)
        self.assertEqual(len(user.reviews), 0)


if __name__ == "__main__":
    unittest.main()
