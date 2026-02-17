"""
Orbital Video Routes
Handles video generation, storage, and retrieval
"""

from fastapi import APIRouter, HTTPException, Depends, Header, BackgroundTasks
from pydantic import BaseModel
from typing import Optional, List
from datetime import datetime, timedelta
import os
import uuid
from supabase import create_client, Client
from utils.emotion import count_total_narration_chars

router = APIRouter(prefix="/videos", tags=["videos"])

# Constants
CHARS_PER_MINUTE = 1000  # ~150 words/min at 6 chars/word
VIDEO_EXPIRY_HOURS = 48

# Supabase client
def get_supabase_admin() -> Client:
    url = os.environ.get("SUPABASE_URL")
    key = os.environ.get("SUPABASE_SERVICE_KEY")
    if not url or not key:
        raise HTTPException(status_code=500, detail="Supabase not configured")
    return create_client(url, key)

# ============================================
# Models
# ============================================

class PreviewRequest(BaseModel):
    problem: str
    image_base64: Optional[str] = None

class PreviewResponse(BaseModel):
    problem: str
    steps: List[dict]
    total_characters: int
    estimated_minutes: float
    cost_display: str  # "2.5 minutes"

class GenerateRequest(BaseModel):
    problem: str
    image_base64: Optional[str] = None
    # User confirms after seeing preview

class VideoResponse(BaseModel):
    id: str
    problem_text: str
    minutes_used: float
    status: str
    video_url: Optional[str]
    expires_at: str
    created_at: str

class VideoListResponse(BaseModel):
    videos: List[VideoResponse]
    total_count: int

# ============================================
# Auth dependency
# ============================================

async def get_current_user(authorization: str = Header(...)):
    """Verify JWT and return user"""
    if not authorization.startswith("Bearer "):
        raise HTTPException(status_code=401, detail="Invalid authorization header")
    
    token = authorization.replace("Bearer ", "")
    url = os.environ.get("SUPABASE_URL")
    key = os.environ.get("SUPABASE_ANON_KEY")
    supabase = create_client(url, key)
    
    try:
        user = supabase.auth.get_user(token)
        if not user or not user.user:
            raise HTTPException(status_code=401, detail="Invalid token")
        return user.user
    except Exception as e:
        raise HTTPException(status_code=401, detail=str(e))

# ============================================
# Helper Functions
# ============================================

def calculate_minutes(total_chars: int) -> float:
    """Convert character count to minutes (rounded up to 0.1)"""
    minutes = total_chars / CHARS_PER_MINUTE
    return round(minutes * 10) / 10  # Round to 1 decimal

async def parse_problem(problem: str, image_base64: Optional[str] = None) -> dict:
    """
    Parse problem with DeepSeek and return steps.
    This is the "free preview" - costs ~$0.001
    """
    # Import the parser from main module
    from parser import parse_problem as do_parse, parse_problem_from_image
    
    if image_base64:
        return await parse_problem_from_image(image_base64)
    else:
        return await do_parse(problem)

async def generate_video_task(video_id: str, user_id: str, steps: List[dict]):
    """
    Background task to generate video.
    Called after user confirms the cost.
    """
    # This would call the Manim + TTS pipeline
    # For now, placeholder
    pass

# ============================================
# Routes
# ============================================

@router.post("/preview", response_model=PreviewResponse)
async def preview_video(request: PreviewRequest, user = Depends(get_current_user)):
    """
    Parse problem and show cost preview.
    This is FREE - user sees cost before committing.
    DeepSeek parsing costs ~$0.001 (negligible)
    """
    
    try:
        # Parse the problem
        result = await parse_problem(request.problem, request.image_base64)
        
        steps = result.get("steps", [])
        
        # Calculate SPOKEN characters (excludes emotion markers like "(excited)")
        spoken_chars, total_chars = count_total_narration_chars(steps)
        
        # Calculate minutes based on spoken text only
        minutes = calculate_minutes(spoken_chars)
        
        return PreviewResponse(
            problem=result.get("problem", request.problem),
            steps=steps,
            total_characters=spoken_chars,  # Report spoken chars, not total
            estimated_minutes=minutes,
            cost_display=f"{minutes} minutes"
        )
        
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

@router.post("/generate", response_model=VideoResponse)
async def generate_video(
    request: GenerateRequest, 
    background_tasks: BackgroundTasks,
    user = Depends(get_current_user)
):
    """
    Generate video after user confirms cost.
    Deducts minutes from balance.
    """
    
    supabase = get_supabase_admin()
    
    # First, get the preview to calculate cost
    result = await parse_problem(request.problem, request.image_base64)
    steps = result.get("steps", [])
    # Use spoken chars (excludes emotion markers) for billing
    spoken_chars, total_chars = count_total_narration_chars(steps)
    minutes_needed = calculate_minutes(spoken_chars)
    
    # Check and deduct minutes
    try:
        deduct_result = supabase.rpc("deduct_minutes", {
            "p_user_id": user.id,
            "p_minutes": minutes_needed
        }).execute()
        
        if not deduct_result.data:
            raise HTTPException(
                status_code=402, 
                detail=f"Insufficient minutes. Need {minutes_needed} minutes."
            )
    except Exception as e:
        if "402" in str(e):
            raise
        raise HTTPException(status_code=400, detail=str(e))
    
    # Create video record
    video_id = str(uuid.uuid4())
    expires_at = datetime.utcnow() + timedelta(hours=VIDEO_EXPIRY_HOURS)
    
    try:
        video_data = {
            "id": video_id,
            "user_id": user.id,
            "problem_text": result.get("problem", request.problem),
            "minutes_used": minutes_needed,
            "character_count": spoken_chars,  # Spoken chars only, excludes emotion markers
            "steps_count": len(steps),
            "status": "generating",
            "expires_at": expires_at.isoformat()
        }
        
        supabase.table("videos").insert(video_data).execute()
        
    except Exception as e:
        # Refund minutes if we fail to create record
        supabase.rpc("add_minutes", {
            "p_user_id": user.id,
            "p_minutes": minutes_needed,
            "p_amount_cents": 0,
            "p_tier": "refund",
            "p_stripe_session_id": f"refund_{video_id}"
        }).execute()
        raise HTTPException(status_code=500, detail=str(e))
    
    # Queue video generation in background
    background_tasks.add_task(generate_video_task, video_id, user.id, steps)
    
    return VideoResponse(
        id=video_id,
        problem_text=result.get("problem", request.problem),
        minutes_used=minutes_needed,
        status="generating",
        video_url=None,
        expires_at=expires_at.isoformat(),
        created_at=datetime.utcnow().isoformat()
    )

@router.get("/list", response_model=VideoListResponse)
async def list_videos(
    user = Depends(get_current_user),
    limit: int = 20,
    offset: int = 0
):
    """Get user's video history (non-expired only by default)"""
    
    supabase = get_supabase_admin()
    
    try:
        # Get non-expired videos
        result = supabase.table("videos") \
            .select("*", count="exact") \
            .eq("user_id", user.id) \
            .gte("expires_at", datetime.utcnow().isoformat()) \
            .order("created_at", desc=True) \
            .range(offset, offset + limit - 1) \
            .execute()
        
        videos = [
            VideoResponse(
                id=v["id"],
                problem_text=v["problem_text"],
                minutes_used=float(v["minutes_used"]),
                status=v["status"],
                video_url=v.get("video_url"),
                expires_at=v["expires_at"],
                created_at=v["created_at"]
            )
            for v in (result.data or [])
        ]
        
        return VideoListResponse(
            videos=videos,
            total_count=result.count or 0
        )
        
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

@router.get("/{video_id}", response_model=VideoResponse)
async def get_video(video_id: str, user = Depends(get_current_user)):
    """Get single video by ID"""
    
    supabase = get_supabase_admin()
    
    try:
        result = supabase.table("videos") \
            .select("*") \
            .eq("id", video_id) \
            .eq("user_id", user.id) \
            .single() \
            .execute()
        
        if not result.data:
            raise HTTPException(status_code=404, detail="Video not found")
        
        v = result.data
        return VideoResponse(
            id=v["id"],
            problem_text=v["problem_text"],
            minutes_used=float(v["minutes_used"]),
            status=v["status"],
            video_url=v.get("video_url"),
            expires_at=v["expires_at"],
            created_at=v["created_at"]
        )
        
    except Exception as e:
        if "404" in str(e):
            raise
        raise HTTPException(status_code=400, detail=str(e))
