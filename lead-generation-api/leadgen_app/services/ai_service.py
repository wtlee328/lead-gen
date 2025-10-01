"""
AI service for lead generation and processing
Replicates n8n workflow: LLM -> Apollo URL -> Apify Crawler -> Lead Data
"""

import asyncio
import logging
import json
import re
import uuid
from typing import List, Dict, Any, Optional, Tuple
from datetime import datetime
from openai import OpenAI # Use the official library
from anthropic import Anthropic
import httpx
from apify_client import ApifyClient

from leadgen_app.config import settings
from leadgen_app.models.request_models import LeadSearchRequest, LeadFilters
from leadgen_app.models.response_models import LeadData, ConfidenceLevel
from leadgen_app.models.lead_models import ApifyLeadData, ProcessedLead, convert_apify_to_processed
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
        self.apify_client = None
        
        if settings.OPENAI_API_KEY:
            logger.info("OpenAI API key is loaded. Initializing client.")
            self.openai_client = OpenAI(api_key=settings.OPENAI_API_KEY)
        else:
            logger.warning("OpenAI API key is NOT loaded. LLM functionality will be disabled.")
            
        if settings.APIFY_API_TOKEN:
            self.apify_client = ApifyClient(settings.APIFY_API_TOKEN)
    
    async def process_lead_search(
        self, 
        request: LeadSearchRequest, 
        user_id: str
    ) -> Tuple[List[LeadData], Dict[str, Any]]:
        """
        Main method replicating n8n workflow.
        """
        start_time = datetime.now()
        logger.info(f"--- URL Generation Debug Trace ---")
        logger.info(f"[1/5] Starting lead search for user {user_id}. Request data:\n{request.model_dump()}")
        
        try:
            apollo_url = await self._convert_to_apollo_url(request)
            
            logger.info(f"[6/6] Final URL passed to Apify crawler: {apollo_url}")
            
            raw_leads = await self._run_apify_crawler(apollo_url, request.max_results)
            logger.info(f"Apify crawler returned {len(raw_leads)} leads")
            
            processed_leads = await self._process_apify_leads(raw_leads, request, user_id)
            
            processing_time = (datetime.now() - start_time).total_seconds()
            metrics = self._generate_metrics(processed_leads, processing_time, 1)
            
            logger.info(f"Lead search completed: {len(processed_leads)} leads processed")
            return processed_leads, metrics
            
        except Exception as e:
            logger.error(f"Error in lead search processing: {str(e)}")
            raise
    
    async def _convert_to_apollo_url(self, request: LeadSearchRequest) -> str:
        """
        Convert natural language input to Apollo.io search URL using LLM.
        """
        # Log input mode detection
        has_regular_input = request.main_query and request.main_query.strip()
        has_advanced_input = any(
            getattr(request.filters, field, None) and str(getattr(request.filters, field, '')).strip()
            for field in ['job_title', 'industry', 'location', 'company_size', 'company_names', 'general_keywords']
        )
        
        input_mode = "regular" if has_regular_input and not has_advanced_input else "advanced"
        logger.info(f"[2/5] Input mode detected: {input_mode}")
        logger.info(f"      Regular input: {'Yes' if has_regular_input else 'No'}")
        logger.info(f"      Advanced input: {'Yes' if has_advanced_input else 'No'}")
        
        prompt = self._construct_llm_prompt(request)
        logger.info(f"[3/5] Constructed LLM prompt for {input_mode} mode:\n{prompt}")
        
        try:
            if not self.openai_client:
                raise ValueError("OpenAI client not available. Please configure OPENAI_API_KEY.")
            
            response = await self._call_openai(prompt, max_tokens=1500)
            logger.info(f"[4/5] Raw response from OpenAI:\n{response}")
            
            try:
                result = json.loads(response.strip())
                apollo_url = result.get("searchUrl", "")
                
                if not apollo_url or not apollo_url.startswith("https://app.apollo.io"):
                    raise ValueError(f"LLM generated an invalid Apollo URL: {apollo_url}")
                
                logger.info(f"[5/5] Successfully parsed URL from LLM response: {apollo_url}")
                return apollo_url
                
            except json.JSONDecodeError as e:
                raise ValueError(f"Failed to parse LLM response as JSON: {str(e)}")
                
        except Exception as e:
            logger.error(f"Apollo URL generation failed: {str(e)}")
            raise
    
    def _construct_llm_prompt(self, request: LeadSearchRequest) -> str:
        """Constructs the prompt for the LLM based on input mode."""
        
        # Determine if we're in regular input mode or advanced input mode
        has_regular_input = request.main_query and request.main_query.strip()
        has_advanced_input = any(
            getattr(request.filters, field, None) and str(getattr(request.filters, field, '')).strip()
            for field in ['job_title', 'industry', 'location', 'company_size', 'company_names', 'general_keywords']
        )
        
        if has_regular_input and not has_advanced_input:
            # Regular input mode - LLM should parse and populate filter fields
            return self._construct_regular_input_prompt(request)
        else:
            # Advanced input mode - directly insert entered values into prompt
            return self._construct_advanced_input_prompt(request)
    
    def _construct_regular_input_prompt(self, request: LeadSearchRequest) -> str:
        """Constructs prompt for regular input mode where LLM parses natural language."""
        return f"""
Your task is to convert a natural language description of prospects into a precise Apollo.io Search URL.

**REGULAR INPUT MODE**: Parse the natural language input and extract all filter criteria from it.

Process:
1. **Parse the input description** to extract job titles, locations, company names, industry, and keywords
2. **Generate the Apollo URL** using the extracted information as the main filters

Example parsing:
Input: "Marketing manager at OpenAI in California"
Extracted filters:
- Job Title: Marketing manager
- Industry: Not specified  
- Location: California
- Company Size: Not specified
- Company Names: OpenAI
- Keywords: Not specified

**Base URL (always start with this):**
https://app.apollo.io/#/people?page=1

Apollo URL Parameters:
- `&contactEmailStatusV2[]=verified`: REQUIRED - must be included in every URL
- `&personLocations[]`: Geographic locations (e.g., "United States", "NYC", "San Francisco")
- `&personTitles[]`: Job titles (e.g., "project manager", "director")  
- `&qOrganizationKeywordTags[]`: Specific company names (e.g., "Google", "OpenAI")
- `&includedOrganizationKeywordFields[]=name`: Required when using qOrganizationKeywordTags
- `&qAndedOrganizationKeywordTags[]`: Company-related concepts/keywords (e.g., "startup", "VC-backed")
- `&includedAndedOrganizationKeywordFields[]=name`: Required when using qAndedOrganizationKeywordTags
- `&includedAndedOrganizationKeywordFields[]=tags`: Additional field for keyword matching
- `&organizationIndustryTagIds[]`: Industries (map name to ID from reference below)
- `&organizationNumEmployeesRanges[]`: Company size ranges

Company Size Mapping:
- "1-10" → &organizationNumEmployeesRanges[]=1%2C10
- "11-50" → &organizationNumEmployeesRanges[]=11%2C50  
- "51-200" → &organizationNumEmployeesRanges[]=51%2C200
- "201-500" → &organizationNumEmployeesRanges[]=201%2C500
- "501-1000" → &organizationNumEmployeesRanges[]=501%2C1000
- "1001-5000" → &organizationNumEmployeesRanges[]=1001%2C5000
- "5001-10000" → &organizationNumEmployeesRanges[]=5001%2C10000
- "10001+" → &organizationNumEmployeesRanges[]=10001%2C

**IMPORTANT RULES:**
- You **MUST** start with the base URL: https://app.apollo.io/#/people?page=1
- You **MUST** include `&contactEmailStatusV2[]=verified` in every URL
- Only use information explicitly mentioned in the input
- Do not infer or add extra filters
- URL encode spaces as %20 and special characters appropriately

Industry ID Reference:
{json.dumps(list(APOLLO_INDUSTRY_IDS.items()), indent=2)}

Input Description: "{request.main_query or ''}"

Return the generated URL in JSON format:
{{"searchUrl":"Search URL goes here"}}
"""

    def _construct_advanced_input_prompt(self, request: LeadSearchRequest) -> str:
        """Constructs prompt for advanced input mode where values are directly inserted."""
        return f"""
Your task is to convert specified filter criteria into a precise Apollo.io Search URL.

**ADVANCED INPUT MODE**: Use the provided filter values directly to construct the URL.

The following filter criteria have been specified:
- Job Title: {request.filters.job_title or 'Not specified'}
- Industry: {request.filters.industry or 'Not specified'}
- Location: {request.filters.location or 'Not specified'}
- Company Size: {request.filters.company_size or 'Not specified'}
- Company Names: {request.filters.company_names or 'Not specified'}
- Keywords: {request.filters.general_keywords or 'Not specified'}

{f'Additional context from regular input: "{request.main_query}"' if request.main_query and request.main_query.strip() else ''}

**Base URL (always start with this):**
https://app.apollo.io/#/people?page=1

Apollo URL Parameters:
- `&contactEmailStatusV2[]=verified`: REQUIRED - must be included in every URL
- `&personLocations[]`: Geographic locations (e.g., "United States", "NYC", "San Francisco")
- `&personTitles[]`: Job titles (e.g., "project manager", "director")
- `&qOrganizationKeywordTags[]`: Specific company names (e.g., "Google", "OpenAI")
- `&includedOrganizationKeywordFields[]=name`: Required when using qOrganizationKeywordTags
- `&qAndedOrganizationKeywordTags[]`: Company-related concepts/keywords (e.g., "startup", "VC-backed")
- `&includedAndedOrganizationKeywordFields[]=name`: Required when using qAndedOrganizationKeywordTags
- `&includedAndedOrganizationKeywordFields[]=tags`: Additional field for keyword matching
- `&organizationIndustryTagIds[]`: Industries (map name to ID from reference below)
- `&organizationNumEmployeesRanges[]`: Company size ranges

Company Size Mapping:
- "1-10" → &organizationNumEmployeesRanges[]=1%2C10
- "11-50" → &organizationNumEmployeesRanges[]=11%2C50  
- "51-200" → &organizationNumEmployeesRanges[]=51%2C200
- "201-500" → &organizationNumEmployeesRanges[]=201%2C500
- "501-1000" → &organizationNumEmployeesRanges[]=501%2C1000
- "1001-5000" → &organizationNumEmployeesRanges[]=1001%2C5000
- "5001-10000" → &organizationNumEmployeesRanges[]=5001%2C10000
- "10001+" → &organizationNumEmployeesRanges[]=10001%2C

Industry ID Reference:
{json.dumps(list(APOLLO_INDUSTRY_IDS.items()), indent=2)}

**IMPORTANT RULES:**
- You **MUST** start with the base URL: https://app.apollo.io/#/people?page=1
- You **MUST** include `&contactEmailStatusV2[]=verified` in every URL
- Use only the specified filter values - do not infer additional criteria
- For "Not specified" fields, do not include those parameters in the URL
- URL encode spaces as %20 and special characters appropriately

Return the generated URL in JSON format:
{{"searchUrl":"Search URL goes here"}}
"""


    
    async def _run_apify_crawler(self, apollo_url: str, max_results: int) -> List[Dict[str, Any]]:
        """
        Run Apify crawler to scrape Apollo.io
        """
        if not self.apify_client:
            raise ValueError("Apify client not initialized - missing APIFY_API_TOKEN")
        
        try:
            run_input = {
                "url": apollo_url,
                "totalRecords": max(500, min(max_results, 500)),
                "fileName": "Apollo Prospects"
            }
            
            logger.info(f"Running Apify actor with input: {run_input}")
            
            run = await asyncio.get_event_loop().run_in_executor(
                None,
                lambda: self.apify_client.actor("jljBwyyQakqrL1wae").call(run_input=run_input)
            )
            
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
            return []
    
    async def _process_apify_leads(
        self, 
        raw_leads: List[Dict[str, Any]], 
        request: LeadSearchRequest,
        user_id: str
    ) -> List[LeadData]:
        """
        Process raw Apify data into structured LeadData format.
        """
        start_time = datetime.now()
        processed_leads = []
        error_count = 0
        
        source_query_criteria = {
            "mainQuery": request.main_query or "",
            "filters": request.filters.model_dump()
        }
        
        for raw_lead in raw_leads:
            try:
                apify_lead = ApifyLeadData(**raw_lead)
                processed_lead = convert_apify_to_processed(apify_lead, source_query_criteria)
                
                lead_data = LeadData(
                    id=processed_lead.id or str(uuid.uuid4()),
                    user_id=user_id,
                    first_name=processed_lead.first_name,
                    last_name=processed_lead.last_name,
                    name=processed_lead.name,
                    email=processed_lead.email,
                    phone=processed_lead.phone,
                    linkedin_url=processed_lead.linkedin_url,
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
        
        log_processing_metrics(
            "apify_lead_processing",
            start_time,
            len(processed_leads),
            error_count,
            {"user_id": user_id, "raw_count": len(raw_leads)}
        )
        
        return processed_leads
    
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
            response = self.openai_client.chat.completions.create(
                model="gpt-5-nano",
                messages=[{"role": "user", "content": prompt}],
                max_tokens=max_tokens,
                response_format={"type": "json_object"},
            )
            return response.choices[0].message.content.strip()
        except Exception as e:
            logger.error(f"OpenAI API error: {str(e)}")
            raise

# Global AI service instance
ai_service = AIService()