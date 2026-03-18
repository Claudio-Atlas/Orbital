"""Orbital Lissajous outro with wordmark and tagline."""
from manim import *
import numpy as np


def build_outro(cyan="#00E5FF", box_fill="#13121f"):
    """Returns (None, animate_fn) — always 3s."""
    def animate(scene, dur):
        A, B = 2.0, 1.5
        liss_glow = ParametricFunction(
            lambda t: np.array([A*np.sin(2*t), B*np.sin(3*t), 0]),
            t_range=[0, TAU, 0.01], color=cyan,
            stroke_width=10, stroke_opacity=0.2)
        liss_core = ParametricFunction(
            lambda t: np.array([A*np.sin(2*t), B*np.sin(3*t), 0]),
            t_range=[0, TAU, 0.01], color=cyan,
            stroke_width=3, stroke_opacity=1.0)
        logo = VGroup(liss_glow, liss_core).move_to([0, 0.5, 0])

        wordmark = Text("ORBITAL", font_size=48, color=cyan, weight=BOLD)
        wm_glow = wordmark.copy().set_opacity(0.3).scale(1.03)
        wordmark.next_to(logo, DOWN, buff=0.35)
        wm_glow.move_to(wordmark.get_center())

        handle = Text("@orbital-solver", font_size=24, color=cyan)
        handle.set_opacity(0.7)
        handle.next_to(wordmark, DOWN, buff=0.2)

        tagline = Text("Watch it click.", font_size=26, color=WHITE)
        tagline.set_opacity(0.6)
        tagline.next_to(handle, DOWN, buff=0.3)

        cta_box = SurroundingRectangle(
            VGroup(wordmark, handle), color=cyan, fill_color=box_fill,
            fill_opacity=0.3, buff=0.25, corner_radius=0.1, stroke_width=2)

        scene.play(Create(liss_core, run_time=1.0), FadeIn(liss_glow, run_time=0.8))
        scene.play(FadeIn(VGroup(wm_glow, wordmark), shift=UP*0.2), run_time=0.4)
        scene.play(FadeIn(handle), FadeIn(tagline), run_time=0.3)
        scene.play(Create(cta_box), run_time=0.3)
        scene.wait(1.0)
        scene.play(
            FadeOut(VGroup(logo, wm_glow, wordmark, handle, tagline, cta_box)),
            run_time=0.5)
        scene.wait(0.3)

    return None, animate
