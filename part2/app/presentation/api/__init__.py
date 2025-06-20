#!/usr/bin/python3
"""
API Controllers package for the HBnB project presentation layer

This package contains the API controller classes that handle HTTP requests
and responses for the HBnB application. These controllers are responsible
for routing requests to the appropriate business logic facades and formatting
responses according to the API specifications.
"""

from app.presentation.api.user_controller import api as user_api

__all__ = ['user_api']