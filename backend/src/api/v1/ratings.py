from http import HTTPStatus
from uuid import UUID

from fastapi import Body, Depends, Path

from services.auth import AuthService
from services.crud import CRUDService, get_crud_service
from core.enums import MongoCollections
from core.exceptions import NotFoundFilmError, NotFoundReviewError
from models.base import VotesChoices
from models.queries import AddRating, RemoveRating
from models.responses import RatingResponse


async def rate_film(
    auth: AuthService = Depends(),
    film_id: UUID = Path(title='Film ID'),
    score: VotesChoices = Body(embed=True),
    mongo: CRUDService = Depends(get_crud_service),
) -> RatingResponse:
    """Set the user's rating for a film.

    Args:
        auth: User authentication
        film_id: Film ID
        score: User's rating
        mongo: Object for MongoDB queries

    Raises:
        NotFoundFilmError: 404 error if the film is not found

    Returns:
        RatingResponse: Film rating
    """
    film = await mongo.update(
        collection=MongoCollections.films,
        query=AddRating(user_id=auth.user_id, source_id=film_id, score=score),
    )
    if not film:
        raise NotFoundFilmError(status_code=HTTPStatus.NOT_FOUND)
    return film.get('rating', {})


async def unrate_film(
    auth: AuthService = Depends(),
    film_id: UUID = Path(title='Film ID'),
    mongo: CRUDService = Depends(get_crud_service),
) -> RatingResponse:
    """Remove the user's rating for a film.

    Args:
        auth: User authentication
        film_id: Film ID
        mongo: Object for MongoDB queries

    Raises:
        NotFoundFilmError: 404 error if the film is not found

    Returns:
        RatingResponse: Film rating
    """
    film = await mongo.update(
        collection=MongoCollections.films,
        query=RemoveRating(user_id=auth.user_id, source_id=film_id),
    )
    if not film:
        raise NotFoundFilmError(status_code=HTTPStatus.NOT_FOUND)
    return film.get('rating', {})


async def get_film_rating(
    film_id: UUID = Path(title='Film ID'),
    mongo: CRUDService = Depends(get_crud_service),
) -> RatingResponse:
    """Get the rating for a film.

    Args:
        film_id: Film ID
        mongo: Object for MongoDB queries

    Raises:
        NotFoundFilmError: 404 error if the film is not found

    Returns:
        RatingResponse: Film rating
    """
    film = await mongo.retrieve(collection=MongoCollections.films, doc_id=film_id)
    if not film:
        raise NotFoundFilmError(status_code=HTTPStatus.NOT_FOUND)
    return film.get('rating', {})


async def rate_review(
    auth: AuthService = Depends(),
    film_id: UUID = Path(title='Film ID'),
    review_id: UUID = Path(title='Review ID'),
    score: VotesChoices = Body(embed=True),
    mongo: CRUDService = Depends(get_crud_service),
) -> RatingResponse:
    """Set the user's rating for a film review.

    Args:
        auth: User authentication
        film_id: Film ID
        review_id: Review ID
        score: User's rating
        mongo: Object for MongoDB queries

    Raises:
        NotFoundReviewError: 404 error if the review is not found

    Returns:
        RatingResponse: Rating for the film review
    """
    review = await mongo.update(
        collection=MongoCollections.reviews,
        query=AddRating(user_id=auth.user_id, source_id=review_id, score=score),
    )
    if not review:
        raise NotFoundReviewError(status_code=HTTPStatus.NOT_FOUND)
    return review.get('rating', {})


async def unrate_review(
    auth: AuthService = Depends(),
    film_id: UUID = Path(title='Film ID'),
    review_id: UUID = Path(title='Review ID'),
    mongo: CRUDService = Depends(get_crud_service),
) -> RatingResponse:
    """Remove the user's rating for a film review.

    Args:
        auth: User authentication
        film_id: Film ID
        review_id: Review ID
        mongo: Object for MongoDB queries

    Raises:
        NotFoundReviewError: 404 error if the review is not found

    Returns:
        RatingResponse: Rating for the film review
    """
    review = await mongo.update(
        collection=MongoCollections.reviews,
        query=RemoveRating(user_id=auth.user_id, source_id=review_id),
    )
    if not review:
        raise NotFoundReviewError(status_code=HTTPStatus.NOT_FOUND)
    return review.get('rating', {})


async def get_review_rating(
    film_id: UUID = Path(title='Film ID'),
    review_id: UUID = Path(title='Review ID'),
    mongo: CRUDService = Depends(get_crud_service),
) -> RatingResponse:
    """Get the rating for a film review.

    Args:
        film_id: Film ID
        review_id: Review ID
        mongo: Object for MongoDB queries

    Raises:
        NotFoundReviewError: 404 error if the review is not found

    Returns:
        RatingResponse: Rating for the film review
    """
    review = await mongo.retrieve(collection=MongoCollections.reviews, doc_id=review_id)
    if not review:
        raise NotFoundReviewError(status_code=HTTPStatus.NOT_FOUND)
    return review.get('rating', {})
