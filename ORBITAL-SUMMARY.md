# ORBITAL — Course-Specific Video Tutoring

## What It Is

Orbital is a consumer-facing education platform that auto-generates professional math tutorial videos. Students select their university (ASU, GCU) and course (MAT144, MAT170, etc.), then watch step-by-step problem walkthroughs.

## How It Works

1. We write problems as simple JSON scripts (narration + LaTeX math)
2. Pipeline generates voice narration via ElevenLabs AI
3. Manim (3Blue1Brown's animation library) renders the math visuals
4. Audio is measured, animations are synced perfectly, video is stitched together
5. Output: Polished tutorial videos with professional narration

**Key insight:** Audio-first approach — generate audio, measure exact durations, render animations to match. Perfect sync every time.

## Current State

| Component | Status |
|-----------|--------|
| **Video Factory** (`orbital_factory/`) | ✅ Working — Python pipeline generates videos from JSON |
| **Website** (`orbital_site/`) | ✅ Built — Next.js site with course/university selection |
| **Sample Output** | ✅ Done — `linear_equation_final.mp4` in output folder |
| **Voices** | ✅ 5 voices configured (Allison, Sarah, Alice, Daniel, George) |

## Folder Structure

```
~/Desktop/Orbital/
├── orbital_factory/     # Video generation pipeline
│   ├── pipeline.py      # Main orchestrator
│   ├── scripts/         # Problem JSON files
│   ├── audio/           # Generated voice clips
│   └── output/          # Final MP4s
│
└── orbital_site/        # Consumer website (Next.js)
    └── src/app/         # Pages, components
```

## Business Model

- **Free videos** — Attract users, build trust
- **$2 Minis** — Focused topic guides  
- **$9 Exam Packs** — Full exam prep bundles

## To Run Locally

```bash
# Website
cd ~/Desktop/Orbital/orbital_site && npm run dev
# → http://localhost:3000

# Generate a video
cd ~/Desktop/Orbital/orbital_factory
python pipeline.py scripts/test_problem.json --voice allison
```

## Example Problem JSON

```json
{
  "meta": {
    "brand": "Orbital",
    "course": "MAT170",
    "topic": "Solving Linear Equations"
  },
  "steps": [
    {
      "narration": "Let's solve the equation two x plus five equals eleven.",
      "latex": "2x + 5 = 11"
    },
    {
      "narration": "First, subtract five from both sides.",
      "latex": "2x + 5 - 5 = 11 - 5"
    },
    {
      "narration": "This simplifies to two x equals six.",
      "latex": "2x = 6"
    },
    {
      "narration": "Now divide both sides by two.",
      "latex": "\\frac{2x}{2} = \\frac{6}{2}"
    },
    {
      "narration": "And we get our answer: x equals three.",
      "latex": "x = 3"
    }
  ]
}
```

## Next Steps

- Scale up content (more courses, more problems)
- Deploy website (Vercel)
- Build content submission flow (if letting users request videos)
- Expand to more universities

---

*Questions? Ask Clayton or Claudio.*
