#!/usr/bin/python3
"""
BaseModel module for the HBnB project
"""
import uuid
from datetime import datetime


class BaseModel:
    """
    Base class for all models in the HBnB application
    """

    def __init__(self, *args, **kwargs):
        """
        Initialize a new BaseModel instance

        Args:
            *args: Variable length argument list (not used)
            **kwargs: Arbitrary keyword arguments to set attributes
        """
        self.id = str(uuid.uuid4())
        self.created_at = datetime.utcnow()
        self.updated_at = self.created_at

        if kwargs:
            for key, value in kwargs.items():
                if key in ["created_at", "updated_at"] and isinstance(value, str):
                    value = datetime.fromisoformat(value)
                if key != "__class__":
                    setattr(self, key, value)

    def __str__(self):
        """
        Return a string representation of the BaseModel instance
        """
        return "[{}] ({}) {}".format(
            self.__class__.__name__, self.id, self.__dict__)

    def __eq__(self, other):
        """
        Check if two model instances are equal (based on ID)
        """
        if not isinstance(other, BaseModel):
            return False
        return self.id == other.id

    def save(self):
        """
        Update the updated_at attribute with current datetime
        """
        self.updated_at = datetime.utcnow()

    def to_dict(self):
        """
        Return a dictionary representation of the BaseModel instance
        """
        obj_dict = self.__dict__.copy()
        obj_dict["__class__"] = self.__class__.__name__
        obj_dict["created_at"] = self.created_at.isoformat()
        obj_dict["updated_at"] = self.updated_at.isoformat()
        
        for key, value in obj_dict.items():
            if isinstance(value, list) and len(value) > 0 and isinstance(value[0], BaseModel):
                obj_dict[key] = [item.id for item in value]
        
        return obj_dict

    @classmethod
    def from_dict(cls, data):
        """
        Create a new instance from a dictionary

        Args:
            data: Dictionary containing attribute values

        Returns:
            A new instance of the class
        """
        if data.get("__class__", "") != cls.__name__:
            data = data.copy()
            data["__class__"] = cls.__name__
        return cls(**data)
