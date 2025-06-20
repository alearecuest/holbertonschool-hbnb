# HBnB Architecture Design

## Overview
The HBnB application follows a multi-layered architecture to ensure separation of concerns, maintainability, and scalability.

## Architectural Layers

### 1. Presentation Layer
- Responsible for handling HTTP requests and responses
- Implements RESTful API endpoints using Flask and flask-restx
- Handles input validation and response formatting
- Components:
  - API Controllers
  - Request/Response DTOs
  - API Documentation

### 2. Business Logic Layer
- Contains core application logic and business rules
- Implements service facades to coordinate operations
- Manages entity relationships and validations
- Components:
  - Service Facades
  - Entity Models (User, Place, Review, Amenity)
  - Business Logic Validators

### 3. Persistence Layer
- Manages data storage and retrieval
- Implements repository pattern for data access
- Handles database operations and transactions
- Components:
  - Repositories
  - Data Mappers
  - Database Models

## Design Patterns
- **Facade Pattern**: Simplifies the interface to the Business Logic Layer
- **Repository Pattern**: Abstracts data persistence operations
- **DTO Pattern**: Transfers data between layers with specific formats

## Entity Relationships
- Users can have multiple Places and Reviews
- Places can have multiple Reviews and Amenities
- Reviews belong to a User and a Place
- Amenities can be associated with multiple Places
