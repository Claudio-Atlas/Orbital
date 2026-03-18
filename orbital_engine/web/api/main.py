"""
Orbital Engine — Web API
FastAPI backend for the video production platform.
"""
import json
import os
import sys
from pathlib import Path
from typing import Optional
from fastapi import FastAPI, HTTPException, BackgroundTasks
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from pydantic import BaseModel

# Add engine to path
ENGINE_DIR = str(Path(__file__).parent.parent.parent)
sys.path.insert(0, ENGINE_DIR)

from config import (
    VIDEO_TYPES, TOPICS, TTS_PROFILES, LAYOUTS,
    ORBITAL_CYAN, VIOLET, GOLD, NEON_GREEN, END_CYAN
)

app = FastAPI(title="Orbital Engine", version="1.0.0")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# ── State ──
RENDERS_DIR = Path(ENGINE_DIR) / "renders"
RENDERS_DIR.mkdir(exist_ok=True)
OUTPUT_DIR = Path(ENGINE_DIR) / "output"
OUTPUT_DIR.mkdir(exist_ok=True)

# Track active/completed renders
render_jobs: dict = {}


# ── Models ──
class RenderRequest(BaseModel):
    video_type: str  # short, lesson, problem, longform
    topic: Optional[str] = None
    chapter: Optional[int] = None
    section: Optional[int] = None
    video_sub: Optional[str] = None  # A, B, C for lessons
    title: Optional[str] = None
    description: Optional[str] = None


class TTSPreviewRequest(BaseModel):
    text: str
    profile: str = "lesson"


# ── Routes ──
@app.get("/")
def root():
    return {"name": "Orbital Engine", "version": "1.0.0", "status": "online"}


@app.get("/api/config")
def get_config():
    """Return all configuration for the frontend."""
    return {
        "video_types": VIDEO_TYPES,
        "topics": TOPICS,
        "tts_profiles": TTS_PROFILES,
        "layouts": LAYOUTS,
        "colors": {
            "orbital_cyan": ORBITAL_CYAN,
            "violet": VIOLET,
            "gold": GOLD,
            "neon_green": NEON_GREEN,
            "end_cyan": END_CYAN,
        },
    }


@app.get("/api/library")
def get_visual_library():
    """Return available visual components organized by topic."""
    visuals_dir = Path(ENGINE_DIR) / "visuals"
    library = {}

    for topic_dir in sorted(visuals_dir.iterdir()):
        if topic_dir.is_dir() and not topic_dir.name.startswith("_"):
            components = []
            for py_file in sorted(topic_dir.glob("*.py")):
                if py_file.name.startswith("_"):
                    continue
                name = py_file.stem
                # Read docstring from file
                content = py_file.read_text()
                doc = ""
                if '"""' in content:
                    start = content.index('"""') + 3
                    end = content.index('"""', start)
                    doc = content[start:end].strip()
                components.append({
                    "name": name,
                    "path": str(py_file.relative_to(ENGINE_DIR)),
                    "description": doc,
                })
            library[topic_dir.name] = {
                "label": TOPICS.get(topic_dir.name, {}).get("label", topic_dir.name.title()),
                "components": components,
                "count": len(components),
            }

    return library


@app.get("/api/library/stats")
def get_library_stats():
    """Quick stats on the visual library."""
    visuals_dir = Path(ENGINE_DIR) / "visuals"
    total = 0
    by_topic = {}
    for topic_dir in visuals_dir.iterdir():
        if topic_dir.is_dir() and not topic_dir.name.startswith("_"):
            count = len([f for f in topic_dir.glob("*.py") if not f.name.startswith("_")])
            by_topic[topic_dir.name] = count
            total += count
    return {"total_components": total, "by_topic": by_topic}


@app.get("/api/renders")
def list_renders():
    """List all render jobs."""
    return {"jobs": render_jobs}


@app.get("/api/renders/{job_id}")
def get_render(job_id: str):
    """Get status of a specific render job."""
    if job_id not in render_jobs:
        raise HTTPException(404, "Job not found")
    return render_jobs[job_id]


@app.get("/api/textbook/sections")
def list_sections():
    """List available textbook sections."""
    from config import TEXTBOOK_DIR
    textbook_dir = Path(TEXTBOOK_DIR)
    sections = []
    for ch_dir in sorted(textbook_dir.glob("ch*")):
        ch_num = int(ch_dir.name.replace("ch", "").lstrip("0") or "0")
        for sec_file in sorted(ch_dir.glob("sec*.json")):
            sec_num = int(sec_file.stem.replace("sec", "").lstrip("0") or "0")
            with open(sec_file) as f:
                data = json.load(f)
            sections.append({
                "chapter": ch_num,
                "section": sec_num,
                "title": data.get("title", ""),
                "objectives": len(data.get("objectives", [])),
                "content_blocks": len(data.get("content", [])),
            })
    return {"sections": sections}


def run_render_job(job_id: str, req: RenderRequest):
    """Background render task."""
    import traceback
    try:
        render_jobs[job_id]["status"] = "extracting"
        render_jobs[job_id]["progress"] = 10

        # Import pipeline components
        lesson_pipeline = Path(ENGINE_DIR).parent / "orbital_longform" / "lesson_pipeline"
        sys.path.insert(0, str(lesson_pipeline))

        from extract import extract_section, split_into_videos
        from scriptwriter import generate_script, save_script

        # Extract content
        section_data = extract_section(req.chapter, req.section)
        split = split_into_videos(section_data)

        video_key = (req.video_sub or "A").upper()
        video_data = split.get(video_key)
        if not video_data:
            render_jobs[job_id]["status"] = "error"
            render_jobs[job_id]["error"] = f"No content for Video {video_key}"
            return

        # Generate script
        render_jobs[job_id]["status"] = "scripting"
        render_jobs[job_id]["progress"] = 20
        manifest = generate_script(video_data, section_data)
        manifest["video_type"] = req.video_type
        manifest["video_sub"] = video_key

        scripts_dir = Path(ENGINE_DIR) / "scripts"
        scripts_dir.mkdir(exist_ok=True)
        script_path = scripts_dir / f"sec{req.chapter}_{req.section}_video{video_key}.json"
        with open(script_path, "w") as f:
            json.dump(manifest, f, indent=2)

        # TTS
        render_jobs[job_id]["status"] = "tts"
        render_jobs[job_id]["progress"] = 30
        sys.path.insert(0, ENGINE_DIR)
        from tts.generator import generate_tts_for_manifest
        manifest = generate_tts_for_manifest(str(script_path), profile=req.video_type)

        # Render
        render_jobs[job_id]["status"] = "rendering"
        render_jobs[job_id]["progress"] = 50
        from renderer import render_from_manifest
        result = render_from_manifest(str(script_path), job_id=job_id)

        render_jobs[job_id]["status"] = result["status"]
        render_jobs[job_id]["progress"] = 100
        render_jobs[job_id]["output"] = result.get("output_path")
        render_jobs[job_id]["desktop_path"] = result.get("desktop_path")
        render_jobs[job_id]["duration"] = result.get("duration")
        render_jobs[job_id]["size_mb"] = result.get("size_mb")
        render_jobs[job_id]["error"] = result.get("error")

    except Exception as e:
        render_jobs[job_id]["status"] = "error"
        render_jobs[job_id]["error"] = f"{type(e).__name__}: {str(e)}\n{traceback.format_exc()[-500:]}"


@app.post("/api/render")
async def start_render(req: RenderRequest, background_tasks: BackgroundTasks):
    """Start a new render job."""
    import uuid
    job_id = str(uuid.uuid4())[:8]

    if req.video_type not in VIDEO_TYPES:
        raise HTTPException(400, f"Invalid video type: {req.video_type}")

    if req.video_type in ("lesson", "problem") and (not req.chapter or not req.section):
        raise HTTPException(400, "chapter and section required for lesson/problem videos")

    render_jobs[job_id] = {
        "id": job_id,
        "status": "queued",
        "video_type": req.video_type,
        "topic": req.topic,
        "chapter": req.chapter,
        "section": req.section,
        "video_sub": req.video_sub,
        "title": req.title,
        "progress": 0,
        "output": None,
        "error": None,
        "started_at": __import__("datetime").datetime.now().isoformat(),
    }

    background_tasks.add_task(run_render_job, job_id, req)

    return {"job_id": job_id, "status": "queued"}


@app.get("/api/renders/{job_id}/poll")
def poll_render(job_id: str):
    """Poll render job status — for frontend progress tracking."""
    if job_id not in render_jobs:
        raise HTTPException(404, "Job not found")
    job = render_jobs[job_id]
    return {
        "id": job_id,
        "status": job["status"],
        "progress": job["progress"],
        "output": job.get("output"),
        "desktop_path": job.get("desktop_path"),
        "duration": job.get("duration"),
        "size_mb": job.get("size_mb"),
        "error": job.get("error"),
    }


@app.get("/api/outputs")
def list_outputs():
    """List completed video files."""
    files = []
    for f in sorted(OUTPUT_DIR.glob("*.mp4")):
        stat = f.stat()
        files.append({
            "name": f.name,
            "path": str(f),
            "size_mb": round(stat.st_size / (1024*1024), 1),
            "modified": stat.st_mtime,
        })
    return {"files": files}


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8787)
