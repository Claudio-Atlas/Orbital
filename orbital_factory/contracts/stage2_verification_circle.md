# Stage 2: Verification Circle — Contract
**Owner:** Verification Circle (3 Opus + 1 Sonnet)
**Last Updated:** 2026-03-02

---

## Purpose
Review a Stage 1 script for mathematical correctness, pedagogical quality, and student comprehension. Output a revised script ready for Stage 3 (Lean formalization).

## Model Assignments

| Role | Model | Focus |
|------|-------|-------|
| **Mathematician A (Rigor)** | claude-opus-4 | Verify every computation, check logical flow, flag notation errors |
| **Mathematician B (Breadth)** | claude-opus-4 | Sanity-check answer, consider alternative approaches, edge cases |
| **Pedagogy Expert** | claude-opus-4 | Evaluate explanation clarity, pacing, narration tone, common mistakes |
| **Student Simulator** | claude-sonnet-4 | Read as a student: what's confusing? where do you get lost? |

**Why 3 Opus + 1 Sonnet:** Mathematicians and Pedagogy make *judgments* requiring deep reasoning. The Student asks *questions* — Sonnet is sufficient and keeps costs down.

## Protocol: Single Session, 4 Rounds

The entire circle runs in **ONE session** with one model playing all 4 roles across 4 structured rounds. This ensures agents reference each other, debate, and converge — not 4 independent reviews.

### Round 1: Independent Reviews
Each agent reviews the script independently and posts findings.

**Format per agent:**
```
## [Role Name] — Round 1 Review

### Findings
- [Finding 1: description, affected step(s)]
- [Finding 2: ...]

### Vote: [PASS | PASS WITH REVISIONS | FAIL]
```

### Round 2: Cross-Discussion
Agents **respond to each other** by name.
- Mathematicians debate contested findings
- Student asks questions about confusing steps → Mathematicians answer
- Pedagogy proposes specific narration text for flagged steps
- Agents may change their initial positions based on discussion

### Round 3: Convergence
- Compile a concrete, enumerated revision list
- Each agent states their final vote
- Each change must have a reason

**Format:**
```
## Revision List

| # | Step(s) | Change | Reason |
|---|---------|--------|--------|
| 1 | ...     | ...    | ...    |

### Final Votes
- Mathematician A: [VOTE]
- Mathematician B: [VOTE]
- Pedagogy Expert: [VOTE]
- Student Simulator: [VOTE]
```

### Round 4: Final Consensus
- Brief confirmation of the final verdict
- Summary of Changes table (matches Round 3)
- If PASS or PASS WITH REVISIONS → output the revised script JSON
- If FAIL → list blocking issues that must be resolved before re-submission

## Input

**Required:**
```json
{
  "script": "<Stage 1 script JSON (array of steps)>",
  "problem": "<original problem statement>",
  "course": "<course level, e.g., MAT-230 Calculus 2>",
  "detail_level": "quick | standard | detailed",
  "known_answer": "<expected answer if available, for sanity check>"
}
```

## Output

**Circle Log** (markdown, saved to `memory/circle-log-{slug}.md`):
- Full transcript of all 4 rounds
- Revision table
- Final votes and verdict

**Revised Script** (JSON, saved to `scripts/{slug}_revised.json`):
- Same schema as Stage 1 output
- All revisions applied
- Ready for Stage 3 (Lean formalization)

## Verdict Definitions

| Verdict | Meaning | Action |
|---------|---------|--------|
| **PASS** | No changes needed | Proceed to Stage 3 |
| **PASS WITH REVISIONS** | Changes needed, all enumerated | Apply revisions, proceed to Stage 3 |
| **FAIL** | Fundamental errors (wrong answer, broken logic, unsalvageable structure) | Return to Stage 1 for regeneration |

## Quality Gates

The circle MUST catch:
- [ ] Incorrect computations (wrong arithmetic, sign errors)
- [ ] Logical gaps (steps that don't follow from previous)
- [ ] Notation inconsistencies (LaTeX display ≠ narration)
- [ ] Missing justifications (why, not just what)
- [ ] Pedagogical anti-patterns (jargon without explanation, steps too large)
- [ ] Student confusion points (double negatives, ambiguous notation)

## Cost Estimate

| Component | Cost |
|-----------|------|
| Round 1 (4 reviews) | ~$0.20 |
| Rounds 2-4 (discussion + consensus) | ~$0.40 |
| **Total per circle** | **~$0.60** |

Input: ~2K tokens (script). Output: ~4-6K tokens (full log + revised script).

## Professor Bypass Option

Professors can optionally **skip the circle** and review/edit scripts themselves. This saves ~$0.60/video but trades AI verification for human review. The pipeline UI should offer:
- "Auto-verify (recommended)" → runs full circle
- "I'll review it myself" → shows script editor, professor approves

## Prompt Template

```
You are running a Verification Circle for Orbital, an AI math video generator.

You will play 4 roles across 4 rounds: Mathematician A (Rigor), Mathematician B (Breadth), Pedagogy Expert, and Student Simulator.

PROBLEM: {problem}
COURSE: {course}
EXPECTED ANSWER: {known_answer}
DETAIL LEVEL: {detail_level}

SCRIPT TO REVIEW:
{script_json}

Run the circle now. For each round, write each agent's contribution under a clear header. Agents should reference each other by name in Rounds 2-4. End with the revision table and revised script JSON.
```

## Examples

See verified circle logs:
- `memory/circle-log-area-between-curves.md` (Area between curves, 7 revisions, PASS WITH REVISIONS)
- `Desktop/Verification-Circle-Log.pdf` (Group Order 15, original reference implementation)

---

## Integration Notes

- Stage 2 receives output from Stage 1 (script JSON)
- Stage 2 outputs to Stage 3 (revised script → Lean formalization)
- Circle log is saved for audit trail and professor review
- If verdict is FAIL, pipeline returns to Stage 1 with failure reasons attached to the regeneration prompt
