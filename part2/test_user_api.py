#!/usr/bin/python3
"""
Test script for User API endpoints
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

def test_create_user():
    """Test creating a user"""
    print("\n=== Testing Create User ===")
    
    user_data = {
        "email": "test@example.com",
        "password": "password123",
        "first_name": "Test",
        "last_name": "User"
    }
    
    response = requests.post(f"{BASE_URL}/users/", json=user_data)
    
    print_response(response)
    
    if response.status_code == 201:
        return response.json().get("id")
    return None

def test_get_all_users():
    """Test getting all users"""
    print("\n=== Testing Get All Users ===")
    
    response = requests.get(f"{BASE_URL}/users/")
    
    print_response(response)

def test_get_user_by_id(user_id):
    """Test getting a user by ID"""
    print(f"\n=== Testing Get User by ID: {user_id} ===")
    
    response = requests.get(f"{BASE_URL}/users/{user_id}")
    
    print_response(response)

def test_update_user(user_id):
    """Test updating a user"""
    print(f"\n=== Testing Update User: {user_id} ===")
    
    update_data = {
        "first_name": "Updated",
        "last_name": "Name"
    }
    
    response = requests.put(f"{BASE_URL}/users/{user_id}", json=update_data)
    
    print_response(response)

def test_invalid_update(user_id):
    """Test updating a user with invalid data"""
    print(f"\n=== Testing Invalid Update: {user_id} ===")
    
    invalid_data = {
        "email": "invalid-email"
    }
    
    response = requests.put(f"{BASE_URL}/users/{user_id}", json=invalid_data)
    
    print_response(response)

def test_nonexistent_user():
    """Test getting a nonexistent user"""
    print("\n=== Testing Nonexistent User ===")
    
    response = requests.get(f"{BASE_URL}/users/nonexistent-id")
    
    print_response(response)

def main():
    """Main function to run the tests"""
    print("Starting User API Tests")
    
    user_id = test_create_user()
    
    if not user_id:
        print("Failed to create user. Aborting tests.")
        sys.exit(1)
    
    test_get_all_users()
    test_get_user_by_id(user_id)
    test_update_user(user_id)
    test_invalid_update(user_id)
    test_nonexistent_user()
    
    print("\nAll tests completed!")

if __name__ == "__main__":
    main()
