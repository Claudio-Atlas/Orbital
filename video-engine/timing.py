"""
timing.py — Narration Timeline & Audio-Visual Sync System
===========================================================
Implements the Production Bible's timing model for the Video Template Engine.

Pipeline:
  1. Template generates manifest with estimated timing + narration text
  2. TTS generates audio files per step → exact durations in manifest.json
  3. sync_pass() adjusts manifest timing to match actual TTS durations
  4. Renderer uses synced manifest → audio and visuals land together

Key concepts from the Bible:
  - Narration timeline choreography: visuals appear WHEN she says the thing
  - Gate wait: prevents TTS overlap between scenes
  - Sync pass: compares TTS duration vs animation time, adjusts accordingly
  - Alive fillers: glow/drift/breathe during audio > animation gaps
  - Audio-first rule: never re-generate TTS to match visuals
  - 0.8s minimum gap between scenes (breathing room)

Usage:
    from timing import (
        estimate_narration_duration,
        build_narration_timeline,
        sync_pass,
        gate_wait,
        generate_tts_manifest,
    )
"""

import os
import re
import json
import subprocess
from pathlib import Path
from typing import Optional


# ─── Constants ────────────────────────────────────────────────────────────────

# Words per second for TTS estimation (Allison at 0.90 speed)
WORDS_PER_SECOND = 2.8

# Minimum gap between scenes (Bible: 0.8s)
SCENE_GAP_SECONDS = 0.8

# Animation ratio (portion of step duration spent animating vs holding)
ANIMATION_RATIO = 0.35

# Extra hold between steps (breathing room)
EXTRA_HOLD = 0.5

# Thresholds for sync pass decisions
SYNC_CLOSE_THRESHOLD = 1.5    # ±1.5s = gate_wait handles it
SYNC_FILLER_THRESHOLD = 2.0   # >2s gap = needs alive filler
SYNC_MAJOR_THRESHOLD = 5.0    # >5s = scene design is wrong

# TTS settings (Allison voice — from Bible)
TTS_VOICE_ID = "5jVVMAv2LzffTcLGarKh"
TTS_MODEL = "eleven_turbo_v2_5"
TTS_SETTINGS = {
    "stability": 0.50,
    "similarity_boost": 0.75,
    "style": 0.25,
    "speed": 0.90,
}

# Audio normalization target
NORMALIZE_DB = -26.0


# ─── Duration Estimation ─────────────────────────────────────────────────────

def estimate_narration_duration(text: str) -> float:
    """
    Estimate TTS duration from narration text.

    Uses word count / words-per-second with adjustments for:
      - Math expressions (slower to speak)
      - Short phrases (minimum duration)
      - Punctuation pauses

    Returns estimated seconds.
    """
    if not text or not text.strip():
        return 1.0

    # Count words (split on whitespace)
    words = text.split()
    word_count = len(words)

    # Base duration from word count
    base_duration = word_count / WORDS_PER_SECOND

    # Math content takes longer to speak (numbers, variables, operators)
    math_chars = sum(1 for c in text if c in '0123456789+-*/^=(){}[]<>≤≥')
    math_penalty = math_chars * 0.08  # ~80ms per math character

    # Pause for periods, commas, colons
    pause_chars = text.count('.') + text.count('?') + text.count('!')
    comma_chars = text.count(',') + text.count(':') + text.count(';')
    pause_time = pause_chars * 0.3 + comma_chars * 0.15

    # "Equals" spoken as a word takes time
    equals_count = text.lower().count('equals')
    equals_time = equals_count * 0.2

    total = base_duration + math_penalty + pause_time + equals_time

    # Minimum duration (even a short phrase needs time)
    return max(1.5, total)


def estimate_animation_time(step: dict) -> float:
    """
    Estimate how long the animations for a step will take.

    Based on step type and content complexity.
    """
    stype = step.get("type", "math")
    duration = step.get("duration", 3.0)

    if stype == "algebra_solve":
        sub_steps = step.get("algebra_solve", {}).get("steps", [])
        total = 0
        for s in sub_steps:
            sub_dur = s.get("duration", 3.0)
            # Each sub-step: write animation + note + hold + extra_hold
            # The renderer actually holds for most of sub_dur, not just the anim portion
            anim = max(0.6, sub_dur * ANIMATION_RATIO)
            note_time = 0.3 if s.get("note") else 0
            note_fadeout = 0.2 if s.get("note") else 0
            final_time = 0.6 if s == sub_steps[-1] else 0
            remaining = max(0.3, sub_dur - anim - note_time - final_time)
            total += anim + note_time + note_fadeout + final_time + remaining + EXTRA_HOLD
        # Add title animation time
        if step.get("algebra_solve", {}).get("title"):
            total += 1.3  # write(0.5) + wait(0.5) + fadeout(0.3)
        return total

    elif stype == "graph":
        return max(1.2, duration * ANIMATION_RATIO) + 0.8  # slide-down

    elif stype == "box":
        anim = max(1.2, duration * ANIMATION_RATIO)
        return anim + 0.45  # transition

    else:  # math
        anim = max(1.2, duration * ANIMATION_RATIO)
        return anim + 0.45


# ─── Narration Timeline ──────────────────────────────────────────────────────

def build_narration_timeline(narration_text: str, total_duration: float) -> list[dict]:
    """
    Build a word-level timeline from narration text.

    Splits narration into phrases (by sentence/clause) and estimates
    when each phrase starts within the total duration.

    This is the estimated version — after TTS generation, actual timestamps
    from the audio should replace these estimates.

    Returns:
        List of dicts: [{"phrase": str, "start_s": float, "end_s": float}, ...]
    """
    if not narration_text or total_duration <= 0:
        return []

    # Split into phrases at natural breaks
    phrases = _split_into_phrases(narration_text)
    if not phrases:
        return [{"phrase": narration_text, "start_s": 0.0, "end_s": total_duration}]

    # Estimate duration of each phrase proportionally
    phrase_durations = []
    total_words = 0
    for phrase in phrases:
        word_count = len(phrase.split())
        total_words += word_count
        phrase_durations.append(word_count)

    # Distribute total_duration across phrases proportionally
    timeline = []
    current_time = 0.0
    for i, (phrase, word_count) in enumerate(zip(phrases, phrase_durations)):
        proportion = word_count / max(1, total_words)
        phrase_dur = total_duration * proportion
        timeline.append({
            "phrase": phrase,
            "start_s": round(current_time, 2),
            "end_s": round(current_time + phrase_dur, 2),
        })
        current_time += phrase_dur

    return timeline


def _split_into_phrases(text: str) -> list[str]:
    """Split narration text into speakable phrases."""
    # Split on sentence boundaries and clause boundaries
    # Keep splits meaningful (not single words)
    parts = re.split(r'(?<=[.!?])\s+|(?<=,)\s+(?=[A-Z])|;\s+', text)
    phrases = [p.strip() for p in parts if p.strip() and len(p.strip()) > 2]
    return phrases if phrases else [text]


# ─── Sync Points ─────────────────────────────────────────────────────────────

def build_sync_points(step: dict, narration_timeline: list[dict]) -> list[dict]:
    """
    Define sync points: which visual event should land on which narration phrase.

    A sync point maps a narration moment to a visual action:
        {"narration_phrase": "...", "at_s": 1.5, "visual_action": "write_equation"}

    These are used by the renderer to time animations to specific words.

    Returns:
        List of sync point dicts
    """
    sync_points = []
    stype = step.get("type", "math")

    if not narration_timeline:
        return sync_points

    if stype == "math":
        # The equation should appear when the narrator mentions it
        # Usually the first phrase is setup, equation appears on second
        if len(narration_timeline) >= 2:
            sync_points.append({
                "at_s": narration_timeline[1]["start_s"],
                "visual_action": "write_equation",
                "narration_phrase": narration_timeline[1]["phrase"],
            })
        else:
            sync_points.append({
                "at_s": narration_timeline[0]["start_s"] + 0.5,
                "visual_action": "write_equation",
                "narration_phrase": narration_timeline[0]["phrase"],
            })

    elif stype == "box":
        # Box appears right at the start (it's usually a header or answer)
        sync_points.append({
            "at_s": 0.3,
            "visual_action": "reveal_box",
            "narration_phrase": narration_timeline[0]["phrase"],
        })

    elif stype == "algebra_solve":
        # Each sub-step should sync to a narration phrase
        sub_steps = step.get("algebra_solve", {}).get("steps", [])
        # Distribute sync points across the narration timeline
        if len(sub_steps) > 0 and len(narration_timeline) > 0:
            # Map each sub-step to the nearest timeline entry
            step_interval = len(narration_timeline) / max(1, len(sub_steps))
            for i in range(len(sub_steps)):
                timeline_idx = min(int(i * step_interval), len(narration_timeline) - 1)
                sync_points.append({
                    "at_s": narration_timeline[timeline_idx]["start_s"],
                    "visual_action": f"write_substep_{i}",
                    "narration_phrase": narration_timeline[timeline_idx]["phrase"],
                })

    elif stype == "graph":
        # Graph axes appear first, curve draws when narrator mentions the function
        if len(narration_timeline) >= 1:
            sync_points.append({
                "at_s": 0.2,
                "visual_action": "show_axes",
                "narration_phrase": "",
            })
            sync_points.append({
                "at_s": narration_timeline[0]["start_s"] + 0.5,
                "visual_action": "draw_curve",
                "narration_phrase": narration_timeline[0]["phrase"],
            })

    return sync_points


# ─── Gate Wait ────────────────────────────────────────────────────────────────

def gate_wait(audio_duration: float, total_animation_time: float) -> float:
    """
    Calculate wait time to prevent TTS overlap.

    From the Bible:
        wait = max(0.1, audio_duration - total_animation_time)

    This ensures the next add_sound() doesn't fire until the current
    audio has finished playing.
    """
    return max(0.1, audio_duration - total_animation_time)


# ─── Sync Pass ────────────────────────────────────────────────────────────────

def sync_pass(manifest: list[dict]) -> list[dict]:
    """
    The sync pass — adjusts manifest timing after TTS generation.

    For each step, compares:
        delta = TTS_duration - total_animation_time

    Actions (from the Bible):
        ±1.5s  → gate_wait handles it (no changes)
        >+2s   → add alive_filler instruction
        <-2s   → scale animation run_times down
        >+5s   → flag as needing scene redesign
        <-5s   → flag narration as too short

    Args:
        manifest: list of step dicts WITH tts_duration field set
                  (from TTS generation or estimation)

    Returns:
        Updated manifest with sync metadata added to each step
    """
    synced = []

    for step in manifest:
        step = dict(step)  # copy
        stype = step.get("type", "math")

        # Get TTS duration (actual from audio, or estimated from narration)
        tts_dur = step.get("tts_duration", 0)
        if tts_dur == 0:
            narration = step.get("narration", "")
            tts_dur = estimate_narration_duration(narration)
            step["tts_duration"] = tts_dur

        # Get animation time estimate
        anim_time = estimate_animation_time(step)

        # Calculate delta
        delta = tts_dur - anim_time
        step["_sync"] = {
            "tts_duration": round(tts_dur, 2),
            "animation_time": round(anim_time, 2),
            "delta": round(delta, 2),
            "action": "none",
        }

        if abs(delta) <= SYNC_CLOSE_THRESHOLD:
            # Close enough — gate_wait handles it
            step["_sync"]["action"] = "gate_wait"
            step["gate_wait"] = gate_wait(tts_dur, anim_time)

        elif delta > SYNC_MAJOR_THRESHOLD:
            # Way too long — scene needs redesign
            step["_sync"]["action"] = "REDESIGN_NEEDED"
            step["_sync"]["warning"] = (
                f"Audio is {delta:.1f}s longer than visuals. "
                f"Split this scene or add a secondary visual beat."
            )
            step["gate_wait"] = gate_wait(tts_dur, anim_time)
            step["alive_filler"] = _suggest_filler(stype, delta)

        elif delta > SYNC_FILLER_THRESHOLD:
            # Audio longer — add alive filler
            step["_sync"]["action"] = "alive_filler"
            step["gate_wait"] = gate_wait(tts_dur, anim_time)
            step["alive_filler"] = _suggest_filler(stype, delta)

        elif delta < -SYNC_MAJOR_THRESHOLD:
            # Way too short — narration needs revision
            step["_sync"]["action"] = "NARRATION_TOO_SHORT"
            step["_sync"]["warning"] = (
                f"Audio is {abs(delta):.1f}s shorter than visuals. "
                f"Revise narration for this scene only."
            )
            step["animation_scale"] = tts_dur / max(0.1, anim_time)

        elif delta < -SYNC_FILLER_THRESHOLD:
            # Audio shorter — compress animations
            step["_sync"]["action"] = "compress_animations"
            step["animation_scale"] = tts_dur / max(0.1, anim_time)

        else:
            step["_sync"]["action"] = "gate_wait"
            step["gate_wait"] = max(0.1, delta)

        # Update step duration to match TTS (audio is king)
        step["duration"] = max(step.get("duration", 0), tts_dur + SCENE_GAP_SECONDS)

        # Build narration timeline for this step
        timeline = build_narration_timeline(
            step.get("narration", ""),
            tts_dur
        )
        step["narration_timeline"] = timeline

        # Build sync points
        sync_points = build_sync_points(step, timeline)
        step["sync_points"] = sync_points

        synced.append(step)

    return synced


def _suggest_filler(stype: str, gap: float) -> dict:
    """
    Suggest an alive filler strategy for audio > animation gaps.

    From the Bible:
      - Glow pulse cycle: best for boxed content
      - Subtle drift: best for standalone equations
      - Opacity breathe: best for background elements
    """
    if stype == "box":
        return {
            "type": "glow_pulse",
            "duration": round(gap, 2),
            "cycles": max(1, int(gap / 1.0)),
            "note": "Bloom glow on boxed content while narration continues",
        }
    elif stype == "math":
        return {
            "type": "subtle_drift",
            "duration": round(gap, 2),
            "shift_y": 0.05,
            "note": "Gentle up/down drift on equation while narration continues",
        }
    elif stype == "algebra_solve":
        return {
            "type": "opacity_breathe",
            "duration": round(gap, 2),
            "target": "latest_equation",
            "note": "Breathe opacity on latest equation while narration continues",
        }
    elif stype == "graph":
        return {
            "type": "glow_pulse",
            "duration": round(gap, 2),
            "target": "curve",
            "note": "Pulse glow on curve while narration continues",
        }
    return {
        "type": "wait",
        "duration": round(gap, 2),
        "note": "Simple hold — consider adding visual interest",
    }


# ─── TTS Manifest Generation ─────────────────────────────────────────────────

def generate_tts_manifest(manifest: list[dict], output_dir: str) -> dict:
    """
    Generate a TTS manifest from a video manifest.

    Creates a JSON file that gen_tts.py can consume to generate
    per-step audio files.

    Args:
        manifest: video manifest with narration fields
        output_dir: directory for TTS output files

    Returns:
        TTS manifest dict (also written to output_dir/tts_manifest.json)
    """
    os.makedirs(output_dir, exist_ok=True)

    tts_manifest = {
        "voice_id": TTS_VOICE_ID,
        "model_id": TTS_MODEL,
        "voice_settings": TTS_SETTINGS,
        "normalize_db": NORMALIZE_DB,
        "output_dir": output_dir,
        "scenes": [],
    }

    for i, step in enumerate(manifest):
        narration = step.get("narration", "")
        if not narration:
            continue

        stype = step.get("type", "math")
        step_id = f"step_{i:02d}_{stype}"

        # For algebra_solve, we can do per-substep TTS or one big chunk
        # Bible says: "One API call per scene/step. NOT per-sentence."
        # So we combine all sub-step narrations for algebra_solve

        if stype == "algebra_solve":
            sub_steps = step.get("algebra_solve", {}).get("steps", [])
            combined_narration = " ".join(
                s.get("narration", "") for s in sub_steps if s.get("narration")
            )
            if combined_narration:
                narration = combined_narration

        # Apply pronunciation fixes (from Bible)
        narration_fixed = _fix_pronunciation(narration)

        scene_entry = {
            "id": step_id,
            "text": narration_fixed,
            "estimated_duration": estimate_narration_duration(narration),
            "output_file": f"{step_id}.mp3",
        }
        tts_manifest["scenes"].append(scene_entry)

    # Write the manifest
    manifest_path = os.path.join(output_dir, "tts_manifest.json")
    with open(manifest_path, 'w') as f:
        json.dump(tts_manifest, f, indent=2)

    print(f"  ✓ TTS manifest: {manifest_path} ({len(tts_manifest['scenes'])} scenes)")
    return tts_manifest


def _fix_pronunciation(text: str) -> str:
    """
    Apply ElevenLabs pronunciation fixes from the Bible.

    - "sine" → "sign"
    - "cosine" → "cosign"
    - "ln" → "L N"
    - "d/dx" → "dee dee ex"
    """
    fixes = [
        (r'\bsine\b', 'sign'),
        (r'\bcosine\b', 'cosign'),
        (r'\bln\b', 'L N'),
        (r'\bd/dx\b', 'dee dee ex'),
        (r'\bd/dy\b', 'dee dee why'),
        (r'\bdx\b', 'dee ex'),
        (r'\bdy\b', 'dee why'),
    ]
    for pattern, replacement in fixes:
        text = re.sub(pattern, replacement, text, flags=re.IGNORECASE)
    return text


# ─── Load TTS Results ─────────────────────────────────────────────────────────

def load_tts_results(tts_dir: str, manifest: list[dict]) -> list[dict]:
    """
    After TTS generation, load actual durations and audio paths into manifest.

    Reads the TTS output manifest (with actual durations from audio files)
    and updates the video manifest with:
      - tts_duration: actual seconds from audio file
      - audio_path: path to the generated .mp3

    Then runs sync_pass() to adjust timing.

    Args:
        tts_dir: directory containing generated TTS files + manifest.json
        manifest: original video manifest

    Returns:
        Updated manifest with actual TTS durations and sync metadata
    """
    # Look for the TTS results manifest
    results_path = os.path.join(tts_dir, "manifest.json")
    if not os.path.exists(results_path):
        results_path = os.path.join(tts_dir, "tts_manifest.json")

    tts_results = {}
    if os.path.exists(results_path):
        with open(results_path) as f:
            data = json.load(f)
        for scene in data.get("scenes", []):
            tts_results[scene["id"]] = scene

    # Update manifest with actual durations
    updated = []
    for i, step in enumerate(manifest):
        step = dict(step)
        stype = step.get("type", "math")
        step_id = f"step_{i:02d}_{stype}"

        if step_id in tts_results:
            result = tts_results[step_id]
            audio_file = os.path.join(tts_dir, result.get("output_file", ""))

            if os.path.exists(audio_file):
                # Get actual duration from audio file
                actual_dur = _get_audio_duration(audio_file)
                if actual_dur > 0:
                    step["tts_duration"] = actual_dur
                step["audio_path"] = audio_file
            else:
                # Use estimated duration
                step["tts_duration"] = result.get("duration",
                    result.get("estimated_duration",
                        estimate_narration_duration(step.get("narration", ""))))

        updated.append(step)

    # Run the sync pass with actual durations
    return sync_pass(updated)


def _get_audio_duration(audio_path: str) -> float:
    """Get duration of an audio file using ffprobe."""
    try:
        result = subprocess.run(
            ["ffprobe", "-v", "error", "-show_entries", "format=duration",
             "-of", "csv=p=0", audio_path],
            capture_output=True, text=True, timeout=10
        )
        if result.returncode == 0:
            return float(result.stdout.strip())
    except (subprocess.TimeoutExpired, ValueError, FileNotFoundError):
        pass
    return 0.0


# ─── Sync Report ──────────────────────────────────────────────────────────────

def sync_report(manifest: list[dict]) -> str:
    """
    Generate a human-readable sync report for a manifest.

    Shows per-step timing analysis and any warnings.
    Use this to verify timing before rendering.
    """
    lines = [
        "═" * 60,
        "  Audio-Visual Sync Report",
        "═" * 60,
        "",
    ]

    total_duration = 0
    warnings = []

    for i, step in enumerate(manifest):
        stype = step.get("type", "?")
        sync = step.get("_sync", {})
        tts_dur = sync.get("tts_duration", step.get("tts_duration", 0))
        anim_time = sync.get("animation_time", 0)
        delta = sync.get("delta", 0)
        action = sync.get("action", "unknown")
        duration = step.get("duration", 0)
        total_duration += duration

        status = "✅" if action in ("gate_wait", "none") else "⚠️" if "filler" in action else "❌"

        lines.append(f"  [{i+1:2d}] {stype:18s} | TTS: {tts_dur:5.1f}s | Anim: {anim_time:5.1f}s | Δ: {delta:+5.1f}s | {status} {action}")

        if sync.get("warning"):
            warnings.append(f"  Step {i+1}: {sync['warning']}")

        # Show alive filler if present
        filler = step.get("alive_filler")
        if filler:
            lines.append(f"       → Filler: {filler['type']} ({filler['duration']:.1f}s)")

    lines += [
        "",
        "─" * 60,
        f"  Total estimated duration: {total_duration:.1f}s",
        f"  Scene gaps ({SCENE_GAP_SECONDS}s × {len(manifest)}): {SCENE_GAP_SECONDS * len(manifest):.1f}s",
        "",
    ]

    if warnings:
        lines += ["  ⚠️  WARNINGS:", ""] + warnings + [""]

    # Sync checklist (from Bible)
    lines += [
        "  Sync Checklist:",
        "  □ Every scene has narration text",
        "  □ No gap > 2s without an alive filler",
        "  □ No silence during active animation",
        f"  □ Total duration within ±3s of TTS sum",
        "",
        "═" * 60,
    ]

    return "\n".join(lines)


# ─── CLI ──────────────────────────────────────────────────────────────────────

if __name__ == "__main__":
    import sys

    if len(sys.argv) < 2:
        print("Usage:")
        print("  python timing.py <manifest.json>              — run sync pass + report")
        print("  python timing.py <manifest.json> --tts <dir>  — generate TTS manifest")
        print("  python timing.py <manifest.json> --load <dir> — load TTS results + sync")
        sys.exit(0)

    manifest_path = sys.argv[1]
    with open(manifest_path) as f:
        manifest = json.load(f)

    if len(sys.argv) >= 4 and sys.argv[2] == "--tts":
        # Generate TTS manifest
        tts_dir = sys.argv[3]
        generate_tts_manifest(manifest, tts_dir)

    elif len(sys.argv) >= 4 and sys.argv[2] == "--load":
        # Load TTS results and run sync pass
        tts_dir = sys.argv[3]
        synced = load_tts_results(tts_dir, manifest)
        print(sync_report(synced))

        # Save synced manifest
        output_path = manifest_path.replace(".json", "_synced.json")
        with open(output_path, 'w') as f:
            json.dump(synced, f, indent=2)
        print(f"\n  ✓ Synced manifest: {output_path}")

    else:
        # Just run sync pass with estimated durations
        synced = sync_pass(manifest)
        print(sync_report(synced))
