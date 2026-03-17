"""
templates/graph_explore.py — Graph Exploration Video Template
==============================================================
Handles questions that involve graphing functions. Uses scene_short.py's
`graph` step type to render the function, then `math` steps to explain
key features (zeros, vertex, intercepts, domain/range).

Supported question templateIds:
  - graph-linear
  - graph-parabola
  - graph-quadratic-*
  - graph-polynomial-*
  - graph-absolute-value
  - graph-rational
  - function-evaluation-*
  - any question with graphData

Input example:
    {
        "templateId": "graph-parabola-vertex",
        "questionText": "Graph f(x) = x² - 4x + 3 and identify its vertex.",
        "correctAnswer": "vertex at (2, -1)",
        "solution": "Step 1: Find the vertex...\\n...",
        "graphData": {
            "functions": [{"expr": "lambda x: x**2 - 4*x + 3", "label": "f(x)"}],
            "x_range": [-1, 5, 1],
            "y_range": [-2, 6, 1],
            "dots": [{"x": 2, "y": -1, "label": "(2,-1)", "color": "#39FF14"}],
            "zeros": [[1, 0], [3, 0]]
        },
        "difficulty": "medium",
        "skill": "graphing-quadratics"
    }

Output manifest structure:
    [
        { "type": "box",   "content": "Graphing Quadratics" },  # skill header
        { "type": "math",  "content": "f(x) = x^2 - 4x + 3" }, # the function
        { "type": "graph", "graph": {...} },                     # render the graph
        { "type": "math",  "content": "vertex = (2, -1)" },     # key feature callout
        { "type": "box",   "content": "Answer: vertex at (2, -1)" }, # answer
    ]
"""

import re
from templates.base import VideoTemplate, NEON_GREEN, ORBITAL_CYAN, ORANGE_ACCENT, BOX_BORDER


class GraphExploreTemplate(VideoTemplate):
    """
    Video template for function graphing questions.

    Flow:
      1. Skill header box
      2. Function equation (math step)
      3. Graph render (graph step with the actual function plotted)
      4. Key features callout (math/box steps for vertex, zeros, etc.)
      5. Answer summary

    If no graphData is provided, the template tries to infer the graph
    config from the questionText (extracts the function expression).
    """

    template_id = "graph-explore"

    supported_template_ids = [
        "graph-linear",
        "graph-parabola",
        "graph-parabola-vertex",
        "graph-parabola-intercepts",
        "graph-quadratic",
        "graph-quadratic-vertex",
        "graph-polynomial",
        "graph-absolute-value",
        "graph-rational",
        "graph-exponential",
        "graph-logarithm",
        "function-evaluation",
        "identify-graph-features",
        "graph-*",
    ]

    INTRO_DURATION  = 3.0
    GRAPH_DURATION  = 6.0
    FEATURE_DURATION = 3.5
    ANSWER_DURATION = 4.0

    def generate_manifest(self, question_data: dict) -> list[dict]:
        """Convert a graphing question into a Manim manifest."""
        question_text = question_data.get("questionText", "")
        solution_str  = question_data.get("solution", "")
        answer        = question_data.get("correctAnswer", "")
        difficulty    = question_data.get("difficulty", "medium")
        skill         = question_data.get("skill", "graphing")
        graph_data    = question_data.get("graphData", {})
        template_id   = question_data.get("templateId", "")

        manifest = []

        # ── Step 1: Skill Header ───────────────────────────────────────────
        skill_label = skill.replace('-', ' ').title() if skill else "Graphing"
        manifest.append({
            "type": "box",
            "content": skill_label,
            "duration": self.INTRO_DURATION,
            "narration": f"Let's explore {skill_label.lower()}.",
            "metadata": {"role": "intro_header", "difficulty": difficulty},
        })

        # ── Step 2: Function Equation ──────────────────────────────────────
        # Extract the function expression for display
        func_display = _extract_function_display(question_text)
        func_latex   = _text_to_function_latex(func_display)

        manifest.append({
            "type": "math",
            "content": func_latex,
            "duration": self.INTRO_DURATION + 0.5,
            "narration": f"We are working with {func_display}.",
            "metadata": {"role": "function_equation", "raw": func_display},
        })

        # ── Step 3: Graph Render ───────────────────────────────────────────
        # Build the graph config from graphData or infer it
        graph_config = _build_graph_config(graph_data, question_text)

        manifest.append({
            "type": "graph",
            "graph": graph_config,
            "duration": self.GRAPH_DURATION,
            "narration": f"Here is the graph of {func_display}.",
            "metadata": {"role": "graph_render"},
        })

        # ── Step 4: Key Features ───────────────────────────────────────────
        # Extract notable features from graphData and solution
        features = _extract_features(graph_data, solution_str, answer)

        for feature in features:
            manifest.append({
                "type": "math",
                "content": feature["latex"],
                "duration": self.FEATURE_DURATION,
                "narration": feature["narration"],
                "metadata": {"role": "feature_callout", "feature_type": feature["type"]},
            })

        # ── Step 5: Answer Summary ─────────────────────────────────────────
        if answer:
            manifest.append({
                "type": "box",
                "content": answer,
                "duration": self.ANSWER_DURATION,
                "narration": f"Answer: {answer}",
                "metadata": {"role": "answer_reveal", "answer": answer},
            })

        return manifest

    def validate_question(self, question_data: dict) -> bool:
        """Graph explore needs at minimum a questionText with a function."""
        qt = question_data.get("questionText", "")
        return bool(qt) and ('=' in qt or 'f(' in qt or question_data.get("graphData"))


# ─── Graph Config Builders ────────────────────────────────────────────────────

def _build_graph_config(graph_data: dict, question_text: str) -> dict:
    """
    Build a graph config dict for scene_short.py's _build_graph().

    If graphData is provided, use it directly.
    Otherwise, try to infer from the question text.
    """
    if graph_data and graph_data.get("functions"):
        # graphData already has the right structure — pass through
        cfg = {
            "x_range": graph_data.get("x_range", [-5, 5, 1]),
            "y_range": graph_data.get("y_range", [-5, 15, 2]),
            "functions": graph_data.get("functions", []),
        }
        # Add dots for key points (zeros, vertex, intercepts)
        dots = []
        for zero in graph_data.get("zeros", []):
            dots.append({
                "x": zero[0], "y": 0,
                "color": ORBITAL_CYAN,
                "label": f"({zero[0]},0)",
                "radius": 0.08
            })
        if graph_data.get("vertex"):
            vx, vy = graph_data["vertex"]
            dots.append({
                "x": vx, "y": vy,
                "color": NEON_GREEN,
                "label": f"({vx},{vy})",
                "radius": 0.09
            })
        for pt in graph_data.get("dots", []):
            dots.append(pt)

        if dots:
            cfg["dots"] = dots

        # Add tangent if specified
        if graph_data.get("tangent"):
            cfg["tangent"] = graph_data["tangent"]

        return cfg

    # ── Infer from question text ──────────────────────────────────────
    func_expr = _infer_function_expr(question_text)
    x_range, y_range = _infer_ranges(func_expr)

    return {
        "x_range": x_range,
        "y_range": y_range,
        "functions": [{"expr": func_expr, "label": "f(x)", "color": ORBITAL_CYAN}],
    }


def _infer_function_expr(question_text: str) -> str:
    """
    Try to extract a Python-evaluable lambda from the question text.

    Examples:
        "Graph f(x) = x² - 4x + 3"  → "lambda x: x**2 - 4*x + 3"
        "Graph y = 2x + 1"           → "lambda x: 2*x + 1"
        "Graph f(x) = |x - 2|"      → "lambda x: abs(x - 2)"
    """
    # Extract the RHS of f(x) = ... or y = ...
    m = re.search(r'(?:f\(x\)|y)\s*=\s*(.+?)(?:\s*and|\s*\.|\s*$)', question_text, re.IGNORECASE)
    if not m:
        return "lambda x: x**2"  # safe default

    rhs = m.group(1).strip()

    # Convert math notation to Python
    rhs = rhs.replace('²', '**2').replace('³', '**3')
    rhs = rhs.replace('^2', '**2').replace('^3', '**3')
    rhs = re.sub(r'\^(\d+)', r'**\1', rhs)  # x^n → x**n
    rhs = re.sub(r'(\d)([a-z])', r'\1*\2', rhs)  # 4x → 4*x
    rhs = rhs.replace('|', 'abs(').replace('abs(', 'abs(')  # crude abs handling
    rhs = rhs.replace('√', 'sqrt')

    # Make it a lambda
    return f"lambda x: {rhs}"


def _infer_ranges(func_expr: str) -> tuple:
    """Infer reasonable x/y ranges for a function."""
    # Check if it's quadratic
    if '**2' in func_expr:
        return [-5, 5, 1], [-5, 15, 2]
    # Check if it's absolute value
    if 'abs(' in func_expr:
        return [-5, 5, 1], [-1, 8, 1]
    # Default: generic range
    return [-5, 5, 1], [-10, 10, 2]


def _extract_function_display(question_text: str) -> str:
    """Extract a clean display string for the function."""
    m = re.search(r'(?:Graph|Sketch|Plot)\s+(.+?)(?:\s+and|\s*$)', question_text, re.IGNORECASE)
    if m:
        return m.group(1).strip()
    m = re.search(r'f\(x\)\s*=\s*(.+?)(?:\s*$)', question_text)
    if m:
        return f"f(x) = {m.group(1).strip()}"
    return question_text.strip()


def _text_to_function_latex(display: str) -> str:
    """Convert a display function string to LaTeX."""
    # x² → x^2
    latex = display.replace('²', '^2').replace('³', '^3')
    # |x| → \left|x\right|
    latex = re.sub(r'\|([^|]+)\|', r'\\left|\1\\right|', latex)
    # sqrt(x) → \sqrt{x}
    latex = re.sub(r'sqrt\(([^)]+)\)', r'\\sqrt{\1}', latex)
    return latex


def _extract_features(graph_data: dict, solution_str: str, answer: str) -> list[dict]:
    """
    Extract key features to display as individual math steps.

    Looks for: vertex, zeros/roots, y-intercept, domain, range.
    Returns list of {latex, narration, type} dicts.
    """
    features = []

    if not graph_data:
        # Try to extract from solution string
        if 'vertex' in solution_str.lower():
            m = re.search(r'vertex.*?at\s*\(([^)]+)\)', solution_str, re.IGNORECASE)
            if m:
                coords = m.group(1)
                features.append({
                    "type": "vertex",
                    "latex": f"\\text{{vertex}} = ({coords})",
                    "narration": f"The vertex is at ({coords}).",
                })
        return features

    # Vertex
    if graph_data.get("vertex"):
        vx, vy = graph_data["vertex"]
        features.append({
            "type": "vertex",
            "latex": f"\\text{{vertex}} = ({vx},\\ {vy})",
            "narration": f"The vertex is at ({vx}, {vy}).",
        })

    # Zeros / x-intercepts
    zeros = graph_data.get("zeros", [])
    if zeros:
        zero_strs = [f"x = {z[0]}" for z in zeros]
        if len(zero_strs) == 1:
            features.append({
                "type": "zeros",
                "latex": f"x\\text{{-intercept: }}{zero_strs[0]}",
                "narration": f"The x-intercept is at {zero_strs[0]}.",
            })
        else:
            zero_latex = ",\\ ".join(zero_strs)
            features.append({
                "type": "zeros",
                "latex": f"x\\text{{-intercepts: }}{zero_latex}",
                "narration": f"The x-intercepts are at {', '.join(zero_strs)}.",
            })

    # Y-intercept (evaluate function at x=0)
    if graph_data.get("y_intercept") is not None:
        yi = graph_data["y_intercept"]
        features.append({
            "type": "y_intercept",
            "latex": f"y\\text{{-intercept: }}(0,\\ {yi})",
            "narration": f"The y-intercept is at (0, {yi}).",
        })

    return features
