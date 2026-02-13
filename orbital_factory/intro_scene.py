"""
Orbital VideoFactory - Intro Scene
Logo animation with brand colors
"""

from manim import *

# Orbital brand colors
ORBITAL_VIOLET = "#8B5CF6"
ORBITAL_CYAN = "#22D3EE"

class OrbitalIntro(Scene):
    """
    Animated intro with Orbital logo (with name).
    Clean and simple - logo already has the brand name.
    """
    
    def construct(self):
        self.camera.background_color = "#000000"
        
        # Load logo WITH name (cropped version)
        logo = ImageMobject("orbital-logo-with-name.png")
        logo.scale(0.6)
        
        # Subtle glow ring (orbital motif)
        ring = Circle(radius=2.2, color=ORBITAL_VIOLET, stroke_width=2)
        ring.set_opacity(0.3)
        
        # Animations
        self.play(
            FadeIn(ring, scale=0.5),
            run_time=0.5
        )
        self.play(
            FadeIn(logo, scale=0.85),
            ring.animate.set_opacity(0.05),
            run_time=1.2
        )
        self.wait(1.5)
        
        # Fade out
        self.play(
            FadeOut(logo),
            FadeOut(ring),
            run_time=0.5
        )
        self.wait(0.2)


class OrbitalIntroMinimal(Scene):
    """
    Minimal intro - just logo fade in/out.
    """
    
    def construct(self):
        self.camera.background_color = "#000000"
        
        logo = ImageMobject("orbital-logo-with-name.png")
        logo.scale(0.5)
        
        self.play(FadeIn(logo, scale=0.9), run_time=1)
        self.wait(1.5)
        self.play(FadeOut(logo, shift=UP * 0.3), run_time=0.5)
        self.wait(0.2)


if __name__ == "__main__":
    print("Render with: manim -ql intro_scene.py OrbitalIntro")
