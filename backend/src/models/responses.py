from datetime import datetime
from typing import Dict, List, Optional
from uuid import UUID

from pydantic import Field, root_validator, validator

from models.base import APIResponse, OrjsonMixin, VotesChoices


class BookmarkResponse(APIResponse):
    """Response model for representing a bookmark (movie saved for later)."""

    film_id: UUID


class Vote(OrjsonMixin):
    """Class for user rating."""

    user_id: UUID
    score: VotesChoices


class RatingResponse(APIResponse):
    """Response model for representing a rating."""

    likes: int = Field(default=0)
    dislikes: int = Field(default=0)
    average_rating: Optional[int]
    votes: Optional[List[Vote]] = Field(exclude=True)

    @root_validator
    def scoring(cls, data: Dict) -> Dict:
        """Primary validator for counting the number of likes, dislikes, and the average user rating.

        Args:
            data: User vote data

        Returns:
            Dict: Calculated rating
        """
        if votes := data.get('votes'):
            total_scores = 0
            for vote in votes:
                if vote.score == VotesChoices.like.value:
                    data['likes'] += 1
                elif vote.score == VotesChoices.dislike.value:
                    data['dislikes'] += 1
                total_scores += vote.score
            data['average_rating'] = total_scores // (data['likes'] + data['dislikes'])
        return data


class ReviewResponse(APIResponse):
    """Response model for representing a film review."""

    id: UUID = Field(alias='_id')
    author: UUID
    film_id: UUID
    text: str
    pub_date: datetime
    film_score: Optional[VotesChoices]
    likes: int = Field(default=0)
    dislikes: int = Field(default=0)
    average_rating: Optional[int]

    @validator('film_score')
    def get_film_vote(cls, film_score: VotesChoices) -> str:
        """Convert the film rating by the review author to a like or dislike.

        Args:
            film_score: Film rating associated with the review

        Returns:
            str: Like or dislike
        """
        return film_score.name
