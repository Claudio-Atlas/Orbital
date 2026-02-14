"""
Celery Tasks
============
These are the "chefs" - the actual work that gets done.

Each task is a function that:
1. Gets picked up from the queue
2. Does the heavy lifting (render video, call APIs, etc.)
3. Reports back when done

The API just drops tasks onto the queue and walks away.
Workers pick them up whenever they're free.
"""

import os
import sys
import json
import subprocess
from pathlib import Path
from datetime import datetime

from celery import states
from celery_app import celery_app

# Paths
API_DIR = Path(__file__).parent
OUTPUT_PATH = API_DIR / "output"
SCRIPTS_PATH = API_DIR / "scripts"
FACTORY_PATH = API_DIR.parent / "orbital_factory"

# Ensure directories exist
OUTPUT_PATH.mkdir(exist_ok=True)
SCRIPTS_PATH.mkdir(exist_ok=True)


@celery_app.task(bind=True, name="tasks.generate_video")
def generate_video(self, job_id: str, script_data: dict, voice: str, user_id: str):
    """
    Generate a video from parsed problem data.
    
    This is the "chef making the pizza":
    1. Save the script to a file
    2. Run the Manim + audio pipeline
    3. Upload to R2 (TODO)
    4. Return the video URL
    
    Args:
        job_id: Unique identifier for this job
        script_data: Parsed problem with steps, latex, narration
        voice: Voice ID for Fish Audio
        user_id: Who requested this (for billing, access control)
    
    Returns:
        dict with status, video_url, or error
    """
    
    try:
        # Update task state to "STARTED" with progress info
        self.update_state(
            state="PROCESSING",
            meta={
                "job_id": job_id,
                "step": "preparing",
                "progress": 10,
                "message": "Preparing video script..."
            }
        )
        
        # Save script to file
        script_path = SCRIPTS_PATH / f"{job_id}.json"
        with open(script_path, "w") as f:
            json.dump(script_data, f, indent=2)
        
        # Update progress
        self.update_state(
            state="PROCESSING",
            meta={
                "job_id": job_id,
                "step": "rendering",
                "progress": 30,
                "message": "Rendering video with Manim..."
            }
        )
        
        # Run the pipeline
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
            timeout=540  # 9 minute timeout (soft limit)
        )
        
        if result.returncode != 0:
            raise Exception(f"Pipeline failed: {result.stderr[:500]}")
        
        # Check video was created
        video_path = OUTPUT_PATH / f"{job_id}.mp4"
        if not video_path.exists():
            # Check factory output as fallback
            factory_output = FACTORY_PATH / "output" / f"{job_id}.mp4"
            if factory_output.exists():
                # Move to API output
                import shutil
                shutil.move(str(factory_output), str(video_path))
            else:
                raise Exception("Video file not created")
        
        # TODO: Upload to Cloudflare R2
        # video_url = upload_to_r2(video_path, f"videos/{user_id}/{job_id}.mp4")
        
        # For now, serve locally
        video_url = f"/videos/{job_id}.mp4"
        
        # Update progress
        self.update_state(
            state="PROCESSING",
            meta={
                "job_id": job_id,
                "step": "complete",
                "progress": 100,
                "message": "Video ready!"
            }
        )
        
        return {
            "status": "complete",
            "job_id": job_id,
            "video_url": video_url,
            "completed_at": datetime.now().isoformat()
        }
        
    except subprocess.TimeoutExpired:
        return {
            "status": "failed",
            "job_id": job_id,
            "error": "Video generation timed out (>9 minutes)",
            "completed_at": datetime.now().isoformat()
        }
        
    except Exception as e:
        return {
            "status": "failed",
            "job_id": job_id,
            "error": str(e),
            "completed_at": datetime.now().isoformat()
        }


@celery_app.task(bind=True, name="tasks.parse_problem_task")
def parse_problem_task(self, problem: str = None, image_b64: str = None):
    """
    Parse a problem (text or image) into structured steps.
    
    This is lighter than video generation - just calls GPT.
    Could run on the "fast" queue.
    
    Returns:
        Parsed script data with steps, latex, etc.
    """
    from parser import parse_problem, parse_problem_from_image
    
    try:
        if image_b64:
            script_data, extracted_problem = parse_problem_from_image(image_b64)
            return {
                "status": "success",
                "problem": extracted_problem,
                "script_data": script_data
            }
        else:
            script_data = parse_problem(problem)
            return {
                "status": "success", 
                "problem": problem,
                "script_data": script_data
            }
            
    except Exception as e:
        return {
            "status": "failed",
            "error": str(e)
        }
