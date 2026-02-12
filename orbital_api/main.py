"""
Orbital Solver API
==================
FastAPI backend for the Orbital video solver.

Endpoints:
- POST /solve - Submit a problem (text or image)
- GET /job/{job_id} - Check job status and get video URL
- GET /health - Health check
"""

# Load environment variables from .env file
from dotenv import load_dotenv
load_dotenv()

import os
import sys
import json
import uuid
import asyncio
from pathlib import Path
from datetime import datetime
from typing import Optional
from contextlib import asynccontextmanager

from fastapi import FastAPI, HTTPException, BackgroundTasks, Depends
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from pydantic import BaseModel

from routes.payments import router as payments_router
from utils.auth import get_current_user

# Add parent directory to path for imports
sys.path.insert(0, str(Path(__file__).parent.parent / "orbital_factory"))

from parser import parse_problem, parse_problem_from_image

# Job storage (in-memory for now, use Redis/DB for production)
jobs = {}

# Paths
FACTORY_PATH = Path(__file__).parent.parent / "orbital_factory"
OUTPUT_PATH = FACTORY_PATH / "output"
SCRIPTS_PATH = FACTORY_PATH / "scripts"


class SolveRequest(BaseModel):
    problem: Optional[str] = None  # Text problem
    image: Optional[str] = None     # Base64 image
    voice: str = "allison"          # Voice choice


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
    created_at: str
    completed_at: Optional[str] = None


@asynccontextmanager
async def lifespan(app: FastAPI):
    # Startup
    OUTPUT_PATH.mkdir(exist_ok=True)
    SCRIPTS_PATH.mkdir(exist_ok=True)
    print(f"🚀 Orbital API started")
    print(f"   Factory: {FACTORY_PATH}")
    print(f"   Output: {OUTPUT_PATH}")
    yield
    # Shutdown
    print("👋 Orbital API shutting down")


app = FastAPI(
    title="Orbital Solver API",
    description="Generate step-by-step math tutorial videos",
    version="1.0.0",
    lifespan=lifespan
)

# CORS for frontend
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Tighten for production
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Serve generated videos
app.mount("/videos", StaticFiles(directory=str(OUTPUT_PATH)), name="videos")

# Include routers
app.include_router(payments_router)


def run_pipeline(job_id: str, script_data: dict, voice: str):
    """
    Run the video generation pipeline.
    This runs in a background thread.
    """
    import subprocess
    
    try:
        jobs[job_id]["status"] = "processing"
        
        # Save script to file
        script_path = SCRIPTS_PATH / f"{job_id}.json"
        with open(script_path, "w") as f:
            json.dump(script_data, f, indent=2)
        
        # Run pipeline
        cmd = [
            sys.executable,  # Current Python interpreter
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
            timeout=300  # 5 minute timeout
        )
        
        if result.returncode != 0:
            raise Exception(f"Pipeline failed: {result.stderr}")
        
        # Check if video was created
        video_path = OUTPUT_PATH / f"{job_id}.mp4"
        if not video_path.exists():
            raise Exception("Video file not created")
        
        # Update job
        jobs[job_id]["status"] = "complete"
        jobs[job_id]["video_url"] = f"/videos/{job_id}.mp4"
        jobs[job_id]["completed_at"] = datetime.now().isoformat()
        
    except Exception as e:
        jobs[job_id]["status"] = "failed"
        jobs[job_id]["error"] = str(e)
        jobs[job_id]["completed_at"] = datetime.now().isoformat()


@app.get("/health")
async def health():
    """Health check endpoint."""
    return {
        "status": "healthy",
        "service": "orbital-solver",
        "jobs_in_memory": len(jobs)
    }


@app.post("/solve", response_model=SolveResponse)
async def solve(
    request: SolveRequest, 
    background_tasks: BackgroundTasks,
    user = Depends(get_current_user)
):
    """
    Submit a math problem to solve.
    Requires authentication.
    
    Provide either:
    - problem: Text description of the problem
    - image: Base64-encoded image of the problem
    """
    
    if not request.problem and not request.image:
        raise HTTPException(400, "Must provide either 'problem' or 'image'")
    
    job_id = str(uuid.uuid4())[:8]
    
    try:
        # Parse the problem
        if request.image:
            # OCR + parse
            script_data, extracted_problem = parse_problem_from_image(request.image)
            problem_text = extracted_problem
        else:
            # Direct parse
            script_data = parse_problem(request.problem)
            problem_text = request.problem
        
        # Add meta info
        script_data["meta"]["brand"] = "Orbital"
        script_data["meta"]["job_id"] = job_id
        
        # Create job record
        jobs[job_id] = {
            "job_id": job_id,
            "status": "pending",
            "problem": problem_text,
            "steps": script_data.get("steps", []),
            "video_url": None,
            "error": None,
            "created_at": datetime.now().isoformat(),
            "completed_at": None
        }
        
        # Start pipeline in background
        background_tasks.add_task(run_pipeline, job_id, script_data, request.voice)
        
        return SolveResponse(
            job_id=job_id,
            status="pending",
            message=f"Problem received. Generating video for: {problem_text[:50]}..."
        )
        
    except Exception as e:
        raise HTTPException(500, f"Failed to parse problem: {str(e)}")


class ParseRequest(BaseModel):
    problem: Optional[str] = None
    image: Optional[str] = None


class ParseResponse(BaseModel):
    problem: str
    latex: Optional[str] = None
    steps: list
    total_characters: int
    estimated_minutes: float


@app.post("/parse", response_model=ParseResponse)
async def parse_only(request: ParseRequest, user = Depends(get_current_user)):
    """
    Parse a problem WITHOUT generating video.
    Requires authentication.
    
    This is FREE (doesn't deduct minutes) - used for the verification screen.
    User sees the parsed result and cost before confirming.
    
    Returns:
    - problem: The problem text (extracted if from image)
    - latex: LaTeX representation of the problem
    - steps: List of {narration, latex} steps
    - total_characters: Total narration characters (for cost calc)
    - estimated_minutes: Estimated video length (chars / 1000)
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
        
        # Calculate total characters (for cost estimation)
        total_chars = sum(len(step.get("narration", "")) for step in steps)
        
        # 1000 chars = 1 minute
        estimated_minutes = round(total_chars / 1000, 1)
        estimated_minutes = max(0.1, estimated_minutes)  # Minimum 0.1 min
        
        # Get latex for the problem if available
        problem_latex = script_data.get("meta", {}).get("latex")
        
        return ParseResponse(
            problem=problem_text,
            latex=problem_latex,
            steps=steps,
            total_characters=total_chars,
            estimated_minutes=estimated_minutes
        )
        
    except Exception as e:
        raise HTTPException(500, f"Failed to parse problem: {str(e)}")


@app.get("/job/{job_id}", response_model=JobStatus)
async def get_job(job_id: str, user = Depends(get_current_user)):
    """Get the status of a solve job. Requires authentication."""
    
    if job_id not in jobs:
        raise HTTPException(404, f"Job {job_id} not found")
    
    # TODO: Verify job belongs to this user when we add user_id to jobs
    return JobStatus(**jobs[job_id])


# REMOVED: /jobs debug endpoint - exposed all user data
# If needed for admin, add proper admin auth first


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
