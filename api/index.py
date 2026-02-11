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

# Vercel expects handler to be a class that can be instantiated
# Mangum returns a callable that wraps the ASGI app
class Handler:
    def __init__(self):
        self.mangum = Mangum(app, lifespan="off")
    
    def __call__(self, event, context):
        return self.mangum(event, context)

# Export handler class for Vercel
handler = Handler
