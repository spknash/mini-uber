import logging
from typing import Dict, Any, Optional, Union

logger = logging.getLogger(__name__)
logging.basicConfig(level=logging.INFO)

# In production, replace this dictionary with a persistent database solution.
DRIVERS_DB: Dict[int, Dict[str, Any]] = {}
CURRENT_ID = 1

# Create a driver class that matches expectations in tests
class DriverObject:
    def __init__(self, id: int, name: str, license_number: str, vehicle_info: Dict[str, Any]):
        self.id = id
        self.name = name
        self.license_number = license_number
        self.vehicle_info = vehicle_info

def _verify_license_number(license_number: str) -> bool:
    """
    Verifies the format of the driver's license number.

    :param license_number: The license number to verify.
    :return: True if the license number is valid, False otherwise.
    """
    # For demonstration, ensure the license has at least 5 alphanumeric characters.
    # In a real-world scenario, implement more complex checks or external validation as needed.
    return len(license_number) >= 5 and license_number.isalnum()

def create_driver(name: str, license_number: str, vehicle_info: Dict[str, Any]) -> DriverObject:
    """
    Persists a new driver record.

    Creates a new driver record with the provided name, license number,
    and vehicle information.

    :param name: The name of the driver.
    :param license_number: The driver's license number.
    :param vehicle_info: Dictionary containing vehicle information.
    :return: A DriverObject representing the newly created driver.
    :raises ValueError: If the provided license number is invalid or name is empty.
    """
    if not name:
        raise ValueError("Driver name cannot be empty.")
    if not license_number:
        raise ValueError("Invalid license: license number cannot be empty.")

    # Validate license number format
    if not _verify_license_number(license_number):
        raise ValueError("Invalid license: license number format is incorrect.")

    global CURRENT_ID

    logger.info("Creating driver entry in the database.")
    driver_id = CURRENT_ID
    DRIVERS_DB[driver_id] = {
        "name": name,
        "license_number": license_number,
        "vehicle_info": vehicle_info,
    }
    CURRENT_ID += 1
    logger.info("Driver created successfully with ID %s.", driver_id)

    return DriverObject(driver_id, name, license_number, vehicle_info)

def update_vehicle_details(driver_id: int, vehicle_info: Dict[str, Any]) -> Optional[DriverObject]:
    """
    Updates the driver's vehicle data.

    Updates the vehicle information of an existing driver record.

    :param driver_id: The unique identifier of the driver.
    :param vehicle_info: Dictionary containing vehicle information to update.
    :return: A DriverObject representing the updated driver, or None if driver not found.
    """
    logger.info("Updating vehicle details for driver with ID %s.", driver_id)

    if driver_id not in DRIVERS_DB:
        logger.error("Driver with ID %s does not exist.", driver_id)
        return None  # Return None instead of raising an exception

    DRIVERS_DB[driver_id]["vehicle_info"] = vehicle_info
    logger.info("Vehicle details updated for driver with ID %s.", driver_id)
    
    # Return a DriverObject with the updated data
    driver_data = DRIVERS_DB[driver_id]
    return DriverObject(
        id=driver_id,
        name=driver_data["name"],
        license_number=driver_data["license_number"],
        vehicle_info=vehicle_info
    )

# For testing purposes, expose the Driver class to mimic the models
Driver = DriverObject