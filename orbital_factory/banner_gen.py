from manim import *
import numpy as np

config.pixel_width = 2560
config.pixel_height = 1440
config.frame_width = 25.6
config.frame_height = 14.4

class YoutubeBanner(Scene):
    def construct(self):
        self.camera.background_color = BLACK
        
        violet = "#8B5CF6"
        cyan = "#22D3EE"
        green = "#39FF14"
        
        # === LEFT SIDE (desktop/TV): Parabola graph with tangent line ===
        axes = Axes(
            x_range=[-3, 3, 1],
            y_range=[-2, 20, 5],
            x_length=6,
            y_length=5,
            axis_config={"color": GREY_D, "stroke_width": 1.5},
            tips=False,
        )
        axes.shift(LEFT * 8.5)
        
        # Parabola
        parabola = axes.plot(lambda x: x**2 * 3, x_range=[-2.5, 2.5], color=cyan, stroke_width=3)
        
        # Tangent line at x=1
        x0 = 1
        y0 = 3
        slope = 6  # derivative of 3x^2 at x=1
        tangent = axes.plot(lambda x: slope*(x - x0) + y0, x_range=[-0.5, 2.5], color=green, stroke_width=3)
        
        # Tangent point
        dot = Dot(axes.c2p(x0, y0), color=green, radius=0.12)
        
        # Neon grid lines (subtle)
        grid_lines = VGroup()
        for x in range(-3, 4):
            line = axes.get_vertical_line(axes.c2p(x, 20), color=violet, stroke_width=0.5).set_opacity(0.15)
            grid_lines.add(line)
        
        graph_group = VGroup(grid_lines, axes, parabola, tangent, dot)
        
        # === CENTER (all devices safe zone): Equation + tagline ===
        eq = MathTex(
            r"\frac{d}{dx}[3x^2] = 6x",
            font_size=58,
            color=WHITE
        )
        eq.shift(LEFT * 1.5 + UP * 0.3)
        
        # Subtle glow behind equation
        glow = RoundedRectangle(
            width=eq.width + 1.2,
            height=eq.height + 0.8,
            corner_radius=0.3,
            fill_color=violet,
            fill_opacity=0.05,
            stroke_width=0
        ).move_to(eq)
        
        # Tagline
        line1 = Text("Type a problem.", font_size=46, weight=BOLD, color=WHITE)
        line2 = Text("Get a video.", font_size=46, weight=BOLD, color=violet)
        line3 = Text("AI-powered math walkthroughs", font_size=22, color=GREY_C)
        tagline = VGroup(line1, line2, line3).arrange(DOWN, buff=0.25, aligned_edge=LEFT)
        tagline.shift(RIGHT * 5.5)
        
        # === RIGHT SIDE (desktop/TV): Scattered math symbols ===
        symbols = VGroup()
        symbol_texts = [r"\int", r"\sum", r"\pi", r"\infty", r"\nabla", r"\partial"]
        positions = [(10, 2.5), (11.5, -1), (9.5, -2.5), (11, 1), (10.5, -0.5), (12, -2)]
        for s, (x, y) in zip(symbol_texts, positions):
            sym = MathTex(s, font_size=40, color=violet).set_opacity(0.15)
            sym.shift(RIGHT * x + UP * y)
            symbols.add(sym)
        
        self.add(graph_group, glow, eq, tagline, symbols)
