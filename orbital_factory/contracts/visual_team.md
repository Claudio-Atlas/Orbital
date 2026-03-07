# Visual Creation Team — Contract
**Created:** 2026-03-05
**Last Updated:** 2026-03-07

---

## Overview

The Visual Creation Team designs and builds new visual types for Orbital's video pipeline. The scene library grows with every video produced.

## The Team

| Agent | Role | Model | Label | Focus |
|-------|------|-------|-------|-------|
| **Iris** | Creative Lead & Visual Architect | claude-opus-4-6 | `orbital-iris` | Generates viral short concepts + designs visual briefs. The idea engine AND the visual eye. |
| **Claudio** | Renderer & Integrator | (main assistant) | — | Renders Iris's briefs in Manim, shows her the output, iterates until approved. |

**Forge** (Visual Engineer) is retired from the core loop as of 2026-03-07. Claudio handles rendering directly, which lets Iris close the feedback loop — she sees the actual render and iterates, instead of designing blind.

**Agent specs:** `~/.openclaw/workspace/memory/agents/iris.md`

## Workflow (Updated 2026-03-07)

```
IRIS generates concept pitches (calculus-focused, WHY questions, visual potential)
    ↓
CLAYTON picks from pitches (or assigns a concept)
    ↓
┌─────────────────────────────────────────────┐
│ IRIS reads:                                  │
│   - visual_library.md (what exists)          │
│   - The concept to visualize                 │
│   - Past briefs (learns what works)          │
│                                              │
│ IRIS delivers: Visual Brief                  │
│   - Core insight                             │
│   - Existing types to reuse                  │
│   - New types needed (with specs)            │
│   - Step-by-step storyboard                  │
└──────────────────┬──────────────────────────┘
                   ↓
┌─────────────────────────────────────────────┐
│ CLAUDIO:                                     │
│   - Reads Iris's visual brief                │
│   - Implements in Manim                      │
│   - Renders preview (silent or with TTS)     │
│   - Shows Iris the rendered frames           │
└──────────────────┬──────────────────────────┘
                   ↓
┌─────────────────────────────────────────────┐
│ IRIS REVIEW:                                 │
│   - Compares render against her vision       │
│   - Approves OR requests changes             │
│   - "Graph too small", "fade too fast", etc. │
│   - Iterate with Claudio until satisfied     │
└──────────────────┬──────────────────────────┘
                   ↓
         CLAYTON FINAL REVIEW (approve for library)
                   ↓
┌─────────────────────────────────────────────┐
│ IF APPROVED:                                 │
│   - Claudio adds code to scene_short.py      │
│   - Updates visual_library.md                │
│   - Commits to git                           │
│   - New type available for ALL future videos  │
└─────────────────────────────────────────────┘
```

### Why This Works Better
- **Iris closes the loop** — she sees real renders and iterates, building taste over time
- **No middleman** — Clayton doesn't need to judge every visual iteration
- **Faster cycles** — Claudio renders immediately, no waiting for a separate agent to spin up
- **Iris gets better** — every render she reviews teaches her what Manim can do, making future briefs tighter
- **The flywheel** — more shorts → more Iris briefs → more renders → Iris improves → briefs get tighter → faster production → more shorts

## Key Principles

### 0. ALIVE Is the Default (Established 2026-03-07)
Every visual must feel like a living organism. Inspired by AIGENTS neural net visualization.
- **Glow layers** on every key mobject (stroke 6, opacity 0.15)
- **Pulsing** on active elements (opacity 0.7↔1.0)
- **Brightness = attention** (discussed = bright, context = dim at 0.3)
- **Bloom flash** on reveals (0.2s spike then settle)
- **Breathing** on persistent elements (scale 1.0↔1.02)
- **Organic easing** always (never linear)
- **Spark particles** on transitions and connections
- Every storyboard step must include an "Alive Layer" column
- Full spec locked in `settings.json` under `aliveStandard`

### 1. Text Is Sacred
The text presentation types (math, box, mixed, text, transform) are the Orbital brand. They are LOCKED. Iris doesn't redesign them. They are consistent across every video.

### 2. Build Reusable, Not One-Off
Every new visual type should be designed for reuse. "factorial_cascade" is better than "zero_factorial_video_scene_3". Iris should think about what OTHER videos could use this type.

### 3. Library Grows Monotonically
We only ADD types, never remove working ones. The visual library is an ever-expanding toolkit. After 20 videos, we should have 30+ types. After 50, the pipeline can handle almost any concept without new code.

### 4. Clayton Approves for Library
- Iris + Claudio iterate on the visuals together
- Clayton gives final approval before code goes into scene_short.py
- No code enters the scene library without explicit approval

### 5. Iris Knows the Library
Iris MUST read `visual_library.md` before every brief. The worst outcome is designing something that already exists. The second worst is designing something that's 90% the same as an existing type — just extend the existing one.

## Spawn Commands

```
Iris (Visionary):  sessions_spawn label=orbital-iris model=claude-opus-4-6
```

## Integration with Other Teams

- **Shorts Circle** (Rigby, Vex, Zara, etc.) reviews the SCRIPT and NARRATION
- **Visual Team** (Iris + Claudio) handles the VISUALS
- These are separate concerns — the Circle doesn't design visuals, Iris doesn't write narration
- The script generator (Stage 1) references available visual types from the library

## Files

| File | Purpose |
|------|---------|
| `contracts/visual_library.md` | Catalog of all visual types (Iris reads, Claudio updates) |
| `contracts/visual_team.md` | This contract |
| `scene_short.py` | The scene generator (Claudio's render target) |
| `memory/agents/iris.md` | Iris's full spec |
