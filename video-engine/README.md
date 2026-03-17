# Orbital Video Template Engine

**The compound play**: same math content that powers Axiom assessments now powers Orbital instructional videos.

One question JSON → one landscape 16:9 instructional video.

---

## Architecture

```
Axiom Question Engine (TypeScript)
           │
           │  { templateId, questionText, solution, correctAnswer, ... }
           ▼
     ┌─────────────────────────────────────────────┐
     │           Video Template Engine              │
     │                                             │
     │   TemplateRegistry                          │
     │   (finds matching VideoTemplate)            │
     │           │                                 │
     │           ▼                                 │
     │   VideoTemplate.generate_manifest()         │
     │   (converts question → step manifest)       │
     │           │                                 │
     └───────────┼─────────────────────────────────┘
                 │
                 │  manifest = [{ type, content, duration, narration, ... }, ...]
                 ▼
     ┌─────────────────────────────────────────────┐
     │         render.py / scene_short.py           │
     │   (renders manifest → Manim → mp4)           │
     └─────────────────────────────────────────────┘
                 │
                 ▼
        video.mp4 (1920×1080, landscape)
```

### The Manifest is the Interface

Templates output a **JSON manifest** (list of step dicts). The renderer consumes it.
This clean separation means:
- You can inspect manifests without rendering (fast, free)
- Templates are easy to test
- Renderer is completely independent of question logic

---

## Quick Start

```bash
cd ~/Desktop/Orbital/video-engine

# Print manifests for all 3 demo questions
python demo.py

# Human-readable step summaries
python demo.py --preview

# Single question
python demo.py --index 0 --preview

# Render all 3 to video (requires orbital_longform venv)
python demo.py --render

# From JSON file
python bridge.py --json sample_questions/examples.json --index 0

# From Axiom Question Engine (requires Node.js + Axiom Platform)
python bridge.py solve-linear-1step --seed 42

# Direct API
python video_engine.py sample_questions/examples.json
```

---

## File Structure

```
video-engine/
├── video_engine.py          # Core engine + template registry
├── bridge.py                # Question Engine → Video Engine connector
├── render.py                # Manim rendering (uses scene_short.py)
├── demo.py                  # Demo with 3 hardcoded examples
├── manim_landscape.cfg      # Manim config for 1920×1080 landscape
├── templates/
│   ├── __init__.py          # Package exports
│   ├── base.py              # VideoTemplate abstract base class
│   ├── algebra_solve.py     # Solve-for-x template
│   ├── graph_explore.py     # Graphing template
│   └── factor_reveal.py     # Factoring template
├── sample_questions/
│   └── examples.json        # 6 sample question JSONs for testing
└── README.md
```

---

## Templates

### AlgebraSolveTemplate
Handles "Solve for x" questions using the `algebra_solve` scene type.

**Supported IDs**: `solve-linear-1step`, `solve-linear-2step`, `solve-multistep`, `linear-*`, `solve-*`

**Video structure**:
1. Skill header box
2. Problem equation
3. Step-by-step algebra (whiteboard style — equations build up)
4. Answer reveal

### GraphExploreTemplate
Handles function graphing questions.

**Supported IDs**: `graph-linear`, `graph-parabola`, `graph-quadratic-*`, `graph-*`

**Video structure**:
1. Skill header box
2. Function equation
3. Graph render (with labeled points, zeros, vertex)
4. Key feature callouts (vertex, x-intercepts, y-intercept)
5. Answer summary

### FactorRevealTemplate
Handles polynomial factoring questions with built-in verification step.

**Supported IDs**: `factor-quadratic`, `factor-gcf`, `factor-difference-of-squares`, `factor-*`

**Video structure**:
1. Skill header box
2. Expression to factor
3. Factoring process (whiteboard steps)
4. Factored form reveal
5. Verification by expansion (proves the factoring is correct)
6. Final answer

---

## Manifest Step Types

These are the proven step types from `scene_short.py`:

| Type | Description | Key Fields |
|------|-------------|------------|
| `math` | MathTex equation | `content` (LaTeX string) |
| `box` | Text in purple-bordered box | `content` (plain text) |
| `graph` | Function graph with NumberPlane | `graph` (see below) |
| `algebra_solve` | Whiteboard equation building | `algebra_solve.steps` |
| `transform` | Morph one equation to another | `from_tex`, `to_tex` |
| `indicate` | Flash/highlight equation | `content` |

### algebra_solve step format:
```python
{
    "type": "algebra_solve",
    "algebra_solve": {
        "title": "Solve for x",          # shown briefly at top
        "steps": [
            {
                "latex": "3x + 7 = 22",  # equation in LaTeX
                "note": "Start here",    # annotation (shown below-right)
                "note_color": "#22D3EE", # annotation color
                "duration": 3.0,         # hold time in seconds
                "narration": "...",      # metadata for future TTS
            },
            # ... more steps
        ],
        "final_color": "#39FF14",        # last step glows green
    }
}
```

### graph step format:
```python
{
    "type": "graph",
    "graph": {
        "x_range": [-5, 5, 1],
        "y_range": [-2, 10, 2],
        "functions": [
            {"expr": "lambda x: x**2", "label": "f(x)", "color": "#22D3EE"}
        ],
        "dots": [
            {"x": 0, "y": 0, "label": "(0,0)", "color": "#39FF14", "radius": 0.08}
        ],
    },
    "duration": 6.0,
}
```

---

## Adding a New Template

1. Create `templates/my_template.py`
2. Inherit from `VideoTemplate`
3. Set `template_id` and `supported_template_ids`
4. Implement `generate_manifest(question_data) -> list[dict]`
5. Import it in `templates/__init__.py`
6. It's auto-discovered by `TemplateRegistry`

```python
from templates.base import VideoTemplate

class MyTemplate(VideoTemplate):
    template_id = "my-template"
    supported_template_ids = ["my-exact-id", "my-prefix-*"]

    def generate_manifest(self, question_data: dict) -> list[dict]:
        return [
            {
                "type": "box",
                "content": question_data["questionText"],
                "duration": 3.0,
                "narration": "...",
            },
            # ... more steps
        ]
```

---

## Style Constants

All templates use Orbital brand colors. **DO NOT change these.**

```python
ORBITAL_CYAN  = "#22D3EE"   # Main equation color
NEON_GREEN    = "#39FF14"   # Final answers, correct indicators
BOX_BORDER    = "#8B5CF6"   # Purple box borders
BOX_FILL      = "#1a1130"   # Dark box fill
LABEL_COLOR   = "#22D3EE"   # Label text
ORANGE_ACCENT = "#F97316"   # Step annotations
```

---

## Narration (TTS-Ready)

Every manifest step includes a `narration` field with natural-language text.
This is **not rendered to audio** yet — it's metadata for future TTS integration.

When TTS is ready:
1. Pass narration text to ElevenLabs (Allison voice)
2. Save audio files
3. Set `audio_path` on each step
4. The renderer will sync audio automatically

---

## Design Principles

- **Deterministic**: same input → same manifest, every time
- **JSON is the interface**: templates know nothing about rendering
- **Reuse, don't rewrite**: uses scene_short.py's proven infrastructure
- **Style is locked**: Orbital brand colors, not negotiable
- **TTS comes later**: narration as metadata now, audio rendering when ready

---

## Dependencies

- Python 3.9+
- Manim Community v0.20+ (in `~/Desktop/Orbital/orbital_longform/venv/`)
- `scene_short.py` (in `~/Desktop/Orbital/orbital_longform/`)
- LaTeX (TinyTeX, for Manim math rendering)
- Node.js + tsx (optional — only needed for live TS engine calls)
