from typing import Optional
from pydantic import BaseModel, Field, EmailStr
from sqlalchemy import Column, Integer, String, Boolean
from sqlalchemy.orm import declarative_base

Base = declarative_base()


class Rider(Base):
    """
    SQLAlchemy model for the riders table.
    """
    __tablename__ = "riders"

    id = Column(Integer, primary_key=True, index=True)
    first_name = Column(String(50), nullable=False)
    last_name = Column(String(50), nullable=False)
    email = Column(String(255), unique=True, index=True, nullable=False)
    phone_number = Column(String(20), unique=True, index=True, nullable=True)
    is_active = Column(Boolean, default=True)


class RiderBase(BaseModel):
    """
    Shared base model for rider data.
    """
    first_name: str = Field(..., max_length=50)
    last_name: str = Field(..., max_length=50)
    email: EmailStr
    phone_number: Optional[str] = None
    is_active: bool = True


class RiderCreate(RiderBase):
    """
    Model for creating a new rider.
    Currently no additional fields are required beyond RiderBase.
    """
    pass


class RiderUpdate(RiderBase):
    """
    Model for updating rider data.
    All fields are optional here to allow partial updates.
    """
    first_name: Optional[str] = Field(None, max_length=50)
    last_name: Optional[str] = Field(None, max_length=50)
    email: Optional[EmailStr] = None
    phone_number: Optional[str] = None
    is_active: Optional[bool] = None


class RiderInDB(RiderBase):
    """
    Model representing rider data stored in the database.
    """
    id: int

    class Config:
        from_attributes = True
        populate_by_name = True