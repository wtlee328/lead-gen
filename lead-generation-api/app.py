"""
HuggingFace Spaces entry point for Lead Generation API
This file serves as the main entry point expected by HuggingFace Spaces
"""

# Import the FastAPI app from the leadgen_app package
from leadgen_app.main import app

# Export the FastAPI app instance for HuggingFace Spaces
__all__ = ["app"]