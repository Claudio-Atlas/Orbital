"""
"Secant Lines" — Final voiced version
Render: cd orbital_factory && source venv/bin/activate && PATH="/Library/TeX/texbin:$PATH" manim render prototypes/secant_line_voiced.py SecantLineVoiced -o secant_voiced.mp4 --format mp4 -r 1080,1920 --frame_rate 60
"""
from manim import *
import numpy as np
import json

config.frame_width = 4.5
config.frame_height = 8.0

VIOLET = "#8B5CF6"
CYAN = "#22D3EE"
GREEN = "#39FF14"
ORANGE = "#F97316"
BOX_FILL = "#1a1130"
MATH_Y = 3.0

with open("jobs/short_secant_lines/manifest.json") as f:
    _manifest = json.load(f)
    MANIFEST = {}
    for s in _manifest:
        key = s["scene"]
        if isinstance(key, float) and key == int(key):
            key = int(key)
        MANIFEST[key] = s

def AUDIO(sc):
    return MANIFEST[sc]["audio_path"]

def DUR(sc):
    return MANIFEST[sc]["duration"]

class SecantLineVoiced(Scene):
    def construct(self):
        self.camera.background_color = BLACK

        border = Rectangle(width=4.35, height=7.85, color=VIOLET, stroke_width=2.5, stroke_opacity=0.7, fill_opacity=0)
        border_glow = Rectangle(width=4.40, height=7.90, color=VIOLET, stroke_width=6, stroke_opacity=0.15, fill_opacity=0)
        self.add(border_glow, border)

        fn = lambda x: x**2
        x1, x2 = 1, 3
        y1, y2 = fn(x1), fn(x2)

        # ═══ SCENE 1: Callback (5.4s) ═══
        axes = Axes(
            x_range=[-1, 4, 1], y_range=[-1, 10, 2],
            x_length=3.4, y_length=3.5,
            axis_config={"color": GREY_B, "include_numbers": True, "font_size": 12, "numbers_to_exclude": [0]},
            tips=False,
        )
        grid = NumberPlane(
            x_range=[-1, 4, 1], y_range=[-1, 10, 2],
            x_length=3.4, y_length=3.5,
            background_line_style={"stroke_color": VIOLET, "stroke_opacity": 0.2, "stroke_width": 0.8},
            faded_line_style={"stroke_color": CYAN, "stroke_opacity": 0.08, "stroke_width": 0.4},
        )
        grid.move_to(axes.get_center())
        curve = axes.plot(fn, x_range=[-0.5, 3.3], color=CYAN, stroke_width=3)
        fn_label = MathTex("f(x) = x^2", font_size=20, color=CYAN)
        fn_label.move_to(axes.c2p(0.2, 9.5))

        graph_group = VGroup(grid, axes, curve, fn_label)
        graph_group.move_to([0, -1.5, 0])

        callback = Text("How do we find\nthe slope?", font_size=30, color=WHITE, line_spacing=1.3)
        callback.move_to([0, 2.5, 0])

        self.add_sound(AUDIO(1))
        self.play(FadeIn(grid, axes), Create(curve), Write(fn_label), run_time=1.2)
        self.play(Write(callback), run_time=0.8)
        self.wait(DUR(1) - 2.0)
        self.play(FadeOut(callback), run_time=0.3)

        # ═══ SCENE 2: Pick two points (2.9s) ═══
        dot1 = Dot(axes.c2p(x1, y1), color=GREEN, radius=0.08)
        dot2 = Dot(axes.c2p(x2, y2), color=ORANGE, radius=0.08)

        pt1_label = MathTex("(1, 1)", font_size=18, color=GREEN)
        pt1_label.next_to(dot1, DL, buff=0.12)
        pt2_label = MathTex("(3, 9)", font_size=18, color=ORANGE)
        pt2_label.next_to(dot2, UR, buff=0.12)

        self.add_sound(AUDIO(2))
        self.play(FadeIn(dot1, scale=1.5), Write(pt1_label), run_time=0.5)
        self.play(Flash(dot1.get_center(), color=GREEN, num_lines=6), run_time=0.3)
        self.play(FadeIn(dot2, scale=1.5), Write(pt2_label), run_time=0.5)
        self.play(Flash(dot2.get_center(), color=ORANGE, num_lines=6), run_time=0.3)
        self.wait(max(0.1, DUR(2) - 1.6))

        # ═══ SCENE 3: Secant line (4.4s) ═══
        slope_val = (y2 - y1) / (x2 - x1)
        sec_line = Line(
            axes.c2p(x1 - 0.8, y1 - 0.8 * slope_val),
            axes.c2p(x2 + 0.5, y2 + 0.5 * slope_val),
            color=VIOLET, stroke_width=3
        )

        secant_label = Text("Secant Line", font_size=24, color=VIOLET, weight=BOLD)
        secant_label.move_to([0, MATH_Y, 0])

        self.add_sound(AUDIO(3))
        self.play(Create(sec_line), run_time=1.0)
        self.play(Write(secant_label), run_time=0.6)
        self.wait(DUR(3) - 1.6)
        self.play(FadeOut(secant_label), run_time=0.3)

        # ═══ SCENE 4: Rise/Run (6.0s) ═══
        run_line = DashedLine(
            axes.c2p(x1, y1), axes.c2p(x2, y1),
            color=CYAN, stroke_width=2, dash_length=0.08
        )
        rise_line = DashedLine(
            axes.c2p(x2, y1), axes.c2p(x2, y2),
            color=GREEN, stroke_width=2, dash_length=0.08
        )

        run_brace = Brace(run_line, DOWN, buff=0.05, color=CYAN)
        run_brace_label = Text("run = 2", font_size=16, color=CYAN)
        run_brace_label.next_to(run_brace, DOWN, buff=0.05)

        rise_brace = Brace(rise_line, RIGHT, buff=0.05, color=GREEN)
        rise_brace_label = Text("rise = 8", font_size=16, color=GREEN)
        rise_brace_label.next_to(rise_brace, RIGHT, buff=0.05)

        self.add_sound(AUDIO(4))
        self.play(Create(run_line), FadeIn(run_brace), Write(run_brace_label), run_time=0.8)
        self.wait(0.8)
        self.play(Create(rise_line), FadeIn(rise_brace), Write(rise_brace_label), run_time=0.8)
        self.wait(DUR(4) - 2.4)

        # ═══ SCENE 5: Specific formula (8.8s) ═══
        formula = MathTex(
            r"\text{slope}", r"=", r"\frac{f(3) - f(1)}{3 - 1}",
            r"=", r"\frac{9 - 1}{2}",
            r"=", r"4",
            font_size=28, color=WHITE
        )
        formula.move_to([0, MATH_Y, 0])
        formula[0].set_color(VIOLET)
        formula[6].set_color(GREEN)

        self.add_sound(AUDIO(5))
        self.play(Write(formula[0:3]), run_time=1.0)
        self.wait(1.5)
        self.play(Write(formula[3:5]), run_time=0.8)
        self.wait(1.2)
        self.play(Write(formula[5:7]), run_time=0.6)
        self.play(Circumscribe(formula[6], color=GREEN), run_time=0.6)
        self.wait(DUR(5) - 5.7)

        # Clean up rise/run and formula
        self.play(
            FadeOut(run_line), FadeOut(rise_line),
            FadeOut(run_brace), FadeOut(run_brace_label),
            FadeOut(rise_brace), FadeOut(rise_brace_label),
            FadeOut(formula),
            run_time=0.4
        )

        # ═══ SCENE 6: Relabel points (6.9s) ═══
        x_label = MathTex("x", font_size=22, color=GREEN)
        x_label.next_to(dot1, DL, buff=0.12)
        xh_label = MathTex("x + h", font_size=22, color=ORANGE)
        xh_label.next_to(dot2, UR, buff=0.12)

        self.add_sound(AUDIO(6))
        self.wait(0.8)  # "Now here's the powerful part"
        self.play(Transform(pt1_label, x_label), run_time=0.8)
        self.wait(0.5)
        self.play(Transform(pt2_label, xh_label), run_time=0.8)
        self.wait(DUR(6) - 2.9)

        # ═══ SCENE 6.5: Show h gap (8.4s) ═══
        h_line = Line(
            axes.c2p(x1, -0.3), axes.c2p(x2, -0.3),
            color=ORANGE, stroke_width=3
        )
        h_arrow_l = Line(axes.c2p(x1, -0.15), axes.c2p(x1, -0.45), color=ORANGE, stroke_width=2)
        h_arrow_r = Line(axes.c2p(x2, -0.15), axes.c2p(x2, -0.45), color=ORANGE, stroke_width=2)

        h_eq = MathTex(r"h = 3 - 1 = 2", font_size=20, color=ORANGE)
        h_eq.next_to(h_line, DOWN, buff=0.08)

        explain_h = Text("h = the gap between\nthe two x-values", font_size=18, color=WHITE, line_spacing=1.2)
        explain_h.move_to([0, MATH_Y, 0])

        self.add_sound(AUDIO(6.5))
        self.play(Create(h_line), Create(h_arrow_l), Create(h_arrow_r), run_time=0.6)
        self.play(Write(h_eq), run_time=0.8)
        self.play(Write(explain_h), run_time=0.6)
        self.wait(DUR(6.5) - 2.0)
        self.play(FadeOut(explain_h), run_time=0.3)

        # ═══ SCENE 7: Full denominator + cancel (12.7s) ═══
        rewrite_1 = MathTex(
            r"\frac{f(x+h) - f(x)}{(x+h) - x}",
            font_size=28, color=WHITE
        )
        rewrite_1.move_to([0, MATH_Y, 0])

        self.add_sound(AUDIO(7))
        self.play(Write(rewrite_1), run_time=1.5)
        self.wait(5.0)  # Let narration describe the formula

        # "Watch: x+h - x simplifies to just h"
        cancel_text = MathTex(r"(x+h) - x = h", font_size=24, color=ORANGE)
        cancel_text.move_to([0, MATH_Y - 0.7, 0])
        self.play(Write(cancel_text), run_time=0.8)
        self.wait(DUR(7) - 7.3)
        self.play(FadeOut(rewrite_1), FadeOut(cancel_text), run_time=0.3)

        # ═══ SCENE 7.5: Difference Quotient reveal (7.0s) ═══
        final_dq = MathTex(
            r"\frac{f(x+h) - f(x)}{h}",
            font_size=32, color=WHITE
        )
        final_dq.move_to([0, MATH_Y, 0])

        diff_quot_label = Text("The Difference Quotient", font_size=20, color=VIOLET, weight=BOLD)
        diff_quot_label.move_to([0, MATH_Y + 0.6, 0])

        self.add_sound(AUDIO(7.5))
        self.play(Write(final_dq), run_time=1.0)
        self.play(Write(diff_quot_label), run_time=0.5)
        self.play(Circumscribe(final_dq, color=VIOLET), run_time=0.8)
        self.wait(DUR(7.5) - 2.3)

        # Clean up
        self.play(
            FadeOut(diff_quot_label), FadeOut(final_dq),
            FadeOut(h_line), FadeOut(h_arrow_l), FadeOut(h_arrow_r), FadeOut(h_eq),
            run_time=0.4
        )

        # ═══ SCENE 8: Tease — h shrinks (10.9s) ═══
        tease_text = Text("Average rate of change ✓", font_size=22, color=GREEN)
        tease_text.move_to([0, MATH_Y, 0])

        self.add_sound(AUDIO(8))
        self.play(Write(tease_text), run_time=0.8)
        self.wait(1.5)

        h_tracker = ValueTracker(2.0)

        moving_dot = always_redraw(lambda: Dot(
            axes.c2p(x1 + h_tracker.get_value(), fn(x1 + h_tracker.get_value())),
            color=ORANGE, radius=0.08
        ))

        def _get_moving_secant():
            h = max(h_tracker.get_value(), 0.05)
            x_a = x1
            y_a = fn(x_a)
            x_b = x1 + h
            y_b = fn(x_b)
            s = (y_b - y_a) / h
            ext = 0.5
            return Line(
                axes.c2p(x_a - ext, y_a - ext * s),
                axes.c2p(x_b + ext, y_b + ext * s),
                color=VIOLET, stroke_width=3
            )

        moving_secant = always_redraw(_get_moving_secant)

        self.remove(dot2, pt2_label, sec_line)
        self.add(moving_dot, moving_secant)

        self.play(FadeOut(tease_text), run_time=0.3)

        tease_q = Text("What if h → 0?", font_size=28, color=GREEN, weight=BOLD)
        tease_q.move_to([0, MATH_Y, 0])

        self.play(h_tracker.animate.set_value(0.3), run_time=4.0, rate_func=smooth)
        self.play(Write(tease_q), run_time=0.5)
        self.wait(DUR(8) - 7.1)

        # ═══ CLEANUP & END CARD ═══
        self.play(
            FadeOut(tease_q), FadeOut(graph_group),
            FadeOut(dot1), FadeOut(pt1_label),
            FadeOut(moving_dot), FadeOut(moving_secant),
            run_time=0.5
        )

        _A, _B = 1.2, 0.95
        liss_glow = ParametricFunction(
            lambda t: np.array([_A*np.sin(2*t), _B*np.sin(3*t), 0]),
            t_range=[0, TAU, 0.02],
            color=VIOLET, stroke_width=8, stroke_opacity=0.2
        )
        liss_core = ParametricFunction(
            lambda t: np.array([_A*np.sin(2*t), _B*np.sin(3*t), 0]),
            t_range=[0, TAU, 0.02],
            color=VIOLET, stroke_width=2, stroke_opacity=1.0
        )
        logo = VGroup(liss_glow, liss_core).move_to([0, 0.5, 0])
        wordmark = Text("ORBITAL", font_size=22, color=VIOLET, weight=BOLD)
        wordmark.next_to(logo, DOWN, buff=0.3)

        self.play(Create(liss_core, run_time=0.8), FadeIn(liss_glow, run_time=0.6))
        self.play(FadeIn(wordmark, shift=UP*0.2), run_time=0.4)
        self.wait(1.5)
        self.play(FadeOut(VGroup(logo, wordmark)), run_time=0.3)
