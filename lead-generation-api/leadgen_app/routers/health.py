"""
Health check endpoints
"""

import logging
from datetime import datetime
from fastapi import APIRouter, HTTPException
from leadgen_app.models.response_models import HealthResponse
from leadgen_app.config import settings
from leadgen_app.services.supabase_service import get_supabase_service

logger = logging.getLogger(__name__)
router = APIRouter()

@router.get(
    "/",
    response_model=HealthResponse,
    summary="Basic health check",
    description="Check if the service is running"
)
async def health_check():
    """
    Basic health check endpoint
    """
    return HealthResponse(
        status="healthy",
        timestamp=datetime.utcnow(),
        version=settings.VERSION,
        dependencies={"status": "not_checked"}
    )

@router.get(
    "/detailed",
    response_model=HealthResponse,
    summary="Detailed health check",
    description="Check service health including dependencies"
)
async def detailed_health_check():
    """
    Detailed health check including dependencies
    """
    dependencies = {}
    overall_status = "healthy"
    
    # Check Supabase connection
    try:
        # Try a simple query to test database connectivity
        test_result = await supabase_service.get_user_lead_count("health-check-user")
        dependencies["supabase"] = "healthy"
    except Exception as e:
        logger.warning(f"Supabase health check failed: {str(e)}")
        dependencies["supabase"] = "unhealthy"
        overall_status = "degraded"
    
    # Check AI services
    ai_services = []
    if settings.OPENAI_API_KEY:
        ai_services.append("openai")
    if settings.ANTHROPIC_API_KEY:
        ai_services.append("anthropic")
    
    dependencies["ai_services"] = "configured" if ai_services else "not_configured"
    
    # Check enrichment services
    enrichment_services = []
    if settings.APOLLO_API_KEY:
        enrichment_services.append("apollo")
    if settings.HUNTER_API_KEY:
        enrichment_services.append("hunter")
    if settings.CLEARBIT_API_KEY:
        enrichment_services.append("clearbit")
    
    dependencies["enrichment_services"] = "configured" if enrichment_services else "not_configured"
    
    return HealthResponse(
        status=overall_status,
        timestamp=datetime.utcnow(),
        version=settings.VERSION,
        dependencies=dependencies
    )

@router.get(
    "/ready",
    summary="Readiness check",
    description="Check if service is ready to handle requests"
)
async def readiness_check():
    """
    Kubernetes readiness probe endpoint
    """
    try:
        # Test critical dependencies
        await supabase_service.get_user_lead_count("readiness-check")
        
        return {"status": "ready", "timestamp": datetime.utcnow()}
        
    except Exception as e:
        logger.error(f"Readiness check failed: {str(e)}")
        raise HTTPException(status_code=503, detail="Service not ready")

@router.get(
    "/live",
    summary="Liveness check", 
    description="Check if service is alive"
)
async def liveness_check():
    """
    Kubernetes liveness probe endpoint
    """
    return {"status": "alive", "timestamp": datetime.utcnow()}