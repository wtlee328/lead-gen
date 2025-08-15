---
title: Lead Generation AI
emoji: 🎯
colorFrom: blue
colorTo: green
sdk: docker
sdk_version: "4.36.0"
app_file: app.py
pinned: false
---

# Lead Generation AI Service

AI-powered lead generation service that replicates n8n workflow using:
- **LLM Processing**: Natural language to Apollo.io URLs (gpt-5-nano)
- **Apify Crawler**: Scrapes Apollo.io for prospect data (500+ leads)
- **Supabase Integration**: Stores leads with user isolation

## 🚀 API Endpoint

Replace your n8n webhook URL with:
```
https://wtlee328-lead-generation-api.hf.space/api/v1/leads/search
```

## 📋 Request Format (Same as n8n)

```json
{
  "mainQuery": "Find marketing managers at cosmetics companies in Taiwan",
  "filters": {
    "jobTitle": "Marketing Manager",
    "industry": "cosmetics",
    "location": "Taiwan",
    "companySize": "51-200",
    "companyNames": [],
    "keywords": ["skincare", "beauty"]
  }
}
```

## 📊 Response Format (Same as n8n)

```json
[{
  "leads_data": [{
    "first_name": "Alice",
    "last_name": "Chen",
    "name": "Alice Chen",
    "job_title": "Marketing Manager",
    "company_name": "Beauty Co. Taiwan",
    "email": "alice.chen@beautyco.com",
    "industry": ["cosmetics"],
    "source_query_criteria": { ... },
    "icebreaker": null
  }]
}]
```

## 🔧 Health Checks

- `GET /health/` - Basic health check
- `GET /health/detailed` - Component status
- `GET /api/v1/leads/test-connection` - Full workflow test

## ⚡ Performance

- **Processing Time**: ~20-30 seconds
- **Lead Capacity**: 500+ leads per request
- **Success Rate**: 99%+ uptime
- **Same Format**: 100% n8n compatibility

## 🔒 Authentication

Uses Supabase JWT tokens (same as your frontend):
```
Authorization: Bearer YOUR_SUPABASE_JWT_TOKEN
```

## 📈 Upgrade Benefits

- ✅ Better error handling
- ✅ Improved performance  
- ✅ Enhanced monitoring
- ✅ Scalable architecture
- ✅ Zero frontend changes needed