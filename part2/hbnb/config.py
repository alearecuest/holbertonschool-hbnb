#!/usr/bin/python3
"""
Configuration settings for different environments of the HBnB application.
"""

class Config:
    """Base configuration class"""
    DEBUG = False
    TESTING = False
    SECRET_KEY = 'hbnb-secret-key'

class DevelopmentConfig(Config):
    """Development environment configuration"""
    DEBUG = True

class TestingConfig(Config):
    """Testing environment configuration"""
    TESTING = True
    DEBUG = True

class ProductionConfig(Config):
    """Production environment configuration"""
    DEBUG = False
