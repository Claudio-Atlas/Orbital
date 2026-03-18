"""
Orbital Engine — Universal Renderer
Reads a manifest JSON, dispatches to visual components,
renders Manim scene, and mixes audio.
"""
import json
import os
import subprocess
import shutil
import uuid
from pathlib import Path
from datetime import datetime

from config import (
    ENGINE_DIR, VENV_PYTHON, BG_MUSIC,
    BG_VOLUME, BG_FADE_IN, BG_FADE_OUT,
    LAYOUTS, TTS_PROFILES, VIDEO_TYPES,
    ELEVENLABS_MODEL, ALLISON_VOICE_ID, TTS_OUTPUT_FORMAT, TTS_NORMALIZE_DB,
)


def render_from_manifest(manifest_path: str, job_id: str = None,
                         on_progress=None) -> dict:
    """
    Render a video from a manifest JSON file.

    Args:
        manifest_path: Path to the script manifest JSON
        job_id: Optional job ID for tracking
        on_progress: Callback(stage, pct, msg)

    Returns dict with {status, output_path, duration, error}
    """
    if job_id is None:
        job_id = str(uuid.uuid4())[:8]

    manifest_path = Path(manifest_path)
    if not manifest_path.exists():
        return {"status": "error", "error": f"Manifest not found: {manifest_path}"}

    with open(manifest_path) as f:
        manifest = json.load(f)

    video_type = manifest.get("video_type", "lesson")
    layout_name = VIDEO_TYPES.get(video_type, {}).get("layout", "landscape")

    if on_progress:
        on_progress("render", 0, "Starting Manim render...")

    # ── Step 1: Render Manim scene ──
    scene_file = str(Path(ENGINE_DIR) / "scene_engine.py")
    renders_dir = Path(ENGINE_DIR) / "renders" / job_id
    renders_dir.mkdir(parents=True, exist_ok=True)

    cmd = [
        VENV_PYTHON, "-m", "manim", "render",
        "-qh", "--fps", "60",
        "--media_dir", str(renders_dir / "media"),
        scene_file, "EngineScene",
    ]

    env = dict(os.environ)
    env["PATH"] = f"/Library/TeX/texbin:{env.get('PATH', '')}"
    env["LESSON_MANIFEST"] = str(manifest_path.resolve())
    env["ORBITAL_ENGINE_DIR"] = ENGINE_DIR

    result = subprocess.run(cmd, capture_output=True, text=True,
                          env=env, cwd=ENGINE_DIR)

    if result.returncode != 0:
        return {
            "status": "error",
            "error": f"Manim render failed:\n{result.stderr[-1000:]}",
        }

    if on_progress:
        on_progress("render", 50, "Manim render complete, finding output...")

    # Find the output mp4
    media_dir = renders_dir / "media" / "videos" / "scene_engine" / "1080p60"
    mp4_files = sorted(media_dir.glob("*.mp4"), key=lambda p: p.stat().st_mtime,
                       reverse=True) if media_dir.exists() else []

    if not mp4_files:
        # Broader search
        all_mp4 = list((renders_dir / "media").rglob("*.mp4"))
        if all_mp4:
            all_mp4.sort(key=lambda p: p.stat().st_mtime, reverse=True)
            raw_video = str(all_mp4[0])
        else:
            return {"status": "error", "error": "No video output found after render"}
    else:
        raw_video = str(mp4_files[0])

    if on_progress:
        on_progress("mix", 60, "Mixing background music...")

    # ── Step 2: Mix audio ──
    output_dir = Path(ENGINE_DIR) / "output"
    output_dir.mkdir(exist_ok=True)

    # Build output filename
    sec = manifest.get("section", "0.0")
    vtype = manifest.get("video_sub", "A")
    video_label = manifest.get("video_type", "lesson")
    timestamp = datetime.now().strftime("%H%M")
    output_name = f"sec{sec}_{video_label}_{vtype}_{timestamp}.mp4"
    output_path = str(output_dir / output_name)

    final_path = mix_audio(raw_video, output_path)

    if not final_path:
        # Fallback — use raw video without music
        shutil.copy2(raw_video, output_path)
        final_path = output_path

    if on_progress:
        on_progress("complete", 100, "Done!")

    # Get duration
    try:
        probe = subprocess.run([
            "ffprobe", "-v", "error", "-show_entries", "format=duration",
            "-of", "csv=p=0", final_path
        ], capture_output=True, text=True)
        duration = float(probe.stdout.strip())
    except Exception:
        duration = 0

    # Copy to Desktop
    desktop_name = f"Sec{sec}_Video{vtype}.mp4"
    desktop_path = Path.home() / "Desktop" / desktop_name
    shutil.copy2(final_path, desktop_path)

    return {
        "status": "complete",
        "output_path": final_path,
        "desktop_path": str(desktop_path),
        "duration": duration,
        "size_mb": round(Path(final_path).stat().st_size / (1024*1024), 1),
    }


def mix_audio(raw_video: str, output_path: str) -> str:
    """Mix background music into a rendered video."""
    if not Path(BG_MUSIC).exists():
        return None

    try:
        probe = subprocess.run([
            "ffprobe", "-v", "error", "-show_entries", "format=duration",
            "-of", "csv=p=0", raw_video
        ], capture_output=True, text=True)
        video_dur = float(probe.stdout.strip())
    except Exception:
        return None

    fade_out_start = max(0, video_dur - BG_FADE_OUT)

    cmd = [
        "ffmpeg", "-y",
        "-i", raw_video,
        "-i", BG_MUSIC,
        "-filter_complex",
        f"[1:a]volume={BG_VOLUME},"
        f"afade=t=in:st=0:d={BG_FADE_IN},"
        f"afade=t=out:st={fade_out_start}:d={BG_FADE_OUT}[music];"
        f"[0:a][music]amix=inputs=2:duration=first[aout]",
        "-map", "0:v",
        "-map", "[aout]",
        "-c:v", "copy",
        "-c:a", "aac", "-b:a", "128k",
        "-shortest",
        output_path,
    ]

    result = subprocess.run(cmd, capture_output=True, text=True)
    if result.returncode != 0:
        print(f"  ❌ Audio mix failed: {result.stderr[-500:]}")
        return None

    size = Path(output_path).stat().st_size / (1024*1024)
    print(f"  ✅ Final video: {output_path}\n     Size: {size:.1f} MB")
    return output_path
