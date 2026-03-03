"""
Orbital Outro Short — TikTok/Reels Outro (2 seconds, 9:16)
===========================================================
Quick outro card:
- "ORBITAL" wordmark + logo centered
- CTA text below ("Follow for more" or parameterizable)
- 2 seconds total, clean fade in/hold/fade out

Usage (programmatic):
    from outro_short import build_outro_short_scene
    build_outro_short_scene("my_outro.py", cta="Follow for more")

Usage (direct render):
    manim --config_file manim_short.cfg -ql outro_short.py OrbitalOutroShort
"""

from manim import *
import numpy as np

# ── brand colours ─────────────────────────────────────────────────
NEON_VIOLET  = "#A855F7"
NEON_WHITE   = "#FFFFFF"
NEON_BLUE    = "#00D4FF"
ORBITAL_CYAN = "#22D3EE"

# ── CTA options ────────────────────────────────────────────────────
DEFAULT_CTA = "Follow for more"
CTA_OPTIONS = [
    "Follow for more",
    "Follow @orbital.math",
    "More proofs → follow",
    "Like if that helped 🙌",
    "Comment your answer below",
    "Save this for later 📌",
]


class OrbitalOutroShort(Scene):
    """
    Short-form outro card.
    Set `cta_text` class attribute to customise the call-to-action.
    """

    cta_text: str = DEFAULT_CTA

    def construct(self):
        self.camera.background_color = "#000000"

        cta = getattr(self, "cta_text", DEFAULT_CTA)

        # ── Logo (small, centred high) ─────────────────────────────
        # Planet
        planet_layers = VGroup()
        planet_core = Circle(radius=0.42, color=NEON_WHITE, stroke_width=7)
        planet_layers.add(planet_core)
        for r_off, op, w in [(0.025, 0.5, 5), (0.045, 0.25, 3), (0.07, 0.12, 2)]:
            planet_layers.add(Circle(radius=0.42 + r_off, color=NEON_WHITE,
                                     stroke_width=w, stroke_opacity=op))
        planet_glow = Circle(radius=0.48, color=NEON_VIOLET, stroke_width=14, stroke_opacity=0.18)

        # Rings
        def make_ring(w, h, col, sw, op=1.0):
            e = Ellipse(width=w, height=h, color=col, stroke_width=sw, stroke_opacity=op)
            e.rotate(-30 * DEGREES)
            return e

        orbit_rings = VGroup(
            make_ring(1.55, 0.52, NEON_VIOLET, 10, 0.15),
            make_ring(1.65, 0.56, NEON_WHITE,  2,  0.4),
            make_ring(1.52, 0.50, NEON_WHITE,  2.5),
            make_ring(1.40, 0.45, NEON_BLUE,   2,  0.85),
        )

        # Satellite
        angle = 50 * DEGREES
        sx = 0.76 * np.cos(angle) * np.cos(-30 * DEGREES) - 0.26 * np.sin(angle) * np.sin(-30 * DEGREES)
        sy = 0.76 * np.cos(angle) * np.sin(-30 * DEGREES) + 0.26 * np.sin(angle) * np.cos(-30 * DEGREES)
        satellite = VGroup(
            Dot([sx, sy, 0], radius=0.15, color=NEON_BLUE, fill_opacity=0.25),
            Dot([sx, sy, 0], radius=0.10, color=NEON_BLUE, fill_opacity=0.75),
            Dot([sx, sy, 0], radius=0.05, color=NEON_WHITE, fill_opacity=1.0),
        )

        logo = VGroup(planet_glow, planet_layers, orbit_rings, satellite)
        logo.move_to(UP * 1.5)

        # ── Wordmark ───────────────────────────────────────────────
        wordmark = Text("ORBITAL", font_size=88, color=NEON_WHITE,
                        weight=BOLD, font="Arial").set_opacity(0.95)
        wordmark.next_to(logo, DOWN, buff=0.35)

        # ── CTA ────────────────────────────────────────────────────
        cta_mob = Text(cta, font_size=44, color=ORBITAL_CYAN)
        cta_mob.next_to(wordmark, DOWN, buff=0.55)

        # Subtle divider line
        divider = Line(LEFT * 2.5, RIGHT * 2.5, color=WHITE, stroke_width=1, stroke_opacity=0.3)
        divider.next_to(wordmark, DOWN, buff=0.2)
        cta_mob.next_to(divider, DOWN, buff=0.25)

        full_card = VGroup(logo, wordmark, divider, cta_mob)

        # ── Animate (2 seconds total) ──────────────────────────────
        # 0.0–0.4s: fade in
        self.play(FadeIn(full_card, scale=0.92), run_time=0.4)

        # 0.4–1.6s: hold
        self.wait(1.2)

        # 1.6–2.0s: fade out
        self.play(FadeOut(full_card), run_time=0.4)


# ─────────────────────────────────────────────────────────────────
#  Programmatic builder (used by pipeline_short.py)
# ─────────────────────────────────────────────────────────────────

def build_outro_short_scene(output_path: str, cta: str = None) -> str:
    """
    Write a self-contained outro scene .py file for pipeline rendering.

    Args:
        output_path : Where to write the .py file.
        cta         : Call-to-action text. Defaults to "Follow for more".

    Returns:
        output_path
    """
    cta = cta or DEFAULT_CTA

    scene_code = f'''"""Auto-generated OrbitalOutroShort scene."""
from manim import *
import numpy as np

NEON_VIOLET  = "#A855F7"
NEON_WHITE   = "#FFFFFF"
NEON_BLUE    = "#00D4FF"
ORBITAL_CYAN = "#22D3EE"

class OrbitalOutroShort(Scene):
    def construct(self):
        self.camera.background_color = "#000000"

        planet_layers = VGroup()
        planet_core = Circle(radius=0.42, color=NEON_WHITE, stroke_width=7)
        planet_layers.add(planet_core)
        for r_off, op, w in [(0.025, 0.5, 5), (0.045, 0.25, 3), (0.07, 0.12, 2)]:
            planet_layers.add(Circle(radius=0.42+r_off, color=NEON_WHITE,
                                     stroke_width=w, stroke_opacity=op))
        planet_glow = Circle(radius=0.48, color=NEON_VIOLET, stroke_width=14, stroke_opacity=0.18)

        def make_ring(w, h, col, sw, op=1.0):
            e = Ellipse(width=w, height=h, color=col, stroke_width=sw, stroke_opacity=op)
            e.rotate(-30 * DEGREES)
            return e

        orbit_rings = VGroup(
            make_ring(1.55, 0.52, NEON_VIOLET, 10, 0.15),
            make_ring(1.65, 0.56, NEON_WHITE,  2,  0.4),
            make_ring(1.52, 0.50, NEON_WHITE,  2.5),
            make_ring(1.40, 0.45, NEON_BLUE,   2,  0.85),
        )

        angle = 50 * DEGREES
        sx = 0.76*np.cos(angle)*np.cos(-30*DEGREES) - 0.26*np.sin(angle)*np.sin(-30*DEGREES)
        sy = 0.76*np.cos(angle)*np.sin(-30*DEGREES) + 0.26*np.sin(angle)*np.cos(-30*DEGREES)
        satellite = VGroup(
            Dot([sx,sy,0], radius=0.15, color=NEON_BLUE, fill_opacity=0.25),
            Dot([sx,sy,0], radius=0.10, color=NEON_BLUE, fill_opacity=0.75),
            Dot([sx,sy,0], radius=0.05, color=NEON_WHITE, fill_opacity=1.0),
        )

        logo = VGroup(planet_glow, planet_layers, orbit_rings, satellite)
        logo.move_to(UP * 1.5)

        wordmark = Text("ORBITAL", font_size=88, color=NEON_WHITE,
                        weight=BOLD, font="Arial").set_opacity(0.95)
        wordmark.next_to(logo, DOWN, buff=0.35)

        divider = Line(LEFT*2.5, RIGHT*2.5, color=WHITE, stroke_width=1, stroke_opacity=0.3)
        divider.next_to(wordmark, DOWN, buff=0.2)

        cta_mob = Text({repr(cta)}, font_size=44, color=ORBITAL_CYAN)
        cta_mob.next_to(divider, DOWN, buff=0.25)

        full_card = VGroup(logo, wordmark, divider, cta_mob)

        self.play(FadeIn(full_card, scale=0.92), run_time=0.4)
        self.wait(1.2)
        self.play(FadeOut(full_card), run_time=0.4)
'''

    with open(output_path, "w") as fh:
        fh.write(scene_code)

    return output_path


if __name__ == "__main__":
    print("Render with:")
    print("  manim --config_file manim_short.cfg -ql outro_short.py OrbitalOutroShort")
