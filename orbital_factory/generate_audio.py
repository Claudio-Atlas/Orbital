"""
Orbital VideoFactory - Audio Generation
Supports: ElevenLabs, OpenAI TTS
"""

import os
import json
from pathlib import Path

# === PROVIDER CONFIG ===
# Set TTS_PROVIDER to "openai" or "elevenlabs" (default: elevenlabs)
TTS_PROVIDER = os.environ.get("TTS_PROVIDER", "elevenlabs").lower()

ELEVEN_API_KEY = os.environ.get("ELEVEN_API_KEY")
OPENAI_API_KEY = os.environ.get("OPENAI_API_KEY")

print(f"🔊 TTS Provider: {TTS_PROVIDER.upper()}")


def generate_step_audio_elevenlabs(text: str, output_path: str, voice_id: str = "EXAVITQu4vr4xnSDxMaL") -> float:
    """Generate audio using ElevenLabs."""
    from elevenlabs import ElevenLabs
    
    if not ELEVEN_API_KEY:
        raise ValueError("ELEVEN_API_KEY environment variable not set")
    
    client = ElevenLabs(api_key=ELEVEN_API_KEY)
    
    audio = client.text_to_speech.convert(
        text=text,
        voice_id=voice_id,
        model_id="eleven_turbo_v2_5",
        output_format="mp3_44100_128"
    )
    
    with open(output_path, "wb") as f:
        for chunk in audio:
            f.write(chunk)
    
    from pydub import AudioSegment
    audio_segment = AudioSegment.from_mp3(output_path)
    return len(audio_segment) / 1000.0


def generate_step_audio_openai(text: str, output_path: str, voice: str = "nova") -> float:
    """Generate audio using OpenAI TTS."""
    from openai import OpenAI
    
    if not OPENAI_API_KEY:
        raise ValueError("OPENAI_API_KEY environment variable not set")
    
    client = OpenAI(api_key=OPENAI_API_KEY)
    
    # OpenAI TTS voices: alloy, echo, fable, onyx, nova, shimmer
    # nova = warm female, good for educational content
    response = client.audio.speech.create(
        model="tts-1",  # or "tts-1-hd" for higher quality
        voice=voice,
        input=text,
        response_format="mp3"
    )
    
    # Save the audio
    response.stream_to_file(output_path)
    
    from pydub import AudioSegment
    audio_segment = AudioSegment.from_mp3(output_path)
    return len(audio_segment) / 1000.0


def generate_step_audio(text: str, output_path: str, voice: str = None) -> float:
    """
    Generate audio for a single step using configured provider.
    
    Args:
        text: Narration text
        output_path: Where to save the audio file
        voice: Voice name/ID (provider-specific)
    
    Returns:
        Duration of audio in seconds
    """
    if TTS_PROVIDER == "openai":
        voice = voice or "nova"
        return generate_step_audio_openai(text, output_path, voice)
    else:
        voice = voice or "EXAVITQu4vr4xnSDxMaL"  # Sarah
        return generate_step_audio_elevenlabs(text, output_path, voice)


def generate_all_audio(script_path: str, output_dir: str, voice: str = None) -> list:
    """
    Generate audio for all steps in a script.
    
    Args:
        script_path: Path to JSON script
        output_dir: Directory to save audio files
        voice: Voice name/ID (optional)
    
    Returns:
        List of dicts with step info and audio duration
    """
    with open(script_path) as f:
        script = json.load(f)
    
    os.makedirs(output_dir, exist_ok=True)
    
    results = []
    
    for i, step in enumerate(script.get("steps", [])):
        narration = step.get("narration", "")
        if not narration:
            continue
        
        output_path = os.path.join(output_dir, f"step_{i:02d}.mp3")
        
        print(f"Generating audio for step {i}: {narration[:50]}...")
        duration = generate_step_audio(narration, output_path, voice)
        
        results.append({
            "step": i,
            "narration": narration,
            "latex": step.get("latex", ""),
            "audio_path": output_path,
            "duration": duration
        })
        
        print(f"  → {duration:.2f}s saved to {output_path}")
    
    # Save manifest
    manifest_path = os.path.join(output_dir, "manifest.json")
    with open(manifest_path, "w") as f:
        json.dump(results, f, indent=2)
    
    print(f"\nGenerated {len(results)} audio files")
    print(f"Manifest saved to {manifest_path}")
    
    return results


# Voice options
VOICES_ELEVENLABS = {
    "sarah": "EXAVITQu4vr4xnSDxMaL",
    "adam": "pNInz6obpgDQGcFmaJgB",
    "rachel": "21m00Tcm4TlvDq8ikWAM",
    "josh": "TxGEqnHWrfWFTfGW9XjX",
}

VOICES_OPENAI = {
    "alloy": "alloy",     # Neutral
    "echo": "echo",       # Male
    "fable": "fable",     # British male
    "onyx": "onyx",       # Deep male
    "nova": "nova",       # Warm female ← recommended
    "shimmer": "shimmer", # Soft female
}


if __name__ == "__main__":
    import sys
    
    if len(sys.argv) < 2:
        print("Usage: python generate_audio.py <script.json> [output_dir]")
        print(f"\nCurrent provider: {TTS_PROVIDER.upper()}")
        print("\nTo switch providers:")
        print("  export TTS_PROVIDER=openai")
        print("  export TTS_PROVIDER=elevenlabs")
        sys.exit(1)
    
    script_path = sys.argv[1]
    output_dir = sys.argv[2] if len(sys.argv) > 2 else "audio/output"
    
    generate_all_audio(script_path, output_dir)
