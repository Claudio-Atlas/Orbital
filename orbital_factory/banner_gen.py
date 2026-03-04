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
        
        # Lissajous curve rotated 90°
        curve = ParametricFunction(
            lambda t: np.array([
                1.5 * np.sin(2 * t),
                2.0 * np.sin(3 * t),
                0
            ]),
            t_range=[0, TAU, 0.005],
            color=violet,
            stroke_width=4,
        )
        glow = curve.copy().set_stroke(color=violet, width=14, opacity=0.15)
        glow2 = curve.copy().set_stroke(color=violet, width=8, opacity=0.25)
        
        curve_group = VGroup(glow, glow2, curve).shift(LEFT * 4.5)
        
        # ORBITAL wordmark
        title = Text("ORBITAL", font_size=72, weight=BOLD, color=WHITE)
        title.next_to(curve_group, RIGHT, buff=2.0)
        
        # Tagline
        tagline = Text("Type a problem. Get a video.", font_size=28, color=GREY_C)
        tagline.next_to(title, DOWN, buff=0.4, aligned_edge=LEFT)
        
        # Subtle violet accents at far edges
        for x_off in [-12.0, -11.5]:
            accent = ParametricFunction(
                lambda t: np.array([
                    x_off + 0.12 * np.sin(6 * t),
                    5.0 * np.sin(t),
                    0
                ]),
                t_range=[0, TAU, 0.01],
                color=violet,
                stroke_width=1.5,
                stroke_opacity=0.15,
            )
            self.add(accent)
            self.add(accent.copy().shift(RIGHT * (abs(x_off) * 2)))
        
        self.add(curve_group, title, tagline)
