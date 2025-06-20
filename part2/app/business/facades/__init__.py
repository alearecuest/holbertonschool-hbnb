#!/usr/bin/python3
"""
Facades package for the HBnB project business logic layer

This package contains facade classes that provide simplified interfaces
to the complex subsystems of the business logic layer.
"""

from app.business.facades.base_facade import BaseFacade
from app.business.facades.user_facade import UserFacade

__all__ = ['BaseFacade', 'UserFacade']
