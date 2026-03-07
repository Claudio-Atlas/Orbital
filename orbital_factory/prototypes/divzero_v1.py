"""
"Why You Can't Divide by Zero" — Orbital Short v1
====================================================
Novel visuals: Division Machine, Equation Shatter, Tearing Graph
Contradiction FIRST, graph SECOND (Circle consensus)

Render:
  cd ~/Desktop/Orbital/orbital_factory && source venv/bin/activate
  PATH="/Library/TeX/texbin:$PATH" manim render prototypes/divzero_v1.py DivZeroV1 \
    -o divzero_v1.mp4 --format mp4 -r 1080,1920 --frame_rate 60 --flush_cache
"""
from manim import *
import numpy as np
import json

config.frame_width = 4.5
config.frame_height = 8.0

VIOLET = "#8B5CF6"
CYAN = "#22D3EE"
GREEN = "#39FF14"
ORANGE = "#F97316"
RED = "#FF4444"
BOX_FILL = "#1a1130"
END_CYAN = "#00E5FF"
GRID_COL = "#1a1a3a"
FW, FH = 4.5, 8.0

# ── TTS MANIFEST ──
with open("output/tts/divzero_scenes/manifest.json") as f:
    _m = json.load(f)
    MANIFEST = {s["id"]: s for s in _m["scenes"]}

def DUR(sid): return MANIFEST[sid]["duration"]

SILENCE = {
    "contradiction_setup": 2.0,
    "contradiction_payoff": 3.0,
    "graph_explosion": 3.0,
    "punchline": 1.0,
}


def _box(mob, color=VIOLET, fill=BOX_FILL, opacity=0.6, buff=0.12):
    return SurroundingRectangle(mob, color=color, fill_color=fill,
        fill_opacity=opacity, buff=buff, corner_radius=0.1, stroke_width=2.5)


def _neon_grid(center, w, h, spacing=0.5, color=GRID_COL, opacity=0.25):
    lines = VGroup()
    cx, cy = center[0], center[1]
    x = cx - w/2
    while x <= cx + w/2:
        lines.add(Line([x, cy-h/2, 0], [x, cy+h/2, 0],
                       color=color, stroke_width=0.5, stroke_opacity=opacity))
        x += spacing
    y = cy - h/2
    while y <= cy + h/2:
        lines.add(Line([cx-w/2, y, 0], [cx+w/2, y, 0],
                       color=color, stroke_width=0.5, stroke_opacity=opacity))
        y += spacing
    return lines


class DivZeroV1(Scene):
    def construct(self):
        self.camera.background_color = BLACK

        # ── Persistent border + watermark ──
        border = Rectangle(width=FW-0.1, height=FH-0.1, color=VIOLET,
                           stroke_width=2.5, stroke_opacity=0.7, fill_opacity=0)
        border_glow = Rectangle(width=FW-0.05, height=FH-0.05, color=VIOLET,
                                stroke_width=5, stroke_opacity=0.12, fill_opacity=0)
        self.add(border_glow, border)
        wm = Text("ORBITAL", font_size=10, color=WHITE, weight=BOLD)
        wm.set_opacity(0.35).move_to([-FW/2+0.45, -FH/2+0.2, 0])
        self.add(wm)

        # ═══════════════════════════════════════════════
        # S1: HOOK (6.2s)
        # "Your calculator says ERROR..."
        # ═══════════════════════════════════════════════
        dur = DUR("hook")
        grid_h = _neon_grid([0, 0], FW, FH, 0.6, GRID_COL, 0.15)
        self.add(grid_h)

        # Calculator ERROR display
        calc_body = RoundedRectangle(width=2.0, height=2.8, color=VIOLET,
            fill_color=BOX_FILL, fill_opacity=0.8, corner_radius=0.15,
            stroke_width=2).move_to([0, 1.5, 0])
        calc_screen = RoundedRectangle(width=1.6, height=0.7, color=GREEN,
            fill_color="#001100", fill_opacity=0.9, corner_radius=0.05,
            stroke_width=1).move_to([0, 2.3, 0])
        err_text = Text("ERROR", font_size=20, color=RED, weight=BOLD)
        err_text.move_to(calc_screen.get_center())

        # Calculator buttons (decorative)
        buttons = VGroup()
        for r in range(3):
            for c in range(3):
                b = RoundedRectangle(width=0.35, height=0.3, color=VIOLET,
                    fill_color="#2a1a4a", fill_opacity=0.6, corner_radius=0.04,
                    stroke_width=1)
                b.move_to([c*0.45 - 0.45, 1.3 - r*0.4, 0])
                buttons.add(b)
        calc = VGroup(calc_body, calc_screen, buttons)

        self.play(FadeIn(calc), run_time=0.4)  # 0.4
        self.play(Write(err_text), run_time=0.3)  # 0.7

        # Glitch effect
        self.play(
            err_text.animate.set_color(GREEN).shift(RIGHT*0.03),
            run_time=0.1
        )
        self.play(
            err_text.animate.set_color(RED).shift(LEFT*0.03),
            run_time=0.1
        )  # 0.9

        # "They're lying" text
        lying = Text("they're lying to you", font_size=20, color=RED, weight=BOLD)
        lying_bx = _box(lying, RED, "#2a0a0a", 0.5, 0.1)
        VGroup(lying_bx, lying).move_to([0, -1.0, 0])
        self.play(FadeIn(lying_bx), Write(lying), run_time=0.4)  # 1.3

        self.wait(max(0.3, dur - 1.3))

        self.play(FadeOut(VGroup(calc, err_text, lying, lying_bx, grid_h)), run_time=0.3)

        # ═══════════════════════════════════════════════
        # S2: WHAT IS DIVISION? (16.1s)
        # Division Machine visual
        # ═══════════════════════════════════════════════
        dur = DUR("what_is_division")
        g2 = _neon_grid([0, 0], FW, FH, 0.6, GRID_COL, 0.12)
        self.add(g2)

        # Title
        div_title = Text("What is division?", font_size=18, color=VIOLET, weight=BOLD)
        div_bx = _box(div_title, VIOLET, BOX_FILL, 0.5, 0.08)
        VGroup(div_bx, div_title).move_to([0, 3.3, 0])
        self.play(FadeIn(div_bx), FadeIn(div_title), run_time=0.3)  # 0.3

        # Division Machine body
        machine = RoundedRectangle(width=2.5, height=2.0, color=VIOLET,
            fill_color=BOX_FILL, fill_opacity=0.7, corner_radius=0.15,
            stroke_width=2.5).move_to([0, 1.0, 0])
        div_sym = MathTex(r"\div", font_size=36, color=VIOLET)
        div_sym.move_to(machine.get_center())
        # Input slot (top)
        in_slot = Rectangle(width=0.8, height=0.3, color=CYAN,
            fill_color=CYAN, fill_opacity=0.2, stroke_width=1.5).move_to([0, 2.15, 0])
        # Output slot (bottom)
        out_slot = Rectangle(width=0.8, height=0.3, color=GREEN,
            fill_color=GREEN, fill_opacity=0.2, stroke_width=1.5).move_to([0, -0.15, 0])

        mach_grp = VGroup(machine, div_sym, in_slot, out_slot)
        self.play(FadeIn(mach_grp), run_time=0.4)  # 0.7

        # 8 ÷ 2 = 4 demo
        num8 = MathTex("8", font_size=28, color=CYAN).move_to([0, 3.0, 0])
        by2 = MathTex(r"\div 2", font_size=22, color=ORANGE).move_to([1.6, 1.0, 0])

        self.play(FadeIn(num8), FadeIn(by2), run_time=0.3)  # 1.0
        self.play(num8.animate.move_to(in_slot.get_center()), run_time=0.4)  # 1.4

        # Machine processes — flash
        self.play(
            Flash(machine, color=VIOLET, line_length=0.3, num_lines=8, run_time=0.3),
            run_time=0.3
        )  # 1.7

        # Output: 4 groups
        groups = VGroup()
        for i in range(4):
            g = MathTex("2", font_size=18, color=GREEN)
            g.move_to([-0.9 + i*0.6, -1.0, 0])
            box = _box(g, GREEN, BOX_FILL, 0.3, 0.06)
            groups.add(VGroup(box, g))

        result = MathTex("= 4", font_size=24, color=GREEN)
        result.move_to([0, -1.8, 0])
        res_bx = _box(result, GREEN, BOX_FILL, 0.5, 0.08)

        self.play(
            *[FadeIn(g, shift=DOWN*0.2) for g in groups],
            run_time=0.5
        )  # 2.2
        self.play(FadeIn(res_bx), Write(result), run_time=0.3)  # 2.5

        self.wait(1.5)  # 4.0

        # Clear for ÷0
        self.play(FadeOut(VGroup(num8, by2, groups, result, res_bx)), run_time=0.3)  # 4.3

        # 8 ÷ 0 — machine breaks
        num8b = MathTex("8", font_size=28, color=CYAN).move_to([0, 3.0, 0])
        by0 = MathTex(r"\div 0", font_size=22, color=RED).move_to([1.6, 1.0, 0])
        q_out = MathTex("?", font_size=36, color=RED)
        q_out.move_to([0, -1.0, 0])

        self.play(FadeIn(num8b), FadeIn(by0), run_time=0.3)  # 4.6
        self.play(num8b.animate.move_to(in_slot.get_center()), run_time=0.4)  # 5.0

        # Machine shakes!
        for _ in range(4):
            self.play(
                machine.animate.shift(RIGHT*0.05), run_time=0.05
            )
            self.play(
                machine.animate.shift(LEFT*0.1), run_time=0.05
            )
            self.play(
                machine.animate.shift(RIGHT*0.05), run_time=0.05
            )
        # 5.0 + 0.6 = 5.6

        # Sparks
        self.play(
            Flash(machine, color=RED, line_length=0.4, num_lines=12, run_time=0.3),
            FadeIn(q_out, scale=2),
            run_time=0.4
        )  # 6.0

        # "Zero never adds up to 8" caption
        cap = Text("zero never adds up to 8", font_size=14, color=RED, weight=BOLD)
        cap_bx = _box(cap, RED, "#2a0a0a", 0.4, 0.06)
        VGroup(cap_bx, cap).move_to([0, -2.5, 0])
        self.play(FadeIn(cap_bx), FadeIn(cap), run_time=0.3)  # 6.3

        self.wait(max(0.3, dur - 6.3))

        self.play(FadeOut(VGroup(
            div_title, div_bx, mach_grp, num8b, by0, q_out, cap, cap_bx, g2
        )), run_time=0.3)

        # ═══════════════════════════════════════════════
        # S3: CONTRADICTION SETUP (6.9s + 2s silence)
        # ═══════════════════════════════════════════════
        dur = DUR("contradiction_setup")
        sil = SILENCE["contradiction_setup"]
        g3 = _neon_grid([0, 0], FW, FH, 0.6, GRID_COL, 0.15)
        self.add(g3)

        setup_title = Text("What if it DID have an answer?", font_size=16,
                           color=ORANGE, weight=BOLD)
        setup_bx = _box(setup_title, ORANGE, BOX_FILL, 0.5, 0.08)
        VGroup(setup_bx, setup_title).move_to([0, 3.3, 0])
        self.play(FadeIn(setup_bx), FadeIn(setup_title), run_time=0.3)  # 0.3

        # Big equation with glowing ?
        suppose = MathTex(r"1 \div 0 = \, ?", font_size=36, color=WHITE)
        suppose.move_to([0, 1.0, 0])
        suppose_bx = _box(suppose, ORANGE, BOX_FILL, 0.6, 0.15)

        self.play(FadeIn(suppose_bx), Write(suppose), run_time=0.5)  # 0.8

        # ? pulses
        qmark = suppose[-1]  # the ? character
        self.play(
            Indicate(qmark, color=ORANGE, scale_factor=1.3),
            run_time=0.5
        )  # 1.3

        # "any number" caption
        any_num = Text("any number — doesn't matter", font_size=14,
                       color=CYAN, weight=BOLD)
        any_bx = _box(any_num, CYAN, BOX_FILL, 0.4, 0.06)
        VGroup(any_bx, any_num).move_to([0, -0.5, 0])
        self.play(FadeIn(any_bx), FadeIn(any_num), run_time=0.3)  # 1.6

        self.wait(max(0.3, dur - 1.6))

        # Silence beat
        self.wait(sil)

        self.play(FadeOut(VGroup(setup_title, setup_bx, any_num, any_bx)), run_time=0.2)
        # Keep suppose on screen for next scene

        # ═══════════════════════════════════════════════
        # S4: CONTRADICTION PAYOFF (12.6s + 3s silence)
        # EQUATION SHATTER
        # ═══════════════════════════════════════════════
        dur = DUR("contradiction_payoff")
        sil = SILENCE["contradiction_payoff"]

        # Step 1: ? × 0 = 1
        step1 = MathTex(r"? \times 0 = 1", font_size=28, color=CYAN)
        step1.move_to([0, -0.3, 0])
        step1_bx = _box(step1, CYAN, BOX_FILL, 0.4, 0.1)
        self.play(FadeIn(step1_bx), Write(step1), run_time=0.5)  # 0.5

        self.wait(1.0)  # 1.5

        # Step 2: but ? × 0 = 0 (always!)
        step2 = MathTex(r"\text{but } ? \times 0 = 0", font_size=28, color=ORANGE)
        step2.move_to([0, -1.5, 0])
        step2_bx = _box(step2, ORANGE, BOX_FILL, 0.4, 0.1)
        always = Text("(always!)", font_size=12, color=ORANGE, weight=BOLD)
        always.next_to(step2, RIGHT, buff=0.1)

        self.play(FadeIn(step2_bx), Write(step2), FadeIn(always), run_time=0.5)  # 2.0

        self.wait(1.5)  # 3.5

        # Step 3: 0 = 1 — THE BIG ONE
        self.play(FadeOut(VGroup(suppose, suppose_bx, step1, step1_bx,
                                  step2, step2_bx, always)), run_time=0.3)  # 3.8

        zero_eq_one = MathTex(r"0 = 1", font_size=48, color=RED)
        zero_eq_one.move_to([0, 1.0, 0])
        zeo_bx = _box(zero_eq_one, RED, "#2a0a0a", 0.6, 0.2)

        self.play(FadeIn(zeo_bx), Write(zero_eq_one), run_time=0.4)  # 4.2

        # The equals sign "cracks"
        crack1 = Line(
            zero_eq_one.get_center() + UP*0.3 + LEFT*0.1,
            zero_eq_one.get_center() + DOWN*0.3 + RIGHT*0.1,
            color=RED, stroke_width=4
        )
        crack2 = Line(
            zero_eq_one.get_center() + UP*0.2 + RIGHT*0.15,
            zero_eq_one.get_center() + DOWN*0.35 + LEFT*0.05,
            color=RED, stroke_width=3
        )
        self.play(Create(crack1), Create(crack2), run_time=0.3)  # 4.5

        # Equation shatter cascade!
        shatter_eqs = [
            r"2 = 3", r"100 = 0", r"7 = -5",
            r"\pi = 42", r"1{,}000{,}000 = 1"
        ]
        shatter_mobs = []
        positions = [
            [-1.2, -0.5], [1.0, -0.8], [-0.8, -1.8],
            [0.9, -2.2], [-0.3, -3.0]
        ]
        for eq_str, pos in zip(shatter_eqs, positions):
            eq = MathTex(eq_str, font_size=18, color=RED)
            eq.set_opacity(0.6)
            eq.move_to([pos[0], pos[1], 0])
            # Crack through each
            cr = Line(
                eq.get_corner(UL) + UL*0.05,
                eq.get_corner(DR) + DR*0.05,
                color=RED, stroke_width=2, stroke_opacity=0.5
            )
            shatter_mobs.append(VGroup(eq, cr))

        # Cascade them in
        for i, mob in enumerate(shatter_mobs):
            self.play(FadeIn(mob, scale=0.8), run_time=0.15)
        # 4.5 + 5*0.15 = 5.25

        # "Math destroying itself" text
        destroy = Text("math destroying itself", font_size=18, color=RED, weight=BOLD)
        destroy_bx = _box(destroy, RED, "#2a0a0a", 0.5, 0.08)
        VGroup(destroy_bx, destroy).move_to([0, -3.5, 0])
        self.play(FadeIn(destroy_bx), Write(destroy), run_time=0.4)  # 5.65

        self.wait(max(0.3, dur - 5.65))

        # 3s silence — hold the destruction
        self.wait(sil)

        self.play(FadeOut(VGroup(
            zero_eq_one, zeo_bx, crack1, crack2,
            *shatter_mobs, destroy, destroy_bx, g3
        )), run_time=0.3)

        # ═══════════════════════════════════════════════
        # S5: GRAPH INTRO (12.2s)
        # Animated fractions shrinking
        # ═══════════════════════════════════════════════
        dur = DUR("graph_intro")
        g5 = _neon_grid([0, 0], FW, FH, 0.6, GRID_COL, 0.15)
        self.add(g5)

        intro_title = Text("See the breaking point", font_size=16,
                           color=CYAN, weight=BOLD)
        intro_bx = _box(intro_title, CYAN, BOX_FILL, 0.5, 0.08)
        VGroup(intro_bx, intro_title).move_to([0, 3.3, 0])
        self.play(FadeIn(intro_bx), FadeIn(intro_title), run_time=0.3)  # 0.3

        # Animated division countdown
        divisions = [
            (r"1 \div 1", "= 1"),
            (r"1 \div 0.1", "= 10"),
            (r"1 \div 0.01", "= 100"),
            (r"1 \div 0.001", "= 1{,}000"),
            (r"1 \div 0.0001", "= 10{,}000"),
        ]

        prev_mob = None
        for i, (left, right) in enumerate(divisions):
            eq = MathTex(left, font_size=22, color=WHITE)
            res = MathTex(right, font_size=22, color=GREEN)
            res.next_to(eq, RIGHT, buff=0.15)
            row = VGroup(eq, res)
            y_pos = 2.2 - i * 0.7
            row.move_to([0, y_pos, 0])

            if prev_mob:
                self.play(FadeIn(row, shift=DOWN*0.1), run_time=0.3)
            else:
                self.play(Write(row), run_time=0.4)
            prev_mob = row

            # Results get progressively bigger/brighter
            self.play(
                Indicate(res, color=GREEN, scale_factor=1.1 + i*0.05),
                run_time=0.2
            )
        # 0.3 + 5*(0.3+0.2) = 2.8

        # Arrow pointing down → infinity
        arr = MathTex(r"\downarrow \infty", font_size=28, color=GREEN)
        arr.move_to([0, -1.8, 0])
        arr_bx = _box(arr, GREEN, BOX_FILL, 0.5, 0.08)
        self.play(FadeIn(arr_bx), Write(arr), run_time=0.3)  # 3.1

        self.wait(max(0.3, dur - 3.1))

        self.play(FadeOut(VGroup(intro_title, intro_bx, *[prev_mob],
                                  arr, arr_bx)), run_time=0.3)
        # Keep grid for next scene

        # ═══════════════════════════════════════════════
        # S6: GRAPH EXPLOSION — TEARING NUMBER LINE (11.5s + 3s silence)
        # ═══════════════════════════════════════════════
        dur = DUR("graph_explosion")
        sil = SILENCE["graph_explosion"]

        exp_title = MathTex(r"y = \frac{1}{x}", font_size=24, color=CYAN)
        exp_bx = _box(exp_title, CYAN, BOX_FILL, 0.4, 0.08)
        VGroup(exp_bx, exp_title).move_to([0, 3.3, 0])
        self.play(FadeIn(exp_bx), FadeIn(exp_title), run_time=0.2)  # 0.2

        # Axes
        ax = Axes(
            x_range=[-3, 3, 1], y_range=[-8, 8, 2],
            x_length=3.5, y_length=5.0,
            tips=False,
            axis_config={"color": VIOLET, "stroke_width": 1.5, "stroke_opacity": 0.6},
        ).move_to([0, -0.3, 0])

        self.play(Create(ax), run_time=0.3)  # 0.5

        # Right side (positive) — GREEN
        curve_right = ax.plot(lambda x: 1/x, x_range=[0.13, 3],
                               color=GREEN, stroke_width=3)
        # Left side (negative) — RED
        curve_left = ax.plot(lambda x: 1/x, x_range=[-3, -0.13],
                              color=RED, stroke_width=3)

        self.play(Create(curve_right), run_time=0.8)  # 1.3
        self.play(Create(curve_left), run_time=0.8)  # 2.1

        # Vertical asymptote — dashed, pulsing
        asymp = DashedLine(
            ax.c2p(0, -8), ax.c2p(0, 8),
            color=ORANGE, stroke_width=2.5, dash_length=0.12
        )
        self.play(Create(asymp), run_time=0.3)  # 2.4

        # Labels: +∞ and -∞
        plus_inf = MathTex(r"+\infty", font_size=22, color=GREEN)
        plus_inf.move_to([0.8, 2.5, 0])
        plus_bx = _box(plus_inf, GREEN, BOX_FILL, 0.4, 0.06)

        minus_inf = MathTex(r"-\infty", font_size=22, color=RED)
        minus_inf.move_to([-0.8, -2.8, 0])
        minus_bx = _box(minus_inf, RED, "#2a0a0a", 0.4, 0.06)

        self.play(FadeIn(plus_bx), FadeIn(plus_inf), run_time=0.3)  # 2.7
        self.play(FadeIn(minus_bx), FadeIn(minus_inf), run_time=0.3)  # 3.0

        # TEARING effect — graph halves pull apart
        # Shift right curve right, left curve left
        self.play(
            VGroup(curve_right, plus_bx, plus_inf).animate.shift(RIGHT*0.15),
            VGroup(curve_left, minus_bx, minus_inf).animate.shift(LEFT*0.15),
            run_time=0.5
        )  # 3.5

        # Glowing void at the center
        void_glow = Ellipse(width=0.3, height=5.0, color=ORANGE,
            fill_color=ORANGE, fill_opacity=0.15, stroke_width=2,
            stroke_opacity=0.4).move_to(ax.c2p(0, 0))
        self.play(FadeIn(void_glow), run_time=0.3)  # 3.8

        # "Two directions" caption
        two_dir = Text("two directions — no answer", font_size=14,
                       color=ORANGE, weight=BOLD)
        two_bx = _box(two_dir, ORANGE, BOX_FILL, 0.4, 0.06)
        VGroup(two_bx, two_dir).move_to([0, -3.5, 0])
        self.play(FadeIn(two_bx), FadeIn(two_dir), run_time=0.3)  # 4.1

        self.wait(max(0.3, dur - 4.1))

        # 3s silence
        self.wait(sil)

        self.play(FadeOut(VGroup(
            exp_title, exp_bx, ax, curve_right, curve_left, asymp,
            plus_bx, plus_inf, minus_bx, minus_inf, void_glow,
            two_dir, two_bx, g5
        )), run_time=0.3)

        # ═══════════════════════════════════════════════
        # S7: PUNCHLINE (11.3s + 1s silence)
        # ═══════════════════════════════════════════════
        dur = DUR("punchline")
        sil = SILENCE["punchline"]
        g7 = _neon_grid([0, 0], FW, FH, 0.6, GRID_COL, 0.15)
        self.add(g7)

        # "Not infinity"
        not_inf = MathTex(r"1 \div 0 \neq \infty", font_size=30, color=RED)
        not_inf.move_to([0, 2.5, 0])
        ni_bx = _box(not_inf, RED, "#2a0a0a", 0.5, 0.1)
        self.play(FadeIn(ni_bx), Write(not_inf), run_time=0.5)  # 0.5

        self.wait(0.8)  # 1.3

        # "Not nothing"
        not_zero = MathTex(r"1 \div 0 \neq 0", font_size=30, color=RED)
        not_zero.move_to([0, 1.0, 0])
        nz_bx = _box(not_zero, RED, "#2a0a0a", 0.5, 0.1)
        self.play(FadeIn(nz_bx), Write(not_zero), run_time=0.5)  # 1.8

        self.wait(0.8)  # 2.6

        # "A logical impossibility"
        impossible = Text("a logical impossibility", font_size=18,
                          color=ORANGE, weight=BOLD)
        imp_bx = _box(impossible, ORANGE, BOX_FILL, 0.5, 0.08)
        VGroup(imp_bx, impossible).move_to([0, -0.5, 0])
        self.play(FadeIn(imp_bx), Write(impossible), run_time=0.4)  # 3.0

        self.wait(1.0)  # 4.0

        # UNDEFINED — big stamp
        undef = Text("UNDEFINED", font_size=32, color=VIOLET, weight=BOLD)
        undef.move_to([0, -2.2, 0])
        undef_bx = _box(undef, VIOLET, BOX_FILL, 0.6, 0.15)

        self.play(FadeIn(undef_bx, scale=1.3), FadeIn(undef, scale=1.3), run_time=0.4)  # 4.4
        self.play(
            Circumscribe(undef_bx, color=VIOLET, run_time=0.5),
            Flash(undef, color=VIOLET, line_length=0.3, num_lines=10, run_time=0.3),
        )  # 4.9

        self.wait(max(0.3, dur - 4.9))

        # 1s silence
        self.wait(sil)

        self.play(FadeOut(VGroup(
            not_inf, ni_bx, not_zero, nz_bx, impossible, imp_bx,
            undef, undef_bx, g7
        )), run_time=0.3)

        # ═══════════════════════════════════════════════
        # S8: RESOLUTION (6.4s)
        # Three punches
        # ═══════════════════════════════════════════════
        dur = DUR("resolution")
        g8 = _neon_grid([0, 0], FW, FH, 0.6, GRID_COL, 0.12)
        self.add(g8)

        words = [
            ("NOT FORBIDDEN", ORANGE, 1.5),
            ("NOT BROKEN", RED, 0.0),
            ("JUST IMPOSSIBLE", GREEN, -1.5),
        ]

        mobs = []
        for text, color, y in words:
            t = Text(text, font_size=22, color=color, weight=BOLD)
            bx = _box(t, color, BOX_FILL, 0.5, 0.1)
            VGroup(bx, t).move_to([0, y, 0])
            mobs.append(VGroup(bx, t))

        for i, mob in enumerate(mobs):
            self.play(FadeIn(mob, shift=RIGHT*0.2 if i%2==0 else LEFT*0.2),
                      run_time=0.4)
            self.wait(0.3)
        # 3 * (0.4 + 0.3) = 2.1

        # "And now you know why"
        why = Text("and now you know why", font_size=16, color=WHITE, weight=BOLD)
        why.set_opacity(0.7).move_to([0, -3.2, 0])
        self.play(FadeIn(why), run_time=0.3)  # 2.4

        self.wait(max(0.3, dur - 2.4))

        self.play(FadeOut(VGroup(*mobs, why, g8)), run_time=0.3)

        # ═══════════════════════════════════════════════
        # S9: END CARD (2.5s CTA + 3s card)
        # ═══════════════════════════════════════════════
        end_grid = _neon_grid([0, 0], FW, FH, 0.8, GRID_COL, 0.1)
        self.add(end_grid)

        _A, _B = 1.2, 0.95
        liss_glow = ParametricFunction(
            lambda t: np.array([_A*np.sin(2*t), _B*np.sin(3*t), 0]),
            t_range=[0, TAU, 0.01],
            color=END_CYAN, stroke_width=6, stroke_opacity=0.2
        )
        liss_core = ParametricFunction(
            lambda t: np.array([_A*np.sin(2*t), _B*np.sin(3*t), 0]),
            t_range=[0, TAU, 0.01],
            color=END_CYAN, stroke_width=2, stroke_opacity=1.0
        )
        logo = VGroup(liss_glow, liss_core).move_to([0, 0.8, 0])
        wordmark = Text("ORBITAL", font_size=28, color=END_CYAN, weight=BOLD)
        wordmark.next_to(logo, DOWN, buff=0.3)
        tagline = Text("Watch it click.", font_size=14, color=WHITE)
        tagline.set_opacity(0.5).next_to(wordmark, DOWN, buff=0.15)

        self.play(Create(liss_core, run_time=0.8), FadeIn(liss_glow, run_time=0.6))
        self.play(FadeIn(wordmark, shift=UP*0.1), run_time=0.3)
        self.play(FadeIn(tagline), run_time=0.2)
        self.wait(1.5)
        self.play(FadeOut(VGroup(logo, wordmark, tagline, end_grid)), run_time=0.2)
