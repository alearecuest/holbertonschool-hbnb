# HBnB API Endpoints

## Users

### GET /api/users
- Description: Get all users
- Response: List of users with basic information

### GET /api/users/{id}
- Description: Get a specific user by ID
- Response: User details including places and reviews

### POST /api/users
- Description: Create a new user
- Request Body: User information (email, password, first_name, last_name)
- Response: Created user details

### PUT /api/users/{id}
- Description: Update a user
- Request Body: Updated user information
- Response: Updated user details

### DELETE /api/users/{id}
- Description: Delete a user
- Response: Success confirmation

## Places

### GET /api/places
- Description: Get all places
- Query Parameters: Filters for location, price, amenities
- Response: List of places with basic information

### GET /api/places/{id}
- Description: Get a specific place by ID
- Response: Place details including amenities and reviews

### POST /api/places
- Description: Create a new place
- Request Body: Place information
- Response: Created place details

### PUT /api/places/{id}
- Description: Update a place
- Request Body: Updated place information
- Response: Updated place details

### DELETE /api/places/{id}
- Description: Delete a place
- Response: Success confirmation

## Reviews

### GET /api/reviews
- Description: Get all reviews
- Response: List of reviews

### GET /api/reviews/{id}
- Description: Get a specific review by ID
- Response: Review details

### POST /api/reviews
- Description: Create a new review
- Request Body: Review information
- Response: Created review details

### PUT /api/reviews/{id}
- Description: Update a review
- Request Body: Updated review information
- Response: Updated review details

### DELETE /api/reviews/{id}
- Description: Delete a review
- Response: Success confirmation

## Amenities

### GET /api/amenities
- Description: Get all amenities
- Response: List of amenities

### GET /api/amenities/{id}
- Description: Get a specific amenity by ID
- Response: Amenity details

### POST /api/amenities
- Description: Create a new amenity
- Request Body: Amenity information
- Response: Created amenity details

### PUT /api/amenities/{id}
- Description: Update an amenity
- Request Body: Updated amenity information
- Response: Updated amenity details

### DELETE /api/amenities/{id}
- Description: Delete an amenity
- Response: Success confirmation
