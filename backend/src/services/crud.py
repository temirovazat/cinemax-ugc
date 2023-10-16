import logging
from functools import lru_cache
from http import HTTPStatus
from typing import Dict, List
from uuid import UUID

from fastapi import Depends, HTTPException
from motor.motor_asyncio import AsyncIOMotorDatabase
from pymongo.errors import ServerSelectionTimeoutError

from core.enums import MongoCollections
from db.mongo import get_mongo
from models.base import MongoQuery


class CRUDService:
    """Class for performing basic data processing operations in MongoDB."""

    def __init__(self, mongo: AsyncIOMotorDatabase):
        """When initializing the class, it accepts the MongoDB database client.

        Args:
            mongo: MongoDB client
        """
        self.mongo = mongo

    async def create(self, collection: MongoCollections, query: MongoQuery) -> Dict:
        """Create a document in the collection.

        Args:
            collection: Collection with documents
            query: MongoDB query

        Raises:
            HTTPException: An error if the MongoDB server is unavailable for the operation

        Returns:
            Dict: New document
        """
        try:
            result = await self.mongo[collection.name].find_one_and_replace(**query.params)
        except ServerSelectionTimeoutError as exc:
            logging.error(exc)
            raise HTTPException(status_code=HTTPStatus.BAD_REQUEST)
        return result or {}

    async def retrieve(self, collection: MongoCollections, doc_id: UUID) -> Dict:
        """Read a document by ID from the collection.

        Args:
            collection: Collection with documents
            doc_id: Document ID

        Raises:
            HTTPException: An error if the MongoDB server is unavailable for the operation

        Returns:
            Dict: Document by ID
        """
        try:
            result = await self.mongo[collection.name].find_one(doc_id)
        except ServerSelectionTimeoutError as exc:
            logging.error(exc)
            raise HTTPException(status_code=HTTPStatus.BAD_REQUEST)
        return result or {}

    async def search(self, collection: MongoCollections, query: MongoQuery) -> List[Dict]:
        """Search for documents in the collection.

        Args:
            collection: Collection with documents
            query: MongoDB query

        Raises:
            HTTPException: An error if the MongoDB server is unavailable for the operation

        Returns:
            List: List of documents
        """
        try:
            result = await self.mongo[collection.name].aggregate(**query.params).to_list(None)
        except ServerSelectionTimeoutError as exc:
            logging.error(exc)
            raise HTTPException(status_code=HTTPStatus.BAD_REQUEST)
        return result

    async def update(self, collection: MongoCollections, query: MongoQuery) -> Dict:
        """Update a document in the collection.

        Args:
            collection: Collection with documents
            query: MongoDB query

        Raises:
            HTTPException: An error if the MongoDB server is unavailable for the operation

        Returns:
            Dict: Document after the update
        """
        try:
            result = await self.mongo[collection.name].find_one_and_update(**query.params)
        except ServerSelectionTimeoutError as exc:
            logging.error(exc)
            raise HTTPException(status_code=HTTPStatus.BAD_REQUEST)
        return result or {}

    async def delete(self, collection: MongoCollections, query: MongoQuery) -> Dict:
        """Delete a document from the collection.

        Args:
            collection: Collection with documents
            query: MongoDB query

        Raises:
            HTTPException: An error if the MongoDB server is unavailable for the operation

        Returns:
            Dict: Document to be deleted
        """
        try:
            result = await self.mongo[collection.name].find_one_and_delete(**query.params)
        except ServerSelectionTimeoutError as exc:
            logging.error(exc)
            raise HTTPException(status_code=HTTPStatus.BAD_REQUEST)
        return result


@lru_cache()
def get_crud_service(mongo: AsyncIOMotorDatabase = Depends(get_mongo)) -> CRUDService:
    """Create a CRUDService object as a singleton.

    Args:
        mongo: MongoDB connection

    Returns:
        CRUDService: Service for data processing in MongoDB
    """
    return CRUDService(mongo)
