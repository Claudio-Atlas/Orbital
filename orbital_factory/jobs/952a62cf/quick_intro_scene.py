
from manim import *

class QuickIntro(Scene):
    def construct(self):
        self.camera.background_color = "#000000"
        
        # Load logo
        try:
            logo = ImageMobject("/Users/claudioatlas/Desktop/Orbital/orbital_factory/orbital-logo-with-name.png")
            logo.scale(0.5)
        except:
            # Fallback: text logo
            logo = Text("ORBITAL", font_size=72, color=WHITE)
        
        self.play(FadeIn(logo, scale=0.9), run_time=0.8)
        self.wait(0.7)
        self.play(FadeOut(logo), run_time=0.5)
