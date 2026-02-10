import os
import sys
import logging

# Configure logging for debugging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Vercel entry point
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

# Import the FastAPI app
try:
    from server import app
    logger.info("Successfully imported app from server")
except ImportError as e:
    logger.error(f"Failed to import from server: {e}")
    try:
        from .server import app
        logger.info("Successfully imported app from .server")
    except ImportError as e2:
        logger.error(f"Failed to import from .server: {e2}")
        raise

# Wrap with Mangum for Vercel serverless compatibility
from mangum import Mangum

# Create handler with proper configuration for Vercel
# lifespan="off" prevents issues with startup/shutdown events in serverless
handler = Mangum(
    app,
    lifespan="off",
    api_gateway_base_path=None  # Let Vercel handle the base path
)

logger.info("Handler created successfully")
