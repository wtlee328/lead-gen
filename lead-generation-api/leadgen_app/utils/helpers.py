"""
Utility helper functions
"""

import re
import uuid
from typing import Dict, Any, List, Optional
from datetime import datetime
import logging

logger = logging.getLogger(__name__)

def generate_request_id() -> str:
    """Generate a unique request ID"""
    return str(uuid.uuid4())

def clean_phone_number(phone: str) -> Optional[str]:
    """
    Clean and format phone number
    
    Args:
        phone: Raw phone number string
        
    Returns:
        Cleaned phone number or None if invalid
    """
    if not phone:
        return None
    
    # Remove all non-digit characters except +
    cleaned = re.sub(r'[^\d+]', '', phone)
    
    # Basic validation
    if len(cleaned) < 7 or len(cleaned) > 20:
        return None
    
    return cleaned

def extract_domain_from_email(email: str) -> Optional[str]:
    """
    Extract domain from email address
    
    Args:
        email: Email address
        
    Returns:
        Domain name or None if invalid
    """
    if not email or '@' not in email:
        return None
    
    try:
        domain = email.split('@')[1].lower()
        return domain
    except IndexError:
        return None

def normalize_company_name(company_name: str) -> str:
    """
    Normalize company name for better matching
    
    Args:
        company_name: Raw company name
        
    Returns:
        Normalized company name
    """
    if not company_name:
        return ""
    
    # Remove common suffixes
    suffixes = [
        r'\s+(inc\.?|incorporated)$',
        r'\s+(ltd\.?|limited)$', 
        r'\s+(llc\.?)$',
        r'\s+(corp\.?|corporation)$',
        r'\s+(co\.?)$',
        r'\s+&\s+co\.?$'
    ]
    
    normalized = company_name.strip()
    for suffix in suffixes:
        normalized = re.sub(suffix, '', normalized, flags=re.IGNORECASE)
    
    return normalized.strip()

def extract_keywords_from_text(text: str, max_keywords: int = 10) -> List[str]:
    """
    Extract keywords from text using simple heuristics
    
    Args:
        text: Input text
        max_keywords: Maximum number of keywords to return
        
    Returns:
        List of extracted keywords
    """
    if not text:
        return []
    
    # Common stop words to exclude
    stop_words = {
        'the', 'a', 'an', 'and', 'or', 'but', 'in', 'on', 'at', 'to', 'for',
        'of', 'with', 'by', 'is', 'are', 'was', 'were', 'be', 'been', 'have',
        'has', 'had', 'do', 'does', 'did', 'will', 'would', 'could', 'should',
        'may', 'might', 'must', 'can', 'this', 'that', 'these', 'those'
    }
    
    # Extract words (alphanumeric, 3+ characters)
    words = re.findall(r'\b[a-zA-Z]{3,}\b', text.lower())
    
    # Filter out stop words and get unique keywords
    keywords = list(set([word for word in words if word not in stop_words]))
    
    # Sort by length (longer words first) and limit
    keywords.sort(key=len, reverse=True)
    
    return keywords[:max_keywords]

def calculate_confidence_score(lead_data: Dict[str, Any]) -> float:
    """
    Calculate confidence score for a lead based on data completeness
    
    Args:
        lead_data: Lead data dictionary
        
    Returns:
        Confidence score between 0.0 and 1.0
    """
    score = 0.0
    
    # Email is most important
    if lead_data.get('email'):
        score += 0.4
    
    # Contact information
    if lead_data.get('phone'):
        score += 0.2
    if lead_data.get('linkedin_url'):
        score += 0.1
    
    # Professional information
    if lead_data.get('job_title'):
        score += 0.15
    if lead_data.get('company_name'):
        score += 0.1
    
    # Additional data
    if lead_data.get('location'):
        score += 0.05
    
    return min(1.0, score)

def format_apollo_url_params(params: Dict[str, Any]) -> str:
    """
    Format parameters for Apollo URL
    
    Args:
        params: Dictionary of parameters
        
    Returns:
        URL-encoded parameter string
    """
    param_parts = []
    
    for key, value in params.items():
        if isinstance(value, list):
            for item in value:
                param_parts.append(f"{key}[]={str(item).replace(' ', '%20')}")
        else:
            param_parts.append(f"{key}={str(value).replace(' ', '%20')}")
    
    return '&'.join(param_parts)

def parse_company_size_range(size_str: str) -> Optional[Dict[str, int]]:
    """
    Parse company size range string
    
    Args:
        size_str: Size range string like "51-200" or "10001+"
        
    Returns:
        Dictionary with min and max values or None
    """
    if not size_str:
        return None
    
    # Handle "X+" format
    if size_str.endswith('+'):
        try:
            min_size = int(size_str[:-1])
            return {"min": min_size, "max": None}
        except ValueError:
            return None
    
    # Handle "X-Y" format
    if '-' in size_str:
        try:
            parts = size_str.split('-')
            if len(parts) == 2:
                min_size = int(parts[0])
                max_size = int(parts[1])
                return {"min": min_size, "max": max_size}
        except ValueError:
            return None
    
    # Handle single number
    try:
        size = int(size_str)
        return {"min": size, "max": size}
    except ValueError:
        return None

def validate_linkedin_url(url: str) -> bool:
    """
    Validate LinkedIn URL format
    
    Args:
        url: LinkedIn URL to validate
        
    Returns:
        True if valid LinkedIn URL
    """
    if not url:
        return False
    
    linkedin_patterns = [
        r'^https?://(www\.)?linkedin\.com/in/[\w\-]+/?$',
        r'^https?://(www\.)?linkedin\.com/pub/[\w\-]+/[\w\-]+/[\w\-]+/[\w\-]+/?$'
    ]
    
    return any(re.match(pattern, url, re.IGNORECASE) for pattern in linkedin_patterns)

def merge_lead_data(existing: Dict[str, Any], new: Dict[str, Any]) -> Dict[str, Any]:
    """
    Merge two lead data dictionaries, preferring non-empty values
    
    Args:
        existing: Existing lead data
        new: New lead data to merge
        
    Returns:
        Merged lead data dictionary
    """
    merged = existing.copy()
    
    for key, value in new.items():
        if value and (not merged.get(key) or merged[key] == ""):
            merged[key] = value
        elif isinstance(value, list) and value:
            # Merge lists and remove duplicates
            existing_list = merged.get(key, [])
            if isinstance(existing_list, list):
                merged[key] = list(set(existing_list + value))
            else:
                merged[key] = value
    
    return merged

def log_processing_metrics(
    operation: str,
    start_time: datetime,
    success_count: int,
    error_count: int,
    additional_data: Optional[Dict[str, Any]] = None
):
    """
    Log processing metrics for monitoring
    
    Args:
        operation: Operation name
        start_time: Operation start time
        success_count: Number of successful operations
        error_count: Number of failed operations
        additional_data: Additional metrics data
    """
    duration = (datetime.now() - start_time).total_seconds()
    
    metrics = {
        "operation": operation,
        "duration_seconds": round(duration, 2),
        "success_count": success_count,
        "error_count": error_count,
        "total_count": success_count + error_count,
        "success_rate": round(success_count / (success_count + error_count) * 100, 2) if (success_count + error_count) > 0 else 0
    }
    
    if additional_data:
        metrics.update(additional_data)
    
    logger.info(f"Processing metrics: {metrics}")

def chunk_list(lst: List[Any], chunk_size: int) -> List[List[Any]]:
    """
    Split a list into chunks of specified size
    
    Args:
        lst: List to chunk
        chunk_size: Size of each chunk
        
    Returns:
        List of chunks
    """
    return [lst[i:i + chunk_size] for i in range(0, len(lst), chunk_size)]

def safe_get_nested(data: Dict[str, Any], keys: List[str], default: Any = None) -> Any:
    """
    Safely get nested dictionary value
    
    Args:
        data: Dictionary to search
        keys: List of keys for nested access
        default: Default value if key not found
        
    Returns:
        Value at nested key or default
    """
    current = data
    
    for key in keys:
        if isinstance(current, dict) and key in current:
            current = current[key]
        else:
            return default
    
    return current