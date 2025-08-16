"""
Pydantic models for API requests
"""

from pydantic import BaseModel, Field, validator
from typing import List, Optional, Dict, Any, Union
from enum import Enum

def to_camel(string: str) -> str:
    words = string.split('_')
    return words[0] + ''.join(word.capitalize() for word in words[1:])

class CompanySize(str, Enum):
    """Company size options"""
    SMALL = "1-10"
    STARTUP = "11-50" 
    MEDIUM = "51-200"
    LARGE = "201-500"
    ENTERPRISE = "501-1000"
    MEGA = "1001-5000"
    GIANT = "5001-10000"
    MASSIVE = "10001+"

class Industry(str, Enum):
    """Industry categories"""
    TECHNOLOGY = "technology"
    HEALTHCARE = "healthcare"
    FINANCE = "finance"
    EDUCATION = "education"
    RETAIL = "retail"
    MANUFACTURING = "manufacturing"
    CONSULTING = "consulting"
    REAL_ESTATE = "real_estate"
    MEDIA = "media"
    NONPROFIT = "nonprofit"
    GOVERNMENT = "government"
    COSMETICS = "cosmetics"
    # Add more as needed

class LeadFilters(BaseModel):
    """Structured filters for lead search"""
    job_title: Optional[str] = Field(None, max_length=200, description="Target job title")
    industry: Optional[str] = Field(None, description="Industry category")
    location: Optional[str] = Field(None, max_length=200, description="Geographic location")
    company_size: Optional[str] = Field(None, description="Company size range")
    company_names: Optional[str] = Field(None, description="Specific company names as a comma-separated string")
    general_keywords: Optional[str] = Field(None, description="Relevant keywords as a comma-separated string")

    @validator('job_title', 'industry', 'location', 'company_size', 'company_names', 'general_keywords', pre=True)
    def validate_strings(cls, v):
        """Validate string fields and convert empty strings to None"""
        if v is None:
            return None
        if isinstance(v, str):
            v = v.strip()
            return v if v else None
        return v

    class Config:
        alias_generator = to_camel
        populate_by_name = True

class LeadSearchRequest(BaseModel):
    """Main request model for lead search"""
    main_query: Union[str, None] = Field(
        None, 
        description="Natural language description of ideal prospects"
    )
    filters: LeadFilters = Field(default_factory=LeadFilters, description="Structured search filters")
    max_results: Optional[int] = Field(50, ge=1, le=500, description="Maximum number of results")
    include_enrichment: bool = Field(True, description="Whether to enrich lead data")
    
    @validator('main_query', pre=True, always=True)
    def validate_main_query(cls, v):
        """Validate main query with conditional length requirement"""
        # Handle null/None values
        if v is None:
            return None
        # Handle string values
        if isinstance(v, str):
            v = v.strip()
            # Validate length if it's not empty
            if v and len(v) > 1000:
                raise ValueError("Main query must be 1000 characters or less")
            # Convert empty strings to None
            return v if v else None
        # Convert other types to string if possible, or reject
        if isinstance(v, (int, float, bool)):
            return str(v)
        # Reject other types
        raise ValueError("Main query must be a string or null")
        return v
    
    @validator('filters')
    def validate_search_criteria(cls, filters, values):
        """Custom validation to ensure at least one search criteria is provided"""
        main_query = values.get('main_query')
        main_query_text = main_query if main_query else ''
        
        # Check if any filter has a value
        has_filter_values = False
        if filters:
            filter_dict = filters.model_dump() if hasattr(filters, 'model_dump') else (filters.dict() if hasattr(filters, 'dict') else filters)
            has_filter_values = any(
                val and str(val).strip() 
                for val in filter_dict.values()
            )
        
        # If no filters provided, main query must be at least 10 characters
        if not has_filter_values and main_query_text and len(main_query_text) < 10:
            raise ValueError("Main query must be at least 10 characters when no filters are provided")
        
        # At least one search criteria must be provided
        if not main_query_text and not has_filter_values:
            raise ValueError("Either main_query or at least one filter must be provided")
        
        return filters
    
    class Config:
        alias_generator = to_camel
        populate_by_name = True
        json_schema_extra = {
            "example": {
                "mainQuery": "I'm looking for CEOs and Marketing Managers at cosmetics companies in Taiwan",
                "filters": {
                    "jobTitle": "CEO, Marketing Manager",
                    "industry": "cosmetics",
                    "location": "Taiwan",
                    "companySize": "51-200",
                    "companyNames": [],
                    "keywords": ["skincare", "beauty", "cosmetics"]
                },
                "maxResults": 50,
                "includeEnrichment": True
            }
        }

class LeadEnrichmentRequest(BaseModel):
    """Request model for lead enrichment"""
    lead_id: str = Field(..., description="Lead ID to enrich")
    enrich_contact: bool = Field(True, description="Enrich contact information")
    enrich_company: bool = Field(True, description="Enrich company information")
    enrich_social: bool = Field(True, description="Enrich social media profiles")

class BulkLeadRequest(BaseModel):
    """Request model for bulk lead operations"""
    lead_ids: List[str] = Field(..., min_items=1, max_items=100, description="List of lead IDs")
    operation: str = Field(..., description="Operation to perform")
    
    @validator('lead_ids')
    def validate_lead_ids(cls, v):
        """Validate lead IDs"""
        if not v:
            raise ValueError("At least one lead ID is required")
        return list(set(v))  # Remove duplicates
