# Pipeline Paths — Contract
**Last Updated:** 2026-03-02

---

## Overview

Orbital supports three generation paths. All paths converge at Stage 4 (TTS) and share Stages 5-6 (Render + Delivery).

```
                    ┌─────────────────────────────────────┐
                    │         Professor Input              │
                    │  "Type a problem" | "Upload photo"   │
                    │  "Provide my own solution"           │
                    └──────────┬──────────┬───────────┬────┘
                               │          │           │
                    ┌──────────▼──┐ ┌─────▼─────┐ ┌──▼──────────┐
                    │   Path A    │ │  Path B   │ │   Path C    │
                    │  Full AI    │ │ AI + Prof │ │ Prof Source  │
                    │  Pipeline   │ │  Review   │ │  Solution   │
                    └──────┬──────┘ └─────┬─────┘ └──────┬──────┘
                           │              │              │
                    Stage 1: Script  Stage 1: Script   Script from
                           │              │           prof's steps
                    Stage 2: Circle  Prof reviews/     (text or OCR)
                           │         edits script          │
                    Stage 3: Lean        │                 │
                           │              │                │
                    ┌──────▼──────────────▼────────────────▼──┐
                    │            Stage 4: TTS                  │
                    │            Stage 5: Render                │
                    │            Stage 6: Delivery              │
                    └──────────────────────────────────────────┘
```

---

## Path A: Full AI Pipeline

**When:** Professor wants hands-off, fully automated, highest verification tier.

| Stage | What Happens | Cost |
|-------|-------------|------|
| 1. Script | DeepSeek V3 generates script from problem | $0.001 |
| 2. Circle | 3 Opus + 1 Sonnet verify & revise | $0.60 |
| 3. Lean | Opus writes Lean 4 proof (if enabled) | $0.10 |
| 4. TTS | ElevenLabs narration | $0.12-0.56 |
| 5. Render | Manim + ffmpeg | $0.00 |
| 6. Delivery | Storage + caching | $0.001 |
| **Total** | | **$0.82-1.26** |

**Badge:** 🏛️ Lean 4 Verified (with Lean) or ✅ AI Verified (without Lean)

---

## Path B: AI Script + Professor Review

**When:** Professor wants AI to draft the script but wants to review/edit before rendering. Saves Circle + Lean costs.

| Stage | What Happens | Cost |
|-------|-------------|------|
| 1. Script | DeepSeek V3 generates script from problem | $0.001 |
| 2. Review | Professor views script in dashboard editor | $0.00 |
| — | Professor edits narration, math, step order | $0.00 |
| — | Professor approves | $0.00 |
| 4. TTS | ElevenLabs narration | $0.12-0.56 |
| 5. Render | Manim + ffmpeg | $0.00 |
| 6. Delivery | Storage + caching | $0.001 |
| **Total** | | **$0.12-0.56** |

**Badge:** 👨‍🏫 Teacher Verified

### Script Editor UI
Professor sees each step as a card:
```
┌──────────────────────────────────────────┐
│ Step 3 of 15                    [math]  ▼│
│                                          │
│ Narration:                               │
│ ┌──────────────────────────────────────┐ │
│ │ We substitute x = -1 into both      │ │
│ │ equations to verify the intersection │ │
│ └──────────────────────────────────────┘ │
│                                          │
│ Display:                                 │
│   y = (-1) + 2 = 1                      │
│   y = (-1)² = 1  ✓                      │
│                                          │
│ [⬆ Move Up] [⬇ Move Down] [🗑 Delete]   │
└──────────────────────────────────────────┘
```

Controls:
- Edit narration text inline
- Edit LaTeX inline (with live preview)
- Reorder steps via drag or buttons
- Delete steps
- Add new steps
- Change step type (text, math, transform, box, graph)
- **[✅ Approve & Generate Video]** button

---

## Path C: Professor-Sourced Solution

**When:** Professor provides their OWN solution (typed or photographed). They are the source of mathematical truth — no AI verification needed.

### Input Methods

**Option 1: Typed Steps**
Professor types their solution step by step in a structured form:
```
┌─────────────────────────────────────────────┐
│ Your Solution                               │
│                                             │
│ Problem: Find the area between y=x+2, y=x² │
│                                             │
│ Step 1: [Find intersection points         ] │
│ Math:   [x² = x + 2 → x² - x - 2 = 0    ] │
│                                             │
│ Step 2: [Factor                            ] │
│ Math:   [(x-2)(x+1) = 0 → x = -1, x = 2  ] │
│                                             │
│ Step 3: [Set up the integral               ] │
│ Math:   [\int_{-1}^{2} (x+2-x^2) dx       ] │
│                                             │
│ [+ Add Step]                                │
│                                             │
│ [📸 Or upload a photo instead]              │
│ [🎬 Generate Video]                         │
└─────────────────────────────────────────────┘
```

**Option 2: Photo Upload (OCR)**
Professor photographs their handwritten work (whiteboard, notebook, tablet):
1. Upload image(s) to dashboard
2. Vision model (Claude or GPT-4o) extracts steps + math
3. Professor reviews extracted steps in the editor (same as Path B editor)
4. Professor confirms/edits → generate

### Script Generation from Professor Input

A single, cheap AI call converts the professor's steps into our script JSON schema:

**Prompt:**
```
You are a script formatter for Orbital, an AI math video generator.

A professor has provided their own solution steps. Convert them into our script JSON format.

REQUIREMENTS:
- Keep the professor's math EXACTLY as provided — do not change any calculations
- Add pedagogical narration in Orbital's voice: explain WHY before HOW, call out common mistakes, talk to ONE student
- Choose appropriate step types (text, math, mixed, transform, box, graph)
- Add an intro step and a closing takeaway step
- Detail level: {detail_level}

PROFESSOR'S SOLUTION:
{professor_steps}

PROBLEM: {problem}
COURSE: {course}

Output the script as a JSON array of steps matching the Stage 1 schema.
```

**Model:** DeepSeek V3 (cheapest) or claude-sonnet-4 (better narration quality)
- DeepSeek: ~$0.001
- Sonnet: ~$0.01-0.03

### OCR / Vision Extraction

**Prompt for photo extraction:**
```
Extract the mathematical solution from this image. Output each step as:

Step [n]: [Description of what's being done]
Math: [The mathematical expression in LaTeX]

Preserve the exact mathematical content. If handwriting is ambiguous, note it with [?].
```

**Model:** Claude claude-sonnet-4 vision or GPT-4o
- Cost: ~$0.01-0.03 per image
- Supports: handwriting, whiteboard photos, tablet screenshots, printed worksheets

### Professor Reviews Extracted Steps
After OCR or typed input, professor always sees the extracted/formatted steps in the editor before generation. This is their chance to fix any OCR misreads or adjust narration.

### Cost Breakdown

| Component | Typed Input | Photo Input |
|-----------|-------------|-------------|
| OCR/Vision | — | $0.01-0.03 |
| Script formatting | $0.001-0.03 | $0.001-0.03 |
| Professor review | $0.00 | $0.00 |
| TTS | $0.12-0.56 | $0.12-0.56 |
| Render | $0.00 | $0.00 |
| Delivery | $0.001 | $0.001 |
| **Total** | **$0.12-0.59** | **$0.13-0.62** |

**Badge:** 👨‍🏫 Teacher Verified

---

## Badge Summary

| Badge | Meaning | Paths |
|-------|---------|-------|
| 🏛️ **Lean 4 Verified** | Formally proven correct by Lean 4 compiler | Path A (with Lean) |
| ✅ **AI Verified** | Passed 4-agent Verification Circle | Path A (without Lean) |
| 👨‍🏫 **Teacher Verified** | Professor reviewed/provided the solution | Path B, Path C |

Badges are displayed on:
- Video player overlay (corner watermark)
- Video library card in dashboard
- Shared/embedded video page

---

## Dashboard UI: Path Selection

When a professor clicks "Generate Video," they see:

```
┌─────────────────────────────────────────────────┐
│                                                 │
│  How do you want to create this video?          │
│                                                 │
│  ┌───────────────────────────────────────────┐  │
│  │ 🤖 Let AI solve it                       │  │
│  │ Type a problem. AI generates and verifies │  │
│  │ the full solution.                        │  │
│  │ Cost: ~$0.72-1.26  Badge: AI/Lean        │  │
│  └───────────────────────────────────────────┘  │
│                                                 │
│  ┌───────────────────────────────────────────┐  │
│  │ ✏️ AI draft, I'll review                  │  │
│  │ AI writes the script. You review and      │  │
│  │ edit before rendering.                    │  │
│  │ Cost: ~$0.12-0.56  Badge: Teacher         │  │
│  └───────────────────────────────────────────┘  │
│                                                 │
│  ┌───────────────────────────────────────────┐  │
│  │ 📝 I'll provide my solution               │  │
│  │ Type your steps or upload a photo.        │  │
│  │ We'll turn it into a polished video.      │  │
│  │ Cost: ~$0.12-0.62  Badge: Teacher         │  │
│  └───────────────────────────────────────────┘  │
│                                                 │
└─────────────────────────────────────────────────┘
```

---

## Integration Notes

- All three paths converge at Stage 4 (TTS) — same output format regardless of path
- Path B and C skip Stages 2 and 3 entirely
- Path C adds an OCR step (optional) before the formatting call
- The script editor component is shared between Path B (review AI draft) and Path C (review extracted steps)
- Professor always has final approval before TTS + render begins
- Caching works the same across all paths — problem_hash + detail_level
