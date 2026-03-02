from manim import *
import numpy as np

NEON_GREEN = "#39FF14"
VIOLET = "#8B5CF6"
CYAN = "#22D3EE"
AMBER = "#F59E0B"
ROSE = "#F43F5E"

class ThumbnailSizzle(Scene):
    def construct(self):
        self.camera.background_color = "#0a0a0a"
        self.camera.frame_width = 16
        self.camera.frame_height = 9
        
        # Parametric curve as background decoration
        axes = Axes(
            x_range=[-3, 3], y_range=[-2, 2],
            x_length=14, y_length=7,
            axis_config={"stroke_opacity": 0},
        )
        curve = axes.plot_parametric_curve(
            lambda t: np.array([np.sin(2*t), np.sin(3*t), 0]),
            t_range=[0, 2*PI], color=VIOLET, stroke_opacity=0.25, stroke_width=3,
        )
        self.add(curve)
        
        # Big title
        title = Text("Orbital", font_size=96, color=WHITE, weight=BOLD)
        subtitle = Text("AI Math Video Generator", font_size=36, color=VIOLET)
        group = VGroup(title, subtitle).arrange(DOWN, buff=0.4)
        self.add(group)
        
        # Small equation in corner for flavor
        eq = MathTex(r"\frac{d}{dx}\left[x^3\right] = 3x^2", font_size=28, color=WHITE)
        eq.set_opacity(0.4).to_corner(DR, buff=0.6)
        self.add(eq)


class ThumbnailDedekind(Scene):
    def construct(self):
        self.camera.background_color = "#0a0a0a"
        self.camera.frame_width = 16
        self.camera.frame_height = 9
        
        # Nested intervals visual
        line = NumberLine(x_range=[0, 1, 0.25], length=12, color=WHITE,
                         numbers_with_elongated_ticks=[0, 1],
                         include_numbers=False, stroke_opacity=0.4)
        line.shift(DOWN*1.2)
        self.add(line)
        
        colors = [CYAN, VIOLET, AMBER, ROSE]
        intervals = [(0.1, 0.9), (0.2, 0.75), (0.3, 0.65), (0.38, 0.58)]
        for i, ((a, b), col) in enumerate(zip(intervals, colors)):
            bracket_l = MathTex("[", color=col, font_size=36)
            bracket_r = MathTex("]", color=col, font_size=36)
            bracket_l.move_to(line.n2p(a))
            bracket_r.move_to(line.n2p(b))
            bar = Line(line.n2p(a), line.n2p(b), color=col, stroke_width=4 - i*0.5, stroke_opacity=0.7)
            bar.shift(UP*(0.3 + i*0.2))
            self.add(bracket_l, bracket_r, bar)
        
        # Title
        title = Text("The Reals Are", font_size=64, color=WHITE, weight=BOLD)
        title2 = Text("Uncountable", font_size=72, color=CYAN, weight=BOLD)
        group = VGroup(title, title2).arrange(DOWN, buff=0.2).shift(UP*1.2)
        self.add(group)
        
        # R symbol
        r_sym = MathTex(r"\mathbb{R}", font_size=48, color=WHITE)
        r_sym.set_opacity(0.3).to_corner(DR, buff=0.6)
        self.add(r_sym)
        
        # Verified badge
        badge = Text("Lean 4 Verified ✓", font_size=20, color=NEON_GREEN)
        badge.to_corner(DL, buff=0.6)
        self.add(badge)


class ThumbnailGroupOrder15(Scene):
    def construct(self):
        self.camera.background_color = "#0a0a0a"
        self.camera.frame_width = 16
        self.camera.frame_height = 9
        
        # Z15 cycle visualization — dots in a circle
        n = 15
        radius = 2.5
        dots = VGroup()
        for i in range(n):
            angle = i * 2 * PI / n + PI/2
            dot = Dot(
                point=[radius * np.cos(angle), radius * np.sin(angle) - 0.5, 0],
                color=VIOLET if i % 5 == 0 else (AMBER if i % 3 == 0 else WHITE),
                radius=0.08,
            )
            dots.add(dot)
        
        # Connect some edges to hint at group structure
        edges = VGroup()
        for i in range(n):
            j = (i + 1) % n
            edge = Line(dots[i].get_center(), dots[j].get_center(),
                       stroke_width=1.5, stroke_opacity=0.2, color=VIOLET)
            edges.add(edge)
        
        cycle_group = VGroup(edges, dots).shift(RIGHT*3.5)
        self.add(cycle_group)
        
        # Title on the left
        title = Text("Every Group of", font_size=52, color=WHITE, weight=BOLD)
        title2 = Text("Order 15", font_size=72, color=VIOLET, weight=BOLD)
        title3 = Text("is Cyclic", font_size=52, color=WHITE, weight=BOLD)
        group = VGroup(title, title2, title3).arrange(DOWN, buff=0.2)
        group.shift(LEFT*2.8 + UP*0.3)
        self.add(group)
        
        # Sylow equation
        eq = MathTex(r"\mathbb{Z}_{15} \cong \mathbb{Z}_3 \times \mathbb{Z}_5",
                     font_size=32, color=AMBER)
        eq.next_to(group, DOWN, buff=0.6)
        self.add(eq)
        
        # Badges
        badge = Text("Lean 4 Verified ✓", font_size=20, color=NEON_GREEN)
        badge.to_corner(DL, buff=0.6)
        self.add(badge)
        
        grade = Text('Graded A+ by PhD Mathematician', font_size=18, color=WHITE)
        grade.set_opacity(0.5)
        grade.to_corner(DR, buff=0.6)
        self.add(grade)
