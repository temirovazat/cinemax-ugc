from datetime import datetime
from typing import Dict
from uuid import UUID

from pydantic import Field, validator

from models.base import MongoQuery, SortChoices, VotesChoices


class AddBookmark(MongoQuery):
    """Model for adding a movie to a user's bookmarks."""

    user_id: UUID
    film_id: UUID

    @property
    def params(self) -> Dict:
        """Request parameters for updating a user's bookmarks list.

        Returns:
            Dict: Request to update the document with the user.
        """
        mapping = {}
        mapping['$addToSet'] = {'bookmarks': {'film_id': self.film_id}}
        return self.update_operations(self.user_id, mapping, upsert=True)


class RemoveBookmark(MongoQuery):
    """Model for removing a movie from a user's bookmarks."""

    user_id: UUID
    film_id: UUID

    @property
    def params(self) -> Dict:
        """Request parameters for updating a user's bookmarks list.

        Returns:
            Dict: Request to update the document with the user.
        """
        mapping = {}
        mapping['$pull'] = {'bookmarks': {'film_id': self.film_id}}
        return self.update_operations(self.user_id, mapping)


class AddRating(MongoQuery):
    """Model for setting a user's rating."""

    user_id: UUID
    source_id: UUID
    score: VotesChoices

    @property
    def params(self) -> Dict:
        """Request parameters for updating a movie's or review's rating.

        Returns:
            Dict: Request to update the document with the movie or review.
        """
        pipeline = []
        pipeline.append(
            {'$set': {'rating.votes': {
                '$concatArrays': [
                    [{'user_id': self.user_id, 'score': self.score.value}],
                    {'$filter': {
                        'input': {'$ifNull': ['$rating.votes', []]},
                        'cond': {'$ne': ['$$this.user_id', self.user_id]},
                    }},
                ]},
            }},
        )
        return self.update_operations(self.source_id, pipeline)


class RemoveRating(MongoQuery):
    """Model for removing a user's rating."""

    user_id: UUID
    source_id: UUID

    @property
    def params(self) -> Dict:
        """Request parameters for updating a movie's or review's rating.

        Returns:
            Dict: Request to update the document with the movie or review.
        """
        mapping = {}
        mapping['$pull'] = {'rating.votes': {'user_id': {'$eq': self.user_id}}}
        return self.update_operations(self.source_id, mapping)


class CreateReview(MongoQuery):
    """Model for creating a review by a user for a movie."""

    author: UUID
    film_id: UUID
    text: str
    pub_date: datetime = Field(default_factory=datetime.now)

    @property
    def params(self) -> Dict:
        """Request parameters for inserting a movie review.

        Returns:
            Dict: Request to insert a document with the review.
        """
        new_doc = self.dict()
        new_doc['rating'] = {'votes': []}
        return self.insert_operations(new_doc)


class DestroyReview(MongoQuery):
    """Model for deleting a user's movie review."""

    id: UUID = Field(alias='_id')
    author: UUID

    @property
    def params(self) -> Dict:
        """Request parameters for deleting a movie review.

        Returns:
            Dict: Request to delete the document with the review.
        """
        filtering = self.dict(by_alias=True)
        return self.delete_operations(filtering)

    class Config:
        """Validation settings."""

        allow_population_by_field_name = True


class ListReview(MongoQuery):
    """Model for retrieving a list of movie reviews with flexible sorting options."""

    film_id: UUID
    sort: SortChoices
    offset: int
    limit: int

    @validator('sort')
    def ordering(cls, sort: SortChoices) -> Dict:
        """Validate the sorting parameter to prepare it for the request.

        Args:
            sort: Sorting parameter

        Returns:
            Dict: Request data with sorting.
        """
        result = {}
        if sort == SortChoices.top:
            result.update({'average_rating': -1})
        elif sort == SortChoices.new:
            result.update({'pub_date': -1})
        elif sort == SortChoices.old:
            result.update({'pub_date': 1})
        return result

    @property
    def params(self) -> Dict:
        """Request parameters for retrieving movie reviews.

        Returns:
            Dict: Request to find documents with reviews.
        """
        pipeline = []
        pipeline.extend([
            {'$match': {'film_id': self.film_id}},
            {'$lookup': {
                'from': 'films',
                'let': {'author': '$author'},
                'pipeline': [
                    {'$match': {'_id': self.film_id}},
                    {'$unwind': '$rating.votes'},
                    {'$match': {'$expr': {'$eq': ['$rating.votes.user_id', '$$author']}}},
                ],
                'as': 'films',
            }},
            {'$addFields': {
                'film_score': {
                    '$first': '$films.rating.votes.score',
                },
                'likes': {'$size': {'$filter': {
                    'input': '$rating.votes',
                    'cond': {'$eq': ['$$this.score', VotesChoices.like.value]},
                }}},
                'dislikes': {'$size': {'$filter': {
                    'input': '$rating.votes',
                    'cond': {'$eq': ['$$this.score', VotesChoices.dislike.value]},
                }}},
                'average_rating': {
                    '$avg': '$rating.votes.score',
                },
            }},
            {'$sort': self.sort},
            {'$skip': self.offset},
            {'$limit': self.limit},
        ])
        return self.find_operations(pipeline)
