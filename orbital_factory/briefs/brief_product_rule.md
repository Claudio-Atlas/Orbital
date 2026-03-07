# Visual Brief: Why the Product Rule ISN'T Random (Visual Proof)

> **Revised 2026-03-07 — ALIVE PASS** — Every visual breathes, glows, and pulses. Grounded to `settings.json`. AIGENTS-inspired living aesthetic.

## The Core Insight
The derivative of f·g measures how a **rectangle's area changes** — two strips grow (f'g and fg'), and the tiny corner square vanishes as dx→0, which is why the formula has two terms, not one.

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
| Violet | `#8B5CF6` | Box borders, glow halos, branded elements |
| Cyan | `#22D3EE` | Right strip (f'g term), curve color, labels, glow trails |
| Green | `#39FF14` | Top strip (fg' term), punchline text, callouts, pulse highlights |
| Orange | `#F97316` | Wrong formula emphasis |
| Box Fill | `#1a1130` | Dark box interior |
| Surface | `#0d0a14` | Deep background for overlays |
| End Card Cyan | `#00E5FF` | Lissajous + wordmark |
| Background | `#000000` | Scene background |
| Red (error) | `#FF4444` | Corner square, wrong answer X |

### Text Hierarchy (LOCKED — settings.json)

| Tier | Name | Size | Color | Use in this video |
|------|------|------|-------|-------------------|
| 1 | Punchline | 42px | `#39FF14` | Final product rule reveal in green box |
| 2 | Key Fact | 28px | `#22D3EE` | Product rule formula (theorem) |
| 3 | Callout | 24px | `#39FF14` | "That's just GEOMETRY" tagline |
| 4 | Title | 26px | `#8B5CF6` | "Think about AREA." transition |
| 5 | Equation | 30px | `#FFFFFF` | Wrong formula, intermediate math |
| 6 | Caption | 24px | `#22D3EE` | Rectangle side labels, strip labels |
| 7 | Counter | 22px | — | NOT USED |

### 🔮 ALIVE Constants (AIGENTS-Inspired)

| Effect | Value | Usage |
|--------|-------|-------|
| Glow stroke | 6 (from settings.json `glowStroke`) | Behind every key mobject — formula boxes, rectangle edges, strips, braces |
| Glow opacity | 0.15 (from settings.json `glowOpacity`) | Soft halo layer, always behind the crisp mobject |
| Pulse range | opacity 0.7 ↔ 1.0 | Active elements breathe; `rate_func=there_and_back` over 1.5s |
| Dim state | opacity 0.3–0.4 | Contextual/dormant elements fade back; brightness = attention |
| Bloom flash | 0.2s bright spike (opacity 1.0 + glow 0.35) → settle to glow 0.15 | Key reveal moments: corner vanish, formula slam, strip appearance |
| Breathing | scale 1.0 ↔ 1.02, over 3–4s | Background elements (rectangle outline, persistent labels) subtly pulse |
| Organic easing | `rate_func=smooth` (default), `ease_in_out_cubic` (movements) | Nothing linear, nothing robotic |
| Spark particles | Dot radius 0.03, opacity 0.6, `MoveAlongPath` over 0.8–1.2s | Travel along connection lines during formula reveals and strip growth |

---

## Existing Types to Reuse

| Type | Use Case | Source |
|------|----------|--------|
| `math` | Displaying the product rule formula, wrong formula, limit expressions | Brand standard |
| `text` | Hook question, labels, transition text | Brand standard |
| `box` | Stating the final product rule (Tier 1/2 branded box) | Brand standard |
| `contradiction` | Red X slam on the WRONG formula f'·g' | scene_short.py |
| `equation_highlight` | Color-coding f'g (cyan) and fg' (green) in final formula | scene_short.py |
| `brace_anatomy` | Labeling the two strips and corner in the rectangle | scene_short.py |

---

## NEW Visual Type #1: `rectangle_area_proof`

### What it shows
A rectangle with sides labeled f(x) (width) and g(x) (height). When x increases by dx, the rectangle grows — the width becomes f(x+dx) and the height becomes g(x+dx). The area change decomposes into: a vertical strip on the right (width = Δf, height = g), a horizontal strip on top (width = f, height = Δg), and a tiny corner square (width = Δf, height = Δg).

### Motion (3 phases)

1. **Phase 1 — The rectangle materializes:**
   The rectangle doesn't just appear — it *emerges from the void*. First, a faint violet glow outline (stroke_width=6, opacity=0.15, color `#8B5CF6`) shimmers into existence at y ≈ -0.5. Then the crisp white outline (stroke_width=2, opacity=0.8) traces itself on top of the glow, edge by edge, using `Create` over 1.2s with `rate_func=smooth`. The interior fills with `#1a1130` at 0.15 opacity — a dark, deep pool.

   Side labels breathe to life: "f(x)" (Tier 6, cyan `#22D3EE`, `font_size=24`) writes in along the bottom edge, its own cyan glow halo (stroke_width=6, opacity=0.15) pulsing once on arrival. "g(x)" writes in along the left edge, same treatment. Each label has a **spark** — a tiny cyan dot (radius 0.03, opacity 0.6) that travels from the label to the rectangle corner it references, tracing the connection, then dissolving.

   "Area = f·g" fades into the rectangle center (white, opacity 0.6), with a barely perceptible breathing pulse (opacity 0.55 ↔ 0.65 over 3s, `rate_func=there_and_back`). The entire rectangle begins its **ambient breathing** — a scale oscillation of 1.0 ↔ 1.015 over 4s that persists for the rest of its life on screen.

2. **Phase 2 — Growth and decomposition (the living diagram):**
   The growth doesn't happen mechanically — it PULSES into existence. The right edge begins sliding right, the top edge sliding up, using `rate_func=ease_in_out_cubic` over 1.5s. As the edges move, faint **trailing sparks** (3–4 tiny dots, radius 0.02, green/cyan, opacity 0.4) follow the moving edges like particles in a current.

   The three new regions materialize with bloom:

   - **Right strip (f'g term):** A brief FLASH — the entire strip region blooms bright (cyan `#22D3EE` fill at 0.7 opacity + glow stroke 6 at 0.3 opacity for 0.2s), then settles to its resting state: fill opacity 0.4, stroke cyan at 0.6, glow halo (stroke_width=6, opacity=0.15) breathing behind it. The strip begins a slow pulse (opacity 0.35 ↔ 0.45 over 1.5s, `rate_func=there_and_back`). Label "f'g · dx" (Tier 6) writes in — the text itself has a faint cyan glow behind it.

   - **Top strip (fg' term):** Same bloom-then-settle, but in green `#39FF14`. Flash at 0.7 fill opacity → settle to 0.4. Green glow halo breathing. Label "fg' · dx" writes in with green glow backing. A **gradient connection line** (cyan→green, stroke_width=1, opacity=0.3) briefly appears between the two strips — showing they're *siblings*, two parts of the same change — then fades to 0.1 opacity.

   - **Corner square (the doomed piece):** Materializes in red `#FF4444` with an OMINOUS quality — fill opacity 0.5, but the glow halo is red (stroke_width=6, opacity=0.2), making it look like it's smoldering. Label "f'g'·dx²" Tier 6 writes in with a slight flicker (opacity jitter 0.8–1.0 over 0.3s), foreshadowing its destruction.

   Each region appears 0.3s apart. When each arrives, the OTHER regions dim slightly (existing strips drop to 0.25 opacity) for 0.5s, then recover — **brightness as attention**, exactly like AIGENTS neural activation.

3. **Phase 3 — The corner's death (the "oh!" moment):**
   The corner doesn't just shrink — it *fights to survive, then collapses*. First, two red `Indicate` pulses (0.3s each) — the corner flares bright red (glow opacity spikes to 0.35), like a node firing desperately. On the second pulse, both the cyan and green strips BRIGHTEN (opacity → 0.6) as if absorbing the corner's energy.

   Then `ShrinkToCenter` over 1.2s with `rate_func=ease_in_out_cubic`. As the corner collapses, **red spark particles** (4–5 tiny dots, radius 0.02, red `#FF4444`, opacity 0.5) scatter outward from its center along random short paths (0.3 unit radius), fading to zero over 0.6s — like embers dying.

   The moment the corner disappears: a **BLOOM FLASH** on the remaining two strips (both flash to 0.7 opacity + glow 0.3 for 0.15s, then settle back). They're all that's left. They're the answer.

   "dx → 0" materializes above the rectangle — Tier 3 callout (`font_size=24`, green `#39FF14`, weight=BOLD) — with its own green glow halo pulsing once on arrival (glow 0.15 → 0.3 → 0.15 over 0.4s).

### Timing
~12s total for all three phases. Phase 1: ~3s. Phase 2: ~5s. Phase 3: ~4s.

### Colors (all from settings.json)
- Original rectangle outline: white at 0.8 opacity, stroke_width 2
- Rectangle glow halo: violet `#8B5CF6`, stroke_width 6, opacity 0.15 (BREATHING)
- Original rectangle fill: `#1a1130` (boxFill) at 0.15 opacity
- Right strip: cyan `#22D3EE`, fill_opacity 0.4, stroke `#22D3EE` at 0.6, glow halo cyan stroke 6 opacity 0.15 (BREATHING)
- Top strip: green `#39FF14`, fill_opacity 0.4, stroke `#39FF14` at 0.6, glow halo green stroke 6 opacity 0.15 (BREATHING)
- Corner: red `#FF4444`, fill_opacity 0.5, stroke `#FF4444` at 0.8, glow halo red stroke 6 opacity 0.2 (SMOLDERING)
- Side labels: Tier 6 MathTex, `font_size=24`, cyan `#22D3EE`, with glow backing
- Strip labels: Tier 6 MathTex, `font_size=24`, white, with color-matched glow backing
- Spark particles: matched to parent color, radius 0.02–0.03, opacity 0.4–0.6

### Sizing for portrait frame
- Rectangle: ~2.2 units wide × ~1.8 units tall max to fit within MAX_WIDTH (3.69)
- Positioned at y ≈ -0.5 (between math zone and graph zone) — this is a HERO visual, it gets the center
- Growth extends right/top by ~0.6 units each
- Braces + labels need 0.3 unit clearance from rectangle edges

### Alive Layer (persistent effects during this type's screen time)
| Element | Effect | Parameters |
|---------|--------|------------|
| Rectangle outline | Breathing scale | 1.0 ↔ 1.015, 4s cycle, `rate_func=there_and_back` |
| Rectangle glow | Breathing opacity | 0.12 ↔ 0.18, 3s cycle |
| Side labels | Subtle pulse | opacity 0.85 ↔ 1.0, 2s cycle |
| Active strip (being discussed) | BRIGHT | full opacity + glow 0.2 |
| Inactive strips | DIM | 0.25–0.3 opacity, glow 0.08 |
| Area label ("f·g") | Breathing | opacity 0.55 ↔ 0.65, 3s cycle |

### Reusability: HIGH
- ANY product-based proof: quotient rule (inverted), (a+b)² = a²+2ab+b²
- Any "area decomposition" argument in calculus
- Parameter: `f_label`, `g_label`, `strip_labels[]`, `show_corner_shrink` (bool), `duration`

### Config Fields (proposed)
```json
{
  "type": "rectangle_area_proof",
  "f_label": "f(x)",
  "g_label": "g(x)",
  "strip_labels": ["f'g \\cdot dx", "fg' \\cdot dx", "f'g' \\cdot dx^2"],
  "show_corner_shrink": true,
  "phase": 1,
  "duration": 12.0
}
```

---

## NEW Visual Type #2: `wrong_vs_right`

### What it shows
A split-screen comparison: the WRONG answer on top, the RIGHT answer on bottom, separated by a horizontal divider. The wrong answer has a red `#FF4444` tint/strike, the right answer has a green `#39FF14` glow. This is a reusable "common misconception debunk" visual.

### Motion

1. **Wrong answer writes in** at y = mathCenterY + 1.0 — Tier 5 MathTex (`font_size=30`, white). The text arrives with a faint white glow halo (stroke_width=6, opacity=0.1) that gives it presence. Holds 1.5s — during the hold, the text breathes (opacity 0.9 ↔ 1.0, 2s cycle). It looks confident. It looks *wrong but doesn't know it yet*.

2. **Red treatment (the kill):** The glow halo shifts from white to orange `#F97316` over 0.3s — a warning. Then the formula text itself shifts to orange. A diagonal strikethrough line SLASHES across (red `#FF4444`, stroke_width 3) with `rate_func=rush_into` — fast, violent, decisive. On impact, a brief RED BLOOM (the entire wrong formula's glow spikes to red, opacity 0.3, for 0.15s) then dims. Small "✗" in red appears with a 0.1s scale pop (1.3 → 1.0). **Red spark particles** (3 dots, radius 0.02, red, opacity 0.4) scatter from the strike intersection point, fading over 0.4s.

3. **Divider draws:** Thin horizontal line (white, opacity 0.15, stroke_width 1) draws from left to right at y = mathCenterY, with a tiny cyan spark (radius 0.03) riding the leading edge of the line as it draws — a living data flow, not just a line.

4. **Right answer materializes** at y = mathCenterY − 1.0 — Tier 2 Key Fact box. First the violet border (`#8B5CF6`, stroke 2.5) traces itself with `Create`, its glow halo (stroke_width=6, opacity=0.15, violet) shimmering into existence just ahead of the crisp stroke. BoxFill `#1a1130` opacity 0.6 fills behind. Cyan `#22D3EE` text writes in. Then a green `#39FF14` Circumscribe animation rings the box — but with BLOOM: the Circumscribe line has a glow trail (stroke_width=6, green, opacity=0.2) that follows 0.1s behind the leading edge, creating a neon sweep effect.

5. **Wrong fades, right glows:** Wrong answer + strike fade to 0.15 opacity — dying into the background. Right answer BRIGHTENS: box glow halo pulses up to 0.25 opacity, then settles to a breathing 0.12 ↔ 0.18 pulse. The right formula is ALIVE. The wrong one is a ghost.

### Timing
~8s total. Wrong display: 2s. Red strike: 1s. Divider: 0.5s. Right reveal: 2s. Comparison hold: 2.5s.

### Colors (all from settings.json)
- Wrong formula: white → orange `#F97316` on strike
- Wrong formula glow: white (0.1) → orange (0.15) → red bloom (0.3, 0.15s) → dim (0.05)
- Strikethrough line: red `#FF4444`, stroke_width 3
- ✗ label: red `#FF4444`, `font_size=20`
- Divider: white, opacity 0.15, with cyan spark rider
- Right formula box: cyan `#22D3EE` text, violet `#8B5CF6` border 2.5 stroke, `#1a1130` fill 0.6 opacity
- Right glow halo: violet `#8B5CF6`, stroke_width 6, opacity 0.15 (BREATHING 0.12 ↔ 0.18)
- Circumscribe + trail: green `#39FF14`, glow stroke 6, opacity 0.2

### Reusability: HIGH
- ANY "common mistake" reveal: d/dx[fg] ≠ f'g', integral rules, limit misconceptions
- Chain rule: d/dx[f(g(x))] ≠ f'(g'(x))
- Power rule edge cases: d/dx[xⁿ] ≠ xⁿ⁻¹
- Parameters: `wrong_tex`, `right_tex`, `right_label` (optional box label), `strike_style` ("diagonal" | "horizontal"), `duration`

### Config Fields (proposed)
```json
{
  "type": "wrong_vs_right",
  "wrong_tex": "\\frac{d}{dx}[f \\cdot g] = f' \\cdot g'",
  "right_tex": "\\frac{d}{dx}[f \\cdot g] = f'g + fg'",
  "right_label": "Product Rule",
  "strike_style": "diagonal",
  "duration": 8.0
}
```

---

## Step-by-Step Visual Storyboard

| Step | Time | Duration | Visual Type | Tier | What's On Screen | Motion/Animation | Alive Layer |
|------|------|----------|-------------|------|------------------|-----------------|-------------|
| 1 | 0.0–3.5s | 3.5s | `text` | 5 | "Most people memorize the product rule…" | Write animation (`rate_func=smooth`), white `#FFFFFF`, `font_size=30`, centered at y=1.2. Text arrives with a faint white glow halo (stroke_width=6, opacity=0.08) that breathes. | **Glow**: white halo 0.08 behind text. **Breathing**: text opacity 0.9↔1.0 over 2s. **Background**: pure black — the text floats in void. |
| 2 | 4.0–8.5s | 4.5s | `wrong_vs_right` | 5/2 | Wrong: $\frac{d}{dx}[f \cdot g] = f' \cdot g'$ — Right: $f'g + fg'$ in Tier 2 box | Wrong writes in with white glow → orange shift → RED BLOOM + diagonal strike + red sparks → divider with cyan spark rider → right box materializes with violet glow trace → green Circumscribe with neon trail → wrong dims to ghost, right breathes bright | **Active element**: right formula BRIGHT (glow 0.18, breathing). **Dimmed**: wrong formula at 0.15 opacity. **Sparks**: red scatter on strike, cyan rider on divider. |
| 3 | 9.0–12.5s | 3.5s | `text` | 4 | "The real answer has TWO terms. Why?" | Tier 4 Title, `font_size=26`, violet `#8B5CF6`, weight=BOLD, centered at y=1.2. Writes in with `rate_func=smooth`. Violet glow halo (stroke_width=6, opacity=0.12) shimmers as text arrives, then settles to breathing pulse. | **Glow**: violet halo 0.12 breathing behind text. **Pulse**: "TWO" could get a brief green flash (0.15s, `#39FF14` set_color then back) to emphasize. |
| 4 | 13.0–16.0s | 3.0s | `text` | 4 | "Think about AREA." | Tier 4 Title, `font_size=26`, violet `#8B5CF6`, centered at y=1.2. Writes in with `rate_func=smooth`. On the word "AREA" — a brief BLOOM: the word flashes bright white for 0.15s with expanded glow (opacity 0.3), then settles to violet. Like a neuron firing on the key concept. | **Bloom**: "AREA" fires bright on arrival. **Breathing**: entire text 0.9↔1.0 over 2s. |
| 5 | 16.5–21.5s | 5.0s | `rectangle_area_proof` (phase 1) | 6 | Rectangle with sides f(x) and g(x), area=f·g labeled inside | Violet glow outline shimmers first → white crisp outline traces on top via `Create` (`rate_func=smooth`) → side labels write in with cyan glow + spark connectors → "Area = f·g" fades in center, breathing. Entire rectangle begins ambient scale breathing (1.0↔1.015, 4s). | **Glow**: violet halo behind rectangle. **Breathing**: rectangle scale, label opacity, area label. **Sparks**: cyan dots trace from labels to corners. |
| 6 | 22.0–30.0s | 8.0s | `rectangle_area_proof` (phase 2) | 6 | Rectangle GROWS — right+top edges extend. Three colored strips appear with bloom flashes. | Edges slide with `rate_func=ease_in_out_cubic`, trailing sparks follow. Each strip: BLOOM FLASH (0.7 opacity + glow 0.3, 0.2s) → settle to resting glow. Gradient connection line between strips (cyan→green, 0.3 opacity, fades to 0.1). Corner smolders red. When each new strip appears, others dim briefly (brightness-as-attention). | **Active**: current strip BRIGHT (0.4 fill + 0.15 glow). **Inactive**: other strips dim to 0.25. **Sparks**: trailing particles on moving edges. **Gradient**: cyan→green sibling connection. **Corner**: red smolder glow 0.2. |
| 7 | 30.5–35.5s | 5.0s | `brace_anatomy` | 6 | Braces pointing at three colored regions: "f'g·dx", "fg'·dx", "f'g'·dx²" | Braces Write in one at a time (0.8s each, `rate_func=smooth`). Each brace has a color-matched glow halo (stroke_width=6, opacity=0.15). Label appears 0.2s after brace, with its own glow backing. When a brace appears, its corresponding strip BRIGHTENS (activation) while others dim. A tiny spark travels along each brace from tip to label. | **Activation**: strip brightens when its brace appears. **Glow**: color-matched halos on braces. **Sparks**: dot follows brace path. **Dim**: non-active regions at 0.3 opacity. |
| 8 | 36.0–42.0s | 6.0s | `rectangle_area_proof` (phase 3) | 3 | Corner square SHRINKS — pulses red, scales to zero. "dx→0" appears with bloom. | Corner Indicate 2× (0.3s each, red glow spikes to 0.35). On second pulse, cyan+green strips BRIGHTEN (absorbing energy). `ShrinkToCenter` 1.2s (`rate_func=ease_in_out_cubic`) with red spark particles scattering outward (4–5 dots, fading 0.6s). BLOOM FLASH on remaining strips (0.7 opacity, 0.15s). "dx → 0" materializes with green glow pulse (0.15→0.3→0.15 over 0.4s). | **Bloom**: strips flash on corner death. **Sparks**: red embers scatter from dying corner. **Activation**: strips reach peak brightness. **Pulse**: "dx→0" arrival bloom. |
| 9 | 42.5–48.5s | 6.0s | `math` | 5 | $\frac{dA}{dx} = f'g + fg'$ | FadeOut rectangle (0.4s, `rate_func=smooth` — the glow fades LAST, lingering 0.2s after the solid shape). Write formula at y=1.2. "f'g" colored cyan `#22D3EE` with cyan glow halo, "fg'" colored green `#39FF14` with green glow halo. The "+" sign pulses white (opacity 0.7↔1.0, 1.5s) — the connector between the two living terms. | **Glow**: each colored term has its own glow halo (stroke 6, opacity 0.15). **Breathing**: "+" pulses. **Lingering glow**: rectangle glow outlasts solid on fadeout. **Dim**: "dA/dx =" at 0.8 opacity (contextual), colored terms at 1.0 (active). |
| 10 | 49.0–55.0s | 6.0s | `box` | 1 | **Product Rule** — $\frac{d}{dx}[f \cdot g] = f'g + fg'$ | Tier 1 Punchline box materializes: violet border traces with `Create` (`rate_func=smooth`), glow halo (stroke 6, violet, opacity 0.15) shimmers ahead of the border. BoxFill `#1a1130` pools behind. Formula writes in green `#39FF14`, `font_size=42`. BLOOM on completion — entire box glow spikes to 0.3 for 0.2s, then settles to breathing (0.12↔0.18, 3s). Label "Product Rule" above in cyan `#22D3EE` `font_size=14`, with its own faint glow. | **Bloom**: completion flash. **Breathing**: box glow 0.12↔0.18. **Glow**: violet halo on border, cyan halo on label. **The box is alive** — not a static frame, but a breathing, glowing container. |
| 11 | 55.5–60.0s | 4.5s | `equation_highlight` | — | Same formula: f'g flashes cyan `#22D3EE`, fg' flashes green `#39FF14` | Indicate animation on each term in sequence (0.8s each, `rate_func=smooth`). When a term activates, its glow halo FLARES (opacity → 0.35, scale 1.0 → 1.05, then settle). The OTHER term dims to 0.4 opacity during the flash (brightness-as-attention). Tiny spark particles (2 dots each) orbit the active term once during its flash. Terms get set_color permanently. | **Activation**: flaring glow + scale pop. **Dim**: inactive term drops to 0.4. **Sparks**: orbiting dots during each flash. **Sequence**: cyan first, then green — matching strip order. |
| 12 | 60.5–64.5s | 4.0s | `text` | 3 | "Not random. Not memorized. Just geometry." | Tier 3 Callout: `font_size=24`, green `#39FF14`, weight=BOLD, centered at y=1.2. Writes in with `rate_func=smooth`. Green glow halo (stroke 6, opacity 0.15) breathing behind. On "geometry" — a brief violet bloom (the word flashes with violet glow 0.25 for 0.15s), tying it back to the rectangle that proved it. | **Glow**: green halo breathing. **Bloom**: "geometry" gets a violet callback flash. **Breathing**: text 0.9↔1.0. |
| EC | 65.0–67.7s | 2.7s | `end_card` | — | Lissajous curve (`#00E5FF`, A=1.2, B=0.95) + "ORBITAL" wordmark (`#00E5FF`, 22px) + "Watch it click." (14px, white, 0.5 opacity) | Create lissajous core (stroke 2) 0.8s → lissajous glow halo (stroke 8, opacity 0.2) fades in 0.6s, breathing (0.15↔0.25, 2s cycle) → FadeIn wordmark with cyan glow + tagline 0.4s → hold 1.2s → FadeOut 0.3s. The lissajous itself breathes — scale 1.0↔1.02, 3s cycle. | Standard end card per settings.json — but the lissajous BREATHES. |

### Total Duration: ~67.7s (content: ~65s + end card: 2.7s)

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

---

## Technical Notes for Claudio

### 🔮 ALIVE Effects — Manim Implementation Guide

#### Glow Layers (the foundation of everything)
Every key mobject needs TWO copies: the glow layer and the crisp layer.
```python
# Pattern: glow behind, crisp on top
crisp_rect = Rectangle(stroke_width=2, stroke_color=WHITE, stroke_opacity=0.8)
glow_rect = crisp_rect.copy().set_stroke(
    color="#8B5CF6", width=6, opacity=0.15  # settings.json: glowStroke=6, glowOpacity=0.15
)
rect_group = VGroup(glow_rect, crisp_rect)  # glow BEHIND crisp
```

#### Breathing / Pulsing (the heartbeat)
Use `ValueTracker` + `always_redraw` or `add_updater` for continuous effects:
```python
breath_tracker = ValueTracker(0)
def breathing_updater(mob, dt):
    t = breath_tracker.get_value()
    # Opacity oscillation: center ± amplitude
    mob.set_opacity(0.15 + 0.03 * np.sin(2 * PI * t / 3.0))  # 3s cycle
    breath_tracker.increment_value(dt)
glow_rect.add_updater(breathing_updater)
```
For scale breathing:
```python
def scale_breath(mob, dt):
    t = breath_tracker.get_value()
    scale = 1.0 + 0.015 * np.sin(2 * PI * t / 4.0)  # 4s cycle, ±1.5%
    mob.become(mob.copy().scale(scale / mob.get_height() * original_height))
```
**Important:** Use `rate_func=there_and_back` for explicit pulse animations (one-shot). Use updaters for continuous breathing.

#### Bloom Flash (the "oh!" moment)
```python
# Brief bright spike on a key reveal
def bloom(mob, glow_mob, duration=0.2, peak_opacity=0.35, rest_opacity=0.15):
    return Succession(
        glow_mob.animate(run_time=duration/2, rate_func=rush_into).set_opacity(peak_opacity),
        glow_mob.animate(run_time=duration/2, rate_func=rush_from).set_opacity(rest_opacity),
    )
```

#### Spark Particles (living connections)
```python
# Small dot that follows a path and fades
spark = Dot(radius=0.03, color="#22D3EE", fill_opacity=0.6)
path = Line(start_point, end_point)
self.play(
    MoveAlongPath(spark, path, run_time=0.8, rate_func=smooth),
    spark.animate(run_time=0.8).set_opacity(0),
)
```
For scatter effects (corner death):
```python
# Multiple sparks scattering from a point
sparks = VGroup(*[Dot(radius=0.02, color="#FF4444", fill_opacity=0.5) for _ in range(5)])
sparks.move_to(corner.get_center())
scatter_anims = [
    spark.animate(run_time=0.6, rate_func=rush_from).move_to(
        corner.get_center() + 0.3 * np.array([np.cos(a), np.sin(a), 0])
    ).set_opacity(0)
    for spark, a in zip(sparks, np.linspace(0, 2*PI, 5, endpoint=False))
]
self.play(*scatter_anims)
```

#### Brightness as Meaning (AIGENTS activation pattern)
```python
# When focusing on a term, dim everything else
def activate(target, others, bright=1.0, dim=0.3):
    return AnimationGroup(
        target.animate(run_time=0.3).set_opacity(bright),
        *[other.animate(run_time=0.3).set_opacity(dim) for other in others],
        lag_ratio=0
    )
```

#### Gradient Connection Lines
```python
# Cyan→Green gradient line between sibling elements
gradient_line = Line(strip_right.get_center(), strip_top.get_center())
gradient_line.set_color(color=[("#22D3EE"), ("#39FF14")])
gradient_line.set_stroke(width=1, opacity=0.3)
```

#### Organic Easing (nothing robotic)
- **Default all FadeIn/FadeOut:** `rate_func=smooth`
- **All movements:** `rate_func=ease_in_out_cubic` (Manim: `smooth` is close, or use `rate_functions.ease_in_out_cubic` if available)
- **Strikes/slams:** `rate_func=rush_into` for violent impact
- **Pulsing loops:** `rate_func=there_and_back`
- **NEVER** use `rate_func=linear` except for continuous sweeps (like the area accumulator)

#### Lingering Glow on FadeOut
When fading out a glowing element, fade the glow LAST:
```python
self.play(
    FadeOut(crisp_mob, run_time=0.4),
    FadeOut(glow_mob, run_time=0.6),  # lingers 0.2s longer
)
```

### Building `rectangle_area_proof`
- Core: `Rectangle` mobjects. Base rect ~2.2×1.8 units, positioned at y ≈ -0.5.
- **Every rectangle and strip needs a glow twin** — see glow layer pattern above.
- Growth: Create three sub-rectangles (`strip_right`, `strip_top`, `corner`) positioned flush against the base rect edges. Use bloom flash on each appearance.
- Corner shrink: `ShrinkToCenter(corner)` over 1.2s with `rate_func=ease_in_out_cubic` + scatter sparks.
- Label positioning: `Brace` mobjects — they auto-position against rectangle edges. Each brace gets a glow twin.
- The three phases can be one step type with `"phase": 1|2|3` parameter, sharing persistent mobjects via `graph_mobs[]`.
- ALL font sizes use explicit `font_size=` — NEVER `.scale()`.
- **Ambient breathing runs throughout** — add updaters in Phase 1, they persist through Phases 2–3.

### Building `wrong_vs_right`
- Wrong: plain `MathTex(wrong_tex, font_size=30, color=WHITE)` at y = mathCenterY + 1.0, **with glow twin** (white, stroke 6, opacity 0.1)
- Strike: diagonal `Line` from corner UL to DR of the MathTex, color `#FF4444`, stroke_width 3, `rate_func=rush_into`
- **On strike impact:** glow twin shifts to red, spikes opacity to 0.3 for 0.15s (bloom), then dims
- Divider: `Line` at y = mathCenterY, white, opacity 0.15, **with cyan spark riding the Create animation**
- Right: Tier 2 box pattern with glow twin. Circumscribe gets a glow trail (second Circumscribe at stroke_width=6, opacity=0.2, delayed 0.1s).

### `contradiction` reuse (step 2 alternative)
The original brief used `contradiction` for the X slam. The new `wrong_vs_right` type REPLACES steps 2 and 3 from v1 — it shows BOTH wrong and right in one visual, which is more impactful and more reusable. If Claudio prefers, the old `contradiction` still works for step 2 alone, but then we'd need a separate step for the correct formula.

### Muted viewer check
- Step 2 (wrong_vs_right): Red strike BLOOM + green box GLOW — fully readable without audio. The visual violence of the strike tells the story.
- Steps 5–8 (rectangle proof): Colors + glow tell the story — cyan strip BREATHES, green strip BREATHES, red corner SMOLDERS then SCATTERS. Self-explanatory even silent.
- Step 9 (color-coded formula): Cyan f'g + green fg' glow with their own halos, tying back to the strips
- Step 10 (Tier 1 box): Final formula, large, glowing, BREATHING
- Step 12 (green callout): The one-liner takeaway, green glow, screenshot-ready

### Portrait framing notes
- Rectangle sits at y ≈ -0.5 (below math zone, above graph zone) — this is intentional. It's the HERO visual and deserves center screen.
- Math formulas stay at y = 1.2 (mathCenterY).
- When rectangle is on screen, no math should appear at mathCenterY simultaneously — it would crowd the frame. Steps 5–8 are rectangle-only.
- Step 9 transitions: FadeOut rectangle (glow lingers), then formula writes at y = 1.2.
- **Glow halos add visual width** — account for ~0.15 extra units on each side when positioning near MAX_WIDTH.
