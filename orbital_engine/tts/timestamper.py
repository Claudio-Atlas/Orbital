"""
Orbital Engine — TTS Timestamper
Runs local Whisper on generated TTS audio to extract word-level timestamps.
This is Stage 3.5: bridges TTS generation and scene rendering.

No API key needed. Runs entirely on-device.
"""
import json
import whisper
from pathlib import Path


# Load model once (cached after first call)
_model = None

def _get_model(size="base"):
    global _model
    if _model is None:
        print(f"  📡 Loading Whisper model ({size})...")
        _model = whisper.load_model(size)
    return _model


def timestamp_audio(audio_path: str, model_size: str = "base") -> list:
    """
    Get word-level timestamps from an audio file.
    
    Returns list of {"word": str, "start": float, "end": float}
    """
    model = _get_model(model_size)
    result = model.transcribe(audio_path, word_timestamps=True)
    
    words = []
    for segment in result["segments"]:
        for w in segment.get("words", []):
            words.append({
                "word": w["word"].strip(),
                "start": round(w["start"], 2),
                "end": round(w["end"], 2),
            })
    return words


def find_trigger(words: list, trigger_words: list, after: float = 0.0) -> float:
    """
    Find the timestamp when a trigger phrase starts.
    
    Args:
        words: Word timestamps from timestamp_audio()
        trigger_words: List of words to match in sequence, e.g. ["put", "in", "three"]
        after: Only match occurrences after this timestamp
    
    Returns timestamp (float) or -1 if not found.
    """
    trigger_lower = [w.lower().strip(".,!?") for w in trigger_words]
    n = len(trigger_lower)
    
    for i in range(len(words) - n + 1):
        if words[i]["start"] < after:
            continue
        match = True
        for j in range(n):
            if words[i+j]["word"].lower().strip(".,!?") != trigger_lower[j]:
                match = False
                break
        if match:
            return words[i]["start"]
    return -1


def find_word(words: list, target: str, after: float = 0.0, occurrence: int = 1) -> float:
    """
    Find the Nth occurrence of a single word after a given timestamp.
    
    Returns timestamp (float) or -1 if not found.
    """
    target_lower = target.lower().strip(".,!?")
    count = 0
    for w in words:
        if w["start"] < after:
            continue
        if w["word"].lower().strip(".,!?") == target_lower:
            count += 1
            if count == occurrence:
                return w["start"]
    return -1


def timestamp_manifest(manifest_path: str, model_size: str = "base") -> dict:
    """
    Run Whisper on all audio clips in a manifest and add word timestamps.
    
    Adds 'word_timestamps' field to each step.
    """
    with open(manifest_path) as f:
        manifest = json.load(f)
    
    model = _get_model(model_size)
    
    for step in manifest["steps"]:
        audio_path = step.get("audio_path", "")
        if not audio_path or not Path(audio_path).exists():
            continue
        
        print(f"  🔍 Timestamping {step['id']}...")
        words = timestamp_audio(audio_path, model_size)
        step["word_timestamps"] = words
        
        # Print summary
        if words:
            dur = words[-1]["end"]
            print(f"     {len(words)} words, {dur:.1f}s")
    
    # Save updated manifest
    with open(manifest_path, "w") as f:
        json.dump(manifest, f, indent=2)
    
    print(f"\n  ✅ Timestamps added to {manifest_path}")
    return manifest


if __name__ == "__main__":
    import sys
    if len(sys.argv) < 2:
        print("Usage: python timestamper.py <manifest.json>")
        sys.exit(1)
    timestamp_manifest(sys.argv[1])
