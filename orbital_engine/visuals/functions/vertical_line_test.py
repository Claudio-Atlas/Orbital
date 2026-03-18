"""Vertical line test animation — sweeps a vertical line across a graph, highlights pass/fail."""
from manim import *
import numpy as np


def build_vertical_line_test(func_expr, x_range=(-3, 3), y_range=(-3, 5),
                             passes=True, fail_x=None,
                             cyan="#22D3EE", green="#39FF14", crimson="#FF4444"):
    """
    Animate the vertical line test on a function.

    Args:
        func_expr: Lambda string, e.g. "lambda x: x**2"
        x_range: (min, max) for x-axis
        y_range: (min, max) for y-axis
        passes: Whether the test passes (is a function)
        fail_x: x-value where the test fails (for non-functions)
    """
    def animate(scene, dur):
        t = 0

        # Build axes
        axes = Axes(
            x_range=[x_range[0], x_range[1], 1],
            y_range=[y_range[0], y_range[1], 1],
            x_length=8, y_length=5,
            axis_config={"color": GREY_B, "include_numbers": True, "font_size": 14},
            tips=False,
        )
        grid = NumberPlane(
            x_range=[x_range[0], x_range[1], 1],
            y_range=[y_range[0], y_range[1], 1],
            x_length=8, y_length=5,
            background_line_style={
                "stroke_color": "#8B5CF6", "stroke_opacity": 0.15, "stroke_width": 1},
        )
        grid.move_to(axes.get_center())

        fn = eval(func_expr)
        curve = axes.plot(fn, color=cyan, stroke_width=2.5)

        scene.play(FadeIn(grid), FadeIn(axes), run_time=0.4); t += 0.4
        scene.play(Create(curve), run_time=0.6); t += 0.6

        # Vertical line sweep
        x_tracker = ValueTracker(x_range[0])

        vert_line = always_redraw(lambda: DashedLine(
            axes.c2p(x_tracker.get_value(), y_range[0]),
            axes.c2p(x_tracker.get_value(), y_range[1]),
            color=YELLOW, stroke_width=2, dash_length=0.1))

        scene.add(vert_line)
        sweep_time = min(dur * 0.5, 4.0)
        scene.play(x_tracker.animate.set_value(x_range[1]),
            run_time=sweep_time, rate_func=linear); t += sweep_time

        scene.remove(vert_line)

        # Result
        if passes:
            result = Text("✓ Passes Vertical Line Test", font_size=22,
                color=green, weight=BOLD)
            subtitle = Text("This IS a function", font_size=16, color="#888888")
        else:
            result = Text("✗ Fails Vertical Line Test", font_size=22,
                color=crimson, weight=BOLD)
            subtitle = Text("This is NOT a function", font_size=16, color="#888888")

        result.move_to(DOWN*3.2)
        subtitle.next_to(result, DOWN, buff=0.15)

        scene.play(FadeIn(result, scale=1.2), FadeIn(subtitle), run_time=0.4); t += 0.4

        scene.wait(max(0.5, dur - t - 0.5))
        scene.play(FadeOut(VGroup(grid, axes, curve, result, subtitle)), run_time=0.4)
        scene.wait(0.3)

    return None, animate
