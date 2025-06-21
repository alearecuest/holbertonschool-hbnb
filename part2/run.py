#!/usr/bin/python3
"""
Entry point for the HBnB application
"""
from app import create_app

app = create_app()

if __name__ == '__main__':
    print("\n=== HBnB Application ===")
    print("Starting server on http://localhost:5000/api/v1/")
    print("API documentation available at http://localhost:5000/api/v1/")

    print("\nAvailable routes:")
    for rule in app.url_map.iter_rules():
        print(f"  {rule}")

    print("\nStarting server...")
    app.run(debug=True, host='0.0.0.0', port=5000)
