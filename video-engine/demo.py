"""
demo.py — Video Engine Demonstration
======================================
Hardcodes 3 example questions (one linear solve, one factoring, one with graph)
and demonstrates the video engine by generating and printing their manifests.

Usage:
    python demo.py              # Print all 3 manifests
    python demo.py --render     # Render all 3 to video (takes ~5min)
    python demo.py --index 0    # Print manifest for question 0 only
    python demo.py --index 1 --render  # Render question 1 only
    python demo.py --preview    # Print human-readable step summary

This is the end-to-end smoke test:
  question JSON in → manifest generated → (optionally) video rendered
"""

import json
import sys
import os
import argparse
from pathlib import Path

# Ensure video-engine modules are importable
sys.path.insert(0, str(Path(__file__).parent))

from video_engine import VideoEngine
from render import preview_manifest
from timing import sync_pass, sync_report


# ─── Hardcoded Example Questions ─────────────────────────────────────────────
# These mirror what the Axiom Question Engine would generate.
# Same format as GeneratedQuestion interface in question-engine.ts.

EXAMPLE_QUESTIONS = [

    # ── Example 1: Linear equation (2-step solve) ──────────────────────────
    # templateId: "solve-linear-2step"
    # Typical output from AlgebraSolveTemplate
    {
        "templateId": "solve-linear-2step",
        "questionText": "Solve: 3x + 7 = 22",
        "correctAnswer": "5",
        "solution": (
            "Step 1: Subtract 7 from both sides.\n"
            "3x + 7 - 7 = 22 - 7\n"
            "3x = 15\n"
            "Step 2: Divide both sides by 3.\n"
            "x = 15/3\n"
            "x = 5"
        ),
        "hint": "Isolate the variable by undoing the operations in reverse order.",
        "section": "Solving Linear Equations",
        "difficulty": "easy",
        "skill": "linear-equations",
    },

    # ── Example 2: Factoring quadratic ─────────────────────────────────────
    # templateId: "factor-quadratic-leading-1"
    # Typical output from FactorRevealTemplate
    {
        "templateId": "factor-quadratic-leading-1",
        "questionText": "Factor: x² + 5x + 6",
        "correctAnswer": "(x + 2)(x + 3)",
        "solution": (
            "Step 1: Find two numbers that multiply to 6 and add to 5.\n"
            "Factors of 6: 1×6=6, 2×3=6\n"
            "Try a=2, b=3: 2×3=6 and 2+3=5\n"
            "Step 2: Write the factored form.\n"
            "x² + 5x + 6 = (x + 2)(x + 3)\n"
            "Step 3: Verify by expanding.\n"
            "(x + 2)(x + 3) = x² + 3x + 2x + 6 = x² + 5x + 6"
        ),
        "hint": "Look for two numbers that multiply to the constant and add to the middle coefficient.",
        "section": "Factoring Polynomials",
        "difficulty": "medium",
        "skill": "factoring-quadratics",
    },

    # ── Example 3: Graphing a parabola ────────────────────────────────────
    # templateId: "graph-parabola-vertex"
    # Typical output from GraphExploreTemplate
    {
        "templateId": "graph-parabola-vertex",
        "questionText": "Graph f(x) = x² - 4x + 3 and find the vertex.",
        "correctAnswer": "vertex at (2, -1)",
        "solution": (
            "Step 1: Complete the square to find vertex form.\n"
            "f(x) = x² - 4x + 3\n"
            "f(x) = (x² - 4x + 4) - 4 + 3\n"
            "f(x) = (x - 2)² - 1\n"
            "Step 2: The vertex is at (h, k) = (2, -1).\n"
            "Step 3: Find x-intercepts by setting f(x) = 0.\n"
            "(x - 2)² = 1\n"
            "x - 2 = ±1\n"
            "x = 1 or x = 3"
        ),
        "hint": "Complete the square to convert to vertex form f(x) = a(x-h)² + k.",
        "section": "Graphing Quadratic Functions",
        "difficulty": "medium",
        "skill": "graphing-quadratics",
        "graphData": {
            "functions": [
                {
                    "expr": "lambda x: x**2 - 4*x + 3",
                    "label": "f(x) = x^2 - 4x + 3",
                    "color": "#22D3EE",
                }
            ],
            "x_range": [-1, 5, 1],
            "y_range": [-2, 6, 1],
            "vertex": [2, -1],
            "zeros": [[1, 0], [3, 0]],
            "dots": [
                {"x": 2, "y": -1, "color": "#39FF14", "label": "(2,-1)", "radius": 0.09},
                {"x": 1, "y": 0,  "color": "#22D3EE", "label": "(1,0)",  "radius": 0.07},
                {"x": 3, "y": 0,  "color": "#22D3EE", "label": "(3,0)",  "radius": 0.07},
            ],
        },
    },

]


# ─── Demo Runner ──────────────────────────────────────────────────────────────

def run_demo(
    questions: list[dict],
    render: bool = False,
    output_dir: str = "output",
    preview: bool = False,
    sync: bool = False,
    tts_output_dir: str = None,
) -> dict:
    """
    Run the demo: generate manifests for each question and optionally render.

    Args:
        questions:   List of question dicts
        render:      If True, render each question to video
        output_dir:  Directory for rendered videos
        preview:     If True, print human-readable step summaries

    Returns:
        Dict with manifests and (if rendered) video paths
    """
    engine = VideoEngine()
    results = {}

    print("=" * 60)
    print("  Orbital Video Template Engine — Demo")
    print("=" * 60)
    print()

    for i, question in enumerate(questions):
        template_id = question.get("templateId", f"question-{i}")
        question_text = question.get("questionText", "")
        answer = question.get("correctAnswer", "")

        print(f"Question {i+1}: {template_id}")
        print(f"  Text:   {question_text}")
        print(f"  Answer: {answer}")
        print()

        # Generate manifest
        try:
            manifest = engine.generate_manifest(question)
            print(f"  ✓ Generated manifest: {len(manifest)} steps")
        except Exception as e:
            print(f"  ❌ Failed: {e}")
            results[template_id] = {"error": str(e)}
            continue

        # Preview mode
        if preview:
            print()
            print(preview_manifest(manifest))
            print()
        else:
            # Print compact manifest JSON
            print()
            print("  Manifest (JSON):")
            print("  " + "-" * 56)
            # Strip audio_path for cleaner output
            display = [
                {k: v for k, v in s.items() if k != "audio_path"}
                for s in manifest
            ]
            print(json.dumps(display, indent=4).replace("\n", "\n  "))
            print()

        results[template_id] = {"manifest": manifest, "num_steps": len(manifest)}

        # Sync analysis if requested
        if sync:
            synced = sync_pass(manifest)
            print(sync_report(synced))
            print()
            results[template_id]["synced_manifest"] = synced

        # TTS manifest if requested
        if tts_output_dir:
            from timing import generate_tts_manifest
            q_tts_dir = os.path.join(tts_output_dir, template_id.replace('-', '_'))
            generate_tts_manifest(manifest, q_tts_dir)
            print()

        # Render if requested
        if render:
            from render import render_manifest

            output_path = Path(output_dir) / f"{template_id.replace('-', '_')}.mp4"
            output_path.parent.mkdir(parents=True, exist_ok=True)

            print(f"  🎬 Rendering → {output_path} ...")
            try:
                video_path = render_manifest(manifest, str(output_path))
                print(f"  ✓ Video: {video_path}")
                results[template_id]["video_path"] = video_path
            except Exception as e:
                print(f"  ❌ Render failed: {e}")
                results[template_id]["render_error"] = str(e)

        print("-" * 60)
        print()

    # Summary
    print("=" * 60)
    print("  Summary")
    print("=" * 60)
    for key, val in results.items():
        status = "✓" if "error" not in val and "render_error" not in val else "❌"
        steps  = val.get("num_steps", 0)
        video  = val.get("video_path", "")
        print(f"  {status} {key}: {steps} steps" + (f" → {video}" if video else ""))

    return results


# ─── CLI ──────────────────────────────────────────────────────────────────────

def main():
    parser = argparse.ArgumentParser(
        description="Orbital Video Template Engine Demo",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  python demo.py                    # Print all 3 manifests as JSON
  python demo.py --preview          # Human-readable step summaries
  python demo.py --index 0          # Show question 0 only
  python demo.py --render           # Render all 3 videos
  python demo.py --index 1 --render # Render question 1 only
        """
    )
    parser.add_argument(
        "--render", action="store_true",
        help="Render videos (requires Manim + orbital_longform venv)"
    )
    parser.add_argument(
        "--index", type=int, default=None,
        help="Show/render only this question index (0, 1, or 2)"
    )
    parser.add_argument(
        "--preview", action="store_true",
        help="Print human-readable step summaries instead of raw JSON"
    )
    parser.add_argument(
        "--output-dir", default="output",
        help="Output directory for rendered videos (default: output/)"
    )
    parser.add_argument(
        "--list", action="store_true",
        help="List all example questions without generating manifests"
    )
    parser.add_argument(
        "--sync", action="store_true",
        help="Run sync pass and show timing analysis report"
    )
    parser.add_argument(
        "--tts-manifest", type=str, default=None,
        help="Generate TTS manifest to this directory (e.g. output/tts/)"
    )

    args = parser.parse_args()

    if args.list:
        print("Example Questions:")
        for i, q in enumerate(EXAMPLE_QUESTIONS):
            print(f"  [{i}] {q['templateId']}: {q['questionText'][:60]}")
        return

    # Select questions to demo
    if args.index is not None:
        if args.index < 0 or args.index >= len(EXAMPLE_QUESTIONS):
            print(f"Error: index must be 0-{len(EXAMPLE_QUESTIONS)-1}")
            sys.exit(1)
        questions = [EXAMPLE_QUESTIONS[args.index]]
    else:
        questions = EXAMPLE_QUESTIONS

    # Run
    run_demo(
        questions=questions,
        render=args.render,
        output_dir=args.output_dir,
        preview=args.preview,
        sync=args.sync,
        tts_output_dir=args.tts_manifest,
    )


if __name__ == "__main__":
    main()
