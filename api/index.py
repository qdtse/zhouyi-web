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

# Create handler instance - Vercel expects a callable
handler = Mangum(app, lifespan="off")
