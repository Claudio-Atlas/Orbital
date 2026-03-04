# Short-Form Video Production Guide
**Owner:** Video Production Lead  
**Last Updated:** 2026-03-03  
**READ THIS BEFORE EVERY VIDEO SESSION — NO EXCEPTIONS**

---

## Pipeline Phases

### Phase 1: Planning
- Decide the topic and scope (ONE concept per video)
- Keep each video 45-90s (under 120s absolute max for YouTube Shorts)
- Write a 1-sentence goal: "After watching, the viewer understands ___"

### Phase 2: Script Generation
- Draft a script JSON (array of steps)
- Each step: `{step, type, content, narration, layout}`
- Types: `"box"` (text), `"math"` (LaTeX), `"graph"` (function plot)
- Wrap in `{"problem": "...", "steps": [...]}` for the pipeline

### Phase 3: Circle Review
- Spawn Circle subagent with 6 reviewers
- Circle MUST output the **complete revised script JSON** — not just a list of issues
- Model: `anthropic/claude-sonnet-4-6`
- Contract: `contracts/stage2_verification_circle.md`

### Phase 4: Render
```bash
cd ~/Desktop/Orbital/orbital_factory
source venv/bin/activate
PATH="/Library/TeX/texbin:$PATH" python3 -c "
from pipeline_short import generate_short_video
result = generate_short_video(
    problem='<PROBLEM>',
    script_path='jobs/<SLUG>/script_wrapped.json',
    output_name='short_<SLUG>.mp4',
    skip_verify=True,
)
"
```

### Phase 5: QA
- Watch the full video
- Check: text readable? graph visible? voice synced? no overlaps?
- Duration under 120s?

### Phase 6: Upload
- Add YouTube ID to `/watch` page on orbital_site
- Git push to deploy

---

## CRITICAL SETTINGS — DO NOT CHANGE

### Frame
- **Resolution:** 1080×1920 (9:16)
- **Frame rate:** 60fps
- **Manim frame:** 4.5 wide × 8.0 tall
- **Config:** `manim_short.cfg`

### Text Sizing (THESE MATTER)
- **Box text:** `Text(content, font_size=42, color=WHITE)` — NOT MathTex for plain text
- **Math:** `MathTex(content, color=WHITE).scale(MATH_SCALE * scale_override)` where `MATH_SCALE=0.85`
- **BOX_SCALE:** `0.65` (applied to MathTex boxes only, NOT Text boxes)
- **Minimum readable font:** 28pt equivalent in Manim = `font_size=36` minimum
- **65% width rule:** No content wider than 3.105 Manim units (`MAX_WIDTH = FRAME_W * 0.82` but visual content capped at 65%)

### Layout Constants
```python
FRAME_W = 4.5
FRAME_H = 8.0
MAX_WIDTH = FRAME_W * 0.82  # 3.69 Manim units
MATH_SCALE = 0.85
BOX_SCALE = 0.65  # for MathTex boxes only
GRAPH_WIDTH = 3.4
GRAPH_HEIGHT = 2.8
MATH_CENTER_Y = 1.2    # Zone B center
GRAPH_CENTER_Y = -1.8  # Zone C center
ANIMATION_RATIO = 0.35
EXTRA_HOLD = 0.8
```

### Colors
```python
VIOLET    = "#8B5CF6"  # Primary brand, borders, glow
CYAN      = "#22D3EE"  # Graphs, labels
GREEN     = "#39FF14"  # Tangent lines, solutions, highlights
BOX_BORDER = "#8B5CF6"
BOX_FILL   = "#1a1130"
```

### Voice
- **Voice:** Allison (teaching voice)
- **Voice ID:** `5jVVMAv2LzffTcLGarKh`
- **Model:** `eleven_turbo_v2_5`
- **Settings (LOCKED — Option C):**
  - stability: 0.50
  - similarity_boost: 0.75
  - style: 0.25
  - speed: 0.90
- **Profile:** `voice_profiles/allison_tiktok.json`

### Music
- **File:** `assets/audio/bg_synthwave.mp3` (88.2s)
- **Volume:** 12% under voice
- **Loop:** `-stream_loop -1` in FFmpeg
- **Duration:** `duration=first` (stops when video ends)

### Timing Model
```python
anim_time = max(1.2, duration * ANIMATION_RATIO)  # ANIMATION_RATIO = 0.35
# After fadeout: 0.15s beat (voice leads visual)
# Between steps: EXTRA_HOLD = 0.8s
```

### Graph Steps
- When script has `"type": "graph", "content": "x**2"`:
  - scene_short.py auto-converts to graph config with functions array
  - Graph renders center screen first (hero moment), then slides to GRAPH_CENTER_Y
- Graph persists on screen for remaining steps

### End Card
- Lissajous curve (3:2) in violet `#8B5CF6` — NOT cyan (brand updated 2026-03-03)
- Draw animation via `Create()`, then "ORBITAL" wordmark fades in
- No separate outro video — end card is built into Manim scene

---

## Common Bugs & Fixes

| Bug | Cause | Fix |
|-----|-------|-----|
| Text has no spaces | Using `MathTex()` for plain text | Use `Text()` for box steps |
| Graph shows empty axes | Script has `"content": "x**2"` but no `"graph"` config | scene_short.py auto-converts (fixed 2026-03-03) |
| Voice overlapping | Total narration > video duration | Trim narrations or split into multiple videos |
| Music cuts early | Video longer than music file | `-stream_loop -1` loops the music |
| Tiny text | Wrong font_size or scale | Box text: `font_size=42`, math: `MATH_SCALE=0.85` |
| Equations run off screen | Long equation not auto-broken | Equations with 2+ `=` signs auto-break to `aligned` |

---

## Playlist: "Derivatives from Scratch"

| # | Video | Duration | Status | YouTube ID |
|---|-------|----------|--------|------------|
| 0 | What is a Derivative? (conceptual) | ~60s | PLANNING | — |
| 1 | The Constant Rule | 59s | ✅ LIVE | WaSbLQewrp8 |
| 2 | The Power Rule | 66s | ✅ LIVE | CVAdvoqXaqw |
| 3 | Power Rule: Negative Exponents | 119s | ✅ LIVE | r-vMVR_3208 |
| 4 | Find the Derivative of 3x²+2x-5 | 103s | ✅ LIVE | lGc-f3--Nas |
| — | Secant Lines | ~60s | PLANNING | — |
| — | The Limit Definition | ~90s | PLANNING | — |
| — | Fractional Exponents | ~90s | PLANNING | — |

---

## File Locations

| File | Path |
|------|------|
| Pipeline | `~/Desktop/Orbital/orbital_factory/pipeline_short.py` |
| Scene generator | `~/Desktop/Orbital/orbital_factory/scene_short.py` |
| Manim config | `~/Desktop/Orbital/orbital_factory/manim_short.cfg` |
| Voice profile | `~/Desktop/Orbital/orbital_factory/voice_profiles/allison_tiktok.json` |
| Circle contract | `~/Desktop/Orbital/orbital_factory/contracts/stage2_verification_circle.md` |
| Design spec | `~/Desktop/Orbital/orbital_factory/TIKTOK-DESIGN-SPEC.md` |
| Background music | `~/Desktop/Orbital/orbital_factory/assets/audio/bg_synthwave.mp3` |
| Output folder | `~/Desktop/Orbital/orbital_factory/output/` |
| Jobs folder | `~/Desktop/Orbital/orbital_factory/jobs/` |
| **THIS FILE** | `~/Desktop/Orbital/orbital_factory/SHORT_PRODUCTION_GUIDE.md` |

---

## Before EVERY Render

✅ Read this file  
✅ Check `scene_short.py` uses `Text()` for boxes (not `MathTex`)  
✅ Check box `font_size >= 42`  
✅ Check total narration word count ÷ 2.5 < 120s  
✅ Check graph steps have `"content"` field with expression  
✅ Run Circle with 6 reviewers  
✅ Circle outputs revised script JSON (not just issues)  
✅ Watch the rendered video before declaring done  
