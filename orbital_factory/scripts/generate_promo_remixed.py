#!/usr/bin/env python3
"""Generate promo TTS with remixed voice — clean output, no post-processing."""

import os
import requests
import json
from pathlib import Path

API_KEY = "sk_4abfbb388b66e23c7df0424e9228691ae139ab56a449e2a7"
VOICE_ID = "pGonXF8d9dgN6rrS2GWU"  # Clayton remixed voice
OUTPUT_DIR = Path(os.path.expanduser("~/Desktop/Orbital/orbital_factory/output/tts/promo_remixed"))
OUTPUT_DIR.mkdir(parents=True, exist_ok=True)

SCRIPT = """[Energetic, happy, speaking to old friends with genuine excitement]

Hey! If you're watching this, you probably know me from MAINFRAME.

I've been building something new. A channel that takes the HARDEST concepts in math... and makes them CLICK! Short breakdowns that show you the WHY in under two minutes. And deep dives into stuff like Dedekind cuts and abstract group theory, for when you want the full picture.

It's called Orbital. Everything from algebra to calculus, all the way up to real analysis.

If you've ever stared at a formula and thought... "but WHY does that work?" That's EXACTLY what this channel is for!

It's called Orbital. Link is in the description."""

SETTINGS = {
    "stability": 0.25,
    "similarity_boost": 0.63,
    "style": 0.80,
    "use_speaker_boost": True,
    "speed": 1.00,
}
MODEL = "eleven_multilingual_v2"

def generate(take_num):
    url = f"https://api.elevenlabs.io/v1/text-to-speech/{VOICE_ID}"
    headers = {"xi-api-key": API_KEY, "Content-Type": "application/json"}
    payload = {
        "text": SCRIPT,
        "model_id": MODEL,
        "voice_settings": SETTINGS,
    }
    print(f"  Generating take {take_num}...")
    resp = requests.post(url, headers=headers, json=payload, timeout=120)
    resp.raise_for_status()
    out = OUTPUT_DIR / f"remixed_take{take_num}.mp3"
    out.write_bytes(resp.content)
    print(f"  ✅ {out} ({len(resp.content)/1024:.0f}KB)")
    return out

def main():
    print("=" * 50)
    print("PROMO — Remixed Voice, No Post-Processing")
    print(f"Voice ID: {VOICE_ID}")
    print(f"Model: {MODEL}")
    print(f"Settings: {json.dumps(SETTINGS, indent=2)}")
    print("=" * 50)

    for i in range(1, 4):
        generate(i)

    # Save settings
    (OUTPUT_DIR / "settings.json").write_text(json.dumps({
        "voice_id": VOICE_ID,
        "model": MODEL,
        "settings": SETTINGS,
        "script": SCRIPT,
        "post_processing": "NONE — raw ElevenLabs output",
    }, indent=2))

    print(f"\n✅ 3 takes in: {OUTPUT_DIR}")
    print("No post-processing applied — pure remixed voice output.")

if __name__ == "__main__":
    main()
