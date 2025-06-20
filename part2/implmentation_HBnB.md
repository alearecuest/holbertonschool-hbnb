hbnb/
├── app/
│   ├── __init__.py
│   ├── presentation/
│   │   ├── __init__.py
│   │   └── api/
│   │       ├── __init__.py
│   │       ├── users.py
│   │       ├── places.py
│   │       ├── reviews.py
│   │       └── amenities.py
│   ├── business/
│   │   ├── __init__.py
│   │   ├── facade/
│   │   │   ├── __init__.py
│   │   │   └── business_facade.py
│   │   └── models/
│   │       ├── __init__.py
│   │       ├── user.py
│   │       ├── place.py
│   │       ├── review.py
│   │       └── amenity.py
│   └── persistence/
│       ├── __init__.py
│       └── repositories/
│           ├── __init__.py
│           ├── in_memory/
│           │   ├── __init__.py
│           │   ├── user_repository.py
│           │   ├── place_repository.py
│           │   ├── review_repository.py
│           │   └── amenity_repository.py
│           └── interfaces/
│               ├── __init__.py
│               ├── user_repository_interface.py
│               ├── place_repository_interface.py
│               ├── review_repository_interface.py
│               └── amenity_repository_interface.py
├── config.py
├── run.py
└── requirements.txt