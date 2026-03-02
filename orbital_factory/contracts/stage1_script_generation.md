# Stage 1: Script Generation — Contract
**Owner:** Gauss (via DeepSeek V3 API)
**Last Updated:** 2026-03-02

---

## Input (from Professor Portal)

### Required
- **Problem statement** (text, eventually image upload via OCR)

### Optional
- **Detail level:** `quick` | `standard` | `detailed`
  - `quick` → ~90 seconds, minimal hand-holding, worked example
  - `standard` → ~3-4 minutes, step-by-step with motivation (DEFAULT)
  - `detailed` → ~6+ minutes, full hand-holding, every substep shown
- **Course level:** Free text or dropdown (e.g., "MAT-230 Calculus 2", "College Algebra")
  - Affects vocabulary, assumed prerequisite knowledge, and hand-holding calibration
- **Professor notes:** Free text for specific emphasis
  - e.g., "Emphasize integration by parts", "Skip the factoring — they already know that"
  - e.g., "Focus on the geometric interpretation"

### Auto-detected (future)
- Topic classification from problem text
- Prerequisite knowledge from course level

---

## Output

### JSON Script with this schema:
```json
{
  "meta": {
    "topic": "Area Between Curves",
    "course": "Calculus 2",
    "course_id": "MAT-230",
    "product_family": "explanation",
    "difficulty": "standard",
    "detail_level": "standard",
    "estimated_duration_sec": 200,
    "description": "Find the area enclosed by y = x + 2 and y = x²"
  },
  "steps": [
    {
      "type": "text | math | graph | transform | box | geometric | diagram",
      "content": "LaTeX content",
      "narration": "What the narrator says aloud",
      "display": "replace | build",
      "label": "for box steps: Theorem | Key Fact | Answer | Warning",
      "graph": { ... },
      "transform": { ... },
      "geometric": { ... },
      "diagram": { ... }
    }
  ]
}
```

### Step Types Available
| Type | Use For | Example |
|------|---------|---------|
| `text` | Plain narration, setup, warnings | "Let's find the area between these curves" |
| `math` | Display equation | `A = \int_{-1}^{2} [(x+2) - x^2] dx` |
| `transform` | Show algebraic steps | from_latex → intermediate_steps → to_latex |
| `graph` | Function plots, shaded regions | function_plot, between_curves, tangent_line |
| `box` | Key formulas, theorems, final answers | Area Formula, Answer |
| `geometric` | Shapes, Riemann rectangles | triangle, circle, rectangle |
| `diagram` | Number lines, set diagrams, tables | number_line_cut, sequence_list, table |

### Graph Kinds
| Kind | Description |
|------|-------------|
| `function_plot` | Plot one or more functions |
| `between_curves` | Shade between two functions (func_index + func_index_2) |
| `tangent_line` | Plot with tangent at a point |
| `area_under` | Shade under single curve to x-axis |

---

## Pedagogical Rules (baked into prompt)

1. **Narrator voice:** Tutor talking to ONE student. Conversational, encouraging, not lecturing.
2. **WHY before HOW:** Always motivate the method before executing it.
   - ❌ "We set the equations equal" 
   - ✅ "To find where these curves cross, we need points where they have the same y-value — so we set the equations equal"
3. **Common student mistakes:** Call out when applicable.
   - "Watch the signs — this is where most students make errors"
   - "A negative area means you subtracted in the wrong order"
4. **Detail level scaling:**
   - `quick`: Skip obvious substeps, assume fluency, get to answer
   - `standard`: Show each step, brief motivation, intermediate algebra
   - `detailed`: Show every substep, explain each manipulation, multiple checks
5. **Visual-first when possible:** If the problem has a geometric interpretation, SHOW it before doing algebra.
6. **Every video ends with:**
   - Final answer in a `box` step
   - Pedagogical takeaway (what to remember)
   - Final visual showing the complete picture (when applicable)
7. **Professor notes override defaults:** If professor says "skip factoring," the script skips it regardless of detail level.

---

## Color Palette (locked)
| Color | Hex | Use |
|-------|-----|-----|
| Violet | #8B5CF6 | Primary curve / main object |
| Cyan | #22D3EE | Secondary curve / comparison |
| Neon Green | #39FF14 | Shading / highlighted regions |
| Yellow | #FACC15 | Points / markers / highlights |
| White | #FFFFFF | Text / equations |
| Label Orange | #F59E0B | Box labels, theorem names |

---

## Cost
~$0.001 per script (DeepSeek V3: ~400 tokens in, ~3K tokens out)

---

## What Happens Next
Raw script JSON → **Stage 2: Verification Circle** (or professor review if they choose to bypass circle)

### Professor Review Option
After Stage 2 (or instead of Stage 2), the professor can:
- **Review the script** in their portal
- **Add comments** on specific steps
- **Bypass the circle entirely** and make their own revisions (saves API cost)
- **Approve as-is** to proceed to rendering

---

## API Contract (future)
```
POST /api/v1/generate-script
{
  "problem": "Find the area between y = x+2 and y = x²",
  "detail_level": "standard",      // optional
  "course_level": "Calculus 2",     // optional
  "notes": "Emphasize the setup",   // optional
}

Response:
{
  "script_id": "abc123",
  "script": { ... },               // full JSON script
  "estimated_duration_sec": 200,
  "estimated_cost": {
    "script": 0.001,
    "circle": 0.60,
    "tts": 0.015,
    "total": 0.62
  }
}
```

---

## Visual Types — Full Registry (Updated 2026-03-02)

### Core Step Types
| Type | Use For |
|------|---------|
| `text` | Plain narration, setup, context, warnings |
| `math` | Display a single equation or expression |
| `transform` | Show algebraic manipulation (from → intermediates → to) |
| `box` | Key formulas, theorems, definitions, final answers |
| `graph` | Function plots and shaded regions |
| `geometric` | Basic shapes, Riemann rectangles |
| `diagram` | Number lines, set diagrams, sequences, tables |

### Graph Kinds
| Kind | Description | Key Config |
|------|-------------|------------|
| `function_plot` | Plot one or more functions | `functions[]`, `points[]` |
| `between_curves` | Shade between two functions | `shaded_area.func_index` + `func_index_2` |
| `tangent_line` | Plot with tangent at a point | `tangent_at`, `slope` |
| `area_under` | Shade under curve to x-axis | `shaded_area.func_index` |
| `implicit_function` | Plot implicit curves (circles, ellipses, conics) | `equation`, `x_range`, `y_range` | **NEW** |
| `traced_path` | Animate a point tracing along a curve | `function`, `t_range`, `trace_color` | **NEW** |

### Diagram Kinds
| Kind | Description | Key Config |
|------|-------------|------------|
| `number_line_cut` | Number line with colored regions (Dedekind cuts, intervals) | `cut_at`, `left_label`, `right_label` |
| `set_containment` | Nested/overlapping sets (Venn-style) | `sets[]`, `labels[]` |
| `sequence_list` | Display a sequence of values | `terms[]`, `labels[]` |
| `table` | Formatted table (sign charts, value tables) | `headers[]`, `rows[][]` |
| `bar_chart` | Bar graph for data visualization | `values[]`, `labels[]`, `colors[]` | **NEW** |

### Geometric Kinds
| Kind | Description | Key Config |
|------|-------------|------------|
| `triangle` | Triangle with labeled sides/angles | `vertices`, `labels` |
| `circle` | Circle with radius/center | `center`, `radius`, `labels` |
| `rectangle` | Rectangle (Riemann sums, area models) | `width`, `height`, `labels` |

### Standalone New Types
| Type | Description | Key Config |
|------|-------------|------------|
| `matrix` | Matrix display with brackets (linear algebra) | `entries[][]`, `bracket_type` (round/square/pipe) | **NEW** |
| `brace_label` | Annotate part of a displayed expression with a curly brace | `target_ref`, `label`, `direction` (UP/DOWN) | **NEW** |
| `3d_surface` | 3D surface/solid of revolution (Calc 3, multivariable) | `function`, `x_range`, `y_range`, `camera_angle` | **NEW** |

### Summary: 6 New Visual Types Added
1. **`implicit_function`** (graph kind) — conic sections, circles, level curves
2. **`traced_path`** (graph kind) — animated point tracing, parametric curves, accumulation
3. **`bar_chart`** (diagram kind) — statistics, data comparison
4. **`matrix`** (standalone) — linear algebra, systems of equations
5. **`brace_label`** (standalone) — annotate sub-expressions ("this part equals...")
6. **`3d_surface`** (standalone) — multivariable calc, surfaces, solids of revolution
