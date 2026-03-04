"""
"What is a Derivative?" — Final voiced version
Render: cd orbital_factory && source venv/bin/activate && PATH="/Library/TeX/texbin:$PATH" manim render prototypes/derivative_concept_voiced.py DerivativeConceptVoiced -o deriv_voiced.mp4 --format mp4 -r 1080,1920 --frame_rate 60
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

# Load audio durations
with open("jobs/short_what_is_a_derivative_v2/manifest.json") as f:
    MANIFEST = {s["scene"]: s for s in json.load(f)}

AUDIO = lambda sc: MANIFEST[sc]["audio_path"]
DUR = lambda sc: MANIFEST[sc]["duration"]

class DerivativeConceptVoiced(Scene):
    def construct(self):
        self.camera.background_color = BLACK

        # Neon border
        border = Rectangle(width=4.35, height=7.85, color=VIOLET, stroke_width=2.5, stroke_opacity=0.7, fill_opacity=0)
        border_glow = Rectangle(width=4.40, height=7.90, color=VIOLET, stroke_width=6, stroke_opacity=0.15, fill_opacity=0)
        self.add(border_glow, border)

        # ═══ SCENE 1: Hook (4.7s) ═══
        hook = Text("Every curve has a\nhidden slope", font_size=38, color=WHITE, line_spacing=1.3)
        hook.move_to([0, 2.5, 0])
        self.add_sound(AUDIO(1))
        self.play(Write(hook), run_time=1.5)
        self.wait(DUR(1) - 1.5)
        self.play(FadeOut(hook, shift=UP * 0.3), run_time=0.4)

        # ═══ SCENE 2: Build graph (8.0s) ═══
        axes = Axes(
            x_range=[-3, 3, 1], y_range=[-1, 9, 2],
            x_length=3.4, y_length=3.5,
            axis_config={"color": GREY_B, "include_numbers": True, "font_size": 12, "numbers_to_exclude": [0]},
            tips=False,
        )
        grid = NumberPlane(
            x_range=[-3, 3, 1], y_range=[-1, 9, 2],
            x_length=3.4, y_length=3.5,
            background_line_style={"stroke_color": VIOLET, "stroke_opacity": 0.2, "stroke_width": 0.8},
            faded_line_style={"stroke_color": CYAN, "stroke_opacity": 0.08, "stroke_width": 0.4},
        )
        grid.move_to(axes.get_center())

        fn = lambda x: x**2
        curve = axes.plot(fn, x_range=[-2.8, 2.8], color=CYAN, stroke_width=3)
        label = MathTex("f(x) = x^2", font_size=20, color=CYAN)
        label.move_to(axes.c2p(-2.2, 8.0))

        graph_group = VGroup(grid, axes, curve, label)
        graph_group.move_to([0, -1.5, 0])

        self.add_sound(AUDIO(2))
        self.play(FadeIn(grid, axes), run_time=0.8)
        self.play(Create(curve), Write(label), run_time=1.5)
        self.wait(DUR(2) - 2.3)

        # ═══ SCENE 3: Animated dot sweep (9.0s) ═══
        t = ValueTracker(-2.5)

        dot = always_redraw(lambda: Dot(
            axes.c2p(t.get_value(), fn(t.get_value())),
            color=GREEN, radius=0.07
        ))

        def get_tangent():
            x0 = t.get_value()
            dx = 0.001
            slope = (fn(x0 + dx) - fn(x0 - dx)) / (2 * dx)
            y0 = fn(x0)
            half = 1.2
            return Line(
                axes.c2p(x0 - half, y0 - slope * half),
                axes.c2p(x0 + half, y0 + slope * half),
                color=GREEN, stroke_width=2.5
            )

        tangent = always_redraw(get_tangent)

        slope_label = always_redraw(lambda: Text(
            f"slope = {2 * t.get_value():.1f}",
            font_size=22, color=GREEN
        ).move_to([0, 2.0, 0]))

        self.add_sound(AUDIO(3))
        self.play(FadeIn(dot), Create(tangent), Write(slope_label), run_time=0.8)
        self.play(t.animate.set_value(2.5), run_time=DUR(3) - 1.5, rate_func=smooth)
        self.wait(0.7)

        # ═══ SCENE 4: Pause at x=0 (4.3s) ═══
        self.add_sound(AUDIO(4))
        self.play(t.animate.set_value(0), run_time=1.5, rate_func=smooth)
        flat_label = Text("slope = 0", font_size=24, color=WHITE, weight=BOLD)
        flat_label.move_to([0, 2.8, 0])
        self.play(Write(flat_label), run_time=0.5)
        self.play(Flash(dot.get_center(), color=GREEN, num_lines=8), run_time=0.5)
        self.wait(DUR(4) - 2.5)
        self.play(FadeOut(flat_label), run_time=0.3)

        # ═══ SCENE 5: Move to x=2 (6.9s) ═══
        self.add_sound(AUDIO(5))
        self.play(t.animate.set_value(2), run_time=2.0, rate_func=smooth)
        steep_label = Text("slope = 4", font_size=24, color=WHITE, weight=BOLD)
        steep_label.move_to([0, 2.8, 0])
        self.play(Write(steep_label), run_time=0.5)
        self.play(Flash(dot.get_center(), color=GREEN, num_lines=8), run_time=0.5)
        self.wait(DUR(5) - 3.0)
        self.play(FadeOut(steep_label), run_time=0.3)

        # ═══ SCENE 6: The question (5.0s) ═══
        self.play(FadeOut(slope_label), run_time=0.2)

        question = Text("How do we find the\nexact slope at any point?", font_size=28, color=WHITE, line_spacing=1.3)
        question.move_to([0, 2.2, 0])
        box = SurroundingRectangle(question, color=VIOLET, fill_color=BOX_FILL, fill_opacity=0.6, buff=0.2, corner_radius=0.1, stroke_width=2)
        
        self.add_sound(AUDIO(6))
        self.play(FadeIn(box), Write(question), run_time=1.0)
        self.wait(DUR(6) - 1.0)

        # ═══ SCENE 7: "That's the derivative" (5.9s) ═══
        self.play(FadeOut(question), FadeOut(box), run_time=0.3)

        answer = Text("That's the derivative.", font_size=34, color=GREEN, weight=BOLD)
        answer.move_to([0, 2.2, 0])
        self.add_sound(AUDIO(7))
        self.play(Write(answer), run_time=1.0)
        self.play(Circumscribe(answer, color=GREEN, run_time=1.0))
        self.wait(DUR(7) - 2.0)

        # ═══ SCENE 8: Applications (14.5s) ═══
        self.play(
            FadeOut(answer), FadeOut(dot), FadeOut(tangent), FadeOut(graph_group),
            run_time=0.5
        )

        apps_title = Text("Derivatives are everywhere", font_size=28, color=WHITE, weight=BOLD)
        apps_title.move_to([0, 3.2, 0])

        # Mini position-vs-time graph
        app_axes = Axes(
            x_range=[0, 5, 1], y_range=[0, 6, 2],
            x_length=2.8, y_length=2.0,
            axis_config={"color": GREY_C, "font_size": 10, "include_numbers": False},
            tips=False,
        )
        app_axes.move_to([-0.8, 0.8, 0])
        pos_curve = app_axes.plot(lambda x: 0.2 * x**2 + 0.5, x_range=[0, 4.5], color=CYAN, stroke_width=2)
        x_lab = Text("time", font_size=12, color=GREY_C).next_to(app_axes, DOWN, buff=0.05)
        y_lab = Text("position", font_size=12, color=GREY_C).next_to(app_axes, LEFT, buff=0.05).rotate(PI/2)
        vel_label = Text("Slope = velocity", font_size=18, color=GREEN)
        vel_label.move_to([0, -0.6, 0])

        vt = ValueTracker(0.5)
        vel_dot = always_redraw(lambda: Dot(
            app_axes.c2p(vt.get_value(), 0.2 * vt.get_value()**2 + 0.5),
            color=GREEN, radius=0.06
        ))
        def get_vel_tangent():
            x0 = vt.get_value()
            slope = 0.4 * x0
            y0 = 0.2 * x0**2 + 0.5
            half = 0.8
            return Line(
                app_axes.c2p(x0 - half, y0 - slope * half),
                app_axes.c2p(x0 + half, y0 + slope * half),
                color=GREEN, stroke_width=2
            )
        vel_tangent = always_redraw(get_vel_tangent)

        self.add_sound(AUDIO(8))
        self.play(Write(apps_title), run_time=0.6)
        self.play(FadeIn(app_axes, x_lab, y_lab), Create(pos_curve), run_time=0.8)
        self.add(vel_dot, vel_tangent)
        self.play(Write(vel_label), run_time=0.4)
        self.play(vt.animate.set_value(4.0), run_time=3.0, rate_func=smooth)

        # Application list
        growth = Text("📈  Tumor growth rate", font_size=18, color=ORANGE)
        growth.move_to([0, -1.5, 0])
        econ = Text("💰  Marginal cost", font_size=18, color=VIOLET)
        econ.move_to([0, -2.1, 0])
        physics = Text("🚀  Acceleration", font_size=18, color=CYAN)
        physics.move_to([0, -2.7, 0])

        self.play(Write(growth), run_time=0.5)
        self.wait(0.8)
        self.play(Write(econ), run_time=0.5)
        self.wait(0.8)
        self.play(Write(physics), run_time=0.5)
        self.wait(DUR(8) - 8.4)

        self.play(
            FadeOut(apps_title), FadeOut(app_axes), FadeOut(pos_curve),
            FadeOut(x_lab), FadeOut(y_lab), FadeOut(vel_label),
            FadeOut(vel_dot), FadeOut(vel_tangent),
            FadeOut(growth), FadeOut(econ), FadeOut(physics),
            run_time=0.5
        )

        # ═══ SCENE 9: End card (5.1s) ═══
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

        self.add_sound(AUDIO(9))
        self.play(Create(liss_core, run_time=0.8), FadeIn(liss_glow, run_time=0.6))
        self.play(FadeIn(wordmark, shift=UP*0.2), run_time=0.4)
        self.wait(DUR(9) - 1.2)
        self.play(FadeOut(VGroup(logo, wordmark)), run_time=0.3)
