"""
Input validation utilities
"""

import re
import logging
from typing import Dict, Any, List
from leadgen_app.models.request_models import LeadSearchRequest
from leadgen_app.config import settings

logger = logging.getLogger(__name__)

async def validate_search_request(
    request: LeadSearchRequest, 
    user_id: str
) -> Dict[str, Any]:
    """
    Validate lead search request
    
    Args:
        request: Lead search request to validate
        user_id: User identifier
        
    Returns:
        Validation result dictionary
    """
    try:
        # Check if either main query or filters are provided
        has_main_query = request.main_query and request.main_query.strip()
        has_filters = any(
            getattr(request.filters, field, None) and str(getattr(request.filters, field, '')).strip()
            for field in ['job_title', 'industry', 'location', 'company_size', 'company_names', 'general_keywords']
        )
        
        if not has_main_query and not has_filters:
            return {
                "valid": False,
                "error": "Either main query or at least one filter must be provided"
            }
        
        # If main query is provided without filters, check minimum length
        if has_main_query and not has_filters and len(request.main_query.strip()) < 10:
            return {
                "valid": False,
                "error": "Main query must be at least 10 characters when no filters are provided"
            }
        
        # Check for potentially harmful content in main query
        if has_main_query and contains_harmful_content(request.main_query):
            return {
                "valid": False,
                "error": "Query contains inappropriate content"
            }
        
        # Check for harmful content in filter fields
        filter_values = [
            request.filters.job_title,
            request.filters.industry,
            request.filters.location,
            request.filters.company_names,
            request.filters.general_keywords
        ]
        
        for value in filter_values:
            if value and contains_harmful_content(str(value)):
                return {
                    "valid": False,
                    "error": "Filter contains inappropriate content"
                }
        
        # Check max results
        if request.max_results > settings.MAX_LEADS_PER_REQUEST:
            return {
                "valid": False,
                "error": f"Maximum results cannot exceed {settings.MAX_LEADS_PER_REQUEST}"
            }
        
        return {"valid": True}
        
    except Exception as e:
        logger.error(f"Error validating search request: {str(e)}")
        return {
            "valid": False,
            "error": "Validation error occurred"
        }

def contains_harmful_content(text: str) -> bool:
    """
    Check if text contains potentially harmful content
    
    Args:
        text: Text to check
        
    Returns:
        True if harmful content detected
    """
    # List of patterns to check for
    harmful_patterns = [
        r'\b(hack|exploit|attack|malware|virus)\b',
        r'\b(illegal|fraud|scam|phishing)\b',
        r'\b(spam|bulk email|mass email)\b',
    ]
    
    text_lower = text.lower()
    
    for pattern in harmful_patterns:
        if re.search(pattern, text_lower):
            logger.warning(f"Harmful content detected: {pattern}")
            return True
    
    return False