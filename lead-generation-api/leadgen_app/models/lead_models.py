"""
Lead-specific data models and utilities
"""

from pydantic import BaseModel, Field, validator
from typing import List, Optional, Dict, Any
from datetime import datetime
from enum import Enum
import uuid

class LeadSource(str, Enum):
    """Lead source types"""
    APOLLO = "apollo"
    LINKEDIN = "linkedin"
    MANUAL = "manual"
    IMPORT = "import"
    API = "api"

class LeadQuality(str, Enum):
    """Lead quality ratings"""
    HIGH = "high"
    MEDIUM = "medium"
    LOW = "low"
    UNKNOWN = "unknown"

class ContactMethod(str, Enum):
    """Available contact methods"""
    EMAIL = "email"
    PHONE = "phone"
    LINKEDIN = "linkedin"
    WEBSITE = "website"

class ApifyLeadData(BaseModel):
    """
    Model for raw lead data from Apify Apollo scraper
    """
    id: Optional[str] = None # Add the ID field
    firstName: Optional[str] = None
    lastName: Optional[str] = None
    name: Optional[str] = None
    email: Optional[str] = None
    phone: Optional[str] = None
    linkedin_url: Optional[str] = None
    title: Optional[str] = None
    organization: Optional[Any] = None
    organizationNumEmployees: Optional[int] = None
    city: Optional[str] = None
    state: Optional[str] = None
    country: Optional[str] = None
    industry: Optional[str] = None
    organizationIndustry: Optional[str] = None
    keywords: Optional[Any] = None
    organizationKeywords: Optional[List[str]] = Field(default_factory=list)
    apolloUrl: Optional[str] = None
    scrapedAt: Optional[str] = None
    
    class Config:
        extra = "allow"

class ProcessedLead(BaseModel):
    """
    Processed lead data in the format expected by frontend
    """
    id: str # Add the ID field
    first_name: Optional[str] = None
    last_name: Optional[str] = None
    name: Optional[str] = None
    job_title: Optional[str] = None
    company_name: Optional[str] = None
    company_size: Optional[str] = None
    industry: List[str] = Field(default_factory=list)
    location: Optional[str] = None
    email: Optional[str] = None
    phone: Optional[str] = None
    linkedin_url: Optional[str] = None
    keywords: List[str] = Field(default_factory=list)
    source_query_criteria: Optional[Dict[str, Any]] = None
    icebreaker: Optional[str] = None
    confidence_score: Optional[float] = Field(None, ge=0.0, le=1.0)
    lead_source: LeadSource = LeadSource.APOLLO
    lead_quality: LeadQuality = LeadQuality.UNKNOWN
    processing_notes: Optional[str] = None
    
    @validator('name', always=True)
    def generate_name(cls, v, values):
        if not v:
            first = values.get('first_name', '')
            last = values.get('last_name', '')
            return f"{first} {last}".strip() if first or last else None
        return v
    
    @validator('company_size')
    def validate_company_size(cls, v):
        if v is not None:
            return str(v)
        return v
    
    @validator('linkedin_url')
    def validate_linkedin_url(cls, v):
        """Basic LinkedIn URL validation"""
        if v and not v.startswith(('http://', 'https://')):
            return f"https://{v}"
        return v

def convert_apify_to_processed(apify_lead: ApifyLeadData, source_criteria: Dict[str, Any]) -> ProcessedLead:
    """
    Convert Apify lead data to processed lead format
    """
    location_parts = [apify_lead.city, apify_lead.state, apify_lead.country]
    location = ", ".join([part for part in location_parts if part])
    
    industries = []
    if apify_lead.industry:
        industries.append(apify_lead.industry)
    if apify_lead.organizationIndustry and apify_lead.organizationIndustry not in industries:
        industries.append(apify_lead.organizationIndustry)
    
    keywords = []
    if apify_lead.keywords:
        if isinstance(apify_lead.keywords, str):
            keywords.extend([kw.strip() for kw in apify_lead.keywords.split(',') if kw.strip()])
        elif isinstance(apify_lead.keywords, list):
            keywords.extend(apify_lead.keywords)
    
    if apify_lead.organizationKeywords:
        keywords.extend(apify_lead.organizationKeywords)
    keywords = list(set(keywords))
    
    company_name = None
    if apify_lead.organization:
        if isinstance(apify_lead.organization, str):
            company_name = apify_lead.organization
        elif isinstance(apify_lead.organization, dict):
            company_name = apify_lead.organization.get('name') or apify_lead.organization.get('organization_name')
    
    return ProcessedLead(
        id=apify_lead.id or str(uuid.uuid4()),
        first_name=apify_lead.firstName,
        last_name=apify_lead.lastName,
        name=apify_lead.name,
        job_title=apify_lead.title,
        company_name=company_name,
        company_size=str(apify_lead.organization.get("estimated_num_employees")) if isinstance(apify_lead.organization, dict) and apify_lead.organization.get("estimated_num_employees") else None,
        industry=industries,
        location=location or None,
        email=apify_lead.email,
        phone=apify_lead.organization.get("phone") if isinstance(apify_lead.organization, dict) else None,
        linkedin_url=apify_lead.linkedin_url,
        keywords=keywords,
        source_query_criteria=source_criteria,
        icebreaker=None,
        lead_source=LeadSource.APOLLO,
        lead_quality=LeadQuality.HIGH if apify_lead.email else LeadQuality.MEDIUM
    )
