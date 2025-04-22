"""
Module for storing ratings and reviews for the application.

This module contains:
    - Pydantic model definitions for ratings and reviews data validation.
    - SQLAlchemy ORM models for persisting ratings and reviews in the database.
"""

from datetime import datetime
from typing import Optional

from pydantic import BaseModel, conint, Field
from sqlalchemy import Column, DateTime, ForeignKey, Integer, String, CheckConstraint
from sqlalchemy.orm import declarative_base, relationship

Base = declarative_base()


class RatingBase(BaseModel):
    """
    Pydantic base class for ratings.
    Defines shared fields and validation logic.
    """

    ride_id: Optional[int] = None
    rating: conint(ge=1, le=5) = Field(
        ...,
        description="Value of the rating on a scale of 1 (lowest) to 5 (highest)."
    )
    review: Optional[str] = Field(
        None,
        description="Optional text review accompanying the rating."
    )
    rating_value: Optional[conint(ge=1, le=5)] = Field(
        None,
        description="Alternative field name for rating value on a scale of 1 (lowest) to 5 (highest)."
    )
    review_text: Optional[str] = Field(
        None,
        description="Optional text review accompanying the rating."
    )
    comment: Optional[str] = None


class RatingCreate(RatingBase):
    """
    Pydantic model for creating a new rating.
    Extends RatingBase with additional fields needed at creation.
    """

    reviewer_id: Optional[int] = Field(
        None,
        description="Identifier for the user posting the rating."
    )


class RatingInDB(RatingBase):
    """
    Pydantic model representing a rating as stored in the database.
    Extends RatingBase with ID and timestamp.
    """

    id: int
    timestamp: datetime


class RatingORM(Base):
    """
    SQLAlchemy ORM model for ratings.
    Maps Python objects to database records in the 'ratings' table.
    Provides a reference to the reviewer (User) if such relationship exists.
    Ensures rating_value is within the acceptable range via a CHECK constraint.
    """

    __tablename__ = "ratings"

    id = Column(Integer, primary_key=True, index=True)
    rating_value = Column(Integer, nullable=False)
    review_text = Column(String, nullable=True)
    reviewer_id = Column(Integer, ForeignKey("users.id"), nullable=True)
    timestamp = Column(DateTime, default=datetime.utcnow)

    __table_args__ = (
        CheckConstraint('rating_value >= 1 AND rating_value <= 5', name='ck_rating_value_range'),
    )

    reviewer = relationship("User", back_populates="ratings", lazy="joined", uselist=False)


class ReviewBase(BaseModel):
    """
    Pydantic base class for reviews.
    Defines shared fields and validation logic.
    """

    title: str = Field(..., description="Title of the review.")
    content: Optional[str] = Field(None, description="Main text of the review.")


class ReviewCreate(ReviewBase):
    """
    Pydantic model for creating a new review.
    Extends ReviewBase with additional fields needed at creation.
    """

    reviewer_id: Optional[int] = Field(
        None,
        description="Identifier for the user posting the review."
    )


class ReviewInDB(ReviewBase):
    """
    Pydantic model representing a review as stored in the database.
    Extends ReviewBase with ID and timestamp.
    """

    id: int
    timestamp: datetime


class ReviewORM(Base):
    """
    SQLAlchemy ORM model for reviews.
    Maps Python objects to database records in the 'reviews' table.
    Provides a reference to the reviewer (User) if such a relationship exists.
    """

    __tablename__ = "reviews"

    id = Column(Integer, primary_key=True, index=True)
    title = Column(String, nullable=False)
    content = Column(String, nullable=True)
    reviewer_id = Column(Integer, ForeignKey("users.id"), nullable=True)
    timestamp = Column(DateTime, default=datetime.utcnow)

    reviewer = relationship("User", back_populates="reviews", lazy="joined", uselist=False)