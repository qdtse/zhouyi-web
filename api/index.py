import sys
import os

# Add the current directory to sys.path
sys.path.append(os.path.dirname(__file__))

# Import app directly from server module
# Note: In Vercel serverless environment, we need to expose 'app' as a variable
try:
    from server import app
except ImportError:
    # Fallback for Vercel's unique import structure if needed
    from .server import app
