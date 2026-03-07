"""
Generate scene-based TTS for "Why eˣ Is Its Own Derivative" short.
Voice: Allison (5jVVMAv2LzffTcLGarKh)
Model: eleven_turbo_v2_5
Settings: stability=0.50, similarity_boost=0.75, style=0.25, speed=0.90
"""
import os
import json
import requests
from pathlib import Path

API_KEY = os.getenv("ELEVENLABS_API_KEY", "sk_4abfbb388b66e23c7df0424e9228691ae139ab56a449e2a7")
VOICE_ID = "5jVVMAv2LzffTcLGarKh"
MODEL = "eleven_turbo_v2_5"
OUT_DIR = Path("output/tts/ex_derivative_scenes")
OUT_DIR.mkdir(parents=True, exist_ok=True)

SCENES = [
    {
        "id": "hook",
        "text": "This function's derivative is itself. Here's why that's not magic."
    },
    {
        "id": "derivative_reminder",
        "text": "Quick reminder. The derivative at a point is just the slope of the tangent line. It tells you how steep the curve is, right there."
    },
    {
        "id": "the_claim",
        "text": "Now here's what makes e to the x special. At every single point on this curve, the slope equals the height."
    },
    {
        "id": "proof_watch",
        "text": "Watch. As we move along the curve, the height changes, and the slope changes with it. They're always the same number."
    },
    {
        "id": "contrast_2x",
        "text": "This doesn't work for other bases. On 2 to the x, the slope is always less than the height."
    },
    {
        "id": "contrast_3x",
        "text": "On 3 to the x, the slope overshoots. Always more than the height."
    },
    {
        "id": "the_answer",
        "text": "Only one base makes them match. That base is e, about 2.718. The slope at every point IS the value at that point."
    },
    {
        "id": "punchline",
        "text": "So when you take the derivative of e to the x, which just asks what's the slope, the answer is e to the x. The function doesn't change. Because the slope was always the height."
    },
]

url = f"https://api.elevenlabs.io/v1/text-to-speech/{VOICE_ID}"
headers = {"xi-api-key": API_KEY, "Content-Type": "application/json"}

manifest = {"scenes": [], "voice_id": VOICE_ID, "model": MODEL}

for scene in SCENES:
    print(f"Generating: {scene['id']}...")
    payload = {
        "text": scene["text"],
        "model_id": MODEL,
        "voice_settings": {
            "stability": 0.50,
            "similarity_boost": 0.75,
            "style": 0.25,
            "speed": 0.90
        }
    }
    resp = requests.post(url, json=payload, headers=headers)
    if resp.status_code == 200:
        out_path = OUT_DIR / f"{scene['id']}.mp3"
        out_path.write_bytes(resp.content)
        
        # Get duration via ffprobe
        import subprocess
        dur = subprocess.run(
            ["ffprobe", "-v", "error", "-show_entries", "format=duration",
             "-of", "csv=p=0", str(out_path)],
            capture_output=True, text=True
        ).stdout.strip()
        
        entry = {
            "id": scene["id"],
            "text": scene["text"],
            "file": str(out_path),
            "duration": float(dur) if dur else 0
        }
        manifest["scenes"].append(entry)
        print(f"  ✓ {scene['id']}: {dur}s")
    else:
        print(f"  ✗ {scene['id']}: {resp.status_code} {resp.text[:200]}")

# Save manifest
manifest_path = OUT_DIR / "manifest.json"
manifest_path.write_text(json.dumps(manifest, indent=2))
print(f"\nManifest saved: {manifest_path}")
print(f"Total scenes: {len(manifest['scenes'])}")
total_dur = sum(s['duration'] for s in manifest['scenes'])
print(f"Total audio duration: {total_dur:.1f}s")
