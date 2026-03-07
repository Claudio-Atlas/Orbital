"""Meridian Press District Promo — Hale voice, sentence-by-sentence with context. 3 takes per chunk."""

import requests
import subprocess
from pathlib import Path

API_KEY = "sk_4abfbb388b66e23c7df0424e9228691ae139ab56a449e2a7"
VOICE_ID = "wWWn96OtTHu1sn8SRGEr"  # Hale (promo/cinematic)
MODEL = "eleven_turbo_v2_5"
SETTINGS = {"stability": 0.55, "similarity_boost": 0.65, "style": 0.25, "use_speaker_boost": True, "speed": 0.8}
TAKES = 3

OUTPUT_DIR = Path.home() / "Desktop/Orbital/orbital_factory/output/tts/meridian_promo"
OUTPUT_DIR.mkdir(parents=True, exist_ok=True)

CHUNKS = [
    "Every student learns at a different pace. The problem is, most math programs don't.",
    "One textbook. One speed. And if you miss a step, good luck catching up.",
    "We built Meridian to fix that.",
    "Complete math programs with digital textbooks, video walkthroughs, thousands of practice problems, and a personal AI tutor that adapts to EVERY student.",
    "When a student gets stuck, the AI tutor meets them right where they are. Step by step. No judgment. No falling through the cracks.",
    "Teachers get real-time dashboards showing exactly where each student needs help, not just a grade at the end of the unit.",
    "Pre-Algebra through Calculus. Every course built on one platform.",
    "Not a textbook with a website bolted on. A complete system built by educators who've been in the classroom.",
    "Because every student deserves a program that actually meets them where they are.",
    "Meridian Press. Mathematics for every student.",
]

for ci, chunk in enumerate(CHUNKS, 1):
    print(f"\n{'='*50}")
    print(f"CHUNK {ci}: {chunk[:60]}...")
    print(f"{'='*50}")
    
    prev = " ".join(CHUNKS[:ci-1]) if ci > 1 else None
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
        
        # Get duration
        dur = subprocess.run(
            ["ffprobe", "-v", "quiet", "-show_entries", "format=duration", "-of", "csv=p=0", str(out)],
            capture_output=True, text=True
        )
        print(f"OK ({float(dur.stdout.strip()):.1f}s)" if dur.stdout.strip() else "OK")

print(f"\n\nDone! {len(CHUNKS)} chunks × {TAKES} takes = {len(CHUNKS)*TAKES} files")
print(f"Output: {OUTPUT_DIR}")
