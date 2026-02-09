import sys
import os
import traceback

# Add the current directory to sys.path
current_dir = os.path.dirname(os.path.abspath(__file__))
if current_dir not in sys.path:
    sys.path.insert(0, current_dir)

# Try to import and provide detailed error info
error_details = []

try:
    from fastapi import FastAPI
    from fastapi.responses import JSONResponse
    error_details.append("✓ FastAPI imported")
except Exception as e:
    error_details.append(f"✗ FastAPI import failed: {str(e)}")

try:
    from mangum import Mangum
    error_details.append("✓ Mangum imported")
except Exception as e:
    error_details.append(f"✗ Mangum import failed: {str(e)}")

try:
    from server import app
    error_details.append("✓ Server module imported")
    
    # Wrap with Mangum
    handler = Mangum(app, lifespan="off")
    error_details.append("✓ Handler created successfully")
    
except Exception as e:
    error_details.append(f"✗ Server import failed: {str(e)}")
    error_details.append(f"Traceback: {traceback.format_exc()}")
    
    # Create fallback app
    from fastapi import FastAPI
    from fastapi.responses import JSONResponse
    from mangum import Mangum
    
    app = FastAPI()
    
    @app.get("/api/{path:path}")
    @app.post("/api/{path:path}")
    async def error_handler(path: str):
        return JSONResponse(
            status_code=500,
            content={
                "error": "Server initialization failed",
                "details": error_details,
                "path": path,
                "python_version": sys.version,
                "cwd": os.getcwd(),
                "sys_path": sys.path[:3]
            }
        )
    
    handler = Mangum(app, lifespan="off")
