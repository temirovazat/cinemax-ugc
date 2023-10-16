from enum import Enum


class MongoCollections(Enum):
    """Enumeration of collections in MongoDB.

    Provides names for the following collections:
    - users
    - films
    - reviews
    """

    users = 'users'
    films = 'films'
    reviews = 'reviews'
