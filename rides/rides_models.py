from datetime import datetime
from enum import Enum as PyEnum
from typing import Optional, Dict, Any

import logging
from pydantic import BaseModel, Field, ValidationError, validator
from sqlalchemy import Column, DateTime, Enum, Integer, String, ForeignKey
from sqlalchemy.ext.declarative import declarative_base

logger = logging.getLogger(__name__)

Base = declarative_base()


class RideStatus(PyEnum):
    """
    Enum for indicating the ride status.
    """
    PENDING = "PENDING"
    IN_PROGRESS = "IN_PROGRESS"
    COMPLETED = "COMPLETED"
    CANCELLED = "CANCELLED"


class Ride(Base):
    """
    SQLAlchemy model for ride data, storing information about ride locations,
    status, and timestamps.
    
    This includes:
     - A passenger_id foreign key for referencing a user (if a 'users' table exists).
     - Automatic 'updated_at' timestamp updates on changes.
     - Indexed columns for potential performance improvements.
    """
    __tablename__ = "rides"

    id = Column(Integer, primary_key=True, index=True)
    start_location = Column(String, nullable=False, index=True)
    end_location = Column(String, nullable=False, index=True)
    status = Column(Enum(RideStatus), nullable=False, default=RideStatus.PENDING)
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    passenger_id = Column(
        Integer,
        ForeignKey("users.id", ondelete="SET NULL"),
        nullable=True,
        index=True
    )


class RideBaseModel(BaseModel):
    """
    Base Pydantic model for shared ride fields and validation.
    """
    start_location: str = Field(..., description="Starting point of the ride.")
    end_location: str = Field(..., description="Destination point of the ride.")
    status: RideStatus = Field(RideStatus.PENDING, description="Current status of the ride.")

    class Config:
        use_enum_values = True
        extra = "forbid"
        error_msg_templates = {
            "value_error.enum": "Invalid status value provided."
        }


class RideCreateModel(RideBaseModel):
    """
    Pydantic model used when creating a new ride.
    
    Includes an additional field for passenger_id with validation.
    """
    passenger_id: int = Field(..., description="ID of the passenger creating the ride.")

    @validator("passenger_id")
    def passenger_id_positive(cls, value: int) -> int:
        """
        Ensure that the passenger_id is a positive integer.
        """
        if value <= 0:
            raise ValueError("passenger_id must be a positive integer.")
        return value


class RideUpdateModel(BaseModel):
    """
    Pydantic model used for updating ride data, with optional fields.
    """
    start_location: Optional[str]
    end_location: Optional[str]
    status: Optional[RideStatus]

    class Config:
        use_enum_values = True
        extra = "forbid"


class RideReadModel(RideBaseModel):
    """
    Pydantic model for reading ride data from the database.
    """
    id: int
    created_at: datetime
    updated_at: datetime

    class Config:
        orm_mode = True


def handle_model_error(data: Dict[str, Any]) -> Optional[RideBaseModel]:
    """
    Demonstrates error handling while parsing data into a RideBaseModel.

    :param data: A dictionary containing ride fields.
    :return: A valid RideBaseModel instance or None if validation fails.
    """
    try:
        return RideBaseModel(**data)
    except ValidationError as e:
        # Log validation errors for debugging and return None.
        logger.error(f"Validation error: {e}")
        return None
    # In a real application, consider raising custom exceptions or returning
    # structured error messages to the application layer.