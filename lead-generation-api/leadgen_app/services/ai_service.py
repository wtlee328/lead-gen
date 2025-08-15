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
        logger.info(f"[1/5] Starting lead search for user {user_id}. Request data:\n{request.dict()}")
        
        try:
            apollo_url = await self._convert_to_apollo_url(request)
            
            logger.info(f"[5/5] Final URL passed to Apify crawler: {apollo_url}")
            
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
        prompt = self._construct_llm_prompt(request)
        logger.info(f"[2/5] Constructed LLM prompt:\n{prompt}")
        
        try:
            if self.openai_client:
                response = await self._call_openai(prompt, max_tokens=1500)
                logger.info(f"[3/5] Raw response from OpenAI:\n{response}")
            else:
                logger.warning("OpenAI client not available, using fallback URL generation.")
                return self._generate_apollo_url_fallback(request)
            
            try:
                result = json.loads(response.strip())
                apollo_url = result.get("searchUrl", "")
                
                if not apollo_url or not apollo_url.startswith("https://app.apollo.io"):
                    logger.warning(f"LLM generated an invalid URL: {apollo_url}. Using fallback.")
                    return self._generate_apollo_url_fallback(request)
                
                logger.info(f"[4/5] Successfully parsed URL from LLM response: {apollo_url}")
                return apollo_url
                
            except json.JSONDecodeError:
                logger.warning("Failed to parse LLM response as JSON, using fallback.")
                return self._generate_apollo_url_fallback(request)
                
        except Exception as e:
            logger.warning(f"LLM Apollo URL generation failed: {str(e)}, using fallback.")
            return self._generate_apollo_url_fallback(request)
    
    def _construct_llm_prompt(self, request: LeadSearchRequest) -> str:
        """Constructs the prompt for the LLM."""
        return f"""
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

You must extract all relevant information (like titles, locations, company names, etc.) from the "Input Description" first, and then supplement it with any "Additional Filters" provided.

- If a/multiple company name is explicitly mentioned (e.g., "Google"), include: &qOrganizationKeywordTags[]=COMPANY_NAME1 &qOrganizationKeywordTags[]=COMPANY_NAME2 &includedOrganizationKeywordFields[]=name
- If a company name is mentioned in the main query (e.g., "Software engineer at Anthropic"), you MUST treat it as a company name and use the `qOrganizationKeywordTags` parameter.
	- If a/multiple company-related concept is mentioned (e.g., "startup", "VC-backed", "open-source", "remote-first"), treat it as a required keyword. These describe company identity, structure, or positioning, not names. Use: &qAndedOrganizationKeywordTags[]=KEYWORD1 &qAndedOrganizationKeywordTags[]=KEYWORD2 &includedAndedOrganizationKeywordFields[]=tags &includedAndedOrganizationKeywordFields[]=social_media_description 

You can change those fields (and only those fields).

ABSOLUTELY DO NOT infer or add any extra filters that are not explicitly mentioned in the user's request. For example, if the user asks for "Software engineers at OpenAI", do not add a keyword for "open-source". Stick strictly to the provided information.

Industry ID Reference:
{json.dumps(list(APOLLO_INDUSTRY_IDS.items()), indent=2)}

Input Description: "{request.main_query}"

Additional Filters:
- Job Title: {request.filters.job_title or 'Not specified'}
- Industry: {request.filters.industry or 'Not specified'}
- Location: {request.filters.location or 'Not specified'}
- Company Size: {request.filters.company_size or 'Not specified'}
- Company Names: {request.filters.company_names or 'Not specified'}
- Keywords: {request.filters.general_keywords or 'Not specified'}

Return the generated URL in a JSON object without quotations:
{{"searchUrl":"Search URL goes here"}}
"""

    def _generate_apollo_url_fallback(self, request: LeadSearchRequest) -> str:
        """
        Fallback method to generate Apollo URL when LLM fails.
        """
        logger.info("Executing fallback URL generation.")
        base_url = "https://app.apollo.io/#/people?page=1&contactEmailStatusV2[]=verified"
        
        if not request.main_query and not request.filters.dict(exclude_none=True):
             return "https://app.apollo.io/#/people?page=1&contactEmailStatusV2[]=verified&personTitles[]=project%20manager&personTitles[]=director&personLocations[]=United%20States&organizationIndustryTagIds[]=5567cdd67369643e64020000&organizationNumEmployeesRanges[]=11%2C20&organizationNumEmployeesRanges[]=21%2C50&organizationIndustryTagIds%5B%5D=5567ced173696450cb580000&qOrganizationKeywordTags%5B%5D=Google&includedOrganizationKeywordFields%5B%5D=name&qAndedOrganizationKeywordTags[]=startup&includedAndedOrganizationKeywordFields[]=name&includedAndedOrganizationKeywordFields[]=tags &includedAndedOrganizationKeywordFields[]=social_media_description"

        return base_url
    
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
            "mainQuery": request.main_query,
            "filters": request.filters.dict()
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
                model="gpt-4o-mini",
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