# HBnB Class Diagram

## Core Entities

### BaseModel
- Attributes:
  - id: UUID
  - created_at: DateTime
  - updated_at: DateTime
- Methods:
  - save(): void
  - to_dict(): dict

### User (extends BaseModel)
- Attributes:
  - email: string
  - password: string
  - first_name: string
  - last_name: string
  - places: List<Place>
  - reviews: List<Review>
- Methods:
  - add_place(place): void
  - add_review(review): void

### Place (extends BaseModel)
- Attributes:
  - user_id: string
  - name: string
  - description: string
  - number_rooms: int
  - number_bathrooms: int
  - max_guest: int
  - price_by_night: int
  - latitude: float
  - longitude: float
  - amenities: List<Amenity>
  - reviews: List<Review>
- Methods:
  - add_amenity(amenity): void
  - add_review(review): void

### Review (extends BaseModel)
- Attributes:
  - text: string
  - user_id: string
  - place_id: string
  - rating: int
- Methods:
  - None specific

### Amenity (extends BaseModel)
- Attributes:
  - name: string
  - description: string
  - places: List<Place>
- Methods:
  - add_place(place): void

## Relationships
- User 1:N Place (A user can have multiple places)
- User 1:N Review (A user can write multiple reviews)
- Place 1:N Review (A place can have multiple reviews)
- Place N:N Amenity (A place can have multiple amenities, and amenities can be in multiple places)
