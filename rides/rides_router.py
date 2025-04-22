from fastapi import APIRouter, HTTPException, status as http_status
from pydantic import BaseModel
from typing import Optional, Dict, Any

router = APIRouter(tags=["rides"])

# In-memory storage for rides (for demonstration purposes only).
# In a real-world application, replace this with a proper database integration.
rides_db: Dict[int, Dict[str, Any]] = {}
current_ride_id = 0


class RideRequest(BaseModel):
    """
    Data model for ride request containing pickup and drop-off locations.
    """
    pickup: Optional[str] = None
    dropoff: Optional[str] = None
    additional_info: Optional[str] = None


class RideStatusUpdate(BaseModel):
    """
    Data model for ride status update.
    """
    status: str


def get_next_ride_id() -> int:
    """
    Retrieves the next ride ID in a thread-unsafe manner.
    For production, ensure thread safety or use a DB auto-increment.
    """
    global current_ride_id
    current_ride_id += 1
    return current_ride_id


def find_available_driver() -> Optional[str]:
    """
    Placeholder logic to find an available driver.
    In a real implementation, there would be a more complex search/dispatch system.
    Returns a driver ID if available, otherwise None.
    """
    # In a real scenario, we'd check for the nearest/available driver.
    # For demonstration, we return a mock driver_id.
    return "driver_123"


@router.post("/rides/request_ride")
async def request_ride_endpoint(request_data: RideRequest):
    """
    Creates a new ride request using the provided pickup and drop-off locations.

    :param request_data: Contains pickup, dropoff, and optional additional info.
    :return: JSON response containing ride details or an error if creation fails.
    """
    try:
        # Generate a new ride ID
        ride_id = get_next_ride_id()

        # Default values if not provided
        pickup = request_data.pickup or "Default pickup location"
        dropoff = request_data.dropoff or "Default dropoff location"

        # Attempt to find an available driver
        driver_id = find_available_driver()
        if not driver_id:
            raise HTTPException(
                status_code=http_status.HTTP_503_SERVICE_UNAVAILABLE,
                detail="No drivers currently available."
            )

        # Store ride details in an in-memory database
        rides_db[ride_id] = {
            "ride_id": ride_id,
            "pickup": pickup,
            "dropoff": dropoff,
            "status": "pending",
            "driver_id": driver_id,
            "additional_info": request_data.additional_info
        }

        return {
            "message": "Ride requested successfully.",
            "ride_id": ride_id,
            "pickup": pickup,
            "dropoff": dropoff,
            "status": "pending",
            "driver_id": driver_id
        }
    except HTTPException:
        # Just re-raise the already created HTTPException
        raise
    except Exception as e:
        # Log error and raise an HTTPException
        raise HTTPException(
            status_code=http_status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=str(e)
        )


@router.put("/rides/{ride_id}/status")
async def update_ride_status_endpoint(ride_id: int, ride_status: RideStatusUpdate):
    """
    Updates the status of an existing ride.

    :param ride_id: The unique identifier of the ride to update.
    :param ride_status: The new status for the ride (accepted, started, completed, etc.).
    :return: JSON response indicating success or an error if update fails.
    """
    try:
        if ride_id not in rides_db:
            raise HTTPException(
                status_code=http_status.HTTP_404_NOT_FOUND,
                detail=f"Ride with ID {ride_id} not found."
            )

        # Update the status of the ride
        new_status = ride_status.status
        rides_db[ride_id]["status"] = new_status

        return {
            "message": "Ride status updated successfully.",
            "ride_id": ride_id,
            "new_status": new_status
        }
    except HTTPException:
        # Re-raise HTTPException for proper error response
        raise
    except Exception as e:
        # Log error and raise an HTTPException
        raise HTTPException(
            status_code=http_status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=str(e)
        )


@router.get("/rides/{ride_id}")
async def get_ride_details_endpoint(ride_id: int):
    """
    Retrieves details of a specific ride.

    :param ride_id: The unique identifier of the ride.
    :return: Ride details or an error if not found.
    """
    try:
        if ride_id not in rides_db:
            raise HTTPException(
                status_code=http_status.HTTP_404_NOT_FOUND,
                detail=f"Ride with ID {ride_id} not found."
            )

        return rides_db[ride_id]
    except HTTPException:
        # Re-raise to propagate 404 or other HTTP errors
        raise
    except Exception as e:
        # Log error and raise an HTTPException
        raise HTTPException(
            status_code=http_status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=str(e)
        )