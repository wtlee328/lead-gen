"""
FastAPI Lead Generation Service
Replaces n8n workflow for AI-powered lead discovery
"""

from fastapi import FastAPI, HTTPException, Depends, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.middleware.trustedhost import TrustedHostMiddleware
from fastapi.responses import JSONResponse
import uvicorn
import logging
from contextlib import asynccontextmanager

from leadgen_app.config import settings
from leadgen_app.routers import leads, health
from leadgen_app.utils.logger import setup_logging
from leadgen_app.services.auth_service import verify_jwt_token

# Setup logging
setup_logging()
logger = logging.getLogger(__name__)

@asynccontextmanager
async def lifespan(app: FastAPI):
    """Application lifespan events"""
    logger.info("🚀 Lead Generation API starting up...")
    logger.info(f"Environment: {settings.ENVIRONMENT}")
    logger.info(f"Port: {settings.PORT}")
    logger.info(f"Supabase URL configured: {bool(settings.SUPABASE_URL and settings.SUPABASE_URL != 'https://example.supabase.co')}")
    logger.info(f"OpenAI API Key configured: {bool(settings.OPENAI_API_KEY)}")
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