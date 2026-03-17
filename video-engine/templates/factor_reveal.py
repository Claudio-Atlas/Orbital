"""
templates/factor_reveal.py — Factoring Video Template
=======================================================
Handles polynomial factoring questions. Shows the original expression,
works through the factoring process step by step, and verifies the answer
by expanding the factored form.

Supported question templateIds:
  - factor-quadratic
  - factor-quadratic-leading-1
  - factor-quadratic-leading-a
  - factor-gcf
  - factor-difference-of-squares
  - factor-sum-cubes
  - factor-difference-cubes
  - factor-by-grouping
  - factor-*

Input example:
    {
        "templateId": "factor-quadratic-leading-1",
        "questionText": "Factor: x² + 5x + 6",
        "correctAnswer": "(x + 2)(x + 3)",
        "solution": "Step 1: Find two numbers that multiply to 6 and add to 5.\\nFactors of 6: (1,6), (2,3)\\n2 + 3 = 5 ✓\\nStep 2: Write the factored form.\\nx² + 5x + 6 = (x + 2)(x + 3)\\nStep 3: Verify.\\n(x + 2)(x + 3) = x² + 3x + 2x + 6 = x² + 5x + 6 ✓",
        "difficulty": "medium",
        "skill": "factoring-quadratics"
    }

Output manifest structure:
    [
        { "type": "box",           "content": "Factoring Quadratics" },
        { "type": "math",          "content": "x^2 + 5x + 6" },         # show expression
        { "type": "algebra_solve", ... },                                # factor step-by-step
        { "type": "math",          "content": "(x+2)(x+3)" },           # reveal factored form
        { "type": "algebra_solve", ... },                                # verify by expanding
        { "type": "box",           "content": "(x + 2)(x + 3)" },       # final answer
    ]
"""

import re
from templates.base import VideoTemplate, NEON_GREEN, ORBITAL_CYAN, ORANGE_ACCENT, BOX_BORDER
from templates.algebra_solve import parse_solution, latex_for_equation, text_to_latex


class FactorRevealTemplate(VideoTemplate):
    """
    Video template for polynomial factoring questions.

    The "reveal" structure shows:
      1. The unfactored expression
      2. The search process (finding factor pairs)
      3. The factored form revealed
      4. Verification by expansion (shows it multiplies back correctly)
      5. Final answer

    This two-part structure (factor + verify) is pedagogically important:
    students learn that factoring is always reversible.
    """

    template_id = "factor-reveal"

    supported_template_ids = [
        "factor-quadratic",
        "factor-quadratic-leading-1",
        "factor-quadratic-leading-a",
        "factor-gcf",
        "factor-difference-of-squares",
        "factor-perfect-square",
        "factor-sum-cubes",
        "factor-difference-cubes",
        "factor-by-grouping",
        "factor-trinomial",
        "factor-*",
    ]

    INTRO_DURATION   = 3.0
    SEARCH_DURATION  = 3.5
    REVEAL_DURATION  = 4.0
    VERIFY_DURATION  = 3.5
    ANSWER_DURATION  = 4.0

    def generate_manifest(self, question_data: dict) -> list[dict]:
        """Convert a factoring question into a Manim manifest."""
        question_text = question_data.get("questionText", "")
        solution_str  = question_data.get("solution", "")
        answer        = question_data.get("correctAnswer", "")
        difficulty    = question_data.get("difficulty", "medium")
        skill         = question_data.get("skill", "factoring")
        template_id   = question_data.get("templateId", "")

        # Extract the expression to factor
        expression = _extract_expression(question_text)
        expression_latex = _expression_to_latex(expression)

        # Parse the solution
        parsed_steps = parse_solution(solution_str)

        # Build manifest
        manifest = []

        # ── Step 1: Skill Header ───────────────────────────────────────────
        skill_label = skill.replace('-', ' ').title() if skill else "Factoring"
        manifest.append({
            "type": "box",
            "content": skill_label,
            "duration": self.INTRO_DURATION,
            "narration": f"Let's factor a {skill_label.lower()} expression.",
            "metadata": {"role": "intro_header", "difficulty": difficulty},
        })

        # ── Step 2: Show the Expression ────────────────────────────────────
        manifest.append({
            "type": "math",
            "content": expression_latex,
            "duration": self.INTRO_DURATION + 0.5,
            "narration": f"We need to factor {expression}.",
            "metadata": {"role": "expression_display", "raw": expression},
        })

        # ── Step 3: Factoring Walkthrough (algebra_solve) ──────────────────
        # Split steps: factoring steps vs verification steps
        factor_steps, verify_steps = _split_factor_verify_steps(parsed_steps, answer)

        if factor_steps:
            factor_substeps = _build_algebra_substeps(
                expression_latex, factor_steps, self.SEARCH_DURATION
            )
            # Combine sub-step narrations for TTS (Bible: one call per scene)
            combined_factor_narration = " ".join(
                s["narration"] for s in factor_substeps if s.get("narration")
            )
            manifest.append({
                "type": "algebra_solve",
                "algebra_solve": {
                    "title": "Factoring Process",
                    "steps": factor_substeps,
                    "final_color": ORBITAL_CYAN,
                },
                "duration": sum(s["duration"] for s in factor_substeps),
                "narration": combined_factor_narration or "Working through the factoring process.",
                "metadata": {"role": "factoring_walkthrough"},
            })

        # ── Step 4: Factored Form Reveal ────────────────────────────────────
        answer_latex = _expression_to_latex(answer)
        manifest.append({
            "type": "math",
            "content": answer_latex,
            "duration": self.REVEAL_DURATION,
            "narration": f"The factored form is {answer}.",
            "metadata": {"role": "factored_form_reveal"},
        })

        # ── Step 5: Verification (expand back) ────────────────────────────
        if verify_steps:
            verify_substeps = _build_verification_substeps(
                answer, expression, verify_steps, self.VERIFY_DURATION
            )
            if verify_substeps:
                combined_verify_narration = " ".join(
                    s["narration"] for s in verify_substeps if s.get("narration")
                )
                manifest.append({
                    "type": "algebra_solve",
                    "algebra_solve": {
                        "title": "Verify by Expanding",
                        "steps": verify_substeps,
                        "final_color": NEON_GREEN,
                    },
                    "duration": sum(s["duration"] for s in verify_substeps),
                    "narration": combined_verify_narration or "Let's verify by expanding the factored form.",
                    "metadata": {"role": "verification"},
                })
        else:
            # Always show at least a basic verification
            verify_substeps = _build_basic_verification(answer, expression, self.VERIFY_DURATION)
            combined_verify_narration = " ".join(
                s["narration"] for s in verify_substeps if s.get("narration")
            )
            manifest.append({
                "type": "algebra_solve",
                "algebra_solve": {
                    "title": "Verify",
                    "steps": verify_substeps,
                    "final_color": NEON_GREEN,
                },
                "duration": sum(s["duration"] for s in verify_substeps),
                "narration": combined_verify_narration or "Check: expanding the factored form gives back the original.",
                "metadata": {"role": "verification"},
            })

        # ── Step 6: Final Answer ────────────────────────────────────────────
        manifest.append({
            "type": "box",
            "content": answer,
            "duration": self.ANSWER_DURATION,
            "narration": f"The answer is {answer}.",
            "metadata": {"role": "answer_reveal", "answer": answer},
        })

        return manifest

    def validate_question(self, question_data: dict) -> bool:
        """Factoring needs questionText with an expression and a correctAnswer."""
        qt = question_data.get("questionText", "")
        ans = question_data.get("correctAnswer", "")
        return bool(qt) and bool(ans)


# ─── Expression Helpers ───────────────────────────────────────────────────────

def _extract_expression(question_text: str) -> str:
    """Extract the expression to factor from question text."""
    # Strip "Factor: " or "Factor completely: " prefix
    prefixes = [
        r'^Factor\s+completely\s*:\s*',
        r'^Factor\s+the\s+expression\s*:\s*',
        r'^Factor\s*:\s*',
        r'^Completely\s+factor\s*:\s*',
    ]
    text = question_text.strip()
    for pattern in prefixes:
        text = re.sub(pattern, '', text, flags=re.IGNORECASE)
    return text.strip()


def _expression_to_latex(expr: str) -> str:
    """Convert an expression string to LaTeX."""
    # Handle unicode superscripts
    expr = expr.replace('²', '^2').replace('³', '^3')
    # x^2 → x^{2} for proper LaTeX rendering (optional, MathTex handles x^2 fine)
    # Handle explicit multiplication
    expr = re.sub(r'(\d)\s*\*\s*([a-zA-Z])', r'\1\2', expr)
    # sqrt
    expr = re.sub(r'sqrt\(([^)]+)\)', r'\\sqrt{\1}', expr)
    return expr


def _split_factor_verify_steps(
    parsed_steps: list[dict],
    answer: str
) -> tuple[list[dict], list[dict]]:
    """
    Split parsed solution steps into factoring steps and verification steps.

    Verification steps are those that involve "verify", "check", or "expand".
    """
    factor_steps = []
    verify_steps = []
    in_verify = False

    for step in parsed_steps:
        note = step.get("note", "").lower()
        if any(kw in note for kw in ["verify", "check", "expand", "foil", "distribute"]):
            in_verify = True

        if in_verify:
            verify_steps.append(step)
        else:
            factor_steps.append(step)

    return factor_steps, verify_steps


def _build_algebra_substeps(
    start_latex: str,
    steps: list[dict],
    step_duration: float,
) -> list[dict]:
    """Build algebra_solve sub-steps from parsed factor steps."""
    substeps = []

    # Start with the original expression
    substeps.append({
        "latex": start_latex,
        "note": "Factor this expression",
        "note_color": ORBITAL_CYAN,
        "duration": step_duration,
        "narration": f"We need to factor this expression.",
    })

    for step in steps:
        note = step.get("note", "")
        equations = step.get("equations", [])

        for i, eq_str in enumerate(equations):
            eq_latex = _expression_to_latex(
                latex_for_equation(eq_str) if '=' in eq_str else eq_str
            )
            substeps.append({
                "latex": eq_latex,
                "note": note if i == 0 else "",
                "note_color": ORANGE_ACCENT if i == 0 else ORBITAL_CYAN,
                "duration": step_duration,
                "narration": f"{note}: {eq_str}" if note and i == 0 else eq_str,
            })

    return substeps


def _build_verification_substeps(
    factored: str,
    original: str,
    steps: list[dict],
    step_duration: float,
) -> list[dict]:
    """Build verification sub-steps (expand back to original)."""
    factored_latex = _expression_to_latex(factored)
    original_latex = _expression_to_latex(original)

    substeps = [{
        "latex": factored_latex,
        "note": "Expand to verify",
        "note_color": ORANGE_ACCENT,
        "duration": step_duration,
        "narration": f"Starting with the factored form {factored}.",
    }]

    for step in steps:
        equations = step.get("equations", [])
        note = step.get("note", "")
        for i, eq_str in enumerate(equations):
            eq_latex = _expression_to_latex(eq_str)
            substeps.append({
                "latex": eq_latex,
                "note": note if i == 0 else "",
                "note_color": NEON_GREEN,
                "duration": step_duration,
                "narration": eq_str,
            })

    # Ensure last step shows the original expression (closing the loop)
    substeps.append({
        "latex": original_latex,
        "note": "✓ Matches original",
        "note_color": NEON_GREEN,
        "duration": step_duration + 0.5,
        "narration": f"This matches our original expression. Factoring verified.",
    })

    return substeps


def _build_basic_verification(
    factored: str,
    original: str,
    step_duration: float,
) -> list[dict]:
    """Build a minimal verification showing factored → expanded = original."""
    factored_latex = _expression_to_latex(factored)
    original_latex = _expression_to_latex(original)

    return [
        {
            "latex": factored_latex,
            "note": "Expand to check",
            "note_color": ORANGE_ACCENT,
            "duration": step_duration,
            "narration": f"Let's expand {factored} to verify.",
        },
        {
            "latex": f"{factored_latex} = {original_latex}",
            "note": "✓ Correct",
            "note_color": NEON_GREEN,
            "duration": step_duration + 0.5,
            "narration": f"Expanding gives back the original. Verified.",
        },
    ]
