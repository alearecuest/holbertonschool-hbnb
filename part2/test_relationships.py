#!/usr/bin/python3
"""
Test script for HBnB business logic classes relationships
"""
import sys
import os

sys.path.insert(0, os.path.abspath(os.path.dirname(__file__)))

from app.business.models.user import User
from app.business.models.place import Place
from app.business.models.review import Review
from app.business.models.amenity import Amenity

if __name__ == "__main__":
    print("Testing HBnB Business Logic Classes Relationships...")
    print("\n" + "=" * 50)
    
    print("\nCreating a User:")
    user = User(
        email="alearecuest@example.com",
        password="secure_password123",
        first_name="Alea",
        last_name="Recuest"
    )
    print(user)
    print(f"User ID: {user.id}")
    print(f"User Email: {user.email}")
    print(f"User Name: {user.first_name} {user.last_name}")
    
    print("\n" + "=" * 50)
    
    print("\nCreating a Place:")
    place = Place(
        user_id=user.id,
        name="Beautiful Apartment in Madrid",
        description="A cozy place near the city center",
        number_rooms=2,
        number_bathrooms=1,
        max_guest=4,
        price_by_night=80,
        latitude=40.4168,
        longitude=-3.7038
    )
    print(place)
    print(f"Place ID: {place.id}")
    print(f"Place Name: {place.name}")
    print(f"Place Owner ID: {place.user_id}")
    
    # Establish relationship
    user.add_place(place)
    print(f"Number of places owned by user: {len(user.places)}")
    
    print("\n" + "=" * 50)
    
    print("\nCreating Amenities:")
    amenities = [
        Amenity(name="WiFi", description="High-speed internet"),
        Amenity(name="Kitchen", description="Fully equipped kitchen"),
        Amenity(name="AC", description="Air conditioning")
    ]
    
    for amenity in amenities:
        print(f"Amenity: {amenity.name} - {amenity.description}")
        place.add_amenity(amenity)
    
    print(f"Number of amenities in place: {len(place.amenities)}")
    print(f"Places with WiFi amenity: {len(amenities[0].places)}")
    
    print("\n" + "=" * 50)
    
    print("\nCreating Reviews:")
    reviews = [
        Review(
            text="Great place, would definitely stay again!",
            user_id=user.id,
            place_id=place.id,
            rating=5
        ),
        Review(
            text="Nice apartment but a bit noisy.",
            user_id=user.id,
            place_id=place.id,
            rating=4
        )
    ]
    
    for review in reviews:
        print(f"Review: {review.text}")
        print(f"Review rating: {review.rating}")
        # Establish relationships
        user.add_review(review)
        place.add_review(review)
    
    print(f"Number of reviews by user: {len(user.reviews)}")
    print(f"Number of reviews for place: {len(place.reviews)}")
    print(f"Average rating for place: {place.get_average_rating()}")
    
    print("\n" + "=" * 50)
    
    print("\nTesting serialization/deserialization:")
    user_dict = user.to_dict()
    print(f"User serialized: {user_dict}")
    
    new_user = User.from_dict(user_dict)
    print(f"User deserialized: {new_user}")
    print(f"Same ID? {new_user.id == user.id}")
    
    print("\n" + "=" * 50)
    
    print("\nTesting relationship modification:")
    # Remove an amenity
    removed = place.remove_amenity(amenities[0])
    print(f"Removed WiFi amenity: {removed}")
    print(f"Number of amenities in place: {len(place.amenities)}")
    print(f"Places with WiFi amenity: {len(amenities[0].places)}")
    
    print("\nTest completed!")
