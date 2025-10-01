"""
Supabase service for database operations
"""

import logging
import uuid
from typing import List, Dict, Any, Optional
from datetime import datetime
from supabase import create_client, Client
import asyncio
from concurrent.futures import ThreadPoolExecutor

from leadgen_app.config import settings
from leadgen_app.models.response_models import LeadData

logger = logging.getLogger(__name__)

class SupabaseService:
    """Service for Supabase database operations"""
    
    def __init__(self):
        self.client: Client = create_client(
            settings.SUPABASE_URL,
            settings.SUPABASE_SERVICE_ROLE_KEY
        )
        self.executor = ThreadPoolExecutor(max_workers=5)
    
    async def save_leads_batch(
        self, 
        leads: List[LeadData], 
        user_id: str,
        source_query_criteria: Dict[str, Any]
    ) -> Dict[str, Any]:
        """
        Save a batch of leads to Supabase
        
        Args:
            leads: List of LeadData objects
            user_id: User identifier
            source_query_criteria: Original search criteria
            
        Returns:
            Dictionary with save results
        """
        try:
            # Prepare lead records for insertion
            lead_records = []
            
            for lead in leads:
                # Generate unique ID if not present
                lead_id = lead.id or str(uuid.uuid4())
                
                record = {
                    "id": lead_id,
                    "user_id": user_id,
                    "tab": "new",  # New leads start in 'new' tab
                    "lead_status": "new",
                    "first_name": lead.first_name,
                    "last_name": lead.last_name,
                    "name": lead.name,
                    "email": lead.email,
                    "phone": lead.phone,
                    "linkedin_url": lead.linkedin_url,
                    "job_title": lead.job_title,
                    "company_name": lead.company_name,
                    "company_size": lead.company_size,
                    "industry": lead.industry,
                    "location": lead.location,
                    "keywords": lead.keywords,
                    "source_query_criteria": {
                        **source_query_criteria,
                        "confidence_score": lead.confidence_score,
                        "confidence_level": lead.confidence_level.value if lead.confidence_level else None
                    },
                    "created_at": datetime.utcnow().isoformat()
                }
                
                lead_records.append(record)
            
            # Execute database insertion in thread pool
            result = await asyncio.get_event_loop().run_in_executor(
                self.executor,
                self._insert_leads_sync,
                lead_records
            )
            
            logger.info(f"Successfully saved {len(lead_records)} leads for user {user_id}")
            
            return {
                "success": True,
                "inserted_count": len(lead_records),
                "lead_ids": [record["id"] for record in lead_records]
            }
            
        except Exception as e:
            logger.error(f"Error saving leads batch: {str(e)}")
            return {
                "success": False,
                "error": str(e),
                "inserted_count": 0
            }
    
    def _insert_leads_sync(self, lead_records: List[Dict[str, Any]]) -> Dict[str, Any]:
        """
        Synchronous lead insertion (runs in thread pool)
        
        Args:
            lead_records: List of lead record dictionaries
            
        Returns:
            Insertion result
        """
        try:
            # Use upsert to handle duplicates gracefully
            # This will insert new records and ignore duplicates
            result = self.client.table("leads").upsert(
                lead_records,
                on_conflict="id",
                ignore_duplicates=True
            ).execute()
            
            return {
                "success": True,
                "data": result.data,
                "count": len(result.data) if result.data else 0
            }
            
        except Exception as e:
            error_str = str(e)
            logger.error(f"Synchronous lead insertion error: {error_str}")
            
            # If upsert fails, try individual insertions to identify problematic records
            if "duplicate key value violates unique constraint" in error_str or "upsert" in error_str.lower():
                logger.warning("Upsert failed, trying individual insertions to handle duplicates")
                successful_inserts = []
                
                for record in lead_records:
                    try:
                        individual_result = self.client.table("leads").insert([record]).execute()
                        if individual_result.data:
                            successful_inserts.extend(individual_result.data)
                    except Exception as individual_error:
                        if "duplicate key value violates unique constraint" in str(individual_error):
                            logger.info(f"Skipping duplicate lead with ID: {record.get('id')}")
                        else:
                            logger.error(f"Failed to insert individual lead {record.get('id')}: {individual_error}")
                
                return {
                    "success": True,
                    "data": successful_inserts,
                    "count": len(successful_inserts)
                }
            
            raise
    
    async def get_user_lead_count(self, user_id: str, tab: str = None) -> int:
        """
        Get count of leads for a user
        
        Args:
            user_id: User identifier
            tab: Optional tab filter ('new', 'saved', 'archived')
            
        Returns:
            Count of leads
        """
        try:
            query = self.client.table("leads").select("id", count="exact").eq("user_id", user_id)
            
            if tab:
                query = query.eq("tab", tab)
            
            result = await asyncio.get_event_loop().run_in_executor(
                self.executor,
                lambda: query.execute()
            )
            
            return result.count or 0
            
        except Exception as e:
            logger.error(f"Error getting user lead count: {str(e)}")
            return 0
    
    async def get_user_stats(self, user_id: str) -> Dict[str, Any]:
        """
        Get user statistics
        
        Args:
            user_id: User identifier
            
        Returns:
            User statistics dictionary
        """
        try:
            # Get counts for each tab
            stats = {}
            
            for tab in ["new", "saved", "archived"]:
                count = await self.get_user_lead_count(user_id, tab)
                stats[f"{tab}_count"] = count
            
            # Get total count
            stats["total_count"] = await self.get_user_lead_count(user_id)
            
            # Get recent activity (leads created in last 7 days)
            from datetime import timedelta
            recent_date = (datetime.utcnow() - timedelta(days=7)).isoformat()
            
            recent_result = await asyncio.get_event_loop().run_in_executor(
                self.executor,
                lambda: self.client.table("leads")
                .select("id", count="exact")
                .eq("user_id", user_id)
                .gte("created_at", recent_date)
                .execute()
            )
            
            stats["recent_count"] = recent_result.count or 0
            
            return stats
            
        except Exception as e:
            logger.error(f"Error getting user stats: {str(e)}")
            return {
                "new_count": 0,
                "saved_count": 0,
                "archived_count": 0,
                "total_count": 0,
                "recent_count": 0
            }
    
    async def check_duplicate_leads(
        self, 
        user_id: str, 
        emails: List[str]
    ) -> List[str]:
        """
        Check for duplicate leads by email
        
        Args:
            user_id: User identifier
            emails: List of email addresses to check
            
        Returns:
            List of duplicate email addresses
        """
        try:
            if not emails:
                return []
            
            result = await asyncio.get_event_loop().run_in_executor(
                self.executor,
                lambda: self.client.table("leads")
                .select("email")
                .eq("user_id", user_id)
                .in_("email", emails)
                .execute()
            )
            
            existing_emails = [row["email"] for row in result.data if row.get("email")]
            return existing_emails
            
        except Exception as e:
            logger.error(f"Error checking duplicate leads: {str(e)}")
            return []

    async def check_duplicate_ids(
        self, 
        user_id: str,
        lead_ids: List[str]
    ) -> List[str]:
        """
        Check for duplicate leads by ID for a specific user
        
        Args:
            user_id: User identifier
            lead_ids: List of lead IDs to check
            
        Returns:
            List of duplicate lead IDs
        """
        try:
            if not lead_ids:
                return []
            
            result = await asyncio.get_event_loop().run_in_executor(
                self.executor,
                lambda: self.client.table("leads")
                .select("id")
                .eq("user_id", user_id)
                .in_("id", lead_ids)
                .execute()
            )
            
            existing_ids = [row["id"] for row in result.data if row.get("id")]
            return existing_ids
            
        except Exception as e:
            logger.error(f"Error checking duplicate IDs: {str(e)}")
            return []
    
    async def close(self):
        """Close the service and cleanup resources"""
        if hasattr(self, 'executor'):
            self.executor.shutdown(wait=True)

# Global Supabase service instance - initialized lazily
supabase_service = None

def get_supabase_service():
    """Get or create the global Supabase service instance"""
    global supabase_service
    if supabase_service is None:
        supabase_service = SupabaseService()
    return supabase_service