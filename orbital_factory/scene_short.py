"""
Orbital Scene Generator — Short-Form Vertical (9:16)
=====================================================
FORKED FROM standard pipeline's SyncedMathScene — the proven timing model.

TIMING MODEL (exact copy of standard pipeline):
  1. Build mobject + position it (NO timeline cost)
  2. add_sound() — audio starts HERE
  3. FadeOut(previous, 0.4s) — voice plays over fadeout
  4. Write(new, anim_time) — writing begins ~0.4s into audio
  5. wait(remaining) — hold until voice done
  6. wait(EXTRA_HOLD) — breathing room between steps

Changes from standard: portrait frame, graph zone, neon grid, built-in end card.
"""

import json
import os

FRAME_W = 4.5
FRAME_H = 8.0
GRAPH_CENTER_Y = -1.8
MATH_CENTER_Y = 1.2
GRAPH_WIDTH = 3.4
GRAPH_HEIGHT = 2.8
MATH_SCALE = 0.85
BOX_SCALE = 0.65
ANIMATION_RATIO = 0.35
EXTRA_HOLD = 0.8


def create_synced_scene_short(manifest: list, output_path: str, intro_duration: float = 0.0):
    for step in manifest:
        ap = step.get("audio_path", "")
        if ap and not os.path.isabs(ap):
            step["audio_path"] = os.path.abspath(ap)

    scene_code = f'''"""
Auto-generated 9:16 TikTok scene.
Timing model copied verbatim from standard pipeline SyncedMathScene.
"""
from manim import *
import os
import numpy as np

config.frame_width = {FRAME_W}
config.frame_height = {FRAME_H}

ORBITAL_CYAN  = "#22D3EE"
NEON_GREEN    = "#39FF14"
BOX_BORDER    = "#8B5CF6"
BOX_FILL      = "#1a1130"
LABEL_COLOR   = "#22D3EE"
FRAME_W       = {FRAME_W}
FRAME_H       = {FRAME_H}
MAX_WIDTH     = FRAME_W * 0.82
MATH_SCALE    = {MATH_SCALE}
BOX_SCALE     = {BOX_SCALE}
GRAPH_WIDTH   = {GRAPH_WIDTH}
GRAPH_HEIGHT  = {GRAPH_HEIGHT}
MATH_CENTER_Y = {MATH_CENTER_Y}
GRAPH_CENTER_Y = {GRAPH_CENTER_Y}
ANIMATION_RATIO = {ANIMATION_RATIO}
EXTRA_HOLD = {EXTRA_HOLD}


def _clamp(mob, max_w=None):
    if max_w is None:
        max_w = MAX_WIDTH
    if mob.width > max_w:
        mob.scale(max_w / mob.width)
    return mob


def _build_graph(cfg):
    x_range   = cfg.get("x_range", [-3, 3, 1])
    y_range   = cfg.get("y_range", [-7, 25, 5])
    functions = cfg.get("functions", [])
    tangent   = cfg.get("tangent", None)

    x_abs = max(abs(x_range[0]), abs(x_range[1]))
    x_step = x_range[2] if len(x_range) > 2 else 1
    x_range = [-x_abs, x_abs, x_step]

    grid = NumberPlane(
        x_range=x_range, y_range=y_range,
        x_length=GRAPH_WIDTH, y_length=GRAPH_HEIGHT,
        background_line_style={{
            "stroke_color": "#8B5CF6", "stroke_opacity": 0.25, "stroke_width": 1,
        }},
        faded_line_style={{
            "stroke_color": "#22D3EE", "stroke_opacity": 0.12, "stroke_width": 0.5,
        }},
    )
    axes = Axes(
        x_range=x_range, y_range=y_range,
        x_length=GRAPH_WIDTH, y_length=GRAPH_HEIGHT,
        axis_config={{
            "color": GREY_B, "include_numbers": True, "font_size": 12,
            "numbers_to_exclude": [0],
        }},
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
            if "lambda" in expr_str:
                fn_obj = eval(expr_str)
            else:
                fn_obj = eval(f"lambda x: {{expr_str}}")
            y_min, y_max = y_range[0], y_range[1]
            x_lo, x_hi = x_range[0], x_range[1]
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
            print(f"  ⚠️  Graph eval failed: {{e}}")

    if tangent and plotted:
        at_x  = tangent.get("at_x", 0)
        t_len = tangent.get("length", 2.0)
        t_col = tangent.get("color", NEON_GREEN)
        try:
            fn = plotted[tangent.get("func_index", 0)]
            dx = 1e-5
            slope = (fn(at_x + dx) - fn(at_x - dx)) / (2 * dx)
            y0 = fn(at_x)
            half = t_len / 2
            tline = Line(
                axes.c2p(at_x - half, y0 - slope * half),
                axes.c2p(at_x + half, y0 + slope * half),
                color=t_col, stroke_width=2.5
            )
            dot = Dot(axes.c2p(at_x, y0), color=t_col, radius=0.06)
            group.add(tline, dot)
        except Exception:
            pass

    shaded = cfg.get("shaded_area", None)
    if shaded and plotted:
        fi = shaded.get("func_index", 0)
        sr = shaded.get("x_range", [x_range[0], x_range[1]])
        sc = shaded.get("color", ORBITAL_CYAN)
        so = shaded.get("opacity", 0.3)
        try:
            if fi < len(plotted):
                top_graph = axes.plot(plotted[fi], color=sc)
                area = axes.get_area(top_graph, x_range=sr, color=sc, opacity=so)
                group.add(area)
        except Exception:
            pass

    return group


class SyncedShortScene(Scene):
    STEPS_DATA = {repr(manifest)}

    def construct(self):
        self.camera.background_color = "#000000"

        # Neon border around entire screen
        border = Rectangle(
            width=FRAME_W - 0.15, height=FRAME_H - 0.15,
            color="#8B5CF6", stroke_width=2.5, stroke_opacity=0.7,
            fill_opacity=0,
        )
        border.move_to(ORIGIN)
        # Outer glow layer
        border_glow = Rectangle(
            width=FRAME_W - 0.10, height=FRAME_H - 0.10,
            color="#8B5CF6", stroke_width=6, stroke_opacity=0.15,
            fill_opacity=0,
        )
        border_glow.move_to(ORIGIN)
        self.add(border_glow, border)

        # Watermark
        wm = Text("ORBITAL", font_size=10, color=WHITE, weight=BOLD)
        wm.set_opacity(0.35)
        wm.move_to([-FRAME_W/2 + 0.5, -FRAME_H/2 + 0.2, 0])
        self.add(wm)

        steps = self.STEPS_DATA
        graph_mobs = []

        # ── ALL STEPS IN ORDER (respect script sequence) ──
        previous = None

        for i, step in enumerate(steps):
            stype = step.get("type", "math")

            # ── GRAPH STEP ──
            if stype == "graph":
                duration   = step.get("duration", 8.0)
                audio_path = step.get("audio_path", "")
                graph_cfg  = step.get("graph", step.get("diagram", {{}}))

                # If graph_cfg is empty but we have a "content" expression, build a default config
                if not graph_cfg.get("functions") and step.get("content"):
                    expr = step["content"]
                    graph_cfg = {{
                        "x_range": [-3, 3, 1],
                        "y_range": [-2, 10, 2],
                        "functions": [{{"expr": expr, "label": "f(x)"}}],
                    }}

                # 1. BUILD mobject first
                mob = _build_graph(graph_cfg)
                mob.move_to([0, 0, 0])  # center screen — hero moment

                anim_time = max(1.2, duration * ANIMATION_RATIO)
                axes_parts = VGroup(*[m for m in mob[:2]])
                curve_parts = VGroup(*[m for m in mob[2:]]) if len(mob) > 2 else VGroup()

                # Fade out previous content if any
                if previous is not None:
                    self.play(FadeOut(previous, shift=UP * 0.3), run_time=0.4)
                    previous = None

                # 2. Start audio
                if audio_path and os.path.exists(audio_path):
                    self.add_sound(audio_path)

                # 3. Animate
                self.play(FadeIn(axes_parts), run_time=anim_time * 0.35)
                if len(curve_parts) > 0:
                    self.play(Create(curve_parts), run_time=anim_time * 0.65)

                # 4. Hold at center
                hold_center = max(0.3, (duration - anim_time) * 0.5)
                self.wait(hold_center)

                # 5. Slide down
                self.play(mob.animate.move_to([0, GRAPH_CENTER_Y, 0]), run_time=0.8)

                # 6. Remaining hold
                remaining = max(0.2, duration - anim_time - hold_center - 0.8)
                self.wait(remaining)

                graph_mobs.append(mob)
                if i < len(steps) - 1:
                    self.wait(EXTRA_HOLD)
                continue

            # ── ANIMATED DOT (dot slides along curve with tangent line) ──
            if stype == "animated_dot":
                duration   = step.get("duration", 8.0)
                audio_path = step.get("audio_path", "")
                content    = step.get("content", "x**2")
                dot_range  = step.get("dot_range", [-2, 2])
                show_tangent = step.get("show_tangent", True)
                layout     = step.get("layout", {{}})

                fn = eval(f"lambda x: {{content}}")

                # Use existing graph or build one
                if graph_mobs:
                    axes = graph_mobs[-1][1]  # axes is second element
                else:
                    axes = Axes(
                        x_range=[-3, 3, 1], y_range=[-2, 10, 2],
                        x_length=GRAPH_WIDTH, y_length=GRAPH_HEIGHT,
                        axis_config={{"color": GREY_B, "include_numbers": True, "font_size": 12, "numbers_to_exclude": [0]}},
                        tips=False,
                    )
                    axes.move_to([0, GRAPH_CENTER_Y, 0])
                    curve = axes.plot(fn, x_range=[dot_range[0]-0.5, dot_range[1]+0.5], color=ORBITAL_CYAN, stroke_width=2.5)
                    self.play(FadeIn(axes), Create(curve), run_time=1.0)

                # Fade out previous content
                if previous is not None:
                    self.play(FadeOut(previous, shift=UP * 0.3), run_time=0.3)
                    previous = None

                # ValueTracker drives the dot position
                t = ValueTracker(dot_range[0])

                dot = always_redraw(lambda: Dot(
                    axes.c2p(t.get_value(), fn(t.get_value())),
                    color=NEON_GREEN, radius=0.08
                ))

                if show_tangent:
                    def _get_tangent_line():
                        x0 = t.get_value()
                        dx = 0.001
                        slope = (fn(x0 + dx) - fn(x0 - dx)) / (2 * dx)
                        y0 = fn(x0)
                        half = 1.2
                        return Line(
                            axes.c2p(x0 - half, y0 - slope * half),
                            axes.c2p(x0 + half, y0 + slope * half),
                            color=NEON_GREEN, stroke_width=2.5
                        )
                    tangent_line = always_redraw(_get_tangent_line)

                # Optional live slope label
                show_slope = step.get("show_slope", False)
                slope_mob = None
                if show_slope:
                    slope_mob = always_redraw(lambda: Text(
                        f"slope = {{2 * t.get_value():.1f}}" if "x**2" in content else f"slope = {{(fn(t.get_value()+0.001)-fn(t.get_value()-0.001))/0.002:.1f}}",
                        font_size=22, color=NEON_GREEN
                    ).move_to([0, MATH_CENTER_Y, 0]))

                # Start audio
                if audio_path and os.path.exists(audio_path):
                    self.add_sound(audio_path)

                self.play(FadeIn(dot), run_time=0.3)
                if show_tangent:
                    self.play(Create(tangent_line), run_time=0.5)
                if slope_mob:
                    self.play(Write(slope_mob), run_time=0.3)

                self.play(t.animate.set_value(dot_range[1]), run_time=duration * 0.7, rate_func=smooth)
                remaining = max(0.3, duration * 0.2)
                self.wait(remaining)

                self.remove(dot)
                if show_tangent:
                    self.remove(tangent_line)
                if slope_mob:
                    self.remove(slope_mob)
                if i < len(steps) - 1:
                    self.wait(EXTRA_HOLD)
                continue

            # ── SECANT TO TANGENT (two dots merge, secant becomes tangent) ──
            if stype == "secant_to_tangent":
                duration   = step.get("duration", 10.0)
                audio_path = step.get("audio_path", "")
                content    = step.get("content", "x**2")
                fixed_x    = step.get("fixed_x", 1)
                h_start    = step.get("h_start", 2.0)
                h_end      = step.get("h_end", 0.05)
                layout     = step.get("layout", {{}})

                fn = eval(f"lambda x: {{content}}")

                if graph_mobs:
                    axes = graph_mobs[-1][1]
                else:
                    axes = Axes(
                        x_range=[-3, 3, 1], y_range=[-2, 10, 2],
                        x_length=GRAPH_WIDTH, y_length=GRAPH_HEIGHT,
                        axis_config={{"color": GREY_B, "include_numbers": True, "font_size": 12, "numbers_to_exclude": [0]}},
                        tips=False,
                    )
                    axes.move_to([0, GRAPH_CENTER_Y, 0])
                    curve = axes.plot(fn, x_range=[-3, 3], color=ORBITAL_CYAN, stroke_width=2.5)
                    self.play(FadeIn(axes), Create(curve), run_time=1.0)

                if previous is not None:
                    self.play(FadeOut(previous, shift=UP * 0.3), run_time=0.3)
                    previous = None

                h_tracker = ValueTracker(h_start)
                x0 = fixed_x

                fixed_dot = Dot(axes.c2p(x0, fn(x0)), color=NEON_GREEN, radius=0.08)

                moving_dot = always_redraw(lambda: Dot(
                    axes.c2p(x0 + h_tracker.get_value(), fn(x0 + h_tracker.get_value())),
                    color="#F97316", radius=0.08
                ))

                secant = always_redraw(lambda: Line(
                    axes.c2p(x0 - 1, fn(x0) + (-1) * (fn(x0 + h_tracker.get_value()) - fn(x0)) / max(h_tracker.get_value(), 0.001)),
                    axes.c2p(x0 + h_tracker.get_value() + 1, fn(x0 + h_tracker.get_value()) + 1 * (fn(x0 + h_tracker.get_value()) - fn(x0)) / max(h_tracker.get_value(), 0.001)),
                    color=BOX_BORDER, stroke_width=2.5
                ))

                h_label = always_redraw(lambda: Text(
                    f"h = {{h_tracker.get_value():.3f}}",
                    font_size=24, color=WHITE
                ).move_to([FRAME_W/2 - 0.8, MATH_CENTER_Y + 1.5, 0]))

                if audio_path and os.path.exists(audio_path):
                    self.add_sound(audio_path)

                self.add(fixed_dot, moving_dot, secant, h_label)
                self.play(
                    h_tracker.animate.set_value(h_end),
                    run_time=duration * 0.75,
                    rate_func=smooth
                )

                # Flash the tangent line green when it locks in
                final_tangent = secant.copy().set_color(NEON_GREEN)
                self.play(Transform(secant, final_tangent), Flash(fixed_dot, color=NEON_GREEN), run_time=0.5)
                self.wait(max(0.3, duration * 0.2))

                self.remove(moving_dot, secant, h_label)
                if i < len(steps) - 1:
                    self.wait(EXTRA_HOLD)
                continue

            # ── RISE/RUN (triangle showing slope between two points) ──
            if stype == "rise_run":
                duration   = step.get("duration", 6.0)
                audio_path = step.get("audio_path", "")
                content    = step.get("content", "x**2")
                x1         = step.get("x1", 1)
                x2         = step.get("x2", 3)
                layout     = step.get("layout", {{}})

                fn = eval(f"lambda x: {{content}}")

                if graph_mobs:
                    axes = graph_mobs[-1][1]
                else:
                    axes = Axes(
                        x_range=[-3, 3, 1], y_range=[-2, 10, 2],
                        x_length=GRAPH_WIDTH, y_length=GRAPH_HEIGHT,
                        axis_config={{"color": GREY_B, "include_numbers": True, "font_size": 12, "numbers_to_exclude": [0]}},
                        tips=False,
                    )
                    axes.move_to([0, GRAPH_CENTER_Y, 0])

                if previous is not None:
                    self.play(FadeOut(previous, shift=UP * 0.3), run_time=0.3)
                    previous = None

                y1, y2 = fn(x1), fn(x2)
                dot1 = Dot(axes.c2p(x1, y1), color=NEON_GREEN, radius=0.08)
                dot2 = Dot(axes.c2p(x2, y2), color="#F97316", radius=0.08)

                # Horizontal line (run)
                run_line = DashedLine(axes.c2p(x1, y1), axes.c2p(x2, y1), color=ORBITAL_CYAN, stroke_width=2)
                # Vertical line (rise)
                rise_line = DashedLine(axes.c2p(x2, y1), axes.c2p(x2, y2), color=NEON_GREEN, stroke_width=2)
                # Secant line
                slope = (y2 - y1) / (x2 - x1)
                sec_line = Line(
                    axes.c2p(x1 - 0.5, y1 - 0.5 * slope),
                    axes.c2p(x2 + 0.5, y2 + 0.5 * slope),
                    color=BOX_BORDER, stroke_width=2.5
                )

                # Labels
                run_label = Text("run", font_size=18, color=ORBITAL_CYAN)
                run_label.next_to(run_line, DOWN, buff=0.1)
                rise_label = Text("rise", font_size=18, color=NEON_GREEN)
                rise_label.next_to(rise_line, RIGHT, buff=0.1)

                anim_time = max(1.2, duration * ANIMATION_RATIO)

                if audio_path and os.path.exists(audio_path):
                    self.add_sound(audio_path)

                self.play(FadeIn(dot1), FadeIn(dot2), Create(sec_line), run_time=anim_time * 0.4)
                self.play(Create(run_line), Write(run_label), run_time=anim_time * 0.3)
                self.play(Create(rise_line), Write(rise_label), run_time=anim_time * 0.3)

                remaining = max(0.3, duration - anim_time)
                self.wait(remaining)

                mob = VGroup(dot1, dot2, run_line, rise_line, sec_line, run_label, rise_label)
                previous = mob
                if i < len(steps) - 1:
                    self.wait(EXTRA_HOLD)
                continue

            # ── H COUNTDOWN (animated number showing h shrinking) ──
            if stype == "h_countdown":
                duration   = step.get("duration", 5.0)
                audio_path = step.get("audio_path", "")
                h_start    = step.get("start", 2.0)
                h_end      = step.get("end", 0.01)
                layout     = step.get("layout", {{}})

                if previous is not None:
                    self.play(FadeOut(previous, shift=UP * 0.3), run_time=0.3)
                    previous = None

                h_val = ValueTracker(h_start)
                h_text = Text("h = ", font_size=42, color=WHITE).move_to([0, MATH_CENTER_Y + 0.3, 0])
                h_num = always_redraw(lambda: DecimalNumber(
                    h_val.get_value(), num_decimal_places=4, font_size=48, color=NEON_GREEN
                ).next_to(h_text, RIGHT, buff=0.15))

                if audio_path and os.path.exists(audio_path):
                    self.add_sound(audio_path)

                self.play(Write(h_text), FadeIn(h_num), run_time=0.8)
                self.play(h_val.animate.set_value(h_end), run_time=duration * 0.7, rate_func=smooth)
                self.play(Indicate(h_num, color=NEON_GREEN), run_time=0.5)
                remaining = max(0.3, duration * 0.15)
                self.wait(remaining)

                previous = VGroup(h_text, h_num)
                if i < len(steps) - 1:
                    self.wait(EXTRA_HOLD)
                continue

            # ── EQUATION HIGHLIGHT (color-coded parts light up) ──
            if stype == "equation_highlight":
                duration   = step.get("duration", 6.0)
                audio_path = step.get("audio_path", "")
                parts      = step.get("parts", [])
                colors     = step.get("colors", [])
                layout     = step.get("layout", {{}})
                scale_override = layout.get("scale", 1.0) if layout else 1.0

                if previous is not None:
                    self.play(FadeOut(previous, shift=UP * 0.3), run_time=0.3)
                    previous = None

                # Build equation with colored substrings
                tex_parts = parts if parts else [step.get("content", "")]
                mob = MathTex(*tex_parts, color=WHITE).scale(MATH_SCALE * scale_override)
                _clamp(mob)
                mob.move_to([0, MATH_CENTER_Y, 0])

                if audio_path and os.path.exists(audio_path):
                    self.add_sound(audio_path)

                self.play(Write(mob), run_time=1.2)

                # Highlight each part sequentially
                part_colors = colors if colors else [ORBITAL_CYAN, NEON_GREEN, "#F97316", BOX_BORDER]
                time_per_part = max(0.4, (duration - 2.0) / max(len(tex_parts), 1))
                for idx, part_mob in enumerate(mob):
                    if idx < len(part_colors):
                        self.play(
                            part_mob.animate.set_color(part_colors[idx]),
                            Indicate(part_mob, color=part_colors[idx]),
                            run_time=time_per_part
                        )

                remaining = max(0.3, duration - 1.2 - time_per_part * len(tex_parts))
                self.wait(remaining)

                previous = mob
                if i < len(steps) - 1:
                    self.wait(EXTRA_HOLD)
                continue

            # ── TRANSFORM (morph one equation into another) ──
            if stype == "transform":
                duration   = step.get("duration", 5.0)
                audio_path = step.get("audio_path", "")
                from_tex   = step.get("from_tex", step.get("content", ""))
                to_tex     = step.get("to_tex", "")
                layout     = step.get("layout", {{}})
                scale_override = layout.get("scale", 1.0) if layout else 1.0

                if previous is not None:
                    self.play(FadeOut(previous, shift=UP * 0.3), run_time=0.3)
                    previous = None

                mob_from = MathTex(from_tex, color=WHITE).scale(MATH_SCALE * scale_override)
                mob_to   = MathTex(to_tex, color=WHITE).scale(MATH_SCALE * scale_override)
                _clamp(mob_from)
                _clamp(mob_to)
                mob_from.move_to([0, MATH_CENTER_Y, 0])
                mob_to.move_to([0, MATH_CENTER_Y, 0])

                if audio_path and os.path.exists(audio_path):
                    self.add_sound(audio_path)

                self.play(Write(mob_from), run_time=1.0)
                self.wait(max(0.5, duration * 0.3))
                self.play(TransformMatchingTex(mob_from, mob_to), run_time=1.5)
                remaining = max(0.3, duration - 3.0)
                self.wait(remaining)

                previous = mob_to
                if i < len(steps) - 1:
                    self.wait(EXTRA_HOLD)
                continue

            # ── INDICATE (flash/highlight an existing element) ──
            if stype == "indicate":
                duration   = step.get("duration", 3.0)
                audio_path = step.get("audio_path", "")
                content    = step.get("content", "")
                layout     = step.get("layout", {{}})
                scale_override = layout.get("scale", 1.0) if layout else 1.0

                mob = MathTex(content, color=WHITE).scale(MATH_SCALE * scale_override)
                _clamp(mob)
                mob.move_to([0, MATH_CENTER_Y, 0])

                if previous is not None:
                    self.play(FadeOut(previous, shift=UP * 0.3), run_time=0.3)

                if audio_path and os.path.exists(audio_path):
                    self.add_sound(audio_path)

                self.play(Write(mob), run_time=0.8)
                self.play(Circumscribe(mob, color=NEON_GREEN, run_time=1.0))
                self.play(Flash(mob.get_center(), color=NEON_GREEN, num_lines=8, run_time=0.5))
                remaining = max(0.3, duration - 2.3)
                self.wait(remaining)

                previous = mob
                if i < len(steps) - 1:
                    self.wait(EXTRA_HOLD)
                continue

            # ── CONTENT STEP ──
            duration   = step.get("duration", 2.0)
            audio_path = step.get("audio_path", "")
            stype      = step.get("type", "math")
            content    = step.get("content") or step.get("latex", "")
            label_txt  = step.get("label", "")
            layout     = step.get("layout", {{}})
            scale_override = layout.get("scale", 1.0) if layout else 1.0

            anim_time = max(1.2, duration * ANIMATION_RATIO)

            # ═══════════════════════════════════════════════════
            # ALGEBRA SOLVE (proven in definition of derivative prototype)
            # ═══════════════════════════════════════════════════
            if stype == "algebra_solve":
                as_cfg = step.get("algebra_solve", {{}})
                as_steps = as_cfg.get("steps", [])
                as_title = as_cfg.get("title", "")
                final_color = as_cfg.get("final_color", NEON_GREEN)

                if previous is not None:
                    self.play(FadeOut(previous, shift=UP * 0.3), run_time=0.3)
                    previous = None

                if audio_path and os.path.exists(audio_path):
                    self.add_sound(audio_path)

                if as_title:
                    t_mob = Text(as_title, font_size=24, color=WHITE)
                    t_mob.move_to([0, ZONE_A_Y, 0])
                    self.play(Write(t_mob), run_time=0.5)
                    self.wait(0.5)
                    self.play(FadeOut(t_mob), run_time=0.3)

                visible_steps = []
                spacing = 0.55
                max_visible = 3
                start_y = ZONE_A_Y

                for si, s in enumerate(as_steps):
                    latex = s.get("latex", "")
                    note = s.get("note", "")
                    note_color = s.get("note_color", ORANGE)
                    is_final = si == len(as_steps) - 1
                    hold = s.get("hold", 1.5)

                    eq = MathTex(latex, font_size=24, color=final_color if is_final else WHITE)
                    target_y = start_y - len(visible_steps) * spacing
                    eq.move_to([0, target_y, 0])

                    if note:
                        n_mob = Text(note, font_size=16, color=note_color)
                        n_mob.move_to([1.5, target_y + 0.15, 0])
                        self.play(Write(n_mob), run_time=0.3)

                    self.play(Write(eq), run_time=0.8)
                    if is_final:
                        self.play(Circumscribe(eq, color=final_color), run_time=0.6)
                    visible_steps.append(eq)

                    if note:
                        self.wait(max(0.3, hold - 1.1))
                        self.play(FadeOut(n_mob), run_time=0.2)
                    else:
                        self.wait(max(0.3, hold - 0.8))

                    if len(visible_steps) >= max_visible and si < len(as_steps) - 1:
                        oldest = visible_steps.pop(0)
                        self.play(FadeOut(oldest, shift=UP*0.4), run_time=0.25)
                        for vi, v in enumerate(visible_steps):
                            v.generate_target()
                            v.target.move_to([0, start_y - vi * spacing, 0])
                        self.play(*[MoveToTarget(v) for v in visible_steps], run_time=0.3)

                if visible_steps:
                    previous = VGroup(*visible_steps)

                remaining = max(0.1, duration - sum(s.get("hold", 1.5) for s in as_steps))
                if remaining > 0:
                    self.wait(remaining)
                continue

            # ═══════════════════════════════════════════════════
            # FOIL EXPANSION (proven in definition of derivative prototype)
            # ═══════════════════════════════════════════════════
            if stype == "foil_expansion":
                fe_cfg = step.get("foil_expansion", {{}})
                expression = fe_cfg.get("expression", "(x+h)^2")
                factored = fe_cfg.get("factored", "(x+h)(x+h)")
                terms = fe_cfg.get("terms", [
                    {{"latex": r"x \\cdot x", "color": ORBITAL_CYAN}},
                    {{"latex": r"+ x \\cdot h", "color": ORBITAL_VIOLET}},
                    {{"latex": r"+ h \\cdot x", "color": ORBITAL_VIOLET}},
                    {{"latex": r"+ h \\cdot h", "color": ORANGE}},
                ])
                result = fe_cfg.get("result", r"x^2 + 2xh + h^2")

                if previous is not None:
                    self.play(FadeOut(previous, shift=UP * 0.3), run_time=0.3)
                    previous = None

                if audio_path and os.path.exists(audio_path):
                    self.add_sound(audio_path)

                fe_title = Text(f"Expand {{expression}}", font_size=20, color=ORANGE)
                fe_title.move_to([0, ZONE_A_Y + 0.3, 0])
                self.play(Write(fe_title), run_time=0.4)

                fe_factored = MathTex(f"{{expression}} = {{factored}}", font_size=24, color=WHITE)
                fe_factored.move_to([0, ZONE_A_Y - 0.1, 0])
                self.play(Write(fe_factored), run_time=0.8)
                self.wait(0.8)

                term_parts = []
                for t in terms:
                    tp = MathTex(t["latex"], font_size=22, color=t.get("color", WHITE))
                    term_parts.append(tp)

                foil_line = VGroup(*term_parts).arrange(RIGHT, buff=0.05)
                foil_line.move_to([0, ZONE_A_Y - 0.6, 0])
                eq_sign = MathTex("=", font_size=22, color=WHITE).next_to(foil_line, LEFT, buff=0.1)

                self.play(Write(eq_sign), run_time=0.2)
                for tp in term_parts:
                    self.play(Write(tp), run_time=0.4)
                    self.wait(0.3)
                self.wait(0.5)

                fe_result = MathTex(f"= {{result}}", font_size=26, color=NEON_GREEN)
                fe_result.move_to([0, ZONE_A_Y - 1.1, 0])
                self.play(Write(fe_result), run_time=0.8)
                self.play(Circumscribe(fe_result, color=NEON_GREEN), run_time=0.5)
                self.wait(1.0)

                self.play(
                    FadeOut(fe_title), FadeOut(fe_factored),
                    FadeOut(eq_sign), FadeOut(foil_line), FadeOut(fe_result),
                    run_time=0.3
                )
                previous = None
                continue

            # ═══════════════════════════════════════════════════
            # STEP 1: BUILD MOBJECT (before audio starts)
            # ═══════════════════════════════════════════════════
            if stype == "box":
                # Use Text() for boxes to preserve spaces; MathTex strips whitespace
                inner = Text(content, color=WHITE, font_size=42).scale(scale_override)
                _clamp(inner, MAX_WIDTH * 0.85)
                box_rect = SurroundingRectangle(
                    inner, color=BOX_BORDER, fill_color=BOX_FILL,
                    fill_opacity=0.6, buff=0.2, corner_radius=0.1, stroke_width=2,
                )
                if label_txt:
                    lbl = Text(label_txt, color=LABEL_COLOR, font_size=14)
                    lbl.next_to(box_rect, UP, buff=0.1)
                    mob = VGroup(box_rect, lbl, inner)
                else:
                    mob = VGroup(box_rect, inner)
                _clamp(mob)
            else:
                # Auto-break long equations at = signs for vertical layout
                eq_count = content.count('=')
                has_aligned = 'aligned' in content or 'begin{{' in content
                if eq_count >= 2 and not has_aligned:
                    # Split at = signs, rebuild as aligned with & before each =
                    parts = content.split('=')
                    # First line: everything before first = , then &= rest
                    aligned_lines = [parts[0].strip() + ' &= ' + parts[1].strip()]
                    for p in parts[2:]:
                        aligned_lines.append('&= ' + p.strip())
                    aligned_content = r'\\begin{{aligned}} ' + r' \\\\[8pt] '.join(aligned_lines) + r' \\end{{aligned}}'
                    mob = MathTex(aligned_content, color=WHITE).scale(MATH_SCALE * scale_override)
                else:
                    mob = MathTex(content, color=WHITE).scale(MATH_SCALE * scale_override)
                _clamp(mob)

            mob.move_to([0, MATH_CENTER_Y, 0])

            # ═══════════════════════════════════════════════════
            # STEP 2: START AUDIO (nothing between this and animation)
            # ═══════════════════════════════════════════════════
            if audio_path and os.path.exists(audio_path):
                self.add_sound(audio_path)

            # ═══════════════════════════════════════════════════
            # STEP 3: FADEOUT previous + WRITE new
            # (exact same pattern as standard pipeline)
            # ═══════════════════════════════════════════════════
            if previous is None:
                self.play(Write(mob), run_time=anim_time)
            else:
                self.play(FadeOut(previous, shift=UP * 0.3), run_time=0.3)
                self.wait(0.15)  # brief beat so voice leads the visual
                self.play(Write(mob), run_time=anim_time)

            # ═══════════════════════════════════════════════════
            # STEP 4: HOLD (voice finishes during this)
            # ═══════════════════════════════════════════════════
            remaining = max(0.3, duration - anim_time - (0.45 if previous else 0))
            self.wait(remaining)

            if i < len(steps) - 1:
                self.wait(EXTRA_HOLD)

            previous = mob

        # ── END CARD (replaces separate outro) ──
        if previous:
            box = SurroundingRectangle(
                previous, color=NEON_GREEN, buff=0.2,
                stroke_width=3, corner_radius=0.08,
            )
            self.play(Create(box), run_time=0.5)
            self.wait(1.5)
            self.play(FadeOut(previous), FadeOut(box), run_time=0.4)

        if graph_mobs:
            self.play(*[FadeOut(m) for m in graph_mobs], run_time=0.4)

        # ── Orbital Lissajous end card ──
        _A, _B = 1.2, 0.95  # scaled for end card
        liss_glow = ParametricFunction(
            lambda t: np.array([_A*np.sin(3*t), _B*np.sin(2*t), 0]),
            t_range=[0, TAU, 0.02],
            color="#00E5FF", stroke_width=8, stroke_opacity=0.2
        )
        liss_core = ParametricFunction(
            lambda t: np.array([_A*np.sin(3*t), _B*np.sin(2*t), 0]),
            t_range=[0, TAU, 0.02],
            color="#00E5FF", stroke_width=2, stroke_opacity=1.0
        )
        logo = VGroup(liss_glow, liss_core)
        logo.move_to([0, 0.5, 0])
        
        wordmark = Text("ORBITAL", font_size=22, color="#00E5FF", weight=BOLD)
        wordmark.next_to(logo, DOWN, buff=0.3)
        wm_glow = wordmark.copy().set_opacity(0.3).scale(1.05)
        
        end_card = VGroup(logo, wm_glow, wordmark)
        end_card.move_to([0, 0, 0])
        
        self.play(Create(liss_core, run_time=0.8), FadeIn(liss_glow, run_time=0.6))
        self.play(FadeIn(VGroup(wm_glow, wordmark), shift=UP*0.2), run_time=0.4)
        self.wait(1.2)
        self.play(FadeOut(end_card), run_time=0.3)
'''

    with open(output_path, "w") as f:
        f.write(scene_code)

    print(f"  ✓ Created 9:16 TikTok 3-zone scene: {output_path}")
