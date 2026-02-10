import os
import sys
import traceback

# Vercel entry point
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

# Import the FastAPI app with error handling
try:
    from server import app
except ImportError as e:
    error_msg = f"Failed to import app: {str(e)}\n{traceback.format_exc()}"
    # Create a minimal app that returns the error
    from fastapi import FastAPI
    app = FastAPI()
    
    @app.get("/")
    @app.get("/{path:path}")
    async def error_handler(path: str = ""):
        return {"error": error_msg}

# Wrap with Mangum for Vercel serverless compatibility
try:
    from mangum import Mangum
    handler = Mangum(app, lifespan="off")
except ImportError as e:
    # Fallback if mangum is not available
    def handler(event, context):
        return {
            "statusCode": 500,
            "body": f"Mangum import error: {str(e)}"
        }
