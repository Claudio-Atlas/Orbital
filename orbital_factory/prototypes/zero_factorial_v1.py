"""
Why is 0! = 1? — Shorts Prototype v1
======================================
Custom prototype following L'Hôpital visual spec exactly.
Scene-based TTS (Allison, locked settings).

Render:
  cd ~/Desktop/Orbital/orbital_factory && source venv/bin/activate
  PATH="/Library/TeX/texbin:$PATH" manim render prototypes/zero_factorial_v1.py ZeroFactorialV1 \
    -o zero_factorial_v1.mp4 --format mp4 -r 1080,1920 --frame_rate 60 --flush_cache
"""
from manim import *
from itertools import permutations
import numpy as np
import json, os

config.frame_width = 4.5
config.frame_height = 8.0

# ── LOCKED VISUAL SPEC (from orbital-visual-spec-locked.md) ──
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
EXTRA_HOLD = 0.5
ANIMATION_RATIO = 0.35

# ── LOAD TTS MANIFEST ──
with open("output/tts/zero_factorial_scenes/manifest.json") as f:
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
    inner = MathTex(content_tex, color=WHITE).scale(BOX_SCALE)
    _clamp(inner, MAX_WIDTH * 0.85)
    box_rect = SurroundingRectangle(
        inner, color=BOX_BORDER, fill_color=BOX_FILL,
        fill_opacity=0.6, buff=0.2, corner_radius=0.1, stroke_width=2,
    )
    if label_text:
        lbl = Text(label_text, color=LABEL_COLOR, font_size=14)
        lbl.next_to(box_rect, UP, buff=0.1)
        return VGroup(box_rect, lbl, inner)
    return VGroup(box_rect, inner)


class ZeroFactorialV1(Scene):
    def construct(self):
        self.camera.background_color = BLACK
        t = 0  # time tracker for reference only

        # ── PERSISTENT ELEMENTS ──
        border = Rectangle(
            width=FRAME_W - 0.15, height=FRAME_H - 0.15,
            color=VIOLET, stroke_width=2.5, stroke_opacity=0.7,
            fill_opacity=0,
        ).move_to(ORIGIN)
        border_glow = Rectangle(
            width=FRAME_W - 0.10, height=FRAME_H - 0.10,
            color=VIOLET, stroke_width=6, stroke_opacity=0.15,
            fill_opacity=0,
        ).move_to(ORIGIN)
        self.add(border_glow, border)

        wm = Text("ORBITAL", font_size=10, color=WHITE, weight=BOLD)
        wm.set_opacity(0.35)
        wm.move_to([-FRAME_W/2 + 0.5, -FRAME_H/2 + 0.2, 0])
        self.add(wm)

        previous = None

        # ═══════════════════════════════════════════════════════════
        # SCENE 1: HOOK — "Why does 0! = 1?"
        # ═══════════════════════════════════════════════════════════
        dur = DUR("hook")
        anim_time = max(1.2, dur * ANIMATION_RATIO)

        mob1 = MathTex(r"0! = 1 \text{ ?}", color=WHITE).scale(MATH_SCALE)
        _clamp(mob1)
        mob1.move_to([0, MATH_CENTER_Y, 0])

        self.add_sound(AUDIO("hook"))
        self.play(Write(mob1), run_time=anim_time)
        remaining = max(0.3, dur - anim_time)
        self.wait(remaining)
        self.wait(EXTRA_HOLD)
        previous = mob1

        # ═══════════════════════════════════════════════════════════
        # SCENE 2: DEFINITION — "Factorial counts arrangements"
        # Show 3 blocks appearing on shelf + definition box
        # ═══════════════════════════════════════════════════════════
        dur = DUR("definition")

        # Build blocks
        block_size = 0.45
        gap = 0.12
        colors = [CYAN, GREEN, VIOLET]
        labels = ["A", "B", "C"]

        def _make_blocks(perm, shelf_y):
            blocks = VGroup()
            total_w = len(perm) * block_size + (len(perm) - 1) * gap
            start_x = -total_w / 2 + block_size / 2
            for pos, idx in enumerate(perm):
                sq = RoundedRectangle(
                    width=block_size, height=block_size,
                    color=colors[idx], fill_color=colors[idx],
                    fill_opacity=0.25, stroke_width=2,
                    corner_radius=0.06
                )
                lbl = MathTex(labels[idx], font_size=22, color=colors[idx])
                lbl.move_to(sq.get_center())
                block = VGroup(sq, lbl)
                block.move_to([start_x + pos * (block_size + gap), shelf_y, 0])
                blocks.add(block)
            return blocks

        shelf_y = MATH_CENTER_Y - 0.2
        shelf_w = 3 * block_size + 2 * gap + 0.3
        shelf = Line(LEFT * shelf_w/2, RIGHT * shelf_w/2, color=GREY_B, stroke_width=2)
        shelf.move_to([0, shelf_y - block_size/2 - 0.06, 0])

        blocks_3 = _make_blocks([0, 1, 2], shelf_y)

        # Definition box below
        def_box = _make_box(r"n! = \text{arrangements of } n \text{ objects}", "FACTORIAL")
        def_box.move_to([0, shelf_y - block_size/2 - 0.7, 0])

        self.add_sound(AUDIO("definition"))

        # Fade out previous
        self.play(FadeOut(previous, shift=UP * 0.3), run_time=0.4)

        # Show shelf + blocks
        self.play(Create(shelf), run_time=0.3)
        self.play(FadeIn(blocks_3, lag_ratio=0.15), run_time=0.6)

        # Show definition box
        self.play(FadeIn(def_box), run_time=0.6)

        remaining = max(0.3, dur - 0.4 - 0.3 - 0.6 - 0.6)
        self.wait(remaining)
        self.wait(EXTRA_HOLD)

        # Fade out definition box, keep shelf + blocks
        self.play(FadeOut(def_box), run_time=0.3)

        # ═══════════════════════════════════════════════════════════
        # SCENE 3: THREE DEMO — shuffle + "3! = 6"
        # ═══════════════════════════════════════════════════════════
        dur = DUR("three_demo")
        all_perms = list(permutations(range(3)))

        # Counter
        count_mob = MathTex("1", font_size=22, color=WHITE)
        count_mob.move_to([0, shelf_y - block_size/2 - 0.45, 0])

        self.add_sound(AUDIO("three_demo"))
        self.play(Write(count_mob), run_time=0.2)

        # Cycle through permutations
        current_blocks = blocks_3
        swap_budget = dur * 0.55  # ~55% for shuffling
        swap_time = swap_budget / max(len(all_perms) - 1, 1)

        for pi in range(1, len(all_perms)):
            new_blocks = _make_blocks(all_perms[pi], shelf_y)
            self.play(
                *[Transform(current_blocks[j], new_blocks[j]) for j in range(3)],
                run_time=max(0.25, swap_time * 0.6)
            )
            new_count = MathTex(str(pi + 1), font_size=22, color=WHITE)
            new_count.move_to(count_mob.get_center())
            self.play(Transform(count_mob, new_count), run_time=0.1)
            self.wait(max(0.1, swap_time * 0.3))

        # Show 3! = 6 result
        result_3 = MathTex(r"3! = 6", color=GREEN).scale(MATH_SCALE)
        _clamp(result_3)
        result_3.move_to([0, shelf_y - block_size/2 - 1.0, 0])
        self.play(Write(result_3), run_time=0.5)
        self.play(Circumscribe(result_3, color=GREEN), run_time=0.4)

        rest_time = max(0.3, dur - swap_budget - 0.2 - 0.5 - 0.4)
        self.wait(rest_time)
        self.wait(EXTRA_HOLD)

        # Clean up scene 3
        scene3_group = VGroup(shelf, current_blocks, count_mob, result_3)

        # ═══════════════════════════════════════════════════════════
        # SCENE 4: CASCADE — "2! = 2, 1! = 1"
        # ═══════════════════════════════════════════════════════════
        dur = DUR("cascade")
        anim_time = max(1.2, dur * ANIMATION_RATIO)

        cascade = MathTex(r"2! = 2", r"\qquad", r"1! = 1", color=WHITE).scale(MATH_SCALE)
        _clamp(cascade)
        cascade.move_to([0, MATH_CENTER_Y, 0])

        self.add_sound(AUDIO("cascade"))
        self.play(FadeOut(scene3_group, shift=UP * 0.3), run_time=0.4)
        self.play(Write(cascade), run_time=anim_time)
        remaining = max(0.3, dur - 0.4 - anim_time)
        self.wait(remaining)
        self.wait(EXTRA_HOLD)
        previous = cascade

        # ═══════════════════════════════════════════════════════════
        # SCENE 5: ZERO SETUP — "Now. Zero blocks."
        # ═══════════════════════════════════════════════════════════
        dur = DUR("zero_setup")

        # Empty shelf
        empty_shelf_y = MATH_CENTER_Y
        empty_shelf_w = 2.0
        empty_shelf_bar = Line(
            LEFT * empty_shelf_w/2, RIGHT * empty_shelf_w/2,
            color=GREY_B, stroke_width=2
        )
        empty_shelf_bar.move_to([0, empty_shelf_y - 0.35, 0])

        self.add_sound(AUDIO("zero_setup"))
        self.play(FadeOut(previous, shift=UP * 0.3), run_time=0.4)
        self.play(Create(empty_shelf_bar), run_time=0.4)
        remaining = max(0.3, dur - 0.8)
        self.wait(remaining)
        self.wait(EXTRA_HOLD)

        # ═══════════════════════════════════════════════════════════
        # SCENE 5.5: SILENCE BEAT — shelf glows
        # ═══════════════════════════════════════════════════════════
        glow_rect = Rectangle(
            width=empty_shelf_w * 0.7, height=0.5,
            color=CYAN, fill_color=CYAN,
            fill_opacity=0.0, stroke_width=0, stroke_opacity=0
        )
        glow_rect.move_to([0, empty_shelf_y, 0])
        glow_ring = RoundedRectangle(
            width=empty_shelf_w * 0.75, height=0.55,
            color=CYAN, stroke_width=1.5, stroke_opacity=0.0,
            fill_opacity=0, corner_radius=0.1
        )
        glow_ring.move_to([0, empty_shelf_y, 0])

        self.play(
            glow_rect.animate.set_fill(opacity=0.12),
            glow_ring.animate.set_stroke(opacity=0.35),
            run_time=1.5,
            rate_func=smooth
        )
        self.wait(0.8)

        # ═══════════════════════════════════════════════════════════
        # SCENE 6: INSIGHT — "Doing nothing IS the arrangement"
        # ═══════════════════════════════════════════════════════════
        dur = DUR("insight")

        cap_mob = MathTex(r"\text{The empty arrangement}", font_size=28, color=CYAN)
        _clamp(cap_mob)
        cap_mob.move_to([0, empty_shelf_y - 0.85, 0])

        self.add_sound(AUDIO("insight"))

        # Caption appears
        self.play(Write(cap_mob), run_time=0.8)
        self.wait(max(0.3, dur - 0.8))
        self.wait(EXTRA_HOLD)

        # ═══════════════════════════════════════════════════════════
        # SCENE 7: PUNCHLINE — "0! = 1"
        # ═══════════════════════════════════════════════════════════
        dur = DUR("punchline")

        # Clean up empty shelf scene
        shelf_group = VGroup(empty_shelf_bar, glow_rect, glow_ring, cap_mob)

        # Punchline box
        punch_box = _make_box(r"0! = 1")
        punch_box.move_to([0, MATH_CENTER_Y, 0])

        self.add_sound(AUDIO("punchline"))
        self.play(FadeOut(shelf_group, shift=UP * 0.3), run_time=0.4)
        self.play(FadeIn(punch_box), run_time=0.6)
        self.play(Circumscribe(punch_box, color=GREEN), run_time=0.5)

        # Closer text below
        closer = MathTex(
            r"\text{Exactly one way to arrange nothing.}",
            font_size=24, color=WHITE
        )
        _clamp(closer)
        closer.move_to([0, MATH_CENTER_Y - 1.0, 0])
        self.play(Write(closer), run_time=0.8)

        remaining = max(0.3, dur - 0.4 - 0.6 - 0.5 - 0.8)
        self.wait(remaining)
        self.wait(EXTRA_HOLD)

        # ═══════════════════════════════════════════════════════════
        # END CARD — Lissajous + ORBITAL (LOCKED)
        # ═══════════════════════════════════════════════════════════
        final_group = VGroup(punch_box, closer)
        self.play(FadeOut(final_group), run_time=0.4)

        _A, _B = 1.2, 0.95
        liss_glow = ParametricFunction(
            lambda t: np.array([_A*np.sin(2*t), _B*np.sin(3*t), 0]),
            t_range=[0, TAU, 0.02],
            color="#00E5FF", stroke_width=8, stroke_opacity=0.2
        )
        liss_core = ParametricFunction(
            lambda t: np.array([_A*np.sin(2*t), _B*np.sin(3*t), 0]),
            t_range=[0, TAU, 0.02],
            color="#00E5FF", stroke_width=2, stroke_opacity=1.0
        )
        logo = VGroup(liss_glow, liss_core).move_to([0, 0.5, 0])
        wordmark = Text("ORBITAL", font_size=22, color="#00E5FF", weight=BOLD)
        wordmark.next_to(logo, DOWN, buff=0.3)
        wm_glow2 = wordmark.copy().set_opacity(0.3).scale(1.05)
        end_card = VGroup(logo, wm_glow2, wordmark)
        end_card.move_to([0, 0, 0])

        self.play(Create(liss_core, run_time=0.8), FadeIn(liss_glow, run_time=0.6))
        self.play(FadeIn(VGroup(wm_glow2, wordmark), shift=UP*0.2), run_time=0.4)
        self.wait(1.2)
        self.play(FadeOut(end_card), run_time=0.3)
