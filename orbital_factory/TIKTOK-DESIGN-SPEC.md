# TikTok Short-Form Design Spec
*Established: 2026-03-03 | Reference: 3Blue1Brown Shorts layout*

---

## Screen Dimensions
- **Resolution:** 1080 × 1920 (9:16)
- **Frame rate:** 60fps
- **Duration target:** 30-60 seconds

## TikTok Safe Zones (content-free areas)

```
┌──────────────────────┐
│  ░░░░░░░░░░░░░░░░░░  │ ← Top 10%: Status bar, account name
│                      │
│                      │
│  CONTENT SAFE ZONE   │
│                      │
│                      │
│               [♥]    │ ← Right 15%: Like/Comment/Share buttons
│               [💬]    │    (from ~40% to ~75% down)
│               [↗]    │
│                      │
│  ░░░░░░░░░░░░░░░░░░  │ ← Bottom 15%: Caption, sound, username
└──────────────────────┘
```

**Safe content area:** 
- Horizontal: left 5% to right 80% (leave room for TikTok buttons on right)
- Vertical: top 12% to bottom 82%
- In Manim units (~8 wide × ~14.2 tall frame): 
  - X: -3.0 to +2.5 (shifted slightly left to avoid right-side buttons)
  - Y: -5.0 to +5.5

## Layout Zones (3B1B-inspired)

```
┌──────────────────────┐
│                      │
│   HOOK TEXT / CONTEXT │ ← Zone A: Top 15% of safe area
│   (1-2 lines, white) │    Small text, problem setup
│                      │
│ ──────────────────── │
│                      │
│   MATH / EQUATIONS   │ ← Zone B: Middle 25% of safe area  
│   (color-coded)      │    Steps appear here, build mode
│   f'(x) = 6x + 2    │    ~60-65% screen width MAX
│                      │
│ ──────────────────── │
│                      │
│   ┌──────────────┐   │
│   │              │   │
│   │   GRAPH /    │   │ ← Zone C: Bottom 50% of safe area
│   │   VISUAL     │   │    THE DOMINANT ELEMENT
│   │              │   │    Graph, 3D surface, animation
│   │              │   │
│   └──────────────┘   │
│                      │
└──────────────────────┘
```

### Zone A — Context (Top)
- **Content:** Hook text, problem statement, brief context
- **Font:** White, 28-32px equivalent in Manim
- **Position:** Y = +4.5 to +5.5 (Manim coords)
- **Max lines:** 2
- **Alignment:** Left or center

### Zone B — Math Work (Middle)
- **Content:** Equations, algebraic steps, key rules
- **Font:** White with color accents, 36-42px equivalent
- **Position:** Y = +1.0 to +3.5
- **Max width:** 65% of frame (~5.2 Manim units)
- **Build mode:** Dependent steps accumulate (max 3 lines), then collapse into result
- **Replace mode:** Independent steps fade in/out one at a time

### Zone C — Visual (Bottom, DOMINANT)
- **Content:** Function graph, tangent line, 3D surface, area shading
- **Position:** Y = -5.0 to +0.5 (takes up ~40% of vertical space)
- **Scale:** As large as possible while fitting width
- **Priority:** THIS is what stops the scroll. Math supports the visual, not vice versa.

## Color Palette

| Element | Color | Hex |
|---------|-------|-----|
| Background | Pure black | #000000 |
| Primary text | White | #FFFFFF |
| Function curve | Orbital Cyan | #22D3EE |
| Derivative/tangent | Neon Green | #39FF14 |
| Key rule box | Orbital Violet | #8B5CF6 |
| Box fill | Dark purple | #1a1130 |
| Highlighted terms | Orange | #F97316 |
| Error/caution | Pink | #EC4899 |
| Axis/grid | Dim gray | #333333 |

## Typography Rules
- Math equations: **60-65% of screen width max** — breathing room on sides
- Color-code variables when showing multiple terms (each term gets its own color)
- Key formulas in violet boxes with dark fill
- Plain text in white, smaller than math
- Never use more than 2 sizes on screen at once

## Animation Flow (Derivative Example)

| Time | Zone A (Top) | Zone B (Middle) | Zone C (Bottom) | Voice |
|------|-------------|-----------------|-----------------|-------|
| 0-2s | "solve this 👇" | — | Graph of f(x) fades in | — |
| 2-5s | — | f(x) = 3x² + 2x - 5 | Tangent line appears | "Find the derivative" |
| 5-7s | — | Power Rule box | Graph stays | "Power rule — bring down, subtract one" |
| 7-10s | — | 3x² → 6x (line 1) | Graph stays | "3 times 2 gives us 6x" |
| 10-12s | — | 2x → 2 (line 2, builds) | Graph stays | "2x becomes just 2" |
| 12-14s | — | -5 → 0 (line 3, builds) | Graph stays | "Constant drops off" |
| 14-18s | — | Lines collapse → f'(x) = 6x + 2 | Graph stays | "Combine: 6x plus 2" |
| 18-25s | — | Answer boxed | Derivative line appears | "That's the slope at any x" |
| 25-28s | — | — | Tangent slides along curve | "Watch it match" |
| 28-30s | — | ORBITAL | — | — |

## Build vs Replace Logic

**Use BUILD mode when:**
- Steps are algebraically dependent (term-by-term derivative)
- Showing a running calculation
- Building up to a final result
- Max 3 lines, then collapse/transform into result

**Use REPLACE mode when:**
- Moving to a new concept (problem → rule → work → answer)
- Showing a graph after equations
- Switching between visual and algebra

## Voice Profile
- **Voice:** Allison TikTok (see `voice_profiles/allison_tiktok.json`)
- **Tone:** Warm, confident, slightly playful. "Cool TA" energy.
- **Pacing:** 0.85x speed (slightly slower than normal)
- **Lines:** 1 sentence max per step. Teach, don't lecture.

## Branding
- **Intro:** Orbital logo (planet + ring) — 2 seconds max, with hook overlay
- **Watermark:** "ORBITAL" small, bottom-right corner, 40% opacity
- **Outro:** 2 seconds, logo centered, "Follow for more" below
- **No heavy branding during content** — the quality IS the brand

## Key Principles
1. **The visual stops the scroll.** Graph/animation is the hero, not the equation.
2. **Math supports the visual.** Equations explain what you're seeing, not the other way around.
3. **60-65% width rule.** Nothing wider. Breathing room = professional.
4. **Build dependent, replace independent.** Mimic how a real tutor writes on a board.
5. **Color-code everything.** Each term, function, or concept gets its own color.
6. **Respect TikTok UI.** Don't put content where buttons go.

---

*This spec should be the source of truth for all TikTok renders. Update as we learn what works.*
