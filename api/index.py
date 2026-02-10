import os
import sys

# Vercel entry point
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

# Import the FastAPI app
try:
    from server import app
except ImportError:
    from .server import app

# Wrap with Mangum for Vercel serverless compatibility
from mangum import Mangum

# Create a callable handler for Vercel
# Vercel Python runtime expects a handler that can be called with (event, context)
def handler(event, context):
    """Vercel serverless handler"""
    mangum_handler = Mangum(app, lifespan="off")
    return mangum_handler(event, context)
