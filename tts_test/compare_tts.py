"""
TTS Comparison Test for Orbital
Compare OpenAI TTS vs XTTS v2 vs Fish Speech on math narration.

Usage:
    cd ~/Desktop/Orbital/tts_test
    source venv/bin/activate
    python compare_tts.py
"""

import os
import json
import time
from pathlib import Path

# ============================================
# PREPROCESSING - Fix math pronunciation
# ============================================

import re

def preprocess_math_narration(text: str) -> str:
    """Fix common math pronunciation issues for TTS engines."""
    
    # Differential notation - must be spelled out
    differentials = ['du', 'dx', 'dy', 'dt', 'dz', 'dw', 'dr']
    for diff in differentials:
        pattern = rf'\b{diff}\b'
        replacement = f"{diff[0]} {diff[1]}"
        text = re.sub(pattern, replacement, text, flags=re.IGNORECASE)
    
    # Common math terms
    replacements = {
        r'\bln\b': 'natural log',
        r'\bwrt\b': 'with respect to',
        r'([a-z])\^2\b': r'\1 squared',
        r'([a-z])\^3\b': r'\1 cubed',
    }
    
    for pattern, replacement in replacements.items():
        text = re.sub(pattern, replacement, text, flags=re.IGNORECASE)
    
    return re.sub(r'\s+', ' ', text).strip()


# ============================================
# OpenAI TTS
# ============================================

def generate_openai(text: str, output_path: str, voice: str = "nova"):
    """Generate audio using OpenAI TTS."""
    from openai import OpenAI
    
    api_key = os.environ.get("OPENAI_API_KEY")
    if not api_key:
        print("❌ OPENAI_API_KEY not set")
        return None
    
    client = OpenAI(api_key=api_key)
    
    start = time.time()
    response = client.audio.speech.create(
        model="tts-1",
        voice=voice,
        input=text,
        response_format="mp3"
    )
    response.stream_to_file(output_path)
    elapsed = time.time() - start
    
    return elapsed


# ============================================
# XTTS v2 (Coqui)
# ============================================

_xtts_model = None

def get_xtts_model():
    """Load XTTS model (cached)."""
    global _xtts_model
    if _xtts_model is None:
        from TTS.api import TTS
        print("Loading XTTS v2 model (first time takes a while)...")
        _xtts_model = TTS("tts_models/multilingual/multi-dataset/xtts_v2")
    return _xtts_model

def generate_xtts(text: str, output_path: str, speaker_wav: str = None):
    """Generate audio using XTTS v2."""
    tts = get_xtts_model()
    
    start = time.time()
    
    # XTTS needs a reference audio for voice cloning
    # If none provided, use the default speaker
    if speaker_wav and os.path.exists(speaker_wav):
        tts.tts_to_file(
            text=text,
            file_path=output_path,
            speaker_wav=speaker_wav,
            language="en"
        )
    else:
        # Use built-in speaker
        tts.tts_to_file(
            text=text,
            file_path=output_path,
            language="en"
        )
    
    elapsed = time.time() - start
    return elapsed


# ============================================
# Fish Speech
# ============================================

def generate_fish_speech(text: str, output_path: str):
    """Generate audio using Fish Speech."""
    try:
        # Fish Speech requires running their inference server or using their API
        # For local testing, we'll use their command-line tool
        import subprocess
        
        start = time.time()
        
        # Check if fish_speech CLI is available
        result = subprocess.run(
            ["python", "-m", "fish_speech.tools.api", "--help"],
            capture_output=True,
            text=True,
            timeout=10
        )
        
        if result.returncode != 0:
            print("⚠️  Fish Speech CLI not ready. Needs model download.")
            print("   Run: python -m fish_speech.tools.download_models")
            return None
        
        # For now, note that Fish Speech typically runs as a server
        # We'll document this for later setup
        print("ℹ️  Fish Speech requires server mode or model download")
        print("   See: https://speech.fish.audio/inference/")
        return None
        
    except Exception as e:
        print(f"⚠️  Fish Speech error: {e}")
        return None


# ============================================
# Main Comparison
# ============================================

def run_comparison():
    """Run TTS comparison on test script."""
    
    print("\n" + "="*60)
    print("🎙️  TTS COMPARISON TEST - Orbital")
    print("="*60 + "\n")
    
    # Load test script
    script_path = Path(__file__).parent / "test_script.json"
    with open(script_path) as f:
        script = json.load(f)
    
    # Create output directory
    output_dir = Path(__file__).parent / "comparison_output"
    output_dir.mkdir(exist_ok=True)
    
    # Use first step for quick test
    test_step = script["steps"][2]  # Step with "du" pronunciation
    raw_text = test_step["narration"]
    processed_text = preprocess_math_narration(raw_text)
    
    print(f"📝 Test text (raw):       {raw_text}")
    print(f"📝 Test text (processed): {processed_text}")
    print()
    
    results = {}
    
    # Test 1: OpenAI TTS
    print("🔊 Testing OpenAI TTS...")
    output_openai = output_dir / "openai_nova.mp3"
    try:
        elapsed = generate_openai(processed_text, str(output_openai))
        if elapsed:
            results["openai"] = {"path": str(output_openai), "time": elapsed}
            print(f"   ✅ Generated in {elapsed:.2f}s → {output_openai}")
    except Exception as e:
        print(f"   ❌ Error: {e}")
    print()
    
    # Test 2: XTTS v2
    print("🔊 Testing XTTS v2...")
    output_xtts = output_dir / "xtts_v2.wav"
    try:
        elapsed = generate_xtts(processed_text, str(output_xtts))
        if elapsed:
            results["xtts"] = {"path": str(output_xtts), "time": elapsed}
            print(f"   ✅ Generated in {elapsed:.2f}s → {output_xtts}")
    except Exception as e:
        print(f"   ❌ Error: {e}")
    print()
    
    # Test 3: Fish Speech (informational)
    print("🔊 Testing Fish Speech...")
    output_fish = output_dir / "fish_speech.wav"
    try:
        elapsed = generate_fish_speech(processed_text, str(output_fish))
        if elapsed:
            results["fish"] = {"path": str(output_fish), "time": elapsed}
    except Exception as e:
        print(f"   ❌ Error: {e}")
    print()
    
    # Summary
    print("="*60)
    print("📊 RESULTS")
    print("="*60)
    print()
    
    for name, data in results.items():
        print(f"  {name.upper():12} → {data['path']}")
        print(f"               Time: {data['time']:.2f}s")
        print()
    
    print("🎧 Open the output files to compare quality:")
    print(f"   open {output_dir}")
    print()
    
    return results


if __name__ == "__main__":
    run_comparison()
