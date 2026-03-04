# Video Production Queue
**Owner:** Atlas (Video Production Lead)  
**Updated:** 2026-03-03

---

## Next Up: Derivative Concept Trilogy

### Video A: "What is a Derivative?" (CONCEPTUAL — NO FORMULAS)
**Goal:** After watching, viewer understands WHY derivatives matter before learning any math.
**Duration:** 45-60s
**Tone:** Curiosity-driven, real-world

**Script outline:**
1. Hook: "You've been using derivatives your whole life without knowing it"
2. Speedometer in a car — you're reading a derivative right now (speed = rate of position change)
3. A doctor watching a patient's temperature over time — "is it getting worse faster or slower?"
4. A stock chart — "how fast is the price rising?"
5. All of these are the SAME question: "How fast is something changing at THIS exact moment?"
6. That question has a name — it's called the derivative
7. "In the next videos, we'll show you exactly how to compute it. But first, you need to know what you're looking for."

**Visual ambition (3B1B-level):**
- Animated car on a position-vs-time curve, speedometer needle moves as slope changes
- Temperature curve with a glowing dot sliding along it, tangent line rotating
- Stock chart with animated "steepness indicator"
- These should NOT be static text boxes — they should be Manim animations

---

### Video B: "Secant Lines" (SETUP)
**Goal:** After watching, viewer can draw a secant line and compute its slope.
**Duration:** 45-60s

**Script outline:**
1. Hook: "Before you can find exact speed, you need average speed"
2. Show a curve (x²), pick two points, draw a straight line through them
3. "This line is called a secant line" — label it
4. The slope of this line = average rate of change
5. Show the difference quotient formula: (f(x+h) - f(x)) / h
6. "But average isn't exact. What if we want the speed at ONE moment?"
7. Tease: "That's where the limit comes in — next video"

**Visual ambition:**
- Animated: two dots appear on curve, line draws between them
- Show the rise/run visually on the graph (vertical + horizontal lines)
- h labeled as the horizontal gap, animated to shrink slightly as a tease

---

### Video C: "The Limit Definition" (PAYOFF)
**Goal:** After watching, viewer understands the limit definition of the derivative.
**Duration:** 60-90s

**Script outline:**
1. Hook: "What happens when two points on a curve become one?"
2. Recall secant line from Video B
3. "Now slide the second point closer" — animated, h shrinking
4. As h→0, secant line rotates smoothly into tangent line
5. "This process of letting h approach zero is called taking a limit"
6. Show the formal definition: f'(x) = lim_{h→0} (f(x+h) - f(x)) / h
7. "This gives you the exact slope at a single point — the derivative"
8. "Every rule you'll learn — power rule, chain rule — is just a shortcut for computing this limit"

**Visual ambition (THE KEY ANIMATION):**
- THE signature visual: animated secant→tangent with h shrinking
- Two dots on x², one fixed, one sliding toward it
- Secant line rotates smoothly as dots merge
- h value displayed and counting down: 1.0, 0.5, 0.1, 0.01, 0.001...
- Final tangent line glows green when it "locks in"

---

## Live Playlist: "Derivatives from Scratch"

| # | Video | Duration | Status | YouTube ID |
|---|-------|----------|--------|------------|
| 0a | What is a Derivative? (concept) | ~60s | QUEUED | — |
| 0b | Secant Lines | ~60s | QUEUED | — |
| 0c | The Limit Definition | ~90s | QUEUED | — |
| 1 | The Constant Rule | 59s | ✅ LIVE | WaSbLQewrp8 |
| 2 | The Power Rule | 66s | ✅ LIVE | CVAdvoqXaqw |
| 3 | Negative Exponents | 119s | ✅ LIVE | r-vMVR_3208 |
| 4 | Derivative of 3x²+2x-5 | 103s | ✅ LIVE | lGc-f3--Nas |
| 5 | Fractional Exponents | ~90s | PLANNED | — |

## Future Topics
- Sum/Difference Rule
- Product Rule
- Quotient Rule
- Chain Rule
- Trig Derivatives
- Implicit Differentiation
- Related Rates

---

## Tutorials (Long-Form)

| Video | Duration | Status | YouTube ID |
|-------|----------|--------|------------|
| Group Order 15 | 5:30 | ✅ LIVE | USmfu88O0ew |
| Dedekind Cuts | 4:45 | ✅ LIVE | x1fx09DyKx4 |
