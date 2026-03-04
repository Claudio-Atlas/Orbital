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
    STEPS_DATA = [{'type': 'box', 'content': '\\text{What is the derivative of } 5 \\text{ ?}', 'narration': "Quick question — what's the derivative of just the number 5?", 'mode': 'replace', 'label': '', 'step': 0, 'audio_path': '/Users/claudioatlas/Desktop/Orbital/orbital_factory/jobs/short_the_constant_rule/audio/step_00.mp3', 'duration': 5.133}, {'type': 'graph', 'content': '', 'narration': "Let's graph it. y equals 5 is a perfectly flat horizontal line.", 'mode': 'replace', 'persistent': True, 'diagram': {'kind': 'function_plot', 'x_range': [-5, 5, 1], 'y_range': [-2, 8, 1], 'functions': [{'expr': 'lambda x: 5', 'color': '#22D3EE', 'label': 'y = 5'}]}, 'step': 1, 'audio_path': '/Users/claudioatlas/Desktop/Orbital/orbital_factory/jobs/short_the_constant_rule/audio/step_01.mp3', 'duration': 5.969}, {'type': 'box', 'content': '\\text{No slope. It never goes up or down.}', 'narration': 'No matter where you look, this line never rises or falls. Zero slope, everywhere.', 'mode': 'replace', 'label': '', 'step': 2, 'audio_path': '/Users/claudioatlas/Desktop/Orbital/orbital_factory/jobs/short_the_constant_rule/audio/step_02.mp3', 'duration': 7.502}, {'type': 'box', 'label': 'The Constant Rule', 'content': '\\frac{d}{dx}[c] = 0', 'narration': 'The Constant Rule — the derivative of any constant is always zero.', 'mode': 'replace', 'step': 3, 'audio_path': '/Users/claudioatlas/Desktop/Orbital/orbital_factory/jobs/short_the_constant_rule/audio/step_03.mp3', 'duration': 6.619}, {'type': 'math', 'content': '\\begin{aligned} \\frac{d}{dx}[7] &= 0 \\\\[6pt] \\frac{d}{dx}[\\pi] &= 0 \\end{aligned}', 'narration': "Seven, pi — doesn't matter what the constant is. The derivative is always zero.", 'mode': 'replace', 'step': 4, 'audio_path': '/Users/claudioatlas/Desktop/Orbital/orbital_factory/jobs/short_the_constant_rule/audio/step_04.mp3', 'duration': 7.827}, {'type': 'math', 'content': '\\frac{d}{dx}[5x] = 5 \\quad \\text{vs} \\quad \\frac{d}{dx}[5] = 0', 'narration': "Don't confuse 5x with 5. Five-x has a variable — its derivative is 5, not zero.", 'mode': 'replace', 'step': 5, 'audio_path': '/Users/claudioatlas/Desktop/Orbital/orbital_factory/jobs/short_the_constant_rule/audio/step_05.mp3', 'duration': 8.847999999999999}, {'type': 'box', 'content': '\\text{Next: The Power Rule}', 'narration': "Next up — the Power Rule. That's where things get interesting.", 'mode': 'replace', 'label': 'ORBITAL', 'step': 6, 'audio_path': '/Users/claudioatlas/Desktop/Orbital/orbital_factory/jobs/short_the_constant_rule/audio/step_06.mp3', 'duration': 5.783}]

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

            anim_time = max(1.2, duration * ANIMATION_RATIO)

            # ═══════════════════════════════════════════════════
            # STEP 1: BUILD MOBJECT (before audio starts)
            # ═══════════════════════════════════════════════════
            if stype == "box":
                inner = MathTex(content, color=WHITE).scale(BOX_SCALE)
                _clamp(inner, MAX_WIDTH * 0.75)
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
                mob = MathTex(content, color=WHITE).scale(MATH_SCALE)
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
                self.play(FadeOut(previous, shift=UP * 0.3), run_time=0.4)
                self.play(Write(mob), run_time=anim_time)

            # ═══════════════════════════════════════════════════
            # STEP 4: HOLD (voice finishes during this)
            # ═══════════════════════════════════════════════════
            remaining = max(0.3, duration - anim_time - (0.4 if previous else 0))
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

        # ── Orbital logo end card ──
        # Planet
        planet_core = Circle(radius=0.45, color=WHITE, stroke_width=7)
        planet_glow = Circle(radius=0.52, color="#8B5CF6", stroke_width=12, stroke_opacity=0.15)
        for r_off, op, w in [(0.03, 0.5, 5), (0.06, 0.25, 3), (0.09, 0.12, 2)]:
            planet_core.add(Circle(radius=0.45+r_off, color=WHITE, stroke_width=w, stroke_opacity=op))
        
        # Orbit rings
        orbit_ring = Ellipse(width=1.7, height=0.55, color=WHITE, stroke_width=2)
        orbit_ring.rotate(-30 * DEGREES)
        orbit_glow = Ellipse(width=1.75, height=0.57, color="#8B5CF6", stroke_width=8, stroke_opacity=0.15)
        orbit_glow.rotate(-30 * DEGREES)
        orbit_inner = Ellipse(width=1.55, height=0.48, color="#22D3EE", stroke_width=1.5, stroke_opacity=0.85)
        orbit_inner.rotate(-30 * DEGREES)
        
        # Satellite dot
        angle = 50 * DEGREES
        sat_x = 0.85 * np.cos(angle) * np.cos(-30*DEGREES) - 0.28 * np.sin(angle) * np.sin(-30*DEGREES)
        sat_y = 0.85 * np.cos(angle) * np.sin(-30*DEGREES) + 0.28 * np.sin(angle) * np.cos(-30*DEGREES)
        sat_glow = Dot([sat_x, sat_y, 0], radius=0.15, color="#22D3EE", fill_opacity=0.25)
        sat_core = Dot([sat_x, sat_y, 0], radius=0.05, color=WHITE, fill_opacity=1.0)
        
        logo = VGroup(planet_glow, planet_core, orbit_glow, orbit_ring, orbit_inner, sat_glow, sat_core)
        logo.move_to([0, 0.6, 0])
        
        # Wordmark
        wordmark = Text("ORBITAL", font_size=24, color=WHITE, weight=BOLD)
        wordmark.next_to(logo, DOWN, buff=0.35)
        wm_glow = wordmark.copy().set_color("#8B5CF6").set_opacity(0.4).scale(1.08)
        wm_glow.set_stroke(color="#8B5CF6", width=6, opacity=0.2)
        
        end_card = VGroup(logo, wm_glow, wordmark)
        end_card.move_to([0, 0, 0])
        
        self.play(FadeIn(logo, scale=0.7), run_time=0.6)
        self.play(FadeIn(VGroup(wm_glow, wordmark), shift=UP*0.2), run_time=0.4)
        self.wait(1.5)
        self.play(FadeOut(end_card), run_time=0.3)
