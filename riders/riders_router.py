from fastapi import APIRouter, HTTPException, status, Depends
from pydantic import BaseModel
from typing import Optional
from riders.riders_service import create_rider, fetch_rider

router = APIRouter()

# In-memory storage for demonstration purposes.
# In a production environment, you would replace this with a database.
riders_db = {}
rider_id_counter = 1


class RiderCreateRequest(BaseModel):
    """
    Schema for creating a new rider.
    """
    name: str
    phone_number: str
    payment_method: str


@router.post("/riders", status_code=status.HTTP_201_CREATED)
def create_rider_endpoint(request_data: RiderCreateRequest) -> dict:
    """
    Registers a new rider account.

    :param request_data: Rider creation details.
    :return: Rider details including the new rider's ID.

    Raises:
        HTTPException: If any validation errors occur.
    """
    try:
        # Call the service function to create a rider
        rider = create_rider(
            name=request_data.name,
            phone_number=request_data.phone_number,
            payment_method=request_data.payment_method
        )
        return rider
    except ValueError as exc:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(exc)
        )
    except Exception as exc:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error occurred while creating rider: {exc}"
        )


@router.get("/riders/{rider_id}", status_code=status.HTTP_200_OK)
def get_rider_profile_endpoint(rider_id: int) -> dict:
    """
    Fetches a rider's profile details.

    :param rider_id: Unique rider ID.
    :return: Rider profile information.

    Raises:
        HTTPException: If the rider does not exist or any other error occurs.
    """
    try:
        rider = fetch_rider(rider_id=rider_id)
        if rider is None:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"Rider with ID {rider_id} not found."
            )
        return rider
    except HTTPException:
        # Propagate HTTPExceptions as they are
        raise
    except Exception as exc:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error retrieving rider: {exc}"
        )