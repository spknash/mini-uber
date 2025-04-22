from typing import Optional, Dict, Any

from pydantic import BaseModel, Field
from sqlalchemy import Column, String, Integer, ForeignKey, JSON
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship

Base = declarative_base()


class Driver(Base):
    """
    SQLAlchemy model representing a driver in the system.
    Includes name, license number, and optional phone number
    for contact.
    """
    __tablename__ = "drivers"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(100), nullable=False)
    license_number = Column(String(20), unique=True, index=True, nullable=False)
    phone_number = Column(String(20), nullable=True)
    vehicle_info = Column(JSON, nullable=True)

    vehicles = relationship("Vehicle", back_populates="driver")


class Vehicle(Base):
    """
    SQLAlchemy model representing a vehicle associated with a driver.
    Includes information such as make, model, year, and VIN.
    """
    __tablename__ = "vehicles"

    id = Column(Integer, primary_key=True, index=True)
    driver_id = Column(Integer, ForeignKey("drivers.id"), nullable=False)
    make = Column(String, nullable=False)
    model = Column(String, nullable=False)
    year = Column(Integer, nullable=False)
    vin = Column(String(17), unique=True, index=True, nullable=True)

    driver = relationship("Driver", back_populates="vehicles")


class DriverBase(BaseModel):
    """
    Pydantic model for driver data validation.
    """
    name: str = Field(..., description="The name of the driver")
    license_number: str = Field(..., description="The license number of the driver")


class DriverCreate(DriverBase):
    """
    Pydantic model for creating a new driver entry.
    """
    vehicle_info: Optional[Dict[str, Any]] = Field(None, description="The vehicle information")


class DriverUpdate(BaseModel):
    """
    Pydantic model for updating an existing driver entry.
    Fields are optional to allow partial updates.
    """
    name: Optional[str] = Field(None, description="The name of the driver")
    license_number: Optional[str] = Field(None, description="The license number of the driver")
    phone_number: Optional[str] = Field(None, description="The phone number of the driver, if available")
    vehicle_info: Optional[Dict[str, Any]] = Field(None, description="The vehicle information")


class DriverInDB(DriverBase):
    """
    Pydantic model for representing a driver entry in the database.
    """
    id: int = Field(..., description="The unique identifier of the driver")
    vehicle_info: Optional[Dict[str, Any]] = Field(None, description="The vehicle information")

    class Config:
        orm_mode = True


class VehicleBase(BaseModel):
    """
    Pydantic model for vehicle data validation.
    """
    make: str = Field(..., description="The make of the vehicle")
    model: str = Field(..., description="The model of the vehicle")
    year: int = Field(..., description="The year of the vehicle")


class VehicleCreate(VehicleBase):
    """
    Pydantic model for creating a new vehicle entry.
    """
    pass


class VehicleUpdate(BaseModel):
    """
    Pydantic model for updating an existing vehicle entry.
    Fields are optional to allow partial updates.
    """
    make: Optional[str] = Field(None, description="The make of the vehicle")
    model: Optional[str] = Field(None, description="The model of the vehicle")
    year: Optional[int] = Field(None, description="The year of the vehicle")
    vin: Optional[str] = Field(None, description="The vehicle identification number (VIN)")


class VehicleInDB(VehicleBase):
    """
    Pydantic model for representing a vehicle entry in the database.
    """
    id: int = Field(..., description="The unique identifier of the vehicle")
    driver_id: int = Field(..., description="The unique identifier of the driver owning the vehicle")

    class Config:
        orm_mode = True