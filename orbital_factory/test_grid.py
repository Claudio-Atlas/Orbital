from manim import *

config.frame_width = 4.5
config.frame_height = 8.0

class TestGrid(Scene):
    def construct(self):
        self.camera.background_color = "#000000"
        
        x_range = [-3, 3, 1]
        y_range = [-7, 25, 5]
        GRAPH_WIDTH = 3.375 * 0.90
        GRAPH_HEIGHT = 2.8
        
        # Neon grid — bump opacity so it's visible
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
        graph_group = VGroup(grid, axes)
        graph_group.move_to([0, -1.8, 0])
        
        # Plot the function
        fn = lambda x: 3*x**2 + 2*x - 5
        import numpy as np
        test_xs = np.linspace(-3, 3, 200)
        test_ys = [fn(x) for x in test_xs]
        valid = [x for x, y in zip(test_xs, test_ys) if -7 <= y <= 25]
        safe_lo = max(-3, min(valid) - 0.1)
        safe_hi = min(3, max(valid) + 0.1)
        curve = axes.plot(fn, x_range=[safe_lo, safe_hi], color="#22D3EE", stroke_width=2.5)
        
        self.add(graph_group, curve)
        
        # Also test some math above
        eq = MathTex(r"f(x) = 3x^2 + 2x - 5", color=WHITE, font_size=36)
        eq.move_to([0, 1.5, 0])
        self.add(eq)
        
        self.wait(3)
