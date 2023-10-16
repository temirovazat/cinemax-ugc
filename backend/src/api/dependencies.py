from http import HTTPStatus
from uuid import UUID

from fastapi import Depends

from services.crud import CRUDService, get_crud_service
from core.config import CONFIG
from core.enums import MongoCollections
from core.exceptions import NotFoundFilmError, NotFoundReviewError


async def check_film_exists(film_id: UUID, mongo: CRUDService = Depends(get_crud_service)):
    """Check if a film exists, for dependency injection.

    Args:
        film_id: The film ID
        mongo: Object for executing MongoDB queries

    Raises:
        NotFoundFilmError: 404 error if the film is not found
    """
    if not CONFIG.fastapi.debug:
        if not (await mongo.retrieve(MongoCollections.films, film_id)):
            raise NotFoundFilmError(status_code=HTTPStatus.NOT_FOUND)


async def check_review_exists(review_id: UUID, mongo: CRUDService = Depends(get_crud_service)):
    """Check if a review exists, for dependency injection.

    Args:
        review_id: The review ID
        mongo: Object for executing MongoDB queries

    Raises:
        NotFoundReviewError: 404 error if the review is not found
    """
    if not (await mongo.retrieve(MongoCollections.reviews, review_id)):
        raise NotFoundReviewError(status_code=HTTPStatus.NOT_FOUND)
