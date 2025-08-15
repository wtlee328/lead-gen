# HuggingFace Spaces Setup Instructions

## Required Environment Variables

To run this Lead Generation API on HuggingFace Spaces, you need to configure the following environment variables in your Space settings:

### 1. Go to your Space Settings
Visit: https://huggingface.co/spaces/wtlee328/lead-generation-api/settings

### 2. Add Repository Secrets
Click on "Repository secrets" and add the following variables:

#### Application Configuration
```
APP_NAME=Lead Generation AI Service
VERSION=1.0.0
ENVIRONMENT=production
PORT=7860
LOG_LEVEL=INFO
```

#### Security
```
JWT_SECRET_KEY=your-jwt-secret-key-for-testing
ALLOWED_ORIGINS=["*"]
ALLOWED_HOSTS=["*"]
```

#### Supabase Configuration
```
SUPABASE_URL=https://zpfozexgfpquxzhfgjdf.supabase.co
SUPABASE_SERVICE_ROLE_KEY=eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJzdXBhYmFzZSIsInJlZiI6InpwZm96ZXhnZnBxdXh6aGZnamRmIiwicm9sZSI6InNlcnZpY2Vfcm9sZSIsImlhdCI6MTc0NjgxNTY1OSwiZXhwIjoyMDYyMzkxNjU5fQ.RPyh67evW_asyZ9BWyEpyiPeVgivrqlvWf3ub1-IxSA
SUPABASE_JWT_SECRET=RPyh67evW_asyZ9BWyEpyiPeVgivrqlvWf3ub1-IxSA
```

#### AI Services
```
OPENAI_API_KEY=your-openai-api-key-here
```

#### Apify
```
APIFY_API_TOKEN=your-apify-api-token-here
```

#### Processing Limits
```
MAX_LEADS_PER_REQUEST=10
REQUEST_TIMEOUT=300
DATABASE_POOL_SIZE=5
DATABASE_MAX_OVERFLOW=10
```

### 3. Restart the Space
After adding all environment variables, restart your Space to apply the changes.

### 4. Test the Deployment
Once the Space is running, test these endpoints:

- **Health Check**: `https://wtlee328-lead-generation-api.hf.space/health/`
- **API Documentation**: `https://wtlee328-lead-generation-api.hf.space/docs` (if enabled)
- **Lead Search**: `https://wtlee328-lead-generation-api.hf.space/api/v1/leads/search`

### 5. API Usage
```bash
# Test with curl
curl -X POST "https://wtlee328-lead-generation-api.hf.space/api/v1/leads/search" \
  -H "Authorization: Bearer YOUR_SUPABASE_JWT_TOKEN" \
  -H "Content-Type: application/json" \
  -d '{
    "mainQuery": "Find marketing managers at cosmetics companies in Taiwan",
    "filters": {"industry": "cosmetics", "location": "Taiwan"}
  }'
```

## Notes
- The Space will automatically rebuild when you push changes to the repository
- Environment variables are securely stored and not visible in the public repository
- Port 7860 is required for HuggingFace Spaces