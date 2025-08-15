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
        # Check main query
        if not request.main_query or len(request.main_query.strip()) < 10:
            return {
                "valid": False,
                "error": "Main query must be at least 10 characters long"
            }
        
        # Check for potentially harmful content
        if contains_harmful_content(request.main_query):
            return {
                "valid": False,
                "error": "Query contains inappropriate content"
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