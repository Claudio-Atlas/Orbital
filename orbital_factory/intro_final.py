"""
Orbital Intro — Final Production Version
=========================================
Animated logo: planet with layered rings + orbiting satellite.
Fades out ready for main content.
"""

from manim import *
import numpy as np

# Brand colors
NEON_VIOLET = "#A855F7"
NEON_PURPLE = "#C084FC"
NEON_WHITE = "#FFFFFF"
NEON_BLUE = "#00D4FF"


class OrbitalIntro(Scene):
    """
    Production intro animation:
    - Thick planet with 3D glow effect
    - Layered orbital rings (white outer, blue inner)
    - Orbiting satellite (blue outside, white inside)
    - Pulse and fade out
    
    Duration: ~2 seconds
    """
    
    def construct(self):
        self.camera.background_color = "#000000"
        
        # === WATERMARK ===
        watermark = Text("ORBITAL", font_size=14, color=NEON_WHITE).set_opacity(0.4)
        watermark.to_corner(DR, buff=0.3)
        self.add(watermark)
        
        # === PLANET (3D sphere effect) ===
        planet_layers = VGroup()
        
        # Core solid circle (thickest)
        planet_core = Circle(radius=0.5, color=NEON_WHITE, stroke_width=8)
        planet_layers.add(planet_core)
        
        # Outer glow layers for 3D depth
        for r_offset, opacity, width in [
            (0.02, 0.5, 5),
            (0.04, 0.25, 4),
            (0.07, 0.12, 3),
        ]:
            glow_layer = Circle(
                radius=0.5 + r_offset,
                color=NEON_WHITE,
                stroke_width=width,
                stroke_opacity=opacity
            )
            planet_layers.add(glow_layer)
        
        # Planet violet glow
        planet_glow = Circle(radius=0.55, color=NEON_VIOLET, stroke_width=14, stroke_opacity=0.15)
        
        # === ORBITAL RINGS (layered) ===
        
        # Outer white ring (subtle)
        orbit_outer = Ellipse(
            width=1.9, height=0.65,
            color=NEON_WHITE,
            stroke_width=2,
            stroke_opacity=0.4
        )
        orbit_outer.rotate(-30 * DEGREES)
        
        # Main white ring
        orbit_ring = Ellipse(
            width=1.8, height=0.6,
            color=NEON_WHITE,
            stroke_width=2.5
        )
        orbit_ring.rotate(-30 * DEGREES)
        
        # Inner blue ring
        orbit_inner = Ellipse(
            width=1.7, height=0.55,
            color=NEON_BLUE,
            stroke_width=2,
            stroke_opacity=0.8
        )
        orbit_inner.rotate(-30 * DEGREES)
        
        # Violet glow behind rings
        orbit_glow = Ellipse(
            width=1.85, height=0.62,
            color=NEON_VIOLET,
            stroke_width=10,
            stroke_opacity=0.15
        )
        orbit_glow.rotate(-30 * DEGREES)
        
        orbit_rings = VGroup(orbit_glow, orbit_outer, orbit_ring, orbit_inner)
        
        # === SATELLITE (blue outside, white inside) ===
        angle = 50 * DEGREES
        sat_x = 0.9 * np.cos(angle) * np.cos(-30 * DEGREES) - 0.3 * np.sin(angle) * np.sin(-30 * DEGREES)
        sat_y = 0.9 * np.cos(angle) * np.sin(-30 * DEGREES) + 0.3 * np.sin(angle) * np.cos(-30 * DEGREES)
        
        satellite_outer_glow = Dot(point=[sat_x, sat_y, 0], radius=0.18, color=NEON_BLUE, fill_opacity=0.25)
        satellite_blue = Dot(point=[sat_x, sat_y, 0], radius=0.12, color=NEON_BLUE, fill_opacity=0.7)
        satellite_white = Dot(point=[sat_x, sat_y, 0], radius=0.06, color=NEON_WHITE, fill_opacity=1.0)
        satellite = VGroup(satellite_outer_glow, satellite_blue, satellite_white)
        
        # === GROUP LOGO ===
        logo_glow = VGroup(planet_glow)
        logo_core = VGroup(planet_layers, orbit_rings, satellite)
        full_logo = VGroup(logo_glow, logo_core)
        
        # === ANIMATION ===
        
        # 1. Draw planet (0.25s)
        self.play(
            *[Create(layer) for layer in planet_layers],
            Create(planet_glow),
            run_time=0.25
        )
        
        # 2. Draw orbital rings (0.3s)
        self.play(
            *[Create(ring) for ring in orbit_rings],
            run_time=0.3
        )
        
        # 3. Satellite appears + orbits (0.35s)
        self.play(
            GrowFromCenter(satellite),
            run_time=0.15
        )
        
        self.play(
            Rotate(satellite, angle=40 * DEGREES, about_point=ORIGIN),
            run_time=0.2
        )
        
        # 4. Pulse (0.3s)
        self.play(
            full_logo.animate.scale(1.1),
            run_time=0.15
        )
        self.play(
            full_logo.animate.scale(1/1.1),
            run_time=0.15
        )
        
        # 5. Hold briefly then fade out (0.5s)
        self.wait(0.2)
        self.play(
            FadeOut(full_logo),
            run_time=0.3
        )


if __name__ == "__main__":
    print("Render with:")
    print("  manim -ql intro_final.py OrbitalIntro")
    print("  manim -qh intro_final.py OrbitalIntro  # high quality")
