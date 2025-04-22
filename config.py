import os
import logging
from typing import Optional, Dict, Any
from dotenv import load_dotenv

logger = logging.getLogger(__name__)

def load_config() -> Dict[str, Any]:
    """
    Reads environment variables or a .env file for application configuration.
    It also logs whether the application is running in a production or
    non-production environment based on the APP_ENV variable.

    Returns:
        Dict[str, Any]: Dictionary containing configuration values from environment variables

    Raises:
        Exception: If an error occurs during loading of environment variables.
    """
    try:
        # Load environment variables from a .env file if present
        load_dotenv()

        # Determine current environment (default: development)
        environment = os.getenv("APP_ENV", "development").lower()

        if environment == "production":
            logger.info("Production environment detected. Make sure environment variables are set.")
        else:
            logger.info("Non-production environment detected. .env file loaded if present.")

        logger.info("Configuration successfully loaded for environment: %s", environment)

        # Get all environment variables and return as a dict
        config_dict = {key: value for key, value in os.environ.items()}
        
        # Add any default configuration if needed
        if "SOME_OTHER_CONFIG" not in config_dict and os.getenv("SOME_OTHER_CONFIG"):
            config_dict["SOME_OTHER_CONFIG"] = os.getenv("SOME_OTHER_CONFIG")

        return config_dict

    except Exception as e:
        logger.error("Failed to load configuration: %s", e)
        raise

def get_database_url() -> str:
    """
    Returns a valid SQLAlchemy database URL based on environment variables.

    Raises:
        ValueError: If the DATABASE_URL environment variable is not set.

    Returns:
        str: The database URL.
    """
    database_url = os.getenv("DATABASE_URL")
    if not database_url:
        raise ValueError("DATABASE_URL is not set in the environment.")
    return database_url