#!/usr/bin/env python3
"""Generate promo TTS takes with max personality settings + multiple post-processing versions."""

import os
import subprocess
import requests
import json
from pathlib import Path

# Config
API_KEY = os.getenv("ELEVENLABS_API_KEY", "sk_4abfbb388b66e23c7df0424e9228691ae139ab56a449e2a7")
VOICE_ID = "xlXKskObS9esCiw6VZNZ"  # Clayton's clone
OUTPUT_DIR = Path(os.path.expanduser("~/Desktop/Orbital/orbital_factory/output/tts/promo_takes"))
OUTPUT_DIR.mkdir(parents=True, exist_ok=True)

# Script with expression-optimized punctuation
SCRIPT = """Hey — if you're watching this, you probably know me from MAINFRAME. And you know I love teaching math.

I've been building something new. A channel that takes the HARDEST concepts in math — and makes them click. Short breakdowns that show you the WHY... in under two minutes. And deep dives into stuff like Dedekind cuts and abstract group theory — for when you want the full picture.

It's called Orbital. Calculus, precalculus, algebra, statistics, linear algebra — and eventually? Real analysis, abstract algebra, and number theory.

If you've ever stared at a formula and thought... "but WHY does that work?" — that's EXACTLY what this channel is for.

It's called Orbital. Link is in the description."""

# ElevenLabs settings — max personality
SETTINGS = {
    "stability": 0.25,
    "similarity_boost": 0.63,
    "style": 0.80,
    "use_speaker_boost": True,
}
SPEED = 0.92
MODEL = "eleven_multilingual_v2"

# Post-processing filters
# EQ only (warmth + nasal cut, NO compression, NO loudnorm)
LIGHT_FILTER = (
    "highpass=f=80,lowpass=f=10500,"
    "equalizer=f=90:t=q:w=0.7:g=2,"
    "equalizer=f=180:t=q:w=1:g=3,"
    "equalizer=f=350:t=q:w=1:g=2,"
    "equalizer=f=550:t=q:w=2.5:g=-6,"
    "equalizer=f=800:t=q:w=2.5:g=-9,"
    "equalizer=f=1050:t=q:w=2.5:g=-8,"
    "equalizer=f=1300:t=q:w=2:g=-5,"
    "equalizer=f=1600:t=q:w=1.5:g=-2,"
    "equalizer=f=1900:t=q:w=1:g=2.5,"
    "equalizer=f=3200:t=q:w=1:g=0.5,"
    "equalizer=f=5000:t=q:w=2:g=-3.5,"
    "highshelf=f=6000:g=-3"
)

# Full processing (original clayton_final.json)
FULL_FILTER = (
    f"{LIGHT_FILTER},"
    "acompressor=threshold=-23dB:ratio=2:attack=18:release=200,"
    "aecho=0.8:0.72:20:0.09,"
    "loudnorm=I=-16:TP=-1:LRA=11"
)

# Light v2 — EQ + gentle reverb + WIDE loudnorm (preserves dynamics)
LIGHT_V2_FILTER = (
    f"{LIGHT_FILTER},"
    "aecho=0.8:0.72:20:0.09,"
    "loudnorm=I=-16:TP=-1:LRA=20"
)


def generate_tts(text: str, take_num: int) -> Path:
    """Generate TTS via ElevenLabs API."""
    url = f"https://api.elevenlabs.io/v1/text-to-speech/{VOICE_ID}"
    headers = {
        "xi-api-key": API_KEY,
        "Content-Type": "application/json",
    }
    payload = {
        "text": text,
        "model_id": MODEL,
        "voice_settings": SETTINGS,
    }
    # Speed is set via query param for some models, or in voice_settings
    # For multilingual_v2, speed goes in voice_settings
    payload["voice_settings"]["speed"] = SPEED

    print(f"  Generating take {take_num}...")
    resp = requests.post(url, headers=headers, json=payload, timeout=120)
    resp.raise_for_status()

    raw_path = OUTPUT_DIR / f"take{take_num}_raw.mp3"
    raw_path.write_bytes(resp.content)
    print(f"  ✅ Raw: {raw_path} ({len(resp.content) / 1024:.0f}KB)")
    return raw_path


def post_process(raw_path: Path, take_num: int, label: str, af: str) -> Path:
    """Apply ffmpeg audio filter."""
    out_path = OUTPUT_DIR / f"take{take_num}_{label}.mp3"
    cmd = [
        "ffmpeg", "-y", "-i", str(raw_path),
        "-af", af,
        "-ar", "48000", "-ab", "192k",
        str(out_path)
    ]
    subprocess.run(cmd, capture_output=True, check=True)
    print(f"  ✅ {label}: {out_path}")
    return out_path


def main():
    print("=" * 60)
    print("PROMO TTS — Max Personality Takes")
    print(f"Model: {MODEL}")
    print(f"Settings: stability={SETTINGS['stability']}, similarity={SETTINGS['similarity_boost']}, "
          f"style={SETTINGS['style']}, speed={SPEED}, speaker_boost={SETTINGS['use_speaker_boost']}")
    print("=" * 60)

    # Generate 3 takes (non-deterministic, each will be different)
    for take in range(1, 4):
        print(f"\n--- Take {take} ---")
        raw = generate_tts(SCRIPT, take)

        # Three processing versions
        # 1. Raw — no processing
        print(f"  ✅ raw: {raw}")

        # 2. Light — EQ only, no compression
        post_process(raw, take, "light", LIGHT_FILTER)

        # 3. Light v2 — EQ + reverb + wide loudnorm (dynamics preserved)
        post_process(raw, take, "light_v2", LIGHT_V2_FILTER)

        # 4. Full — original clayton_final.json processing
        post_process(raw, take, "full", FULL_FILTER)

    print(f"\n✅ Done! All files in: {OUTPUT_DIR}")
    print("\nListen to raw vs light vs full to hear if compression is killing expression.")
    print("Settings saved for reproduction.")

    # Save settings for reference
    settings_log = {
        "model": MODEL,
        "voice_id": VOICE_ID,
        "voice_settings": {**SETTINGS, "speed": SPEED},
        "script": SCRIPT,
        "processing_versions": {
            "raw": "No processing",
            "light": "EQ only (warmth + nasal cut), no compression, no loudnorm",
            "light_v2": "EQ + reverb + wide loudnorm (LRA=20, preserves dynamics)",
            "full": "Original clayton_final.json (compressor + loudnorm LRA=11)",
        }
    }
    (OUTPUT_DIR / "settings.json").write_text(json.dumps(settings_log, indent=2))


if __name__ == "__main__":
    main()
