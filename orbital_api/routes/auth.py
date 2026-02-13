"""
Orbital Auth Routes
Uses Supabase Auth
"""

from fastapi import APIRouter, HTTPException, Depends, Header
from pydantic import BaseModel, EmailStr
from typing import Optional
import os
from supabase import create_client, Client

router = APIRouter(prefix="/auth", tags=["auth"])

# Supabase client
supabase_url = os.environ.get("SUPABASE_URL")
supabase_key = os.environ.get("SUPABASE_ANON_KEY")
supabase_service_key = os.environ.get("SUPABASE_SERVICE_KEY")

def get_supabase() -> Client:
    if not supabase_url or not supabase_key:
        raise HTTPException(status_code=500, detail="Supabase not configured")
    return create_client(supabase_url, supabase_key)

def get_supabase_admin() -> Client:
    """Service role client for admin operations"""
    if not supabase_url or not supabase_service_key:
        raise HTTPException(status_code=500, detail="Supabase not configured")
    return create_client(supabase_url, supabase_service_key)

# ============================================
# Models
# ============================================

class SignUpRequest(BaseModel):
    email: EmailStr
    password: str

class LoginRequest(BaseModel):
    email: EmailStr
    password: str

class UserResponse(BaseModel):
    id: str
    email: str
    minutes_balance: float
    created_at: str

class ProfileResponse(BaseModel):
    id: str
    email: str
    minutes_balance: float
    total_minutes_purchased: float
    total_spent_cents: int

# ============================================
# Auth dependency
# ============================================

async def get_current_user(authorization: str = Header(...)):
    """Verify JWT and return user"""
    if not authorization.startswith("Bearer "):
        raise HTTPException(status_code=401, detail="Invalid authorization header")
    
    token = authorization.replace("Bearer ", "")
    supabase = get_supabase()
    
    try:
        # Verify token with Supabase
        user = supabase.auth.get_user(token)
        if not user or not user.user:
            raise HTTPException(status_code=401, detail="Invalid token")
        return user.user
    except Exception as e:
        raise HTTPException(status_code=401, detail=str(e))

# ============================================
# Routes
# ============================================

@router.post("/signup")
async def signup(request: SignUpRequest):
    """Create new account"""
    supabase = get_supabase()
    
    try:
        result = supabase.auth.sign_up({
            "email": request.email,
            "password": request.password
        })
        
        if result.user:
            return {
                "success": True,
                "user": {
                    "id": result.user.id,
                    "email": result.user.email
                },
                "session": {
                    "access_token": result.session.access_token if result.session else None,
                    "refresh_token": result.session.refresh_token if result.session else None
                }
            }
        else:
            raise HTTPException(status_code=400, detail="Signup failed")
            
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

@router.post("/login")
async def login(request: LoginRequest):
    """Login with email/password"""
    supabase = get_supabase()
    
    try:
        result = supabase.auth.sign_in_with_password({
            "email": request.email,
            "password": request.password
        })
        
        if result.user and result.session:
            # Get profile with minutes balance
            profile = supabase.table("profiles").select("*").eq("id", result.user.id).single().execute()
            
            return {
                "success": True,
                "user": {
                    "id": result.user.id,
                    "email": result.user.email,
                    "minutes_balance": profile.data.get("minutes_balance", 0) if profile.data else 0
                },
                "session": {
                    "access_token": result.session.access_token,
                    "refresh_token": result.session.refresh_token,
                    "expires_at": result.session.expires_at
                }
            }
        else:
            raise HTTPException(status_code=401, detail="Invalid credentials")
            
    except Exception as e:
        raise HTTPException(status_code=401, detail=str(e))

@router.post("/logout")
async def logout(authorization: str = Header(...)):
    """Logout / invalidate session"""
    supabase = get_supabase()
    token = authorization.replace("Bearer ", "")
    
    try:
        supabase.auth.sign_out()
        return {"success": True}
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

@router.get("/me", response_model=ProfileResponse)
async def get_profile(user = Depends(get_current_user)):
    """Get current user profile with minutes balance"""
    supabase = get_supabase()
    
    try:
        profile = supabase.table("profiles").select("*").eq("id", user.id).single().execute()
        
        if not profile.data:
            raise HTTPException(status_code=404, detail="Profile not found")
        
        return ProfileResponse(
            id=profile.data["id"],
            email=profile.data["email"],
            minutes_balance=float(profile.data.get("minutes_balance", 0)),
            total_minutes_purchased=float(profile.data.get("total_minutes_purchased", 0)),
            total_spent_cents=profile.data.get("total_spent_cents", 0)
        )
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

@router.post("/refresh")
async def refresh_token(refresh_token: str):
    """Refresh access token"""
    supabase = get_supabase()
    
    try:
        result = supabase.auth.refresh_session(refresh_token)
        
        if result.session:
            return {
                "success": True,
                "session": {
                    "access_token": result.session.access_token,
                    "refresh_token": result.session.refresh_token,
                    "expires_at": result.session.expires_at
                }
            }
        else:
            raise HTTPException(status_code=401, detail="Invalid refresh token")
            
    except Exception as e:
        raise HTTPException(status_code=401, detail=str(e))
