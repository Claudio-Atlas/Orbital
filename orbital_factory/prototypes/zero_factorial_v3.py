"""
Why is 0! = 1? — Shorts Prototype v3
======================================
v3: Locked font_size values from L'Hôpital v6. No .scale() calls.
Visual cascade: 3→2→1→0 blocks.

Render:
  cd ~/Desktop/Orbital/orbital_factory && source venv/bin/activate
  PATH="/Library/TeX/texbin:$PATH" manim render prototypes/zero_factorial_v3.py ZeroFactorialV3 \
    -o zero_factorial_v3.mp4 --format mp4 -r 1080,1920 --frame_rate 60 --flush_cache
"""
from manim import *
from itertools import permutations
import numpy as np
import json, os

config.frame_width = 4.5
config.frame_height = 8.0

# ── LOCKED VISUAL SPEC ──
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
MATH_CENTER_Y = 1.2
EXTRA_HOLD = 0.5
ANIMATION_RATIO = 0.35

# ── LOCKED FONT SIZES (from L'Hôpital v6) ──
FS_MAIN = 30        # Main equation
FS_TITLE = 22       # Title/heading (Text, bold)
FS_CALLOUT = 24     # Callout text (Text, bold)
FS_ANSWER = 32      # Final answer / punchline
FS_BOX_LABEL = 14   # Box label (Text)
FS_BOX_CONTENT = 28 # Text inside box (MathTex)
FS_WATERMARK = 10   # Watermark (Text, bold)
FS_COUNTER = 22     # Counter / small numbers
FS_CAPTION = 24     # Caption text
FS_BLOCK_LABEL = 28 # Block labels (A, B, C)

# ── TTS ──
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
    inner = MathTex(content_tex, font_size=FS_BOX_CONTENT, color=WHITE)
    _clamp(inner, MAX_WIDTH * 0.85)
    box_rect = SurroundingRectangle(
        inner, color=BOX_BORDER, fill_color=BOX_FILL,
        fill_opacity=0.6, buff=0.2, corner_radius=0.1, stroke_width=2,
    )
    if label_text:
        lbl = Text(label_text, color=LABEL_COLOR, font_size=FS_BOX_LABEL)
        lbl.next_to(box_rect, UP, buff=0.1)
        return VGroup(box_rect, lbl, inner)
    return VGroup(box_rect, inner)


class ZeroFactorialV3(Scene):
    def construct(self):
        self.camera.background_color = BLACK

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

        wm = Text("ORBITAL", font_size=FS_WATERMARK, color=WHITE, weight=BOLD)
        wm.set_opacity(0.35)
        wm.move_to([-FRAME_W/2 + 0.5, -FRAME_H/2 + 0.2, 0])
        self.add(wm)

        previous = None

        # ── BLOCK BUILDER ──
        BLOCK_SIZE = 0.65
        GAP = 0.14
        BLOCK_COLORS = [CYAN, GREEN, VIOLET]
        BLOCK_LABELS = ["A", "B", "C"]

        def _make_blocks(indices, shelf_y, block_size=BLOCK_SIZE):
            n = len(indices)
            blocks = VGroup()
            total_w = n * block_size + (n - 1) * GAP
            start_x = -total_w / 2 + block_size / 2
            for pos, idx in enumerate(indices):
                sq = RoundedRectangle(
                    width=block_size, height=block_size,
                    color=BLOCK_COLORS[idx], fill_color=BLOCK_COLORS[idx],
                    fill_opacity=0.25, stroke_width=2,
                    corner_radius=0.08
                )
                lbl = MathTex(BLOCK_LABELS[idx], font_size=FS_BLOCK_LABEL, color=BLOCK_COLORS[idx])
                lbl.move_to(sq.get_center())
                block = VGroup(sq, lbl)
                block.move_to([start_x + pos * (block_size + GAP), shelf_y, 0])
                blocks.add(block)
            return blocks

        def _make_shelf(n, shelf_y, block_size=BLOCK_SIZE):
            total_w = n * block_size + (n - 1) * GAP + 0.3
            shelf = Line(LEFT * total_w/2, RIGHT * total_w/2, color=GREY_B, stroke_width=2)
            shelf.move_to([0, shelf_y - block_size/2 - 0.06, 0])
            return shelf

        # ── CASCADE LAYOUT ──
        ACTIVE_Y = 2.5
        ROW_SPACING = 1.3
        COMPLETED_START_Y = 0.8

        completed_rows = VGroup()

        # ═══════════════════════════════════════════════════════════
        # SCENE 1: HOOK
        # ═══════════════════════════════════════════════════════════
        dur = DUR("hook")
        anim_time = max(1.2, dur * ANIMATION_RATIO)

        mob1 = MathTex(r"0! = 1 \text{ ?}", font_size=FS_MAIN, color=WHITE)
        _clamp(mob1)
        mob1.move_to([0, MATH_CENTER_Y, 0])

        self.add_sound(AUDIO("hook"))
        self.play(Write(mob1), run_time=anim_time)
        self.wait(max(0.3, dur - anim_time))
        self.wait(EXTRA_HOLD)
        previous = mob1

        # ═══════════════════════════════════════════════════════════
        # SCENE 2: DEFINITION
        # ═══════════════════════════════════════════════════════════
        dur = DUR("definition")

        shelf_3 = _make_shelf(3, ACTIVE_Y)
        blocks_3 = _make_blocks([0, 1, 2], ACTIVE_Y)

        def_box = _make_box(r"n! = \text{arrangements of } n \text{ objects}", "FACTORIAL")
        def_box.move_to([0, ACTIVE_Y - BLOCK_SIZE/2 - 0.8, 0])

        self.add_sound(AUDIO("definition"))
        self.play(FadeOut(previous, shift=UP * 0.3), run_time=0.4)
        self.play(Create(shelf_3), FadeIn(blocks_3, lag_ratio=0.15), run_time=0.6)
        self.play(FadeIn(def_box), run_time=0.5)
        self.wait(max(0.3, dur - 0.4 - 0.6 - 0.5))
        self.wait(EXTRA_HOLD)
        self.play(FadeOut(def_box), run_time=0.3)

        # ═══════════════════════════════════════════════════════════
        # SCENE 3: THREE DEMO
        # ═══════════════════════════════════════════════════════════
        dur = DUR("three_demo")
        all_perms_3 = list(permutations(range(3)))

        count_mob = MathTex("1", font_size=FS_COUNTER, color=WHITE)
        count_mob.move_to([0, ACTIVE_Y - BLOCK_SIZE/2 - 0.45, 0])

        self.add_sound(AUDIO("three_demo"))
        self.play(Write(count_mob), run_time=0.2)

        current_blocks = blocks_3
        swap_budget = dur * 0.5
        swap_time = swap_budget / max(len(all_perms_3) - 1, 1)

        for pi in range(1, len(all_perms_3)):
            new_blocks = _make_blocks(all_perms_3[pi], ACTIVE_Y)
            self.play(
                *[Transform(current_blocks[j], new_blocks[j]) for j in range(3)],
                run_time=max(0.25, swap_time * 0.6)
            )
            new_count = MathTex(str(pi + 1), font_size=FS_COUNTER, color=WHITE)
            new_count.move_to(count_mob.get_center())
            self.play(Transform(count_mob, new_count), run_time=0.1)
            self.wait(max(0.1, swap_time * 0.3))

        result_3 = MathTex(r"3! = 6", font_size=FS_MAIN, color=GREEN)
        result_3.next_to(shelf_3, RIGHT, buff=0.15)
        _clamp(result_3)
        self.play(FadeOut(count_mob), Write(result_3), run_time=0.4)
        rest = max(0.3, dur - swap_budget - 0.2 - 0.4)
        self.wait(rest)

        # SLIDE DOWN
        row_3 = VGroup(shelf_3, current_blocks, result_3)
        shift_3 = ACTIVE_Y - COMPLETED_START_Y
        self.play(row_3.animate.shift(DOWN * shift_3).scale(0.7), run_time=0.5)
        completed_rows.add(row_3)
        self.wait(0.3)

        # ═══════════════════════════════════════════════════════════
        # SCENE 4: TWO DEMO
        # ═══════════════════════════════════════════════════════════
        dur = DUR("two_demo")

        shelf_2 = _make_shelf(2, ACTIVE_Y)
        blocks_2 = _make_blocks([0, 1], ACTIVE_Y)

        self.add_sound(AUDIO("two_demo"))
        self.play(Create(shelf_2), FadeIn(blocks_2, lag_ratio=0.15), run_time=0.4)

        new_blocks_2 = _make_blocks([1, 0], ACTIVE_Y)
        self.play(
            *[Transform(blocks_2[j], new_blocks_2[j]) for j in range(2)],
            run_time=0.5
        )

        result_2 = MathTex(r"2! = 2", font_size=FS_MAIN, color=GREEN)
        result_2.next_to(shelf_2, RIGHT, buff=0.15)
        _clamp(result_2)
        self.play(Write(result_2), run_time=0.3)
        self.wait(max(0.2, dur - 0.4 - 0.5 - 0.3))

        # SLIDE DOWN
        row_2 = VGroup(shelf_2, blocks_2, result_2)
        shift_2 = ACTIVE_Y - (COMPLETED_START_Y - ROW_SPACING * 0.7)
        self.play(row_2.animate.shift(DOWN * shift_2).scale(0.7), run_time=0.4)
        completed_rows.add(row_2)
        self.wait(0.2)

        # ═══════════════════════════════════════════════════════════
        # SCENE 5: ONE DEMO
        # ═══════════════════════════════════════════════════════════
        dur = DUR("one_demo")

        shelf_1 = _make_shelf(1, ACTIVE_Y)
        blocks_1 = _make_blocks([0], ACTIVE_Y)

        self.add_sound(AUDIO("one_demo"))
        self.play(Create(shelf_1), FadeIn(blocks_1), run_time=0.4)

        result_1 = MathTex(r"1! = 1", font_size=FS_MAIN, color=GREEN)
        result_1.next_to(shelf_1, RIGHT, buff=0.15)
        _clamp(result_1)
        self.play(Write(result_1), run_time=0.3)
        self.wait(max(0.2, dur - 0.4 - 0.3))

        # SLIDE DOWN
        row_1 = VGroup(shelf_1, blocks_1, result_1)
        shift_1 = ACTIVE_Y - (COMPLETED_START_Y - ROW_SPACING * 1.4)
        self.play(row_1.animate.shift(DOWN * shift_1).scale(0.7), run_time=0.4)
        completed_rows.add(row_1)
        self.wait(0.3)

        # ═══════════════════════════════════════════════════════════
        # SCENE 6: ZERO SETUP
        # ═══════════════════════════════════════════════════════════
        dur = DUR("zero_setup")

        empty_shelf_y = MATH_CENTER_Y + 0.3
        empty_shelf_w = 1.8
        empty_shelf_bar = Line(
            LEFT * empty_shelf_w/2, RIGHT * empty_shelf_w/2,
            color=GREY_B, stroke_width=2
        )
        empty_shelf_bar.move_to([0, empty_shelf_y - 0.35, 0])

        self.add_sound(AUDIO("zero_setup"))
        self.play(FadeOut(completed_rows, shift=DOWN * 0.5), run_time=0.5)
        self.play(Create(empty_shelf_bar), run_time=0.3)
        self.wait(max(0.3, dur - 0.8))
        self.wait(EXTRA_HOLD)

        # ═══════════════════════════════════════════════════════════
        # SILENCE BEAT
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
        # SCENE 7: INSIGHT
        # ═══════════════════════════════════════════════════════════
        dur = DUR("insight")

        zero_q = MathTex(r"0! = \text{ ?}", font_size=FS_MAIN, color=WHITE)
        zero_q.move_to([0, empty_shelf_y + 0.7, 0])

        cap_mob = MathTex(r"\text{The empty arrangement}", font_size=FS_CAPTION, color=CYAN)
        _clamp(cap_mob)
        cap_mob.move_to([0, empty_shelf_y - 0.85, 0])

        self.add_sound(AUDIO("insight"))
        self.play(Write(zero_q), run_time=0.5)
        self.wait(1.0)
        self.play(Write(cap_mob), run_time=0.6)
        self.wait(max(0.3, dur - 0.5 - 1.0 - 0.6))
        self.wait(EXTRA_HOLD)

        # ═══════════════════════════════════════════════════════════
        # SCENE 8: PUNCHLINE
        # ═══════════════════════════════════════════════════════════
        dur = DUR("punchline")

        shelf_group = VGroup(empty_shelf_bar, glow_rect, glow_ring, cap_mob, zero_q)

        # Punchline — bigger font for final answer
        punch_inner = MathTex(r"0! = 1", font_size=FS_ANSWER, color=GREEN)
        _clamp(punch_inner, MAX_WIDTH * 0.85)
        punch_box = SurroundingRectangle(
            punch_inner, color=BOX_BORDER, fill_color=BOX_FILL,
            fill_opacity=0.6, buff=0.25, corner_radius=0.1, stroke_width=2,
        )
        punch_group = VGroup(punch_box, punch_inner)
        punch_group.move_to([0, MATH_CENTER_Y + 0.5, 0])

        closer = Text(
            "Exactly one way to arrange nothing.",
            font_size=FS_CALLOUT, color=WHITE, weight=BOLD
        )
        _clamp(closer)
        closer.move_to([0, MATH_CENTER_Y - 0.6, 0])

        self.add_sound(AUDIO("punchline"))
        self.play(FadeOut(shelf_group, shift=UP * 0.3), run_time=0.4)
        self.play(FadeIn(punch_group), run_time=0.6)
        self.play(Circumscribe(punch_group, color=GREEN), run_time=0.5)
        self.wait(0.5)
        self.play(Write(closer), run_time=0.8)
        self.wait(max(0.3, dur - 0.4 - 0.6 - 0.5 - 0.5 - 0.8))
        self.wait(EXTRA_HOLD)

        # ═══════════════════════════════════════════════════════════
        # END CARD — Lissajous + ORBITAL (LOCKED)
        # ═══════════════════════════════════════════════════════════
        self.play(FadeOut(VGroup(punch_group, closer)), run_time=0.4)

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
