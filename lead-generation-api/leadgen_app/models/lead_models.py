"""
Lead-specific data models and utilities
"""

from pydantic import BaseModel, Field, validator
from typing import List, Optional, Dict, Any
from datetime import datetime
from enum import Enum

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
    Maps the actual fields returned by the Apify actor
    """
    # Personal information
    firstName: Optional[str] = None
    lastName: Optional[str] = None
    name: Optional[str] = None
    
    # Contact information
    email: Optional[str] = None
    phone: Optional[str] = None
    linkedinUrl: Optional[str] = None
    
    # Professional information
    title: Optional[str] = None
    organization: Optional[Any] = None  # Can be string or dict
    organizationNumEmployees: Optional[int] = None
    
    # Location
    city: Optional[str] = None
    state: Optional[str] = None
    country: Optional[str] = None
    
    # Additional data
    industry: Optional[str] = None
    organizationIndustry: Optional[str] = None
    keywords: Optional[Any] = None  # Can be string or list
    organizationKeywords: Optional[List[str]] = Field(default_factory=list)
    
    # Metadata
    apolloUrl: Optional[str] = None
    scrapedAt: Optional[str] = None
    
    class Config:
        extra = "allow"  # Allow additional fields from Apify

class ProcessedLead(BaseModel):
    """
    Processed lead data in the format expected by frontend
    Matches the n8n output structure exactly
    """
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
    linkedIn_url: Optional[str] = None
    keywords: List[str] = Field(default_factory=list)
    source_query_criteria: Optional[Dict[str, Any]] = None
    icebreaker: Optional[str] = None
    
    # Additional metadata (not in n8n format but useful)
    confidence_score: Optional[float] = Field(None, ge=0.0, le=1.0)
    lead_source: LeadSource = LeadSource.APOLLO
    lead_quality: LeadQuality = LeadQuality.UNKNOWN
    processing_notes: Optional[str] = None
    
    @validator('name', always=True)
    def generate_name(cls, v, values):
        """Generate name from first_name and last_name if not provided"""
        if not v:
            first = values.get('first_name', '')
            last = values.get('last_name', '')
            return f"{first} {last}".strip() if first or last else None
        return v
    
    @validator('company_size')
    def validate_company_size(cls, v):
        """Ensure company_size is string"""
        if v is not None:
            return str(v)
        return v
    
    @validator('linkedIn_url')
    def validate_linkedin_url(cls, v):
        """Basic LinkedIn URL validation"""
        if v and not v.startswith(('http://', 'https://')):
            return f"https://{v}"
        return v

class LeadProcessingResult(BaseModel):
    """Result of lead processing operation"""
    success: bool
    processed_count: int
    error_count: int
    leads: List[ProcessedLead] = Field(default_factory=list)
    errors: List[str] = Field(default_factory=list)
    processing_time: float
    
class LeadEnrichmentData(BaseModel):
    """Additional data for lead enrichment"""
    social_profiles: Dict[str, str] = Field(default_factory=dict)
    company_info: Dict[str, Any] = Field(default_factory=dict)
    contact_verification: Dict[str, bool] = Field(default_factory=dict)
    additional_emails: List[str] = Field(default_factory=list)
    additional_phones: List[str] = Field(default_factory=list)
    technologies_used: List[str] = Field(default_factory=list)
    company_funding: Optional[Dict[str, Any]] = None
    
class ApifyActorConfig(BaseModel):
    """Configuration for Apify actor execution"""
    actor_id: str = "jljBwyyQakqrL1wae"  # Default from n8n
    url: str
    totalRecords: int = 50
    fileName: str = "Apollo Prospects"
    timeout: int = 300  # 5 minutes
    memory: int = 1024  # MB
    
    @validator('totalRecords')
    def validate_total_records(cls, v):
        """Limit total records to prevent excessive usage"""
        return min(v, 100)

class ApolloUrlComponents(BaseModel):
    """Components for building Apollo.io URLs"""
    base_url: str = "https://app.apollo.io/#/people"
    page: int = 1
    email_status: List[str] = Field(default_factory=lambda: ["verified"])
    person_titles: List[str] = Field(default_factory=list)
    person_locations: List[str] = Field(default_factory=list)
    organization_industry_ids: List[str] = Field(default_factory=list)
    organization_num_employees_ranges: List[str] = Field(default_factory=list)
    organization_keyword_tags: List[str] = Field(default_factory=list)
    organization_anded_keyword_tags: List[str] = Field(default_factory=list)
    included_organization_keyword_fields: List[str] = Field(default_factory=list)
    included_anded_organization_keyword_fields: List[str] = Field(default_factory=list)
    
    def build_url(self) -> str:
        """Build complete Apollo URL from components"""
        params = []
        
        # Base parameters
        params.append(f"page={self.page}")
        
        # Email status
        for status in self.email_status:
            params.append(f"contactEmailStatusV2[]={status}")
        
        # Person titles
        for title in self.person_titles:
            params.append(f"personTitles[]={title.replace(' ', '%20')}")
        
        # Person locations
        for location in self.person_locations:
            params.append(f"personLocations[]={location.replace(' ', '%20')}")
        
        # Organization industry IDs
        for industry_id in self.organization_industry_ids:
            params.append(f"organizationIndustryTagIds[]={industry_id}")
        
        # Employee ranges
        for emp_range in self.organization_num_employees_ranges:
            params.append(f"organizationNumEmployeesRanges[]={emp_range}")
        
        # Organization keyword tags
        for keyword in self.organization_keyword_tags:
            params.append(f"qOrganizationKeywordTags[]={keyword.replace(' ', '%20')}")
        
        # Organization anded keyword tags
        for keyword in self.organization_anded_keyword_tags:
            params.append(f"qAndedOrganizationKeywordTags[]={keyword.replace(' ', '%20')}")
        
        # Included keyword fields
        for field in self.included_organization_keyword_fields:
            params.append(f"includedOrganizationKeywordFields[]={field}")
        
        # Included anded keyword fields
        for field in self.included_anded_organization_keyword_fields:
            params.append(f"includedAndedOrganizationKeywordFields[]={field}")
        
        return f"{self.base_url}?{'&'.join(params)}"

def convert_apify_to_processed(apify_lead: ApifyLeadData, source_criteria: Dict[str, Any]) -> ProcessedLead:
    """
    Convert Apify lead data to processed lead format
    
    Args:
        apify_lead: Raw Apify lead data
        source_criteria: Original search criteria
        
    Returns:
        ProcessedLead object
    """
    # Combine location fields
    location_parts = [
        apify_lead.city,
        apify_lead.state,
        apify_lead.country
    ]
    location = ", ".join([part for part in location_parts if part])
    
    # Combine industry information
    industries = []
    if apify_lead.industry:
        industries.append(apify_lead.industry)
    if apify_lead.organizationIndustry and apify_lead.organizationIndustry not in industries:
        industries.append(apify_lead.organizationIndustry)
    
    # Handle keywords - can be string or list
    keywords = []
    if apify_lead.keywords:
        if isinstance(apify_lead.keywords, str):
            # Split string keywords by common delimiters
            keywords.extend([kw.strip() for kw in apify_lead.keywords.split(',') if kw.strip()])
        elif isinstance(apify_lead.keywords, list):
            keywords.extend(apify_lead.keywords)
    
    if apify_lead.organizationKeywords:
        keywords.extend(apify_lead.organizationKeywords)
    keywords = list(set(keywords))  # Remove duplicates
    
    # Handle organization - can be string or dict
    company_name = None
    if apify_lead.organization:
        if isinstance(apify_lead.organization, str):
            company_name = apify_lead.organization
        elif isinstance(apify_lead.organization, dict):
            company_name = apify_lead.organization.get('name') or apify_lead.organization.get('organization_name')
    
    return ProcessedLead(
        first_name=apify_lead.firstName,
        last_name=apify_lead.lastName,
        name=apify_lead.name,
        job_title=apify_lead.title,
        company_name=company_name,
        company_size=str(apify_lead.organizationNumEmployees) if apify_lead.organizationNumEmployees else None,
        industry=industries,
        location=location or None,
        email=apify_lead.email,
        phone=apify_lead.phone,
        linkedIn_url=apify_lead.linkedinUrl,
        keywords=keywords,
        source_query_criteria=source_criteria,
        icebreaker=None,
        lead_source=LeadSource.APOLLO,
        lead_quality=LeadQuality.HIGH if apify_lead.email else LeadQuality.MEDIUM
    )