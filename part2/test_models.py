#!/usr/bin/python3
"""
Test script for HBnB business logic classes
"""
from models.base_model import BaseModel
from models.user import User
from models.place import Place
from models.review import Review
from models.amenity import Amenity

if __name__ == "__main__":
    print("Testing HBnB Business Logic Classes...")
    print("\n" + "=" * 50)
    
    print("\nCreating a User:")
    user = User(
        email="alearecuest@example.com",
        password="secure_password",
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
        amenity.add_place(place)
    
    print(f"Number of amenities in place: {len(place.amenities)}")
    
    print("\n" + "=" * 50)
    
    print("\nCreating a Review:")
    review = Review(
        text="Great place, would definitely stay again!",
        user_id=user.id,
        place_id=place.id,
        rating=5
    )
    print(review)
    print(f"Review text: {review.text}")
    print(f"Review rating: {review.rating}")
    
    # Establish relationships
    user.add_review(review)
    place.add_review(review)
    
    print(f"Number of reviews by user: {len(user.reviews)}")
    print(f"Number of reviews for place: {len(place.reviews)}")
    
    print("\n" + "=" * 50)
    
    print("\nTesting to_dict method:")
    user_dict = user.to_dict()
    print(f"User as dictionary: {user_dict}")
    
    print("\nReconstructing User from dictionary:")
    new_user = User(**user_dict)
    print(new_user)
    print(f"Same ID? {new_user.id == user.id}")
    
    print("\nTest completed!")
