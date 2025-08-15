"""
FastAPI Lead Generation Service
Replaces n8n workflow for AI-powered lead discovery
"""

import logging
from contextlib import asynccontextmanager
from fastapi import FastAPI, Depends, Request, status
from fastapi.exceptions import RequestValidationError
from fastapi.middleware.cors import CORSMiddleware
from fastapi.middleware.trustedhost import TrustedHostMiddleware
from fastapi.responses import JSONResponse
import uvicorn
import json

from leadgen_app.config import settings
from leadgen_app.routers import leads, health
from leadgen_app.services.auth_service import verify_jwt_token
from leadgen_app.utils.logger import setup_logging

# Setup logging
setup_logging()
logger = logging.getLogger(__name__)

@asynccontextmanager
async def lifespan(app: FastAPI):
    """Application lifespan events"""
    logger.info("🚀 Lead Generation API starting up...")
    yield
    logger.info("🛑 Lead Generation API shutting down...")

# Initialize FastAPI app
app = FastAPI(
    title="Lead Generation AI Service",
    description="AI-powered lead discovery and enrichment service",
    version="1.0.0",
    docs_url="/docs" if settings.ENVIRONMENT == "development" else None,
    redoc_url="/redoc" if settings.ENVIRONMENT == "development" else None,
    lifespan=lifespan
)

# --- START ENHANCED VALIDATION LOGGING ---
@app.exception_handler(RequestValidationError)
async def validation_exception_handler(request: Request, exc: RequestValidationError):
    """
    Log detailed validation errors to the server console.
    """
    # Log the full error details
    logger.error(f"Validation error for request to {request.url}:")
    try:
        # The `exc.errors()` method provides a structured list of validation errors
        error_details = exc.errors()
        logger.error(json.dumps(error_details, indent=2))
    except Exception:
        # Fallback for unexpected error structures
        logger.error(str(exc))
        
    # Return the default 422 response to the client
    return JSONResponse(
        status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
        content={"detail": exc.errors()},
    )
# --- END ENHANCED VALIDATION LOGGING ---

# Middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.ALLOWED_ORIGINS,
    allow_credentials=True,
    allow_methods=["GET", "POST", "PUT", "DELETE"],
    allow_headers=["*"],
)

app.add_middleware(
    TrustedHostMiddleware,
    allowed_hosts=settings.ALLOWED_HOSTS
)

# Global exception handler
@app.exception_handler(Exception)
async def global_exception_handler(request: Request, exc: Exception):
    logger.error(f"Global exception: {str(exc)}", exc_info=True)
    return JSONResponse(
        status_code=500,
        content={
            "error": "Internal server error",
            "message": "An unexpected error occurred"
        }
    )

# Include routers
app.include_router(health.router, prefix="/health", tags=["health"])
app.include_router(
    leads.router, 
    prefix="/api/v1/leads", 
    tags=["leads"],
    dependencies=[Depends(verify_jwt_token)]
)

@app.get("/")
async def root():
    """Root endpoint"""
    return {
        "service": "Lead Generation AI",
        "version": "1.0.0",
        "status": "operational",
        "docs": "/docs" if settings.ENVIRONMENT == "development" else "disabled"
    }

if __name__ == "__main__":
    uvicorn.run(
        "app.main:app",
        host="0.0.0.0",
        port=settings.PORT,
        reload=settings.ENVIRONMENT == "development",
        log_level=settings.LOG_LEVEL.lower()
    )
