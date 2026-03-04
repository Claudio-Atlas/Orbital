from manim import *
import numpy as np

config.pixel_width = 1080
config.pixel_height = 1080
config.frame_width = 10.8
config.frame_height = 10.8

class ProfilePic(Scene):
    def construct(self):
        self.camera.background_color = BLACK
        
        violet = "#8B5CF6"
        
        # Lissajous curve rotated 90°
        curve = ParametricFunction(
            lambda t: np.array([
                2.5 * np.sin(2 * t),
                3.3 * np.sin(3 * t),
                0
            ]),
            t_range=[0, TAU, 0.005],
            color=violet,
            stroke_width=6,
        )
        glow = curve.copy().set_stroke(color=violet, width=22, opacity=0.15)
        glow2 = curve.copy().set_stroke(color=violet, width=12, opacity=0.25)
        
        self.add(glow, glow2, curve)
