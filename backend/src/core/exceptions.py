from typing import Optional

from fastapi import HTTPException, Request
from fastapi.responses import JSONResponse


class UGCException(HTTPException):
    """Custom HTTP exception."""

    message: Optional[str] = None

    def __init__(self, status_code: int):
        """Initialize the exception with an HTTP error code.

        Args:
            status_code: Error code
        """
        super().__init__(status_code, detail=self.message)

    @staticmethod
    def handler(request: Request, exc: HTTPException) -> JSONResponse:
        """Generate an HTTP response when a custom exception occurs.

        Args:
            request: Client request
            exc: HTTP exception

        Returns:
            JSONResponse: Server response
        """
        return JSONResponse(content={'message': exc.detail}, status_code=exc.status_code)


class NotFoundFilmError(UGCException):
    """Error due to the absence of a film in the database."""

    message: str = 'Film not found!'


class NotFoundReviewError(UGCException):
    """Error due to the absence of a review in the database."""

    message: str = 'Review not found!'


class UniqueFilmReviewError(UGCException):
    """Error due to violating the uniqueness constraint of a review's author and reviewed film."""

    message: str = 'Creating more than one review for a film is prohibited!'


class NotAuthorContentError(UGCException):
    """Error due to violating the restriction on using someone else's content."""

    message: str = 'Modifying someone else content is prohibited!'


exception_handlers = {exc: exc.handler for exc in UGCException.__subclasses__()}
