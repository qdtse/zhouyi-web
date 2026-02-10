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
from mangum import Mangum

# Create handler class for Vercel
class Handler(Mangum):
    def __init__(self):
        super().__init__(app, api_gateway_base_path="/api")

# Vercel expects a class named 'handler'
handler = Handler
