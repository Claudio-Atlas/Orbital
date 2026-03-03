# Stage 5: Manim Render — Contract
**Owner:** Ramanujan
**Last Updated:** 2026-03-02

---

## Purpose
Render the final video by converting the revised script + audio timing map into a Manim animation with synchronized narration. Output: a single MP4 file ready for delivery.

## Architecture

```
Stage 4 (audio + timing map)
    ↓
scene_v3.py interprets script steps
    ↓
Manim renders each step as animation
    ↓
Raw video (no audio)
    ↓
ffmpeg merges video + combined audio track
    ↓
Final MP4 (1080p60, H.264 + AAC)
```

## Key Design: ffmpeg Post-Merge (NOT add_sound)

**⚠️ CRITICAL:** Manim's `add_sound()` is unreliable for multiple audio clips. It only embeds the first clip properly. **ALWAYS** use ffmpeg post-merge:

```bash
ffmpeg -y -i "$RAW_VIDEO" -i "$COMBINED_AUDIO" \
  -map 0:v -map 1:a \
  -c:v copy -c:a aac -b:a 192k \
  -shortest \
  "$FINAL_OUTPUT"
```

This was learned the hard way — the Area Between Curves video had only 13.7s of audio embedded out of 232s because `add_sound()` silently failed on clips 2-21.

## Scene Engine: scene_v3.py

The scene engine interprets step types from the script JSON and generates corresponding Manim animations.

### Supported Step Types

| Type | Description | Manim Implementation |
|------|-------------|---------------------|
| `text` | Plain text narration | `Text()` objects, fade in/out |
| `math` | LaTeX equation display | `MathTex()`, Write animation |
| `mixed` | Text + math combined | `VGroup` of Text + MathTex |
| `transform` | Equation transformation | `TransformMatchingTex` from→to |
| `box` | Highlighted result box | `MathTex` + `SurroundingRectangle` |
| `graph` | Function plots, shading | `Axes` + `plot()` + `get_area()` |
| `diagram` | Visual diagrams | Custom per diagram kind |

### Graph Kinds (in `graph` steps)

| Kind | Description | Status |
|------|-------------|--------|
| `function_plot` | Plot one or more functions | ✅ Working |
| `area_under` | Shade area under curve to x-axis | ✅ Working |
| `between_curves` | Shade area between two curves | ✅ Working (uses `bounded_graph`) |
| `number_line` | Number line with points/intervals | ✅ Working |
| `implicit_function` | Implicit curve (e.g., circle) | ❌ Not yet built |
| `traced_path` | Animated parametric path | ❌ Not yet built |
| `bar_chart` | Bar chart / histogram | ❌ Not yet built |

### Standalone Visual Types (future)

| Type | Description | Status |
|------|-------------|--------|
| `matrix` | Matrix display with operations | ❌ Not yet built |
| `brace_label` | Brace annotation on expressions | ❌ Not yet built |
| `3d_surface` | 3D surface plot (ThreeDScene) | ❌ Not yet built |

### Color Palette (Orbital brand)

```python
ORBITAL_COLORS = {
    "neon_green": "#39FF14",
    "violet": "#8B5CF6",
    "cyan": "#22D3EE",
    "amber": "#F59E0B",
    "rose": "#F43F5E",
    "background": "#000000",
    "text": "#FFFFFF",
    "dim_text": "#9CA3AF",
}
```

Background is always black. Text is always white. Accent colors used for highlights, boxes, and graph elements.

## Process

### Step 1: Load Script + Timing Map
```python
script = load_json("scripts/{slug}_revised.json")
timing = load_json("output/{slug}_timing.json")
```

### Step 2: Calculate Step Durations
Each step's animation duration is determined by its audio duration from the timing map:

```python
for step in script["steps"]:
    step_timing = timing["step_timings"][step["step_number"]]
    step["anim_duration_s"] = step_timing["duration_ms"] / 1000
```

### Step 3: Render with Manim
```python
class OrbitalVideo(Scene):
    def construct(self):
        self.camera.background_color = "#000000"
        for step in script["steps"]:
            self._render_step(step)
    
    def _render_step(self, step):
        # Dispatch by step type
        if step["type"] == "text":
            self._render_text(step)
        elif step["type"] == "math":
            self._render_math(step)
        elif step["type"] == "transform":
            self._render_transform(step)
        elif step["type"] == "box":
            self._render_box(step)
        elif step["type"] == "graph":
            self._render_graph(step)
        # ... etc
```

### Step 4: Render Command
```bash
cd orbital_factory
source venv/bin/activate
export PATH="/Library/TeX/texbin:$PATH"
manim render -qh --format mp4 scene_v3.py OrbitalVideo
```

**Quality settings:**
- `-qh` = 1080p60 (production)
- `-qm` = 720p30 (preview/testing)
- `-ql` = 480p15 (fast iteration)

### Step 5: ffmpeg Audio Merge
```bash
ffmpeg -y \
  -i media/videos/scene_v3/1080p60/OrbitalVideo.mp4 \
  -i output/{slug}_combined_audio.mp3 \
  -map 0:v -map 1:a \
  -c:v copy -c:a aac -b:a 192k \
  -shortest \
  output/{slug}_final.mp4
```

### Step 6: Verify Output
```python
# Check video has both streams
probe = ffprobe(output_path)
assert probe.has_video_stream
assert probe.has_audio_stream
assert abs(probe.video_duration - probe.audio_duration) < 5.0  # within 5s
```

## Input

From Stage 4:
```json
{
  "revised_script": "<script JSON>",
  "verification": { ... },
  "audio": {
    "combined_path": "output/{slug}_combined_audio.mp3",
    "step_segments": [...],
    "timing_map": { ... },
    "total_duration_ms": 232000
  }
}
```

## Output

To Stage 6:
```json
{
  "video": {
    "path": "output/{slug}_final.mp4",
    "resolution": "1920x1080",
    "fps": 60,
    "duration_s": 232,
    "file_size_mb": 6.1,
    "codec_video": "H.264",
    "codec_audio": "AAC",
    "has_audio": true
  },
  "verification": { ... },
  "metadata": {
    "problem": "...",
    "course": "...",
    "detail_level": "standard",
    "steps": 21,
    "badge": "lean4_verified"
  }
}
```

## Animation Timing Rules

Each step has a total duration determined by its audio. The animation budget is split:

```
Total step time = audio_duration + inter_step_silence
Animation budget:
  - Write/Create: 30% of audio duration (min 0.5s, max 2.0s)
  - Hold/display: remaining time
  - FadeOut: 0.3s (overlaps with next step's FadeIn)
```

**Transform steps** are special:
```
  - Show from_latex: 20% of time
  - Transform animation: 30% of time
  - Hold result: remaining time (THIS MUST USE FULL REMAINING, not 30%)
```

The transform hold bug was fixed — `scene_v3.py` line 616 previously did `self.wait(remaining * 0.3)` which cut ~40s of audio across 8 transform steps. Now uses `self.wait(remaining)`.

## Known Bugs & Fixes Applied

| Bug | Fix | Date |
|-----|-----|------|
| `add_sound()` only embeds first clip | Always use ffmpeg post-merge | 2026-03-02 |
| Transform hold timing cut short | `remaining * 0.3` → `remaining` | 2026-03-02 |
| Box step used `Tex` instead of `MathTex` | Line 500: `Tex` → `MathTex` | 2026-03-02 |
| `area_under` shades to x-axis, not between curves | Added `between_curves` kind with `bounded_graph` | 2026-03-02 |
| Area Between Curves graphs don't render | ❌ OPEN — needs investigation | 2026-03-02 |

## Render Performance

| Video Length | Render Time (1080p60) | File Size |
|---|---|---|
| ~30s (sizzle reel) | ~30s | ~2 MB |
| ~4min (standard) | ~3-5 min | ~6-10 MB |
| ~5min (detailed) | ~5-7 min | ~10-15 MB |

Render is local and free. Mac Mini M4 Pro (arriving ~Mar 30) will cut render times significantly.

## Cost Estimate

| Component | Cost |
|-----------|------|
| Manim render | Free (local CPU) |
| ffmpeg merge | Free (local CPU) |
| **Total** | **$0.00** |

---

## Integration Notes

- Stage 5 receives: script + audio + timing map from Stage 4
- Stage 5 outputs to: Stage 6 (Delivery) with final MP4 + metadata
- The timing map from Stage 4 is the single source of truth for animation sync
- scene_v3.py is the only file that needs to change when adding new visual types
- All rendering happens locally — no cloud costs, no API calls
