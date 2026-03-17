"""
templates/base.py — VideoTemplate Abstract Base Class
======================================================
Every video template inherits from VideoTemplate and implements:
  - template_id: unique string matching the question engine's templateId
  - supported_template_ids: list of templateIds this template can handle
  - generate_manifest(): converts question JSON → Manim step manifest
  - render(): full pipeline (generate manifest → call render.py)

Architecture
------------
The manifest is the contract between templates and the renderer.
Each manifest entry is a dict consumed by scene_short.py's SyncedShortScene.

Proven step types (from scene_short.py):
  - "math"          — MathTex equation with optional narration
  - "box"           — Text in a purple-bordered box
  - "graph"         — NumberPlane + function plots
  - "algebra_solve" — Whiteboard-style step-by-step equation solving (KEY ONE)
  - "transform"     — Morph one equation into another
  - "indicate"      — Flash/highlight an equation

The `narration` field is metadata for future TTS — not rendered to audio now.
Audio is added via audio_path when TTS is integrated.
"""

from abc import ABC, abstractmethod
from typing import Any
import json
import sys
import os

# Add parent dir to path for timing import
sys.path.insert(0, os.path.dirname(os.path.dirname(__file__)))


# ─── Style Constants (Orbital brand — DO NOT CHANGE) ────────────────────────

ORBITAL_CYAN  = "#22D3EE"
NEON_GREEN    = "#39FF14"
BOX_BORDER    = "#8B5CF6"
BOX_FILL      = "#1a1130"
LABEL_COLOR   = "#22D3EE"
ORANGE_ACCENT = "#F97316"


# ─── Base Class ──────────────────────────────────────────────────────────────

class VideoTemplate(ABC):
    """
    Abstract base for all Orbital video templates.

    Subclasses are registered in video_engine.py's TEMPLATE_REGISTRY.
    The question-to-video mapper uses `supported_template_ids` to find
    the right template for a given question.

    Design principle: same input always produces the same manifest.
    Deterministic = testable = reliable.
    """

    # Unique ID for this template (used in template registry)
    template_id: str = ""

    # List of question-engine templateIds this template can handle.
    # e.g. ['solve-linear-1step', 'solve-linear-2step', 'solve-linear-any']
    supported_template_ids: list[str] = []

    # Default duration constants (seconds) — can be overridden
    INTRO_DURATION: float = 3.0
    STEP_DURATION: float = 3.5
    ANSWER_DURATION: float = 4.0

    @abstractmethod
    def generate_manifest(self, question_data: dict) -> list[dict]:
        """
        Convert question JSON to a Manim step manifest.

        Args:
            question_data: dict matching the Axiom GeneratedQuestion interface:
                {
                    "templateId": str,
                    "questionText": str,
                    "correctAnswer": str,
                    "solution": str,       # step-by-step text
                    "hint": str,
                    "section": str,
                    "difficulty": "easy"|"medium"|"hard",
                    "skill": str,
                    "graphData": dict|None
                }

        Returns:
            List of step dicts, each consumed by scene_short.py's SyncedShortScene.
            Include "narration" field in each step for future TTS.
        """
        pass

    def generate_synced_manifest(self, question_data: dict) -> list[dict]:
        """
        Generate manifest WITH timing/sync metadata from the Production Bible.

        Pipeline:
          1. generate_manifest() — raw manifest with estimated timing
          2. sync_pass() — adds narration timelines, sync points, gate waits,
                           alive fillers, animation scaling

        This is what you use before rendering. The sync report tells you
        if any steps need attention before generating TTS.
        """
        from timing import sync_pass
        manifest = self.generate_manifest(question_data)
        return sync_pass(manifest)

    def render(self, question_data: dict, output_path: str) -> str:
        """
        Full pipeline: generate manifest → render via scene_short.py.

        Args:
            question_data: Axiom question JSON
            output_path:   where to put the rendered .mp4

        Returns:
            Path to rendered video, or raises on error.
        """
        # Import here to avoid circular imports
        from render import render_manifest

        manifest = self.generate_synced_manifest(question_data)
        return render_manifest(manifest, output_path)

    def validate_question(self, question_data: dict) -> bool:
        """Check if question data has required fields. Override for type-specific checks."""
        required = ["questionText", "correctAnswer", "solution"]
        return all(k in question_data for k in required)

    def debug_manifest(self, question_data: dict) -> str:
        """Generate manifest and return as formatted JSON for inspection."""
        manifest = self.generate_manifest(question_data)
        return json.dumps(manifest, indent=2)

    def __repr__(self) -> str:
        return (
            f"<{self.__class__.__name__} "
            f"id='{self.template_id}' "
            f"handles={self.supported_template_ids}>"
        )
