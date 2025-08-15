"""
Lead generation API routes - n8n workflow replication
"""

import logging
import uuid
from typing import Dict, Any
from fastapi import APIRouter, HTTPException, Depends, BackgroundTasks, status
from fastapi.responses import JSONResponse

from leadgen_app.models.request_models import LeadSearchRequest, LeadEnrichmentRequest, BulkLeadRequest
from leadgen_app.models.response_models import (
    LeadSearchResponse, 
    ErrorResponse, 
    EnrichmentResponse,
    BulkOperationResponse
)
from leadgen_app.services.auth_service import require_authenticated_user, get_current_user
from leadgen_app.services.ai_service import ai_service
from leadgen_app.services.supabase_service import get_supabase_service
from leadgen_app.utils.validators import validate_search_request
from leadgen_app.config import settings

logger = logging.getLogger(__name__)
router = APIRouter()

@router.post(
    "/search",
    summary="Search for leads using AI - n8n workflow replication",
    description="Process natural language queries using LLM → Apollo URL → Apify Crawler workflow"
)
async def search_leads(
    request: LeadSearchRequest,
    user_id: str = Depends(require_authenticated_user)
):
    """
    Main endpoint replicating n8n workflow:
    1. Convert natural language to Apollo URL using LLM
    2. Run Apify crawler to scrape Apollo.io
    3. Process and return lead data in n8n format
    4. Save results to Supabase
    """
    request_id = str(uuid.uuid4())
    
    try:
        logger.info(f"Lead search request {request_id} from user {user_id} - n8n replication")
        
        # Validate request
        validation_result = await validate_search_request(request, user_id)
        if not validation_result["valid"]:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail=validation_result["error"]
            )
        
        # Process the search request using n8n workflow replication
        leads_data, metrics = await ai_service.process_lead_search(request, user_id)
        
        if not leads_data:
            return JSONResponse(
                status_code=200,
                content={
                    "message": "Search completed but no leads found matching your criteria. Try adjusting your search parameters.",
                    "data": [{"leads_data": []}],
                    "success": True,
                    "request_id": request_id,
                    "metrics": metrics
                }
            )
        
        # Prepare source query criteria for database storage
        source_query_criteria = {
            "mainQuery": request.main_query,
            "filters": request.filters.dict(),
            "maxResults": request.max_results,
            "includeEnrichment": request.include_enrichment,
            "requestId": request_id,
            "timestamp": metrics.get("timestamp", "")
        }
        
        # Save leads to database
        await save_leads_background(
            leads_data,
            user_id,
            source_query_criteria,
            request_id
        )
        
        # Format response to match exact n8n output structure
        n8n_formatted_response = [
            {
                "leads_data": [
                    {
                        "first_name": lead.first_name,
                        "last_name": lead.last_name,
                        "name": lead.name,
                        "job_title": lead.job_title,
                        "company_name": lead.company_name,
                        "company_size": lead.company_size,
                        "industry": lead.industry,
                        "location": lead.location,
                        "email": lead.email,
                        "phone": lead.phone,
                        "linkedin_url": lead.linkedin_url,
                        "keywords": lead.keywords,
                        "source_query_criteria": lead.source_query_criteria,
                        "icebreaker": None
                    }
                    for lead in leads_data
                ]
            }
        ]
        
        success_message = f"Search completed successfully. Found {len(leads_data)} leads matching your criteria."
        if metrics.get("total_enriched", 0) > 0:
            success_message += f" {metrics['total_enriched']} leads were enriched with additional data."
        
        return JSONResponse(
            status_code=200,
            content={
                "message": success_message,
                "data": n8n_formatted_response,
                "success": True,
                "request_id": request_id,
                "metrics": metrics
            }
        )
        
    except HTTPException:
        # Re-raise HTTP exceptions
        raise
    except Exception as e:
        logger.error(f"Error in lead search {request_id}: {str(e)}", exc_info=True)
        
        return JSONResponse(
            status_code=500,
            content={
                "message": f"Internal server error during lead search: {str(e)}",
                "success": False,
                "error": str(e),
                "request_id": request_id
            }
        )

async def save_leads_background(
    leads_data: list,
    user_id: str,
    source_query_criteria: dict,
    request_id: str
):
    """
    Background task to save leads to database
    """
    try:
        logger.info(f"Saving {len(leads_data)} leads for request {request_id}")
        
        # Check for duplicates
        emails = [lead.email for lead in leads_data if lead.email]
        if emails:
            existing_emails = await get_supabase_service().check_duplicate_leads(user_id, emails)
            if existing_emails:
                logger.info(f"Found {len(existing_emails)} duplicate emails, filtering out")
                leads_data = [lead for lead in leads_data if lead.email not in existing_emails]
        
        if leads_data:
            # Save to database
            save_result = await get_supabase_service().save_leads_batch(
                leads_data,
                user_id,
                source_query_criteria
            )
            
            if save_result["success"]:
                logger.info(f"Successfully saved {save_result['inserted_count']} leads for request {request_id}")
            else:
                logger.error(f"Failed to save leads for request {request_id}: {save_result.get('error')}")
        else:
            logger.info(f"No new leads to save for request {request_id} (all duplicates)")
            
    except Exception as e:
        logger.error(f"Error in background lead save for request {request_id}: {str(e)}")

@router.post(
    "/enrich/{lead_id}",
    response_model=EnrichmentResponse,
    summary="Enrich a specific lead with additional data"
)
async def enrich_lead(
    lead_id: str,
    request: LeadEnrichmentRequest,
    user_id: str = Depends(require_authenticated_user)
):
    """Enrich a specific lead with additional data"""
    try:
        # Validate user access to lead
        has_access = await get_supabase_service().validate_user_access(user_id, lead_id)
        if not has_access:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Lead not found or access denied"
            )
        
        # Get current lead data
        leads = await get_supabase_service().get_leads_by_user(user_id, limit=1)
        current_lead = next((lead for lead in leads if lead["id"] == lead_id), None)
        
        if not current_lead:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Lead not found"
            )
        
        # TODO: Implement lead enrichment logic
        return EnrichmentResponse(
            success=True,
            lead_id=lead_id,
            enriched_data=current_lead,
            enrichment_sources=["internal"],
            confidence_score=0.8
        )
        
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error enriching lead {lead_id}: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Internal server error during lead enrichment"
        )

@router.get(
    "/stats",
    summary="Get user lead statistics"
)
async def get_user_stats(
    user_id: str = Depends(require_authenticated_user)
):
    """Get user lead statistics"""
    try:
        stats = await get_supabase_service().get_user_stats(user_id)
        return {
            "success": True,
            "stats": stats
        }
    except Exception as e:
        logger.error(f"Error getting user stats: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Error retrieving user statistics"
        )

@router.post(
    "/bulk-operation",
    response_model=BulkOperationResponse,
    summary="Perform bulk operations on leads"
)
async def bulk_operation(
    request: BulkLeadRequest,
    user_id: str = Depends(require_authenticated_user)
):
    """Perform bulk operations on leads"""
    try:
        if request.operation == "delete":
            result = await get_supabase_service().delete_leads_batch(request.lead_ids, user_id)
            
            return BulkOperationResponse(
                success=result["success"],
                processed=len(request.lead_ids),
                successful=result.get("deleted_count", 0),
                failed=len(request.lead_ids) - result.get("deleted_count", 0),
                errors=[{"error": result.get("error", "")}] if not result["success"] else [],
                results=result.get("deleted_ids", [])
            )
        
        else:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail=f"Unsupported operation: {request.operation}"
            )
            
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error in bulk operation: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Error performing bulk operation"
        )

@router.get(
    "/test-connection",
    summary="Test database connection and n8n workflow replication"
)
async def test_connection(
    user_info: Dict[str, Any] = Depends(get_current_user)
):
    """Test database connection and workflow components"""
    try:
        # Test database connection
        stats = await get_supabase_service().get_user_stats(user_info["user_id"])
        
        # Test AI service initialization
        ai_status = {
            "openai_available": bool(settings.OPENAI_API_KEY),
            "anthropic_available": bool(settings.ANTHROPIC_API_KEY),
            "apify_available": bool(settings.APIFY_API_TOKEN)
        }
        
        return {
            "success": True,
            "message": "n8n workflow replication ready",
            "user": {
                "user_id": user_info["user_id"],
                "email": user_info["email"]
            },
            "database_stats": stats,
            "ai_services": ai_status,
            "workflow_components": {
                "llm_to_apollo_url": ai_status["openai_available"] or ai_status["anthropic_available"],
                "apify_crawler": ai_status["apify_available"],
                "supabase_storage": True
            }
        }
        
    except Exception as e:
        logger.error(f"Connection test failed: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Connection test failed: {str(e)}"
        )