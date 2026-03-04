"""
"The Definition of the Derivative" — Final voiced version (Video C)
Render: cd orbital_factory && source venv/bin/activate && PATH="/Library/TeX/texbin:$PATH" manim render prototypes/definition_derivative_voiced.py DefinitionDerivativeVoiced -o defn_voiced.mp4 --format mp4 -r 1080,1920 --frame_rate 60
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

with open("jobs/short_definition_derivative/manifest.json") as f:
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

class DefinitionDerivativeVoiced(Scene):
    def construct(self):
        self.camera.background_color = BLACK

        border = Rectangle(width=4.35, height=7.85, color=VIOLET, stroke_width=2.5, stroke_opacity=0.7, fill_opacity=0)
        border_glow = Rectangle(width=4.40, height=7.90, color=VIOLET, stroke_width=6, stroke_opacity=0.15, fill_opacity=0)
        self.add(border_glow, border)

        fn = lambda x: x**2
        x_fixed = 1

        # ═══ SCENE 1: Callback — secant shrinks (5.3s) ═══
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

        self.play(FadeIn(grid, axes), Create(curve), Write(fn_label), run_time=0.8)

        fixed_dot = Dot(axes.c2p(x_fixed, fn(x_fixed)), color=GREEN, radius=0.08)
        self.play(FadeIn(fixed_dot), run_time=0.2)

        h_tracker = ValueTracker(2.0)
        moving_dot = always_redraw(lambda: Dot(
            axes.c2p(x_fixed + h_tracker.get_value(), fn(x_fixed + h_tracker.get_value())),
            color=ORANGE, radius=0.08
        ))
        def _get_secant():
            h = max(h_tracker.get_value(), 0.01)
            ya, yb = fn(x_fixed), fn(x_fixed + h)
            s = (yb - ya) / h
            ext = 0.8
            return Line(axes.c2p(x_fixed-ext, ya-ext*s), axes.c2p(x_fixed+h+ext, yb+ext*s), color=VIOLET, stroke_width=3)
        secant = always_redraw(_get_secant)

        h_label = always_redraw(lambda: Text(
            f"h = {h_tracker.get_value():.1f}", font_size=20, color=ORANGE
        ).move_to([0, MATH_Y - 0.5, 0]))

        callback_text = Text("What happens as h → 0?", font_size=24, color=WHITE)
        callback_text.move_to([0, MATH_Y, 0])

        self.add_sound(AUDIO(1))
        self.play(Write(callback_text), run_time=0.5)
        self.add(moving_dot, secant, h_label)
        self.play(h_tracker.animate.set_value(0.1), run_time=DUR(1) - 0.5, rate_func=smooth)

        # ═══ SCENE 1.5: Flash — tangent (4.0s) ═══
        tangent_text = Text("Secant → Tangent!", font_size=22, color=GREEN, weight=BOLD)
        tangent_text.move_to([0, MATH_Y + 0.5, 0])

        self.add_sound(AUDIO(1.5))
        self.play(
            FadeOut(callback_text),
            Flash(fixed_dot.get_center(), color=GREEN, num_lines=12),
            Write(tangent_text),
            run_time=0.6
        )
        self.wait(DUR(1.5) - 0.6)
        self.play(FadeOut(tangent_text), FadeOut(h_label), FadeOut(moving_dot), FadeOut(secant), run_time=0.3)

        # ═══ SCENE 2: Write the definition (12.6s) ═══
        slope_at_1 = 2 * x_fixed
        tangent_line = Line(
            axes.c2p(x_fixed-1.2, fn(x_fixed)-1.2*slope_at_1),
            axes.c2p(x_fixed+1.2, fn(x_fixed)+1.2*slope_at_1),
            color=GREEN, stroke_width=2.5
        )
        self.play(Create(tangent_line), run_time=0.4)

        defn_title = Text("The Definition of the Derivative", font_size=18, color=VIOLET, weight=BOLD)
        defn_title.move_to([0, MATH_Y + 0.5, 0])
        defn = MathTex(r"f'(x) = \lim_{h \to 0} \frac{f(x+h) - f(x)}{h}", font_size=26, color=WHITE)
        defn.move_to([0, MATH_Y, 0])

        self.add_sound(AUDIO(2))
        self.play(Write(defn_title), run_time=0.5)
        self.play(Write(defn), run_time=3.0)
        self.play(Circumscribe(defn, color=VIOLET), run_time=0.8)
        self.wait(DUR(2) - 4.3)

        # ═══ SCENE 3: Prove it (4.4s) ═══
        self.play(FadeOut(defn_title), FadeOut(defn), FadeOut(tangent_line), run_time=0.3)

        prove_title = Text("Let's prove it with x²", font_size=22, color=WHITE)
        prove_title.move_to([0, MATH_Y + 0.5, 0])
        self.add_sound(AUDIO(3))
        self.play(Write(prove_title), run_time=0.5)
        self.wait(DUR(3) - 0.8)
        self.play(FadeOut(prove_title), run_time=0.3)

        # ═══ SCENE 3.1: Plug in (8.5s) ═══
        step1 = MathTex(r"f'(x) = \lim_{h \to 0} \frac{(x+h)^2 - x^2}{h}", font_size=24, color=WHITE)
        step1.move_to([0, MATH_Y, 0])
        self.add_sound(AUDIO(3.1))
        self.play(Write(step1), run_time=1.5)
        self.wait(DUR(3.1) - 1.5)

        # ═══ SCENE 3.2: FOIL expansion (19.5s) ═══
        self.add_sound(AUDIO(3.2))

        foil_title = Text("Expand (x + h)²", font_size=18, color=ORANGE)
        foil_title.move_to([0, MATH_Y - 0.5, 0])
        self.play(Write(foil_title), run_time=0.4)

        foil_1 = MathTex(r"(x+h)^2 = (x+h)(x+h)", font_size=22, color=WHITE)
        foil_1.move_to([0, MATH_Y - 0.9, 0])
        self.play(Write(foil_1), run_time=0.8)
        self.wait(1.5)

        foil_2 = MathTex(
            r"= x \cdot x", r"+ x \cdot h", r"+ h \cdot x", r"+ h \cdot h",
            font_size=22, color=WHITE
        )
        foil_2.move_to([0, MATH_Y - 1.4, 0])
        foil_2[0].set_color(CYAN)
        foil_2[1].set_color(VIOLET)
        foil_2[2].set_color(VIOLET)
        foil_2[3].set_color(ORANGE)

        self.play(Write(foil_2[0]), run_time=0.4)
        self.wait(0.8)
        self.play(Write(foil_2[1]), run_time=0.4)
        self.wait(0.8)
        self.play(Write(foil_2[2]), run_time=0.4)
        self.wait(0.8)
        self.play(Write(foil_2[3]), run_time=0.4)
        self.wait(1.2)

        foil_3 = MathTex(r"= x^2 + 2xh + h^2", font_size=24, color=GREEN)
        foil_3.move_to([0, MATH_Y - 1.9, 0])
        self.play(Write(foil_3), run_time=0.8)
        self.play(Circumscribe(foil_3, color=GREEN), run_time=0.5)
        self.wait(DUR(3.2) - 9.9)

        self.play(FadeOut(foil_title), FadeOut(foil_1), FadeOut(foil_2), FadeOut(foil_3), run_time=0.3)

        # ═══ SCENE 3.3: Substitute + cancel x² (7.7s) ═══
        step2 = MathTex(
            r"= \lim_{h \to 0} \frac{x^2 + 2xh + h^2 - x^2}{h}",
            font_size=24, color=WHITE
        )
        step2.move_to([0, MATH_Y - 0.6, 0])

        self.add_sound(AUDIO(3.3))
        self.play(Write(step2), run_time=1.0)
        self.wait(1.0)

        cancel_note = Text("x² cancels!", font_size=16, color=ORANGE)
        cancel_note.move_to([1.5, MATH_Y - 0.3, 0])
        self.play(Write(cancel_note), run_time=0.3)

        step3 = MathTex(r"= \lim_{h \to 0} \frac{2xh + h^2}{h}", font_size=24, color=WHITE)
        step3.move_to([0, MATH_Y - 1.2, 0])
        self.play(Write(step3), run_time=0.8)
        self.wait(DUR(3.3) - 3.1)
        self.play(FadeOut(cancel_note), run_time=0.2)

        # Scroll up
        self.play(FadeOut(step1), FadeOut(step2), run_time=0.3)
        step3.generate_target()
        step3.target.move_to([0, MATH_Y, 0])
        self.play(MoveToTarget(step3), run_time=0.4)

        # ═══ SCENE 3.4: Factor + cancel h (2.9s) ═══
        step4 = MathTex(r"= \lim_{h \to 0} \frac{h(2x + h)}{h}", font_size=24, color=WHITE)
        step4.move_to([0, MATH_Y - 0.6, 0])

        self.add_sound(AUDIO(3.4))
        self.play(Write(step4), run_time=0.5)

        cancel_h = Text("h cancels!", font_size=16, color=ORANGE)
        cancel_h.move_to([1.5, MATH_Y - 0.3, 0])

        step5 = MathTex(r"= \lim_{h \to 0} (2x + h)", font_size=24, color=WHITE)
        step5.move_to([0, MATH_Y - 1.2, 0])

        self.play(Write(cancel_h), run_time=0.2)
        self.play(Write(step5), run_time=0.5)
        self.wait(max(0.1, DUR(3.4) - 1.2))
        self.play(FadeOut(cancel_h), run_time=0.2)

        # Scroll up
        self.play(FadeOut(step3), FadeOut(step4), run_time=0.3)
        step5.generate_target()
        step5.target.move_to([0, MATH_Y, 0])
        self.play(MoveToTarget(step5), run_time=0.4)

        # ═══ SCENE 3.5: Take the limit (4.4s) ═══
        step6 = MathTex(r"= 2x", font_size=32, color=GREEN)
        step6.move_to([0, MATH_Y - 0.6, 0])

        self.add_sound(AUDIO(3.5))
        self.play(Write(step6), run_time=0.6)
        self.play(Circumscribe(step6, color=GREEN), run_time=0.8)
        self.wait(0.5)

        self.play(FadeOut(step5), run_time=0.2)
        result = MathTex(r"f'(x) = 2x", font_size=34, color=GREEN)
        result.move_to([0, MATH_Y, 0])
        self.play(ReplacementTransform(step6, result), run_time=0.5)
        self.wait(max(0.1, DUR(3.5) - 2.6))

        # ═══ SCENE 4: Callback payoff (13.7s) ═══
        payoff_title = Text("Let's check!", font_size=22, color=WHITE, weight=BOLD)
        payoff_title.move_to([0, MATH_Y + 0.5, 0])

        self.add_sound(AUDIO(4))
        self.play(Write(payoff_title), run_time=0.4)

        check0 = MathTex(r"f'(0) = 2(0) = 0", font_size=22, color=WHITE)
        check0.move_to([0, MATH_Y - 0.5, 0])
        recall0 = Text("Flat at the bottom! ✓", font_size=18, color=GREEN)
        recall0.move_to([0, MATH_Y - 0.9, 0])
        dot_0 = Dot(axes.c2p(0, fn(0)), color=GREEN, radius=0.08)

        self.play(Write(check0), FadeIn(dot_0), run_time=0.6)
        self.play(Flash(dot_0.get_center(), color=GREEN, num_lines=8), Write(recall0), run_time=0.5)
        self.wait(3.0)

        check2 = MathTex(r"f'(2) = 2(2) = 4", font_size=22, color=WHITE)
        check2.move_to([0, MATH_Y - 1.5, 0])
        recall2 = Text("Slope was 4! ✓", font_size=18, color=GREEN)
        recall2.move_to([0, MATH_Y - 1.9, 0])
        dot_2 = Dot(axes.c2p(2, fn(2)), color=GREEN, radius=0.08)

        self.play(Write(check2), FadeIn(dot_2), run_time=0.6)
        self.play(Flash(dot_2.get_center(), color=GREEN, num_lines=8), Write(recall2), run_time=0.5)
        self.wait(DUR(4) - 5.6)

        # ═══ SCENE 5: Congrats (4.0s) ═══
        self.play(
            FadeOut(payoff_title), FadeOut(check0), FadeOut(recall0),
            FadeOut(check2), FadeOut(recall2), FadeOut(result),
            FadeOut(dot_0), FadeOut(dot_2), FadeOut(fixed_dot),
            FadeOut(graph_group),
            run_time=0.5
        )

        congrats = Text("You just computed\nyour first derivative.", font_size=28, color=WHITE, weight=BOLD, line_spacing=1.3)
        congrats.move_to([0, 1.0, 0])
        formula_final = MathTex(r"f(x) = x^2 \implies f'(x) = 2x", font_size=26, color=GREEN)
        formula_final.move_to([0, -0.2, 0])

        self.add_sound(AUDIO(5))
        self.play(Write(congrats), run_time=0.8)
        self.play(Write(formula_final), run_time=0.6)
        self.play(Circumscribe(formula_final, color=GREEN), run_time=0.6)
        self.wait(DUR(5) - 2.0)

        self.play(FadeOut(congrats), FadeOut(formula_final), run_time=0.4)

        # ═══ END CARD ═══
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
