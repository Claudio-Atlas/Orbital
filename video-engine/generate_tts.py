#!/usr/bin/env python3
"""
generate_tts.py — Generate TTS audio for a video engine manifest
================================================================
Uses ElevenLabs (Allison voice) with settings from PRODUCTION_BIBLE.md.

Usage:
    python3 generate_tts.py <manifest_or_question.json> <output_dir>

Generates per-step .mp3 files + updates manifest with audio_path and
actual durations for the sync pass.
"""

import json
import os
import re
import sys
import requests
from pathlib import Path

# ─── Config (LOCKED — from PRODUCTION_BIBLE.md) ──────────────────────────────
VOICE_ID = "5jVVMAv2LzffTcLGarKh"  # Allison
MODEL_ID = "eleven_turbo_v2_5"
SETTINGS = {
    "stability": 0.50,
    "similarity_boost": 0.75,
    "style": 0.25,
}
SPEED = 0.90
TARGET_DBFS = -26.0
API_KEY = os.environ.get(
    "ELEVENLABS_API_KEY",
    "sk_4abfbb388b66e23c7df0424e9228691ae139ab56a449e2a7"
)

# Pronunciation fixes
PRONUNCIATION_FIXES = [
    (r'\bsine\b', 'sign'),
    (r'\bcosine\b', 'cosign'),
    (r'\bln\b', 'L N'),
    (r'\bd/dx\b', 'dee dee ex'),
]


def fix_pronunciation(text: str) -> str:
    for pattern, replacement in PRONUNCIATION_FIXES:
        text = re.sub(pattern, replacement, text, flags=re.IGNORECASE)
    return text


def generate_one(text: str, output_path: str) -> float:
    """Generate TTS for one text string. Returns duration in seconds."""
    import subprocess

    text = fix_pronunciation(text)

    resp = requests.post(
        f"https://api.elevenlabs.io/v1/text-to-speech/{VOICE_ID}",
        json={
            "text": text,
            "model_id": MODEL_ID,
            "voice_settings": {**SETTINGS, "speed": SPEED},
        },
        headers={
            "xi-api-key": API_KEY,
            "Content-Type": "application/json",
        },
        timeout=30,
    )
    resp.raise_for_status()

    raw_path = output_path + ".raw.mp3"
    with open(raw_path, "wb") as f:
        f.write(resp.content)

    # Normalize to -26 dBFS using ffmpeg (avoids pydub/audioop issues)
    # Two-pass: measure loudness, then normalize
    result = subprocess.run(
        ["ffmpeg", "-y", "-i", raw_path,
         "-af", f"loudnorm=I={TARGET_DBFS}:TP=-1.5:LRA=11:print_format=summary",
         "-f", "null", "-"],
        capture_output=True, text=True, timeout=15
    )

    # Single-pass normalize (close enough for TTS)
    subprocess.run(
        ["ffmpeg", "-y", "-i", raw_path,
         "-af", f"loudnorm=I={TARGET_DBFS}:TP=-1.5:LRA=11",
         "-b:a", "192k", output_path],
        capture_output=True, text=True, timeout=15
    )
    os.remove(raw_path)

    # Get duration
    dur_result = subprocess.run(
        ["ffprobe", "-v", "error", "-show_entries", "format=duration",
         "-of", "csv=p=0", output_path],
        capture_output=True, text=True, timeout=10
    )
    duration = float(dur_result.stdout.strip()) if dur_result.returncode == 0 else 3.0
    return duration


def generate_for_manifest(manifest: list[dict], output_dir: str) -> list[dict]:
    """
    Generate TTS for every step in a video manifest.
    
    For algebra_solve steps, generates audio for each sub-step individually
    so they sync with the whiteboard animations.
    
    Returns updated manifest with audio_path and tts_duration set.
    """
    os.makedirs(output_dir, exist_ok=True)
    updated = []

    for i, step in enumerate(manifest):
        step = dict(step)
        stype = step.get("type", "math")

        if stype == "algebra_solve":
            # Generate per-substep audio for precise sync
            sub_steps = step.get("algebra_solve", {}).get("steps", [])
            for si, sub in enumerate(sub_steps):
                narration = sub.get("narration", "")
                if not narration:
                    continue
                audio_file = os.path.join(output_dir, f"step_{i:02d}_sub_{si:02d}.mp3")
                print(f"  🔊 [{i+1}.{si+1}] {narration[:60]}...")
                dur = generate_one(narration, audio_file)
                sub["audio_path"] = os.path.abspath(audio_file)
                sub["tts_duration"] = dur
                sub["duration"] = max(sub.get("duration", 0), dur + 0.3)
                print(f"       → {dur:.2f}s")

            # Update total duration
            step["duration"] = sum(s.get("duration", 3.0) for s in sub_steps)
            # No top-level audio for algebra_solve (sub-steps have their own)
            step["audio_path"] = ""

        else:
            narration = step.get("narration", "")
            if narration:
                audio_file = os.path.join(output_dir, f"step_{i:02d}_{stype}.mp3")
                print(f"  🔊 [{i+1}] {narration[:60]}...")
                dur = generate_one(narration, audio_file)
                step["audio_path"] = os.path.abspath(audio_file)
                step["tts_duration"] = dur
                step["duration"] = max(step.get("duration", 0), dur + 0.5)
                print(f"       → {dur:.2f}s")

        updated.append(step)

    # Save updated manifest
    manifest_path = os.path.join(output_dir, "manifest_with_audio.json")
    with open(manifest_path, "w") as f:
        json.dump(updated, f, indent=2)
    print(f"\n  ✓ Manifest with audio: {manifest_path}")

    return updated


if __name__ == "__main__":
    if len(sys.argv) < 3:
        print("Usage: python3 generate_tts.py <manifest.json> <output_dir>")
        sys.exit(1)

    with open(sys.argv[1]) as f:
        manifest = json.load(f)
    
    output_dir = sys.argv[2]
    generate_for_manifest(manifest, output_dir)
