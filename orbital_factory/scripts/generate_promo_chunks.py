#!/usr/bin/env python3
"""Promo TTS — sentence-by-sentence with previous_text context. 3 takes per chunk."""

import requests
import subprocess
from pathlib import Path

API_KEY = "sk_4abfbb388b66e23c7df0424e9228691ae139ab56a449e2a7"
VOICE_ID = "pGonXF8d9dgN6rrS2GWU"
OUTPUT_DIR = Path.home() / "Desktop/Orbital/orbital_factory/output/tts/promo_chunks"
OUTPUT_DIR.mkdir(parents=True, exist_ok=True)

CHUNKS = [
    "Hey! If you're watching this, you probably know me from MAINFRAME.",
    "I've been building something new. A channel that takes the HARDEST concepts in math, and makes them CLICK!",
    "Short breakdowns that show you the WHY in under two minutes. And deep dives into stuff like Dedekind cuts and group theory, for when you want the full picture.",
    "It's called Orbital. Everything from algebra to calculus, all the way up to real analysis.",
    "Ever stare at a formula and just think, WHY? That's what we do.",
    "It's called Orbital. Link is in the description.",
]

SETTINGS = {"stability": 0.40, "similarity_boost": 0.63, "style": 0.80, "use_speaker_boost": True, "speed": 1.00}
MODEL = "eleven_multilingual_v2"
TAKES = 3

for ci, chunk in enumerate(CHUNKS, 1):
    print(f"\n{'='*50}")
    print(f"CHUNK {ci}: {chunk[:60]}...")
    print(f"{'='*50}")
    
    # Build previous_text from all prior chunks
    prev = " ".join(CHUNKS[:ci-1]) if ci > 1 else None
    # Build next_text from next chunk
    nxt = CHUNKS[ci] if ci < len(CHUNKS) else None
    
    for ti in range(1, TAKES + 1):
        print(f"  Take {ti}...", end=" ", flush=True)
        payload = {
            "text": chunk,
            "model_id": MODEL,
            "voice_settings": SETTINGS,
        }
        if prev:
            payload["previous_text"] = prev
        if nxt:
            payload["next_text"] = nxt
            
        r = requests.post(
            f"https://api.elevenlabs.io/v1/text-to-speech/{VOICE_ID}",
            headers={"xi-api-key": API_KEY, "Content-Type": "application/json"},
            json=payload, timeout=120
        )
        r.raise_for_status()
        out = OUTPUT_DIR / f"chunk{ci}_take{ti}.mp3"
        out.write_bytes(r.content)
        dur = float(subprocess.run(
            ["ffprobe", "-v", "quiet", "-print_format", "json", "-show_format", str(out)],
            capture_output=True, text=True
        ).stdout.split('"duration": "')[1].split('"')[0])
        print(f"✅ {len(r.content)/1024:.0f}KB ({dur:.1f}s)")

print(f"\n✅ All chunks in: {OUTPUT_DIR}")
print(f"\nTo assemble, pick best take of each chunk and run:")
print(f"  ffmpeg -i chunk1_takeX.mp3 -i chunk2_takeX.mp3 ... -filter_complex concat=n=6:v=0:a=1 final.mp3")
