"""Grid background, neon border, Lissajous watermark, section badge — persistent scene chrome."""
from manim import *
import numpy as np


def build_chrome(frame_w, frame_h, colors):
    """Build the persistent background chrome for any Orbital video."""
    VIOLET = colors.get("violet", "#8B5CF6")
    CYAN = colors.get("end_cyan", "#00E5FF")
    GRID = colors.get("grid", "#1a1a3a")

    # Grid
    grid = VGroup()
    for x in np.arange(-frame_w/2, frame_w/2 + 0.1, 1.0):
        grid.add(Line([x, -frame_h/2, 0], [x, frame_h/2, 0],
            color=GRID, stroke_width=0.4, stroke_opacity=0.15))
    for y in np.arange(-frame_h/2, frame_h/2 + 0.1, 1.0):
        grid.add(Line([-frame_w/2, y, 0], [frame_w/2, y, 0],
            color=GRID, stroke_width=0.4, stroke_opacity=0.15))

    # Border
    border = Rectangle(width=frame_w - 0.2, height=frame_h - 0.2,
        color=VIOLET, stroke_width=2, stroke_opacity=0.5, fill_opacity=0)
    glow = Rectangle(width=frame_w - 0.15, height=frame_h - 0.15,
        color=VIOLET, stroke_width=5, stroke_opacity=0.1, fill_opacity=0)

    # Lissajous watermark
    A, B = 0.4, 0.3
    wm_curve = ParametricFunction(
        lambda t: np.array([A*np.sin(2*t), B*np.sin(3*t), 0]),
        t_range=[0, TAU, 0.01], color=CYAN,
        stroke_width=1.5, stroke_opacity=0.25)
    wm_text = Text("ORBITAL", font_size=9, color=CYAN, weight=BOLD)
    wm_text.set_opacity(0.25)
    wm_text.next_to(wm_curve, RIGHT, buff=0.1)
    wm = VGroup(wm_curve, wm_text)
    wm.move_to([frame_w/2 - 1.2, -frame_h/2 + 0.4, 0])

    return VGroup(grid, glow, border, wm)


def build_section_badge(section_str, frame_w, frame_h, color="#8B5CF6"):
    """Small persistent section indicator top-left."""
    bg = RoundedRectangle(width=1.2, height=0.4, corner_radius=0.08,
        fill_color=color, fill_opacity=0.7, stroke_width=0)
    label = Text(f"§{section_str}", font_size=12, color=WHITE, weight=BOLD)
    badge = VGroup(bg, label)
    badge.move_to([-frame_w/2 + 1.0, frame_h/2 - 0.4, 0])
    return badge
