# Meridian Promo V4 — Timing Plan

## Proven Timing Model (from settings.json)
1. Build mobject + position (NO timeline cost)
2. self.add_sound(audio_path) — audio starts HERE
3. FadeOut(previous, 0.4s) — voice plays over fadeout
4. Write/Create(new, anim_time) — begins ~0.4s into audio
5. self.wait(remaining) — hold until voice done
6. self.wait(EXTRA_HOLD=0.5) — breathing room

## Key Rule
- anim_time = max(1.2, duration * 0.35)
- Each scene's total time = audio_duration + EXTRA_HOLD

## Approach for Promo
Since we have ONE continuous audio file (not per-step audio), we need to:
1. Split the TTS into individual segment audio files (one per script line)
2. Use self.add_sound() for EACH segment at the right moment
3. Each visual act plays its audio, animates, holds, then transitions

## Audio Split Plan
From silence detection of meridian_promo_v3.mp3 (65s total):

| Segment | Time Range | Text | Duration |
|---------|-----------|------|----------|
| 1 | 0.0-2.1 | "Every student learns at a different pace." | 2.1s |
| 2 | 2.7-5.2 | "The problem is, most math programs don't." | 2.5s |
| 3 | 6.4-8.6 | "One textbook. One speed." | 2.2s |
| 4 | 9.3-10.4 | "And if you miss a step," | 1.1s |
| 5 | 11.5-12.4 | "good luck catching up." | 0.9s |
| 6 | 13.6-15.8 | "We built Meridian to fix that." | 2.2s |
| 7 | 17.2-20.8 | "Complete math programs with digital textbooks, video walkthroughs," | 3.6s |
| 8 | 22.2-29.8 | "thousands of practice problems, and a personal AI tutor that adapts to EVERY student." | 7.6s |
| 9 | 30.4-34.4 | "When a student gets stuck, the AI tutor meets them right where they are." | 4.0s |
| 10 | 35.0-35.7 | "Step by step." | 0.7s |
| 11 | 36.3-38.8 | "No judgment. No falling through the cracks." | 2.5s |
| 12 | 39.4-43.1 | "Teachers get real-time dashboards showing exactly where each student needs help," | 3.7s |
| 13 | 43.6-45.5 | "not just a grade at the end of the unit." | 1.9s |
| 14 | 46.1-47.8 | "Pre-Algebra through Calculus." | 1.7s |
| 15 | 48.3-50.1 | "Every course built on one platform." | 1.8s |
| 16 | 50.7-52.7 | "Not a textbook with a website bolted on." | 2.0s |
| 17 | 53.3-56.4 | "A complete system built by educators who have been in the classroom." | 3.1s |
| 18 | 57.0-60.8 | "Because every student deserves a program that actually meets them where they are." | 3.8s |
| 19 | 61.5-62.2 | "Meridian Math." | 0.7s |
| 20 | 62.9-65.0 | "Mathematics for every student." | 2.1s |

## Visual Acts (FEWER, BETTER, LONGER)

### Act 0: Collab Intro (add before audio starts — 3s pre-roll)
- Meridian × Orbital particle reveal
- Music starts here

### Act 1: Student Pace (segments 1-2, ~5s)
- Three students on number line, different speeds
- Curriculum pace line sweeps through
- HOLD while voice finishes

### Act 2: Domino Effect (segments 3-5, ~5s)
- Sequential lesson blocks
- One goes red → chain reaction
- Simpler than before, but more impactful

### Act 3: Meridian Logo Reveal (segment 6, ~3s)
- Particle implosion → MERIDIAN MATH appears
- Clean, confident, hold on it

### Act 4: Four Pillars (segments 7-8, ~11s)
- This is the LONGEST section — take our time
- Each pillar appears with a mini demo
- Connect them at the end
- Riemann sum montage fits here as a "video lesson" preview

### Act 5: AI Tutor Demo (segments 9-11, ~7s)
- Problem stuck → AI walks through it
- Step by step solution
- Answer celebration

### Act 6: Teacher Dashboard (segments 12-13, ~6s)
- Dashboard frame appears
- Bars grow
- Alert on struggling students

### Act 7: Course Spectrum (segments 14-15, ~4s)
- Pre-Algebra → Calculus cards
- ONE PLATFORM line

### Act 8: Not Bolted On (segments 16-17, ~5s)
- Traditional vs Meridian side-by-side
- ✗ vs ✓

### Act 9: Emotional Closer (segment 18, ~4s)
- "Every student. Every level. One program that adapts."

### Act 10: End Card (segments 19-20, ~5s + hold)
- Lissajous + MERIDIAN MATH + meridian-math.org
- Hold until music fades

## TTS Settings for V4
Need MORE style/warmth. Adjust:
- stability: 0.38 (more expression)
- similarity_boost: 0.65
- style: 0.55 (way more personality/warmth)
- speed: 0.93
- use_speaker_boost: true

## Better Approach: Use ONE audio file + precise self.wait() timing
Instead of splitting, use the ONE mp3 with self.add_sound() at time 0, 
then use precise self.wait() calls based on the timing map above.
This avoids 20 split files and potential sync drift.

The key: after self.add_sound(full_audio), the Manim timeline IS the audio timeline.
Just make sure total animation time per act matches the audio segment duration.
