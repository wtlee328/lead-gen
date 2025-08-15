"""
AI service for lead generation and processing
Replicates n8n workflow: LLM → Apollo URL → Apify Crawler → Lead Data
"""

import asyncio
import logging
import json
import re
from typing import List, Dict, Any, Optional, Tuple
from datetime import datetime
import openai
from anthropic import Anthropic
import httpx
from apify_client import ApifyClient

from leadgen_app.config import settings
from leadgen_app.models.request_models import LeadSearchRequest, LeadFilters
from leadgen_app.models.response_models import LeadData, ConfidenceLevel
from leadgen_app.models.lead_models import ApifyLeadData, ProcessedLead, convert_apify_to_processed, ApifyActorConfig
from leadgen_app.utils.helpers import log_processing_metrics

logger = logging.getLogger(__name__)

# Apollo Industry ID Mapping (from n8n workflow)
APOLLO_INDUSTRY_IDS = {
    "information technology & services": "5567cd4773696439b10b0000",
    "construction": "5567cd4773696439dd350000",
    "marketing & advertising": "5567cd467369644d39040000",
    "health, wellness & fitness": "5567cddb7369644d250c0000",
    "pharmaceuticals": "5567e0eb73696410e4bd1200",
    "biotechnology": "5567d08e7369645dbc4b0000",
    "real estate": "5567cd477369645401010000",
    "management consulting": "5567cdd47369643dbf260000",
    "computer software": "5567cd4e7369643b70010000",
    "internet": "5567cd4d736964397e020000",
    "semiconductors": "5567e0d87369640e5aa30c00",
    "retail": "5567ced173696450cb580000",
    "financial services": "5567cdd67369643e64020000",
    "consumer services": "5567d1127261697f2b1d0000",
    "hospital & health care": "5567cdde73696439812c0000",
    "automotive": "5567cdf27369644cfd800000",
    "restaurants": "5567e0e0736964198de70700",
    "education management": "5567ce9e736964540d540000",
    "food & beverages": "5567ce1e7369643b806a0000",
    "design": "5567cdbc73696439d90b0000",
    "apparel & fashion": "5567cd82736964540d0b0000",
    "import & export": "5567ce9d7369645430c50000",
    "hospitality": "5567ce9d7369643bc19c0000",
    "accounting": "5567ce1f7369643b78570000",
    "events services": "5567cd8e7369645409450000",
    "luxury goods & jewelry": "5567cda97369644cfd3e0000",
    "cosmetics": "5567e1ae73696423dc040000",
    "logistics & supply chain": "5567cd4973696439b9010000",
    "warehousing": "5567e127736964181e700200",
    "package/freight delivery": "5567e8bb7369641a658f0000"
}

class AIService:
    """AI service replicating n8n workflow for lead generation"""
    
    def __init__(self):
        self.openai_client = None
        self.anthropic_client = None
        self.apify_client = None
        
        # Initialize AI clients
        if settings.OPENAI_API_KEY:
            self.openai_client = True  # Flag to indicate OpenAI is available
            
        if settings.ANTHROPIC_API_KEY:
            self.anthropic_client = Anthropic(api_key=settings.ANTHROPIC_API_KEY)
            
        # Initialize Apify client
        if settings.APIFY_API_TOKEN:
            self.apify_client = ApifyClient(settings.APIFY_API_TOKEN)
    
    async def process_lead_search(
        self, 
        request: LeadSearchRequest, 
        user_id: str
    ) -> Tuple[List[LeadData], Dict[str, Any]]:
        """
        Main method replicating n8n workflow:
        1. Convert input to Apollo URL using LLM
        2. Run Apify crawler with the URL
        3. Process and return lead data
        
        Args:
            request: Lead search request
            user_id: User identifier
            
        Returns:
            Tuple of (leads_data, metrics)
        """
        start_time = datetime.now()
        logger.info(f"Processing lead search for user {user_id} - n8n workflow replication")
        
        try:
            # Step 1: Convert natural language input to Apollo URL using LLM
            apollo_url = await self._convert_to_apollo_url(request)
            logger.info(f"Generated Apollo URL: {apollo_url}")
            
            # Step 2: Run Apify crawler to get prospect data
            raw_leads = await self._run_apify_crawler(apollo_url, request.max_results)
            logger.info(f"Apify crawler returned {len(raw_leads)} leads")
            
            # Step 3: Process raw leads into structured format
            processed_leads = await self._process_apify_leads(
                raw_leads, 
                request, 
                user_id
            )
            
            # Step 4: Generate metrics
            processing_time = (datetime.now() - start_time).total_seconds()
            metrics = self._generate_metrics(processed_leads, processing_time, 1)
            
            logger.info(f"Lead search completed: {len(processed_leads)} leads processed")
            return processed_leads, metrics
            
        except Exception as e:
            logger.error(f"Error in lead search processing: {str(e)}")
            raise
    
    async def _convert_to_apollo_url(self, request: LeadSearchRequest) -> str:
        """
        Convert natural language input to Apollo.io search URL using LLM
        Replicates the LLM step from n8n workflow
        
        Args:
            request: Lead search request
            
        Returns:
            Apollo.io search URL
        """
        # Construct the LLM prompt (exact replica from n8n)
        prompt = f"""
Your task is to take as input a natural language description of a prospect audience, and turn that into an Apollo Search URL. Here's an example of an Apollo Search URL: 
https://app.apollo.io/#/people?page=1&contactEmailStatusV2[]=verified&personTitles[]=project%20manager&personTitles[]=director&personLocations[]=United%20States&organizationIndustryTagIds[]=5567cdd67369643e64020000&organizationNumEmployeesRanges[]=11%2C20&organizationNumEmployeesRanges[]=21%2C50&organizationIndustryTagIds%5B%5D=5567ced173696450cb580000&qOrganizationKeywordTags%5B%5D=Google&includedOrganizationKeywordFields%5B%5D=name&qAndedOrganizationKeywordTags[]=startup&includedAndedOrganizationKeywordFields[]=name&includedAndedOrganizationKeywordFields[]=tags &includedAndedOrganizationKeywordFields[]=social_media_description 

This URL describes a search that people that are: 
1. Email is verified. 
2. Hold the titles: project manager or director. 
3. Are locate in the United States. 
4. Industry: Financial Services. It should be replaced by it's corresponding industry ID in the url. 
5. Company has the number of employees 11-20 or 21-50. 
6. Have a industry related to retail. 
7. Have a company keyword "Google". 
8. Must include companies related to "startup" via keywords in their name, tags, or description.  
	- If a/multiple company name is explicitly mentioned (e.g., "Google"), include: &qOrganizationKeywordTags[]=COMPANY_NAME1 &qOrganizationKeywordTags[]=COMPANY_NAME2 &includedOrganizationKeywordFields[]=name 
	- If a/multiple company-related concept is mentioned (e.g., "startup", "VC-backed", "open-source", "remote-first"), treat it as a required keyword. These describe company identity, structure, or positioning, not names. Use: &qAndedOrganizationKeywordTags[]=KEYWORD1 &qAndedOrganizationKeywordTags[]=KEYWORD2 &includedAndedOrganizationKeywordFields[]=tags &includedAndedOrganizationKeywordFields[]=social_media_description 

You can change those fields (and only those fields).

Industry ID Reference:
{json.dumps(list(APOLLO_INDUSTRY_IDS.items()), indent=2)}

Input Description: "{request.main_query}"

Additional Filters:
- Job Title: {request.filters.job_title or 'Not specified'}
- Industry: {request.filters.industry or 'Not specified'}
- Location: {request.filters.location or 'Not specified'}
- Company Size: {request.filters.company_size or 'Not specified'}
- Company Names: {', '.join(request.filters.company_names) if request.filters.company_names else 'Not specified'}
- Keywords: {', '.join(request.filters.keywords) if request.filters.keywords else 'Not specified'}

Return the generated URL in a JSON object without quotations:
{{"searchUrl":"Search URL goes here"}}
"""
        
        try:
            # Call LLM to generate Apollo URL
            if self.openai_client:
                response = await self._call_openai(prompt, max_tokens=1500)
            elif self.anthropic_client:
                response = await self._call_anthropic(prompt, max_tokens=1500)
            else:
                # Fallback to rule-based URL generation
                return self._generate_apollo_url_fallback(request)
            
            # Parse the JSON response
            try:
                result = json.loads(response.strip())
                apollo_url = result.get("searchUrl", "")
                
                if not apollo_url or not apollo_url.startswith("https://app.apollo.io"):
                    raise ValueError("Invalid Apollo URL generated")
                
                return apollo_url
                
            except json.JSONDecodeError:
                logger.warning("Failed to parse LLM response as JSON, using fallback")
                return self._generate_apollo_url_fallback(request)
                
        except Exception as e:
            logger.warning(f"LLM Apollo URL generation failed: {str(e)}, using fallback")
            return self._generate_apollo_url_fallback(request)
    
    def _generate_apollo_url_fallback(self, request: LeadSearchRequest) -> str:
        """
        Fallback method to generate Apollo URL when LLM fails
        
        Args:
            request: Lead search request
            
        Returns:
            Basic Apollo.io search URL
        """
        base_url = "https://app.apollo.io/#/people?page=1&contactEmailStatusV2[]=verified"
        
        # Add job titles
        if request.filters.job_title:
            titles = [title.strip() for title in request.filters.job_title.split(',')]
            for title in titles:
                base_url += f"&personTitles[]={title.replace(' ', '%20')}"
        
        # Add location
        if request.filters.location:
            base_url += f"&personLocations[]={request.filters.location.replace(' ', '%20')}"
        
        # Add industry
        if request.filters.industry:
            industry_lower = request.filters.industry.lower()
            industry_id = APOLLO_INDUSTRY_IDS.get(industry_lower)
            if industry_id:
                base_url += f"&organizationIndustryTagIds[]={industry_id}"
        
        # Add company size
        if request.filters.company_size:
            size_mapping = {
                "1-10": "1%2C10",
                "11-50": "11%2C50", 
                "51-200": "51%2C200",
                "201-500": "201%2C500",
                "501-1000": "501%2C1000",
                "1001-5000": "1001%2C5000",
                "5001-10000": "5001%2C10000",
                "10001+": "10001%2C"
            }
            size_param = size_mapping.get(request.filters.company_size)
            if size_param:
                base_url += f"&organizationNumEmployeesRanges[]={size_param}"
        
        # Add company names
        for company in request.filters.company_names:
            base_url += f"&qOrganizationKeywordTags[]={company.replace(' ', '%20')}"
        if request.filters.company_names:
            base_url += "&includedOrganizationKeywordFields[]=name"
        
        # Add keywords
        for keyword in request.filters.keywords:
            base_url += f"&qAndedOrganizationKeywordTags[]={keyword.replace(' ', '%20')}"
        if request.filters.keywords:
            base_url += "&includedAndedOrganizationKeywordFields[]=tags"
            base_url += "&includedAndedOrganizationKeywordFields[]=social_media_description"
        
        return base_url
    
    async def _run_apify_crawler(self, apollo_url: str, max_results: int) -> List[Dict[str, Any]]:
        """
        Run Apify crawler to scrape Apollo.io
        Replicates the Apify step from n8n workflow
        
        Args:
            apollo_url: Apollo.io search URL
            max_results: Maximum number of results to retrieve
            
        Returns:
            List of raw lead data from Apify
        """
        if not self.apify_client:
            raise ValueError("Apify client not initialized - missing APIFY_API_TOKEN")
        
        try:
            # Prepare Apify actor input (matching n8n configuration)
            run_input = {
                "url": apollo_url,
                "totalRecords": max(500, min(max_results, 500)),  # Minimum 500 required by actor
                "fileName": "Apollo Prospects"
            }
            
            logger.info(f"Running Apify actor with input: {run_input}")
            
            # Run the Apify actor synchronously (matching n8n behavior)
            # Using the same actor ID from n8n: jljBwyyQakqrL1wae
            run = await asyncio.get_event_loop().run_in_executor(
                None,
                lambda: self.apify_client.actor("jljBwyyQakqrL1wae").call(run_input=run_input)
            )
            
            # Fetch results from the dataset
            items = []
            dataset_client = self.apify_client.dataset(run["defaultDatasetId"])
            
            for item in dataset_client.iterate_items():
                items.append(item)
                if len(items) >= max_results:
                    break
            
            logger.info(f"Apify crawler completed: {len(items)} items retrieved")
            return items
            
        except Exception as e:
            logger.error(f"Apify crawler error: {str(e)}")
            # Return empty list instead of failing completely
            return []
    
    async def _process_apify_leads(
        self, 
        raw_leads: List[Dict[str, Any]], 
        request: LeadSearchRequest,
        user_id: str
    ) -> List[LeadData]:
        """
        Process raw Apify data into structured LeadData format
        Uses proper data models for better type safety and validation
        
        Args:
            raw_leads: Raw data from Apify crawler
            request: Original search request
            user_id: User identifier
            
        Returns:
            List of processed LeadData objects
        """
        start_time = datetime.now()
        processed_leads = []
        error_count = 0
        
        # Prepare source query criteria (matching n8n format)
        source_query_criteria = {
            "mainQuery": request.main_query,
            "filters": {
                "jobTitle": request.filters.job_title or "",
                "industry": request.filters.industry or "",
                "location": request.filters.location or "",
                "companySize": request.filters.company_size or "",
                "companyNames": request.filters.company_names,
                "keywords": request.filters.keywords
            }
        }
        
        for raw_lead in raw_leads:
            try:
                # Parse raw data into structured Apify model
                apify_lead = ApifyLeadData(**raw_lead)
                
                # Convert to processed lead format
                processed_lead = convert_apify_to_processed(apify_lead, source_query_criteria)
                
                # Convert to LeadData format for compatibility
                lead_data = LeadData(
                    first_name=processed_lead.first_name,
                    last_name=processed_lead.last_name,
                    name=processed_lead.name,
                    email=processed_lead.email,
                    phone=processed_lead.phone,
                    linkedin_url=processed_lead.linkedIn_url,
                    job_title=processed_lead.job_title,
                    company_name=processed_lead.company_name,
                    company_size=processed_lead.company_size,
                    industry=processed_lead.industry,
                    location=processed_lead.location,
                    keywords=processed_lead.keywords,
                    confidence_score=processed_lead.confidence_score or 0.8,
                    confidence_level=ConfidenceLevel.HIGH if processed_lead.email else ConfidenceLevel.MEDIUM,
                    source_query_criteria=source_query_criteria,
                    created_at=datetime.now()
                )
                
                processed_leads.append(lead_data)
                
            except Exception as e:
                logger.warning(f"Error processing lead: {str(e)}")
                error_count += 1
                continue
        
        # Log processing metrics
        log_processing_metrics(
            "apify_lead_processing",
            start_time,
            len(processed_leads),
            error_count,
            {"user_id": user_id, "raw_count": len(raw_leads)}
        )
        
        return processed_leads
    
    def _extract_industries(self, raw_lead: Dict[str, Any]) -> List[str]:
        """Extract industry information from raw lead data"""
        industries = []
        
        # Try different possible field names
        industry_fields = ["industry", "organizationIndustry", "industries"]
        
        for field in industry_fields:
            value = raw_lead.get(field)
            if value:
                if isinstance(value, list):
                    industries.extend(value)
                elif isinstance(value, str):
                    industries.append(value)
        
        return list(set(industries))  # Remove duplicates
    
    def _extract_keywords(self, raw_lead: Dict[str, Any]) -> List[str]:
        """Extract keywords from raw lead data"""
        keywords = []
        
        # Extract from various fields that might contain keywords
        keyword_sources = [
            raw_lead.get("organizationKeywords", []),
            raw_lead.get("keywords", []),
            raw_lead.get("tags", [])
        ]
        
        for source in keyword_sources:
            if isinstance(source, list):
                keywords.extend(source)
            elif isinstance(source, str):
                keywords.append(source)
        
        return list(set(keywords))  # Remove duplicates
    
    def _generate_metrics(
        self, 
        leads: List[LeadData], 
        processing_time: float, 
        ai_queries_used: int
    ) -> Dict[str, Any]:
        """Generate search metrics"""
        confidence_dist = {"high": 0, "medium": 0, "low": 0}
        enriched_count = 0
        
        for lead in leads:
            if lead.confidence_level:
                confidence_dist[lead.confidence_level.value] += 1
            
            # Count enriched leads
            contact_methods = sum([
                bool(lead.email),
                bool(lead.phone),
                bool(lead.linkedin_url)
            ])
            if contact_methods >= 2:
                enriched_count += 1
        
        return {
            "total_found": len(leads),
            "total_enriched": enriched_count,
            "processing_time": round(processing_time, 2),
            "ai_queries_used": ai_queries_used,
            "confidence_distribution": confidence_dist
        }
    
    async def _call_openai(self, prompt: str, max_tokens: int = 500) -> str:
        """Call OpenAI API"""
        try:
            from openai import AsyncOpenAI
            client = AsyncOpenAI(api_key=settings.OPENAI_API_KEY)
            
            response = await client.chat.completions.create(
                model="gpt-5-nano",  # Using gpt-5-nano as requested
                messages=[{"role": "user", "content": prompt}],
                max_completion_tokens=max_tokens,  # Fixed parameter name for gpt-5-nano
                # temperature=0.3  # Removed - gpt-5-nano only supports default temperature
            )
            return response.choices[0].message.content.strip()
        except Exception as e:
            logger.error(f"OpenAI API error: {str(e)}")
            raise
    
    async def _call_anthropic(self, prompt: str, max_tokens: int = 500) -> str:
        """Call Anthropic API"""
        try:
            response = await self.anthropic_client.messages.create(
                model="claude-3-sonnet-20240229",
                max_tokens=max_tokens,
                messages=[{"role": "user", "content": prompt}]
            )
            return response.content[0].text.strip()
        except Exception as e:
            logger.error(f"Anthropic API error: {str(e)}")
            raise

# Global AI service instance
ai_service = AIService()