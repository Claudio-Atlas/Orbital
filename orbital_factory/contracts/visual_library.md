# Orbital Visual Library — Scene Type Catalog
**Last Updated:** 2026-03-05
**File:** `orbital_factory/scene_short.py`

---

## How It Works

Every Orbital video is a sequence of **steps**. Each step has a `type` field that tells the scene generator what to render. The text presentation (math, box, mixed) is consistent across all videos — that's the Orbital brand. The special visual types are what make individual videos unique.

## Text Presentation (Brand Standard — DO NOT CHANGE)

These are the baseline. Every video uses these. They define the Orbital look.

| Type | What It Does | Visual Style |
|------|-------------|--------------|
| `math` | Pure LaTeX equation (MathTex) | White text, centered, Write animation |
| `text` | Plain text (also renders as MathTex) | Same as math — used for titles, labels |
| `mixed` | LaTeX with inline prose | Same renderer — for "word + symbol" steps |
| `box` | Highlighted theorem/fact box | Violet border (#9333EA), dark fill (0.6 opacity), optional label above in #A78BFA |
| `transform` | Equation morphs into another | TransformMatchingTex animation between two MathTex objects |

**Layout constants (portrait 9:16):**
- Frame: 4.5 × 8.0
- Math center: y = 1.2
- Graph center: y = -1.8
- Math scale: 0.85, Box scale: 0.65

**Layout constants (landscape 16:9):**
- Frame: 14.2 × 8.0
- Math center: y = 1.5
- Graph center: y = -1.5
- Math scale: 1.4, Box scale: 0.90

---

## Special Visual Types (The Library)

### Graphs & Plotting

| # | Type | Description | Config Fields | Example Use |
|---|------|-------------|---------------|-------------|
| 1 | `graph` | 2D function plot with axes. Supports multiple functions, tangent lines, shaded areas, area between curves. | `graph.functions[]`, `graph.x_range`, `graph.y_range`, `graph.tangent`, `graph.shaded_area` | Derivative videos, integral visualization |

**Graph sub-kinds** (via `diagram.kind`):
- `function_plot` — basic curve on axes
- `tangent_line` — function + tangent at a point
- `area_under` — shaded area under curve
- `between_curves` — shaded between two functions

### Dot & Curve Animations

| # | Type | Description | Config Fields | Example Use |
|---|------|-------------|---------------|-------------|
| 2 | `animated_dot` | Dot slides along a curve with optional tangent line following it | `expr`, `x_start`, `x_end`, `show_tangent` | "Watch the slope change" moments |
| 3 | `trace_dot` | Dot traces along a curve (simpler version of animated_dot) | `expr`, `x_start`, `x_end` | Tracing a function path |

### Derivative-Specific Visuals

| # | Type | Description | Config Fields | Example Use |
|---|------|-------------|---------------|-------------|
| 4 | `secant_to_tangent` | Animated: secant line approaches tangent as Δx → 0 | `expr`, `at_x`, `h_values[]` | Definition of derivative |
| 5 | `rise_run` | Shows rise/run triangle on a graph with labels | `expr`, `at_x`, `dx` | Slope visualization |
| 6 | `h_countdown` | Shows Δx shrinking toward 0 with numerical readout | `expr`, `at_x`, `h_values[]` | Limit definition |

### Equation Manipulation

| # | Type | Description | Config Fields | Example Use |
|---|------|-------------|---------------|-------------|
| 7 | `equation_highlight` | Colors specific parts of an equation | `content`, `highlights[{range, color}]` | Pointing out specific terms |
| 8 | `indicate` | Flash/highlight animation on a mobject | `content`, `target` | Drawing attention |
| 9 | `algebra_solve` | Multi-step algebra walkthrough with color-coded operations and side notes | `title`, `steps[{left, op, right, note}]` | Step-by-step problem solving |
| 10 | `brace_anatomy` | Labeled braces pointing at parts of an equation | `content`, `braces[{range, label, direction}]` | "This part means THIS" |
| 11 | `strikethrough_cancel` | Cross out / cancel terms in an equation | `content`, `cancel_ranges[]` | Simplification, cancellation |
| 12 | `foil_expansion` | FOIL multiplication with colored connections | `term1`, `term2` | Polynomial multiplication |

### Integration-Specific

| # | Type | Description | Config Fields | Example Use |
|---|------|-------------|---------------|-------------|
| 13 | `riemann_sum` | Rectangles under a curve, animates refinement as n increases | `expr`, `x_range`, `n_values[]` | "What integration actually does" |

### Camera & Zoom

| # | Type | Description | Config Fields | Example Use |
|---|------|-------------|---------------|-------------|
| 14 | `zoom_to_point` | Zooms into a specific point on an existing graph | `center_x`, `center_y`, `zoom_factor` | Limit behavior, epsilon-delta |

---

## What's NOT in the Library Yet

These are visual concepts we've discussed or that would serve "why" videos but haven't been built:

| Concept | Difficulty | Would Serve |
|---------|-----------|-------------|
| Factorial cascade (n! → (n-1)! chain) | Easy | "Why is 0! = 1?" |
| Pattern table (rows appearing one by one) | Easy | Any pattern-based proof |
| Rectangle area proof (product rule visual) | Medium | "Why does the product rule work?" |
| Unit circle animation | Medium | "Why is derivative of sin = cos?" |
| Pizza slice → parallelogram (area proof) | Medium | "Why is area of circle πr²?" |
| Chain of function machines | Medium | "Why does the chain rule work?" |
| Number line zoom (ε-δ bands) | Medium | Limit proofs |
| Taylor polynomial accumulation | Medium | "Why do Taylor series work?" |
| Matrix transformation (plane warping) | Hard | Linear algebra visuals |
| 3D surface rotation | Hard | Solids of revolution, multivariable |
| Split-screen comparison | Easy | Before/after, method comparison |
| Countdown/counter display | Easy | Showing numerical convergence |

---

## Adding a New Visual Type

When adding a new step type to `scene_short.py`:

1. Add a new `if stype == "your_type":` block in `SyncedShortScene.construct()`
2. Follow the timing model:
   - Build mobject (no timeline cost)
   - `add_sound()` — audio starts
   - `FadeOut(previous)` — 0.3-0.4s
   - Animate new content
   - `wait(remaining)` — hold for voice
   - `wait(EXTRA_HOLD)` — breathing room
3. Handle both portrait and landscape constants
4. Update THIS catalog
5. Test with a minimal manifest JSON

---

*This catalog is the source of truth for what visuals exist. Visionary reads it before designing. Builder reads it before coding.*
