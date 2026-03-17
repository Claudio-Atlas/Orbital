"""
video_engine.py — Orbital Video Template Engine (Core)
=======================================================
The compound play: same math content that powers Axiom assessments
now powers Orbital instructional videos. One question JSON → one video.

Architecture
------------
                    ┌─────────────────────┐
  Axiom Question    │   Video Engine       │   Manim Renderer
  Engine Output     │                      │
                    │                      │
  { templateId,    ──►  Template Registry  ──►  Manifest (JSON)  ──►  Video
    questionText,   │   (question mapper)   │   (step list)       │   (mp4)
    solution, ... } │                      │                      │
                    └─────────────────────┘

Key Components
--------------
1. TemplateRegistry  — maps templateIds to VideoTemplate instances
2. QuestionMapper    — given a templateId, finds the right template
3. VideoEngine       — the public API: generate_manifest() and render()

Usage
-----
    from video_engine import VideoEngine

    engine = VideoEngine()

    # Generate a manifest (no rendering — fast, for inspection)
    manifest = engine.generate_manifest(question_data)

    # Generate manifest + render to video
    video_path = engine.render(question_data, output_path="out/video.mp4")

    # Just print the manifest as JSON
    engine.print_manifest(question_data)

Template Registry
-----------------
Templates are auto-discovered from the `templates/` package.
Each template declares `supported_template_ids` — a list of exact
template IDs or prefix patterns (e.g. "solve-*") it can handle.

The mapper uses three matching strategies (in order):
  1. Exact match: templateId == supported_template_id
  2. Prefix match: templateId starts with prefix (for "solve-*" etc.)
  3. Contains match: templateId contains a keyword
  4. Category fallback: guess based on question content
"""

import json
import sys
import os
from typing import Optional

# Ensure templates/ is importable
sys.path.insert(0, os.path.dirname(__file__))

from templates.base import VideoTemplate
from templates.algebra_solve import AlgebraSolveTemplate
from templates.graph_explore import GraphExploreTemplate
from templates.factor_reveal import FactorRevealTemplate
from timing import sync_pass, sync_report, generate_tts_manifest, load_tts_results


# ─── Template Registry ────────────────────────────────────────────────────────

class TemplateRegistry:
    """
    Manages all registered VideoTemplate instances.

    Templates self-declare which question templateIds they handle via
    their `supported_template_ids` list. The registry uses a multi-strategy
    matcher to find the best template for any given question.

    Adding a template:
        1. Create templates/my_template.py with a VideoTemplate subclass
        2. Import and instantiate it in the registry below
        3. Done — the matcher picks it up automatically
    """

    def __init__(self):
        self._templates: list[VideoTemplate] = []
        self._register_defaults()

    def _register_defaults(self):
        """Register all known templates. Add new ones here."""
        self.register(AlgebraSolveTemplate())
        self.register(GraphExploreTemplate())
        self.register(FactorRevealTemplate())

    def register(self, template: VideoTemplate) -> None:
        """Add a template to the registry."""
        self._templates.append(template)
        print(f"  📋 Registered: {template}")

    def find(self, template_id: str, question_data: dict = None) -> Optional[VideoTemplate]:
        """
        Find the best matching template for a given question templateId.

        Matching strategy (in order of precedence):
          1. Exact match:   templateId == one of supported_template_ids
          2. Pattern match: "solve-*" pattern where * is a wildcard
          3. Contains:      templateId contains a keyword from supported list
          4. Category guess: based on question content (keywords in questionText)
          5. Default:       AlgebraSolveTemplate as final fallback

        Args:
            template_id:   The templateId from the Axiom question
            question_data: Full question dict (for category-guess fallback)

        Returns:
            Best matching VideoTemplate, or None if no match found
        """
        tid_lower = template_id.lower()

        # ── Strategy 1: Exact match ────────────────────────────────────
        for tmpl in self._templates:
            for supported_id in tmpl.supported_template_ids:
                if supported_id.endswith('*'):
                    continue  # skip patterns in exact pass
                if tid_lower == supported_id.lower():
                    return tmpl

        # ── Strategy 2: Pattern match (prefix*) ───────────────────────
        for tmpl in self._templates:
            for supported_id in tmpl.supported_template_ids:
                if '*' in supported_id:
                    prefix = supported_id.replace('*', '').lower()
                    if tid_lower.startswith(prefix):
                        return tmpl

        # ── Strategy 3: Contains match ─────────────────────────────────
        for tmpl in self._templates:
            for supported_id in tmpl.supported_template_ids:
                if '*' in supported_id:
                    continue
                if supported_id.lower() in tid_lower or tid_lower in supported_id.lower():
                    return tmpl

        # ── Strategy 4: Category guess from question content ──────────
        if question_data:
            result = self._guess_from_content(question_data)
            if result:
                return result

        # ── Strategy 5: Default fallback ──────────────────────────────
        return self._templates[0] if self._templates else None

    def _guess_from_content(self, question_data: dict) -> Optional[VideoTemplate]:
        """
        Guess the template from question content when templateId doesn't match.

        Uses keyword detection in questionText and skill fields.
        """
        question_text = question_data.get("questionText", "").lower()
        skill = question_data.get("skill", "").lower()
        tid = question_data.get("templateId", "").lower()
        has_graph_data = bool(question_data.get("graphData"))
        combined = f"{question_text} {skill} {tid}"

        # Graph signals
        graph_keywords = ["graph", "plot", "sketch", "parabola", "function", "intercept"]
        if has_graph_data or any(kw in combined for kw in graph_keywords):
            for tmpl in self._templates:
                if isinstance(tmpl, GraphExploreTemplate):
                    return tmpl

        # Factor signals
        factor_keywords = ["factor", "factored", "gcf", "trinomial", "quadratic"]
        if any(kw in combined for kw in factor_keywords):
            for tmpl in self._templates:
                if isinstance(tmpl, FactorRevealTemplate):
                    return tmpl

        # Solve signals (default path)
        solve_keywords = ["solve", "equation", "linear", "find x", "for x"]
        if any(kw in combined for kw in solve_keywords):
            for tmpl in self._templates:
                if isinstance(tmpl, AlgebraSolveTemplate):
                    return tmpl

        return None

    def list_templates(self) -> list[dict]:
        """Return info about all registered templates."""
        return [
            {
                "template_id": t.template_id,
                "class": t.__class__.__name__,
                "supported_ids": t.supported_template_ids[:5],  # first 5
                "num_supported": len(t.supported_template_ids),
            }
            for t in self._templates
        ]

    def __repr__(self) -> str:
        return f"<TemplateRegistry templates={[t.template_id for t in self._templates]}>"


# ─── Video Engine (Public API) ────────────────────────────────────────────────

class VideoEngine:
    """
    Main entry point for the Orbital Video Template Engine.

    Usage:
        engine = VideoEngine()

        # Inspect the manifest without rendering
        manifest = engine.generate_manifest(question_data)

        # Render to video
        video_path = engine.render(question_data, "output/video.mp4")

        # Debug: print manifest as JSON
        engine.print_manifest(question_data)
    """

    def __init__(self):
        self.registry = TemplateRegistry()

    def generate_manifest(self, question_data: dict) -> list[dict]:
        """
        Convert a question JSON to a Manim manifest.

        Args:
            question_data: Axiom GeneratedQuestion dict

        Returns:
            List of step dicts for scene_short.py's SyncedShortScene

        Raises:
            ValueError: if no template found and no fallback available
        """
        template_id = question_data.get("templateId", "")

        # Find the right template
        template = self.registry.find(template_id, question_data)
        if not template:
            raise ValueError(
                f"No video template found for question templateId='{template_id}'. "
                f"Check that the template registry has a matching template."
            )

        # Validate the question data
        if not template.validate_question(question_data):
            raise ValueError(
                f"Question data failed validation for template '{template.template_id}'. "
                f"Check that questionText, correctAnswer, and solution are present."
            )

        print(f"  🎬 Using template: {template.template_id} ({template.__class__.__name__})")

        # Generate the manifest
        manifest = template.generate_manifest(question_data)

        # Post-process: ensure all required fields exist
        manifest = self._normalize_manifest(manifest)

        return manifest

    def generate_synced_manifest(self, question_data: dict) -> list[dict]:
        """
        Generate manifest WITH sync metadata (narration timelines, sync points,
        gate waits, alive fillers).

        This is the Bible-compliant version. Use this before rendering.
        """
        manifest = self.generate_manifest(question_data)
        return sync_pass(manifest)

    def sync_report(self, question_data: dict) -> str:
        """
        Generate a sync report for a question — shows timing analysis
        and any warnings before you commit to TTS generation.
        """
        synced = self.generate_synced_manifest(question_data)
        return sync_report(synced)

    def prepare_tts(self, question_data: dict, output_dir: str) -> dict:
        """
        Generate TTS manifest for a question.

        Creates the manifest file that gen_tts.py consumes to generate
        per-step audio with Allison's voice.

        After TTS generation, call load_tts() to wire audio back in.
        """
        manifest = self.generate_manifest(question_data)
        return generate_tts_manifest(manifest, output_dir)

    def load_tts(self, question_data: dict, tts_dir: str) -> list[dict]:
        """
        After TTS generation: load actual audio durations and run sync pass.

        Returns the fully synced manifest ready for rendering.
        """
        manifest = self.generate_manifest(question_data)
        return load_tts_results(tts_dir, manifest)

    def render(self, question_data: dict, output_path: str, tts_dir: str = None) -> str:
        """
        Full pipeline: question JSON → manifest → rendered video.

        Args:
            question_data: Axiom GeneratedQuestion dict
            output_path:   Path for the output .mp4 file
            tts_dir:       Optional: directory with TTS audio files.
                           If provided, uses actual TTS durations for sync.
                           If not, renders with estimated timing (silent).

        Returns:
            Path to the rendered video file
        """
        from render import render_manifest

        if tts_dir:
            manifest = self.load_tts(question_data, tts_dir)
        else:
            manifest = self.generate_synced_manifest(question_data)

        return render_manifest(manifest, output_path)

    def print_manifest(self, question_data: dict, pretty: bool = True) -> str:
        """
        Generate and print the manifest as JSON.
        Useful for debugging templates without rendering.
        """
        manifest = self.generate_manifest(question_data)
        # Strip large audio_path values for display
        display_manifest = _strip_display(manifest)
        json_str = json.dumps(display_manifest, indent=2 if pretty else None)
        print(json_str)
        return json_str

    def get_template_info(self) -> list[dict]:
        """Return info about all registered templates."""
        return self.registry.list_templates()

    def _normalize_manifest(self, manifest: list[dict]) -> list[dict]:
        """
        Ensure all manifest steps have required fields.
        Adds defaults where missing — renderer won't crash on partial steps.
        """
        for step in manifest:
            # Ensure type is set
            if "type" not in step:
                step["type"] = "math"
            # Ensure duration is set
            if "duration" not in step:
                step["duration"] = 3.0
            # Ensure content or algebra_solve exists for the step type
            if step["type"] in ("math", "box") and "content" not in step:
                step["content"] = ""
            # Ensure narration exists (metadata for TTS)
            if "narration" not in step:
                step["narration"] = ""
            # No audio_path by default (TTS not integrated yet)
            if "audio_path" not in step:
                step["audio_path"] = ""
        return manifest

    def __repr__(self) -> str:
        return f"<VideoEngine registry={self.registry}>"


# ─── Module-level convenience functions ──────────────────────────────────────

# Shared engine instance (singleton pattern — avoids re-registering on every call)
_engine: Optional[VideoEngine] = None


def get_engine() -> VideoEngine:
    """Get or create the shared VideoEngine instance."""
    global _engine
    if _engine is None:
        _engine = VideoEngine()
    return _engine


def generate_manifest(question_data: dict) -> list[dict]:
    """Convenience: generate a manifest using the shared engine."""
    return get_engine().generate_manifest(question_data)


def render_question(question_data: dict, output_path: str) -> str:
    """Convenience: render a question to video using the shared engine."""
    return get_engine().render(question_data, output_path)


# ─── Private Helpers ──────────────────────────────────────────────────────────

def _strip_display(manifest: list[dict]) -> list[dict]:
    """Remove audio file paths and large binary data for display purposes."""
    result = []
    for step in manifest:
        clean = {k: v for k, v in step.items() if k not in ("audio_path",)}
        result.append(clean)
    return result


# ─── CLI Entry Point ──────────────────────────────────────────────────────────

if __name__ == "__main__":
    import sys

    if len(sys.argv) < 2:
        print("Usage: python video_engine.py <question.json> [output.mp4]")
        print("\nRegistered templates:")
        engine = VideoEngine()
        for info in engine.get_template_info():
            print(f"  {info['template_id']}: handles {info['num_supported']} template IDs")
        sys.exit(0)

    # Load question JSON
    json_path = sys.argv[1]
    with open(json_path) as f:
        question_data = json.load(f)

    engine = VideoEngine()

    if len(sys.argv) >= 3:
        # Render mode
        output_path = sys.argv[2]
        print(f"  🎬 Rendering {json_path} → {output_path}")
        video_path = engine.render(question_data, output_path)
        print(f"  ✓ Video: {video_path}")
    else:
        # Manifest-only mode
        print(f"  📋 Generating manifest for {json_path}")
        engine.print_manifest(question_data)
