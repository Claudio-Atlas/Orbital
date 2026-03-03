# Stage 3: Lean Formalization — Contract
**Owner:** Euclid (Opus → Lean 4 Compiler)
**Last Updated:** 2026-03-02

---

## Purpose
Formally verify the mathematical claims in a Stage 2 revised script using Lean 4 + Mathlib. The Lean 4 compiler is the real verification gate — deterministic and trustworthy. Opus writes the Lean code; the compiler proves it correct.

## When to Run

| Problem Type | Lean Required? | Rationale |
|---|---|---|
| Formal proofs (group theory, analysis, topology) | ✅ Always | Core value prop — "Lean 4 Verified" badge |
| Calculus (integrals, derivatives, series) | ⚠️ Key claims only | Verify final answer (e.g., HasDerivAt), skip intermediate algebra |
| Algebra/trig (solve, simplify, factor) | ❌ Skip | Circle is sufficient, Lean adds cost without value |
| Conceptual/explanatory | ❌ Skip | Nothing to formally verify |

**Professor override:** Dashboard checkbox "Verify with Lean 4" — defaults based on problem type, professor can toggle on/off.

## Architecture

```
Stage 2 (revised script)
    ↓
Classification: Does this need Lean?
    ├── NO  → Skip to Stage 4 (TTS), badge = "AI Verified ✓"
    └── YES → Opus writes Lean → Compiler verifies
                 ├── PASS  → Stage 4, badge = "Lean 4 Verified ✓"
                 └── FAIL  → Opus rewrites (up to 3 attempts)
                               └── Still fails → Flag for human review
```

## Model Assignment

| Component | Model | Purpose |
|-----------|-------|---------|
| Lean Writer | claude-opus-4 | Write Lean 4 formalizations from script claims |
| Lean 4 Compiler | deterministic | The real gate — compiles or it doesn't |
| Future: Goedel | local (Mac Mini #2) | Free alternative to Opus for Lean writing |

## Process

### Step 1: Extract Claims
From the revised script, identify formalizable mathematical claims:
- Final answer / result
- Key intermediate results (intersection points, inequalities, identities)
- Theorem statements (for proof-type problems)

**Example (Area Between Curves):**
```
Claim 1: Intersections at x = -1 and x = 2
Claim 2: x + 2 ≥ x² on (-1, 2)
Claim 3: ∫₋₁² (x + 2 - x²) dx = 9/2
```

### Step 2: Write Lean 4
Opus generates a `.lean` file with:
- Import Mathlib
- One theorem per claim
- Proofs using Mathlib tactics (norm_num, ring, linarith, HasDerivAt, etc.)

**Prompt template:**
```
You are Euclid, a Lean 4 formalization expert for Orbital.

Write a Lean 4 file that formally verifies the following mathematical claims from a video script. Use Mathlib v4.28.0.

CLAIMS TO VERIFY:
{claims}

REQUIREMENTS:
- Import only from Mathlib
- One theorem per claim, clearly named
- Use standard tactics: norm_num, ring, linarith, simp, exact?, apply?
- If exact?/apply? would find the right lemma, use the fallback pattern:
  `by exact?` then replace with the discovered lemma
- Keep proofs minimal — we need compilation, not elegance
- Add comments explaining what each theorem verifies

Output ONLY the .lean file contents.
```

### Step 3: Compile
```bash
cd orbital_factory/lean_verifier
# Write the file
cat > Verifier/Claims.lean << 'EOF'
{lean_code}
EOF
# Build
lake build 2>&1
```

**Success:** Exit code 0, all theorems compile → PASS
**Failure:** Compilation errors → extract error messages, send back to Opus

### Step 4: Retry on Failure (up to 3 attempts)
If compilation fails, send Opus the error message with context:
```
Your Lean 4 code failed to compile. Fix it.

ERROR:
{compiler_error}

ORIGINAL CODE:
{lean_code}

Common fixes:
- exact? fallback for unknown lemma names
- apply? for type mismatches
- Check import paths against Mathlib v4.28.0
```

### Step 5: Output

**On PASS:**
```json
{
  "verified": true,
  "badge": "lean4",
  "claims_verified": 3,
  "lean_file": "Verifier/Claims.lean",
  "attempts": 1,
  "compiler_output": "Build completed successfully."
}
```

**On FAIL (after 3 attempts):**
```json
{
  "verified": false,
  "badge": "circle_only",
  "claims_attempted": 3,
  "claims_failed": ["claim_3_integral_value"],
  "last_error": "...",
  "recommendation": "Flag for human review or proceed with circle-only verification"
}
```

## Input

From Stage 2:
```json
{
  "revised_script": "<Stage 2 output JSON>",
  "problem": "<original problem statement>",
  "course": "<course level>",
  "known_answer": "<expected answer>",
  "lean_requested": true | false
}
```

## Output

To Stage 4:
```json
{
  "revised_script": "<unchanged from Stage 2>",
  "verification": {
    "method": "lean4" | "circle_only" | "skipped",
    "badge": "lean4_verified" | "ai_verified" | "none",
    "claims_verified": 3,
    "lean_file": "path/to/file.lean" | null,
    "details": "..."
  }
}
```

## Verification Infrastructure

- **Lean verifier project:** `orbital_factory/lean_verifier/`
- **Lean version:** 4.28.0
- **Mathlib version:** 4.28.0
- **lakefile.toml:** lib name `Verifier`
- **Mathlib cache:** 8,010 olean files (pre-built, fast compilation)
- **Future: Lean server mode** — keeps Mathlib in memory for sub-second compilation at scale

## Proof Templates (Future Optimization)

For standard calc problems, build a library of reusable Lean templates:
- `derivative_verification.lean` — swap in function + expected derivative
- `integral_verification.lean` — swap in bounds + integrand + result
- `intersection_verification.lean` — swap in functions + x-values

This reduces Opus calls for common problem types. Best bang for buck at scale.

## Cost Estimate

| Component | Cost |
|-----------|------|
| Opus writes Lean (1 attempt) | ~$0.08 |
| Opus retry (if needed, avg 0.5 retries) | ~$0.04 |
| Lean compilation | Free (local) |
| **Total per video (when enabled)** | **~$0.10** |

Skipped videos: $0.00

## Verification Badges

Videos display one of:
- 🏛️ **"Lean 4 Verified"** — formally proven correct (proofs, key calc results)
- ✅ **"AI Verified"** — passed Verification Circle but no Lean (algebra, conceptual)
- No badge — verification skipped or pending

---

## Integration Notes

- Stage 3 receives: revised script + verification request from Stage 2
- Stage 3 outputs to: Stage 4 (TTS) with verification metadata
- Lean files are saved in `lean_verifier/Verifier/` for audit trail
- If Lean fails after 3 attempts, pipeline continues with "AI Verified" badge (circle already passed)
- Professor dashboard shows verification status in real-time during generation
