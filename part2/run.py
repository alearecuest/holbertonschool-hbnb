#!/usr/bin/python3
"""
Entry point for the HBnB application
"""
from app import create_app

app = create_app()

if __name__ == '__main__':
    print("Starting HBnB server on http://localhost:5000/api/v1/")
    print("API documentation available at http://localhost:5000/api/v1/")
    app.run(debug=True, host='0.0.0.0', port=5000)
