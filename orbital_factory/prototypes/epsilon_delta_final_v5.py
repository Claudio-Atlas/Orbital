"""
Epsilon-Delta — FINAL v5
========================
Built to match the EXACT style of the proven pipeline videos.
Uses: scene-based TTS, DUR timing model, purple boxes, planet end card.
Background music added via ffmpeg post-render.

Render:
  cd ~/Desktop/Orbital/orbital_factory && source venv/bin/activate
  PATH="/Library/TeX/texbin:$PATH" manim render prototypes/epsilon_delta_final_v5.py EpsilonDeltaFinalV5 \
    -o epsilon_delta_final_v5.mp4 --format mp4 -r 1080,1920 --frame_rate 60 --flush_cache
"""
from manim import *
import numpy as np
import json, os

config.frame_width = 4.5
config.frame_height = 8.0

# ── Constants from pipeline ──
VIOLET = "#8B5CF6"
CYAN = "#22D3EE"
GREEN = "#39FF14"
ORANGE = "#F97316"
BOX_BORDER = "#8B5CF6"
BOX_FILL = "#1a1130"
LABEL_COLOR = "#22D3EE"

FRAME_W = 4.5
FRAME_H = 8.0
MAX_WIDTH = FRAME_W * 0.82
MATH_SCALE = 0.85
BOX_SCALE = 0.65
MATH_CENTER_Y = 1.2
GRAPH_CENTER_Y = -1.8
GRAPH_WIDTH = 3.4
GRAPH_HEIGHT = 2.8
ANIMATION_RATIO = 0.35
EXTRA_HOLD = 0.8

# ── Load scene-based audio manifest ──
with open("output/tts/epsilon_delta_scenes/manifest.json") as f:
    _manifest = json.load(f)
    MANIFEST = {s["scene"]: s for s in _manifest}

def AUDIO(scene):
    return MANIFEST[scene]["audio_path"]

def DUR(scene):
    return MANIFEST[scene]["duration"]

def _clamp(mob, max_w=None):
    if max_w is None:
        max_w = MAX_WIDTH
    if mob.width > max_w:
        mob.scale(max_w / mob.width)
    return mob

def _make_box(content_tex, label_text=None):
    """Build a purple-bordered box with MathTex inside (pipeline style)."""
    inner = MathTex(content_tex, color=WHITE).scale(BOX_SCALE)
    _clamp(inner, MAX_WIDTH * 0.75)
    box = SurroundingRectangle(
        inner, color=BOX_BORDER, fill_color=BOX_FILL,
        fill_opacity=0.6, buff=0.2, corner_radius=0.1, stroke_width=2,
    )
    if label_text:
        lbl = Text(label_text, color=LABEL_COLOR, font_size=14)
        lbl.next_to(box, UP, buff=0.1)
        return VGroup(box, lbl, inner)
    return VGroup(box, inner)

def _make_text_box(text_str, label_text=None):
    """Build a purple-bordered box with plain Text inside."""
    inner = Text(text_str, font_size=22, color=WHITE, line_spacing=1.3)
    _clamp(inner, MAX_WIDTH * 0.75)
    box = SurroundingRectangle(
        inner, color=BOX_BORDER, fill_color=BOX_FILL,
        fill_opacity=0.6, buff=0.25, corner_radius=0.1, stroke_width=2,
    )
    if label_text:
        lbl = Text(label_text, color=LABEL_COLOR, font_size=14)
        lbl.next_to(box, UP, buff=0.1)
        return VGroup(box, lbl, inner)
    return VGroup(box, inner)


class EpsilonDeltaFinalV5(Scene):
    def construct(self):
        self.camera.background_color = BLACK

        # ── Persistent chrome (exact pipeline style) ──
        border = Rectangle(
            width=FRAME_W - 0.15, height=FRAME_H - 0.15,
            color=VIOLET, stroke_width=2.5, stroke_opacity=0.7, fill_opacity=0,
        )
        border_glow = Rectangle(
            width=FRAME_W - 0.10, height=FRAME_H - 0.10,
            color=VIOLET, stroke_width=6, stroke_opacity=0.15, fill_opacity=0,
        )
        self.add(border_glow, border)

        wm = Text("ORBITAL", font_size=10, color=WHITE, weight=BOLD).set_opacity(0.35)
        wm.move_to([-FRAME_W/2 + 0.5, -FRAME_H/2 + 0.2, 0])
        self.add(wm)

        # ── Shared math ──
        fn = lambda x: x**2
        a_val = 2.0
        L_val = 4.0

        def get_delta(e):
            lo = max(0.0, L_val - e)
            hi = L_val + e
            d = min(a_val - np.sqrt(lo), np.sqrt(hi) - a_val)
            return max(d, 0.005)

        previous = None  # Track previous mobject for FadeOut transitions

        # ═══ STEP 1: HOOK ═════════════════════════════════════════════
        # Show scary definition in a box
        mob = _make_box(
            r"\forall\,\varepsilon>0,\;\exists\,\delta>0:\;"
            r"|x-a|<\delta\;\Rightarrow\;|f(x)-L|<\varepsilon",
            label_text="epsilon-delta"
        )
        mob.move_to([0, MATH_CENTER_Y, 0])

        duration = DUR("hook")
        anim_time = max(1.2, duration * ANIMATION_RATIO)

        self.add_sound(AUDIO("hook"))
        self.play(Write(mob), run_time=anim_time)
        self.wait(max(0.3, duration - anim_time))
        self.wait(EXTRA_HOLD)
        previous = mob

        # ═══ STEP 2: SETUP — graph + limit question ══════════════════
        # Build graph
        axes = Axes(
            x_range=[-0.3, 4.0, 1], y_range=[-0.5, 6.5, 1],
            x_length=GRAPH_WIDTH, y_length=GRAPH_HEIGHT,
            axis_config={"color": GREY_B, "include_numbers": True,
                         "font_size": 12, "numbers_to_exclude": [0]},
            tips=False,
        )
        grid = NumberPlane(
            x_range=[-0.3, 4.0, 1], y_range=[-0.5, 6.5, 1],
            x_length=GRAPH_WIDTH, y_length=GRAPH_HEIGHT,
            background_line_style={"stroke_color": VIOLET, "stroke_opacity": 0.25,
                                   "stroke_width": 1},
            faded_line_style={"stroke_color": CYAN, "stroke_opacity": 0.12,
                              "stroke_width": 0.5},
        )
        grid.move_to(axes.get_center())
        curve = axes.plot(fn, x_range=[0, 2.5], color=CYAN, stroke_width=2.5)
        limit_dot = Dot(axes.c2p(a_val, L_val), color=GREEN, radius=0.06)

        a_label = MathTex("x = 2", font_size=14, color=GREEN)
        L_label = MathTex("y = 4", font_size=14, color=GREEN)

        graph_mob = VGroup(grid, axes, curve, limit_dot)
        graph_mob.move_to([0, 0, 0])  # Center first (hero moment)

        duration = DUR("setup")
        anim_time = max(1.2, duration * ANIMATION_RATIO)

        self.add_sound(AUDIO("setup"))

        # FadeOut previous
        self.play(FadeOut(previous, shift=UP * 0.3), run_time=0.4)

        # Show graph centered first
        self.play(FadeIn(VGroup(grid, axes)), run_time=anim_time * 0.3)
        self.play(Create(curve), FadeIn(limit_dot), run_time=anim_time * 0.5)

        # Hold center briefly
        self.wait(1.0)

        # Slide graph down to persistent position
        a_label.next_to(axes.c2p(a_val, 0), DOWN, buff=0.1)
        L_label.next_to(axes.c2p(0, L_val), LEFT, buff=0.08)
        self.play(
            graph_mob.animate.move_to([0, GRAPH_CENTER_Y, 0]),
            run_time=0.8
        )
        # Labels need repositioning after graph moves
        a_label.next_to(axes.c2p(a_val, 0), DOWN, buff=0.1)
        L_label.next_to(axes.c2p(0, L_val), LEFT, buff=0.08)
        self.play(Write(a_label), Write(L_label), run_time=0.3)

        remaining = max(0.3, duration - anim_time - 0.4 - 1.0 - 0.8 - 0.3)
        self.wait(remaining)
        self.wait(EXTRA_HOLD)
        previous = None  # Graph stays, no previous to track

        # ═══ STEP 3: EPSILON BAND ════════════════════════════════════
        eps_val = ValueTracker(1.2)

        def make_eps_band():
            e = eps_val.get_value()
            y_lo = axes.c2p(0, L_val - e)[1]
            y_hi = axes.c2p(0, L_val + e)[1]
            x_left = axes.c2p(-0.3, 0)[0]
            x_right = axes.c2p(4.0, 0)[0]
            band = Rectangle(
                width=x_right - x_left, height=y_hi - y_lo,
                color=ORANGE, fill_opacity=0.15, stroke_width=0
            )
            band.move_to([(x_left + x_right)/2, (y_lo + y_hi)/2, 0])
            top = DashedLine([x_left, y_hi, 0], [x_right, y_hi, 0],
                             color=ORANGE, stroke_width=2, dash_length=0.06)
            bot = DashedLine([x_left, y_lo, 0], [x_right, y_lo, 0],
                             color=ORANGE, stroke_width=2, dash_length=0.06)
            return VGroup(band, top, bot)

        eps_band = always_redraw(make_eps_band)
        eps_label = always_redraw(lambda: MathTex(
            r"\varepsilon", font_size=20, color=ORANGE
        ).next_to(axes.c2p(-0.2, L_val + eps_val.get_value()), LEFT, buff=0.05))

        # Text box for this step
        eps_box = _make_text_box("Target zone: epsilon (ε)")
        eps_box.move_to([0, MATH_CENTER_Y, 0])

        duration = DUR("epsilon")
        anim_time = max(1.2, duration * ANIMATION_RATIO)

        self.add_sound(AUDIO("epsilon"))
        self.play(Write(eps_box), run_time=0.6)
        self.play(FadeIn(eps_band), Write(eps_label), run_time=0.8)

        # Trace dot
        trace_dot = Dot(axes.c2p(1.5, fn(1.5)), color=WHITE, radius=0.04)
        self.play(FadeIn(trace_dot), run_time=0.2)
        self.play(MoveAlongPath(trace_dot, axes.plot(fn, x_range=[1.5, 2.0]),
                                rate_func=smooth), run_time=1.2)
        self.play(FadeOut(trace_dot), run_time=0.2)

        remaining = max(0.3, duration - 0.6 - 0.8 - 0.2 - 1.2 - 0.2)
        self.wait(remaining)
        self.wait(EXTRA_HOLD)
        previous = eps_box

        # ═══ STEP 4: DELTA BAND ══════════════════════════════════════
        def make_delta_band():
            e = eps_val.get_value()
            d = get_delta(e)
            x_lo = axes.c2p(a_val - d, 0)[0]
            x_hi = axes.c2p(a_val + d, 0)[0]
            y_bot = axes.c2p(0, -0.5)[1]
            y_top = axes.c2p(0, 6.5)[1]
            band = Rectangle(
                width=x_hi - x_lo, height=y_top - y_bot,
                color=CYAN, fill_opacity=0.12, stroke_width=0
            )
            band.move_to([(x_lo + x_hi)/2, (y_bot + y_top)/2, 0])
            left = DashedLine([x_lo, y_bot, 0], [x_lo, y_top, 0],
                              color=CYAN, stroke_width=2, dash_length=0.06)
            right = DashedLine([x_hi, y_bot, 0], [x_hi, y_top, 0],
                               color=CYAN, stroke_width=2, dash_length=0.06)
            return VGroup(band, left, right)

        delta_band = always_redraw(make_delta_band)
        delta_label = always_redraw(lambda: MathTex(
            r"\delta", font_size=20, color=CYAN
        ).move_to(axes.c2p(a_val + get_delta(eps_val.get_value()) + 0.15, -0.3)))

        delta_box = _make_text_box("Closeness zone: delta (δ)")
        delta_box.move_to([0, MATH_CENTER_Y, 0])

        duration = DUR("delta")
        anim_time = max(1.2, duration * ANIMATION_RATIO)

        self.add_sound(AUDIO("delta"))
        self.play(FadeOut(previous, shift=UP * 0.3), run_time=0.4)
        self.play(Write(delta_box), run_time=0.6)
        self.play(FadeIn(delta_band), Write(delta_label), run_time=0.8)

        remaining = max(0.3, duration - 0.4 - 0.6 - 0.8)
        self.wait(remaining)
        self.wait(EXTRA_HOLD)
        previous = delta_box

        # ═══ STEP 5: THE GAME ════════════════════════════════════════
        game_box = _make_text_box("The game: you shrink ε,\nI find a δ that works.")
        game_box.move_to([0, MATH_CENTER_Y, 0])

        duration = DUR("game")
        anim_time = max(1.2, duration * ANIMATION_RATIO)

        self.add_sound(AUDIO("game"))
        self.play(FadeOut(previous, shift=UP * 0.3), run_time=0.4)
        self.play(Write(game_box), run_time=anim_time)

        remaining = max(0.3, duration - 0.4 - anim_time)
        self.wait(remaining)
        self.wait(EXTRA_HOLD)
        previous = game_box

        # ═══ STEP 6: SMALLER SEQUENCE ════════════════════════════════
        steps = [0.75, 0.45, 0.22, 0.10]
        duration = DUR("smaller")

        self.add_sound(AUDIO("smaller"))
        self.play(FadeOut(previous, shift=UP * 0.3), run_time=0.4)

        # Show "Smaller" in a box that pulses
        smaller_box = _make_text_box("Smaller...")
        smaller_box.move_to([0, MATH_CENTER_Y, 0])
        self.play(Write(smaller_box), run_time=0.5)

        total_shrink_time = 0
        for target in steps:
            self.play(eps_val.animate.set_value(target), run_time=0.9, rate_func=smooth)
            total_shrink_time += 0.9

        remaining = max(0.3, duration - 0.4 - 0.5 - total_shrink_time)
        self.wait(remaining)
        self.wait(EXTRA_HOLD)
        previous = smaller_box

        # ═══ STEP 7: THE PROOF ═══════════════════════════════════════
        proof_box = _make_text_box("No matter how small ε gets...\nδ always has an answer.\nThe limit is real.")
        proof_box.move_to([0, MATH_CENTER_Y, 0])

        duration = DUR("proof")
        anim_time = max(1.2, duration * ANIMATION_RATIO)

        self.add_sound(AUDIO("proof"))
        self.play(FadeOut(previous, shift=UP * 0.3), run_time=0.4)

        # Final dramatic shrink
        self.play(eps_val.animate.set_value(0.03), run_time=1.2, rate_func=smooth)
        self.play(Write(proof_box), run_time=anim_time)
        self.play(Flash(limit_dot.get_center(), color=GREEN,
                        num_lines=12, flash_radius=0.3), run_time=0.5)

        remaining = max(0.3, duration - 0.4 - 1.2 - anim_time - 0.5)
        self.wait(remaining)
        self.wait(EXTRA_HOLD)
        previous = proof_box

        # ═══ STEP 8: PAYOFF ══════════════════════════════════════════
        payoff_box = _make_box(
            r"\lim_{x \to a} f(x) = L",
            label_text="That's a limit."
        )
        payoff_box.move_to([0, MATH_CENTER_Y, 0])

        duration = DUR("payoff")
        anim_time = max(1.2, duration * ANIMATION_RATIO)

        self.add_sound(AUDIO("payoff"))
        self.play(FadeOut(previous, shift=UP * 0.3), run_time=0.4)
        self.play(Write(payoff_box), run_time=anim_time)

        remaining = max(0.3, duration - 0.4 - anim_time)
        self.wait(remaining)

        # ═══ END CARD — Green highlight then planet logo ═════════════
        # Green box around final content (pipeline pattern)
        green_box = SurroundingRectangle(
            payoff_box, color=GREEN, buff=0.2,
            stroke_width=3, corner_radius=0.08,
        )
        self.play(Create(green_box), run_time=0.5)
        self.wait(1.5)

        # Clear everything
        # Freeze updaters before removing
        eps_band_static = make_eps_band()
        delta_band_static = make_delta_band()
        eps_label_static = eps_label.copy()
        delta_label_static = delta_label.copy()
        self.remove(eps_band, delta_band, eps_label, delta_label)
        self.add(eps_band_static, delta_band_static, eps_label_static, delta_label_static)

        self.play(
            FadeOut(payoff_box), FadeOut(green_box),
            FadeOut(graph_mob), FadeOut(a_label), FadeOut(L_label),
            FadeOut(eps_band_static), FadeOut(delta_band_static),
            FadeOut(eps_label_static), FadeOut(delta_label_static),
            run_time=0.4
        )

        # ── Orbital Lissajous End Card (current logo) ──
        _A, _B = 1.2, 0.95
        liss_glow = ParametricFunction(
            lambda t: np.array([_A*np.sin(3*t), _B*np.sin(2*t), 0]),
            t_range=[0, TAU, 0.02],
            color="#00E5FF", stroke_width=8, stroke_opacity=0.2
        )
        liss_core = ParametricFunction(
            lambda t: np.array([_A*np.sin(3*t), _B*np.sin(2*t), 0]),
            t_range=[0, TAU, 0.02],
            color="#00E5FF", stroke_width=2, stroke_opacity=1.0
        )
        logo = VGroup(liss_glow, liss_core)
        logo.move_to([0, 0.5, 0])

        wordmark = Text("ORBITAL", font_size=22, color="#00E5FF", weight=BOLD)
        wordmark.next_to(logo, DOWN, buff=0.3)
        wm_glow = wordmark.copy().set_opacity(0.3).scale(1.05)

        end_card = VGroup(logo, wm_glow, wordmark)
        end_card.move_to([0, 0, 0])

        self.play(Create(liss_core, run_time=0.8), FadeIn(liss_glow, run_time=0.6))
        self.play(FadeIn(VGroup(wm_glow, wordmark), shift=UP*0.2), run_time=0.4)
        self.wait(1.2)
        self.play(FadeOut(end_card), run_time=0.3)
