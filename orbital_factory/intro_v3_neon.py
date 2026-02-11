"""
Orbital Intro V3 — NEON Edition with Watermark
===============================================
Glowing neon rings morphing into equation.
Small watermark in corner throughout.
"""

from manim import *

# Neon colors - brighter, more vibrant
NEON_VIOLET = "#A855F7"      # Brighter violet
NEON_PURPLE = "#C084FC"      # Light purple glow
NEON_PINK = "#E879F9"        # Pink accent
NEON_CYAN = "#22D3EE"        # Cyan accent
NEON_WHITE = "#FFFFFF"


def create_glow_circle(radius, color, stroke_width=3, glow_layers=3):
    """Create a circle with neon glow effect."""
    group = VGroup()
    
    # Outer glow layers (progressively larger, more transparent)
    for i in range(glow_layers, 0, -1):
        glow = Circle(
            radius=radius,
            color=color,
            stroke_width=stroke_width + (i * 4),
            stroke_opacity=0.15 / i,
            fill_opacity=0
        )
        group.add(glow)
    
    # Core ring (brightest)
    core = Circle(
        radius=radius,
        color=color,
        stroke_width=stroke_width,
        stroke_opacity=1,
        fill_opacity=0
    )
    group.add(core)
    
    return group


def create_glow_dot(position, color=NEON_WHITE, radius=0.08):
    """Create a dot with glow effect."""
    group = VGroup()
    
    # Outer glow
    for i in range(3, 0, -1):
        glow = Dot(
            point=position,
            radius=radius + (i * 0.04),
            color=color,
            fill_opacity=0.2 / i
        )
        group.add(glow)
    
    # Core dot
    core = Dot(point=position, radius=radius, color=color, fill_opacity=1)
    group.add(core)
    
    return group


class OrbitalIntroNeon(Scene):
    """
    Neon glowing rings morph into equation.
    Watermark in corner throughout.
    """
    
    def construct(self):
        self.camera.background_color = "#000000"
        
        equation_text = getattr(self, 'equation', r"\int x e^{x^2} \, dx")
        
        # === WATERMARK (stays throughout) ===
        watermark = Text(
            "ORBITAL",
            font_size=14,
            color=NEON_WHITE,
            weight=BOLD,
            font="SF Pro Display"  # Falls back to system font
        ).set_opacity(0.4)
        watermark.to_corner(DR, buff=0.3)
        self.add(watermark)
        
        # === NEON RINGS ===
        ring1 = create_glow_circle(0.8, NEON_VIOLET, stroke_width=2.5, glow_layers=4)
        ring2 = create_glow_circle(0.5, NEON_PURPLE, stroke_width=2, glow_layers=3)
        ring3 = create_glow_circle(0.3, NEON_PINK, stroke_width=1.5, glow_layers=2)
        
        # Orbiting dot with glow
        dot = create_glow_dot(ring1[0].point_at_angle(0), NEON_WHITE, radius=0.06)
        
        # All rings grouped
        rings = VGroup(ring1, ring2, ring3)
        
        # === EQUATION ===
        equation = MathTex(equation_text, color=NEON_WHITE)
        equation.scale(1.4)
        
        # Add subtle glow to equation
        equation_glow = equation.copy().set_color(NEON_VIOLET).set_opacity(0.3)
        equation_glow.scale(1.02)
        equation_with_glow = VGroup(equation_glow, equation)
        
        # === ANIMATION SEQUENCE ===
        
        # 1. Draw rings with stagger (0.5s)
        self.play(
            LaggedStart(
                Create(ring1),
                Create(ring2),
                Create(ring3),
                lag_ratio=0.15
            ),
            FadeIn(dot, scale=0.5),
            run_time=0.5
        )
        
        # 2. Orbit + pulse (0.35s)
        self.play(
            Rotate(dot, angle=PI * 0.6, about_point=ORIGIN),
            rings.animate.scale(1.08),
            run_time=0.35,
            rate_func=smooth
        )
        
        # 3. Morph to equation (0.65s)
        self.play(
            ReplacementTransform(rings, equation_with_glow),
            FadeOut(dot, scale=0.5),
            run_time=0.65,
            rate_func=smooth
        )
        
        # 4. Brief hold (0.3s)
        self.wait(0.3)


class OrbitalIntroNeonMinimal(Scene):
    """
    Simpler neon version - single ring.
    """
    
    def construct(self):
        self.camera.background_color = "#000000"
        
        equation_text = getattr(self, 'equation', r"\int x e^{x^2} \, dx")
        
        # Watermark
        watermark = Text("ORBITAL", font_size=14, color=NEON_WHITE).set_opacity(0.4)
        watermark.to_corner(DR, buff=0.3)
        self.add(watermark)
        
        # Single neon ring
        ring = create_glow_circle(0.6, NEON_VIOLET, stroke_width=3, glow_layers=4)
        
        # Center dot
        dot = create_glow_dot(ORIGIN, NEON_WHITE, radius=0.1)
        
        # Equation
        equation = MathTex(equation_text, color=NEON_WHITE).scale(1.4)
        
        # Animate
        self.play(
            Create(ring),
            GrowFromCenter(dot),
            run_time=0.5
        )
        
        self.play(
            ring.animate.scale(1.1),
            run_time=0.2
        )
        
        self.play(
            ReplacementTransform(VGroup(ring, dot), equation),
            run_time=0.6
        )
        
        self.wait(0.3)


class OrbitalIntroNeonPulse(Scene):
    """
    Neon rings with pulse effect before morph.
    Extra dramatic.
    """
    
    def construct(self):
        self.camera.background_color = "#000000"
        
        equation_text = getattr(self, 'equation', r"\int x e^{x^2} \, dx")
        
        # Watermark
        watermark = Text("ORBITAL", font_size=14, color=NEON_WHITE).set_opacity(0.4)
        watermark.to_corner(DR, buff=0.3)
        self.add(watermark)
        
        # Neon rings
        ring1 = create_glow_circle(0.8, NEON_VIOLET, stroke_width=2.5, glow_layers=4)
        ring2 = create_glow_circle(0.5, NEON_CYAN, stroke_width=2, glow_layers=3)
        ring3 = create_glow_circle(0.25, NEON_PINK, stroke_width=1.5, glow_layers=2)
        
        rings = VGroup(ring1, ring2, ring3)
        
        # Equation
        equation = MathTex(equation_text, color=NEON_WHITE).scale(1.4)
        
        # Draw
        self.play(
            LaggedStart(
                Create(ring1),
                Create(ring2),
                Create(ring3),
                lag_ratio=0.1
            ),
            run_time=0.4
        )
        
        # Pulse out then in
        self.play(
            rings.animate.scale(1.3),
            run_time=0.15,
            rate_func=rush_into
        )
        self.play(
            rings.animate.scale(1/1.3),
            run_time=0.15,
            rate_func=rush_from
        )
        
        # Morph
        self.play(
            ReplacementTransform(rings, equation),
            run_time=0.6
        )
        
        self.wait(0.3)


if __name__ == "__main__":
    print("Render with:")
    print("  manim -ql intro_v3_neon.py OrbitalIntroNeon")
    print("  manim -ql intro_v3_neon.py OrbitalIntroNeonMinimal")
    print("  manim -ql intro_v3_neon.py OrbitalIntroNeonPulse")
    print("\nFor high quality:")
    print("  manim -qh intro_v3_neon.py OrbitalIntroNeon")
