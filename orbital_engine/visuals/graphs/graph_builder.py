"""Build a graph with NumberPlane, Axes, functions, tangent lines, dots, and shaded areas."""
from manim import *
import numpy as np


def build_graph(axes_cfg, scene, dur, layout="landscape",
                cyan="#22D3EE", violet="#8B5CF6", green="#39FF14"):
    """
    Full-featured graph builder extracted from shorts engine.

    Args:
        axes_cfg: Dict with:
            x_range, y_range, functions (list of {expr, color, label}),
            tangent ({at_x, length, color, func_index}),
            shaded_area ({func_index, x_range, color, opacity}),
            dots (list of {x, y, color, radius, label})
        layout: "landscape" or "short"
    """
    GRAPH_WIDTH = 8.0 if layout == "landscape" else 3.4
    GRAPH_HEIGHT = 4.0 if layout == "landscape" else 2.8

    x_range = axes_cfg.get("x_range", [-3, 3, 1])
    y_range = axes_cfg.get("y_range", [-7, 25, 5])
    functions = axes_cfg.get("functions", [])

    grid = NumberPlane(
        x_range=x_range, y_range=y_range,
        x_length=GRAPH_WIDTH, y_length=GRAPH_HEIGHT,
        background_line_style={
            "stroke_color": violet, "stroke_opacity": 0.25, "stroke_width": 1},
        faded_line_style={
            "stroke_color": cyan, "stroke_opacity": 0.12, "stroke_width": 0.5},
    )
    axes = Axes(
        x_range=x_range, y_range=y_range,
        x_length=GRAPH_WIDTH, y_length=GRAPH_HEIGHT,
        axis_config={
            "color": GREY_B, "include_numbers": True, "font_size": 12,
            "numbers_to_exclude": [0]},
        tips=False,
    )
    grid.move_to(axes.get_center())
    group = VGroup(grid, axes)

    colors = [cyan, "#F97316", "#EC4899", green]
    plotted = []

    for idx, fn_cfg in enumerate(functions):
        expr_str = fn_cfg.get("expr", "lambda x: x")
        color = fn_cfg.get("color", colors[idx % len(colors)])
        try:
            fn_obj = eval(expr_str) if "lambda" in expr_str else eval(f"lambda x: {expr_str}")
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
                    lbl_mob.move_to(axes.c2p(lbl_x, fn_obj(lbl_x)) + UP*0.25 + LEFT*0.3)
                except Exception:
                    lbl_mob.move_to(axes.c2p(0, 0) + UP*0.3)
                group.add(lbl_mob)
        except Exception as e:
            print(f"  ⚠️  Graph eval failed: {e}")

    # Tangent line
    tangent = axes_cfg.get("tangent", None)
    if tangent and plotted:
        at_x = tangent.get("at_x", 0)
        t_len = tangent.get("length", 2.0)
        t_col = tangent.get("color", green)
        try:
            fn = plotted[tangent.get("func_index", 0)]
            dx = 1e-5
            slope = (fn(at_x + dx) - fn(at_x - dx)) / (2*dx)
            y0 = fn(at_x)
            half = t_len / 2
            tline = Line(
                axes.c2p(at_x - half, y0 - slope*half),
                axes.c2p(at_x + half, y0 + slope*half),
                color=t_col, stroke_width=2.5)
            dot = Dot(axes.c2p(at_x, y0), color=t_col, radius=0.06)
            group.add(tline, dot)
        except Exception:
            pass

    # Shaded area
    shaded = axes_cfg.get("shaded_area", None)
    if shaded and plotted:
        fi = shaded.get("func_index", 0)
        sr = shaded.get("x_range", [x_range[0], x_range[1]])
        sc = shaded.get("color", cyan)
        so = shaded.get("opacity", 0.3)
        try:
            if fi < len(plotted):
                top_graph = axes.plot(plotted[fi], color=sc)
                area = axes.get_area(top_graph, x_range=sr, color=sc, opacity=so)
                group.add(area)
        except Exception:
            pass

    # Dots
    for d in axes_cfg.get("dots", []):
        dx, dy = d.get("x", 0), d.get("y", 0)
        dc = d.get("color", green)
        dr = d.get("radius", 0.07)
        dl = d.get("label", "")
        try:
            dot_mob = Dot(axes.c2p(dx, dy), color=dc, radius=dr)
            group.add(dot_mob)
            if dl:
                dot_lbl = MathTex(dl, font_size=14, color=dc)
                dot_lbl.next_to(dot_mob, UP + RIGHT, buff=0.08)
                group.add(dot_lbl)
        except Exception:
            pass

    return group, axes, plotted
