"""
Generate scene-based TTS for "Why You Can't Divide by Zero" short.
Voice: Allison (5jVVMAv2LzffTcLGarKh)
Model: eleven_turbo_v2_5
"""
import os, json, requests, subprocess
from pathlib import Path

API_KEY = "sk_4abfbb388b66e23c7df0424e9228691ae139ab56a449e2a7"
VOICE_ID = "5jVVMAv2LzffTcLGarKh"
MODEL = "eleven_turbo_v2_5"
OUT_DIR = Path("output/tts/divzero_scenes")
OUT_DIR.mkdir(parents=True, exist_ok=True)

SCENES = [
    {
        "id": "hook",
        "text": "Your calculator says error. Your teacher says undefined. They're both lying to you."
    },
    {
        "id": "what_is_division",
        "text": "Division is just asking one question. How many times does this fit into that? Eight divided by two. Two fits in four times. Simple. Now ask that same question with zero. How many times does zero fit into eight?"
    },
    {
        "id": "contradiction_setup",
        "text": "Okay. Suppose dividing by zero did give you an answer. Any number. Doesn't matter which one."
    },
    {
        "id": "contradiction_payoff",
        "text": "If that answer times zero gives you back one, but anything times zero is always zero, then zero would have to equal one. That's not an error. That's math destroying itself."
    },
    {
        "id": "graph_intro",
        "text": "And you can see this breaking point. Divide one by smaller and smaller numbers. One tenth. One hundredth. One thousandth. And watch what happens."
    },
    {
        "id": "graph_explosion",
        "text": "From the right, the answer rockets toward infinity. From the left, it plunges toward negative infinity. Two directions at once. No single answer exists."
    },
    {
        "id": "punchline",
        "text": "Division by zero doesn't give you infinity. It doesn't give you nothing. It produces a logical impossibility. And that's exactly why mathematicians call it undefined."
    },
    {
        "id": "resolution",
        "text": "Not forbidden. Not broken. Just impossible. And now you know why."
    },
    {
        "id": "cta",
        "text": "If this clicked, follow Orbital."
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
        dur = subprocess.run(
            ["ffprobe", "-v", "error", "-show_entries", "format=duration",
             "-of", "csv=p=0", str(out_path)],
            capture_output=True, text=True
        ).stdout.strip()
        entry = {
            "id": scene["id"],
            "text": scene["text"],
            "file": f"{scene['id']}.mp3",
            "duration": float(dur) if dur else 0
        }
        manifest["scenes"].append(entry)
        print(f"  ✓ {scene['id']}: {dur}s")
    else:
        print(f"  ✗ {scene['id']}: {resp.status_code} {resp.text[:200]}")

manifest_path = OUT_DIR / "manifest.json"
manifest_path.write_text(json.dumps(manifest, indent=2))
print(f"\nManifest saved: {manifest_path}")
print(f"Total scenes: {len(manifest['scenes'])}")
total_dur = sum(s['duration'] for s in manifest['scenes'])
print(f"Total audio duration: {total_dur:.1f}s")
