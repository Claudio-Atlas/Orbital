"""
Orbital Solver API
==================
FastAPI backend for the Orbital video solver.

Architecture (Pizza Shop Analogy):
- This API = The waiter (takes orders, gives tickets)
- Redis + Celery = The order rail + kitchen (processes in background)  
- Workers = The chefs (can scale independently)

Endpoints:
- POST /solve - Submit a problem → returns job ticket
- GET /job/{job_id} - Check job status (polling)
- POST /parse - Parse only (free, for cost preview)
- GET /health - Health check
"""

from dotenv import load_dotenv
load_dotenv()

import os
import uuid
from pathlib import Path
from datetime import datetime
from typing import Optional
from contextlib import asynccontextmanager

from fastapi import FastAPI, HTTPException, Depends
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from pydantic import BaseModel

from routes.payments import router as payments_router
from utils.auth import get_current_user
from utils.rate_limit import rate_limit
from utils.logging import logger, log_job_event, log_error
from utils.alerts import alert_error_async, AlertHandler
from utils.emotion import count_total_narration_chars
from middleware.request_log import RequestLoggingMiddleware
from parser import parse_problem, parse_problem_from_image
from jobs import job_store

# Paths
API_DIR = Path(__file__).parent
OUTPUT_PATH = API_DIR / "output"
SCRIPTS_PATH = API_DIR / "scripts"

# Create directories
OUTPUT_PATH.mkdir(exist_ok=True)
SCRIPTS_PATH.mkdir(exist_ok=True)

# Check if Celery is available (workers running)
CELERY_ENABLED = os.getenv("CELERY_ENABLED", "false").lower() == "true"

if CELERY_ENABLED:
    from tasks import generate_video


# ============================================
# Request/Response Models
# ============================================

class SolveRequest(BaseModel):
    problem: Optional[str] = None
    image: Optional[str] = None
    voice: str = "allison"


class SolveResponse(BaseModel):
    job_id: str
    status: str
    message: str


class JobStatus(BaseModel):
    job_id: str
    status: str  # pending, processing, complete, failed
    problem: Optional[str] = None
    steps: Optional[list] = None
    video_url: Optional[str] = None
    error: Optional[str] = None
    progress: Optional[int] = None
    progress_message: Optional[str] = None
    created_at: str
    completed_at: Optional[str] = None


class ParseRequest(BaseModel):
    problem: Optional[str] = None
    image: Optional[str] = None


class ParseResponse(BaseModel):
    problem: str
    latex: Optional[str] = None
    steps: list
    total_characters: int
    estimated_minutes: float


# ============================================
# App Setup
# ============================================

@asynccontextmanager
async def lifespan(app: FastAPI):
    OUTPUT_PATH.mkdir(exist_ok=True)
    SCRIPTS_PATH.mkdir(exist_ok=True)
    mode = "Celery workers" if CELERY_ENABLED else "BackgroundTasks (local)"
    logger.info("🚀 Orbital API started", extra={
        "event": "startup",
        "mode": mode,
        "celery_enabled": CELERY_ENABLED,
        "output_path": str(OUTPUT_PATH)
    })
    yield
    logger.info("👋 Orbital API shutting down", extra={"event": "shutdown"})


app = FastAPI(
    title="Orbital Solver API",
    description="Generate step-by-step math tutorial videos",
    version="2.0.0",
    lifespan=lifespan
)

# CORS
ALLOWED_ORIGINS = [
    "http://localhost:3000",
    "http://localhost:3001",
    "https://orbital-lime.vercel.app",
    "https://orbitalsolver.io",
    "https://www.orbitalsolver.io",
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=ALLOWED_ORIGINS,
    allow_credentials=True,
    allow_methods=["GET", "POST", "PUT", "DELETE", "OPTIONS"],
    allow_headers=["Authorization", "Content-Type"],
)

# Request logging middleware (after CORS so it sees all requests)
app.add_middleware(RequestLoggingMiddleware)

# Serve generated videos
app.mount("/videos", StaticFiles(directory=str(OUTPUT_PATH)), name="videos")

# Include routers
app.include_router(payments_router)


# ============================================
# Fallback: Local processing (no Celery)
# ============================================

def run_pipeline_sync(job_id: str, script_data: dict, voice: str):
    """
    Synchronous pipeline for local dev (when Celery not running).
    This blocks - only use for development!
    """
    import subprocess
    import sys
    import json
    
    FACTORY_PATH = API_DIR.parent / "orbital_factory"
    store = job_store()
    
    try:
        store.update(job_id, status="processing", started_at=datetime.now().isoformat())
        
        # Save script
        script_path = SCRIPTS_PATH / f"{job_id}.json"
        with open(script_path, "w") as f:
            json.dump(script_data, f, indent=2)
        
        # Run pipeline
        cmd = [
            sys.executable,
            str(FACTORY_PATH / "pipeline.py"),
            str(script_path),
            "--voice", voice,
            "--output", f"{job_id}.mp4"
        ]
        
        result = subprocess.run(
            cmd,
            cwd=str(FACTORY_PATH),
            capture_output=True,
            text=True,
            timeout=300
        )
        
        if result.returncode != 0:
            raise Exception(f"Pipeline failed: {result.stderr}")
        
        video_path = OUTPUT_PATH / f"{job_id}.mp4"
        if not video_path.exists():
            factory_output = FACTORY_PATH / "output" / f"{job_id}.mp4"
            if factory_output.exists():
                import shutil
                shutil.move(str(factory_output), str(video_path))
            else:
                raise Exception("Video file not created")
        
        store.update(
            job_id,
            status="complete",
            video_url=f"/videos/{job_id}.mp4",
            completed_at=datetime.now().isoformat()
        )
        
    except Exception as e:
        store.update(
            job_id,
            status="failed",
            error=str(e),
            completed_at=datetime.now().isoformat()
        )


# ============================================
# Endpoints
# ============================================

@app.get("/health")
async def health(detailed: bool = False):
    """
    Health check endpoint.
    
    Query params:
        detailed=true — Include component health checks (slower)
    """
    store = job_store()
    
    # Basic health info (always fast)
    health_data = {
        "status": "healthy",
        "service": "orbital-solver",
        "version": "2.0.0",
        "celery_enabled": CELERY_ENABLED,
        "job_store": type(store).__name__,
        "timestamp": datetime.now().isoformat()
    }
    
    if not detailed:
        return health_data
    
    # Detailed component checks
    components = {}
    overall_healthy = True
    
    # Check Redis
    try:
        from utils.rate_limit import get_redis
        redis = get_redis()
        redis.get("health_check")  # Simple read test
        components["redis"] = {"status": "healthy", "type": type(redis).__name__}
    except Exception as e:
        components["redis"] = {"status": "unhealthy", "error": str(e)[:100]}
        overall_healthy = False
    
    # Check Supabase
    try:
        import httpx
        supabase_url = os.getenv("SUPABASE_URL")
        if supabase_url:
            # Just check if URL is reachable
            async with httpx.AsyncClient(timeout=5.0) as client:
                resp = await client.get(f"{supabase_url}/rest/v1/", headers={
                    "apikey": os.getenv("SUPABASE_ANON_KEY", ""),
                })
                components["supabase"] = {
                    "status": "healthy" if resp.status_code < 500 else "degraded",
                    "response_code": resp.status_code
                }
        else:
            components["supabase"] = {"status": "unconfigured"}
    except Exception as e:
        components["supabase"] = {"status": "unhealthy", "error": str(e)[:100]}
        overall_healthy = False
    
    # Check Celery (if enabled)
    if CELERY_ENABLED:
        try:
            from celery_app import celery_app
            inspector = celery_app.control.inspect(timeout=2.0)
            active = inspector.active()
            if active:
                worker_count = sum(len(tasks) for tasks in active.values())
                components["celery"] = {
                    "status": "healthy",
                    "workers": len(active),
                    "active_tasks": worker_count
                }
            else:
                components["celery"] = {"status": "no_workers"}
                # Not necessarily unhealthy - workers might be idle
        except Exception as e:
            components["celery"] = {"status": "unhealthy", "error": str(e)[:100]}
            overall_healthy = False
    else:
        components["celery"] = {"status": "disabled"}
    
    health_data["components"] = components
    health_data["status"] = "healthy" if overall_healthy else "degraded"
    
    return health_data


@app.post("/solve", response_model=SolveResponse)
@rate_limit(requests=5, window=60)  # 5 per minute - expensive operation
async def solve(request: SolveRequest, user = Depends(get_current_user)):
    """
    Submit a math problem to solve.
    
    The "waiter taking your order":
    1. Validates the order (parses the problem)
    2. Writes a ticket (creates job record)
    3. Puts ticket on the rail (queues Celery task)
    4. Gives you a ticket number (returns job_id)
    
    You then poll GET /job/{job_id} to check when it's ready.
    """
    
    if not request.problem and not request.image:
        raise HTTPException(400, "Must provide either 'problem' or 'image'")
    
    job_id = str(uuid.uuid4())[:8]
    user_id = user.get("sub", "anonymous")
    
    try:
        # Parse the problem
        if request.image:
            script_data, extracted_problem = parse_problem_from_image(request.image)
            problem_text = extracted_problem
        else:
            script_data = parse_problem(request.problem)
            problem_text = request.problem
        
        # Add metadata
        script_data["meta"]["brand"] = "Orbital"
        script_data["meta"]["job_id"] = job_id
        
        steps = script_data.get("steps", [])
        
        # Create job record
        store = job_store()
        store.create(
            job_id=job_id,
            user_id=user_id,
            problem=problem_text,
            steps=steps
        )
        
        # Log job creation
        log_job_event(job_id, "created", user_id, step_count=len(steps))
        
        # Queue the task
        if CELERY_ENABLED:
            # Send to Celery worker (async, non-blocking)
            task = generate_video.delay(job_id, script_data, request.voice, user_id)
            store.update(job_id, celery_task_id=task.id)
            log_job_event(job_id, "queued", user_id, celery_task_id=task.id)
        else:
            # Local dev: run in background thread
            import threading
            thread = threading.Thread(
                target=run_pipeline_sync,
                args=(job_id, script_data, request.voice)
            )
            thread.start()
            log_job_event(job_id, "queued_local", user_id)
        
        return SolveResponse(
            job_id=job_id,
            status="pending",
            message=f"Video queued: {problem_text[:50]}..."
        )
        
    except Exception as e:
        log_error(f"Failed to parse/queue problem", error=e, job_id=job_id if 'job_id' in dir() else None)
        await alert_error_async("Solve endpoint failed", error=str(e)[:200])
        raise HTTPException(500, f"Failed to parse problem: {str(e)}")


@app.get("/job/{job_id}", response_model=JobStatus)
@rate_limit(requests=60, window=60)  # 60 per minute - polling endpoint
async def get_job(job_id: str, user = Depends(get_current_user)):
    """
    Check job status.
    
    The "order status board":
    - pending: In queue, waiting for a chef
    - processing: Chef is working on it
    - complete: Ready! Here's your video URL
    - failed: Something went wrong
    """
    
    store = job_store()
    job = store.get(job_id)
    
    if not job:
        raise HTTPException(404, f"Job {job_id} not found")
    
    # Security: Verify job belongs to this user
    user_id = user.get("sub", "anonymous")
    if job.get("user_id") != user_id:
        raise HTTPException(403, "Not authorized to view this job")
    
    # If Celery, check task status for real-time progress
    progress = None
    progress_message = None
    
    if CELERY_ENABLED and job.get("celery_task_id"):
        from celery.result import AsyncResult
        task_result = AsyncResult(job["celery_task_id"])
        
        if task_result.state == "PROCESSING":
            info = task_result.info or {}
            progress = info.get("progress", 0)
            progress_message = info.get("message", "Processing...")
        elif task_result.state == "SUCCESS":
            result = task_result.result or {}
            if result.get("status") == "complete":
                store.update(
                    job_id,
                    status="complete",
                    video_url=result.get("video_url"),
                    completed_at=result.get("completed_at")
                )
                job = store.get(job_id)
        elif task_result.state == "FAILURE":
            store.update(
                job_id,
                status="failed",
                error=str(task_result.result),
                completed_at=datetime.now().isoformat()
            )
            job = store.get(job_id)
    
    return JobStatus(
        job_id=job["job_id"],
        status=job["status"],
        problem=job.get("problem"),
        steps=job.get("steps"),
        video_url=job.get("video_url"),
        error=job.get("error"),
        progress=progress,
        progress_message=progress_message,
        created_at=job.get("created_at", datetime.now().isoformat()),
        completed_at=job.get("completed_at")
    )


@app.post("/parse", response_model=ParseResponse)
@rate_limit(requests=20, window=60)  # 20 per minute - AI call but no render
async def parse_only(request: ParseRequest, user = Depends(get_current_user)):
    """
    Parse a problem WITHOUT generating video.
    
    This is FREE - used for the verification screen.
    User sees the parsed steps and cost estimate before confirming.
    """
    
    if not request.problem and not request.image:
        raise HTTPException(400, "Must provide either 'problem' or 'image'")
    
    try:
        if request.image:
            script_data, extracted_problem = parse_problem_from_image(request.image)
            problem_text = extracted_problem
        else:
            script_data = parse_problem(request.problem)
            problem_text = request.problem
        
        steps = script_data.get("steps", [])
        # Count spoken chars (excludes emotion markers like "(excited)")
        spoken_chars, total_chars = count_total_narration_chars(steps)
        estimated_minutes = max(0.1, round(spoken_chars / 1000, 1))
        
        return ParseResponse(
            problem=problem_text,
            latex=script_data.get("meta", {}).get("latex"),
            steps=steps,
            total_characters=spoken_chars,  # Report spoken chars, not total
            estimated_minutes=estimated_minutes
        )
        
    except Exception as e:
        raise HTTPException(500, f"Failed to parse problem: {str(e)}")


@app.get("/jobs")
@rate_limit(requests=30, window=60)  # 30 per minute - database read
async def list_jobs(user = Depends(get_current_user), limit: int = 20):
    """
    List your recent jobs.
    """
    user_id = user.get("sub", "anonymous")
    store = job_store()
    jobs = store.get_user_jobs(user_id, limit=limit)
    return {"jobs": jobs}


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
