import os
import sys

# Vercel entry point
# Manually add the current directory to path
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

# Import the FastAPI app
try:
    from server import app
except ImportError:
    # Fallback to relative import if sys.path trick fails
    from .server import app

# Wrap with Mangum for Vercel serverless compatibility
try:
    from mangum import Mangum
    handler = Mangum(app)
except ImportError:
    # Fallback if mangum is not installed
    # Vercel should handle this but raise clear error
    raise ImportError(
        "Mangum is required for Vercel deployment. "
        "Please ensure 'mangum>=0.17.0' is in requirements.txt"
    )
