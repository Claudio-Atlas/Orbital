#!/usr/bin/env python3
"""Promo TTS v4 — revised script, stability 0.40."""

import requests
from pathlib import Path

API_KEY = "sk_4abfbb388b66e23c7df0424e9228691ae139ab56a449e2a7"
VOICE_ID = "pGonXF8d9dgN6rrS2GWU"
OUTPUT_DIR = Path.home() / "Desktop/Orbital/orbital_factory/output/tts/promo_remixed_v4"
OUTPUT_DIR.mkdir(parents=True, exist_ok=True)

SCRIPT = """Hey! If you're watching this, you probably know me from MAINFRAME.

I've been building something new. A channel that takes the HARDEST concepts in math... and makes them CLICK! Short breakdowns that show you the WHY in under two minutes. And deep dives into stuff like Dedekind cuts and group theory, for when you want the full picture.

It's called Orbital. Everything from algebra to calculus, all the way up to real analysis.

Ever stared at a formula and just thought... WHY? That's what we do.

It's called Orbital. Link is in the description."""

SETTINGS = {"stability": 0.40, "similarity_boost": 0.63, "style": 0.80, "use_speaker_boost": True, "speed": 1.00}

for i in range(1, 5):
    print(f"  Take {i}...", end=" ", flush=True)
    r = requests.post(f"https://api.elevenlabs.io/v1/text-to-speech/{VOICE_ID}",
        headers={"xi-api-key": API_KEY, "Content-Type": "application/json"},
        json={"text": SCRIPT, "model_id": "eleven_multilingual_v2", "voice_settings": SETTINGS}, timeout=120)
    r.raise_for_status()
    out = OUTPUT_DIR / f"take{i}.mp3"
    out.write_bytes(r.content)
    print(f"✅ {len(r.content)/1024:.0f}KB")

print(f"\n✅ 4 takes in: {OUTPUT_DIR}")
