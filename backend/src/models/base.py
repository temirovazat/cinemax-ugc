from abc import ABC, abstractmethod
from enum import Enum, IntEnum
from typing import Callable, Dict, List, Union
from uuid import UUID, uuid4

import orjson
from pydantic import BaseModel

from core.config import CONFIG


class VotesChoices(IntEnum):
    """Enumeration class for user ratings."""

    like = 10
    dislike = 0


class SortChoices(str, Enum):
    """Enumeration class for sorting options."""

    top = 'top'
    new = 'new'
    old = 'old'


def orjson_dumps(data: object, *, default: Callable) -> str:
    """Decode data into Unicode for parsing objects based on pydantic classes.

    Args:
        data: Data to be converted.
        default: Function for objects that cannot be serialized.

    Returns:
        str: JSON string.
    """
    return orjson.dumps(data, default=default).decode()


class OrjsonMixin(BaseModel):
    """Mixin to replace standard JSON handling with faster methods."""

    class Config:
        """Serialization settings."""

        json_loads = orjson.loads
        json_dumps = orjson_dumps


class MongoQuery(ABC, OrjsonMixin):
    """Abstract model for a query written in the MongoDB query language."""

    @property
    @abstractmethod
    def params(self) -> Dict:
        """The main method of the model, representing the parameters of a MongoDB query."""

    def insert_operations(self, new_doc: Dict) -> Dict:
        """Representation of query parameters for inserting a new document.

        Args:
            new_doc: New document.

        Returns:
            Dict: Parameters for the insert operation.
        """
        return {
            'filter': {'_id': uuid4()},
            'replacement': new_doc,
            'upsert': True,
            'return_document': True,
        }

    def find_operations(self, pipeline: List[Dict]) -> Dict:
        """Representation of query parameters for searching and aggregating documents.

        Args:
            pipeline: List of query stages for data retrieval.

        Returns:
            Dict: Parameters for the find operation.
        """
        return {
            'pipeline': pipeline,
        }

    def update_operations(self, doc_id: UUID, mapping: Union[Dict, List], upsert: bool = False) -> Dict:
        """Representation of query parameters for updating a document.

        Args:
            doc_id: Document ID.
            mapping: Document changes.
            upsert: Perform document insertion if the document does not exist.

        Returns:
            Dict: Parameters for the update operation.
        """
        return {
            'filter': {'_id': doc_id},
            'update': mapping,
            'upsert': True if CONFIG.fastapi.debug else upsert,
            'return_document': True,
        }

    def delete_operations(self, filtering: Dict) -> Dict:
        """Representation of query parameters for deleting a document.

        Args:
            filtering: Filter corresponding to the document to be deleted.

        Returns:
            Dict: Parameters for the delete operation.
        """
        return {
            'filter': filtering,
        }


class APIResponse(ABC, OrjsonMixin):
    """Abstract model for an API response, representing data over HTTP."""
