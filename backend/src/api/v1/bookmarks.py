from uuid import UUID

from fastapi import Depends, Path

from api.v1.base import Paginator
from services.auth import AuthService
from services.crud import CRUDService, get_crud_service
from core.enums import MongoCollections
from models.queries import AddBookmark, RemoveBookmark
from models.responses import BookmarkResponse


async def bookmark_film(
    auth: AuthService = Depends(),
    film_id: UUID = Path(title='Film ID'),
    mongo: CRUDService = Depends(get_crud_service),
) -> BookmarkResponse:
    """Add a movie to the user's bookmarks.

    Args:
        auth: User authentication
        film_id: Film ID
        mongo: Object for performing MongoDB queries

    Returns:
        BookmarkResponse: A list of movies bookmarked by the user.
    """
    user = await mongo.update(
        collection=MongoCollections.users,
        query=AddBookmark(user_id=auth.user_id, film_id=film_id),
    )
    return user.get('bookmarks', [])


async def unbookmark_film(
    auth: AuthService = Depends(),
    film_id: UUID = Path(title='Film ID'),
    mongo: CRUDService = Depends(get_crud_service),
) -> BookmarkResponse:
    """Remove a movie from the user's bookmarks.

    Args:
        auth: User authentication
        film_id: Film ID
        mongo: Object for performing MongoDB queries

    Returns:
        BookmarkResponse: A list of movies bookmarked by the user.
    """
    user = await mongo.update(
        collection=MongoCollections.users,
        query=RemoveBookmark(user_id=auth.user_id, film_id=film_id),
    )
    return user.get('bookmarks', [])


async def get_user_bookmarks(
    auth: AuthService = Depends(),
    page: Paginator = Depends(),
    mongo: CRUDService = Depends(get_crud_service),
) -> BookmarkResponse:
    """Get the user's bookmarks.

    Args:
        auth: User authentication
        page: Page parameters
        mongo: Object for performing MongoDB queries

    Returns:
        BookmarkResponse: A list of movies bookmarked by the user.
    """
    user = await mongo.retrieve(collection=MongoCollections.users, doc_id=auth.user_id)
    return user.get('bookmarks', [])[page.slice]
