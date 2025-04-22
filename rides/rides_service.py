import logging
from typing import Dict, Any, Optional

logger = logging.getLogger(__name__)

class RideServiceError(Exception):
    """
    Custom exception for errors related to the rides service.
    """
    pass

# In-memory data store simulations
RIDES_DB = {}
AVAILABLE_DRIVERS = ["driver123", "driver456", "driver789"]
CURRENT_RIDE_ID = 0

def create_ride(rider_id: str, pickup_location: Dict[str, Any], dropoff_location: Dict[str, Any]) -> int:
    """
    Creates a new ride record.

    Args:
        rider_id (str): The unique identifier of the rider.
        pickup_location (Dict[str, Any]): The pickup location details.
        dropoff_location (Dict[str, Any]): The dropoff location details.

    Returns:
        int: The newly created ride's unique identifier.

    Raises:
        RideServiceError: If the ride cannot be created.
    """
    logger.debug("Attempting to create a new ride for rider_id=%s", rider_id)
    try:
        # Validate input
        if not rider_id or not pickup_location or not dropoff_location:
            raise ValueError("Rider ID, pickup location, and dropoff location are required.")

        global CURRENT_RIDE_ID
        CURRENT_RIDE_ID += 1
        new_ride_id = CURRENT_RIDE_ID

        # Create a new ride record in the in-memory datastore
        RIDES_DB[new_ride_id] = {
            "rider_id": rider_id,
            "pickup_location": pickup_location,
            "dropoff_location": dropoff_location,
            "status": "created",
            "driver_id": None
        }

        logger.info("Created a new ride with ID %s", new_ride_id)
        return new_ride_id
    except Exception as e:
        logger.error("Failed to create ride: %s", e)
        raise RideServiceError("Could not create a new ride") from e

def assign_driver_to_ride(ride_id: int) -> Optional[str]:
    """
    Finds an available driver and assigns them to the specified ride.

    Args:
        ride_id (int): The unique identifier of the ride.

    Returns:
        Optional[str]: The driver's unique identifier if assigned, or None if no driver was found.

    Raises:
        RideServiceError: If there is an issue assigning a driver.
    """
    logger.debug("Attempting to assign a driver to ride_id=%s", ride_id)
    try:
        if ride_id not in RIDES_DB:
            raise ValueError(f"Ride with ID {ride_id} does not exist.")

        # Retrieve ride info
        ride_info = RIDES_DB[ride_id]

        # Check if ride already has a driver assigned
        if ride_info.get("driver_id"):
            logger.info("Ride %s already has a driver assigned: %s", ride_id, ride_info["driver_id"])
            return ride_info["driver_id"]

        # Find an available driver (if any)
        if not AVAILABLE_DRIVERS:
            logger.info("No drivers available at the moment.")
            return None

        driver_id = AVAILABLE_DRIVERS.pop(0)  # Assign the first available driver
        ride_info["driver_id"] = driver_id
        ride_info["status"] = "driver_assigned"
        logger.info("Assigned driver %s to ride %s", driver_id, ride_id)
        return driver_id
    except Exception as e:
        logger.error("Failed to assign driver to ride %s: %s", ride_id, e)
        raise RideServiceError("Could not assign a driver to the ride") from e

def update_ride_status(ride_id: int, new_status: str) -> None:
    """
    Updates the lifecycle status of the specified ride.

    Possible statuses include:
    - in-progress
    - completed
    - canceled

    Args:
        ride_id (int): The unique identifier of the ride.
        new_status (str): The new status to set for the ride.

    Raises:
        RideServiceError: If the status update fails or the status is invalid.
    """
    logger.debug("Attempting to update ride_id=%s to status=%s", ride_id, new_status)
    try:
        if ride_id not in RIDES_DB:
            raise ValueError(f"Ride with ID {ride_id} does not exist.")

        allowed_statuses = ["in-progress", "completed", "canceled"]
        if new_status not in allowed_statuses:
            raise ValueError(f"Invalid status: {new_status}")

        RIDES_DB[ride_id]["status"] = new_status
        logger.info("Ride %s status updated to %s", ride_id, new_status)
    except Exception as e:
        logger.error("Failed to update ride status for ride %s: %s", ride_id, e)
        raise RideServiceError("Could not update the ride status") from e