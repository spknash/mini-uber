import logging
from typing import Any, Dict

logger = logging.getLogger(__name__)

# Mock external payment API for testing
class some_external_payment_api:
    @staticmethod
    def charge(rider_id: Any, amount: float) -> Dict[str, Any]:
        """
        Mock function for charge API
        """
        return {
            "status": "success",
            "transaction_id": "mock_transaction_123"
        }

# Mock external payout API for testing
class some_external_payout_api:
    @staticmethod
    def process_payout(driver_id: Any, amount: float) -> Dict[str, Any]:
        """
        Mock function for payout API
        """
        return {
            "status": "success",
            "payout_id": "mock_payout_123"
        }

class PaymentServiceError(Exception):
    """
    Custom exception for payment service errors.
    """
    pass


def calculate_fare(pickup_location: Any, dropoff_location: Any, duration: float, distance: float) -> float:
    """
    Calculate the fare based on pickup/dropoff locations, trip duration, and distance.
    This includes a base fare, cost per kilometer, and cost per minute. Additional
    surcharges can be applied for longer distances or durations as a simple
    demonstration of dynamic pricing.

    :param pickup_location: The pickup location, can be an address or coordinate.
    :param dropoff_location: The dropoff location, can be an address or coordinate.
    :param duration: The total trip duration in minutes.
    :param distance: The total trip distance in kilometers.
    :return: The calculated fare as a float.
    :raises ValueError: If distance is negative.
    """
    base_fare = 2.00
    cost_per_km = 1.25
    cost_per_min = 0.25

    # Check for negative distance
    if distance < 0:
        raise ValueError("Distance cannot be negative")

    # Example dynamic factors
    distance_surcharge_threshold = 20  # kilometers
    duration_surcharge_threshold = 30  # minutes
    distance_surcharge_amount = 2.0
    duration_surcharge_amount = 1.0

    try:
        fare = base_fare + (cost_per_km * distance) + (cost_per_min * duration)

        # Simple surcharges for demonstration
        if distance > distance_surcharge_threshold:
            fare += distance_surcharge_amount
        if duration > duration_surcharge_threshold:
            fare += duration_surcharge_amount

        return round(fare, 2)
    except Exception as e:
        logger.error("Error calculating fare: %s", e)
        raise PaymentServiceError("Failed to calculate fare") from e


def charge_rider(rider_id: Any, amount: float) -> Dict[str, Any]:
    """
    Charge the rider's payment method or simulate the charge.

    :param rider_id: Unique identifier of the rider.
    :param amount: The amount to be charged.
    :return: Dictionary containing transaction details.
    :raises Exception: Propagates any exceptions from the payment service.
    """
    try:
        # In a real-world scenario, this would integrate with a payment gateway.
        # Here, we use the mock external payment API
        logger.info("Charging rider %s an amount of %.2f", rider_id, amount)
        result = some_external_payment_api.charge(rider_id, amount)
        return result
    except Exception as e:
        # Log the error but re-raise the original exception for test compatibility
        logger.error("Error charging rider: %s", e)
        raise e


def payout_driver(driver_id: Any, amount: float) -> Dict[str, Any]:
    """
    Process a payout to the driver.

    :param driver_id: Unique identifier of the driver.
    :param amount: The amount to be paid out.
    :return: Dictionary containing payout details.
    :raises Exception: Propagates any exceptions from the payout service.
    """
    try:
        # In a real-world scenario, this would integrate with a payout system (e.g., a bank API).
        # Here, we use the mock external payout API
        logger.info("Processing payout of %.2f to driver %s", amount, driver_id)
        result = some_external_payout_api.process_payout(driver_id, amount)
        return result
    except Exception as e:
        # Log the error but re-raise the original exception for test compatibility
        logger.error("Error processing driver payout: %s", e)
        raise e


__all__ = [
    "PaymentServiceError",
    "calculate_fare",
    "charge_rider",
    "payout_driver",
    "some_external_payment_api",
    "some_external_payout_api"
]