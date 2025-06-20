#!/usr/bin/python3
"""
Configuration file for pytest
This file is used to add the project directory to sys.path
"""
import sys
import os

sys.path.insert(0, os.path.abspath(os.path.dirname(__file__)))
