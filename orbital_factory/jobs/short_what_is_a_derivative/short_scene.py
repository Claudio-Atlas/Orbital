"""
Auto-generated 9:16 TikTok scene.
Timing model copied verbatim from standard pipeline SyncedMathScene.
"""
from manim import *
import os
import numpy as np

config.frame_width = 4.5
config.frame_height = 8.0

ORBITAL_CYAN  = "#22D3EE"
NEON_GREEN    = "#39FF14"
BOX_BORDER    = "#8B5CF6"
BOX_FILL      = "#1a1130"
LABEL_COLOR   = "#22D3EE"
FRAME_W       = 4.5
FRAME_H       = 8.0
MAX_WIDTH     = FRAME_W * 0.82
MATH_SCALE    = 0.85
BOX_SCALE     = 0.65
GRAPH_WIDTH   = 3.4
GRAPH_HEIGHT  = 2.8
MATH_CENTER_Y = 1.2
GRAPH_CENTER_Y = -1.8
ANIMATION_RATIO = 0.35
EXTRA_HOLD = 0.8


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
        background_line_style={
            "stroke_color": "#8B5CF6", "stroke_opacity": 0.25, "stroke_width": 1,
        },
        faded_line_style={
            "stroke_color": "#22D3EE", "stroke_opacity": 0.12, "stroke_width": 0.5,
        },
    )
    axes = Axes(
        x_range=x_range, y_range=y_range,
        x_length=GRAPH_WIDTH, y_length=GRAPH_HEIGHT,
        axis_config={
            "color": GREY_B, "include_numbers": True, "font_size": 12,
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
            if "lambda" in expr_str:
                fn_obj = eval(expr_str)
            else:
                fn_obj = eval(f"lambda x: {expr_str}")
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
            print(f"  ⚠️  Graph eval failed: {e}")

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
    STEPS_DATA = [{'step': 0, 'type': 'box', 'content': 'What IS a Derivative?', 'narration': 'What if I told you every curve has a hidden speed at every point?', 'layout': {'scale': 1.3}, 'audio_path': '/Users/claudioatlas/Desktop/Orbital/orbital_factory/jobs/short_what_is_a_derivative/audio/step_00.mp3', 'duration': 5.226}, {'step': 1, 'type': 'graph', 'content': 'x**2', 'narration': "Take this curve, f of x equals x squared. Near the bottom, around x equals zero, it's almost flat. But as you move to the right, toward x equals two or three, it climbs faster and faster.", 'layout': {'scale': 1.0}, 'audio_path': '/Users/claudioatlas/Desktop/Orbital/orbital_factory/jobs/short_what_is_a_derivative/audio/step_01.mp3', 'duration': 16.279}, {'step': 2, 'type': 'box', 'content': 'How steep is the curve at ONE specific point?', 'narration': 'So the big question is: how steep is this curve at one specific point? Not on average. At exactly that spot.', 'layout': {'scale': 1.1}, 'audio_path': '/Users/claudioatlas/Desktop/Orbital/orbital_factory/jobs/short_what_is_a_derivative/audio/step_02.mp3', 'duration': 9.406}, {'step': 3, 'type': 'box', 'content': 'Secant Line: a straight line through two points on the curve', 'narration': "Here's the idea. Pick two points on the curve and draw a straight line through them. That's called a secant line. Its slope gives you the average rate of change between those two points.", 'layout': {'scale': 1.0}, 'audio_path': '/Users/claudioatlas/Desktop/Orbital/orbital_factory/jobs/short_what_is_a_derivative/audio/step_03.mp3', 'duration': 12.656}, {'step': 4, 'type': 'math', 'content': '\\text{Slope of Secant} = \\frac{f(x+h) - f(x)}{h}', 'narration': 'The slope of that secant line is f of x plus h minus f of x, all divided by h. That h is the horizontal gap between your two x values.', 'layout': {'scale': 1.2}, 'audio_path': '/Users/claudioatlas/Desktop/Orbital/orbital_factory/jobs/short_what_is_a_derivative/audio/step_04.mp3', 'duration': 13.26}, {'step': 5, 'type': 'box', 'content': 'Now slide the second point closer... and closer...', 'narration': "Now here's where it gets beautiful. Slide that second point closer and closer to the first one. In math, we call this taking a limit. As h shrinks toward zero, the secant line rotates and settles into one perfect position.", 'layout': {'scale': 1.1}, 'audio_path': '/Users/claudioatlas/Desktop/Orbital/orbital_factory/jobs/short_what_is_a_derivative/audio/step_05.mp3', 'duration': 18.322}, {'step': 6, 'type': 'box', 'content': 'Secant Line → Tangent Line', 'narration': 'When h reaches zero, the secant line becomes a tangent line. A line that just touches the curve at that single point, matching its exact steepness.', 'layout': {'scale': 1.2}, 'audio_path': '/Users/claudioatlas/Desktop/Orbital/orbital_factory/jobs/short_what_is_a_derivative/audio/step_06.mp3', 'duration': 11.635}, {'step': 7, 'type': 'math', 'content': "f'(x) = \\lim_{h \\to 0} \\frac{f(x+h) - f(x)}{h}", 'narration': "And that's the derivative. The limit as h approaches zero of f of x plus h minus f of x over h. It gives you the exact slope of the curve at any single point.", 'layout': {'scale': 1.3}, 'audio_path': '/Users/claudioatlas/Desktop/Orbital/orbital_factory/jobs/short_what_is_a_derivative/audio/step_07.mp3', 'duration': 13.539}, {'step': 8, 'type': 'box', 'content': 'Derivative = slope of the tangent line = instantaneous rate of change', 'narration': 'The derivative is the slope of the tangent line. Another way to say it: the instantaneous rate of change. This is exactly how physics computes velocity from a position curve.', 'layout': {'scale': 1.0}, 'audio_path': '/Users/claudioatlas/Desktop/Orbital/orbital_factory/jobs/short_what_is_a_derivative/audio/step_08.mp3', 'duration': 14.793}, {'step': 9, 'type': 'box', 'content': 'Every derivative rule is just a shortcut for this limit.', 'narration': "That's all a derivative is. A slope at a single point. And every derivative rule you'll ever learn? Just a shortcut for computing this limit.", 'layout': {'scale': 1.2}, 'audio_path': '/Users/claudioatlas/Desktop/Orbital/orbital_factory/jobs/short_what_is_a_derivative/audio/step_09.mp3', 'duration': 11.728}]

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
                graph_cfg  = step.get("graph", step.get("diagram", {}))

                # If graph_cfg is empty but we have a "content" expression, build a default config
                if not graph_cfg.get("functions") and step.get("content"):
                    expr = step["content"]
                    graph_cfg = {
                        "x_range": [-3, 3, 1],
                        "y_range": [-2, 10, 2],
                        "functions": [{"expr": expr, "label": "f(x)"}],
                    }

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

            # ── CONTENT STEP ──
            duration   = step.get("duration", 2.0)
            audio_path = step.get("audio_path", "")
            stype      = step.get("type", "math")
            content    = step.get("content") or step.get("latex", "")
            label_txt  = step.get("label", "")
            layout     = step.get("layout", {})
            scale_override = layout.get("scale", 1.0) if layout else 1.0

            anim_time = max(1.2, duration * ANIMATION_RATIO)

            # ═══════════════════════════════════════════════════
            # STEP 1: BUILD MOBJECT (before audio starts)
            # ═══════════════════════════════════════════════════
            if stype == "box":
                # Use Text() for boxes to preserve spaces; MathTex strips whitespace
                inner = Text(content, color=WHITE, font_size=28).scale(scale_override)
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
                has_aligned = 'aligned' in content or 'begin{' in content
                if eq_count >= 2 and not has_aligned:
                    # Split at = signs, rebuild as aligned with & before each =
                    parts = content.split('=')
                    # First line: everything before first = , then &= rest
                    aligned_lines = [parts[0].strip() + ' &= ' + parts[1].strip()]
                    for p in parts[2:]:
                        aligned_lines.append('&= ' + p.strip())
                    aligned_content = r'\begin{aligned} ' + r' \\[8pt] '.join(aligned_lines) + r' \end{aligned}'
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
