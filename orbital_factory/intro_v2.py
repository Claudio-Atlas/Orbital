"""
Orbital Intro V2 — Ring Morphs to Equation
==========================================
A sleek 2-second intro where orbital rings draw themselves
and then morph into the problem equation.

Tesla-style: Black background, white/violet accents.
"""

from manim import *

# Brand colors
ORBITAL_VIOLET = "#8B5CF6"
ORBITAL_CYAN = "#22D3EE"
ORBITAL_WHITE = "#FFFFFF"


class OrbitalIntroV2(Scene):
    """
    The orbital ring draws itself, then morphs into the equation.
    Total time: ~2 seconds
    """
    
    def construct(self):
        self.camera.background_color = "#000000"
        
        # The equation we'll morph into (passed as config or default)
        equation_text = getattr(self, 'equation', r"\int x e^{x^2} \, dx")
        
        # Create orbital rings
        ring1 = Circle(radius=0.8, color=ORBITAL_VIOLET, stroke_width=2)
        ring2 = Circle(radius=0.5, color=ORBITAL_WHITE, stroke_width=1.5)
        ring3 = Circle(radius=0.3, color=ORBITAL_VIOLET, stroke_width=1, stroke_opacity=0.6)
        
        # Small dot orbiting (like a planet)
        dot = Dot(color=ORBITAL_WHITE, radius=0.06)
        dot.move_to(ring1.point_at_angle(0))
        
        # Group the rings
        rings = VGroup(ring1, ring2, ring3)
        
        # Create the equation (hidden initially)
        equation = MathTex(equation_text, color=ORBITAL_WHITE)
        equation.scale(1.4)
        
        # Animation sequence
        # 1. Draw rings quickly (0.5s)
        self.play(
            Create(ring1, run_time=0.3),
            Create(ring2, run_time=0.25),
            Create(ring3, run_time=0.2),
            FadeIn(dot, scale=0.5, run_time=0.2),
        )
        
        # 2. Brief orbit + pulse (0.3s)
        self.play(
            Rotate(dot, angle=PI/2, about_point=ORIGIN, run_time=0.3),
            rings.animate.scale(1.1).set_stroke(opacity=0.8),
            run_time=0.3
        )
        
        # 3. Morph rings into equation (0.7s)
        self.play(
            ReplacementTransform(rings, equation, run_time=0.6),
            FadeOut(dot, run_time=0.3),
        )
        
        # 4. Brief hold on equation (0.3s)
        self.wait(0.3)
        
        # 5. Subtle glow pulse on equation (0.2s) - signals "ready"
        self.play(
            equation.animate.set_color(ORBITAL_WHITE),
            run_time=0.2
        )


class OrbitalIntroMinimal(Scene):
    """
    Even simpler version — just ring to equation.
    Total time: ~1.5 seconds
    """
    
    def construct(self):
        self.camera.background_color = "#000000"
        
        equation_text = getattr(self, 'equation', r"\int x e^{x^2} \, dx")
        
        # Single elegant ring
        ring = Circle(radius=0.6, color=ORBITAL_VIOLET, stroke_width=2.5)
        
        # Inner dot
        dot = Dot(color=ORBITAL_WHITE, radius=0.08)
        
        # Equation
        equation = MathTex(equation_text, color=ORBITAL_WHITE)
        equation.scale(1.4)
        
        # Quick sequence
        self.play(
            Create(ring, run_time=0.4),
            GrowFromCenter(dot, run_time=0.3),
        )
        
        self.play(
            ReplacementTransform(VGroup(ring, dot), equation, run_time=0.6),
        )
        
        self.wait(0.3)


class OrbitalIntroWithText(Scene):
    """
    Ring morphs to "SOLVER" text, then to equation.
    Total time: ~2.5 seconds
    """
    
    def construct(self):
        self.camera.background_color = "#000000"
        
        equation_text = getattr(self, 'equation', r"\int x e^{x^2} \, dx")
        
        # Orbital ring
        ring = Circle(radius=0.5, color=ORBITAL_VIOLET, stroke_width=3)
        
        # "SOLVER" text
        solver_text = Text("SOLVER", font_size=48, color=ORBITAL_WHITE, weight=BOLD)
        
        # Equation
        equation = MathTex(equation_text, color=ORBITAL_WHITE)
        equation.scale(1.4)
        
        # Sequence
        self.play(Create(ring, run_time=0.4))
        
        self.play(
            ReplacementTransform(ring, solver_text, run_time=0.5),
        )
        
        self.wait(0.4)
        
        self.play(
            ReplacementTransform(solver_text, equation, run_time=0.6),
        )
        
        self.wait(0.3)


class OrbitalIntroOrbitPath(Scene):
    """
    Elliptical orbit path that morphs into equation.
    Most "orbital" feeling.
    """
    
    def construct(self):
        self.camera.background_color = "#000000"
        
        equation_text = getattr(self, 'equation', r"\int x e^{x^2} \, dx")
        
        # Elliptical orbit
        orbit = Ellipse(width=2, height=1, color=ORBITAL_VIOLET, stroke_width=2)
        
        # "Sun" at center
        sun = Dot(color=ORBITAL_VIOLET, radius=0.1)
        sun.set_fill(opacity=0.8)
        
        # "Planet" on orbit
        planet = Dot(color=ORBITAL_WHITE, radius=0.07)
        planet.move_to(orbit.point_at_angle(0))
        
        # Equation
        equation = MathTex(equation_text, color=ORBITAL_WHITE)
        equation.scale(1.4)
        
        # Draw orbit
        self.play(
            Create(orbit, run_time=0.3),
            GrowFromCenter(sun, run_time=0.2),
            FadeIn(planet, run_time=0.2),
        )
        
        # Quick orbit
        self.play(
            Rotate(planet, angle=PI, about_point=ORIGIN, run_time=0.4),
        )
        
        # Morph to equation
        self.play(
            ReplacementTransform(VGroup(orbit, sun, planet), equation, run_time=0.6),
        )
        
        self.wait(0.3)


# For testing
if __name__ == "__main__":
    print("Render with:")
    print("  manim -ql intro_v2.py OrbitalIntroV2")
    print("  manim -ql intro_v2.py OrbitalIntroMinimal")
    print("  manim -ql intro_v2.py OrbitalIntroWithText")
    print("  manim -ql intro_v2.py OrbitalIntroOrbitPath")
