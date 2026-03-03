"""Auto-generated OrbitalIntroShort scene — hook: solve this 👇"""
from manim import *
import numpy as np

NEON_VIOLET  = "#A855F7"
NEON_WHITE   = "#FFFFFF"
NEON_BLUE    = "#00D4FF"

class OrbitalIntroShort(Scene):
    def construct(self):
        self.camera.background_color = "#000000"

        # ── Planet ────────────────────────────────────────────────
        planet_layers = VGroup()
        planet_core = Circle(radius=0.55, color=NEON_WHITE, stroke_width=9)
        planet_layers.add(planet_core)
        for r_off, op, w in [(0.03, 0.5, 6), (0.05, 0.25, 4), (0.08, 0.12, 3)]:
            planet_layers.add(Circle(radius=0.55+r_off, color=NEON_WHITE,
                                     stroke_width=w, stroke_opacity=op))
        planet_glow = Circle(radius=0.62, color=NEON_VIOLET, stroke_width=16, stroke_opacity=0.15)

        # ── Rings ─────────────────────────────────────────────────
        def make_ring(w, h, col, sw, op=1.0):
            e = Ellipse(width=w, height=h, color=col, stroke_width=sw, stroke_opacity=op)
            e.rotate(-30 * DEGREES)
            return e

        orbit_rings = VGroup(
            make_ring(2.0, 0.67, NEON_VIOLET, 12, 0.15),
            make_ring(2.1, 0.72, NEON_WHITE,  2,  0.4),
            make_ring(1.95, 0.65, NEON_WHITE, 2.5),
            make_ring(1.8, 0.58,  NEON_BLUE,  2,  0.85),
        )

        # ── Satellite ─────────────────────────────────────────────
        angle = 50 * DEGREES
        sx = 0.98*np.cos(angle)*np.cos(-30*DEGREES) - 0.33*np.sin(angle)*np.sin(-30*DEGREES)
        sy = 0.98*np.cos(angle)*np.sin(-30*DEGREES) + 0.33*np.sin(angle)*np.cos(-30*DEGREES)
        satellite = VGroup(
            Dot([sx,sy,0], radius=0.20, color=NEON_BLUE, fill_opacity=0.25),
            Dot([sx,sy,0], radius=0.13, color=NEON_BLUE, fill_opacity=0.75),
            Dot([sx,sy,0], radius=0.065, color=NEON_WHITE, fill_opacity=1.0),
        )

        logo = VGroup(planet_glow, planet_layers, orbit_rings, satellite)
        logo.move_to(UP * 1.2)

        wordmark = Text("ORBITAL", font_size=80, color=NEON_WHITE,
                        weight=BOLD, font="Arial").set_opacity(0.92)
        wordmark.next_to(logo, DOWN, buff=0.45)

        hook_mob = Text('solve this 👇', font_size=56, color=NEON_WHITE)
        hook_mob.next_to(wordmark, DOWN, buff=0.7)

        # ── Animation ─────────────────────────────────────────────
        self.play(FadeIn(logo, scale=0.8), run_time=0.45)
        self.play(FadeIn(wordmark, shift=UP*0.2), run_time=0.3)
        self.wait(0.2)
        self.play(FadeIn(hook_mob, shift=UP*0.25), run_time=0.3)
        self.wait(1.5)
        self.play(FadeOut(VGroup(logo, wordmark, hook_mob)), run_time=0.2)
