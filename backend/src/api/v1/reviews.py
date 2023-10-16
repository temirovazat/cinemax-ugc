from http import HTTPStatus
from uuid import UUID

from fastapi import Body, Depends, Path, Query, Response
from pymongo.errors import DuplicateKeyError

from api.v1.base import Paginator
from services.auth import AuthService
from services.crud import CRUDService, get_crud_service
from core.enums import MongoCollections
from core.exceptions import NotAuthorContentError, UniqueFilmReviewError
from models.base import SortChoices
from models.queries import CreateReview, DestroyReview, ListReview
from models.responses import ReviewResponse


async def create_film_review(
    auth: AuthService = Depends(),
    film_id: UUID = Path(title='Film ID'),
    text: str = Body(embed=True),
    mongo: CRUDService = Depends(get_crud_service),
) -> ReviewResponse:
    """Create a movie review by a user.

    Args:
        auth: User authentication
        film_id: Film ID
        text: Review text
        mongo: Object for performing MongoDB queries

    Raises:
        UniqueFilmReviewError: 403 error if the user already has a review for the given film

    Returns:
        ReviewResponse: Movie review
    """
    try:
        review = await mongo.create(
            collection=MongoCollections.reviews,
            query=CreateReview(author=auth.user_id, film_id=film_id, text=text),
        )
    except DuplicateKeyError:
        raise UniqueFilmReviewError(status_code=HTTPStatus.FORBIDDEN)
    return review


async def delete_film_review(
    auth: AuthService = Depends(),
    film_id: UUID = Path(title='Film ID'),
    review_id: UUID = Path(title='Review ID'),
    mongo: CRUDService = Depends(get_crud_service),
) -> Response:
    """Delete a movie review by a user.

    Args:
        auth: User authentication
        film_id: Film ID
        review_id: Review ID
        mongo: Object for performing MongoDB queries

    Raises:
        NotAuthorContentError: 403 error if the user is not the author of the review

    Returns:
        Response: HTTP response with status code 204
    """
    review = await mongo.delete(
        collection=MongoCollections.reviews,
        query=DestroyReview(id=review_id, author=auth.user_id),
    )
    if not review:
        raise NotAuthorContentError(status_code=HTTPStatus.FORBIDDEN)
    return Response(status_code=HTTPStatus.NO_CONTENT)


async def get_film_reviews(
    film_id: UUID = Path(title='Film ID'),
    sort: SortChoices = Query(default=SortChoices.top),
    page: Paginator = Depends(),
    mongo: CRUDService = Depends(get_crud_service),
) -> ReviewResponse:
    """Retrieve a list of movie reviews for a film.

    Args:
        film_id: Film ID
        sort: Sorting parameter
        page: Page parameters
        mongo: Object for performing MongoDB queries

    Returns:
        ReviewResponse: List of movie reviews
    """
    reviews = await mongo.search(
        collection=MongoCollections.reviews,
        query=ListReview(film_id=film_id, sort=sort, offset=page.offset, limit=page.limit),
    )
    return reviews
