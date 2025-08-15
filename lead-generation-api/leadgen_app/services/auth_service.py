"""
Authentication service for JWT token validation
"""

import jwt
import logging
from fastapi import HTTPException, Depends, status
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from typing import Optional, Dict, Any
from datetime import datetime, timezone

from leadgen_app.config import settings

logger = logging.getLogger(__name__)
security = HTTPBearer()

class AuthService:
    """Authentication service for handling JWT tokens"""
    
    def __init__(self):
        # For Supabase JWT verification, we need the JWT secret
        # The JWT secret is typically the same as the service role key for verification
        self.jwt_secret = settings.SUPABASE_SERVICE_ROLE_KEY
        self.algorithm = "HS256"
    
    def verify_token(self, token: str) -> Dict[str, Any]:
        """
        Verify JWT token and extract user information
        
        Args:
            token: JWT token string
            
        Returns:
            Dict containing user information
            
        Raises:
            HTTPException: If token is invalid
        """
        try:
            # Decode the JWT token using the service role key as the secret
            payload = jwt.decode(
                token, 
                self.jwt_secret, 
                algorithms=[self.algorithm],
                options={"verify_exp": True}
            )
            
            # Extract user information
            user_id = payload.get("sub")
            email = payload.get("email")
            role = payload.get("role", "authenticated")
            
            if not user_id:
                raise HTTPException(
                    status_code=status.HTTP_401_UNAUTHORIZED,
                    detail="Invalid token: missing user ID"
                )
            
            logger.info(f"Token verified for user: {user_id}")
            
            return {
                "user_id": user_id,
                "email": email,
                "role": role,
                "payload": payload
            }
            
        except jwt.ExpiredSignatureError:
            logger.warning("Token has expired")
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Token has expired"
            )
        except jwt.InvalidTokenError as e:
            logger.warning(f"Invalid token: {str(e)}")
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Invalid token"
            )
        except Exception as e:
            logger.error(f"Token verification error: {str(e)}")
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Authentication failed"
            )

# Global auth service instance
auth_service = AuthService()

async def verify_jwt_token(
    credentials: HTTPAuthorizationCredentials = Depends(security)
) -> Dict[str, Any]:
    """
    FastAPI dependency for JWT token verification
    
    Args:
        credentials: HTTP authorization credentials
        
    Returns:
        Dict containing user information
    """
    if not credentials:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Authorization header required"
        )
    
    token = credentials.credentials
    return auth_service.verify_token(token)

async def get_current_user(
    user_info: Dict[str, Any] = Depends(verify_jwt_token)
) -> Dict[str, Any]:
    """
    FastAPI dependency to get current user information
    
    Args:
        user_info: User information from token verification
        
    Returns:
        Dict containing current user data
    """
    return {
        "user_id": user_info["user_id"],
        "email": user_info["email"],
        "role": user_info["role"]
    }

async def require_authenticated_user(
    user_info: Dict[str, Any] = Depends(verify_jwt_token)
) -> str:
    """
    FastAPI dependency that returns user_id for authenticated requests
    
    Args:
        user_info: User information from token verification
        
    Returns:
        User ID string
    """
    return user_info["user_id"]