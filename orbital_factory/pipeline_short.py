"""
Orbital VideoFactory — Short-Form Pipeline (TikTok / Reels)
============================================================
Generates 9:16 vertical math videos (30–90 seconds) optimised for
phone playback. Sits alongside the existing tutorial pipeline — does
NOT replace it.

Flow:
  1. Accept problem string + optional hook + difficulty level
  2. DeepSeek V3 writes a teaching-lite script (short_script.txt prompt)
  3. Single Sonnet verification pass (math-correctness only, no Lean)
  4. Generate TTS with Allison voice (ElevenLabs, single API call)
  5. Render Manim scene at 9:16 via scene_short.py + manim_short.cfg
  6. Stitch: intro (2–3s) + content + outro (2s)
  7. Return {"video_path": ..., "duration": ..., "cost": ...}

Usage:
    from pipeline_short import generate_short_video

    result = generate_short_video(
        problem="Find the derivative of f(x) = 3x^2 + 2x - 5",
        hook="solve this 👇",   # optional — random if omitted
        difficulty="easy",      # easy / medium / hard
    )
    print(result["video_path"])
"""

from __future__ import annotations

import json
import os
from dotenv import load_dotenv
load_dotenv()
import random
import re
import shutil
import subprocess
import time
from pathlib import Path
from typing import Optional

from pydub import AudioSegment

# ── paths ──────────────────────────────────────────────────────────────────
FACTORY_ROOT = Path(__file__).parent.resolve()
PROMPTS_DIR  = FACTORY_ROOT / "prompts"
OUTPUT_DIR   = FACTORY_ROOT / "output"
JOBS_DIR     = FACTORY_ROOT / "jobs"

SHORT_SYSTEM_PROMPT = (PROMPTS_DIR / "short_script.txt").read_text()
WHY_SYSTEM_PROMPT   = (PROMPTS_DIR / "why_script.txt").read_text() if (PROMPTS_DIR / "why_script.txt").exists() else SHORT_SYSTEM_PROMPT

# ── API keys ───────────────────────────────────────────────────────────────
ELEVEN_API_KEY   = os.environ.get("ELEVEN_API_KEY",  "sk_4abfbb388b66e23c7df0424e9228691ae139ab56a449e2a7")
DEEPSEEK_API_KEY = os.environ.get("DEEPSEEK_API_KEY", "")
ANTHROPIC_API_KEY = os.environ.get("ANTHROPIC_API_KEY", "")

# ── voice ─────────────────────────────────────────────────────────────────
ALLISON_VOICE_ID = "5jVVMAv2LzffTcLGarKh"
ELEVEN_MODEL     = "eleven_turbo_v2_5"

# ── timing constants ──────────────────────────────────────────────────────
INTRO_DURATION   = 2.5    # seconds — intro_short renders ~2.5s
OUTRO_DURATION   = 2.0    # seconds — outro_short renders ~2.0s
EXTRA_HOLD       = 0.6    # pause between steps

# ── hook pool ─────────────────────────────────────────────────────────────
from intro_short import HOOKS


# ═══════════════════════════════════════════════════════════════════════════
#  STEP 1 — Script generation (DeepSeek V3)
# ═══════════════════════════════════════════════════════════════════════════

def _call_deepseek(problem: str, difficulty: str) -> dict:
    """
    Call DeepSeek V3 to generate a short-form script JSON.
    Falls back to a stub if DEEPSEEK_API_KEY is not set (useful for testing).
    """
    user_prompt = (
        f"Difficulty: {difficulty}\n\n"
        f"Problem: {problem}"
    )

    if not DEEPSEEK_API_KEY:
        print("  ⚠️  DEEPSEEK_API_KEY not set — using stub script for import test")
        return _stub_script(problem, difficulty)

    from openai import OpenAI  # DeepSeek uses OpenAI-compatible API

    client = OpenAI(
        api_key=DEEPSEEK_API_KEY,
        base_url="https://api.deepseek.com/v1",
    )

    response = client.chat.completions.create(
        model="deepseek-chat",
        messages=[
            {"role": "system", "content": SHORT_SYSTEM_PROMPT},
            {"role": "user",   "content": user_prompt},
        ],
        temperature=0.6,
        max_tokens=2048,
    )

    raw = response.choices[0].message.content.strip()

    # Strip any accidental code fences
    raw = re.sub(r"^```(?:json)?\s*", "", raw)
    raw = re.sub(r"\s*```$", "", raw)

    try:
        script = json.loads(raw)
    except json.JSONDecodeError as e:
        raise ValueError(f"DeepSeek returned invalid JSON: {e}\n\nRaw:\n{raw[:500]}")

    return script


def _call_deepseek_why(concept: str) -> dict:
    """
    Call DeepSeek V3 to generate a 'why does this work?' explainer script.
    Uses the why_script.txt prompt template.
    """
    user_prompt = f"Concept: {concept}"

    if not DEEPSEEK_API_KEY:
        print("  ⚠️  DEEPSEEK_API_KEY not set — using stub script for import test")
        return _stub_script(concept, "medium")

    from openai import OpenAI

    client = OpenAI(
        api_key=DEEPSEEK_API_KEY,
        base_url="https://api.deepseek.com/v1",
    )

    response = client.chat.completions.create(
        model="deepseek-chat",
        messages=[
            {"role": "system", "content": WHY_SYSTEM_PROMPT},
            {"role": "user",   "content": user_prompt},
        ],
        temperature=0.7,
        max_tokens=3000,
    )

    raw = response.choices[0].message.content.strip()
    raw = re.sub(r"^```(?:json)?\s*", "", raw)
    raw = re.sub(r"\s*```$", "", raw)

    try:
        script = json.loads(raw)
    except json.JSONDecodeError as e:
        raise ValueError(f"DeepSeek returned invalid JSON: {e}\n\nRaw:\n{raw[:500]}")

    return script


def _stub_script(problem: str, difficulty: str) -> dict:
    """Minimal stub script used when no API key is available (import testing)."""
    return {
        "meta": {
            "topic": problem[:60],
            "difficulty": difficulty,
            "product_family": "short-form",
        },
        "steps": [
            {
                "type": "math",
                "content": r"f(x) = 3x^2 + 2x - 5",
                "narration": "Find the derivative of f of x.",
                "mode": "replace",
                "label": "",
            },
            {
                "type": "box",
                "content": r"f'(x) = 6x + 2",
                "narration": "The answer is 6x plus 2.",
                "mode": "replace",
                "label": "Answer",
            },
        ],
    }


# ═══════════════════════════════════════════════════════════════════════════
#  STEP 2 — Verification (single Sonnet pass)
# ═══════════════════════════════════════════════════════════════════════════

def _verify_script_sonnet(script: dict, difficulty: str) -> tuple[bool, str]:
    """
    Lightweight math-correctness check using Claude Sonnet.
    Returns (passed: bool, feedback: str).
    Skips verification for 'easy' difficulty to keep it fast.
    """
    if difficulty == "easy":
        print("  ℹ️  Easy difficulty — skipping verification pass")
        return True, "skipped"

    if not ANTHROPIC_API_KEY:
        print("  ⚠️  ANTHROPIC_API_KEY not set — skipping verification")
        return True, "skipped (no key)"

    import anthropic

    steps_summary = "\n".join(
        f"  Step {i+1} ({s.get('type','?')}): {s.get('content','')!r}  — {s.get('narration','')}"
        for i, s in enumerate(script.get("steps", []))
    )

    prompt = (
        "You are a math accuracy checker. Review this short-form math video script "
        "for CORRECTNESS ONLY. Check: are the equations right? Is the final answer correct? "
        "Is the step-by-step logic valid?\n\n"
        f"Topic: {script.get('meta', {}).get('topic', 'Unknown')}\n\n"
        f"Steps:\n{steps_summary}\n\n"
        "Reply with exactly one of:\n"
        "  PASS — if everything is mathematically correct\n"
        "  FAIL: <brief reason> — if there is a math error\n"
        "No other output."
    )

    client = anthropic.Anthropic(api_key=ANTHROPIC_API_KEY)
    message = client.messages.create(
        model="claude-sonnet-4-5",
        max_tokens=256,
        messages=[{"role": "user", "content": prompt}],
    )

    verdict = message.content[0].text.strip()
    passed  = verdict.upper().startswith("PASS")
    return passed, verdict


# ═══════════════════════════════════════════════════════════════════════════
#  STEP 3 — TTS (ElevenLabs, single API call)
# ═══════════════════════════════════════════════════════════════════════════

def _generate_all_tts(steps: list, audio_dir: Path) -> list:
    """
    Generate TTS for each narration line as a SEPARATE ElevenLabs API call.
    This ensures each segment has exact duration — no silence-splitting issues.
    Returns manifest list enriched with audio_path + duration.
    """
    audio_dir.mkdir(parents=True, exist_ok=True)

    from elevenlabs import ElevenLabs, VoiceSettings

    # Load TikTok voice profile
    voice_profile_path = FACTORY_ROOT / "voice_profiles" / "allison_tiktok.json"
    if voice_profile_path.exists():
        vp = json.loads(voice_profile_path.read_text())
        vs = vp.get("elevenlabs_settings", {})
    else:
        vs = {}

    client = ElevenLabs(api_key=ELEVEN_API_KEY)
    voice_settings = VoiceSettings(
        stability=vs.get("stability", 0.50),
        similarity_boost=vs.get("similarity_boost", 0.75),
        style=vs.get("style", 0.25),
        speed=vs.get("speed", 0.90),
    )

    MIN_STEP_DURATION = 3.5   # minimum seconds per step (enough to read)
    BREATHING_ROOM    = 0.5   # extra hold after audio finishes

    manifest = []
    narration_count = sum(1 for s in steps if s.get("narration", "").strip())
    print(f"  🎙️  Calling ElevenLabs ({narration_count} API calls, per-step)...")

    def _tts_one(text: str, out_path: Path) -> float:
        """Generate TTS for one narration, return duration in seconds."""
        audio_gen = client.text_to_speech.convert(
            text=text,
            voice_id=ALLISON_VOICE_ID,
            model_id=ELEVEN_MODEL,
            output_format="mp3_44100_128",
            voice_settings=voice_settings,
        )
        with open(out_path, "wb") as fh:
            for chunk in audio_gen:
                fh.write(chunk)
        audio_seg = AudioSegment.from_mp3(out_path)
        return len(audio_seg) / 1000.0

    for i, step in enumerate(steps):
        narration = step.get("narration", "").strip()
        stype = step.get("type", "math")

        # ── ALGEBRA SOLVE: per-sub-step TTS ──
        if stype == "algebra_solve":
            as_cfg = step.get("algebra_solve", {})
            as_steps = as_cfg.get("steps", [])
            total_dur = 0

            for si, sub in enumerate(as_steps):
                sub_narration = sub.get("narration", "").strip()
                if not sub_narration:
                    sub["audio_path"] = ""
                    sub["duration"] = sub.get("hold", MIN_STEP_DURATION)
                    total_dur += sub["duration"]
                    continue

                sub_path = audio_dir / f"step_{i:02d}_sub_{si:02d}.mp3"
                audio_dur = _tts_one(sub_narration, sub_path)
                sub["audio_path"] = str(sub_path)
                sub["duration"] = max(MIN_STEP_DURATION, audio_dur + BREATHING_ROOM)
                total_dur += sub["duration"]

            step["algebra_solve"]["steps"] = as_steps
            manifest.append({
                **step,
                "step": i,
                "audio_path": "",  # no top-level audio — sub-steps have their own
                "duration": total_dur,
            })
            continue

        # ── ALL OTHER STEP TYPES: one TTS per step ──
        if not narration:
            manifest.append({
                **step, "step": i, "audio_path": "", "duration": MIN_STEP_DURATION,
            })
            continue

        out_path = audio_dir / f"step_{i:02d}.mp3"
        audio_dur = _tts_one(narration, out_path)
        step_dur = max(MIN_STEP_DURATION, audio_dur + BREATHING_ROOM)

        manifest.append({
            **step,
            "step":       i,
            "audio_path": str(out_path),
            "duration":   step_dur,
        })

    return manifest


def _split_by_silence(combined_path: Path, audio_dir: Path, narrations: list) -> list[tuple[Path, float]]:
    """
    Split a combined mp3 into per-line segments using pydub silence detection.
    Falls back to equal-duration splitting if silence detection fails.

    Returns list of (path, duration_seconds) tuples.
    """
    combined = AudioSegment.from_mp3(combined_path)

    try:
        from pydub.silence import split_on_silence, detect_silence

        # Find silence gaps ≥250ms (lowered for better splitting)
        silence_ranges = detect_silence(
            combined,
            min_silence_len=250,
            silence_thresh=combined.dBFS - 14,
        )

        if len(silence_ranges) >= len(narrations) - 1:
            # We have enough gaps — split on them
            chunks = []
            prev_end = 0
            for sil_start, sil_end in silence_ranges[:len(narrations) - 1]:
                chunk = combined[prev_end:sil_start]
                chunks.append(chunk)
                prev_end = sil_end
            # Last segment
            chunks.append(combined[prev_end:])

            results = []
            for idx, chunk in enumerate(chunks):
                out = audio_dir / f"step_{idx:02d}.mp3"
                chunk.export(out, format="mp3")
                results.append((out, len(chunk) / 1000.0))
            print(f"  ✓ Split into {len(results)} segments via silence detection")
            return results

    except Exception as e:
        print(f"  ⚠️  Silence detection failed ({e}) — using equal-duration split")

    # Fallback: equal-duration split
    per_line_ms = len(combined) // len(narrations)
    results = []
    for idx in range(len(narrations)):
        start = idx * per_line_ms
        end   = start + per_line_ms if idx < len(narrations) - 1 else len(combined)
        chunk = combined[start:end]
        out   = audio_dir / f"step_{idx:02d}.mp3"
        chunk.export(out, format="mp3")
        results.append((out, len(chunk) / 1000.0))

    print(f"  ✓ Split into {len(results)} segments (equal-duration fallback)")
    return results


# ═══════════════════════════════════════════════════════════════════════════
#  STEP 4 — Render content scene (scene_short.py + manim_short.cfg)
# ═══════════════════════════════════════════════════════════════════════════

def _render_content_scene(manifest: list, job_dir: Path, landscape: bool = False) -> Optional[Path]:
    """
    Write + render the main content scene.
    Portrait (9:16, 1080×1920) by default; landscape (16:9, 1920×1080) if flag set.
    Returns path to rendered mp4 or None on failure.
    """
    from scene_short import create_synced_scene_short

    scene_path = job_dir / "short_scene.py"
    create_synced_scene_short(manifest, str(scene_path), intro_duration=0.0, landscape=landscape)

    env = _manim_env()
    cfg_path = FACTORY_ROOT / "manim_short.cfg"

    resolution = "1920,1080" if landscape else "1080,1920"
    orientation = "16:9, 1920×1080" if landscape else "9:16, 1080×1920"

    cmd = [
        "manim",
        "--config_file", str(cfg_path),
        "--resolution", resolution,
        "--frame_rate", "60",
        "--format", "mp4",
        str(scene_path.name),
        "SyncedShortScene",
    ]

    print(f"  🎨 Rendering content scene ({orientation}) ...")
    result = subprocess.run(cmd, cwd=str(job_dir), env=env, capture_output=True, text=True)

    if result.returncode != 0:
        print(f"  ❌ Manim error:\n{result.stderr[-600:]}")
        return None

    # Manim puts output in media/videos/<scene_stem>/2160p60/ (production_quality)
    # or <quality_folder> depending on config; search broadly
    for quality_folder in ["2160p60", "1080p60", "production_quality", "480p15"]:
        candidate = job_dir / "media" / "videos" / scene_path.stem / quality_folder / "SyncedShortScene.mp4"
        if candidate.exists():
            print(f"  ✓ Content scene: {candidate}")
            return candidate

    # Fallback: glob search
    found = list(job_dir.rglob("SyncedShortScene.mp4"))
    if found:
        print(f"  ✓ Content scene (found): {found[0]}")
        return found[0]

    print("  ❌ Could not locate rendered SyncedShortScene.mp4")
    return None


# ═══════════════════════════════════════════════════════════════════════════
#  STEP 5 — Render intro & outro
# ═══════════════════════════════════════════════════════════════════════════

def _render_intro(job_dir: Path, hook: str) -> Optional[Path]:
    """Render the 2–3s TikTok intro and return path to mp4."""
    from intro_short import build_intro_short_scene

    scene_path = job_dir / "intro_short_scene.py"
    build_intro_short_scene(str(scene_path), hook=hook)

    env = _manim_env()
    cfg_path = FACTORY_ROOT / "manim_short.cfg"

    cmd = [
        "manim",
        "--config_file", str(cfg_path),
        "--resolution", "1080,1920",
        "--frame_rate", "60",
        "--format", "mp4",
        str(scene_path.name),
        "OrbitalIntroShort",
    ]

    print("  🎬 Rendering intro ...")
    result = subprocess.run(cmd, cwd=str(job_dir), env=env, capture_output=True, text=True)

    if result.returncode != 0:
        print(f"  ⚠️  Intro render failed: {result.stderr[-300:]}")
        return None

    found = list(job_dir.rglob("OrbitalIntroShort.mp4"))
    if found:
        print(f"  ✓ Intro: {found[0]}")
        return found[0]

    return None


def _render_outro(job_dir: Path, cta: str = "Follow for more") -> Optional[Path]:
    """Render the 2s outro and return path to mp4."""
    from outro_short import build_outro_short_scene

    scene_path = job_dir / "outro_short_scene.py"
    build_outro_short_scene(str(scene_path), cta=cta)

    env = _manim_env()
    cfg_path = FACTORY_ROOT / "manim_short.cfg"

    cmd = [
        "manim",
        "--config_file", str(cfg_path),
        "--resolution", "1080,1920",
        "--frame_rate", "60",
        "--format", "mp4",
        str(scene_path.name),
        "OrbitalOutroShort",
    ]

    print("  🎬 Rendering outro ...")
    result = subprocess.run(cmd, cwd=str(job_dir), env=env, capture_output=True, text=True)

    if result.returncode != 0:
        print(f"  ⚠️  Outro render failed: {result.stderr[-300:]}")
        return None

    found = list(job_dir.rglob("OrbitalOutroShort.mp4"))
    if found:
        print(f"  ✓ Outro: {found[0]}")
        return found[0]

    return None


# ═══════════════════════════════════════════════════════════════════════════
#  STEP 6 — Stitch (intro + content + outro)
# ═══════════════════════════════════════════════════════════════════════════

def _stitch_video(
    intro_path: Optional[Path],
    content_path: Path,
    outro_path: Optional[Path],
    output_path: Path,
) -> Path:
    """
    FFmpeg concat: intro + content → final mp4.
    Uses the SAME single-pass approach as the standard pipeline.
    NO intermediate normalization — that was causing audio/video desync.
    """
    segments = []
    if intro_path and intro_path.exists():
        segments.append(intro_path)
    segments.append(content_path)
    if outro_path and outro_path.exists():
        segments.append(outro_path)

    if len(segments) == 1:
        shutil.copy(segments[0], output_path)
        print(f"  ✓ No stitch needed — copied content directly")
        return output_path

    # Write concat list (same as standard pipeline)
    concat_list = output_path.parent / "concat_list.txt"
    with open(concat_list, "w") as fh:
        for seg in segments:
            fh.write(f"file '{seg.resolve()}'\n")

    # Single-pass concat + re-encode (same approach as standard pipeline)
    # Add silent audio source to fill gaps (intro has no audio)
    cmd = [
        "ffmpeg", "-y",
        "-f", "concat", "-safe", "0",
        "-i", str(concat_list),
        "-f", "lavfi", "-i", "anullsrc=r=44100:cl=stereo",
        "-filter_complex",
        "[0:a?][1:a]amix=inputs=2:duration=first:dropout_transition=0[aout]",
        "-map", "0:v",
        "-map", "[aout]",
        "-c:v", "libx264",
        "-c:a", "aac", "-b:a", "192k",
        "-movflags", "+faststart",
        str(output_path),
    ]

    result = subprocess.run(cmd, capture_output=True, text=True)
    if result.returncode != 0:
        print(f"  ⚠️  FFmpeg stitch failed: {result.stderr[-400:]}")
        # Fallback: just use content
        shutil.copy(content_path, output_path)
    else:
        print(f"  ✓ Stitched: {output_path}")

    return output_path


def _mix_background_music(video_path: Path, music_path: Path, output_path: Path, volume: float = 0.12) -> Path:
    """
    Mix background music under the video at the given volume (0.0–1.0).
    Music is trimmed/faded to match video length. Original audio preserved at full volume.
    """
    if not music_path.exists():
        print(f"  ⚠️  Background music not found: {music_path}")
        return video_path

    video_dur = _get_video_duration(video_path)
    if video_dur <= 0:
        return video_path

    # FFmpeg: mix original audio (full volume) with music (low volume), fade out music at end
    cmd = [
        "ffmpeg", "-y",
        "-i", str(video_path),
        "-stream_loop", "-1",
        "-i", str(music_path),
        "-filter_complex",
        f"[1:a]atrim=0:{video_dur},afade=t=in:st=0:d=2,afade=t=out:st={video_dur-2}:d=2,volume={volume}[music];"
        f"[0:a][music]amix=inputs=2:duration=first:dropout_transition=2[out]",
        "-map", "0:v",
        "-map", "[out]",
        "-c:v", "copy",
        "-c:a", "aac", "-b:a", "192k",
        "-movflags", "+faststart",
        str(output_path),
    ]

    result = subprocess.run(cmd, capture_output=True, text=True)
    if result.returncode != 0:
        print(f"  ⚠️  Music mix failed: {result.stderr[-300:]}")
        return video_path

    print(f"  ✓ Background music mixed at {int(volume*100)}% volume")
    return output_path


# ═══════════════════════════════════════════════════════════════════════════
#  HELPERS
# ═══════════════════════════════════════════════════════════════════════════

def _manim_env() -> dict:
    env = os.environ.copy()
    home = Path.home()
    extra = ":".join([
        str(home / "Library" / "TinyTeX" / "bin" / "universal-darwin"),
        str(home / "Library" / "Python" / "3.9" / "bin"),
        "/opt/homebrew/bin",
        "/usr/local/bin",
    ])
    env["PATH"] = extra + ":" + env.get("PATH", "")
    return env


def _get_video_duration(path: Path) -> float:
    """Return duration of a video file in seconds via ffprobe."""
    try:
        result = subprocess.run(
            ["ffprobe", "-v", "quiet", "-print_format", "json",
             "-show_format", str(path)],
            capture_output=True, text=True,
        )
        info = json.loads(result.stdout)
        return float(info["format"]["duration"])
    except Exception:
        return 0.0


def _estimate_cost(num_tts_chars: int, num_sonnet_tokens: int) -> float:
    """
    Rough cost estimate in USD.
    ElevenLabs Turbo: ~$0.18 / 1000 chars
    Claude Sonnet input: ~$3 / 1M tokens → $0.003 / 1K
    """
    tts_cost    = (num_tts_chars / 1000) * 0.18
    sonnet_cost = (num_sonnet_tokens / 1000) * 0.003
    return round(tts_cost + sonnet_cost, 4)


# ═══════════════════════════════════════════════════════════════════════════
#  PUBLIC API
# ═══════════════════════════════════════════════════════════════════════════

def generate_short_video(
    problem: str,
    hook: Optional[str] = None,
    difficulty: str = "medium",
    cta: str = "Follow for more",
    output_name: Optional[str] = None,
    skip_verify: bool = False,
    script_path: Optional[str] = None,
    visual_only: bool = False,
    landscape: bool = False,
    mode: str = "howto",
) -> dict:
    """
    Generate a math video end-to-end.

    Args:
        problem     : Math problem description / equation string.
                      For mode="why", this is the concept (e.g., "Why does the chain rule work?")
        hook        : Hook overlay text for intro. Random if None.
        difficulty  : "easy" | "medium" | "hard" (affects verification depth).
        cta         : Call-to-action for outro (default: "Follow for more").
        output_name : Output filename (auto-generated if None).
        skip_verify : Skip Sonnet verification pass.
        visual_only : If True, skip TTS and render silent video for visual review.
        landscape   : If True, render 16:9 (1920x1080) instead of 9:16 (1080x1920).
        mode        : "howto" (step-by-step problem) | "why" (why does this rule work?).

    Returns:
        {
            "video_path": str,
            "duration":   float,  # seconds
            "cost":       float,  # USD estimate
            "script":     dict,   # generated script
        }
    """
    start_time = time.time()

    print("\n" + "=" * 62)
    print(f"🚀 ORBITAL SHORT-FORM PIPELINE ({mode.upper()} mode)")
    print("=" * 62)
    print(f"   {'Concept' if mode == 'why' else 'Problem'}    : {problem[:70]}")
    print(f"   Difficulty : {difficulty}")
    print(f"   Mode       : {mode}")
    hook = hook or random.choice(HOOKS)
    print(f"   Hook       : {hook!r}")
    print()

    # ── job directory ──────────────────────────────────────────────
    job_slug   = re.sub(r"[^\w]", "_", problem[:40]).strip("_").lower()
    job_slug   = re.sub(r"_+", "_", job_slug)
    job_dir    = JOBS_DIR / f"short_{job_slug}"
    job_dir.mkdir(parents=True, exist_ok=True)
    OUTPUT_DIR.mkdir(parents=True, exist_ok=True)

    # ── step 1: script ─────────────────────────────────────────────
    if script_path and Path(script_path).exists():
        print(f"📝 Step 1/6 — Loading pre-built script: {script_path}")
        script = json.loads(Path(script_path).read_text())
        steps  = script.get("steps", [])
        print(f"  ✓ {len(steps)} steps loaded (Circle-reviewed)")
    else:
        if mode == "why":
            print("📝 Step 1/6 — Generating WHY script (DeepSeek V3) ...")
            script = _call_deepseek_why(problem)
        else:
            print("📝 Step 1/6 — Generating script (DeepSeek V3) ...")
            script = _call_deepseek(problem, difficulty)
        steps  = script.get("steps", [])

        # ── Reorder: move graph steps to the front and mark persistent ──
        graph_steps = [s for s in steps if s.get("type") == "graph"]
        non_graph   = [s for s in steps if s.get("type") != "graph"]
        for gs in graph_steps:
            gs["persistent"] = True
        steps = graph_steps + non_graph
        script["steps"] = steps

        print(f"  ✓ {len(steps)} steps generated")
        if graph_steps:
            print(f"  ✓ Graph moved to front (persistent)")

    script_path = job_dir / "script.json"
    script_path.write_text(json.dumps(script, indent=2))

    # ── step 2: verification ───────────────────────────────────────
    if not skip_verify:
        print("\n🔬 Step 2/6 — Verification (Sonnet) ...")
        passed, verdict = _verify_script_sonnet(script, difficulty)
        print(f"  {'✅' if passed else '❌'} {verdict}")
        if not passed:
            raise ValueError(
                f"Verification FAILED — fix the script before rendering.\n"
                f"Verdict: {verdict}\n"
                f"Script saved to: {script_path}"
            )
    else:
        print("\n⏭️  Step 2/6 — Verification skipped")

    # ── step 3: TTS ────────────────────────────────────────────────
    DEFAULT_VISUAL_DURATION = 4.0  # seconds per step when no audio
    audio_dir = job_dir / "audio"
    total_tts_chars = 0

    if visual_only:
        print("\n👁️  Step 3/6 — VISUAL ONLY (no TTS, $0 cost)")
        # Build manifest with default durations, no audio
        manifest = []
        for i, step in enumerate(steps):
            stype = step.get("type", "math")
            if stype == "algebra_solve":
                as_cfg = step.get("algebra_solve", {})
                for sub in as_cfg.get("steps", []):
                    sub["audio_path"] = ""
                    sub["duration"] = sub.get("hold", DEFAULT_VISUAL_DURATION)
                step["algebra_solve"] = as_cfg
                manifest.append({**step, "step": i, "audio_path": "", "duration": sum(s.get("duration", DEFAULT_VISUAL_DURATION) for s in as_cfg.get("steps", []))})
            else:
                manifest.append({**step, "step": i, "audio_path": "", "duration": step.get("duration", DEFAULT_VISUAL_DURATION)})
        total_duration = sum(s.get("duration", 0) for s in manifest)
        print(f"  ✓ Visual preview: {total_duration:.1f}s (default timing)")
    else:
        print("\n🎙️  Step 3/6 — Generating TTS (Allison, ElevenLabs) ...")
        manifest = _generate_all_tts(steps, audio_dir)
        total_tts_chars = sum(len(s.get("narration", "")) for s in steps)
        total_duration  = sum(s.get("duration", 0) for s in manifest)
        print(f"  ✓ Total TTS duration: {total_duration:.1f}s")

    manifest_path = job_dir / "manifest.json"
    manifest_path.write_text(json.dumps(manifest, indent=2))

    # ── step 4: render content scene ──────────────────────────────
    print("\n🎨 Step 4/6 — Rendering content scene ...")
    content_video = _render_content_scene(manifest, job_dir, landscape=landscape)
    if content_video is None:
        raise RuntimeError("Content scene render failed — check Manim logs.")

    # ── step 5: skip intro for now (end card is in scene) ───────────
    print("\n🎬 Step 5/6 — Skipping separate intro (end card built into scene)")

    # ── step 6: just use content video directly (no stitch = no desync) ─
    print("\n🎞️  Step 6/6 — Finalizing video ...")
    output_name = output_name or f"short_{job_slug}_{int(time.time())}.mp4"
    if not output_name.endswith(".mp4"):
        output_name += ".mp4"
    final_path  = OUTPUT_DIR / output_name

    shutil.copy(content_video, final_path)
    print(f"  ✓ Output: {final_path}")

    # ── step 6b: mix background music (skip for visual-only) ──────
    bg_music = FACTORY_ROOT / "assets" / "audio" / "bg_synthwave.mp3"
    if bg_music.exists() and not visual_only:
        print("\n🎵 Mixing background music ...")
        final_with_music = OUTPUT_DIR / f"_music_{output_name}"
        result_path = _mix_background_music(final_path, bg_music, final_with_music, volume=0.12)
        if result_path != final_path:
            # Replace the stitched file with the music version
            shutil.move(str(final_with_music), str(final_path))
    elif visual_only:
        print("\n👁️  Skipping music mix (visual-only)")

    # ── results ────────────────────────────────────────────────────
    final_duration = _get_video_duration(final_path)
    elapsed        = time.time() - start_time
    cost           = _estimate_cost(total_tts_chars, num_sonnet_tokens=512)

    print("\n" + "=" * 62)
    print(f"✅ DONE in {elapsed:.0f}s")
    print(f"   Video  : {final_path}")
    print(f"   Length : {final_duration:.1f}s")
    print(f"   Cost   : ~${cost:.4f}")
    print("=" * 62 + "\n")

    return {
        "video_path": str(final_path),
        "duration":   final_duration,
        "cost":       cost,
        "script":     script,
    }


# ═══════════════════════════════════════════════════════════════════════════
#  CLI entry-point
# ═══════════════════════════════════════════════════════════════════════════

if __name__ == "__main__":
    import argparse

    parser = argparse.ArgumentParser(description="Orbital Short-Form Video Pipeline")
    parser.add_argument("problem", help="Math problem string")
    parser.add_argument("--hook",       default=None,     help="Hook text (random if omitted)")
    parser.add_argument("--difficulty", default="medium", choices=["easy", "medium", "hard"])
    parser.add_argument("--cta",        default="Follow for more", help="Outro call-to-action")
    parser.add_argument("--output",     default=None,     help="Output filename")
    parser.add_argument("--skip-verify", action="store_true")
    parser.add_argument("--visual-only", action="store_true", help="Render silent video (no TTS, $0 cost)")
    parser.add_argument("--landscape", action="store_true", help="Render 16:9 landscape (1920x1080) instead of 9:16 portrait")

    args = parser.parse_args()

    result = generate_short_video(
        problem     = args.problem,
        hook        = args.hook,
        difficulty  = args.difficulty,
        cta         = args.cta,
        output_name = args.output,
        skip_verify = args.skip_verify,
        visual_only = args.visual_only,
        landscape   = args.landscape,
    )

    if result:
        subprocess.run(["open", result["video_path"]])
