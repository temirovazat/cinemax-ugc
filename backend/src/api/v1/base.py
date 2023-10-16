from fastapi import Query


class Paginator:
    """Class for retrieving a page request."""

    def __init__(
        self,
        page_number: int = Query(default=1, description='Page number', ge=1),
        page_size: int = Query(default=10, description='Page size', ge=1, le=100),
    ):
        """
        Initialize the class with page number and page size parameters in the request.

        Args:
            page_number: Page number
            page_size: Page size
        """
        self.offset = (page_number - 1) * page_size if page_number > 1 else 0
        self.limit = page_size

    @property
    def slice(self) -> slice:
        """Slice/part of the object list to retrieve the required page.

        Returns:
            slice: List slice
        """
        return slice(self.offset, self.offset + self.limit)
