#!/usr/bin/python3
"""
Test script for Amenity API endpoints
"""
import requests
import json
import sys

BASE_URL = "http://localhost:5000/api/v1"

def print_response(response):
    """Print the response in a formatted way"""
    print(f"Status Code: {response.status_code}")
    print("Headers:")
    for key, value in response.headers.items():
        print(f"  {key}: {value}")
    print("Body:")
    try:
        print(json.dumps(response.json(), indent=2))
    except json.JSONDecodeError:
        print(response.text)
    print("-" * 80)

def test_create_amenity():
    """Test creating an amenity"""
    print("\n=== Testing Create Amenity ===")
    print(f"POST {BASE_URL}/amenities/")

    amenity_data = {
        "name": "WiFi",
        "description": "High-speed wireless internet"
    }

    print(f"Request data: {json.dumps(amenity_data)}")

    response = requests.post(f"{BASE_URL}/amenities/", json=amenity_data)

    print_response(response)

    if response.status_code == 201:
        return response.json().get("id")
    return None

def main():
    """Main function to run the tests"""
    print("Starting Amenity API Tests")
    print(f"API base URL: {BASE_URL}")
    
    try:

        print("\n=== Testing API Documentation ===")
        print(f"GET {BASE_URL}/")
        response = requests.get(f"{BASE_URL}/")
        if response.status_code == 200:
            print("API documentation is accessible!")
        else:
            print("Warning: API documentation returned status code:", response.status_code)
            print("This might indicate a configuration problem with the API.")
    except requests.exceptions.RequestException as e:
        print(f"Error accessing API documentation: {e}")

    amenity_id = test_create_amenity()
    
    if not amenity_id:
        print("Failed to create amenity. Aborting tests.")
        sys.exit(1)

    print("\nTest completed successfully!")

if __name__ == "__main__":
    main()
