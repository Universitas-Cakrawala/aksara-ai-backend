from decouple import config
import logging
from pymongo import MongoClient
from pymongo.errors import ConnectionFailure, ConfigurationError

# Configure logging
logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)

# Retrieve MongoDB URI from environment variables
MONGO_URI = config("MONGO_URI")


# Initialize MongoDB client
def mongdb_client():
    try:
        client = MongoClient(MONGO_URI)
        # Test the connection
        client.admin.command("ping")
        logger.debug("Connected to MongoDB successfully.")
        return client
    except (ConnectionFailure, ConfigurationError) as e:
        logger.critical(f"MongoDB connection failure: {e}")
        return None
    except Exception as e:
        logger.critical(f"An unexpected error occurred: {e}")
        return None
