"""Auto-generated OrbitalIntroShort scene — hook: solve this 👇"""
from manim import *
import numpy as np

config.frame_width = 4.5
config.frame_height = 8.0

NEON_VIOLET  = "#A855F7"
NEON_WHITE   = "#FFFFFF"
NEON_BLUE    = "#00D4FF"

class OrbitalIntroShort(Scene):
    def construct(self):
        self.camera.background_color = "#000000"

        # ── Planet (scaled for 4.5-wide frame) ────────────────────
        planet_layers = VGroup()
        planet_core = Circle(radius=0.35, color=NEON_WHITE, stroke_width=6)
        planet_layers.add(planet_core)
        for r_off, op, w in [(0.02, 0.5, 4), (0.04, 0.25, 3), (0.06, 0.12, 2)]:
            planet_layers.add(Circle(radius=0.35+r_off, color=NEON_WHITE,
                                     stroke_width=w, stroke_opacity=op))
        planet_glow = Circle(radius=0.42, color=NEON_VIOLET, stroke_width=10, stroke_opacity=0.15)

        # ── Rings ─────────────────────────────────────────────────
        def make_ring(w, h, col, sw, op=1.0):
            e = Ellipse(width=w, height=h, color=col, stroke_width=sw, stroke_opacity=op)
            e.rotate(-30 * DEGREES)
            return e

        orbit_rings = VGroup(
            make_ring(1.3, 0.44, NEON_VIOLET, 8, 0.15),
            make_ring(1.4, 0.47, NEON_WHITE,  1.5, 0.4),
            make_ring(1.28, 0.43, NEON_WHITE, 2),
            make_ring(1.18, 0.38, NEON_BLUE,  1.5, 0.85),
        )

        # ── Satellite ─────────────────────────────────────────────
        angle = 50 * DEGREES
        sx = 0.64*np.cos(angle)*np.cos(-30*DEGREES) - 0.22*np.sin(angle)*np.sin(-30*DEGREES)
        sy = 0.64*np.cos(angle)*np.sin(-30*DEGREES) + 0.22*np.sin(angle)*np.cos(-30*DEGREES)
        satellite = VGroup(
            Dot([sx,sy,0], radius=0.13, color=NEON_BLUE, fill_opacity=0.25),
            Dot([sx,sy,0], radius=0.085, color=NEON_BLUE, fill_opacity=0.75),
            Dot([sx,sy,0], radius=0.04, color=NEON_WHITE, fill_opacity=1.0),
        )

        logo = VGroup(planet_glow, planet_layers, orbit_rings, satellite)
        logo.move_to(UP * 1.0)

        wordmark = Text("ORBITAL", font_size=36, color=NEON_WHITE,
                        weight=BOLD, font="Arial").set_opacity(0.92)
        wordmark.next_to(logo, DOWN, buff=0.3)

        hook_mob = Text('solve this 👇', font_size=24, color=NEON_WHITE)
        hook_mob.next_to(wordmark, DOWN, buff=0.5)

        # ── Animation ─────────────────────────────────────────────
        self.play(FadeIn(logo, scale=0.8), run_time=0.45)
        self.play(FadeIn(wordmark, shift=UP*0.15), run_time=0.3)
        self.wait(0.2)
        self.play(FadeIn(hook_mob, shift=UP*0.15), run_time=0.3)
        self.wait(1.5)
        self.play(FadeOut(VGroup(logo, wordmark, hook_mob)), run_time=0.2)
