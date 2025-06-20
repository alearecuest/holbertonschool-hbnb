#!/usr/bin/python3
"""
Setup script for the HBnB application
"""
from setuptools import setup, find_packages

setup(
    name="hbnb",
    version="0.1",
    packages=find_packages(),
    install_requires=[
        "flask==2.0.1",
        "flask-restx==0.5.1",
        "Werkzeug==2.0.1",
        "requests==2.25.1"
    ],
)
