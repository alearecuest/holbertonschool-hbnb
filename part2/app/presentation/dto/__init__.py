#!/usr/bin/python3
"""
DTO (Data Transfer Object) package for the HBnB project presentation layer

This package contains DTO classes that are used to transfer data between
the presentation layer and the business logic layer, as well as to define
the API models for request/response serialization.
"""

from app.presentation.dto.user_dto import UserDTO

__all__ = ['UserDTO']
