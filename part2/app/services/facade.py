#!/usr/bin/python3
"""
Facade service for the HBnB application
"""
from app.repositories.in_memory_repository import InMemoryRepository
from app.models.user import User
from app.models.amenity import Amenity
from app.models.place import Place


class HBnBFacade:
    """Facade for handling business logic operations"""

    def __init__(self):
        """Initialize repositories for different entities"""
        self.user_repo = InMemoryRepository()
        self.amenity_repo = InMemoryRepository()
        self.place_repo = InMemoryRepository()

    def create_user(self, user_data):
        """
        Create a new user

        Args:
            user_data (dict): Data for the new user

        Returns:
            User: The created user
        """
        user = User(**user_data)
        return self.user_repo.add(user)

    def get_user(self, user_id):
        """
        Get a user by ID

        Args:
            user_id (str): ID of the user

        Returns:
            User: The found user or None
        """
        return self.user_repo.get(user_id)

    def get_all_users(self):
        """
        Get all users

        Returns:
            list: List of all users
        """
        return self.user_repo.get_all()

    def update_user(self, user_id, data):
        """
        Update a user

        Args:
            user_id (str): ID of the user
            data (dict): New data for the user

        Returns:
            User: The updated user or None
        """
        return self.user_repo.update(user_id, data)

    def get_user_by_email(self, email):
        """
        Get a user by email

        Args:
            email (str): Email of the user

        Returns:
            User: The found user or None
        """
        return self.user_repo.get_by_attribute('email', email)

    def create_amenity(self, data):
        """
        Create a new amenity

        Args:
            data (dict): Data for the new amenity

        Returns:
            Amenity: The created amenity
            
        Raises:
            ValueError: If amenity data is invalid
        """
        amenity = Amenity(**data)
        return self.amenity_repo.add(amenity)

    def get_amenity(self, amenity_id):
        """
        Get an amenity by ID

        Args:
            amenity_id (str): ID of the amenity

        Returns:
            Amenity: The found amenity or None
        """
        return self.amenity_repo.get(amenity_id)

    def get_all_amenities(self):
        """
        Get all amenities

        Returns:
            list: List of all amenities
        """
        return self.amenity_repo.get_all()

    def update_amenity(self, amenity_id, data):
        """
        Update an amenity

        Args:
            amenity_id (str): ID of the amenity
            data (dict): New data for the amenity

        Returns:
            Amenity: The updated amenity or None
        """
        return self.amenity_repo.update(amenity_id, data)

    def create_place(self, place_data):
        """
        Create a new place
        
        Args:
            place_data (dict): Data for the new place, including:
                - title: Title of the place
                - description: Description of the place
                - price: Price per night
                - latitude: Latitude coordinate
                - longitude: Longitude coordinate
                - owner_id: ID of the owner (User)
                - amenities: List of amenity IDs
        
        Returns:
            Place: The created place
            
        Raises:
            ValueError: If place data is invalid or owner not found
        """
        required_fields = ['title', 'price', 'latitude', 'longitude', 'owner_id']
        for field in required_fields:
            if field not in place_data:
                raise ValueError(f"Missing required field: {field}")
        
        owner = self.get_user(place_data['owner_id'])
        if not owner:
            raise ValueError(f"Owner with ID {place_data['owner_id']} not found")
        
        place_dict = {
            'title': place_data['title'],
            'description': place_data.get('description', ''),
            'price': float(place_data['price']),
            'latitude': float(place_data['latitude']),
            'longitude': float(place_data['longitude']),
            'owner': owner,
        }
        
        place = Place(**place_dict)
        
        if 'amenities' in place_data and place_data['amenities']:
            for amenity_id in place_data['amenities']:
                amenity = self.get_amenity(amenity_id)
                if amenity:
                    place.add_amenity(amenity)
        
        return self.place_repo.add(place)

    def get_place(self, place_id):
        """
        Get a place by ID, including associated owner and amenities
        
        Args:
            place_id (str): ID of the place
            
        Returns:
            Place: The found place or None
        """
        place = self.place_repo.get(place_id)
        if not place:
            return None
        
        place_dict = place.to_dict()
        
        owner = place.owner
        place_dict['owner'] = {
            'id': owner.id,
            'first_name': owner.first_name,
            'last_name': owner.last_name,
            'email': owner.email
        }
        
        amenities = []
        for amenity in place.get_amenities():
            amenities.append({
                'id': amenity.id,
                'name': amenity.name
            })
        
        place_dict['amenities'] = amenities
        return place_dict

    def get_all_places(self):
        """
        Get all places
        
        Returns:
            list: List of all places with basic information
        """
        places = self.place_repo.get_all()
        
        result = []
        for place in places:
            result.append({
                'id': place.id,
                'title': place.title,
                'latitude': place.latitude,
                'longitude': place.longitude
            })
        return result

    def update_place(self, place_id, place_data):
        """
        Update a place
        
        Args:
            place_id (str): ID of the place to update
            place_data (dict): New data for the place
            
        Returns:
            Place: Updated place
            None: If place not found
            
        Raises:
            ValueError: If place data is invalid
        """
        place = self.place_repo.get(place_id)
        if not place:
            return None
        
        if 'owner_id' in place_data:
            owner = self.get_user(place_data['owner_id'])
            if not owner:
                raise ValueError(f"Owner with ID {place_data['owner_id']} not found")
            place_data['owner'] = owner
            del place_data['owner_id']
        
        if 'amenities' in place_data:
            amenity_list = []
            for amenity_id in place_data['amenities']:
                amenity = self.get_amenity(amenity_id)
                if not amenity:
                    raise ValueError(f"Amenity with ID {amenity_id} not found")
                amenity_list.append(amenity)
            
            place.amenities = []
            
            for amenity in amenity_list:
                place.add_amenity(amenity)
            
            del place_data['amenities']
        
        return self.place_repo.update(place_id, place_data)


_facade = HBnBFacade()

def create_user(user_data):
    """Create a new user"""
    return _facade.create_user(user_data)


def get_user(user_id):
    """Get a user by ID"""
    return _facade.get_user(user_id)


def get_all_users():
    """Get all users"""
    return _facade.get_all_users()


def update_user(user_id, data):
    """Update a user"""
    return _facade.update_user(user_id, data)


def get_user_by_email(email):
    """Get a user by email"""
    return _facade.get_user_by_email(email)


def create_amenity(data):
    """Create a new amenity"""
    return _facade.create_amenity(data)


def get_amenity(amenity_id):
    """Get an amenity by ID"""
    return _facade.get_amenity(amenity_id)


def get_all_amenities():
    """Get all amenities"""
    return _facade.get_all_amenities()


def update_amenity(amenity_id, data):
    """Update an amenity"""
    return _facade.update_amenity(amenity_id, data)


def create_place(place_data):
    """Create a new place"""
    return _facade.create_place(place_data)


def get_place(place_id):
    """Get a place by ID"""
    return _facade.get_place(place_id)


def get_all_places():
    """Get all places"""
    return _facade.get_all_places()


def update_place(place_id, data):
    """Update a place"""
    return _facade.update_place(place_id, data)
