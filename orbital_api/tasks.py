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
from utils.emotion import count_total_narration_chars

# Paths
API_DIR = Path(__file__).parent
OUTPUT_PATH = API_DIR / "output"
SCRIPTS_PATH = API_DIR / "scripts"
FACTORY_PATH = API_DIR.parent / "orbital_factory"

# Ensure directories exist
OUTPUT_PATH.mkdir(exist_ok=True)
SCRIPTS_PATH.mkdir(exist_ok=True)


@celery_app.task(bind=True, name="tasks.verify_proof")
def verify_proof_task(self, job_id: str, script_data: dict):
    """
    Verify mathematical claims in a proof script using DeepSeek Prover + Lean 4.
    
    This runs BEFORE video generation for proof-type content.
    Uses the local verification pipeline (7B prover + Lean 4 + exact?/apply? fallback).
    
    For non-proof content (basic problem solving), this is skipped.
    
    Args:
        job_id: Unique identifier for this job
        script_data: Parsed problem with steps, meta, etc.
    
    Returns:
        dict with verification status, claims checked, and any failures
    """
    try:
        self.update_state(
            state="VERIFYING",
            meta={
                "job_id": job_id,
                "step": "verification",
                "progress": 5,
                "message": "Verifying mathematical correctness..."
            }
        )
        
        meta = script_data.get("meta", {})
        product_family = meta.get("product_family", "").lower()
        
        # Only run verification for proof/theorem content
        if "proof" not in product_family and "theorem" not in product_family:
            return {
                "status": "skipped",
                "job_id": job_id,
                "reason": "Not a proof-type video",
                "verified": True
            }
        
        # Save script temporarily for verification
        script_path = SCRIPTS_PATH / f"{job_id}_verify.json"
        with open(script_path, "w") as f:
            json.dump(script_data, f, indent=2)
        
        # Run verify_proof.py
        cmd = [
            sys.executable,
            str(FACTORY_PATH / "verify_proof.py"),
            "--file", str(script_path)
        ]
        
        result = subprocess.run(
            cmd,
            cwd=str(FACTORY_PATH),
            capture_output=True,
            text=True,
            timeout=300  # 5 minute timeout for verification
        )
        
        # Clean up temp file
        if script_path.exists():
            script_path.unlink()
        
        verified = result.returncode == 0
        
        return {
            "status": "complete",
            "job_id": job_id,
            "verified": verified,
            "output": result.stdout[-500:] if result.stdout else "",
            "errors": result.stderr[-500:] if result.stderr and not verified else ""
        }
        
    except subprocess.TimeoutExpired:
        return {
            "status": "timeout",
            "job_id": job_id,
            "verified": False,
            "error": "Verification timed out (>5 minutes)"
        }
    except Exception as e:
        # Verification failure shouldn't block video generation entirely
        # Log the error but let the pipeline continue with a warning
        return {
            "status": "error",
            "job_id": job_id,
            "verified": False,
            "error": str(e)
        }


@celery_app.task(bind=True, name="tasks.generate_video")
def generate_video(self, job_id: str, script_data: dict, voice: str, user_id: str):
    """
    Generate a video from parsed problem data.
    
    Flow:
    1. Verify mathematical correctness (proof content only)
    2. Save the script to a file
    3. Run the Manim + audio pipeline
    4. Upload to R2 (TODO)
    5. Return the video URL
    
    Args:
        job_id: Unique identifier for this job
        script_data: Parsed problem with steps, latex, narration
        voice: Voice ID for Fish Audio
        user_id: Who requested this (for billing, access control)
    
    Returns:
        dict with status, video_url, or error
    """
    
    try:
        # === VERIFICATION GATE ===
        self.update_state(
            state="PROCESSING",
            meta={
                "job_id": job_id,
                "step": "verifying",
                "progress": 5,
                "message": "Checking mathematical correctness..."
            }
        )
        
        # Run verification synchronously within this task
        # (Could also be a separate chained task for parallel processing)
        verification = verify_proof_task.apply(
            args=[job_id, script_data]
        ).get(timeout=300)
        
        if verification.get("verified") is False:
            log_error(
                f"Verification failed — blocking video generation",
                job_id=job_id,
                error=verification.get("errors", verification.get("error", ""))
            )
            return {
                "status": "verification_failed",
                "job_id": job_id,
                "error": "Mathematical verification failed. The proof contains errors.",
                "verification": verification,
                "completed_at": datetime.now().isoformat()
            }
        
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
        
        # Calculate minutes used (based on SPOKEN narration length)
        # ~1000 characters ≈ 1 minute of video
        # NOTE: We strip emotion markers like (excited) before counting
        # because those are TTS control signals, not spoken text
        steps = script_data.get("steps", [])
        spoken_chars, total_chars = count_total_narration_chars(steps)
        minutes_used = max(0.1, round(spoken_chars / 1000, 2))
        
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
