"""
Pydantic models for API responses
"""

from pydantic import BaseModel, Field
from typing import List, Optional, Dict, Any
from datetime import datetime
from enum import Enum

class LeadStatus(str, Enum):
    """Lead status options"""
    NEW = "new"
    SAVED = "saved"
    ARCHIVED = "archived"
    CONTACTED = "contacted"
    QUALIFIED = "qualified"
    CONVERTED = "converted"

class ConfidenceLevel(str, Enum):
    """Confidence levels for AI-generated data"""
    HIGH = "high"
    MEDIUM = "medium"
    LOW = "low"

class LeadData(BaseModel):
    """Individual lead data structure"""
    # Core identification
    id: Optional[str] = Field(None, description="Unique lead identifier")
    first_name: Optional[str] = Field(None, description="First name")
    last_name: Optional[str] = Field(None, description="Last name")
    name: Optional[str] = Field(None, description="Full name")
    
    # Contact information
    email: Optional[str] = Field(None, description="Email address")
    phone: Optional[str] = Field(None, description="Phone number")
    linkedin_url: Optional[str] = Field(None, description="LinkedIn profile URL")
    
    # Professional information
    job_title: Optional[str] = Field(None, description="Job title")
    company_name: Optional[str] = Field(None, description="Company name")
    company_size: Optional[str] = Field(None, description="Company size")
    industry: List[str] = Field(default_factory=list, description="Industry categories")
    location: Optional[str] = Field(None, description="Location")
    
    # Enrichment data
    keywords: List[str] = Field(default_factory=list, description="Relevant keywords")
    confidence_score: Optional[float] = Field(None, ge=0.0, le=1.0, description="AI confidence score")
    confidence_level: Optional[ConfidenceLevel] = Field(None, description="Confidence level")
    
    # Metadata
    source_query_criteria: Optional[Dict[str, Any]] = Field(None, description="Original search criteria")
    created_at: Optional[datetime] = Field(None, description="Creation timestamp")
    updated_at: Optional[datetime] = Field(None, description="Last update timestamp")
    
    class Config:
        json_schema_extra = {
            "example": {
                "id": "lead_123",
                "first_name": "Alice",
                "last_name": "Chen",
                "name": "Alice Chen",
                "email": "alice.chen@beautyco.com",
                "phone": "+886-2-1234-5678",
                "linkedin_url": "https://linkedin.com/in/alicechen",
                "job_title": "Marketing Manager",
                "company_name": "Beauty Co. Taiwan",
                "company_size": "51-200",
                "industry": ["cosmetics", "beauty"],
                "location": "Taipei, Taiwan",
                "keywords": ["skincare", "digital marketing", "brand management"],
                "confidence_score": 0.85,
                "confidence_level": "high"
            }
        }

class SearchMetrics(BaseModel):
    """Search performance metrics"""
    total_found: int = Field(..., description="Total leads found")
    total_enriched: int = Field(..., description="Total leads enriched")
    processing_time: float = Field(..., description="Processing time in seconds")
    ai_queries_used: int = Field(..., description="Number of AI queries used")
    confidence_distribution: Dict[str, int] = Field(
        default_factory=dict, 
        description="Distribution of confidence levels"
    )

class LeadSearchResponse(BaseModel):
    """Response model for lead search"""
    success: bool = Field(..., description="Whether the request was successful")
    message: str = Field(..., description="Response message")
    leads_data: List[LeadData] = Field(default_factory=list, description="Found leads")
    metrics: Optional[SearchMetrics] = Field(None, description="Search metrics")
    request_id: Optional[str] = Field(None, description="Unique request identifier")
    
    class Config:
        json_schema_extra = {
            "example": {
                "success": True,
                "message": "Search completed successfully. Found 25 leads matching your criteria.",
                "leads_data": [
                    {
                        "first_name": "Alice",
                        "last_name": "Chen", 
                        "email": "alice.chen@beautyco.com",
                        "job_title": "Marketing Manager",
                        "company_name": "Beauty Co. Taiwan",
                        "confidence_score": 0.85
                    }
                ],
                "metrics": {
                    "total_found": 25,
                    "total_enriched": 23,
                    "processing_time": 45.2,
                    "ai_queries_used": 3,
                    "confidence_distribution": {"high": 15, "medium": 8, "low": 2}
                },
                "request_id": "req_abc123"
            }
        }

class ErrorResponse(BaseModel):
    """Error response model"""
    success: bool = Field(False, description="Always false for errors")
    error: str = Field(..., description="Error type")
    message: str = Field(..., description="Error message")
    details: Optional[Dict[str, Any]] = Field(None, description="Additional error details")
    request_id: Optional[str] = Field(None, description="Request identifier")

class HealthResponse(BaseModel):
    """Health check response"""
    status: str = Field(..., description="Service status")
    timestamp: datetime = Field(..., description="Check timestamp")
    version: str = Field(..., description="Service version")
    dependencies: Dict[str, str] = Field(..., description="Dependency status")

class EnrichmentResponse(BaseModel):
    """Lead enrichment response"""
    success: bool = Field(..., description="Whether enrichment was successful")
    lead_id: str = Field(..., description="Lead ID that was enriched")
    enriched_data: LeadData = Field(..., description="Enriched lead data")
    enrichment_sources: List[str] = Field(default_factory=list, description="Data sources used")
    confidence_score: float = Field(..., ge=0.0, le=1.0, description="Overall confidence score")

class BulkOperationResponse(BaseModel):
    """Bulk operation response"""
    success: bool = Field(..., description="Whether the bulk operation was successful")
    processed: int = Field(..., description="Number of items processed")
    successful: int = Field(..., description="Number of successful operations")
    failed: int = Field(..., description="Number of failed operations")
    errors: List[Dict[str, str]] = Field(default_factory=list, description="Error details")
    results: List[Dict[str, Any]] = Field(default_factory=list, description="Operation results")