# DECISIONS.md — Orbital Technical Decisions

*Key decisions and rationale for Orbital's technical stack.*

---

## TTS Provider: Fish Audio S1

**Decision:** Fish Audio S1 over OpenAI TTS, ElevenLabs

**Why:**
- #1 on TTS-Arena2 leaderboard (same price as OpenAI)
- Voice cloning support (unique brand identity)
- Same cost: ~$0.015/1K chars

### Voice Clone Details
- **Reference file:** `clayton_final.mp3`
- **Processing:** Custom EQ profile for 3B1B-style warmth
- **Key adjustment:** "Nuclear nasal cut" (removed nasal frequencies)
- **Post-processing pipeline:** `orbital_factory/audio_postprocess.py`

### Math Pronunciation Fix
- **File:** `tts_test/preprocess_math.py`
- **Problem:** TTS reads "du" as one word, "dx" as "dex"
- **Solution:** Insert space: `du → d u`, `dx → d x`

---

## Script Generation: DeepSeek-V3

**Decision:** DeepSeek-V3 (`deepseek-chat`) over DeepSeek-R1, GPT-4o

**DeepSeek-V3 over R1:**
- Same quality output
- 10x faster (3s vs 30s per problem)
- Reasoning model overkill for math explanations

**DeepSeek over GPT-4o:**
- Same quality output
- 10x cheaper ($0.27/1M input vs $2.50/1M)
- Cost per problem: ~$0.001

### Cost Breakdown
| Service | Rate | Per Problem |
|---------|------|-------------|
| DeepSeek-V3 input | $0.27/1M tokens | ~$0.0005 |
| DeepSeek-V3 output | $1.10/1M tokens | ~$0.0005 |
| Fish Audio S1 | $15/1M UTF-8 bytes | ~$0.015 |
| **Total** | | **~$0.016** |

---

## Prompt Strategy: "Patient Tutor"

**Decision:** Force 15-step detailed breakdowns

**Why:**
- Students need ALL intermediate work shown
- Skipping steps = confusion
- "Patient tutor" persona in system prompt

**Result:** Longer narration, but students actually learn

---

## Video Rendering: Manim (Local)

**Decision:** Render locally with Manim, not cloud

**Why:**
- Zero marginal cost
- Full control over animations
- Same tool as 3Blue1Brown (brand association)
- Celery workers handle queue

---

*Last updated: 2026-02-16*
