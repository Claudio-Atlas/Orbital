"""
templates/algebra_solve.py — Solve-for-X Video Template
=========================================================
Handles any "Solve for x" question from the Axiom Question Engine.
Produces a landscape 16:9 instructional video showing step-by-step
equation solving using scene_short.py's proven `algebra_solve` scene type.

Supported question templateIds:
  - solve-linear-1step
  - solve-linear-2step
  - solve-linear-any
  - solve-multistep
  - solve-with-fractions
  - solve-with-distributive
  - linear-equation-*
  - (anything containing "solve" or "linear" that isn't graphing/factoring)

Input example:
    {
        "templateId": "solve-linear-1step",
        "questionText": "Solve: 3x + 7 = 22",
        "correctAnswer": "5",
        "solution": "Step 1: Subtract 7 from both sides.\\n3x + 7 - 7 = 22 - 7\\n3x = 15\\nStep 2: Divide both sides by 3.\\nx = 15/3\\nx = 5",
        "difficulty": "easy",
        "skill": "linear-equations"
    }

Output manifest structure:
    [
        { "type": "box",          "content": "Solve for x",    ... },  # problem header
        { "type": "math",         "content": "3x + 7 = 22",    ... },  # problem equation
        { "type": "algebra_solve", "algebra_solve": { steps }, ... },  # solution walkthrough
        { "type": "box",          "content": "Answer: x = 5",  ... },  # answer reveal
    ]

Architecture notes:
  - The `algebra_solve` step type in scene_short.py shows equations building
    up on screen in whiteboard style — each sub-step animates Write()
  - narration fields are included as metadata for future TTS integration
  - LaTeX conversion is deterministic: same input always produces same output
"""

import re
from templates.base import VideoTemplate, NEON_GREEN, ORBITAL_CYAN, ORANGE_ACCENT


# ─── LaTeX Utilities ─────────────────────────────────────────────────────────

def text_to_latex(text: str) -> str:
    """
    Convert a plain-text math expression to valid LaTeX for MathTex().

    Handles the most common patterns from Axiom solution strings:
      - "15/3"       → "\\frac{15}{3}"
      - "x/2"        → "\\frac{x}{2}"
      - "a/b"        → "\\frac{a}{b}"  (where a,b can be expressions)
      - "x^2"        → "x^2" (already valid LaTeX)
      - "sqrt(x)"    → "\\sqrt{x}"
      - "+-"         → keeps as-is (LaTeX handles it)
      - "3*x"        → "3x" (remove explicit multiplication dot)

    Note: We intentionally keep it simple — complex expressions may need
    manual LaTeX in the question data's solution field.
    """
    text = text.strip()

    # Handle sqrt(...)
    text = re.sub(r'sqrt\(([^)]+)\)', r'\\sqrt{\1}', text, flags=re.IGNORECASE)

    # Handle simple fractions: integer/integer or variable/integer
    # e.g. "15/3" → "\frac{15}{3}", "x/3" → "\frac{x}{3}"
    # But NOT "Step 1:" style or URLs — only when surrounded by math chars
    # Pattern: word-chars / word-chars (not preceded/followed by :)
    def fraction_replace(m: re.Match) -> str:
        num = m.group(1)
        den = m.group(2)
        # Skip if either part looks like it's not a math term
        if any(c in num + den for c in [':', ' ', '\n']):
            return m.group(0)
        return f'\\frac{{{num}}}{{{den}}}'

    # Simple numeric fractions: digits / digits
    text = re.sub(r'\b(\d+)\s*/\s*(\d+)\b', fraction_replace, text)

    # Variable/number fractions: like "x/2", "3x/4", "2x/3"
    text = re.sub(r'\b([a-zA-Z]\w*)\s*/\s*(\d+)\b', fraction_replace, text)

    # Remove explicit * for multiplication (3*x → 3x, but keep spacing)
    text = re.sub(r'(\w)\s*\*\s*([a-zA-Z])', r'\1\2', text)

    return text


def latex_for_equation(eq: str) -> str:
    """
    Convert a full equation string to LaTeX.
    Applies text_to_latex to each side of an equation.

    Examples:
        "x = 15/3" → "x = \\frac{15}{3}"
        "3x + 7 - 7 = 22 - 7" → "3x + 7 - 7 = 22 - 7"
    """
    if '=' in eq:
        parts = eq.split('=', 1)
        lhs = text_to_latex(parts[0].strip())
        rhs = text_to_latex(parts[1].strip())
        return f"{lhs} = {rhs}"
    else:
        return text_to_latex(eq)


# ─── Solution Parser ──────────────────────────────────────────────────────────

def parse_solution(solution_str: str) -> list[dict]:
    """
    Parse an Axiom solution string into structured step data.

    Handles multiple formats:
      Format 1 — "Step N:" delimited:
          "Step 1: Subtract 7.\\n3x + 7 - 7 = 22 - 7\\n3x = 15\\nStep 2: ..."
      Format 2 — Numbered "1." style:
          "1. Subtract 7 from both sides\\n   3x = 15\\n2. Divide..."
      Format 3 — Plain equations, one per line:
          "3x + 7 = 22\\n3x = 15\\nx = 5"

    Returns:
        List of dicts: [{"note": str, "equations": [str]}, ...]
        Each dict represents one logical step.
        Equations are raw strings (LaTeX conversion happens in manifest builder).
    """
    solution_str = solution_str.strip()
    steps = []

    # ── Format 1: "Step N:" delimited ─────────────────────────────────────
    step_matches = list(re.finditer(
        r'Step\s+\d+\s*:\s*(.+?)(?=\nStep\s+\d+|\Z)',
        solution_str,
        flags=re.IGNORECASE | re.DOTALL
    ))

    if step_matches:
        for m in step_matches:
            content = m.group(1).strip()
            lines = [l.strip() for l in content.split('\n') if l.strip()]
            if not lines:
                continue
            # First line is the description/note; remaining lines are equations
            note = lines[0].rstrip('.')
            equations = [l for l in lines[1:] if l and not l.startswith('Step')]
            steps.append({"note": note, "equations": equations})
        return steps

    # ── Format 2: "1." or "1)" numbered ───────────────────────────────────
    numbered_matches = list(re.finditer(
        r'^\d+[.)]\s*(.+?)(?=\n\d+[.)]|\Z)',
        solution_str,
        flags=re.MULTILINE | re.DOTALL
    ))

    if numbered_matches:
        for m in numbered_matches:
            content = m.group(1).strip()
            lines = [l.strip() for l in content.split('\n') if l.strip()]
            if not lines:
                continue
            note = lines[0].rstrip('.')
            equations = lines[1:] if len(lines) > 1 else []
            steps.append({"note": note, "equations": equations})
        return steps

    # ── Format 3: Plain equations, one per line ─────────────────────────
    # No step markers — treat each line as either an equation or a note
    lines = [l.strip() for l in solution_str.split('\n') if l.strip()]
    equations = []
    current_note = ""

    for line in lines:
        # Heuristic: if line contains "=" it's an equation; otherwise a note/annotation
        if '=' in line or re.match(r'^[\d\s(]', line):
            equations.append(line)
        else:
            # It's a text note — group with the next equations
            if equations:
                # Save accumulated equations as a step
                steps.append({"note": current_note, "equations": equations})
                equations = []
            current_note = line

    # Flush remaining equations
    if equations:
        steps.append({"note": current_note, "equations": equations})

    # If we found nothing useful, treat the whole thing as equations
    if not steps:
        steps = [{"note": "", "equations": lines}]

    return steps


def extract_question_equation(question_text: str) -> str:
    """
    Extract the math equation from a question text string.

    Examples:
        "Solve: 3x + 7 = 22"      → "3x + 7 = 22"
        "Solve for x: 2x - 5 = 9" → "2x - 5 = 9"
        "Find x when 4x = 20"     → "4x = 20"
        "3x + 7 = 22"             → "3x + 7 = 22"  (already clean)
    """
    # Strip common prefixes
    prefixes = [
        r'^Solve\s+for\s+[a-z]\s*:\s*',
        r'^Solve\s*:\s*',
        r'^Find\s+x\s+when\s+',
        r'^Evaluate\s*:\s*',
        r'^Simplify\s*:\s*',
    ]
    text = question_text.strip()
    for prefix_pattern in prefixes:
        text = re.sub(prefix_pattern, '', text, flags=re.IGNORECASE)

    return text.strip()


def get_variable(question_text: str, solution: str) -> str:
    """Detect the variable being solved for (default: x)."""
    # Check for "solve for [var]" pattern
    m = re.search(r'solve\s+for\s+([a-z])', question_text, re.IGNORECASE)
    if m:
        return m.group(1)
    # Look for isolated single letters in solution's final equation
    # Usually the last equation is "x = 5" or "y = -3" etc.
    last_eq = solution.strip().split('\n')[-1]
    m = re.match(r'^([a-z])\s*=', last_eq, re.IGNORECASE)
    if m:
        return m.group(1)
    return 'x'


# ─── Template Class ───────────────────────────────────────────────────────────

class AlgebraSolveTemplate(VideoTemplate):
    """
    Video template for "Solve for x" questions.

    Maps to scene_short.py's `algebra_solve` step type, which animates
    equations building up on screen in whiteboard/blackboard style.
    Each equation transformation writes in, with a note annotation
    appearing below-right to explain the operation.

    Covered question types:
      - Linear 1-step:  ax + b = c
      - Linear 2-step:  ax + b = cx + d
      - Multi-step with distributive property
      - Equations with fractions

    Video structure:
      1. Problem header (box) — "Solve for x" label
      2. Problem equation (math) — shows the starting equation
      3. Solution walkthrough (algebra_solve) — whiteboard steps
      4. Answer reveal (box) — final answer highlighted
    """

    template_id = "algebra-solve"

    supported_template_ids = [
        # Exact matches from Axiom Question Engine
        "solve-linear-1step",
        "solve-linear-2step",
        "solve-linear-any",
        "solve-multistep",
        "solve-with-fractions",
        "solve-with-distributive",
        "solve-literal-equation",
        "linear-equation",
        # Pattern matches (video_engine.py checks prefix/contains)
        "linear-*",
        "solve-*",
    ]

    # Timing tuned for landscape 16:9 instructional pacing
    INTRO_DURATION = 3.0    # Show the problem
    STEP_DURATION = 3.5     # Per solution step
    ANSWER_DURATION = 4.0   # Final answer hold

    def generate_manifest(self, question_data: dict) -> list[dict]:
        """
        Convert a solve-for-x question into a Manim manifest.

        The manifest drives scene_short.py's SyncedShortScene directly.
        All `narration` fields are metadata for future TTS — not rendered yet.
        """
        question_text = question_data.get("questionText", "")
        solution_str  = question_data.get("solution", "")
        answer        = question_data.get("correctAnswer", "?")
        difficulty    = question_data.get("difficulty", "medium")
        skill         = question_data.get("skill", "algebra")
        template_id   = question_data.get("templateId", "")

        # Extract the clean equation from "Solve: 3x + 7 = 22"
        equation = extract_question_equation(question_text)
        variable = get_variable(question_text, solution_str)

        # Parse solution string into structured steps
        parsed_steps = parse_solution(solution_str)

        # Build the manifest
        manifest = []

        # ── Step 1: Problem Header ─────────────────────────────────────────
        # A box with the skill label sets context for the viewer
        skill_label = _format_skill_label(skill, template_id)
        manifest.append({
            "type": "box",
            "content": skill_label,
            "duration": self.INTRO_DURATION,
            "narration": f"Let's solve a {skill_label.lower()} problem.",
            "metadata": {
                "role": "intro_header",
                "difficulty": difficulty,
            }
        })

        # ── Step 2: Problem Equation ───────────────────────────────────────
        # Show the equation cleanly in MathTex
        equation_latex = latex_for_equation(equation)
        spoken_problem = _math_to_speech(equation)
        manifest.append({
            "type": "math",
            "content": equation_latex,
            "duration": self.INTRO_DURATION + 0.5,
            "narration": f"We need to solve {spoken_problem}.",
            "metadata": {
                "role": "problem_statement",
                "raw_equation": equation,
            }
        })

        # ── Step 3: Solution Walkthrough (algebra_solve) ──────────────────
        # Build the sub-steps for the algebra_solve scene type
        # scene_short.py's algebra_solve handler shows these building up
        # on screen in whiteboard style — each equation writes in, then
        # the note annotation appears below-right
        algebra_steps = []

        # Always start with the original equation as the first sub-step
        spoken_equation = _math_to_speech(equation)
        algebra_steps.append({
            "latex": equation_latex,
            "note": "Starting equation",
            "note_color": ORBITAL_CYAN,
            "duration": 2.5,
            "narration": f"We start with {spoken_equation}.",
        })

        # Add each parsed solution step
        for parsed_step in parsed_steps:
            note = parsed_step.get("note", "")
            equations = parsed_step.get("equations", [])

            for i, eq_str in enumerate(equations):
                # Convert to LaTeX
                eq_latex = latex_for_equation(eq_str)

                # The note goes on the first equation of each step;
                # subsequent equations in the same step get a continuation note
                step_note = note if i == 0 else ""
                note_color = ORANGE_ACCENT if i == 0 else ORBITAL_CYAN

                algebra_steps.append({
                    "latex": eq_latex,
                    "note": step_note,
                    "note_color": note_color,
                    "duration": self.STEP_DURATION,
                    "narration": _narrate_step(eq_str, note, i),
                })

        # The last step should be the answer — make sure it's included
        # (sometimes the parser captures it, sometimes not)
        answer_eq = f"{variable} = {answer}"
        answer_latex = latex_for_equation(answer_eq)
        spoken_answer = _math_to_speech(answer_eq)
        if not algebra_steps or latex_for_equation(algebra_steps[-1]["latex"]) != answer_latex:
            algebra_steps.append({
                "latex": answer_latex,
                "note": f"Solution",
                "note_color": NEON_GREEN,
                "duration": self.STEP_DURATION,
                "narration": f"And there it is. {spoken_answer}.",
            })

        # Build combined narration from all sub-steps
        # Bible: "One API call per scene/step" — so we combine all sub-step
        # narrations into one block for the TTS call. The timing system will
        # distribute sync points across the sub-steps.
        combined_narration = " ".join(
            s["narration"] for s in algebra_steps if s.get("narration")
        )

        # The final_color makes the last sub-step glow green + gets circumscribed
        manifest.append({
            "type": "algebra_solve",
            "algebra_solve": {
                "title": f"Solve for {variable}",
                "steps": algebra_steps,
                "final_color": NEON_GREEN,
            },
            "duration": sum(s["duration"] for s in algebra_steps),
            "narration": combined_narration,
            "metadata": {
                "role": "solution_walkthrough",
                "num_steps": len(parsed_steps),
                "variable": variable,
            }
        })

        # ── Step 4: Answer Reveal ──────────────────────────────────────────
        # Final box with the answer — viewers know to screenshot this
        manifest.append({
            "type": "box",
            "content": f"{variable} = {answer}",
            "duration": self.ANSWER_DURATION,
            "narration": f"The answer is {variable} equals {answer}.",
            "metadata": {
                "role": "answer_reveal",
                "answer": answer,
                "variable": variable,
            }
        })

        return manifest

    def validate_question(self, question_data: dict) -> bool:
        """Algebra solve needs questionText, correctAnswer, and solution."""
        required = ["questionText", "correctAnswer", "solution"]
        return all(k in question_data and question_data[k] for k in required)


# ─── Private Helpers ──────────────────────────────────────────────────────────

def _format_skill_label(skill: str, template_id: str) -> str:
    """Format a human-readable skill label for the intro box."""
    if skill:
        # Convert kebab-case to title case: "linear-equations" → "Linear Equations"
        return skill.replace('-', ' ').title()
    if template_id:
        return template_id.replace('-', ' ').title()
    return "Algebra"


def _math_to_speech(expr: str) -> str:
    """
    Convert a math expression to spoken English for TTS.

    "3x + 7 - 7 = 22 - 7"  → "3x plus 7 minus 7 equals 22 minus 7"
    "x = 15/3"              → "x equals 15 over 3"
    "3x = 15"               → "3x equals 15"
    "(x + 2)(x + 3)"        → "x plus 2, times x plus 3"

    The TTS engine reads what we write literally. Math symbols
    need to be words or it sounds robotic/garbled.
    """
    text = expr.strip()

    # Equals sign
    text = text.replace(' = ', ' equals ')
    text = text.replace('=', ' equals ')

    # Plus/minus (handle carefully — don't break negative signs)
    text = re.sub(r'\s*\+\s*', ' plus ', text)
    text = re.sub(r'\s*-\s+', ' minus ', text)  # space after minus = subtraction
    # Leading minus stays: "-3" is "negative 3"
    text = re.sub(r'(?<!\w)-(\d)', r'negative \1', text)

    # Fractions: "15/3" → "15 over 3"
    text = re.sub(r'(\d+)\s*/\s*(\d+)', r'\1 over \2', text)

    # Exponents: "x^2" → "x squared", "x^3" → "x cubed", "x^n" → "x to the n"
    text = re.sub(r'(\w)\^2\b', r'\1 squared', text)
    text = re.sub(r'(\w)\^3\b', r'\1 cubed', text)
    text = re.sub(r'(\w)\^(\w+)', r'\1 to the \2', text)

    # Multiplication: "3x" is fine spoken, but "· " or "×" need words
    text = text.replace('×', ' times ')
    text = text.replace('·', ' times ')

    # Parentheses: soften for speech
    text = text.replace('(', ', ').replace(')', ', ')

    # Clean up extra spaces and commas
    text = re.sub(r'\s+', ' ', text)
    text = re.sub(r',\s*,', ',', text)
    text = text.strip(' ,')

    return text


def _narrate_step(equation: str, note: str, step_index: int) -> str:
    """Generate spoken narration for a solution step (for TTS)."""
    spoken_eq = _math_to_speech(equation)

    if note and step_index == 0:
        return f"{note}. That gives us {spoken_eq}."
    elif equation:
        return f"Which gives us {spoken_eq}."
    return ""
