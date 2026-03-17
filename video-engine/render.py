"""
render.py — Manim Renderer
===========================
Takes a manifest (list of step dicts) and renders it as a 16:9 landscape
video using scene_short.py's proven infrastructure.

This module generates a Manim scene file compatible with scene_short.py's
SyncedShortScene class, then renders it using the orbital_longform venv.

SCENE FILE GENERATION NOTE:
scene_short.py's `create_synced_scene_short()` function has a known bug:
its scene_code f-string contains unescaped `{...}` patterns (dict literals,
comments with LaTeX) that cause NameError/ValueError at runtime in Python 3.12+.
The function cannot be called directly until the bug is fixed.

Our workaround: `_generate_scene()` in this module generates an equivalent
scene file directly using string building (no f-string) for our specific step
types (math, box, algebra_solve, graph). The generated file is 100% compatible
with scene_short.py's SyncedShortScene class — same class name, same structure,
same Orbital visual style, same animation patterns.

When the bug in scene_short.py is fixed, replace `_generate_scene()` with:
    from scene_short import create_synced_scene_short
    create_synced_scene_short(manifest, str(scene_path), landscape=True)

Render Specs (Landscape 16:9)
------------------------------
  Resolution:  1920 × 1080
  Frame rate:  60 fps
  Format:      mp4
  Frame dims:  14.2 × 8.0 (Manim units, 16:9 aspect)
  Background:  #000000 (Orbital dark)
"""

import os
import sys
import json
import subprocess
import tempfile
import shutil
import textwrap
from pathlib import Path
from typing import Optional


# ─── Path Constants ───────────────────────────────────────────────────────────

ORBITAL_LONGFORM = Path.home() / "Desktop" / "Orbital" / "orbital_longform"
VENV_PYTHON      = ORBITAL_LONGFORM / "venv" / "bin" / "python3"
VENV_MANIM       = ORBITAL_LONGFORM / "venv" / "bin" / "manim"
LANDSCAPE_CFG    = Path(__file__).parent / "manim_landscape.cfg"

RESOLUTION = "1920,1080"
FRAME_RATE = "60"


# ─── Environment Setup ────────────────────────────────────────────────────────

def _manim_env() -> dict:
    """Build Manim execution environment — adds LaTeX and homebrew paths."""
    env = os.environ.copy()
    home = Path.home()
    extra = ":".join([
        str(ORBITAL_LONGFORM / "venv" / "bin"),
        str(home / "Library" / "TinyTeX" / "bin" / "universal-darwin"),
        str(home / "Library" / "Python" / "3.9" / "bin"),
        "/opt/homebrew/bin",
        "/usr/local/bin",
    ])
    env["PATH"] = extra + ":" + env.get("PATH", "")
    return env


def _ensure_landscape_cfg() -> None:
    """Create manim_landscape.cfg for 16:9 rendering if it doesn't exist."""
    if LANDSCAPE_CFG.exists():
        return
    LANDSCAPE_CFG.write_text(
        "[CLI]\n"
        "quality = production_quality\n"
        "pixel_width = 1920\n"
        "pixel_height = 1080\n"
        "frame_rate = 60\n"
        "frame_width = 14.2\n"
        "frame_height = 8.0\n\n"
        "[camera]\n"
        "pixel_width = 1920\n"
        "pixel_height = 1080\n"
        "frame_rate = 60\n"
        "background_color = #000000\n"
        "frame_width = 14.2\n"
        "frame_height = 8.0\n"
    )
    print(f"  ✓ Created landscape config: {LANDSCAPE_CFG}")


# ─── Main Render Function ─────────────────────────────────────────────────────

def render_manifest(
    manifest: list[dict],
    output_path: str,
    job_dir: Optional[str] = None,
    keep_temp: bool = False,
) -> str:
    """
    Render a manifest to a 16:9 landscape video (1920×1080).

    Args:
        manifest:    List of step dicts (from VideoTemplate.generate_manifest())
        output_path: Desired output path for the final .mp4
        job_dir:     Optional working directory (temp dir created if not given)
        keep_temp:   If True, keep the temp directory after rendering (for debugging)

    Returns:
        Absolute path to the rendered video file

    Raises:
        RuntimeError: if Manim venv not found or rendering fails
    """
    if not VENV_PYTHON.exists():
        raise RuntimeError(
            f"Python venv not found at {VENV_PYTHON}. "
            f"Check that orbital_longform/venv exists with manim installed."
        )

    _ensure_landscape_cfg()

    cleanup_dir = False
    if job_dir is None:
        job_dir = tempfile.mkdtemp(prefix="orbital_video_")
        cleanup_dir = not keep_temp

    job_path = Path(job_dir)
    job_path.mkdir(parents=True, exist_ok=True)

    try:
        print(f"  📝 Generating Manim scene file...")
        scene_path = job_path / "short_scene.py"
        _generate_scene(manifest, scene_path)

        print(f"  🎨 Rendering 1920×1080 @ 60fps...")
        rendered_path = _run_manim(scene_path, job_path)

        if rendered_path is None:
            raise RuntimeError("Manim rendering failed — check console output.")

        output_path = str(Path(output_path).resolve())
        Path(output_path).parent.mkdir(parents=True, exist_ok=True)
        shutil.copy2(str(rendered_path), output_path)
        print(f"  ✓ Video: {output_path}")
        return output_path

    finally:
        if cleanup_dir and not keep_temp:
            shutil.rmtree(job_dir, ignore_errors=True)


# ─── Scene File Generation ────────────────────────────────────────────────────

def _generate_scene(manifest: list[dict], scene_path: Path) -> None:
    """
    Generate a Manim scene file compatible with SyncedShortScene.

    NOTE ON DESIGN CHOICE:
    scene_short.py's create_synced_scene_short() is currently broken due to
    unescaped {key: value} Python dict literals inside its scene_code f-string.
    These cause NameError/ValueError in Python 3.12+.

    This function generates an equivalent scene file using string building
    (no f-string interpolation issues). The output is compatible:
    - Same class name: SyncedShortScene
    - Same Orbital style constants
    - Same animation patterns (Write, FadeOut, Circumscribe etc.)
    - Same step types: math, box, algebra_solve, graph

    When scene_short.py is fixed, this function can be replaced with:
        from scene_short import create_synced_scene_short
        create_synced_scene_short(manifest, str(scene_path), landscape=True)
    """
    # Embed the manifest as a Python repr — JSON would also work but repr is
    # safer for nested Python objects and handles all Python literals correctly
    manifest_repr = repr(manifest)

    scene_code = _build_scene_code(manifest_repr)
    scene_path.write_text(scene_code, encoding="utf-8")
    print(f"  ✓ Scene file: {scene_path} ({scene_path.stat().st_size:,} bytes)")


def _build_scene_code(manifest_repr: str) -> str:
    """
    Build the complete Manim scene Python file as a string.

    Uses the same constants and animation patterns as scene_short.py.
    Only handles step types used by our video templates:
      - math          → MathTex equation display
      - box           → Text in purple-bordered box
      - algebra_solve → Whiteboard equation building
      - graph         → NumberPlane + function plots
    """

    # The scene code is built using string concatenation to avoid
    # any f-string issues. Format strings are used ONLY where safe
    # (manifest embedding with repr(), numeric constants).

    header = '''\
"""
Orbital Video Engine — Auto-generated landscape scene (16:9, 1920×1080)
Generated by video-engine/render.py
"""
from manim import *
import os
import numpy as np

# ── Landscape 16:9 frame config ──────────────────────────────────────────────
config.frame_width  = 14.2
config.frame_height = 8.0

# ── Orbital brand constants (LOCKED — do not change) ─────────────────────────
ORBITAL_CYAN  = "#22D3EE"
NEON_GREEN    = "#39FF14"
BOX_BORDER    = "#8B5CF6"
BOX_FILL      = "#1a1130"
LABEL_COLOR   = "#22D3EE"
ORANGE        = "#F97316"

# ── Layout constants (landscape-tuned from Group Order 15 video) ─────────────
FRAME_W       = 14.2
FRAME_H       = 8.0
MAX_WIDTH     = FRAME_W * 0.82
MATH_SCALE    = 1.4
BOX_SCALE     = 0.90
GRAPH_WIDTH   = 6.0
GRAPH_HEIGHT  = 3.5
MATH_CENTER_Y = 0.5
GRAPH_CENTER_Y = -1.5
ZONE_A_Y      = 2.8
ANIMATION_RATIO = 0.35
EXTRA_HOLD    = 0.5
EQ_FONT_SIZE  = 52
NOTE_FONT_SIZE = 24
TITLE_FONT_SIZE = 36
WM_FONT_SIZE  = 14


def _clamp(mob, max_w=None):
    """Scale mob down if it exceeds max_w."""
    if max_w is None:
        max_w = MAX_WIDTH
    if mob.width > max_w:
        mob.scale(max_w / mob.width)
    return mob


def _build_graph(cfg):
    """
    Build a graph VGroup from a config dict.
    Supports: x_range, y_range, functions (list), dots (list), tangent, shaded_area.
    """
    x_range   = cfg.get("x_range", [-3, 3, 1])
    y_range   = cfg.get("y_range", [-7, 25, 5])
    functions = cfg.get("functions", [])

    x_abs  = max(abs(x_range[0]), abs(x_range[1]))
    x_step = x_range[2] if len(x_range) > 2 else 1
    x_range = [-x_abs, x_abs, x_step]

    grid = NumberPlane(
        x_range=x_range, y_range=y_range,
        x_length=GRAPH_WIDTH, y_length=GRAPH_HEIGHT,
        background_line_style={
            "stroke_color": "#8B5CF6",
            "stroke_opacity": 0.25,
            "stroke_width": 1,
        },
        faded_line_style={
            "stroke_color": "#22D3EE",
            "stroke_opacity": 0.12,
            "stroke_width": 0.5,
        },
    )
    axes = Axes(
        x_range=x_range, y_range=y_range,
        x_length=GRAPH_WIDTH, y_length=GRAPH_HEIGHT,
        axis_config={
            "color": GREY_B,
            "include_numbers": True,
            "font_size": 12,
            "numbers_to_exclude": [0],
        },
        tips=False,
    )
    grid.move_to(axes.get_center())
    group = VGroup(grid, axes)

    colors = [ORBITAL_CYAN, "#F97316", "#EC4899", NEON_GREEN]
    plotted = []

    for idx, fn_cfg in enumerate(functions):
        expr_str = fn_cfg.get("expr", "lambda x: x")
        color    = fn_cfg.get("color", colors[idx % len(colors)])
        try:
            fn_obj = eval(expr_str) if "lambda" in expr_str else eval(f"lambda x: {expr_str}")
            y_min, y_max = y_range[0], y_range[1]
            x_lo,  x_hi  = x_range[0], x_range[1]
            test_xs = np.linspace(x_lo, x_hi, 200)
            test_ys = [fn_obj(x) for x in test_xs]
            valid = [x for x, y in zip(test_xs, test_ys) if y_min <= y <= y_max]
            safe_lo = max(x_lo, min(valid) - 0.1) if valid else x_lo
            safe_hi = min(x_hi, max(valid) + 0.1) if valid else x_hi
            curve = axes.plot(fn_obj, x_range=[safe_lo, safe_hi], color=color, stroke_width=2.5)
            group.add(curve)
            plotted.append(fn_obj)
            lbl = fn_cfg.get("label", "")
            if lbl:
                lbl_x = (safe_lo + safe_hi) / 2
                lbl_mob = MathTex(lbl, color=color, font_size=18)
                try:
                    lbl_mob.move_to(axes.c2p(lbl_x, fn_obj(lbl_x)) + UP * 0.25 + LEFT * 0.3)
                except Exception:
                    lbl_mob.move_to(axes.c2p(0, 0) + UP * 0.3)
                group.add(lbl_mob)
        except Exception as e:
            print(f"  ⚠️  Graph plot failed: {e}")

    # Dots at key points (zeros, vertex, intercepts)
    for d in cfg.get("dots", []):
        dx, dy = d.get("x", 0), d.get("y", 0)
        dc = d.get("color", NEON_GREEN)
        dr = d.get("radius", 0.07)
        dl = d.get("label", "")
        try:
            dot_mob = Dot(axes.c2p(dx, dy), color=dc, radius=dr)
            group.add(dot_mob)
            if dl:
                dot_lbl = MathTex(dl, font_size=14, color=dc)
                dot_lbl.next_to(dot_mob, UP + RIGHT, buff=0.08)
                group.add(dot_lbl)
        except Exception:
            pass

    return group

'''

    # SyncedShortScene class with construct() method
    # The manifest data is injected here via repr()
    class_code = (
        "\n\nclass SyncedShortScene(Scene):\n"
        "    # Manifest data embedded at scene-generation time\n"
        "    STEPS_DATA = " + manifest_repr + "\n\n"
        "    def construct(self):\n"
        "        self.camera.background_color = \"#000000\"\n\n"
        "        # ── Neon border (Orbital brand) ────────────────────────────────\n"
        "        border = Rectangle(\n"
        "            width=FRAME_W - 0.15, height=FRAME_H - 0.15,\n"
        "            color=\"#8B5CF6\", stroke_width=2.5, stroke_opacity=0.7,\n"
        "            fill_opacity=0,\n"
        "        )\n"
        "        border.move_to(ORIGIN)\n"
        "        border_glow = Rectangle(\n"
        "            width=FRAME_W - 0.10, height=FRAME_H - 0.10,\n"
        "            color=\"#8B5CF6\", stroke_width=6, stroke_opacity=0.15,\n"
        "            fill_opacity=0,\n"
        "        )\n"
        "        border_glow.move_to(ORIGIN)\n"
        "        self.add(border_glow, border)\n\n"
        "        # ── Watermark ─────────────────────────────────────────────────\n"
        "        wm = Text(\"ORBITAL\", font_size=WM_FONT_SIZE, color=WHITE, weight=BOLD)\n"
        "        wm.set_opacity(0.35)\n"
        "        wm.move_to([-FRAME_W/2 + 0.5, -FRAME_H/2 + 0.2, 0])\n"
        "        self.add(wm)\n\n"
        "        steps   = self.STEPS_DATA\n"
        "        previous = None\n"
        "        graph_mobs = []\n\n"
        "        for i, step in enumerate(steps):\n"
        "            stype      = step.get(\"type\", \"math\")\n"
        "            content    = step.get(\"content\", \"\") or step.get(\"latex\", \"\")\n"
        "            label_txt  = step.get(\"label\", \"\")\n"
        "            duration   = step.get(\"duration\", 3.0)\n"
        "            audio_path = step.get(\"audio_path\", \"\")\n"
        "            layout     = step.get(\"layout\", {})\n"
        "            scale_override = layout.get(\"scale\", 1.0) if layout else 1.0\n"
        "            anim_time  = max(1.2, duration * ANIMATION_RATIO)\n\n"
    )

    # GRAPH handler
    graph_handler = (
        "            # ── GRAPH STEP ─────────────────────────────────────────────\n"
        "            if stype == \"graph\":\n"
        "                graph_cfg = step.get(\"graph\", step.get(\"diagram\", {}))\n"
        "                mob = _build_graph(graph_cfg)\n"
        "                mob.move_to([0, 0, 0])\n"
        "                g_anim = max(1.2, duration * ANIMATION_RATIO)\n"
        "                axes_parts  = VGroup(*[m for m in mob[:2]])\n"
        "                curve_parts = VGroup(*[m for m in mob[2:]]) if len(mob) > 2 else VGroup()\n"
        "                if previous is not None:\n"
        "                    self.play(FadeOut(previous, shift=UP * 0.3), run_time=0.4)\n"
        "                    previous = None\n"
        "                if audio_path and os.path.exists(audio_path):\n"
        "                    self.add_sound(audio_path)\n"
        "                self.play(FadeIn(axes_parts), run_time=g_anim * 0.35)\n"
        "                if len(curve_parts) > 0:\n"
        "                    self.play(Create(curve_parts), run_time=g_anim * 0.65)\n"
        "                hold_center = max(0.3, (duration - g_anim) * 0.5)\n"
        "                self.wait(hold_center)\n"
        "                self.play(mob.animate.move_to([0, GRAPH_CENTER_Y, 0]), run_time=0.8)\n"
        "                remaining = max(0.2, duration - g_anim - hold_center - 0.8)\n"
        "                self.wait(remaining)\n"
        "                graph_mobs.append(mob)\n"
        "                if i < len(steps) - 1:\n"
        "                    self.wait(EXTRA_HOLD)\n"
        "                continue\n\n"
    )

    # ALGEBRA_SOLVE handler
    algebra_handler = (
        "            # ── ALGEBRA_SOLVE STEP ─────────────────────────────────────\n"
        "            if stype == \"algebra_solve\":\n"
        "                as_cfg   = step.get(\"algebra_solve\", {})\n"
        "                as_steps = as_cfg.get(\"steps\", [])\n"
        "                as_title = as_cfg.get(\"title\", \"\")\n"
        "                final_color = as_cfg.get(\"final_color\", NEON_GREEN)\n\n"
        "                if previous is not None:\n"
        "                    self.play(FadeOut(previous, shift=UP * 0.3), run_time=0.3)\n"
        "                    previous = None\n\n"
        "                has_substep_audio = any(s.get(\"audio_path\") for s in as_steps)\n\n"
        "                if as_title:\n"
        "                    t_mob = Text(as_title, font_size=TITLE_FONT_SIZE, color=WHITE)\n"
        "                    t_mob.move_to([0, ZONE_A_Y, 0])\n"
        "                    self.play(Write(t_mob), run_time=0.5)\n"
        "                    self.wait(0.5)\n"
        "                    self.play(FadeOut(t_mob), run_time=0.3)\n\n"
        "                visible_steps = []\n"
        "                spacing = 1.10\n"
        "                max_visible = 5\n"
        "                # Center equations vertically: start from top of usable area\n"
        "                start_y = ZONE_A_Y\n\n"
        "                for si, s in enumerate(as_steps):\n"
        "                    latex      = s.get(\"latex\", \"\")\n"
        "                    note       = s.get(\"note\", \"\")\n"
        "                    note_color = s.get(\"note_color\", ORANGE)\n"
        "                    is_final   = si == len(as_steps) - 1\n"
        "                    sub_audio  = s.get(\"audio_path\", \"\")\n"
        "                    sub_dur    = s.get(\"duration\", s.get(\"hold\", 3.0))\n\n"
        "                    eq = MathTex(latex, font_size=EQ_FONT_SIZE,\n"
        "                                 color=final_color if is_final else WHITE)\n"
        "                    _clamp(eq)\n"
        "                    target_y = start_y - len(visible_steps) * spacing\n"
        "                    eq.move_to([0, target_y, 0])\n\n"
        "                    if sub_audio and os.path.exists(sub_audio):\n"
        "                        self.add_sound(sub_audio)\n"
        "                    elif not has_substep_audio and audio_path and os.path.exists(audio_path) and si == 0:\n"
        "                        self.add_sound(audio_path)\n\n"
        "                    sub_anim = max(0.6, sub_dur * ANIMATION_RATIO)\n"
        "                    self.play(Write(eq), run_time=sub_anim)\n\n"
        "                    if note:\n"
        "                        n_mob = Text(note, font_size=NOTE_FONT_SIZE, color=note_color)\n"
        "                        n_mob.next_to(eq, DOWN + RIGHT, buff=0.08)\n"
        "                        if n_mob.get_right()[0] > FRAME_W/2 - 0.2:\n"
        "                            n_mob.shift(LEFT * (n_mob.get_right()[0] - FRAME_W/2 + 0.2))\n"
        "                        self.play(Write(n_mob), run_time=0.3)\n\n"
        "                    if is_final:\n"
        "                        self.play(Circumscribe(eq, color=final_color), run_time=0.6)\n\n"
        "                    visible_steps.append(eq)\n"
        "                    note_time  = 0.3 if note else 0\n"
        "                    final_time = 0.6 if is_final else 0\n"
        "                    remaining  = max(0.3, sub_dur - sub_anim - note_time - final_time)\n"
        "                    self.wait(remaining)\n\n"
        "                    if note:\n"
        "                        self.play(FadeOut(n_mob), run_time=0.2)\n\n"
        "                    if len(visible_steps) >= max_visible and si < len(as_steps) - 1:\n"
        "                        oldest = visible_steps.pop(0)\n"
        "                        self.play(FadeOut(oldest, shift=UP*0.4), run_time=0.25)\n"
        "                        for vi, v in enumerate(visible_steps):\n"
        "                            v.generate_target()\n"
        "                            v.target.move_to([0, start_y - vi * spacing, 0])\n"
        "                        self.play(*[MoveToTarget(v) for v in visible_steps], run_time=0.3)\n\n"
        "                    if si < len(as_steps) - 1:\n"
        "                        self.wait(EXTRA_HOLD)\n\n"
        "                if visible_steps:\n"
        "                    previous = VGroup(*visible_steps)\n"
        "                continue\n\n"
    )

    # BOX handler
    box_handler = (
        "            # ── BOX STEP ───────────────────────────────────────────────\n"
        "            if stype == \"box\":\n"
        "                inner = Text(content, color=WHITE, font_size=42).scale(scale_override)\n"
        "                _clamp(inner, MAX_WIDTH * 0.85)\n"
        "                box_rect = SurroundingRectangle(\n"
        "                    inner, color=BOX_BORDER, fill_color=BOX_FILL,\n"
        "                    fill_opacity=0.6, buff=0.2, corner_radius=0.1, stroke_width=2,\n"
        "                )\n"
        "                if label_txt:\n"
        "                    lbl = Text(label_txt, color=LABEL_COLOR, font_size=14)\n"
        "                    lbl.next_to(box_rect, UP, buff=0.1)\n"
        "                    mob = VGroup(box_rect, lbl, inner)\n"
        "                else:\n"
        "                    mob = VGroup(box_rect, inner)\n"
        "                _clamp(mob)\n"
        "                mob.move_to([0, MATH_CENTER_Y, 0])\n"
        "                if audio_path and os.path.exists(audio_path):\n"
        "                    self.add_sound(audio_path)\n"
        "                if previous is None:\n"
        "                    self.play(Write(mob), run_time=anim_time)\n"
        "                else:\n"
        "                    self.play(FadeOut(previous, shift=UP * 0.3), run_time=0.3)\n"
        "                    self.wait(0.15)\n"
        "                    self.play(Write(mob), run_time=anim_time)\n"
        "                remaining = max(0.3, duration - anim_time - (0.45 if previous else 0))\n"
        "                self.wait(remaining)\n"
        "                if i < len(steps) - 1:\n"
        "                    self.wait(EXTRA_HOLD)\n"
        "                previous = mob\n"
        "                continue\n\n"
    )

    # MATH (default) handler
    math_handler = (
        "            # ── MATH STEP (default) ────────────────────────────────────\n"
        "            eq_count = content.count('=')\n"
        "            has_aligned = 'aligned' in content or 'begin{' in content\n"
        "            if eq_count >= 2 and not has_aligned:\n"
        "                parts = content.split('=')\n"
        "                aligned_lines = [parts[0].strip() + ' &= ' + parts[1].strip()]\n"
        "                for p in parts[2:]:\n"
        "                    aligned_lines.append('&= ' + p.strip())\n"
        "                aligned_content = (\n"
        "                    r'\\begin{aligned} '\n"
        "                    + r' \\\\[8pt] '.join(aligned_lines)\n"
        "                    + r' \\end{aligned}'\n"
        "                )\n"
        "                mob = MathTex(aligned_content, color=WHITE).scale(MATH_SCALE * scale_override)\n"
        "            else:\n"
        "                mob = MathTex(content, color=WHITE).scale(MATH_SCALE * scale_override)\n"
        "            _clamp(mob)\n"
        "            mob.move_to([0, MATH_CENTER_Y, 0])\n"
        "            if audio_path and os.path.exists(audio_path):\n"
        "                self.add_sound(audio_path)\n"
        "            if previous is None:\n"
        "                self.play(Write(mob), run_time=anim_time)\n"
        "            else:\n"
        "                self.play(FadeOut(previous, shift=UP * 0.3), run_time=0.3)\n"
        "                self.wait(0.15)\n"
        "                self.play(Write(mob), run_time=anim_time)\n"
        "            remaining = max(0.3, duration - anim_time - (0.45 if previous else 0))\n"
        "            self.wait(remaining)\n"
        "            if i < len(steps) - 1:\n"
        "                self.wait(EXTRA_HOLD)\n"
        "            previous = mob\n\n"
    )

    # End card (Orbital Lissajous logo)
    end_card = (
        "        # ── End card ───────────────────────────────────────────────────\n"
        "        if previous:\n"
        "            box = SurroundingRectangle(\n"
        "                previous, color=NEON_GREEN, buff=0.2,\n"
        "                stroke_width=3, corner_radius=0.08,\n"
        "            )\n"
        "            self.play(Create(box), run_time=0.5)\n"
        "            self.wait(1.5)\n"
        "            self.play(FadeOut(previous), FadeOut(box), run_time=0.4)\n\n"
        "        if graph_mobs:\n"
        "            self.play(*[FadeOut(m) for m in graph_mobs], run_time=0.4)\n\n"
        "        # Orbital Lissajous end card\n"
        "        _A, _B = 1.2, 0.95\n"
        "        liss_glow = ParametricFunction(\n"
        "            lambda t: np.array([_A*np.sin(2*t), _B*np.sin(3*t), 0]),\n"
        "            t_range=[0, TAU, 0.02],\n"
        "            color=\"#00E5FF\", stroke_width=8, stroke_opacity=0.2\n"
        "        )\n"
        "        liss_core = ParametricFunction(\n"
        "            lambda t: np.array([_A*np.sin(2*t), _B*np.sin(3*t), 0]),\n"
        "            t_range=[0, TAU, 0.02],\n"
        "            color=\"#00E5FF\", stroke_width=2, stroke_opacity=1.0\n"
        "        )\n"
        "        logo = VGroup(liss_glow, liss_core)\n"
        "        logo.move_to([0, 0.5, 0])\n"
        "        wordmark = Text(\"ORBITAL\", font_size=22, color=\"#00E5FF\", weight=BOLD)\n"
        "        wordmark.next_to(logo, DOWN, buff=0.3)\n"
        "        wm_glow = wordmark.copy().set_opacity(0.3).scale(1.05)\n"
        "        end_card = VGroup(logo, wm_glow, wordmark)\n"
        "        end_card.move_to([0, 0, 0])\n"
        "        self.play(Create(liss_core, run_time=0.8), FadeIn(liss_glow, run_time=0.6))\n"
        "        self.play(FadeIn(VGroup(wm_glow, wordmark), shift=UP*0.2), run_time=0.4)\n"
        "        self.wait(1.2)\n"
        "        self.play(FadeOut(end_card), run_time=0.3)\n"
    )

    return (
        header
        + class_code
        + graph_handler
        + algebra_handler
        + box_handler
        + math_handler
        + end_card
    )


# ─── Manim Runner ─────────────────────────────────────────────────────────────

def _run_manim(scene_path: Path, job_path: Path) -> Optional[Path]:
    """Run Manim to render the generated scene. Returns path to mp4 or None."""
    env = _manim_env()

    cmd = [
        str(VENV_PYTHON), "-m", "manim", "render",
        "--config_file", str(LANDSCAPE_CFG),
        "--resolution", RESOLUTION,
        "--frame_rate", FRAME_RATE,
        "--format", "mp4",
        str(scene_path.name),
        "SyncedShortScene",
    ]

    print(f"  ▶ manim SyncedShortScene (1920×1080, 60fps)...")
    result = subprocess.run(cmd, cwd=str(job_path), env=env, capture_output=True, text=True)

    if result.returncode != 0:
        print(f"  ❌ Manim error:\n{result.stderr[-800:]}")
        return None

    # Search for output in Manim's media directory
    for quality_dir in ["1080p60", "production_quality", "2160p60", "480p15"]:
        candidate = (
            job_path / "media" / "videos" /
            scene_path.stem / quality_dir / "SyncedShortScene.mp4"
        )
        if candidate.exists():
            print(f"  ✓ Rendered: {candidate}")
            return candidate

    # Glob fallback
    found = list(job_path.rglob("SyncedShortScene.mp4"))
    if found:
        print(f"  ✓ Rendered (glob): {found[0]}")
        return found[0]

    print("  ❌ Rendered file not found. Searched:", job_path / "media")
    return None


# ─── Manifest Preview ─────────────────────────────────────────────────────────

def preview_manifest(manifest: list[dict]) -> str:
    """Human-readable step summary without rendering."""
    lines = [f"Manifest ({len(manifest)} steps):", "─" * 50]
    total = 0.0

    for i, step in enumerate(manifest):
        stype    = step.get("type", "?")
        content  = step.get("content", "")
        duration = step.get("duration", 0.0)
        narration = step.get("narration", "")
        total += duration

        if stype == "algebra_solve":
            sub_steps = step.get("algebra_solve", {}).get("steps", [])
            content = f"[{len(sub_steps)} sub-steps]"

        content_snip   = (content[:50] + "...") if len(content) > 50 else content
        narration_snip = (narration[:40] + "...") if len(narration) > 40 else narration

        lines.append(f"  [{i+1:2d}] {stype:20s} | {duration:5.1f}s | {content_snip}")
        if narration_snip:
            lines.append(f"       {'':20s}   {'':5s}   💬 {narration_snip}")

    lines += ["─" * 50, f"  Total duration: ~{total:.1f}s"]
    return "\n".join(lines)


# ─── CLI ──────────────────────────────────────────────────────────────────────

if __name__ == "__main__":
    if len(sys.argv) < 3:
        print("Usage: python render.py <manifest.json> <output.mp4>")
        print("       python render.py <manifest.json> --preview")
        sys.exit(1)

    manifest_path = sys.argv[1]
    output_arg    = sys.argv[2]

    with open(manifest_path) as f:
        manifest = json.load(f)

    if output_arg == "--preview":
        print(preview_manifest(manifest))
    else:
        render_manifest(manifest, output_arg)
