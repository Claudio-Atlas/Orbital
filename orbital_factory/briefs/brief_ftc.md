# Visual Brief: Why the Fundamental Theorem of Calculus Works

> **Revised 2026-03-07 — ALIVE PASS** — Every visual breathes, glows, and pulses. Grounded to `settings.json`. AIGENTS-inspired living aesthetic.

## The Core Insight
The area under a curve is an antiderivative because the **rate at which area accumulates** at any point x is exactly f(x) — the function's height IS the speed of area growth, making differentiation and integration natural inverses.

---

## Technical Constants (from settings.json)

| Constant | Value |
|----------|-------|
| Frame | 4.5 × 8.0 (1080×1920, 60fps) |
| mathCenterY | 1.2 |
| graphCenterY | -1.8 |
| mathScale | 0.85 |
| boxScale | 0.65 |
| maxWidthRatio | 0.82 → MAX_WIDTH = 3.69 |
| ANIMATION_RATIO | 0.35 |
| EXTRA_HOLD | 0.5s |
| anim_time formula | `max(1.2, duration × 0.35)` |
| End card | 2.7s (lissajous + ORBITAL wordmark) |
| Border | stroke 2.5, color `#8B5CF6`, opacity 0.7 |
| Glow | stroke 6, opacity 0.15 |

### Colors (LOCKED — settings.json)

| Name | Hex | Usage in this video |
|------|-----|---------------------|
| Violet | `#8B5CF6` | Box borders, glow halos, graph grid lines |
| Cyan | `#22D3EE` | Curve, accumulated area fill, sweeper line, Key Fact text, glow trails |
| Green | `#39FF14` | Strip highlight, punchline text, callouts, reverse sweep, pulse highlights |
| Orange | `#F97316` | Emphasis on "inverse" concept |
| Box Fill | `#1a1130` | Dark box interior |
| Surface | `#0d0a14` | Deep background for overlays |
| End Card Cyan | `#00E5FF` | Lissajous + wordmark |
| Background | `#000000` | Scene background |

### Text Hierarchy (LOCKED — settings.json)

| Tier | Name | Size | Color | Use in this video |
|------|------|------|-------|-------------------|
| 1 | Punchline | 42px | `#39FF14` | FTC formula in green box — the big reveal |
| 2 | Key Fact | 28px | `#22D3EE` | FTC formula first appearance, dA/dx = f(x) |
| 3 | Callout | 24px | `#39FF14` | "The derivative of area IS the function" |
| 4 | Title | 26px | `#8B5CF6` | "This is the most important theorem in calculus" |
| 5 | Equation | 30px | `#FFFFFF` | Intermediate math: A(x) = F(x) + C, etc. |
| 6 | Caption | 24px | `#22D3EE` | Graph labels, strip labels (f(x), dx), A(x) counter |
| 7 | Counter | 22px | — | NOT USED (Tier 6 minimum per text rules) |

### 🔮 ALIVE Constants (AIGENTS-Inspired)

| Effect | Value | Usage |
|--------|-------|-------|
| Glow stroke | 6 (from settings.json `glowStroke`) | Behind every key mobject — formula boxes, curve, sweeper, strips, axes markers |
| Glow opacity | 0.15 (from settings.json `glowOpacity`) | Soft halo layer, always behind the crisp mobject |
| Pulse range | opacity 0.7 ↔ 1.0 | Active elements breathe; `rate_func=there_and_back` over 1.5s |
| Dim state | opacity 0.3–0.4 | Contextual/dormant elements fade back; brightness = attention |
| Bloom flash | 0.2s bright spike (opacity 1.0 + glow 0.35) → settle to glow 0.15 | Key reveal moments: strip pause, dA/dx reveal, FTC formula slam |
| Breathing | scale 1.0 ↔ 1.02, over 3–4s | Background elements (axes, curve, persistent labels) subtly pulse |
| Organic easing | `rate_func=smooth` (default), `ease_in_out_cubic` (movements) | Nothing linear except the sweeper itself (intentionally constant-rate) |
| Spark particles | Dot radius 0.03, opacity 0.6, `MoveAlongPath` over 0.8–1.2s | Travel along sweeper path, formula connections, inverse arrows |
| Area luminance | Fill opacity tracks sweep progress (0.15 → 0.35) | Area gets brighter as it grows — it's ACCUMULATING energy, not just space |

---

## Existing Types to Reuse

| Type | Use Case | Source |
|------|----------|--------|
| `math` | Displaying ∫f(x)dx = F(b)−F(a), area function A(x), dA/dx = f(x) | Brand standard |
| `text` | Hook statement, labels, transition text | Brand standard |
| `box` | Final FTC statement (Tier 1/2 branded box) | Brand standard |
| `graph` | Base function curve f(x) with axes, shaded area | scene_short.py |
| `equation_highlight` | Color-coding dA/dx = f(x) — the punchline equation | scene_short.py |
| `transform` | A(b)−A(a) morphing into ∫f(x)dx = F(b)−F(a) | scene_short.py |

---

## NEW Visual Type #1: `area_accumulator`

### What it shows
A curve f(x) on axes. A vertical "sweeper" line moves from left to right. As it moves, the shaded area behind it grows in real-time. Above the graph (in the math zone at y=1.2), a running label shows A(x) updating. At a key moment, the sweeper pauses and a thin vertical strip is highlighted — its height equals f(x) and its width is dx.

### Motion

1. **The curve is already alive.** It arrived in a prior `graph` step (persisted via `graph_mobs[]`), its cyan stroke already breathing with a glow halo. The axes have faint violet grid lines pulsing at 0.08 opacity. The scene is not static — it's a living canvas waiting for the sweep.

2. **The sweeper awakens.** A vertical dashed line (cyan `#22D3EE`, stroke_width 2) materializes at x = a with a bloom flash — its glow halo (stroke_width=6, cyan, opacity=0.15) flares to 0.3 for 0.2s, then settles to breathing (0.12↔0.18, 2s cycle). A tiny spark dot (radius 0.03, cyan, opacity 0.6) sits at the intersection of the sweeper and the curve, pulsing.

3. **The sweep — area GROWS like a living thing.** The sweeper glides right (`ValueTracker`, `rate_func=linear` — intentionally linear, because accumulation is constant-rate). But the AREA behind it isn't flat — it's luminous. The fill starts at cyan `#22D3EE` opacity 0.15 near x = a and brightens as it grows, reaching 0.35 opacity at x = b. This is NOT uniform fill — it's **area as energy accumulation**. The newer (rightmost) part of the fill is slightly brighter than the older (leftmost) part, creating a gradient-like depth.

   The spark dot at the sweeper-curve intersection rides along, leaving a barely visible **glow trail** (opacity 0.05, fading over 1s) on the curve behind it — the curve is being "activated" by the sweep.

   The A(x) counter at mathCenterY (y=1.2) updates: Tier 6 MathTex `font_size=24`, cyan `#22D3EE`, with a faint cyan glow backing (stroke 6, opacity 0.1). Each time the number ticks up significantly, a micro-bloom (glow → 0.2 for 0.1s) signals the change. The counter breathes (opacity 0.85↔1.0, 2s cycle).

4. **The sweeper PAUSES — the strip moment.** At `pause_at`, the sweeper stops. A brief bloom flash (sweeper glow spikes to 0.3 for 0.15s). The spark dot at the intersection BRIGHTENS (opacity → 1.0, radius → 0.05) and holds — it's marking this moment.

5. **The strip materializes with bloom.** A thin vertical strip at the pause point outlines itself in green `#39FF14` (stroke_width 2), fill green at 0.3 opacity. On appearance: BLOOM FLASH — the strip flares (fill 0.6, glow 0.3 for 0.2s), then settles to its resting state with a breathing glow halo (green, stroke 6, opacity 0.12↔0.18, 1.5s cycle).

   The accumulated area behind the strip DIMS slightly (opacity drops 0.05) — **brightness as attention** shifts to the strip. The sweeper line dims to 0.4 opacity. Everything says: "look HERE."

6. **Braces and labels appear, each alive.** Height brace (green `#39FF14`) writes in on the right side of the strip with `rate_func=smooth`, its own green glow halo (stroke 6, opacity 0.15) appearing simultaneously. Label "f(x)" Tier 6 (`font_size=24`, green) writes in 0.2s after the brace, with a micro-bloom on arrival. A tiny spark travels from the curve intersection point DOWN the brace to the label — showing the connection between the curve height and the label.

   Width brace (white) writes in below the strip, same treatment. Label "dx" Tier 6 (`font_size=24`, white). Spark travels along brace.

7. **The equation crystallizes.** "dA ≈ f(x) · dx" appears at y=1.2 — Tier 5 MathTex (`font_size=30`, white, with "f(x)" colored green via `set_color_by_tex`). Writes in with `rate_func=smooth`. Each colored term has its own glow halo: "f(x)" gets green glow, "dx" stays white. On completion, a BLOOM FLASH on the entire equation (glow 0.15 → 0.3 → 0.15 over 0.3s). **Gradient connection lines** (green → white, stroke 1, opacity 0.2) briefly arc from the strip labels to their corresponding terms in the equation above — then fade to 0.05 over 1s. Living data flows, connecting the visual to the symbolic.

### Timing
- Sweep: ~8s for the full left-to-right sweep (`rate_func=linear`)
- Strip highlight: ~5s for the strip + braces + dA equation
- Total: ~13s

### Colors (all from settings.json)
- Curve: cyan `#22D3EE`, stroke_width 2.5, glow halo cyan stroke 6 opacity 0.15 (BREATHING)
- Accumulated area fill: cyan `#22D3EE` at opacity 0.15→0.35 (luminance gradient)
- Sweeper line: cyan `#22D3EE` DashedLine, stroke_width 2, glow halo stroke 6 opacity 0.15 (BREATHING)
- Spark dot: cyan `#22D3EE`, radius 0.03→0.05 (brightens at pause), opacity 0.6→1.0
- Strip outline: green `#39FF14`, stroke_width 2, glow halo green stroke 6 opacity 0.15 (BREATHING)
- Strip fill: green `#39FF14` at opacity 0.3 (resting), 0.6 (bloom flash)
- Height brace + label: green `#39FF14`, Tier 6 `font_size=24`, glow backing
- Width brace + label: white, Tier 6 `font_size=24`, glow backing
- A(x) label: cyan `#22D3EE`, Tier 6 `font_size=24`, glow backing, micro-blooms on change
- dA equation: white Tier 5, "f(x)" green, glow halos on colored terms
- Connection arcs: green→white gradient, stroke 1, opacity 0.2 → 0.05

### Sizing for portrait frame
- Graph axes sit at graphCenterY = -1.8, using GRAPH_WIDTH = 3.4 and GRAPH_HEIGHT = 2.8
- A(x) label sits at mathCenterY = 1.2
- The strip labels (f(x), dx) must be `font_size=24` (Tier 6) to fit inside the graph zone without clutter
- Braces extend ~0.25 units beyond strip edges

### Alive Layer (persistent effects during this type's screen time)
| Element | Effect | Parameters |
|---------|--------|------------|
| Curve | Glow breathing | halo opacity 0.12↔0.18, 3s cycle |
| Axes/grid | Subtle violet pulse | opacity 0.06↔0.10, 4s cycle |
| Sweeper line | Glow breathing | halo opacity 0.12↔0.18, 2s cycle |
| Spark dot | Pulsing | opacity 0.5↔0.7, radius 0.025↔0.035, 1s cycle |
| Accumulated area | Luminance gradient | newer fill brighter than older fill |
| A(x) counter | Breathing + micro-blooms | opacity 0.85↔1.0, 2s cycle; bloom on change |
| Strip (when present) | Breathing glow | halo 0.12↔0.18, 1.5s cycle |
| Non-active elements | DIM | opacity 0.3–0.4 when strip is focused |

### Reusability: VERY HIGH
- ANY integral concept video: average value, net area, probability density
- Accumulation functions in general
- Can be parameterized for any `expr`, `x_range`, `pause_at` position
- The sweeping fill pattern is the go-to visual for "what integration actually means"

### Config Fields (proposed)
```json
{
  "type": "area_accumulator",
  "expr": "0.5*x**2 + 1",
  "x_range": [0, 4, 1],
  "y_range": [-0.5, 10, 2],
  "a": 0,
  "b": 4,
  "pause_at": 2.5,
  "show_strip": true,
  "show_counter": true,
  "sweep_duration": 8.0,
  "strip_duration": 5.0
}
```

---

## NEW Visual Type #2: `inverse_operation`

### What it shows
Two operations shown as a visual "forward → reverse" cycle. A mathematical object transforms forward (integration: area accumulates under curve), then transforms backward (differentiation: area dissolves, revealing the original function). The forward/reverse creates an "undo" feeling that makes the inverse relationship visceral.

### Motion

1. **Forward pass (Integration) — the area GROWS, luminous and alive.**
   Area under f(x) fills in from left to right — same sweep mechanic as `area_accumulator` but faster (~3s). The fill isn't flat — it breathes as it grows, opacity pulsing 0.25↔0.35 during the sweep. A cyan spark dot rides the sweep front, leaving a fading glow trail on the curve. The entire graph zone feels like it's CHARGING with energy.

   Label "∫f(x)dx" Tier 6 (`font_size=24`, cyan `#22D3EE`) materializes at mathCenterY with a bloom flash (glow 0.15 → 0.3 → 0.15 over 0.3s) and begins breathing (opacity 0.85↔1.0, 2s cycle). Its glow halo (cyan, stroke 6, opacity 0.15) pulses in sync.

2. **Pause + label — the scene holds its breath.**
   "Integration" Tier 4 Title (`font_size=26`, violet `#8B5CF6`, weight=BOLD) appears above the integral label with a violet bloom flash. The accumulated area reaches its peak luminance (opacity 0.35) and the fill begins a slow, deep breathing pulse (0.30↔0.38, 3s cycle) — it's ALIVE, holding all this accumulated energy. The curve's glow halo intensifies to 0.2 opacity. Hold 1.5s. Everything is saturated, charged, waiting.

3. **Reverse pass (Differentiation) — the undo, the unraveling.**
   A green `#39FF14` sweeper line materializes at x = a with a GREEN bloom flash (glow spikes to 0.35, 0.2s). This sweeper is *different* from the forward one — it's thicker (stroke_width 2.5), its glow is brighter (opacity 0.2, breathing), and it carries an AGGRESSIVE spark (green, radius 0.04, opacity 0.8).

   The green sweeper glides right. As it passes each point, the cyan area behind it DISSOLVES — opacity drains to 0 over 0.3 units of horizontal distance, like the green line is *consuming* the area. The dissolution has a subtle effect: tiny cyan spark particles (2–3 dots, radius 0.02, cyan, opacity 0.3) scatter upward from the dissolving edge, like the area's energy being released back into the function.

   At the sweeper's position, a glowing green dot sits ON the curve (radius 0.05, opacity 0.9, with green glow halo stroke 4, opacity 0.2). A green dashed height line drops from the dot to the x-axis (stroke_width 1.5, `#39FF14`, opacity 0.6) — showing that the derivative at this point IS the function's height. The height line has its own faint glow. As the sweeper moves, the dot, height line, and glow all travel together — a living probe reading the function.

   The "Integration" label dims to 0.3 opacity. The ∫f(x)dx label dims to 0.4. Brightness flows to the green elements.

4. **Reveal — the identity crystallizes.**
   After the sweep completes, the area is gone. Only the curve remains, glowing cyan, ALIVE — it was always there under the area, and now it's exposed. The curve's glow halo flares (0.15 → 0.25 → 0.15 over 0.3s) — a rebirth bloom.

   "d/dx" in orange `#F97316` (`font_size=30`) materializes from the left side of the "∫f(x)dx" label, sliding in with `rate_func=ease_in_out_cubic`. The orange text has its own warm glow halo (orange, stroke 6, opacity 0.12). As it arrives next to the integral label, a brief BLOOM — both terms flash (glow spike 0.3, 0.15s).

   Then `TransformMatchingTex` → the whole expression morphs into "f(x)" in green `#39FF14`, Tier 2 Key Fact box. The box materializes with the full treatment: violet border traces with `Create`, glow halo shimmers ahead of the line, boxFill pools behind, green text writes in, BLOOM on completion. The transformation has spark particles — 3–4 tiny dots that arc from the old expression's position to the new box, tracing the metamorphosis.

5. **Label — the punchline lands.**
   "Differentiation" Tier 4 Title (`font_size=26`, violet) appears with a bloom, then transforms (via `TransformMatchingTex`) into "= INVERSE" as green Tier 3 callout (`font_size=24`, `#39FF14`, weight=BOLD). The green text gets a bloom flash and begins breathing. A **gradient connection line** (orange→green, stroke 1, opacity 0.2) arcs between "d/dx" position and the "INVERSE" label, showing the conceptual link — then fades to 0.05 over 1.5s.

### Timing
- Forward pass: ~3s
- Pause: ~1.5s
- Reverse pass: ~4s
- Reveal + label: ~3s
- Total: ~11.5s

### Colors (all from settings.json)
- Forward sweep area: cyan `#22D3EE` at opacity 0.25→0.35 (luminance gradient, breathing 0.30↔0.38)
- Forward sweeper + spark: cyan `#22D3EE`, stroke_width 2, spark dot 0.03
- "Integration" label: violet `#8B5CF6`, Tier 4, with violet glow halo
- Reverse sweeper: green `#39FF14`, stroke_width 2.5, glow halo 0.2 (BRIGHTER than forward)
- Reverse spark: green `#39FF14`, radius 0.04, opacity 0.8
- Dissolution particles: cyan `#22D3EE`, radius 0.02, opacity 0.3, scatter upward
- Height line + dot: green `#39FF14`, DashedLine stroke 1.5, dot radius 0.05, glow halo
- "d/dx" prefix: orange `#F97316`, glow halo orange stroke 6 opacity 0.12
- Final "f(x)": green `#39FF14`, Tier 2 box, full bloom treatment
- "INVERSE" label: green `#39FF14`, Tier 3 callout, bloom + breathing
- Connection arcs: orange→green gradient, stroke 1, opacity 0.2→0.05

### Alive Layer (persistent effects during this type's screen time)
| Element | Effect | Parameters |
|---------|--------|------------|
| Curve | Glow breathing (intensifies during pause) | halo 0.12↔0.18 → 0.18↔0.25 during charge |
| Accumulated area | Breathing luminance | 0.30↔0.38, 3s cycle (during pause hold) |
| Forward sweeper | Glow breathing | 0.12↔0.18, 2s cycle |
| Reverse sweeper | BRIGHTER glow breathing | 0.18↔0.25, 1.5s cycle |
| Height line (during reverse) | Subtle pulse | opacity 0.5↔0.7, 1s cycle |
| Probe dot (during reverse) | Pulsing glow | radius 0.04↔0.06, 1s cycle |
| Dissolution particles | Upward scatter | 2–3 cyan dots per x-unit dissolved |
| "Integration" label | DIM during reverse | fades to 0.3 opacity |
| All non-active labels | DIM | 0.3–0.4 opacity when attention is elsewhere |

### Reusability: HIGH
- ANY inverse operation pair: exponent/logarithm, square/square-root, encode/decode
- Chain rule motivation ("undoing" nested functions)
- Can be parameterized with `forward_label`, `reverse_label`, `expr`, `forward_color`, `reverse_color`
- The "forward/reverse sweep" pattern is distinctive and not in the current library

### Config Fields (proposed)
```json
{
  "type": "inverse_operation",
  "expr": "0.5*x**2 + 1",
  "x_range": [0, 4, 1],
  "y_range": [-0.5, 10, 2],
  "forward_label": "\\int f(x)\\,dx",
  "reverse_label": "\\frac{d}{dx}",
  "result_label": "f(x)",
  "forward_duration": 3.0,
  "reverse_duration": 4.0,
  "duration": 11.5
}
```

---

## Step-by-Step Visual Storyboard

| Step | Time | Duration | Visual Type | Tier | What's On Screen | Motion/Animation | Alive Layer |
|------|------|----------|-------------|------|------------------|-----------------|-------------|
| 1 | 0.0–4.0s | 4.0s | `text` | 4 | "This is the most important theorem in calculus." | Write animation (`rate_func=smooth`), Tier 4 Title, `font_size=26`, violet `#8B5CF6`, weight=BOLD, centered at y=1.2. The text arrives trailing a faint violet glow halo (stroke 6, opacity 0.12) that shimmers as each word materializes. On "most important" — a brief brightness spike (white flash 0.1s, then back to violet). | **Glow**: violet halo 0.12 breathing behind text. **Bloom**: "most important" fires white for 0.1s. **Breathing**: text opacity 0.9↔1.0, 2s cycle. |
| 2 | 4.5–9.0s | 4.5s | `math` | 2 | $\int_a^b f(x)\,dx = F(b) - F(a)$ | Tier 2 Key Fact box materializes: violet border traces with `Create` (`rate_func=smooth`), glow halo (violet, stroke 6, opacity 0.15) shimmers ahead of the tracing line. BoxFill `#1a1130` opacity 0.6 pools into the interior. Formula writes in cyan `#22D3EE`. BLOOM on completion — entire box glow spikes to 0.3 for 0.2s, then settles to breathing (0.12↔0.18, 3s cycle). | **Glow**: violet border halo, breathing. **Bloom**: completion flash. **Breathing**: box glow 0.12↔0.18. This formula is the destination — it should feel *important* even before we explain it. |
| 3 | 9.5–13.0s | 3.5s | `text` | 3 | "Why does AREA have anything to do with ANTIDERIVATIVES?" | Tier 3 Callout, `font_size=24`, green `#39FF14`, weight=BOLD, centered at y=1.2. Green glow halo breathing. On "AREA" — brief cyan flash (0.1s, the area color), foreshadowing the visual. On "ANTIDERIVATIVES" — brief orange flash (0.1s, `#F97316`), foreshadowing the inverse reveal. These micro-blooms plant subconscious color associations. | **Glow**: green halo breathing. **Blooms**: "AREA" flashes cyan, "ANTIDERIVATIVES" flashes orange — color foreshadowing. |
| 4 | 13.5–17.5s | 4.0s | `graph` | — | Curve f(x) = 0.5x² + 1 on axes, x ∈ [0, 4] | FadeIn axes with violet grid lines (opacity 0.08, with subtle breathing pulse 0.06↔0.10, 4s cycle). Then the curve TRACES itself left-to-right — cyan `#22D3EE` stroke with a BRIGHT spark dot (radius 0.04, cyan, opacity 0.8) riding the leading edge, leaving the glow halo (stroke 6, cyan, opacity 0.15) behind it. The curve feels like it's being *drawn by light*. Axes at graphCenterY=-1.8. | **Glow**: curve glow halo breathes (0.12↔0.18, 3s). **Spark**: riding dot traces the curve. **Grid**: violet pulse 0.06↔0.10. The graph is ALIVE from the moment it appears. |
| 5 | 18.0–21.5s | 3.5s | `graph` (shaded_area) | 6 | Same curve, area from 0 to ~2 shaded in cyan `#22D3EE` opacity 0.2 | Shaded region grows from left edge — not a flat FadeIn, but a left-to-right FILL that takes 1.2s (`rate_func=smooth`), like the area is pouring in. Fill opacity 0.2 with a faint luminance gradient (left dimmer, right brighter). Tier 6 label "A(x)" (`font_size=24`, cyan, glow backing) materializes at y=1.2 with a bloom flash. The filled area begins subtle breathing (opacity 0.18↔0.22, 3s cycle). | **Glow**: A(x) label has cyan glow backing. **Luminance**: left-to-right brightness gradient in fill. **Breathing**: area fill pulses, curve halo pulses. **Bloom**: A(x) label arrival flash. |
| 6 | 22.0–30.0s | 8.0s | `area_accumulator` (sweep) | 6 | Sweeper line moves right, area fills in real-time, A(x) counter updates at y=1.2 | Sweeper materializes at x=0.5 with bloom flash. `ValueTracker` drives sweep from x=0.5 to x=3.5 (`rate_func=linear`). Area luminance gradient — newer fill brighter. Spark dot rides sweeper-curve intersection, leaving glow trail on curve. A(x) counter at y=1.2 updates with micro-blooms on significant changes. Counter breathes (0.85↔1.0). The whole graph zone feels like it's ACCUMULATING energy. | **Glow**: sweeper halo breathing (0.12↔0.18). **Spark**: riding dot with trail. **Luminance**: area brightness increases with accumulation. **Counter**: breathing + micro-blooms. **Grid**: faint violet breathing throughout. |
| 7 | 30.5–35.5s | 5.0s | `area_accumulator` (strip) | 5/6 | Sweeper pauses at x≈2.5. Green strip highlighted with bloom. Labels with glowing braces. dA equation with gradient connections. | Sweeper stops → bloom flash (glow spike 0.3). Spark dot BRIGHTENS (opacity 1.0, radius 0.05). Strip materializes green with BLOOM (fill 0.6 glow 0.3 → settle). Accumulated area DIMS (attention shift). Height brace + "f(x)" with green glow + spark along brace. Width brace + "dx" with white glow + spark. "dA ≈ f(x)·dx" writes in at y=1.2, colored terms have glow halos, BLOOM on complete. Gradient connection arcs (green→white) from strip labels to equation terms, fading. | **Bloom**: strip appearance, equation completion. **Activation**: strip BRIGHT, area DIMS. **Sparks**: along braces, connection arcs. **Glow**: green halos on strip/braces, per-term halos in equation. **Breathing**: strip glow 0.12↔0.18. |
| 8 | 36.0–41.0s | 5.0s | `math` | 2 | $\frac{dA}{dx} = f(x)$ | FadeOut graph — glow halo lingers 0.2s after solid fades (the ghost of the visual). Write at y=1.2 in Tier 2 Key Fact box. Violet border traces with glow shimmer. "f(x)" colored green `#39FF14` via set_color_by_tex, with its own green glow halo. "dA/dx" gets cyan glow halo. BLOOM on completion. The equals sign pulses (opacity 0.7↔1.0, 1.5s) — the living bridge between the derivative and the function. | **Lingering glow**: graph glow outlasts solid on fadeout. **Glow**: per-term halos (cyan on dA/dx, green on f(x)). **Bloom**: box completion flash. **Pulse**: equals sign breathing. **Breathing**: box glow 0.12↔0.18. |
| 9 | 41.5–46.0s | 4.5s | `equation_highlight` | — | Same equation. "dA/dx" pulses cyan `#22D3EE`, "f(x)" pulses green `#39FF14` | Indicate animation on left part (cyan), then right part (green). When one activates: its glow halo FLARES (opacity → 0.35, scale 1.0 → 1.05), the OTHER term DIMS to 0.4. Tiny spark particles (2 dots each) orbit the active term during its flash. Gradient connection line (cyan↔green, stroke 1, opacity 0.15) pulses between the two terms — they're LINKED, they're the SAME THING. Permanent color set after. | **Activation**: flaring glow + scale pop, other term dims. **Sparks**: orbiting dots. **Connection**: gradient line pulses between linked terms. **This is the visual punchline** — the equation IS the connection. |
| 10 | 46.5–58.0s | 11.5s | `inverse_operation` | 4/2/3 | Forward: area fills under f(x), luminous and breathing. Reverse: green sweep dissolves area with cyan particles scattering upward, height probe reads curve. d/dx + ∫ → f(x) with spark metamorphosis. "= INVERSE" bloom. | See full `inverse_operation` motion spec above. Every phase has its own alive layer: Forward = charging energy. Pause = held breath. Reverse = controlled unraveling with particle release. Reveal = rebirth bloom. This is the HERO SEQUENCE — 11.5s of pure visual storytelling. | **Everything in the inverse_operation alive layer table applies.** Key moments: area breathing during pause, dissolution sparks, height probe pulsing, rebirth bloom on curve after area dissolves, metamorphosis sparks during transform. |
| 11 | 58.5–62.5s | 4.0s | `math` | 5 | $A(b) - A(a) = F(b) - F(a)$ — C cancels | Write equation with term-specific glow halos. C terms appear dimmer (0.6 opacity, no glow) — they're already marked for death. Red `#FF4444` diagonal strikes cross out C's with `rate_func=rush_into` — each strike has a red bloom flash (0.15s) and 2 red sparks scattering. C terms FadeOut (the strikes linger 0.3s, then follow). Remaining terms BRIGHTEN — glow halos flare briefly. | **Dim**: C terms arrive dim (foreshadowing). **Bloom**: red flash on each strike. **Sparks**: red scatter from C death. **Activation**: survivors brighten after C removal. |
| 12 | 63.0–67.0s | 4.0s | `transform` | 1 | $A(b) - A(a)$ morphs into $\int_a^b f(x)\,dx = F(b) - F(a)$ | `TransformMatchingTex` — left side transforms from subtraction to integral. During the morph, spark particles (4–5 dots) trace arcs between old positions and new, showing the metamorphosis. Result appears as Tier 1 Punchline box (`font_size=42`, green `#39FF14`, violet border), materializing with full treatment: border traces with glow shimmer, fill pools, text writes, BLOOM on completion (glow 0.15→0.35→0.15, 0.3s). | **Sparks**: metamorphosis trails during transform. **Bloom**: Tier 1 box completion flash. **Glow**: violet border halo breathing. **This is the BIG REVEAL** — maximum visual impact. |
| 13 | 67.5–72.0s | 4.5s | `box` | 1 | **Fundamental Theorem of Calculus** — $\int_a^b f(x)\,dx = F(b) - F(a)$ | Tier 1 Punchline: `font_size=42`, green `#39FF14`, violet border `#8B5CF6` stroke 2.5, boxFill `#1a1130` opacity 0.6, glow stroke 6 opacity 0.15. If arriving fresh (not persisted from step 12): full materialization with border trace + glow shimmer + bloom. Label "FTC" above in cyan `#22D3EE` `font_size=14`, with cyan glow backing. The box BREATHES — glow 0.12↔0.20 (slightly more alive than usual, this is THE theorem). Scale 1.0↔1.01, 3s cycle. | **Glow**: violet halo 0.12↔0.20 (wider range = more alive). **Breathing**: box glow + subtle scale. **Label glow**: cyan halo on "FTC". **This box should feel like it's RADIATING importance.** |
| 14 | 72.5–76.0s | 3.5s | `text` | 3 | "The derivative of area IS the function." | Tier 3 Callout: `font_size=24`, green `#39FF14`, weight=BOLD, centered at y=1.2. Green glow halo (stroke 6, opacity 0.15) breathing behind. On "IS" — a bright bloom flash (white spike 0.15s, then green) emphasizing the identity. On "area" — brief cyan flash callback. On "function" — brief green intensification. These micro-blooms create a three-beat rhythm in the text that matches the spoken emphasis. | **Glow**: green halo breathing. **Blooms**: three-beat rhythm — "area" (cyan), "IS" (white flash), "function" (green intensify). **Breathing**: text 0.9↔1.0. **This is the screenshot line** — it needs to look ALIVE in a still frame too. |
| EC | 76.5–79.2s | 2.7s | `end_card` | — | Lissajous curve (`#00E5FF`, A=1.2, B=0.95, sin(2t)/sin(3t)) + "ORBITAL" wordmark (`#00E5FF`, 22px, BOLD) + "Watch it click." (14px, white, 0.5 opacity). No CTA, no handle. | Create lissajous core (stroke 2) 0.8s — the curve traces itself with a bright spark dot riding the pen. Glow halo (stroke 8, opacity 0.2) fades in 0.6s behind. The lissajous begins BREATHING — scale 1.0↔1.02 over 3s cycle, glow 0.15↔0.25 over 2s cycle. FadeIn wordmark (cyan glow backing) + tagline 0.4s → hold 1.2s → FadeOut 0.3s. The lissajous is the last living thing on screen. | Standard end card per settings.json — but the lissajous BREATHES and GLOWS. |

### Total Duration: ~79.2s (content: ~76.5s + end card: 2.7s)

---

## Timing Model Verification

Every step follows the proven model:
1. Build mobject (NO timeline cost)
2. `self.add_sound(audio_path)` — audio starts HERE
3. `FadeOut(previous, 0.4s)` — voice plays over fadeout
4. `Write(new, anim_time)` where `anim_time = max(1.2, duration × 0.35)`
5. `self.wait(duration − anim_time)` — hold until voice done
6. `self.wait(0.5)` — EXTRA_HOLD breathing room

Audio is embedded via `self.add_sound()`, NOT post-mixed. Music (bg_synthwave.mp3, volume 0.12) plays through entire video including end card, mixed via ffmpeg post-render.

**Duration note:** At ~79s this exceeds the 75s soft target but stays under the 2min hard max. The FTC deserves depth — it IS "the most important theorem in calculus." If tightening is needed, steps 11–12 (C cancellation + transform) can be compressed into one 5s step instead of two.

---

## Technical Notes for Claudio

### 🔮 ALIVE Effects — Manim Implementation Guide

#### Glow Layers (the foundation of everything)
Every key mobject needs TWO copies: the glow layer and the crisp layer.
```python
# Pattern: glow behind, crisp on top
crisp_curve = axes.plot(fn, x_range=[0, 4], color="#22D3EE", stroke_width=2.5)
glow_curve = crisp_curve.copy().set_stroke(
    color="#22D3EE", width=6, opacity=0.15  # settings.json: glowStroke=6, glowOpacity=0.15
)
curve_group = VGroup(glow_curve, crisp_curve)  # glow BEHIND crisp
```

#### Breathing / Pulsing (the heartbeat)
Use `add_updater` for continuous breathing that persists throughout the element's life:
```python
breath_tracker = ValueTracker(0)
def glow_breathing(mob, dt):
    t = breath_tracker.get_value()
    # Oscillate glow opacity: 0.12 ↔ 0.18, period 3s
    opacity = 0.15 + 0.03 * np.sin(2 * PI * t / 3.0)
    mob.set_stroke(opacity=opacity)
    breath_tracker.increment_value(dt)
glow_curve.add_updater(glow_breathing)
```
For scale breathing (boxes, the lissajous):
```python
original_center = box.get_center()
def scale_breath(mob, dt):
    t = breath_tracker.get_value()
    scale_factor = 1.0 + 0.015 * np.sin(2 * PI * t / 4.0)  # ±1.5%, 4s cycle
    mob.become(mob.copy().scale(scale_factor).move_to(original_center))
```

#### Bloom Flash (the "oh!" moment)
```python
# Brief bright spike on a key reveal
def bloom(glow_mob, duration=0.2, peak_opacity=0.35, rest_opacity=0.15):
    return Succession(
        glow_mob.animate(run_time=duration*0.4, rate_func=rush_into).set_stroke(opacity=peak_opacity),
        glow_mob.animate(run_time=duration*0.6, rate_func=rush_from).set_stroke(opacity=rest_opacity),
    )
```
Use bloom at: strip appearance, box completion, formula reveal, sweep start/pause, corner death.

#### Spark Particles (living connections)
```python
# Spark that rides along a path and fades
spark = Dot(radius=0.03, color="#22D3EE", fill_opacity=0.6)
spark.move_to(path.get_start())
self.play(
    MoveAlongPath(spark, path, run_time=0.8, rate_func=smooth),
    spark.animate(run_time=0.8).set_opacity(0),
)
```
For the sweeper riding dot (persistent spark):
```python
riding_dot = Dot(radius=0.03, color="#22D3EE", fill_opacity=0.6)
riding_dot.add_updater(lambda m: m.move_to(
    axes.c2p(x_tracker.get_value(), fn(x_tracker.get_value()))
))
```
For dissolution particles (during inverse_operation reverse sweep):
```python
# Scatter cyan dots upward as area dissolves
def spawn_dissolution_particle(x_pos, axes, fn):
    p = Dot(radius=0.02, color="#22D3EE", fill_opacity=0.3)
    p.move_to(axes.c2p(x_pos, fn(x_pos) * 0.5))  # mid-height of area
    target = axes.c2p(x_pos, fn(x_pos) + 0.5)  # scatter upward
    return Succession(
        FadeIn(p, run_time=0.1),
        p.animate(run_time=0.5, rate_func=rush_from).move_to(target).set_opacity(0),
    )
```

#### Brightness as Meaning (AIGENTS activation pattern)
```python
# When focusing on the strip, dim the accumulated area
def shift_attention(active, dimmed, bright_opacity=1.0, dim_opacity=0.3):
    return AnimationGroup(
        active.animate(run_time=0.3, rate_func=smooth).set_opacity(bright_opacity),
        *[mob.animate(run_time=0.3, rate_func=smooth).set_opacity(dim_opacity) for mob in dimmed],
        lag_ratio=0
    )
```

#### Gradient Connection Lines (living data flows)
```python
# Arc connecting a visual element to its symbolic representation
connection = ArcBetweenPoints(
    strip_label.get_center(),
    equation_term.get_center(),
    angle=PI/6
)
connection.set_color(color=["#39FF14", "#FFFFFF"])  # gradient
connection.set_stroke(width=1, opacity=0.2)
self.play(Create(connection, run_time=0.5, rate_func=smooth))
self.play(connection.animate(run_time=1.0).set_opacity(0.05))  # fade to trace
```

#### Luminance Gradient on Area Fill
```python
# Area that gets brighter as it accumulates (newer = brighter)
# Approach: overlay multiple thin vertical strips at increasing opacity
# OR: use a single area with opacity driven by x_tracker position
area = always_redraw(lambda: axes.get_area(
    curve,
    x_range=[a, x_tracker.get_value()],
    color="#22D3EE",
    opacity=0.15 + 0.20 * (x_tracker.get_value() - a) / (b - a)  # 0.15 → 0.35
))
```

#### Lingering Glow on FadeOut
When fading out a glowing element, the glow should outlast the solid:
```python
self.play(
    FadeOut(crisp_mob, run_time=0.4, rate_func=smooth),
    FadeOut(glow_mob, run_time=0.6, rate_func=smooth),  # lingers 0.2s
)
```

#### Organic Easing Summary
| Context | Rate Function |
|---------|--------------|
| Default (FadeIn/FadeOut/Write) | `rate_func=smooth` |
| Movement/sliding | `rate_func=ease_in_out_cubic` (or `smooth`) |
| Strikes/slams/impacts | `rate_func=rush_into` |
| Pulsing loops | `rate_func=there_and_back` |
| Continuous sweep (accumulator) | `rate_func=linear` (intentional — accumulation IS constant-rate) |
| Settling after bloom | `rate_func=rush_from` |
| **NEVER** | `rate_func=linear` for any non-sweep animation |

### Building `area_accumulator`
Core approach using `always_redraw` + `ValueTracker`:
```python
x_tracker = ValueTracker(a)
area = always_redraw(lambda: axes.get_area(
    curve, x_range=[a, x_tracker.get_value()], color="#22D3EE",
    opacity=0.15 + 0.20 * (x_tracker.get_value() - a) / (b - a)
))
sweeper = always_redraw(lambda: DashedLine(
    axes.c2p(x_tracker.get_value(), y_range[0]),
    axes.c2p(x_tracker.get_value(), fn(x_tracker.get_value())),
    color="#22D3EE", stroke_width=2
))
sweeper_glow = always_redraw(lambda: DashedLine(
    axes.c2p(x_tracker.get_value(), y_range[0]),
    axes.c2p(x_tracker.get_value(), fn(x_tracker.get_value())),
    color="#22D3EE", stroke_width=6, stroke_opacity=0.15
))
riding_dot = always_redraw(lambda: Dot(
    axes.c2p(x_tracker.get_value(), fn(x_tracker.get_value())),
    radius=0.03, color="#22D3EE", fill_opacity=0.6
))
self.play(x_tracker.animate.set_value(b), run_time=sweep_duration, rate_func=linear)
```
- **Strip highlight** is a separate phase after the sweep pauses. Draw a narrow `Rectangle` at the paused x, height matching `fn(pause_at)`, width ~0.15 units (in axes coordinates). Give it a glow twin.
- **Graph persistence:** Uses `graph_mobs[]` pattern — store axes/curve from step 4 so `area_accumulator` can reference them.
- **A(x) counter:** `always_redraw` MathTex at y=1.2 showing numeric area value, with glow backing and micro-bloom updater.

### Building `inverse_operation`
- **Forward pass:** Same area fill as `area_accumulator` but faster (3s). Can reuse the ValueTracker sweep. Area breathes during the pause.
- **Reverse pass:** A SECOND ValueTracker sweeps left-to-right with a green line. Where it passes, area opacity → 0. Implement via `UpdateFromAlphaFunc` moving the green line and fading area opacity simultaneously. Spawn dissolution particles at intervals (every ~0.5 units of sweep progress).
- **The "d/dx" label animation:** `MathTex("\\frac{d}{dx}")` in orange slides in from the left with `rate_func=ease_in_out_cubic`. Bloom on arrival. Then `TransformMatchingTex` to morph the whole expression.
- **Metamorphosis sparks:** During `TransformMatchingTex`, spawn 4–5 dots at old positions that arc to new positions in parallel with the transform.

### Transform chain (steps 11–12)
- Use `TransformMatchingTex` for cleanest morphs.
- Step 11: Show A(x) = F(x) + C, then A(b) − A(a) = [F(b)+C] − [F(a)+C]. C terms appear DIM (0.6 opacity, no glow — already foreshadowing their irrelevance). Cross out with red strikes + bloom + sparks. Survivors brighten.
- Step 12: `TransformMatchingTex` from A(b)−A(a) = F(b)−F(a) to ∫ₐᵇf(x)dx = F(b)−F(a), with metamorphosis spark trails.
- **Alternative (simpler):** Skip transforms, just do Write/FadeOut sequences. Transforms on integral signs can be finicky. Claudio's call.

### Function choice
f(x) = 0.5x² + 1 on [0, 4] because:
- Always positive — no sign confusion
- Curves upward — "area growing faster" is visible (and the luminance gradient amplifies this)
- Antiderivative F(x) = x³/6 + x is clean
- The +1 ensures visible strip height at any x
- Max value ~9 fits within y_range [-0.5, 10, 2]

### Muted viewer check
- Step 2 (FTC formula): On screen, large, readable in Tier 2 box, GLOWING — commands attention without audio
- Steps 6–7 (accumulator sweep + strip): Colors + glow + luminance gradient tell the story — cyan area growing BRIGHTER, green strip BLOOMING with labeled braces. Self-explanatory.
- Step 8 (dA/dx = f(x)): Punchline equation — large, centered, color-coded terms with individual glow halos
- Step 10 (inverse_operation): Forward/reverse sweep is visually intuitive — you can SEE integration being built and undone. The dissolution particles ADD to the silent story.
- Step 13 (Tier 1 box): Final FTC formula, large, BREATHING, RADIATING — unmissable
- Step 14 (green callout): Sticky one-liner, green glow, screenshot-ready with alive micro-blooms

### Portrait framing notes
- Graph at graphCenterY = -1.8. Math at mathCenterY = 1.2. ~3 units of vertical separation.
- During accumulator sweep (steps 6–7): A(x) label at y=1.2 (mathCenterY), graph below at y=-1.8. Clean separation. Glow halos add ~0.15 units; accounted for.
- During `inverse_operation` (step 10): This type needs full-screen attention. FadeOut any math at y=1.2 first (glow lingers). The graph can be centered (y≈-0.5) since it's the hero visual, with labels positioned above.
- Strip labels (`font_size=24`, Tier 6) fit within the graph zone. Braces need ~0.25 unit clearance.
- **Glow halos add visual width** — account for ~0.15 extra units on each side when positioning near MAX_WIDTH.
