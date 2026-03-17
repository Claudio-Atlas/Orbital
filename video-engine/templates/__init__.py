"""
templates/__init__.py — Template Package
=========================================
Auto-discovers and exports all video templates in this package.

Adding a new template:
  1. Create templates/my_template.py
  2. Define a class that inherits VideoTemplate
  3. Set template_id and supported_template_ids
  4. Implement generate_manifest()
  5. That's it — the registry in video_engine.py auto-discovers it

No manual registration needed: video_engine.py uses
`get_all_templates()` to scan this package at startup.
"""

from templates.algebra_solve import AlgebraSolveTemplate
from templates.graph_explore import GraphExploreTemplate
from templates.factor_reveal import FactorRevealTemplate

__all__ = [
    "AlgebraSolveTemplate",
    "GraphExploreTemplate",
    "FactorRevealTemplate",
]
