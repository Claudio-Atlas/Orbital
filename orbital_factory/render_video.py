"""
Orbital VideoFactory - Video Renderer
Renders Manim scenes for each step with timing from audio
"""

import os
import json
import subprocess
from pathlib import Path


def render_step(latex: str, duration: float, output_path: str, step_num: int):
    """
    Render a single step as video using Manim.
    
    Args:
        latex: LaTeX content to render
        duration: How long the step should be (matches audio)
        output_path: Where to save the video
        step_num: Step number for naming
    """
    # Create a temporary scene file for this step
    scene_code = f'''
from manim import *

class Step{step_num}Scene(Scene):
    def construct(self):
        self.camera.background_color = "#000000"
        
        math = MathTex(r"{latex}", color=WHITE)
        math.scale(1.8)
        
        # Write animation (about 2 seconds)
        self.play(Write(math), run_time=2)
        
        # Hold for remaining time
        hold_time = max(0.1, {duration} - 2.5)
        self.wait(hold_time)
'''
    
    temp_scene = f"/tmp/orbital_step_{step_num}.py"
    with open(temp_scene, "w") as f:
        f.write(scene_code)
    
    # Run Manim
    cmd = [
        "manim",
        "-qm",  # Medium quality (720p, good for dev)
        "--format", "mp4",
        "-o", f"step_{step_num:02d}",
        temp_scene,
        f"Step{step_num}Scene"
    ]
    
    print(f"Rendering step {step_num}...")
    result = subprocess.run(cmd, capture_output=True, text=True)
    
    if result.returncode != 0:
        print(f"Error rendering step {step_num}:")
        print(result.stderr)
        return None
    
    # Find the output file
    media_dir = Path("media/videos") / f"orbital_step_{step_num}" / "720p30"
    video_file = media_dir / f"step_{step_num:02d}.mp4"
    
    if video_file.exists():
        # Move to desired output location
        os.makedirs(os.path.dirname(output_path), exist_ok=True)
        os.rename(video_file, output_path)
        print(f"  → Saved to {output_path}")
        return output_path
    
    return None


def render_all_steps(manifest_path: str, output_dir: str) -> list:
    """
    Render all steps from an audio manifest.
    
    Args:
        manifest_path: Path to audio manifest JSON
        output_dir: Directory to save video files
    
    Returns:
        List of video file paths
    """
    with open(manifest_path) as f:
        manifest = json.load(f)
    
    os.makedirs(output_dir, exist_ok=True)
    videos = []
    
    for step in manifest:
        step_num = step["step"]
        latex = step["latex"]
        duration = step["duration"]
        
        output_path = os.path.join(output_dir, f"step_{step_num:02d}.mp4")
        result = render_step(latex, duration, output_path, step_num)
        
        if result:
            videos.append({
                "step": step_num,
                "video_path": result,
                "audio_path": step["audio_path"],
                "duration": duration
            })
    
    return videos


def compose_final(videos: list, output_path: str):
    """
    Combine all step videos with audio into final video.
    Uses FFmpeg to merge video clips and add audio.
    """
    if not videos:
        print("No videos to compose")
        return
    
    # Create concat file for FFmpeg
    concat_file = "/tmp/orbital_concat.txt"
    with open(concat_file, "w") as f:
        for v in videos:
            f.write(f"file '{v['video_path']}'\n")
    
    # Concatenate videos
    temp_video = "/tmp/orbital_temp.mp4"
    cmd = [
        "ffmpeg", "-y",
        "-f", "concat",
        "-safe", "0",
        "-i", concat_file,
        "-c", "copy",
        temp_video
    ]
    subprocess.run(cmd, capture_output=True)
    
    # Concatenate audio files
    audio_concat = "/tmp/orbital_audio_concat.txt"
    with open(audio_concat, "w") as f:
        for v in videos:
            f.write(f"file '{v['audio_path']}'\n")
    
    temp_audio = "/tmp/orbital_temp_audio.mp3"
    cmd = [
        "ffmpeg", "-y",
        "-f", "concat",
        "-safe", "0",
        "-i", audio_concat,
        "-c", "copy",
        temp_audio
    ]
    subprocess.run(cmd, capture_output=True)
    
    # Merge video and audio
    cmd = [
        "ffmpeg", "-y",
        "-i", temp_video,
        "-i", temp_audio,
        "-c:v", "copy",
        "-c:a", "aac",
        "-shortest",
        output_path
    ]
    subprocess.run(cmd, capture_output=True)
    
    print(f"\nFinal video saved to: {output_path}")


if __name__ == "__main__":
    import sys
    
    if len(sys.argv) < 2:
        print("Usage: python render_video.py <manifest.json> [output_dir]")
        sys.exit(1)
    
    manifest_path = sys.argv[1]
    output_dir = sys.argv[2] if len(sys.argv) > 2 else "video/output"
    
    videos = render_all_steps(manifest_path, output_dir)
    
    if videos:
        compose_final(videos, os.path.join(output_dir, "final.mp4"))
