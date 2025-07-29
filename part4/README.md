# HBnB Project

## Overview
HBnB (Holberton BnB) is a RESTful API for a vacation rental platform.
Manual of Completed Tasks

## TASK 0 
#### Initial Project Setup • Folder structure:
* templates/
* static/css/
* static/js/

##### Installed dependencies: 
* Flask
* Flask-CORS
* PyJWT

##### Basic Flask routes defined:
* GET / → render_index (renders index.html)
* GET /login → render_login (renders login.html)
* Other placeholder endpoints

## TASK 1 
### Authentication and AJAX Login • templates/login.html
* Email/password form
* Inline error messages for invalid input • static/js/scripts.js
* login() sends POST to /api/v1/auth/login
* setCookie('token', access_token) to store JWT
* Redirect to index.html on successful login
* Handles 400/401 errors

## TASK 2 – Index Page:
### Listing and Filtering Places • templates/index.html
* Container element for place cards
* Inputs for minimum and maximum price filters • static/js/scripts.js
* fetch('/api/v1/places') to load all places
* displayPlaces(places): injects cards with name, price, etc.
* filterPlaces(min, max): client-side price filtering without reload
* Event listeners on price inputs to re-render the list

## TASK 3 – cURL Tests for the API
* Obtain JWT token curl -i -X POST http://localhost:5000/api/v1/auth/login \ -H "Content-Type: application/json" \ -d '{"email":"user@example.com","password":"pass"}'
* GET /api/v1/places/:id without token → expect HTTP 200
* GET /api/v1/places/:id with token → HTTP 200 + JSON keys: name, description, price, amenities, reviews
* Verify JSON keys with jq or grep
* POST /api/v1/places/:id/reviews without token → HTTP 401
* POST /api/v1/places/:id/reviews with token → HTTP 201/200
* GET /api/v1/places/:id to confirm the new review appears

## TASK 4 – Add Review Form • templates/add_review.html
* <div id="place-details"> for injecting place info and reviews
* <section id="add-review"> with form#review-form, select#rating, textarea#comment • static/js/scripts.js
* getCookie(name): read JWT from cookies
* checkAuthentication(): redirect to “/” if no token
* getPlaceIdFromURL(): extract ?id=… from window.location.search
* fetchPlaceDetails(token, placeId): GET place and reviews, then display
* displayPlaceDetails(place): render title, description, price, amenities, reviews
* submitReview(token, placeId, {rating,text}): POST review via fetch
* handleResponse(res):
                    - 200 OK → alert success, reset form, refresh details
                    - 401 → alert session expired, redirect to “/”
                    - Others → alert with server-returned error message
* DOMContentLoaded listener: orchestrates authentication check, data fetch, and form submit handler

## EXPECTED BEHAVIOR AND TESTS
* Without token: immediate redirect to the home page
* With token: place details, existing reviews, and the review form are visible
* Submitting with empty fields → client-side alert “Please fill in all fields.”
* Successful submission → alert “Review submitted successfully!”, form reset, list updated
* Expired/invalid token → alert session expired + redirect
* 405 Method Not Allowed error resolved by removing form’s default method/action and using fetch only

## Project Structure
- `app/`: Core application code
  - `api/`: API endpoints (v1)
  - `models/`: Business logic classes
  - `services/`: Facade pattern implementation
  - `persistence/`: Repository implementation
- `run.py`: Entry point for running the application
- `config.py`: Configuration settings
- `requirements.txt`: Python package dependencies

## Installation

1. Clone the repository:
```bash
git clone <repository-url>
cd hbnb
