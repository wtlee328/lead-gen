"""
Pydantic models for API requests
"""

from pydantic import BaseModel, Field, validator
from typing import List, Optional, Dict, Any
from enum import Enum

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
    company_names: List[str] = Field(default_factory=list, description="Specific company names")
    keywords: List[str] = Field(default_factory=list, description="Relevant keywords")
    
    @validator('company_names', 'keywords')
    def validate_lists(cls, v):
        """Validate list fields"""
        if v is None:
            return []
        # Remove empty strings and limit length
        cleaned = [item.strip() for item in v if item and item.strip()]
        return cleaned[:20]  # Limit to 20 items
    
    @validator('job_title', 'location')
    def validate_strings(cls, v):
        """Validate string fields"""
        if v:
            return v.strip()
        return v

class LeadSearchRequest(BaseModel):
    """Main request model for lead search"""
    main_query: str = Field(
        ..., 
        min_length=10, 
        max_length=1000,
        description="Natural language description of ideal prospects"
    )
    filters: LeadFilters = Field(default_factory=LeadFilters, description="Structured search filters")
    max_results: Optional[int] = Field(50, ge=1, le=500, description="Maximum number of results")
    include_enrichment: bool = Field(True, description="Whether to enrich lead data")
    
    @validator('main_query')
    def validate_main_query(cls, v):
        """Validate main query"""
        if not v or not v.strip():
            raise ValueError("Main query cannot be empty")
        return v.strip()
    
    class Config:
        schema_extra = {
            "example": {
                "main_query": "I'm looking for CEOs and Marketing Managers at cosmetics companies in Taiwan",
                "filters": {
                    "job_title": "CEO, Marketing Manager",
                    "industry": "cosmetics",
                    "location": "Taiwan",
                    "company_size": "51-200",
                    "company_names": [],
                    "keywords": ["skincare", "beauty", "cosmetics"]
                },
                "max_results": 50,
                "include_enrichment": True
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