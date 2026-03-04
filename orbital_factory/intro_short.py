"""
Orbital Intro Short — TikTok/Reels Logo Intro (2–3 seconds, 9:16)
===================================================================
Quick-fire version of intro_v4_logo.py for short-form video:
- Planet + ring + satellite animates in quickly (~0.5s)
- "ORBITAL" text fades in below (~0.3s)
- Hook text overlays in clean white at 1s, holds for 1.5s
- Total duration: ~2.5 seconds

Hook is a parameter so we can rotate from HOOKS pool.

Usage (programmatic):
    from intro_short import build_intro_short_scene
    build_intro_short_scene("my_intro.py", hook="solve this 👇")

Usage (direct render):
    manim --config_file manim_short.cfg -ql intro_short.py OrbitalIntroShort
"""

from manim import *
import numpy as np

# ── brand colours ─────────────────────────────────────────────────
NEON_VIOLET  = "#A855F7"
NEON_PURPLE  = "#C084FC"
NEON_WHITE   = "#FFFFFF"
NEON_BLUE    = "#00D4FF"
ORBITAL_CYAN = "#22D3EE"

# ── hook copy pool ─────────────────────────────────────────────────
HOOKS = [
    "solve this 👇",
    "how fast can you solve this?",
    "pause and try this first",
    "this one's sneaky",
    "most students get this wrong",
    "speed round 🏎️",
    "no calculator allowed",
]


def _build_logo() -> VGroup:
    """Build the Orbital logo as a VGroup (planet + rings + satellite)."""
    # Planet layers (3D depth effect)
    planet_layers = VGroup()
    planet_core = Circle(radius=0.55, color=NEON_WHITE, stroke_width=9)
    planet_layers.add(planet_core)
    for r_offset, opacity, width in [(0.03, 0.5, 6), (0.05, 0.25, 4), (0.08, 0.12, 3)]:
        glow = Circle(radius=0.55 + r_offset, color=NEON_WHITE,
                      stroke_width=width, stroke_opacity=opacity)
        planet_layers.add(glow)

    planet_glow = Circle(radius=0.62, color=NEON_VIOLET, stroke_width=16, stroke_opacity=0.15)

    # Orbital rings (tilted -30°, layered)
    orbit_outer = Ellipse(width=2.1, height=0.72, color=NEON_WHITE,
                          stroke_width=2, stroke_opacity=0.4)
    orbit_outer.rotate(-30 * DEGREES)

    orbit_ring  = Ellipse(width=1.95, height=0.65, color=NEON_WHITE, stroke_width=2.5)
    orbit_ring.rotate(-30 * DEGREES)

    orbit_inner = Ellipse(width=1.8, height=0.58, color=NEON_BLUE,
                          stroke_width=2, stroke_opacity=0.85)
    orbit_inner.rotate(-30 * DEGREES)

    orbit_glow  = Ellipse(width=2.0, height=0.67, color=NEON_VIOLET,
                          stroke_width=12, stroke_opacity=0.15)
    orbit_glow.rotate(-30 * DEGREES)

    orbit_rings = VGroup(orbit_glow, orbit_outer, orbit_ring, orbit_inner)

    # Satellite
    angle = 50 * DEGREES
    sat_x = 0.98 * np.cos(angle) * np.cos(-30 * DEGREES) - 0.33 * np.sin(angle) * np.sin(-30 * DEGREES)
    sat_y = 0.98 * np.cos(angle) * np.sin(-30 * DEGREES) + 0.33 * np.sin(angle) * np.cos(-30 * DEGREES)

    sat_outer = Dot(point=[sat_x, sat_y, 0], radius=0.20, color=NEON_BLUE, fill_opacity=0.25)
    sat_blue  = Dot(point=[sat_x, sat_y, 0], radius=0.13, color=NEON_BLUE, fill_opacity=0.75)
    sat_white = Dot(point=[sat_x, sat_y, 0], radius=0.065, color=NEON_WHITE, fill_opacity=1.0)
    satellite = VGroup(sat_outer, sat_blue, sat_white)

    logo = VGroup(planet_glow, planet_layers, orbit_rings, satellite)
    return logo


class OrbitalIntroShort(Scene):
    """
    Short-form logo intro for TikTok/Reels.
    Render with manim_short.cfg for 9:16 output.

    Parameters (set as class attributes before rendering):
        hook_text : str  — overlay text (default: random from HOOKS)
    """

    hook_text: str = HOOKS[0]

    def construct(self):
        self.camera.background_color = "#000000"

        hook = getattr(self, "hook_text", HOOKS[0])

        # ── Build logo ─────────────────────────────────────────────
        logo = _build_logo()
        logo.move_to(UP * 1.2)

        # ── "ORBITAL" wordmark ─────────────────────────────────────
        wordmark = Text("ORBITAL", font_size=80, color=NEON_WHITE,
                        weight=BOLD, font="Arial")
        wordmark.set_opacity(0.92)
        wordmark.next_to(logo, DOWN, buff=0.45)

        # ── Hook text overlay ──────────────────────────────────────
        # Placed below wordmark in the safe zone — clean white
        hook_mob = Text(hook, font_size=56, color=NEON_WHITE)
        hook_mob.next_to(wordmark, DOWN, buff=0.7)

        # ── Animate ────────────────────────────────────────────────

        # 0.0–0.5s: Logo pops in + planet draws
        self.play(
            FadeIn(logo, scale=0.8),
            run_time=0.45,
        )

        # 0.5–0.8s: "ORBITAL" fades up
        self.play(
            FadeIn(wordmark, shift=UP * 0.2),
            run_time=0.3,
        )

        # 0.8–1.0s: brief breathe
        self.wait(0.2)

        # 1.0–1.3s: hook text slides up
        self.play(
            FadeIn(hook_mob, shift=UP * 0.25),
            run_time=0.3,
        )

        # 1.3–2.8s: hold so viewer reads the hook
        self.wait(1.5)

        # 2.8–3.0s: fade out
        self.play(
            FadeOut(VGroup(logo, wordmark, hook_mob)),
            run_time=0.2,
        )


# ─────────────────────────────────────────────────────────────────
#  Programmatic builder (used by pipeline_short.py)
# ─────────────────────────────────────────────────────────────────

def build_intro_short_scene(output_path: str, hook: str = None) -> str:
    """
    Write a self-contained intro scene .py file that can be rendered
    by the pipeline without needing to import this module at render time.

    Args:
        output_path : Where to write the .py file.
        hook        : Hook text string. Random if None.

    Returns:
        output_path (for chaining)
    """
    import random
    hook = hook or random.choice(HOOKS)

    scene_code = f'''"""Auto-generated OrbitalIntroShort scene — hook: {hook}"""
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

        hook_mob = Text({repr(hook)}, font_size=24, color=NEON_WHITE)
        hook_mob.next_to(wordmark, DOWN, buff=0.5)

        # ── Animation ─────────────────────────────────────────────
        self.play(FadeIn(logo, scale=0.8), run_time=0.45)
        self.play(FadeIn(wordmark, shift=UP*0.15), run_time=0.3)
        self.wait(0.2)
        self.play(FadeIn(hook_mob, shift=UP*0.15), run_time=0.3)
        self.wait(1.5)
        self.play(FadeOut(VGroup(logo, wordmark, hook_mob)), run_time=0.2)
'''

    with open(output_path, "w") as fh:
        fh.write(scene_code)

    return output_path


if __name__ == "__main__":
    import sys
    hook = sys.argv[1] if len(sys.argv) > 1 else HOOKS[0]
    print(f"Hook: {hook!r}")
    print("Render with:")
    print("  manim --config_file manim_short.cfg -ql intro_short.py OrbitalIntroShort")
