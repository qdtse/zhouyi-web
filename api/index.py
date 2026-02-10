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
