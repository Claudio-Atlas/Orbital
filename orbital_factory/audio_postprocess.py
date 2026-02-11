"""
Orbital VideoFactory - Audio Post-Processing Pipeline
=====================================================
Polishes raw TTS audio to broadcast quality.

Pipeline:
1. Noise gate (remove low-level artifacts)
2. High-pass filter (remove rumble < 80Hz)
3. EQ (warm up mids, soften harsh highs)
4. Compression (even out dynamics)
5. Limiter (prevent clipping)
6. Normalize (consistent output level)

Usage:
    from audio_postprocess import process_audio
    process_audio("raw_tts.mp3", "polished_output.mp3")

Or CLI:
    python audio_postprocess.py input.mp3 output.mp3
"""

import os
import subprocess
from pathlib import Path


def process_audio(input_path: str, output_path: str = None, preset: str = "tutor") -> str:
    """
    Apply broadcast-quality post-processing to TTS audio.
    
    Args:
        input_path: Path to raw TTS audio
        output_path: Path for processed output (default: adds _processed suffix)
        preset: Processing preset ("tutor", "energetic", "gentle")
    
    Returns:
        Path to processed audio file
    """
    input_path = Path(input_path)
    
    if output_path is None:
        output_path = input_path.parent / f"{input_path.stem}_processed{input_path.suffix}"
    else:
        output_path = Path(output_path)
    
    # Preset configurations
    presets = {
        "tutor": {
            # Calm, clear, educational — like 3Blue1Brown
            "highpass": 80,           # Remove rumble below 80Hz
            "lowpass": 12000,         # Gentle rolloff above 12kHz
            "eq_low_gain": 1,         # Slight bass boost at 200Hz
            "eq_mid_gain": 2,         # Presence boost at 2.5kHz
            "eq_high_gain": -2,       # Reduce harshness at 6kHz
            "compression_threshold": -20,
            "compression_ratio": 3,
            "compression_attack": 10,
            "compression_release": 100,
            "normalize_level": -1,
        },
        "energetic": {
            # More dynamic, excited delivery
            "highpass": 100,
            "lowpass": 14000,
            "eq_low_gain": 2,
            "eq_mid_gain": 3,
            "eq_high_gain": 0,
            "compression_threshold": -15,
            "compression_ratio": 4,
            "compression_attack": 5,
            "compression_release": 50,
            "normalize_level": -0.5,
        },
        "gentle": {
            # Soft, intimate, ASMR-like
            "highpass": 60,
            "lowpass": 10000,
            "eq_low_gain": 2,
            "eq_mid_gain": 0,
            "eq_high_gain": -4,
            "compression_threshold": -25,
            "compression_ratio": 2,
            "compression_attack": 20,
            "compression_release": 200,
            "normalize_level": -2,
        }
    }
    
    p = presets.get(preset, presets["tutor"])
    
    # Build FFmpeg filter chain
    filters = [
        # 1. High-pass filter (remove rumble)
        f"highpass=f={p['highpass']}",
        
        # 2. Low-pass filter (remove harsh highs)
        f"lowpass=f={p['lowpass']}",
        
        # 3. EQ - three band adjustment
        # Bass warmth around 200Hz
        f"equalizer=f=200:t=q:w=1:g={p['eq_low_gain']}",
        # Presence/clarity around 2.5kHz  
        f"equalizer=f=2500:t=q:w=1:g={p['eq_mid_gain']}",
        # Reduce harshness around 6kHz
        f"equalizer=f=6000:t=q:w=1:g={p['eq_high_gain']}",
        
        # 4. Compression (even out dynamics)
        f"acompressor=threshold={p['compression_threshold']}dB:ratio={p['compression_ratio']}:attack={p['compression_attack']}:release={p['compression_release']}",
        
        # 5. Limiter (prevent clipping)
        "alimiter=limit=0.95:attack=5:release=50",
        
        # 6. Normalize to target level
        f"loudnorm=I=-16:TP={p['normalize_level']}:LRA=11",
    ]
    
    filter_chain = ",".join(filters)
    
    # Run FFmpeg
    cmd = [
        "ffmpeg", "-y",
        "-i", str(input_path),
        "-af", filter_chain,
        "-ar", "44100",  # Standard sample rate
        "-b:a", "192k",  # High quality bitrate
        str(output_path)
    ]
    
    result = subprocess.run(cmd, capture_output=True, text=True)
    
    if result.returncode != 0:
        print(f"FFmpeg error: {result.stderr}")
        return None
    
    return str(output_path)


def process_audio_simple(input_path: str, output_path: str = None) -> str:
    """
    Simpler processing using pydub (fallback if ffmpeg filters unavailable).
    Basic normalization and format conversion.
    """
    try:
        from pydub import AudioSegment
        from pydub.effects import normalize, compress_dynamic_range
        
        audio = AudioSegment.from_file(input_path)
        
        # Apply basic processing
        audio = normalize(audio)
        audio = compress_dynamic_range(audio, threshold=-20.0, ratio=3.0)
        
        if output_path is None:
            input_p = Path(input_path)
            output_path = input_p.parent / f"{input_p.stem}_processed.mp3"
        
        audio.export(output_path, format="mp3", bitrate="192k")
        return str(output_path)
        
    except Exception as e:
        print(f"Pydub error: {e}")
        return None


def batch_process(input_dir: str, output_dir: str = None, preset: str = "tutor"):
    """
    Process all audio files in a directory.
    """
    input_dir = Path(input_dir)
    output_dir = Path(output_dir) if output_dir else input_dir / "processed"
    output_dir.mkdir(exist_ok=True)
    
    audio_extensions = {".mp3", ".wav", ".m4a", ".ogg", ".flac"}
    
    processed = []
    for f in input_dir.iterdir():
        if f.suffix.lower() in audio_extensions:
            out_path = output_dir / f"{f.stem}_processed{f.suffix}"
            result = process_audio(str(f), str(out_path), preset)
            if result:
                processed.append(result)
                print(f"✅ {f.name} → {out_path.name}")
            else:
                print(f"❌ Failed: {f.name}")
    
    return processed


# Quick test function
def test_processing():
    """Test the pipeline with a sample."""
    test_dir = Path(__file__).parent.parent / "tts_test" / "comparison_output"
    
    if not test_dir.exists():
        print("No test files found")
        return
    
    # Find first audio file
    for f in test_dir.iterdir():
        if f.suffix in {".wav", ".mp3"}:
            print(f"Processing: {f.name}")
            output = process_audio(str(f), preset="tutor")
            if output:
                print(f"✅ Output: {output}")
                return output
    
    print("No audio files found in test directory")
    return None


if __name__ == "__main__":
    import sys
    
    if len(sys.argv) < 2:
        print("Usage: python audio_postprocess.py <input> [output] [preset]")
        print("\nPresets: tutor (default), energetic, gentle")
        print("\nOr run test: python audio_postprocess.py --test")
        sys.exit(1)
    
    if sys.argv[1] == "--test":
        test_processing()
    else:
        input_file = sys.argv[1]
        output_file = sys.argv[2] if len(sys.argv) > 2 else None
        preset = sys.argv[3] if len(sys.argv) > 3 else "tutor"
        
        if output_file and output_file in ["tutor", "energetic", "gentle"]:
            preset = output_file
            output_file = None
        
        result = process_audio(input_file, output_file, preset)
        if result:
            print(f"✅ Processed: {result}")
        else:
            print("❌ Processing failed")
