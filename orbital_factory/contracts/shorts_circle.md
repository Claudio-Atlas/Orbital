# Shorts Circle — Contract
**Created:** 2026-03-04
**Last Updated:** 2026-03-04

---

## Overview

The Shorts Circle is a 6-agent review panel specifically for Orbital's short-form video content (TikTok, YouTube Shorts, Instagram Reels). It is **separate** from the full Verification Circle used for instructor-facing proof videos.

**Key differences from the full Verification Circle:**
- 6 real subagents with persistent sessions (not one agent role-playing)
- Includes Hook & SEO + Script & Pacing roles (social media specific)
- Lighter on formal verification (no Lean gate — shorts are conceptual, not proofs)
- Heavier on retention, pacing, and discoverability
- All agents share short-form constraints

## Shared Constraints (All 6 Agents)

| Constraint | Value |
|-----------|-------|
| Target duration | ~75 seconds |
| Hard minimum | 50 seconds |
| Hard maximum | 2 minutes (120s) |
| Format | Vertical 9:16, 1080×1920 |
| Frame rate | 60fps |
| Platforms | TikTok, YouTube Shorts, Instagram Reels (simultaneously) |
| Audience | Cold viewers — assume no prior context |
| Goal | Teach ONE concept clearly AND keep them watching |

## The 6 Agents

| # | Name | Role | Model | Focus |
|---|------|------|-------|-------|
| 1 | **Rigby** | Mathematician A (Rigor) | claude-opus-4-6 | Math correctness — no errors, no hand-waving. Veto power on correctness |
| 2 | **Sagan** | Mathematician B (Breadth) | claude-opus-4-6 | Oversimplification guard — is this catchy but technically wrong? |
| 3 | **Polya** | Pedagogy Expert | claude-opus-4-6 | Teaching clarity — can a cold viewer learn this in one watch? |
| 4 | **Zara** | Student Simulator | claude-sonnet-4-6 | Comprehension check — "I'm scrolling TikTok at 11pm, do I get this?" |
| 5 | **Vex** | Hook & SEO Specialist | claude-sonnet-4-6 | First 3 seconds, title, description, hashtags, retention, re-watch factor |
| 6 | **Tempo** | Script & Pacing Director | claude-sonnet-4-6 | Narration rhythm, timing, energy arc, speakability, silence as a tool |

### Why These Names
- **Rigby** — sounds rigorous (adapted from Mathematician A)
- **Sagan** — Carl Sagan, known for making complex science accessible without oversimplifying (adapted from Mathematician B)
- **Polya** — George Pólya, legendary math pedagogy ("How to Solve It") (adapted from Pedagogy Expert)
- **Zara** — fresh, young-sounding name for the student voice (adapted from Student Simulator)
- **Vex** — sharp, attention-grabbing, fits the hook/SEO energy (NEW role)
- **Tempo** — literally about timing and rhythm (NEW role)

## Discussion Format

**6 separate subagents** — real discussion, not role-playing. Each agent is spawned with their own session and can build expertise over time.

### Round 1: Independent Reviews
Each agent reviews the script/prototype independently and posts findings. Each ends with a vote:
- **PASS** — no issues in my domain
- **PASS WITH REVISIONS** — good but needs specific changes (list them)
- **FAIL** — fundamental issue that must be fixed

### Round 2: Discussion
Agents respond to EACH OTHER by name. Key tensions:
- **Vex vs Polya** — "That explanation is too long, you'll lose them at 0:45" vs "You can't cut that step, they won't understand the payoff"
- **Rigby vs Vex** — "That simplification is misleading" vs "It's a 60-second video, not a textbook"
- **Tempo vs everyone** — "This script is 95 seconds when spoken naturally, we need to cut 20 seconds"
- **Zara asks questions** → Rigby/Sagan/Polya answer them

### Round 3: Convergence
Concrete numbered revision list compiled. All agents state final vote with reasoning.

| # | Line/Section | Change | Proposed By | Reason |
|---|-------------|--------|-------------|--------|

### Round 4: Final Sign-Off
Brief confirmation that all agree.
- **Consensus:** All 6 sign off
- **Forced consensus:** Majority rules BUT **Rigby has veto power** on mathematical correctness
- **Max rounds:** 4 (then force resolution)

## Output

The Shorts Circle produces:
1. **Revised narration script** — line-by-line with timestamps (group effort)
2. **Title** — optimized for search + curiosity (**Vex owns this**)
3. **Description + hashtags** — keywords, CTA, platform tags (**Vex owns this**)
4. **Pacing notes** — sync points, silence beats, energy markers (**Tempo owns this**)
5. **Circle log** — full discussion record (stored in `circle_logs/shorts/`)

### Deliverable Ownership
| Deliverable | Owner | Others Can... |
|------------|-------|---------------|
| Title | **Vex** | Suggest, but Vex has final call on SEO/hook |
| Description + hashtags | **Vex** | Flag factual errors only |
| Revised script | **Group** | All 6 contribute revisions |
| Pacing notes | **Tempo** | Others flag timing concerns, Tempo synthesizes |
| Math correctness | **Rigby** | Veto power — overrides all |

## Spawn Commands

```bash
# Rigby (Math A — Rigor)
sessions_spawn label=shorts-rigby model=claude-opus-4-6 task="You are Rigby..."

# Sagan (Math B — Breadth)
sessions_spawn label=shorts-sagan model=claude-opus-4-6 task="You are Sagan..."

# Polya (Pedagogy)
sessions_spawn label=shorts-polya model=claude-opus-4-6 task="You are Polya..."

# Zara (Student)
sessions_spawn label=shorts-zara model=claude-sonnet-4-6 task="You are Zara..."

# Vex (Hook & SEO)
sessions_spawn label=shorts-vex model=claude-sonnet-4-6 task="You are Vex..."

# Tempo (Script & Pacing)
sessions_spawn label=shorts-tempo model=claude-sonnet-4-6 task="You are Tempo..."
```

## Cost Estimate Per Short

| Component | Cost |
|-----------|------|
| Rigby (Opus, 1 round) | ~$0.08-0.12 |
| Sagan (Opus, 1 round) | ~$0.08-0.12 |
| Polya (Opus, 1 round) | ~$0.08-0.12 |
| Zara (Sonnet, 1 round) | ~$0.02-0.04 |
| Vex (Sonnet, 1 round) | ~$0.02-0.04 |
| Tempo (Sonnet, 1 round) | ~$0.02-0.04 |
| **Total (4 rounds)** | **~$0.60-1.00** |

Plus TTS + render costs from the main pipeline stages.

## Post-Circle Pipeline: From Script to Masterpiece

The Shorts Circle approves the SCRIPT. Getting from approved script to finished video
requires two more critical phases that are NOT optional.

### Full Short-Form Pipeline

```
STAGE 1: CONCEPT
  Claudio generates topic idea + draft narration script

STAGE 2: SHORTS CIRCLE (6 agents, 4 rounds)
  Rigby, Sagan, Polya, Zara, Vex, Tempo review + revise script
  Output: approved script + pacing notes + title/description

STAGE 3: PROTOTYPE (Claudio only — NO subagents)
  Claudio builds visual-only Manim prototype (no audio)
  Render at 1080×1920 60fps, verify all visual elements
  Clayton reviews prototype → visual corrections
  Iterate until visuals are LOCKED

STAGE 4: AUDIO SYNC (Fourier)
  Fourier generates per-line TTS (Allison voice, style=0.40)
  Fourier applies Tempo's pacing notes:
    - Silence beats between sections
    - Energy markers (which lines need emphasis)
    - Speed adjustments per line if needed
  Fourier produces timing manifest with exact timestamps
  Fourier verifies: total duration within 50-120s constraint

STAGE 5: FINAL RENDER (Claudio only — NO subagents)
  Claudio integrates audio manifest into Manim scene
  Each line's visual timing matched to audio duration via fill()
  ALWAYS render with --flush_cache (stale partial movie files cause audio dropout)
  Claudio screenshots key frames and verifies:
    - Audio sync (narration matches visuals)
    - Visual accuracy (dots on intersections, correct math values)
    - Pacing feels right (not rushed, not dragging)
    - End card present

STAGE 6: FINAL REVIEW (Clayton)
  Clayton watches the full video
  Corrections → back to Stage 5 (audio) or Stage 3 (visual)
  LOCKED when Clayton approves
```

### Critical Rules (Established 2026-03-04)

| Rule | Reason |
|------|--------|
| **Claudio renders ALL Manim scenes — no subagents** | Subagents can't see what they render. Every subagent render today had errors. |
| **Always use `--flush_cache`** | Stale partial movie files caused full audio dropout (21s audio in 88s video) |
| **Prototype visuals BEFORE adding audio** | Get visuals locked with Clayton first, then sync audio. Don't do both at once. |
| **Fourier owns audio/sync** | TTS generation, pacing, timing manifest, sync verification. Not Claudio's job to guess. |
| **Circle reviews scripts, not renders** | The Circle catches script issues. Visual QA is Stage 5-6. Different concerns. |
| **Labels outside graph_group** | Function labels (f(x)=...) must NOT be children of animated groups or they scale/drift during zoom |
| **Tangent lines computed AFTER axes positioning** | axes2.c2p() returns wrong coords if called before .move_to() |

## Relationship to Full Pipeline

The Shorts Circle **replaces** Stages 2-3 (Verification Circle + Lean) for short-form content only:

```
FULL/INSTRUCTOR PATH (unchanged):
  DeepSeek V3 generates script
  → Verification Circle (4 roles, 4 rounds)
  → Lean Writer + Lean 4 Compiler
  → Post-circle passes
  → TTS + Render + Delivery
```
