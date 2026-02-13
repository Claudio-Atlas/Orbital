"""
Shared authentication utilities for Orbital API.
"""

import os
from fastapi import HTTPException, Header, Depends
from supabase import create_client


async def get_current_user(authorization: str = Header(...)):
    """
    Verify JWT token and return the authenticated user.
    
    Usage:
        @app.get("/protected")
        async def protected_route(user = Depends(get_current_user)):
            return {"user_id": user.id}
    """
    if not authorization.startswith("Bearer "):
        raise HTTPException(status_code=401, detail="Invalid authorization header")
    
    token = authorization.replace("Bearer ", "")
    url = os.environ.get("SUPABASE_URL")
    key = os.environ.get("SUPABASE_ANON_KEY")
    
    if not url or not key:
        raise HTTPException(status_code=500, detail="Auth not configured")
    
    supabase = create_client(url, key)
    
    try:
        user = supabase.auth.get_user(token)
        if not user or not user.user:
            raise HTTPException(status_code=401, detail="Invalid token")
        return user.user
    except Exception as e:
        # Don't leak internal error details
        raise HTTPException(status_code=401, detail="Authentication failed")


async def get_optional_user(authorization: str = Header(None)):
    """
    Like get_current_user but returns None if no auth header.
    Useful for endpoints that work differently for logged-in vs anonymous users.
    """
    if not authorization:
        return None
    return await get_current_user(authorization)
