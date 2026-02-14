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

from utils.logging import logger, log_job_event, log_error
from utils.minutes import debit_minutes_sync

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
        
        # Calculate minutes used (based on narration length)
        # ~1000 characters ≈ 1 minute of video
        steps = script_data.get("steps", [])
        total_chars = sum(len(step.get("narration", "")) for step in steps)
        minutes_used = max(0.1, round(total_chars / 1000, 2))
        
        # Debit minutes from user's balance
        log_job_event(job_id, "deducting_minutes", user_id, minutes=minutes_used)
        
        debit_result = debit_minutes_sync(
            user_id=user_id,
            amount=minutes_used,
            source="job_complete",
            reference_id=job_id,  # Idempotency: same job_id = same debit
            metadata={
                "total_chars": total_chars,
                "step_count": len(steps)
            }
        )
        
        if not debit_result.success:
            # Log but don't fail the job - video was already generated
            # This handles edge cases like:
            # - User ran out of balance during generation
            # - Duplicate debit attempt (idempotent = OK)
            if debit_result.idempotent:
                log_job_event(job_id, "debit_idempotent", user_id, minutes=minutes_used)
            else:
                log_error(
                    f"Failed to debit minutes (video still delivered)",
                    job_id=job_id,
                    error=debit_result.error,
                    minutes=minutes_used
                )
        else:
            log_job_event(
                job_id, "debit_success", user_id,
                minutes=minutes_used,
                new_balance=debit_result.new_balance
            )
        
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
            "minutes_used": minutes_used,
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
