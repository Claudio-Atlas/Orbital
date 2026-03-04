"""
Prototype: "What is a Derivative?" — Visual Experiments
=======================================================
Testing 3B1B-style animations for the conceptual derivative intro.
Render: cd orbital_factory && source venv/bin/activate && PATH="/Library/TeX/texbin:$PATH" manim render prototypes/derivative_concept.py DerivativeConcept -o deriv_proto.mp4 --format mp4 -r 1080,1920 --frame_rate 60
"""
from manim import *
import numpy as np

config.frame_width = 4.5
config.frame_height = 8.0

VIOLET = "#8B5CF6"
CYAN = "#22D3EE"
GREEN = "#39FF14"
ORANGE = "#F97316"
BOX_FILL = "#1a1130"

class DerivativeConcept(Scene):
    def construct(self):
        self.camera.background_color = BLACK

        # ── Neon border ──
        border = Rectangle(
            width=4.35, height=7.85,
            color=VIOLET, stroke_width=2.5, stroke_opacity=0.7,
            fill_opacity=0,
        )
        border_glow = Rectangle(
            width=4.40, height=7.90,
            color=VIOLET, stroke_width=6, stroke_opacity=0.15,
            fill_opacity=0,
        )
        self.add(border_glow, border)

        # ════════════════════════════════════════════
        # SCENE 1: Hook — "Every curve has a speed"
        # ════════════════════════════════════════════
        hook = Text("Every curve has a\nhidden speed", font_size=38, color=WHITE, line_spacing=1.3)
        hook.move_to([0, 2.5, 0])
        self.play(Write(hook), run_time=1.5)
        self.wait(2.0)
        self.play(FadeOut(hook, shift=UP * 0.3), run_time=0.4)

        # ════════════════════════════════════════════
        # SCENE 2: Build the graph
        # ════════════════════════════════════════════
        axes = Axes(
            x_range=[-3, 3, 1],
            y_range=[-1, 9, 2],
            x_length=3.4,
            y_length=3.5,
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

        self.play(FadeIn(grid, axes), run_time=0.6)
        self.play(Create(curve), Write(label), run_time=1.5)
        self.wait(1.0)

        # ════════════════════════════════════════════
        # SCENE 3: Animated dot with tangent line
        # ════════════════════════════════════════════
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

        # Slope label that updates
        slope_label = always_redraw(lambda: Text(
            f"slope = {2 * t.get_value():.1f}",
            font_size=22, color=GREEN
        ).move_to([0, 2.0, 0]))

        self.play(FadeIn(dot), Create(tangent), Write(slope_label), run_time=0.8)

        # Slow sweep across the curve
        self.play(t.animate.set_value(2.5), run_time=6.0, rate_func=smooth)
        self.wait(1.0)

        # ════════════════════════════════════════════
        # SCENE 4: Pause at flat point (x=0)
        # ════════════════════════════════════════════
        self.play(t.animate.set_value(0), run_time=2.0, rate_func=smooth)

        flat_label = Text("Flat here → slope = 0", font_size=20, color=WHITE)
        flat_label.move_to([0, 2.8, 0])
        self.play(Write(flat_label), run_time=0.6)
        self.play(Flash(dot.get_center(), color=GREEN, num_lines=8), run_time=0.5)
        self.wait(1.5)
        self.play(FadeOut(flat_label), run_time=0.3)

        # ════════════════════════════════════════════
        # SCENE 5: Move to steep point (x=2)
        # ════════════════════════════════════════════
        self.play(t.animate.set_value(2), run_time=2.0, rate_func=smooth)

        steep_label = Text("Steep here → slope = 4", font_size=20, color=WHITE)
        steep_label.move_to([0, 2.8, 0])
        self.play(Write(steep_label), run_time=0.6)
        self.play(Flash(dot.get_center(), color=GREEN, num_lines=8), run_time=0.5)
        self.wait(1.5)
        self.play(FadeOut(steep_label), run_time=0.3)

        # ════════════════════════════════════════════
        # SCENE 6: The question
        # ════════════════════════════════════════════
        self.play(FadeOut(slope_label), run_time=0.3)

        question = Text("How do we find the\nexact slope at any point?", font_size=28, color=WHITE, line_spacing=1.3)
        question.move_to([0, 2.2, 0])
        box = SurroundingRectangle(question, color=VIOLET, fill_color=BOX_FILL, fill_opacity=0.6, buff=0.2, corner_radius=0.1, stroke_width=2)
        self.play(FadeIn(box), Write(question), run_time=1.0)
        self.wait(2.0)

        # ════════════════════════════════════════════
        # SCENE 7: "That's the derivative"
        # ════════════════════════════════════════════
        self.play(FadeOut(question), FadeOut(box), run_time=0.3)

        answer = Text("That's the derivative.", font_size=34, color=GREEN, weight=BOLD)
        answer.move_to([0, 2.2, 0])
        self.play(Write(answer), run_time=1.0)
        self.play(Circumscribe(answer, color=GREEN, run_time=1.0))
        self.wait(2.0)

        # ════════════════════════════════════════════
        # SCENE 8: Applications — "It's everywhere"
        # ════════════════════════════════════════════
        self.play(
            FadeOut(answer),
            FadeOut(dot),
            FadeOut(tangent),
            FadeOut(graph_group),
            run_time=0.5
        )

        apps_title = Text("Derivatives are everywhere", font_size=28, color=WHITE, weight=BOLD)
        apps_title.move_to([0, 3.2, 0])
        self.play(Write(apps_title), run_time=0.8)

        # Application 1: Velocity (position curve → slope = speed)
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
        
        # Animated dot on position curve
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

        self.play(FadeIn(app_axes, x_lab, y_lab), Create(pos_curve), run_time=0.8)
        self.add(vel_dot, vel_tangent)
        self.play(Write(vel_label), run_time=0.5)
        self.play(vt.animate.set_value(4.0), run_time=3.0, rate_func=smooth)
        self.wait(0.5)

        # Application 2: Growth rate
        growth_label = Text("Rate of tumor growth", font_size=16, color=ORANGE)
        growth_label.move_to([0, -1.5, 0])
        
        # Application 3: Economics
        econ_label = Text("Marginal cost in business", font_size=16, color=VIOLET)
        econ_label.move_to([0, -2.2, 0])
        
        # Application 4: Physics
        physics_label = Text("Acceleration from velocity", font_size=16, color=CYAN)
        physics_label.move_to([0, -2.9, 0])

        self.play(Write(growth_label), run_time=0.5)
        self.wait(0.3)
        self.play(Write(econ_label), run_time=0.5)
        self.wait(0.3)
        self.play(Write(physics_label), run_time=0.5)
        self.wait(1.5)

        # Clean up everything
        self.play(
            FadeOut(apps_title), FadeOut(app_axes), FadeOut(pos_curve),
            FadeOut(x_lab), FadeOut(y_lab), FadeOut(vel_label),
            FadeOut(vel_dot), FadeOut(vel_tangent),
            FadeOut(growth_label), FadeOut(econ_label), FadeOut(physics_label),
            run_time=0.5
        )

        # Lissajous end card
        _A, _B = 1.2, 0.95
        # Rotated 90°: swap sin(3t)/sin(2t) roles
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
