"""
Orbital Engine — TTS Generator
Allison voice via ElevenLabs with per-profile settings.
"""
import json
import os
import subprocess
from pathlib import Path

from config import (
    ELEVENLABS_MODEL, ALLISON_VOICE_ID, TTS_OUTPUT_FORMAT,
    TTS_NORMALIZE_DB, TTS_PROFILES,
)


ELEVENLABS_API_KEY = os.environ.get("ELEVENLABS_API_KEY",
    "sk_4abfbb388b66e23c7df0424e9228691ae139ab56a449e2a7")


def generate_tts(text: str, output_path: str, profile: str = "lesson") -> dict:
    """
    Generate TTS audio for a single narration step.

    Args:
        text: Narration text
        output_path: Where to save the mp3
        profile: TTS profile name (short, lesson, problem, longform)

    Returns dict with {duration_ms, path, chars}
    """
    import requests

    prof = TTS_PROFILES.get(profile, TTS_PROFILES["lesson"])

    url = f"https://api.elevenlabs.io/v1/text-to-speech/{ALLISON_VOICE_ID}"
    headers = {
        "xi-api-key": ELEVENLABS_API_KEY,
        "Content-Type": "application/json",
    }
    payload = {
        "text": text,
        "model_id": ELEVENLABS_MODEL,
        "output_format": TTS_OUTPUT_FORMAT,
        "voice_settings": {
            "stability": prof["stability"],
            "similarity_boost": prof["similarity_boost"],
            "style": prof["style"],
            "speed": prof["speed"],
        },
    }

    resp = requests.post(url, json=payload, headers=headers, timeout=60)
    resp.raise_for_status()

    Path(output_path).parent.mkdir(parents=True, exist_ok=True)
    with open(output_path, "wb") as f:
        f.write(resp.content)

    # Normalize to target dBFS
    normalize_audio(output_path)

    # Get duration
    duration_ms = get_audio_duration_ms(output_path)

    return {
        "duration_ms": duration_ms,
        "path": output_path,
        "chars": len(text),
    }


def normalize_audio(path: str, target_db: float = None):
    """Normalize audio to target dBFS using ffmpeg."""
    if target_db is None:
        target_db = TTS_NORMALIZE_DB

    tmp = path + ".norm.mp3"
    try:
        # Measure current loudness
        cmd = [
            "ffmpeg", "-y", "-i", path,
            "-af", f"loudnorm=I={target_db}:TP=-1.5:LRA=11:print_format=json",
            "-f", "null", "-"
        ]
        result = subprocess.run(cmd, capture_output=True, text=True)

        # Apply normalization
        cmd = [
            "ffmpeg", "-y", "-i", path,
            "-af", f"loudnorm=I={target_db}:TP=-1.5:LRA=11",
            "-ar", "44100", "-ab", "128k",
            tmp
        ]
        subprocess.run(cmd, capture_output=True, text=True, check=True)

        os.replace(tmp, path)
    except Exception:
        if os.path.exists(tmp):
            os.remove(tmp)


def get_audio_duration_ms(path: str) -> int:
    """Get audio duration in milliseconds."""
    try:
        result = subprocess.run([
            "ffprobe", "-v", "error",
            "-show_entries", "format=duration",
            "-of", "csv=p=0", path
        ], capture_output=True, text=True)
        return int(float(result.stdout.strip()) * 1000)
    except Exception:
        return 0


def generate_tts_for_manifest(manifest_path: str, profile: str = None) -> dict:
    """
    Generate TTS for all steps in a manifest.

    Returns updated manifest with audio_path and duration_ms per step.
    """
    with open(manifest_path) as f:
        manifest = json.load(f)

    if profile is None:
        video_type = manifest.get("video_type", "lesson")
        profile = video_type

    audio_dir = Path(manifest_path).parent / "audio" / Path(manifest_path).stem
    audio_dir.mkdir(parents=True, exist_ok=True)

    total_chars = 0
    total_dur = 0

    for step in manifest["steps"]:
        narration = step.get("narration", "")
        if not narration:
            continue

        step_id = step["id"]
        audio_file = str(audio_dir / f"{step_id}.mp3")

        # Skip if audio already exists
        if Path(audio_file).exists() and Path(audio_file).stat().st_size > 1000:
            step["audio_path"] = audio_file
            step["duration_ms"] = get_audio_duration_ms(audio_file)
            total_dur += step["duration_ms"]
            continue

        print(f"  🎙️  {step_id}: '{narration[:60]}...' ({len(narration)} chars)")

        result = generate_tts(narration, audio_file, profile=profile)
        step["audio_path"] = result["path"]
        step["duration_ms"] = result["duration_ms"]
        total_chars += result["chars"]
        total_dur += result["duration_ms"]

        print(f"    ✅ {result['duration_ms']}ms ({result['duration_ms']/1000:.1f}s)")

    manifest["total_duration_ms"] = total_dur
    manifest["tts_profile"] = profile

    # Save updated manifest
    with open(manifest_path, "w") as f:
        json.dump(manifest, f, indent=2)

    cost = total_chars / 1000 * 0.10  # rough ElevenLabs cost estimate
    print(f"\n  📊 Total: {total_chars} chars, {total_dur/1000:.1f}s audio")
    print(f"  💰 Cost: ${cost:.2f}")

    return manifest
