"""
Orbital Intro V4 — Original Logo Style (Angled Perspective)
============================================================
Planet with tilted orbital ring + satellite dot.
Morphs into equation.
"""

from manim import *
import numpy as np

# Brand colors
NEON_VIOLET = "#A855F7"
NEON_PURPLE = "#C084FC"
NEON_WHITE = "#FFFFFF"
NEON_BLUE = "#00D4FF"  # Bright cyan-blue for satellite


class OrbitalLogoIntro(Scene):
    """
    The original Orbital logo animated:
    - Central planet (thick circle with 3D sphere effect)
    - Tilted orbital ring (ellipse at -30°)
    - Glowing satellite dot (blue outside, white inside)
    Then morphs into the equation.
    """
    
    def construct(self):
        self.camera.background_color = "#000000"
        
        equation_text = getattr(self, 'equation', r"\int x e^{x^2} \, dx")
        
        # === WATERMARK ===
        watermark = Text("ORBITAL", font_size=14, color=NEON_WHITE).set_opacity(0.4)
        watermark.to_corner(DR, buff=0.3)
        self.add(watermark)
        
        # === LOGO COMPONENTS ===
        
        # Planet (3D sphere effect with varying thickness)
        # Multiple concentric circles with decreasing opacity for that globe look
        planet_layers = VGroup()
        
        # Core solid circle (thickest)
        planet_core = Circle(radius=0.5, color=NEON_WHITE, stroke_width=8)
        planet_layers.add(planet_core)
        
        # Outer glow layers (progressively fainter for 3D depth)
        for i, (r_offset, opacity, width) in enumerate([
            (0.02, 0.5, 5),    # Inner soft edge
            (0.04, 0.25, 4),   # Mid glow
            (0.07, 0.12, 3),   # Outer soft
        ]):
            glow_layer = Circle(
                radius=0.5 + r_offset,
                color=NEON_WHITE,
                stroke_width=width,
                stroke_opacity=opacity
            )
            planet_layers.add(glow_layer)
        
        # Planet violet glow (behind everything)
        planet_glow = Circle(radius=0.55, color=NEON_VIOLET, stroke_width=14, stroke_opacity=0.15)
        
        # Orbital rings (layered for neon depth effect)
        # -30 degree rotation gives that Saturn-like angled look
        
        # Outer white ring (largest, subtle)
        orbit_outer = Ellipse(
            width=1.9,
            height=0.65,
            color=NEON_WHITE,
            stroke_width=2,
            stroke_opacity=0.4
        )
        orbit_outer.rotate(-30 * DEGREES)
        
        # Main white ring
        orbit_ring = Ellipse(
            width=1.8,
            height=0.6,
            color=NEON_WHITE,
            stroke_width=2.5
        )
        orbit_ring.rotate(-30 * DEGREES)
        
        # Inner blue ring (smaller, neon pop)
        orbit_inner = Ellipse(
            width=1.7,
            height=0.55,
            color=NEON_BLUE,
            stroke_width=2,
            stroke_opacity=0.8
        )
        orbit_inner.rotate(-30 * DEGREES)
        
        # Violet glow behind all rings
        orbit_glow = Ellipse(
            width=1.85,
            height=0.62,
            color=NEON_VIOLET,
            stroke_width=10,
            stroke_opacity=0.15
        )
        orbit_glow.rotate(-30 * DEGREES)
        
        # Group all rings
        orbit_rings = VGroup(orbit_glow, orbit_outer, orbit_ring, orbit_inner)
        
        # Satellite dot (neon blue outside, white inside)
        # Calculate position on tilted ellipse
        angle = 50 * DEGREES  # Position on orbit
        sat_x = 0.9 * np.cos(angle) * np.cos(-30 * DEGREES) - 0.3 * np.sin(angle) * np.sin(-30 * DEGREES)
        sat_y = 0.9 * np.cos(angle) * np.sin(-30 * DEGREES) + 0.3 * np.sin(angle) * np.cos(-30 * DEGREES)
        
        # Satellite: layered for blue-outside, white-inside effect
        satellite_outer_glow = Dot(point=[sat_x, sat_y, 0], radius=0.18, color=NEON_BLUE, fill_opacity=0.25)
        satellite_blue = Dot(point=[sat_x, sat_y, 0], radius=0.12, color=NEON_BLUE, fill_opacity=0.7)
        satellite_white = Dot(point=[sat_x, sat_y, 0], radius=0.06, color=NEON_WHITE, fill_opacity=1.0)
        satellite = VGroup(satellite_outer_glow, satellite_blue, satellite_white)
        
        # Group the logo
        logo_glow = VGroup(planet_glow)
        logo_core = VGroup(planet_layers, orbit_rings, satellite)
        full_logo = VGroup(logo_glow, logo_core)
        
        # === EQUATION ===
        equation = MathTex(equation_text, color=NEON_WHITE)
        equation.scale(1.4)
        
        # Equation glow
        eq_glow = equation.copy().set_color(NEON_VIOLET).set_opacity(0.25).scale(1.02)
        equation_full = VGroup(eq_glow, equation)
        
        # === ANIMATION ===
        
        # 1. Draw planet first (0.25s)
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
        
        # 3. Satellite appears + orbits slightly (0.35s)
        self.play(
            GrowFromCenter(satellite),
            run_time=0.15
        )
        
        # Quick orbital movement
        self.play(
            Rotate(satellite, angle=40 * DEGREES, about_point=ORIGIN),
            run_time=0.2
        )
        
        # 4. Pulse + morph to equation (0.7s)
        self.play(
            full_logo.animate.scale(1.1),
            run_time=0.15
        )
        
        self.play(
            ReplacementTransform(full_logo, equation_full),
            run_time=0.55
        )
        
        # 5. Hold (0.3s)
        self.wait(0.3)


class OrbitalLogoIntroFast(Scene):
    """
    Faster version - ~1.5 seconds total.
    """
    
    def construct(self):
        self.camera.background_color = "#000000"
        
        equation_text = getattr(self, 'equation', r"\int x e^{x^2} \, dx")
        
        # Watermark
        watermark = Text("ORBITAL", font_size=14, color=NEON_WHITE).set_opacity(0.4)
        watermark.to_corner(DR, buff=0.3)
        self.add(watermark)
        
        # Planet (3D sphere effect with varying thickness)
        planet_layers = VGroup()
        planet_core = Circle(radius=0.5, color=NEON_WHITE, stroke_width=8)
        planet_layers.add(planet_core)
        for r_offset, opacity, width in [(0.02, 0.5, 5), (0.04, 0.25, 4), (0.07, 0.12, 3)]:
            glow_layer = Circle(radius=0.5 + r_offset, color=NEON_WHITE, stroke_width=width, stroke_opacity=opacity)
            planet_layers.add(glow_layer)
        planet_glow = Circle(radius=0.55, color=NEON_VIOLET, stroke_width=14, stroke_opacity=0.15)
        
        # Tilted orbit rings (layered)
        orbit_outer = Ellipse(width=1.9, height=0.65, color=NEON_WHITE, stroke_width=2, stroke_opacity=0.4)
        orbit_outer.rotate(-30 * DEGREES)
        orbit_ring = Ellipse(width=1.8, height=0.6, color=NEON_WHITE, stroke_width=2.5)
        orbit_ring.rotate(-30 * DEGREES)
        orbit_inner = Ellipse(width=1.7, height=0.55, color=NEON_BLUE, stroke_width=2, stroke_opacity=0.8)
        orbit_inner.rotate(-30 * DEGREES)
        orbit_glow = Ellipse(width=1.85, height=0.62, color=NEON_VIOLET, stroke_width=10, stroke_opacity=0.15)
        orbit_glow.rotate(-30 * DEGREES)
        orbit_rings = VGroup(orbit_glow, orbit_outer, orbit_ring, orbit_inner)
        
        # Satellite (neon blue outside, white inside)
        sat_x = 0.9 * np.cos(50 * DEGREES) * np.cos(-30 * DEGREES) - 0.3 * np.sin(50 * DEGREES) * np.sin(-30 * DEGREES)
        sat_y = 0.9 * np.cos(50 * DEGREES) * np.sin(-30 * DEGREES) + 0.3 * np.sin(50 * DEGREES) * np.cos(-30 * DEGREES)
        satellite_outer_glow = Dot(point=[sat_x, sat_y, 0], radius=0.18, color=NEON_BLUE, fill_opacity=0.25)
        satellite_blue = Dot(point=[sat_x, sat_y, 0], radius=0.12, color=NEON_BLUE, fill_opacity=0.7)
        satellite_white = Dot(point=[sat_x, sat_y, 0], radius=0.06, color=NEON_WHITE, fill_opacity=1.0)
        satellite = VGroup(satellite_outer_glow, satellite_blue, satellite_white)
        
        full_logo = VGroup(planet_glow, planet_layers, orbit_rings, satellite)
        
        # Equation
        equation = MathTex(equation_text, color=NEON_WHITE).scale(1.4)
        
        # All at once draw (0.4s)
        self.play(
            LaggedStart(
                *[Create(layer) for layer in planet_layers],
                Create(planet_glow),
                *[Create(ring) for ring in orbit_rings],
                GrowFromCenter(satellite),
                lag_ratio=0.05
            ),
            run_time=0.4
        )
        
        # Quick pulse + morph (0.6s)
        self.play(
            full_logo.animate.scale(1.1),
            run_time=0.1
        )
        
        self.play(
            ReplacementTransform(full_logo, equation),
            run_time=0.5
        )
        
        self.wait(0.3)


class OrbitalLogoIntroSmooth(Scene):
    """
    Smoothest version - logo fades in fully formed, then morphs.
    """
    
    def construct(self):
        self.camera.background_color = "#000000"
        
        equation_text = getattr(self, 'equation', r"\int x e^{x^2} \, dx")
        
        # Watermark
        watermark = Text("ORBITAL", font_size=14, color=NEON_WHITE).set_opacity(0.4)
        watermark.to_corner(DR, buff=0.3)
        self.add(watermark)
        
        # Build full logo
        # Planet (3D sphere effect with varying thickness)
        planet_layers = VGroup()
        planet_core = Circle(radius=0.5, color=NEON_WHITE, stroke_width=8)
        planet_layers.add(planet_core)
        for r_offset, opacity, width in [(0.02, 0.5, 5), (0.04, 0.25, 4), (0.07, 0.12, 3)]:
            glow_layer = Circle(radius=0.5 + r_offset, color=NEON_WHITE, stroke_width=width, stroke_opacity=opacity)
            planet_layers.add(glow_layer)
        planet_glow = Circle(radius=0.55, color=NEON_VIOLET, stroke_width=14, stroke_opacity=0.15)
        
        # Layered orbit rings
        orbit_outer = Ellipse(width=1.9, height=0.65, color=NEON_WHITE, stroke_width=2, stroke_opacity=0.4)
        orbit_outer.rotate(-30 * DEGREES)
        orbit_ring = Ellipse(width=1.8, height=0.6, color=NEON_WHITE, stroke_width=2.5)
        orbit_ring.rotate(-30 * DEGREES)
        orbit_inner = Ellipse(width=1.7, height=0.55, color=NEON_BLUE, stroke_width=2, stroke_opacity=0.8)
        orbit_inner.rotate(-30 * DEGREES)
        orbit_glow = Ellipse(width=1.85, height=0.62, color=NEON_VIOLET, stroke_width=10, stroke_opacity=0.15)
        orbit_glow.rotate(-30 * DEGREES)
        orbit_rings = VGroup(orbit_glow, orbit_outer, orbit_ring, orbit_inner)
        
        sat_x = 0.75
        sat_y = 0.35
        satellite_outer_glow = Dot(point=[sat_x, sat_y, 0], radius=0.18, color=NEON_BLUE, fill_opacity=0.25)
        satellite_blue = Dot(point=[sat_x, sat_y, 0], radius=0.12, color=NEON_BLUE, fill_opacity=0.7)
        satellite_white = Dot(point=[sat_x, sat_y, 0], radius=0.06, color=NEON_WHITE, fill_opacity=1.0)
        satellite = VGroup(satellite_outer_glow, satellite_blue, satellite_white)
        
        full_logo = VGroup(planet_glow, planet_layers, orbit_rings, satellite)
        full_logo.scale(0.9)
        
        # Equation
        equation = MathTex(equation_text, color=NEON_WHITE).scale(1.4)
        
        # Fade in logo (0.4s)
        self.play(
            FadeIn(full_logo, scale=0.85),
            run_time=0.4
        )
        
        # Brief hold with subtle pulse (0.3s)
        self.play(
            full_logo.animate.scale(1.08),
            run_time=0.15
        )
        self.play(
            full_logo.animate.scale(1/1.08),
            run_time=0.15
        )
        
        # Morph to equation (0.6s)
        self.play(
            ReplacementTransform(full_logo, equation),
            run_time=0.6
        )
        
        self.wait(0.3)


if __name__ == "__main__":
    print("Render with:")
    print("  manim -ql intro_v4_logo.py OrbitalLogoIntro")
    print("  manim -ql intro_v4_logo.py OrbitalLogoIntroFast")
    print("  manim -ql intro_v4_logo.py OrbitalLogoIntroSmooth")
