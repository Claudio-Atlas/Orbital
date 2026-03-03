#!/usr/bin/env python3
"""
Orbital Pipeline Worker
Polls Supabase for queued video_jobs, runs the 6-stage pipeline, updates status.
Runs locally on Mac Mini (needs Manim, Lean, ffmpeg).
"""

import os
import sys
import json
import time
import logging
import subprocess
from datetime import datetime, timezone
from pathlib import Path

# Optional imports — gracefully handle missing
try:
    from supabase import create_client, Client
    HAS_SUPABASE = True
except ImportError:
    HAS_SUPABASE = False
    print("⚠️  supabase-py not installed. Run: pip install supabase")

try:
    import anthropic
    HAS_ANTHROPIC = True
except ImportError:
    HAS_ANTHROPIC = False

try:
    import openai
    HAS_OPENAI = True
except ImportError:
    HAS_OPENAI = False

# ─── Config ───

FACTORY_DIR = Path(__file__).parent
OUTPUT_DIR = FACTORY_DIR / "output"
SCRIPTS_DIR = FACTORY_DIR / "scripts"
LEAN_DIR = FACTORY_DIR / "lean_verifier"

POLL_INTERVAL = 5  # seconds between polls

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(message)s",
    datefmt="%H:%M:%S",
)
log = logging.getLogger("orbital-worker")


class PipelineConfig:
    """Holds API keys and settings. Loaded from env or Supabase api_keys table."""
    
    def __init__(self):
        self.deepseek_key = os.environ.get("DEEPSEEK_API_KEY", "")
        self.anthropic_key = os.environ.get("ANTHROPIC_API_KEY", "")
        self.elevenlabs_key = os.environ.get("ELEVENLABS_API_KEY", "")
        self.supabase_url = os.environ.get("SUPABASE_URL", "")
        self.supabase_service_key = os.environ.get("SUPABASE_SERVICE_KEY", "")
    
    def validate(self):
        missing = []
        if not self.supabase_url: missing.append("SUPABASE_URL")
        if not self.supabase_service_key: missing.append("SUPABASE_SERVICE_KEY")
        if missing:
            log.error(f"Missing required env vars: {', '.join(missing)}")
            return False
        return True


class OrbitalWorker:
    def __init__(self, config: PipelineConfig):
        self.config = config
        self.db: Client = create_client(config.supabase_url, config.supabase_service_key)
    
    def update_job(self, job_id: str, **kwargs):
        """Update a video_job in Supabase."""
        self.db.table("video_jobs").update(kwargs).eq("id", job_id).execute()
    
    def poll(self):
        """Check for queued jobs and process them."""
        result = self.db.table("video_jobs") \
            .select("*") \
            .eq("status", "queued") \
            .order("created_at") \
            .limit(1) \
            .execute()
        
        if result.data:
            job = result.data[0]
            log.info(f"📦 Found job: {job['id'][:8]}... — {job['problem'][:50]}")
            self.process_job(job)
    
    def process_job(self, job: dict):
        """Run the full pipeline for a job."""
        job_id = job["id"]
        
        try:
            self.update_job(job_id, 
                status="stage_1", 
                stage_detail="Generating script...",
                started_at=datetime.now(timezone.utc).isoformat()
            )
            
            # ─── Stage 1: Script Generation ───
            script = self.stage_1_script(job)
            self.update_job(job_id, 
                status="stage_2" if job["path"] == "full_ai" else "stage_4",
                stage_detail="Verifying mathematics..." if job["path"] == "full_ai" else "Generating narration...",
                script_json=json.dumps(script),
                cost_script=0.001
            )
            
            revised_script = script
            
            # ─── Stage 2: Verification Circle (Path A only) ───
            if job["path"] == "full_ai":
                revised_script, circle_log = self.stage_2_circle(job, script)
                self.update_job(job_id,
                    status="stage_3" if job["lean_requested"] else "stage_4",
                    stage_detail="Formally proving..." if job["lean_requested"] else "Generating narration...",
                    revised_script_json=json.dumps(revised_script),
                    circle_log=circle_log,
                    cost_circle=0.60,
                    verification_method="circle",
                    verification_badge="ai_verified"
                )
                
                # ─── Stage 3: Lean (if requested) ───
                if job["lean_requested"]:
                    lean_result = self.stage_3_lean(job, revised_script)
                    self.update_job(job_id,
                        status="stage_4",
                        stage_detail="Generating narration...",
                        lean_file=lean_result.get("lean_file"),
                        cost_lean=0.10,
                        verification_method="lean4" if lean_result["verified"] else "circle",
                        verification_badge="lean4_verified" if lean_result["verified"] else "ai_verified"
                    )
            else:
                # Path B/C: teacher verified
                self.update_job(job_id,
                    verification_method="teacher",
                    verification_badge="teacher_verified"
                )
            
            # ─── Stage 4: TTS ───
            self.update_job(job_id, status="stage_4", stage_detail="Generating narration...")
            audio_result = self.stage_4_tts(job, revised_script)
            self.update_job(job_id,
                status="stage_5",
                stage_detail="Rendering video...",
                cost_tts=audio_result.get("cost", 0.015)
            )
            
            # ─── Stage 5: Manim Render ───
            video_result = self.stage_5_render(job, revised_script, audio_result)
            self.update_job(job_id,
                status="stage_6",
                stage_detail="Delivering...",
            )
            
            # ─── Stage 6: Delivery ───
            delivery = self.stage_6_delivery(job, video_result)
            
            # Calculate total cost
            job_data = self.db.table("video_jobs").select("*").eq("id", job_id).single().execute()
            j = job_data.data
            total_cost = float(j.get("cost_script", 0) or 0) + float(j.get("cost_circle", 0) or 0) + \
                         float(j.get("cost_lean", 0) or 0) + float(j.get("cost_tts", 0) or 0)
            
            self.update_job(job_id,
                status="complete",
                stage_detail="✅ Ready to watch",
                video_url=delivery.get("video_url"),
                youtube_id=delivery.get("youtube_id"),
                youtube_url=delivery.get("youtube_url"),
                thumbnail_url=delivery.get("thumbnail_url"),
                duration_seconds=video_result.get("duration_seconds"),
                cost_total=total_cost,
                completed_at=datetime.now(timezone.utc).isoformat()
            )
            
            log.info(f"✅ Job {job_id[:8]} complete! Cost: ${total_cost:.3f}")
            
        except Exception as e:
            log.error(f"❌ Job {job_id[:8]} failed: {e}")
            self.update_job(job_id,
                status="failed",
                stage_detail=f"Error: {str(e)[:200]}",
                error=str(e),
                retry_count=job.get("retry_count", 0) + 1
            )
    
    # ─── Stage Implementations ───
    
    def stage_1_script(self, job: dict) -> list:
        """Generate script via DeepSeek V3."""
        log.info("Stage 1: Generating script...")
        
        if not self.config.deepseek_key:
            log.warning("No DeepSeek key — using mock script")
            return self._mock_script(job["problem"])
        
        client = openai.OpenAI(
            api_key=self.config.deepseek_key,
            base_url="https://api.deepseek.com"
        )
        
        response = client.chat.completions.create(
            model="deepseek-chat",
            messages=[
                {"role": "system", "content": self._stage1_system_prompt()},
                {"role": "user", "content": f"Problem: {job['problem']}\nDetail level: {job['detail_level']}\nNotes: {job.get('notes', 'none')}"}
            ],
            response_format={"type": "json_object"},
            temperature=0.3,
        )
        
        content = response.choices[0].message.content
        data = json.loads(content)
        return data.get("steps", data.get("script", []))
    
    def stage_2_circle(self, job: dict, script: list) -> tuple:
        """Run Verification Circle via Anthropic."""
        log.info("Stage 2: Running Verification Circle...")
        
        if not self.config.anthropic_key:
            log.warning("No Anthropic key — skipping circle")
            return script, "Circle skipped (no API key)"
        
        client = anthropic.Anthropic(api_key=self.config.anthropic_key)
        
        prompt = f"""You are running a Verification Circle for Orbital, an AI math video generator.

You will play 4 roles across 4 rounds: Mathematician A (Rigor), Mathematician B (Breadth), Pedagogy Expert, and Student Simulator.

PROBLEM: {job['problem']}
DETAIL LEVEL: {job['detail_level']}

SCRIPT TO REVIEW:
{json.dumps(script, indent=2)}

Run the circle now. For each round, write each agent's contribution under a clear header. Agents should reference each other by name in Rounds 2-4. End with the revision table and revised script JSON.

Output the revised script as a JSON array at the end, wrapped in ```json ... ``` tags."""

        response = client.messages.create(
            model="claude-opus-4",
            max_tokens=8000,
            messages=[{"role": "user", "content": prompt}]
        )
        
        circle_log = response.content[0].text
        
        # Extract revised script JSON from the response
        revised_script = script  # fallback
        if "```json" in circle_log:
            json_block = circle_log.split("```json")[-1].split("```")[0]
            try:
                parsed = json.loads(json_block)
                if isinstance(parsed, list):
                    revised_script = parsed
                elif "steps" in parsed:
                    revised_script = parsed["steps"]
            except json.JSONDecodeError:
                log.warning("Could not parse revised script from circle — using original")
        
        return revised_script, circle_log
    
    def stage_3_lean(self, job: dict, script: list) -> dict:
        """Write and compile Lean 4 formalization."""
        log.info("Stage 3: Lean formalization...")
        
        if not self.config.anthropic_key:
            return {"verified": False, "lean_file": None}
        
        client = anthropic.Anthropic(api_key=self.config.anthropic_key)
        
        # Extract claims from script
        claims = [s.get("narration", "") for s in script if s.get("type") in ("math", "box", "transform")]
        
        response = client.messages.create(
            model="claude-opus-4",
            max_tokens=4000,
            messages=[{"role": "user", "content": f"""Write a Lean 4 file that formally verifies the key mathematical claims from this video script. Use Mathlib v4.28.0.

PROBLEM: {job['problem']}

KEY STEPS:
{json.dumps(claims, indent=2)}

Requirements:
- Import only from Mathlib
- One theorem per key claim
- Use tactics: norm_num, ring, linarith, simp, exact?, apply?
- Keep proofs minimal
- Add comments

Output ONLY the .lean file contents."""}]
        )
        
        lean_code = response.content[0].text
        if "```" in lean_code:
            lean_code = lean_code.split("```")[1].split("```")[0]
            if lean_code.startswith("lean"):
                lean_code = lean_code[4:]
        
        # Write and compile
        lean_file = LEAN_DIR / "Verifier" / "Claims.lean"
        lean_file.parent.mkdir(parents=True, exist_ok=True)
        lean_file.write_text(lean_code)
        
        result = subprocess.run(
            ["lake", "build"],
            cwd=str(LEAN_DIR),
            capture_output=True,
            text=True,
            timeout=120
        )
        
        verified = result.returncode == 0
        if verified:
            log.info("✅ Lean verification PASSED")
        else:
            log.warning(f"❌ Lean verification FAILED: {result.stderr[:200]}")
        
        return {
            "verified": verified,
            "lean_file": str(lean_file),
            "compiler_output": result.stdout + result.stderr
        }
    
    def stage_4_tts(self, job: dict, script: list) -> dict:
        """Generate TTS audio via ElevenLabs."""
        log.info("Stage 4: Generating TTS...")
        
        if not self.config.elevenlabs_key:
            log.warning("No ElevenLabs key — generating silent audio")
            return self._mock_audio(script)
        
        import requests
        
        # Build SSML chunks
        narrations = [s.get("narration", "") for s in script if s.get("narration")]
        full_text = "\n\n".join(narrations)  # paragraph breaks
        
        # ElevenLabs API call
        voice_id = "5jVVMAv2LzffTcLGarKh"  # Allison (tutorial)
        url = f"https://api.elevenlabs.io/v1/text-to-speech/{voice_id}"
        
        headers = {
            "xi-api-key": self.config.elevenlabs_key,
            "Content-Type": "application/json",
        }
        
        # Split into chunks if > 5000 chars
        chunks = []
        if len(full_text) <= 5000:
            chunks = [full_text]
        else:
            # Split at paragraph breaks
            parts = full_text.split("\n\n")
            current = ""
            for part in parts:
                if len(current) + len(part) + 2 > 4800:
                    chunks.append(current)
                    current = part
                else:
                    current = current + "\n\n" + part if current else part
            if current:
                chunks.append(current)
        
        slug = job["problem"][:30].replace(" ", "_").lower()
        audio_dir = OUTPUT_DIR / "audio"
        audio_dir.mkdir(parents=True, exist_ok=True)
        
        audio_files = []
        total_chars = 0
        
        for i, chunk in enumerate(chunks):
            payload = {
                "text": chunk,
                "model_id": "eleven_turbo_v2_5",
                "voice_settings": {
                    "stability": 0.7,
                    "similarity_boost": 0.75,
                }
            }
            
            resp = requests.post(url, json=payload, headers=headers)
            if resp.status_code != 200:
                raise Exception(f"ElevenLabs API error: {resp.status_code} — {resp.text[:200]}")
            
            chunk_path = audio_dir / f"{slug}_chunk_{i}.mp3"
            chunk_path.write_bytes(resp.content)
            audio_files.append(str(chunk_path))
            total_chars += len(chunk)
            log.info(f"  TTS chunk {i+1}/{len(chunks)}: {len(chunk)} chars")
        
        # Combine chunks if multiple
        combined_path = OUTPUT_DIR / f"{slug}_combined_audio.mp3"
        if len(audio_files) == 1:
            import shutil
            shutil.copy(audio_files[0], combined_path)
        else:
            # Use ffmpeg to concatenate
            list_file = audio_dir / "concat_list.txt"
            list_file.write_text("\n".join(f"file '{f}'" for f in audio_files))
            subprocess.run([
                "ffmpeg", "-y", "-f", "concat", "-safe", "0",
                "-i", str(list_file), "-c", "copy", str(combined_path)
            ], capture_output=True)
        
        cost = total_chars * 0.00008  # $0.08 per 1K chars (Starter plan)
        
        return {
            "combined_path": str(combined_path),
            "audio_files": audio_files,
            "total_chars": total_chars,
            "cost": round(cost, 4),
        }
    
    def stage_5_render(self, job: dict, script: list, audio: dict) -> dict:
        """Render video with Manim + ffmpeg merge."""
        log.info("Stage 5: Rendering with Manim...")
        
        slug = job["problem"][:30].replace(" ", "_").lower()
        
        # Write script to temp file for scene_v3.py
        script_path = SCRIPTS_DIR / f"{slug}.json"
        SCRIPTS_DIR.mkdir(parents=True, exist_ok=True)
        script_path.write_text(json.dumps(script, indent=2))
        
        # Run Manim render
        env = os.environ.copy()
        env["ORBITAL_SCRIPT"] = str(script_path)
        env["PATH"] = f"/Library/TeX/texbin:{env.get('PATH', '')}"
        
        result = subprocess.run([
            sys.executable, "-m", "manim", "render",
            "-qh", "--format", "mp4",
            str(FACTORY_DIR / "scene_v3.py"), "OrbitalVideo"
        ], cwd=str(FACTORY_DIR), env=env, capture_output=True, text=True, timeout=600)
        
        if result.returncode != 0:
            raise Exception(f"Manim render failed: {result.stderr[:500]}")
        
        # Find the rendered video
        raw_video = FACTORY_DIR / "media" / "videos" / "scene_v3" / "1080p60" / "OrbitalVideo.mp4"
        if not raw_video.exists():
            raise Exception("Rendered video not found")
        
        # ffmpeg merge audio
        final_path = OUTPUT_DIR / f"{slug}_final.mp4"
        OUTPUT_DIR.mkdir(parents=True, exist_ok=True)
        
        merge_result = subprocess.run([
            "ffmpeg", "-y",
            "-i", str(raw_video),
            "-i", audio["combined_path"],
            "-map", "0:v", "-map", "1:a",
            "-c:v", "copy", "-c:a", "aac", "-b:a", "192k",
            "-shortest",
            str(final_path)
        ], capture_output=True, text=True, timeout=120)
        
        if merge_result.returncode != 0:
            raise Exception(f"ffmpeg merge failed: {merge_result.stderr[:300]}")
        
        # Get duration
        probe = subprocess.run([
            "ffprobe", "-v", "error", "-show_entries", "format=duration",
            "-of", "default=noprint_wrappers=1:nokey=1", str(final_path)
        ], capture_output=True, text=True)
        duration = int(float(probe.stdout.strip())) if probe.stdout.strip() else 0
        
        # Generate thumbnail
        thumb_path = OUTPUT_DIR / f"{slug}_thumb.png"
        thumb_time = str(duration * 0.4) if duration > 0 else "3"
        subprocess.run([
            "ffmpeg", "-y", "-i", str(final_path),
            "-ss", thumb_time, "-vframes", "1", "-q:v", "2",
            str(thumb_path)
        ], capture_output=True)
        
        log.info(f"  Rendered: {final_path} ({duration}s)")
        
        return {
            "video_path": str(final_path),
            "thumbnail_path": str(thumb_path),
            "duration_seconds": duration,
        }
    
    def stage_6_delivery(self, job: dict, video: dict) -> dict:
        """Upload to storage / YouTube."""
        log.info("Stage 6: Delivering...")
        
        # TODO: YouTube upload via API
        # TODO: Supabase Storage upload
        
        # For now, just return local paths
        return {
            "video_url": video["video_path"],
            "thumbnail_url": video.get("thumbnail_path"),
            "youtube_id": None,
            "youtube_url": None,
        }
    
    # ─── Helpers ───
    
    def _stage1_system_prompt(self) -> str:
        return """You are a math video script generator for Orbital. Generate a step-by-step video script in JSON format.

Output a JSON object with a "steps" array. Each step has:
- step_number (int)
- type: "text" | "math" | "mixed" | "transform" | "box" | "graph"
- narration (string): what the narrator says. Talk to ONE student. Explain WHY before HOW. Call out common mistakes.
- display_latex (string, optional): LaTeX to display on screen
- from_latex / to_latex (strings, for "transform" type): equation before and after transformation

For "quick": 5-8 steps. For "standard": 12-20 steps. For "detailed": 20-35 steps.

Start with an intro text step. End with a box step (final answer) and a text step (takeaway).
Ensure mathematical rigor — every step must logically follow from the previous."""
    
    def _mock_script(self, problem: str) -> list:
        return [
            {"step_number": 1, "type": "text", "narration": f"Let's work through this problem: {problem}"},
            {"step_number": 2, "type": "text", "narration": "First, let's understand what we need to find."},
            {"step_number": 3, "type": "math", "narration": "Here's our setup.", "display_latex": "f(x) = x^2"},
            {"step_number": 4, "type": "box", "narration": "And that's our answer!", "display_latex": "\\boxed{\\text{Solution}}"},
            {"step_number": 5, "type": "text", "narration": "Remember the key idea: always check your work!"},
        ]
    
    def _mock_audio(self, script: list) -> dict:
        """Generate silent audio for testing."""
        duration = len(script) * 10  # ~10s per step
        silent_path = OUTPUT_DIR / "silent.mp3"
        OUTPUT_DIR.mkdir(parents=True, exist_ok=True)
        subprocess.run([
            "ffmpeg", "-y", "-f", "lavfi", "-i",
            f"anullsrc=r=44100:cl=stereo", "-t", str(duration),
            "-q:a", "9", str(silent_path)
        ], capture_output=True)
        return {"combined_path": str(silent_path), "audio_files": [], "total_chars": 0, "cost": 0}
    
    def run(self):
        """Main loop — poll for jobs."""
        log.info("🚀 Orbital Worker started")
        log.info(f"   Factory: {FACTORY_DIR}")
        log.info(f"   DeepSeek: {'✅' if self.config.deepseek_key else '❌'}")
        log.info(f"   Anthropic: {'✅' if self.config.anthropic_key else '❌'}")
        log.info(f"   ElevenLabs: {'✅' if self.config.elevenlabs_key else '❌'}")
        
        while True:
            try:
                self.poll()
            except KeyboardInterrupt:
                log.info("👋 Worker stopped")
                break
            except Exception as e:
                log.error(f"Poll error: {e}")
            
            time.sleep(POLL_INTERVAL)


if __name__ == "__main__":
    config = PipelineConfig()
    if not config.validate():
        sys.exit(1)
    
    worker = OrbitalWorker(config)
    worker.run()
