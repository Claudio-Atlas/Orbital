"""
Orbital Sizzle Reel - Landing Page Intro Video
Option C: Eye candy → Quick example → Branding
~45-60 seconds, 1080p60
"""
from manim import *
import numpy as np

# Orbital color palette
NEON_GREEN = "#39FF14"
VIOLET = "#8B5CF6"
CYAN = "#22D3EE"
AMBER = "#F59E0B"
ROSE = "#F43F5E"

class OrbitalSizzle(Scene):
    def construct(self):
        self.camera.background_color = "#000000"

        # ═══════════════════════════════════════════
        # PART 1: EYE CANDY MONTAGE (~15 seconds)
        # ═══════════════════════════════════════════

        # --- 1a: Parametric curve tracing ---
        axes1 = Axes(
            x_range=[-3, 3, 1], y_range=[-2, 2, 1],
            x_length=10, y_length=6,
            axis_config={"color": WHITE, "stroke_opacity": 0.3},
        )
        
        parametric = axes1.plot_parametric_curve(
            lambda t: np.array([np.sin(2*t), np.sin(3*t), 0]),
            t_range=[0, 2*PI],
            color=CYAN,
        )
        
        trace_dot = Dot(color=NEON_GREEN, radius=0.08)
        trace_dot.move_to(parametric.get_start())
        
        self.play(Create(axes1), run_time=0.5)
        self.play(
            Create(parametric),
            MoveAlongPath(trace_dot, parametric),
            run_time=3,
            rate_func=smooth,
        )
        self.wait(0.3)
        self.play(FadeOut(axes1), FadeOut(parametric), FadeOut(trace_dot), run_time=0.4)

        # --- 1b: Function transformation ---
        axes2 = Axes(
            x_range=[-4, 4, 1], y_range=[-2, 4, 1],
            x_length=10, y_length=6,
            axis_config={"color": WHITE, "stroke_opacity": 0.3},
        )
        
        sin_graph = axes2.plot(lambda x: np.sin(x), color=VIOLET)
        sin_label = MathTex(r"y = \sin(x)", color=VIOLET, font_size=32)
        sin_label.to_corner(UR).shift(LEFT*0.5)
        
        cos_graph = axes2.plot(lambda x: np.cos(x), color=CYAN)
        cos_label = MathTex(r"y = \cos(x)", color=CYAN, font_size=32)
        cos_label.to_corner(UR).shift(LEFT*0.5)
        
        exp_graph = axes2.plot(lambda x: np.exp(-x**2/2), color=NEON_GREEN)
        exp_label = MathTex(r"y = e^{-x^2/2}", color=NEON_GREEN, font_size=32)
        exp_label.to_corner(UR).shift(LEFT*0.5)
        
        self.play(Create(axes2), Create(sin_graph), FadeIn(sin_label), run_time=0.8)
        self.wait(0.5)
        self.play(
            Transform(sin_graph, cos_graph),
            Transform(sin_label, cos_label),
            run_time=1.2,
        )
        self.wait(0.5)
        self.play(
            Transform(sin_graph, exp_graph),
            Transform(sin_label, exp_label),
            run_time=1.2,
        )
        self.wait(0.5)
        self.play(FadeOut(axes2), FadeOut(sin_graph), FadeOut(sin_label), run_time=0.4)

        # --- 1c: Matrix transformation on a grid ---
        plane = NumberPlane(
            x_range=[-4, 4, 1], y_range=[-4, 4, 1],
            x_length=8, y_length=8,
            background_line_style={"stroke_color": VIOLET, "stroke_opacity": 0.3},
            axis_config={"stroke_opacity": 0.5},
        )
        
        matrix = [[2, 1], [1, 2]]
        matrix_tex = MathTex(
            r"A = \begin{bmatrix} 2 & 1 \\ 1 & 2 \end{bmatrix}",
            color=AMBER, font_size=36
        )
        matrix_tex.to_corner(UL).shift(RIGHT*0.3 + DOWN*0.3)
        
        basis_i = Arrow(plane.c2p(0,0), plane.c2p(1,0), color=CYAN, buff=0)
        basis_j = Arrow(plane.c2p(0,0), plane.c2p(0,1), color=ROSE, buff=0)
        
        self.play(Create(plane), run_time=0.6)
        self.play(GrowArrow(basis_i), GrowArrow(basis_j), FadeIn(matrix_tex), run_time=0.5)
        self.play(
            plane.animate.apply_matrix(matrix),
            basis_i.animate.put_start_and_end_on(plane.c2p(0,0), plane.c2p(2,1)),
            basis_j.animate.put_start_and_end_on(plane.c2p(0,0), plane.c2p(1,2)),
            run_time=2,
        )
        self.wait(0.5)
        self.play(
            FadeOut(plane), FadeOut(basis_i), FadeOut(basis_j), FadeOut(matrix_tex),
            run_time=0.4,
        )

        # ═══════════════════════════════════════════
        # PART 2: QUICK WORKED EXAMPLE (~20 seconds)
        # ═══════════════════════════════════════════

        # "Type a problem..."
        prompt_text = Text("Type a problem...", font_size=28, color=WHITE, font="Menlo")
        prompt_text.shift(UP*2)
        cursor = Rectangle(width=0.12, height=0.4, color=VIOLET, fill_opacity=1)
        cursor.next_to(prompt_text, RIGHT, buff=0.05)
        cursor.add_updater(lambda m, dt: m.set_opacity(
            1 if int(m.get_center()[0] * 10) % 2 == 0 else 0.3
        ))
        
        self.play(FadeIn(prompt_text), FadeIn(cursor), run_time=0.5)
        self.wait(0.8)
        
        problem = MathTex(
            r"\text{Find } \frac{d}{dx}\left[x^3 + 2x^2 - 5x + 1\right]",
            color=WHITE, font_size=40
        )
        problem.shift(UP*2)
        
        self.play(
            FadeOut(prompt_text), FadeOut(cursor),
            Write(problem),
            run_time=1.5,
        )
        self.wait(0.5)
        
        # Step 1: Power rule
        step1_label = Text("Apply the power rule to each term:", font_size=22, color=CYAN)
        step1_label.next_to(problem, DOWN, buff=0.8)
        
        step1 = MathTex(
            r"\frac{d}{dx}\left[x^3\right]", r"+ \frac{d}{dx}\left[2x^2\right]",
            r"- \frac{d}{dx}\left[5x\right]", r"+ \frac{d}{dx}\left[1\right]",
            color=WHITE, font_size=36
        )
        step1.next_to(step1_label, DOWN, buff=0.4)
        
        self.play(FadeIn(step1_label), run_time=0.4)
        self.play(Write(step1), run_time=1.5)
        self.wait(0.5)
        
        # Step 2: Differentiate
        step2 = MathTex(
            r"3x^2", r"+ 4x", r"- 5", r"+ 0",
            color=WHITE, font_size=40
        )
        step2[0].set_color(VIOLET)
        step2[1].set_color(CYAN)
        step2[2].set_color(AMBER)
        step2[3].set_color(WHITE).set_opacity(0.4)
        step2.next_to(step1_label, DOWN, buff=0.4)
        
        self.play(
            TransformMatchingTex(step1, step2),
            run_time=1.5,
        )
        self.wait(0.3)
        
        # Final answer box
        answer = MathTex(r"f'(x) = 3x^2 + 4x - 5", color=WHITE, font_size=44)
        answer.shift(DOWN*0.5)
        
        box = SurroundingRectangle(
            answer, color=VIOLET, fill_color=VIOLET,
            fill_opacity=0.1, buff=0.3, corner_radius=0.1, stroke_width=2,
        )
        
        verified = Text("✓ Verified", font_size=20, color=NEON_GREEN)
        verified.next_to(box, DOWN, buff=0.2)
        
        self.play(
            FadeOut(step1_label), FadeOut(step2), FadeOut(problem),
            run_time=0.4,
        )
        self.play(
            Write(answer),
            Create(box),
            run_time=1.0,
        )
        self.play(FadeIn(verified, shift=UP*0.2), run_time=0.5)
        self.wait(1.0)
        
        self.play(
            FadeOut(answer), FadeOut(box), FadeOut(verified),
            run_time=0.5,
        )

        # ═══════════════════════════════════════════
        # PART 3: BRANDING CLOSE (~8 seconds)
        # ═══════════════════════════════════════════

        tagline1 = Text("Every step explained.", font_size=36, color=WHITE)
        tagline2 = Text("Every answer verified.", font_size=36, color=VIOLET)
        taglines = VGroup(tagline1, tagline2).arrange(DOWN, buff=0.3)
        taglines.shift(UP*0.5)
        
        self.play(FadeIn(tagline1, shift=UP*0.3), run_time=0.8)
        self.wait(0.3)
        self.play(FadeIn(tagline2, shift=UP*0.3), run_time=0.8)
        self.wait(1.0)
        
        self.play(FadeOut(taglines), run_time=0.5)
        
        # Orbital logo
        logo_text = Text("Orbital", font_size=72, color=WHITE, weight=BOLD)
        logo_sub = Text("Type a problem. Get a video.", font_size=24, color=WHITE)
        logo_sub.set_opacity(0.5)
        logo_group = VGroup(logo_text, logo_sub).arrange(DOWN, buff=0.3)
        
        self.play(FadeIn(logo_group, scale=0.9), run_time=1.0)
        self.wait(2.0)
        self.play(FadeOut(logo_group), run_time=0.8)
        self.wait(0.5)
