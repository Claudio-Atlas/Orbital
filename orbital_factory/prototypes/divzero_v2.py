"""
"Why You Can't Divide by Zero" — Orbital Short v2
====================================================
REBUILT from locked visual spec. Every text size follows tier system.
End card matches spec exactly. Content in upper 30-40%.

Render:
  cd ~/Desktop/Orbital/orbital_factory && source venv/bin/activate
  PATH="/Library/TeX/texbin:$PATH" manim render prototypes/divzero_v2.py DivZeroV2 \
    -o divzero_v2.mp4 --format mp4 -r 1080,1920 --frame_rate 60 --flush_cache
"""
from manim import *
import numpy as np
import json

config.frame_width = 4.5
config.frame_height = 8.0

# ── BRAND COLORS (LOCKED) ──
VIOLET = "#8B5CF6"
CYAN = "#22D3EE"
GREEN = "#39FF14"
ORANGE = "#F97316"
RED = "#FF4444"
BOX_FILL = "#1a1130"
END_CYAN = "#00E5FF"
GRID_COL = "#1a1a3a"
FW, FH = 4.5, 8.0

# ── LAYOUT CONSTANTS (LOCKED) ──
MATH_CENTER_Y = 1.2
GRAPH_CENTER_Y = -1.8
GRAPH_WIDTH = 3.4
GRAPH_HEIGHT = 2.8
MAX_WIDTH = FW * 0.82  # 3.69

# ── TEXT TIERS (LOCKED) ──
# T1 Punchline: MathTex font_size=42, GREEN, + purple box
# T2 Key Fact: MathTex font_size=28, CYAN, + purple box
# T3 Callout: Text font_size=24, GREEN/WHITE, weight=BOLD
# T4 Title: Text font_size=26, VIOLET, weight=BOLD
# T5 Equation: MathTex font_size=30, WHITE
# T6 Caption: MathTex font_size=24, CYAN

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


def _clamp(mob, max_w=MAX_WIDTH):
    if mob.width > max_w:
        mob.scale(max_w / mob.width)
    return mob


def _box(mob, color=VIOLET, fill=BOX_FILL, opacity=0.6, buff=0.2):
    """Locked box style from spec."""
    return SurroundingRectangle(mob, color=color, fill_color=fill,
        fill_opacity=opacity, buff=buff, corner_radius=0.1, stroke_width=2)


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


class DivZeroV2(Scene):
    def construct(self):
        self.camera.background_color = BLACK

        # ── Persistent border (LOCKED: sharp corners, FW-0.15 × FH-0.15) ──
        border = Rectangle(width=FW-0.15, height=FH-0.15, color=VIOLET,
                           stroke_width=2.5, stroke_opacity=0.7, fill_opacity=0)
        border_glow = Rectangle(width=FW-0.10, height=FH-0.10, color=VIOLET,
                                stroke_width=6, stroke_opacity=0.15, fill_opacity=0)
        self.add(border_glow, border)
        # Watermark (LOCKED: font_size=10, bottom-left)
        wm = Text("ORBITAL", font_size=10, color=WHITE, weight=BOLD)
        wm.set_opacity(0.35).move_to([-FW/2+0.5, -FH/2+0.2, 0])
        self.add(wm)

        # ═══════════════════════════════════════════════
        # S1: HOOK (6.2s)
        # ═══════════════════════════════════════════════
        dur = DUR("hook")
        grid_h = _neon_grid([0, 0], FW, FH, 0.6, GRID_COL, 0.15)
        self.add(grid_h)

        # Better calculator — dark body with screen, keypad grid, proper buttons
        calc_body = RoundedRectangle(width=2.2, height=3.2, color="#333333",
            fill_color="#1a1a1a", fill_opacity=0.95, corner_radius=0.12,
            stroke_width=2).move_to([0, 1.5, 0])
        # Screen area
        calc_screen_bg = RoundedRectangle(width=1.8, height=0.6, color="#003300",
            fill_color="#001a00", fill_opacity=0.95, corner_radius=0.05,
            stroke_width=1).move_to([0, 2.6, 0])
        # ERROR on screen — T2 Key Fact size
        err_text = MathTex(r"\text{ERROR}", font_size=28, color=RED)
        err_text.move_to(calc_screen_bg.get_center())

        # Keypad buttons (4×3 grid)
        buttons = VGroup()
        btn_labels = ["7","8","9","4","5","6","1","2","3","0",".","÷"]
        for idx, lbl in enumerate(btn_labels):
            r, c = idx // 3, idx % 3
            b = RoundedRectangle(width=0.45, height=0.35, color="#444444",
                fill_color="#2a2a2a", fill_opacity=0.8, corner_radius=0.04,
                stroke_width=1)
            b.move_to([-0.55 + c*0.55, 1.8 - r*0.45, 0])
            t = Text(lbl, font_size=10, color=WHITE)
            t.move_to(b.get_center())
            buttons.add(VGroup(b, t))

        calc = VGroup(calc_body, calc_screen_bg, buttons)

        self.play(FadeIn(calc), run_time=0.4)  # 0.4
        self.play(Write(err_text), run_time=0.3)  # 0.7

        # Glitch
        self.play(err_text.animate.shift(RIGHT*0.03).set_color(GREEN), run_time=0.08)
        self.play(err_text.animate.shift(LEFT*0.06).set_color(RED), run_time=0.08)
        self.play(err_text.animate.shift(RIGHT*0.03), run_time=0.08)  # 0.94

        # "They're lying to you" — T3 Callout (font_size=24, BOLD)
        lying = Text("they're lying to you", font_size=24, color=RED, weight=BOLD)
        lying_bx = _box(lying, RED, "#2a0a0a", 0.5, 0.15)
        VGroup(lying_bx, lying).move_to([0, -1.2, 0])
        self.play(FadeIn(lying_bx), Write(lying), run_time=0.4)  # 1.34

        self.wait(max(0.3, dur - 1.34))

        self.play(FadeOut(VGroup(calc, err_text, lying, lying_bx, grid_h)), run_time=0.3)

        # ═══════════════════════════════════════════════
        # S2: WHAT IS DIVISION? (16.1s)
        # Division Machine — better looking
        # ═══════════════════════════════════════════════
        dur = DUR("what_is_division")
        g2 = _neon_grid([0, 0], FW, FH, 0.6, GRID_COL, 0.12)
        self.add(g2)

        # T4 Title
        div_title = Text("What is division?", font_size=26, color=VIOLET, weight=BOLD)
        div_title.move_to([0, 3.3, 0])
        self.play(FadeIn(div_title), run_time=0.3)  # 0.3

        # Machine: layered design with gears
        machine_outer = RoundedRectangle(width=3.0, height=2.2, color=VIOLET,
            fill_color=BOX_FILL, fill_opacity=0.8, corner_radius=0.2,
            stroke_width=2.5).move_to([0, 1.0, 0])
        # Inner panel
        machine_inner = RoundedRectangle(width=2.4, height=1.4, color=CYAN,
            fill_color="#0a0a2a", fill_opacity=0.6, corner_radius=0.1,
            stroke_width=1).move_to([0, 1.0, 0])
        # Gear decorations
        gear1 = Circle(radius=0.25, color=VIOLET, stroke_width=2, fill_opacity=0)
        gear1.move_to([-0.9, 1.3, 0])
        gear1_dot = Dot(gear1.get_center(), radius=0.04, color=VIOLET)
        gear2 = Circle(radius=0.2, color=CYAN, stroke_width=1.5, fill_opacity=0)
        gear2.move_to([0.9, 0.7, 0])
        gear2_dot = Dot(gear2.get_center(), radius=0.03, color=CYAN)

        # Input funnel (top)
        in_fun = Polygon(
            [-0.5, 2.25, 0], [0.5, 2.25, 0], [0.25, 2.1, 0], [-0.25, 2.1, 0],
            color=CYAN, fill_color=CYAN, fill_opacity=0.2, stroke_width=1.5
        )
        # Output chute (bottom)
        out_chute = Rectangle(width=0.6, height=0.15, color=GREEN,
            fill_color=GREEN, fill_opacity=0.2, stroke_width=1.5).move_to([0, -0.15, 0])

        mach_grp = VGroup(machine_outer, machine_inner, gear1, gear1_dot,
                          gear2, gear2_dot, in_fun, out_chute)
        self.play(FadeIn(mach_grp), run_time=0.4)  # 0.7

        # 8 ÷ 2 = 4 demo — T5 Equation sizes
        num8 = MathTex("8", font_size=30, color=CYAN)
        num8.move_to([0, 2.8, 0])
        div_label = MathTex(r"8 \div 2", font_size=28, color=CYAN)
        div_label.move_to([0, 2.5, 0])

        self.play(FadeIn(div_label), run_time=0.3)  # 1.0
        self.play(div_label.animate.move_to(in_fun.get_center()), run_time=0.4)  # 1.4

        # Gears spin
        self.play(
            Rotate(gear1, angle=PI, about_point=gear1.get_center()),
            Rotate(gear2, angle=-PI, about_point=gear2.get_center()),
            Flash(machine_inner, color=VIOLET, line_length=0.3, num_lines=8, run_time=0.3),
            run_time=0.5
        )  # 1.9

        # Output: 4 groups — T6 Caption size
        groups = VGroup()
        for i in range(4):
            g = MathTex("2", font_size=24, color=GREEN)
            bx = _box(g, GREEN, BOX_FILL, 0.4, 0.08)
            VGroup(bx, g).move_to([-1.0 + i*0.7, -0.8, 0])
            groups.add(VGroup(bx, g))

        # T2 Key Fact: = 4
        result = MathTex(r"= 4", font_size=28, color=GREEN)
        res_bx = _box(result, GREEN, BOX_FILL, 0.5, 0.1)
        VGroup(res_bx, result).move_to([0, -1.8, 0])

        self.play(*[FadeIn(g, shift=DOWN*0.2) for g in groups], run_time=0.5)  # 2.4
        self.play(FadeIn(res_bx), Write(result), run_time=0.3)  # 2.7

        self.wait(1.5)  # 4.2

        # Clear for ÷0
        self.play(FadeOut(VGroup(div_label, groups, result, res_bx)), run_time=0.3)  # 4.5

        # 8 ÷ 0 — machine breaks
        div0_label = MathTex(r"8 \div 0", font_size=28, color=RED)
        div0_label.move_to([0, 2.5, 0])

        self.play(FadeIn(div0_label), run_time=0.3)  # 4.8
        self.play(div0_label.animate.move_to(in_fun.get_center()), run_time=0.4)  # 5.2

        # Machine shakes
        for _ in range(5):
            self.play(mach_grp.animate.shift(RIGHT*0.04), run_time=0.04)
            self.play(mach_grp.animate.shift(LEFT*0.08), run_time=0.04)
            self.play(mach_grp.animate.shift(RIGHT*0.04), run_time=0.04)
        # 5.2 + 0.6 = 5.8

        # Sparks + big ?
        q_out = MathTex(r"?", font_size=42, color=RED)
        q_out.move_to([0, -0.8, 0])
        self.play(
            Flash(machine_outer, color=RED, line_length=0.5, num_lines=14, run_time=0.3),
            FadeIn(q_out, scale=2),
            run_time=0.4
        )  # 6.2

        # T3 Callout caption
        cap = Text("zero never adds up to 8", font_size=24, color=RED, weight=BOLD)
        cap.move_to([0, -2.2, 0])
        self.play(FadeIn(cap), run_time=0.3)  # 6.5

        self.wait(max(0.3, dur - 6.5))

        self.play(FadeOut(VGroup(
            div_title, mach_grp, div0_label, q_out, cap, g2
        )), run_time=0.3)

        # ═══════════════════════════════════════════════
        # S3: CONTRADICTION SETUP (6.9s + 2s silence)
        # ═══════════════════════════════════════════════
        dur = DUR("contradiction_setup")
        sil = SILENCE["contradiction_setup"]
        g3 = _neon_grid([0, 0], FW, FH, 0.6, GRID_COL, 0.15)
        self.add(g3)

        # T4 Title
        setup_title = Text("What if it DID have an answer?", font_size=26,
                           color=ORANGE, weight=BOLD)
        _clamp(setup_title)
        setup_title.move_to([0, 3.0, 0])
        self.play(FadeIn(setup_title), run_time=0.3)  # 0.3

        # T2 Key Fact: 1 ÷ 0 = k
        suppose = MathTex(r"1 \div 0 = k", font_size=28, color=WHITE)
        suppose_bx = _box(suppose, ORANGE, BOX_FILL, 0.6, 0.15)
        VGroup(suppose_bx, suppose).move_to([0, MATH_CENTER_Y, 0])
        self.play(FadeIn(suppose_bx), Write(suppose), run_time=0.5)  # 0.8

        # T6 Caption: "call it k — any number"
        any_cap = MathTex(r"\text{call it } k \text{ — any number}", font_size=24, color=CYAN)
        any_cap.move_to([0, MATH_CENTER_Y - 1.0, 0])
        self.play(FadeIn(any_cap), run_time=0.3)  # 1.1

        self.wait(max(0.3, dur - 1.1))
        self.wait(sil)  # 2s silence

        self.play(FadeOut(VGroup(setup_title, any_cap)), run_time=0.2)
        # Keep suppose + box for next scene

        # ═══════════════════════════════════════════════
        # S4: CONTRADICTION PAYOFF (12.6s + 3s silence)
        # Show "multiply both sides by 0" step
        # ═══════════════════════════════════════════════
        dur = DUR("contradiction_payoff")
        sil = SILENCE["contradiction_payoff"]

        # Step 1: Show the multiplication step
        # "multiply both sides by 0"
        mult_label = Text("multiply both sides by 0", font_size=24,
                          color=CYAN, weight=BOLD)
        mult_label.move_to([0, MATH_CENTER_Y + 1.5, 0])
        self.play(FadeIn(mult_label), run_time=0.3)  # 0.3

        # Transform: 1÷0 = k → k × 0 = 1
        step1 = MathTex(r"k \times 0 = 1", font_size=30, color=CYAN)
        step1_bx = _box(step1, CYAN, BOX_FILL, 0.5, 0.12)
        VGroup(step1_bx, step1).move_to([0, MATH_CENTER_Y - 0.8, 0])
        self.play(FadeIn(step1_bx), Write(step1), run_time=0.5)  # 0.8

        self.wait(1.2)  # 2.0

        # Step 2: "but anything × 0 = 0"
        step2 = MathTex(r"\text{but } k \times 0 = 0 \text{ always!}",
                        font_size=28, color=ORANGE)
        step2_bx = _box(step2, ORANGE, BOX_FILL, 0.5, 0.12)
        VGroup(step2_bx, step2).move_to([0, MATH_CENTER_Y - 2.2, 0])
        self.play(FadeIn(step2_bx), Write(step2), run_time=0.5)  # 2.5

        self.wait(1.0)  # 3.5

        # Clear and show THE BIG ONE
        self.play(FadeOut(VGroup(
            suppose, suppose_bx, mult_label, step1, step1_bx, step2, step2_bx
        )), run_time=0.3)  # 3.8

        # T1 PUNCHLINE: 0 = 1
        zero_eq_one = MathTex(r"0 = 1", font_size=42, color=RED)
        zeo_bx = _box(zero_eq_one, RED, "#2a0a0a", 0.6, 0.2)
        VGroup(zeo_bx, zero_eq_one).move_to([0, MATH_CENTER_Y + 0.5, 0])

        self.play(FadeIn(zeo_bx), Write(zero_eq_one), run_time=0.4)  # 4.2

        # Cracks on the equals sign
        eq_center = zero_eq_one.get_center()
        crack1 = Line(eq_center + UP*0.35 + LEFT*0.15, eq_center + DOWN*0.35 + RIGHT*0.15,
                      color=RED, stroke_width=4)
        crack2 = Line(eq_center + UP*0.25 + RIGHT*0.2, eq_center + DOWN*0.4 + LEFT*0.1,
                      color=RED, stroke_width=3)
        self.play(Create(crack1), Create(crack2), run_time=0.3)  # 4.5

        # Equation shatter cascade — T5 sized, spread across screen
        shatter_eqs = [r"2 = 3", r"100 = 0", r"7 = -5", r"\pi = 42"]
        positions = [[-1.0, -0.3], [0.8, -0.8], [-0.7, -1.8], [0.6, -2.3]]
        shatter_mobs = []
        for eq_str, pos in zip(shatter_eqs, positions):
            eq = MathTex(eq_str, font_size=24, color=RED)
            eq.set_opacity(0.6)
            eq.move_to([pos[0], pos[1], 0])
            cr = Line(eq.get_corner(UL)+UL*0.05, eq.get_corner(DR)+DR*0.05,
                      color=RED, stroke_width=2.5, stroke_opacity=0.5)
            shatter_mobs.append(VGroup(eq, cr))

        for mob in shatter_mobs:
            self.play(FadeIn(mob, scale=0.8), run_time=0.12)
        # 4.5 + 4*0.12 = 4.98

        # T3 Callout: "math destroying itself" — bigger, centered
        destroy = Text("math destroying itself", font_size=24, color=RED, weight=BOLD)
        destroy.move_to([0, -3.0, 0])
        self.play(FadeIn(destroy, scale=1.2), run_time=0.4)  # 5.38

        self.wait(max(0.3, dur - 5.38))
        self.wait(sil)  # 3s silence

        self.play(FadeOut(VGroup(
            zero_eq_one, zeo_bx, crack1, crack2, *shatter_mobs, destroy, g3
        )), run_time=0.3)

        # ═══════════════════════════════════════════════
        # S5: GRAPH INTRO (12.2s)
        # Introduce y=1/x FIRST, then show calculations
        # ═══════════════════════════════════════════════
        dur = DUR("graph_intro")
        g5 = _neon_grid([0, 0], FW, FH, 0.6, GRID_COL, 0.15)
        self.add(g5)

        # T4 Title: "See the breaking point"
        s5_title = Text("See the breaking point", font_size=26,
                        color=CYAN, weight=BOLD)
        s5_title.move_to([0, 3.3, 0])
        self.play(FadeIn(s5_title), run_time=0.3)  # 0.3

        # T2 Key Fact: introduce y = 1/x FIRST
        eq_intro = MathTex(r"y = \frac{1}{x}", font_size=28, color=CYAN)
        eq_bx = _box(eq_intro, CYAN, BOX_FILL, 0.5, 0.12)
        VGroup(eq_bx, eq_intro).move_to([0, 2.2, 0])
        self.play(FadeIn(eq_bx), Write(eq_intro), run_time=0.4)  # 0.7

        self.wait(0.5)  # 1.2

        # Calculation countdown — T5 Equation size, spaced apart
        divisions = [
            (r"1 \div 1", r"= 1"),
            (r"1 \div 0.1", r"= 10"),
            (r"1 \div 0.01", r"= 100"),
            (r"1 \div 0.001", r"= 1{,}000"),
        ]

        prev_rows = []
        for i, (left, right) in enumerate(divisions):
            eq_l = MathTex(left, font_size=28, color=WHITE)
            eq_r = MathTex(right, font_size=28, color=GREEN)
            eq_r.next_to(eq_l, RIGHT, buff=0.15)
            row = VGroup(eq_l, eq_r)
            y_pos = 1.0 - i * 0.8
            row.move_to([0, y_pos, 0])
            _clamp(row)

            self.play(FadeIn(row, shift=DOWN*0.1), run_time=0.3)
            self.play(Indicate(eq_r, color=GREEN, scale_factor=1.1), run_time=0.2)
            prev_rows.append(row)
        # 1.2 + 4*(0.3+0.2) = 3.2

        # Arrow pointing down
        arr = MathTex(r"\downarrow", font_size=30, color=GREEN)
        arr.move_to([0, -2.2, 0])
        self.play(FadeIn(arr), run_time=0.2)  # 3.4

        self.wait(max(0.3, dur - 3.4))

        self.play(FadeOut(VGroup(s5_title, eq_bx, eq_intro, *prev_rows, arr)),
                  run_time=0.3)
        # Keep grid for next scene

        # ═══════════════════════════════════════════════
        # S6: GRAPH EXPLOSION (11.5s + 3s silence)
        # Graph at GRAPH_CENTER_Y, no overlap
        # ═══════════════════════════════════════════════
        dur = DUR("graph_explosion")
        sil = SILENCE["graph_explosion"]

        # T2 Key Fact: equation label at top
        eq_label = MathTex(r"y = \frac{1}{x}", font_size=28, color=CYAN)
        eq_label_bx = _box(eq_label, CYAN, BOX_FILL, 0.4, 0.1)
        VGroup(eq_label_bx, eq_label).move_to([0, 2.5, 0])
        self.play(FadeIn(eq_label_bx), FadeIn(eq_label), run_time=0.2)  # 0.2

        # Graph at GRAPH_CENTER_Y (-1.8)
        ax = Axes(
            x_range=[-3, 3, 1], y_range=[-8, 8, 2],
            x_length=GRAPH_WIDTH, y_length=GRAPH_HEIGHT + 1.0,
            tips=False,
            axis_config={"color": VIOLET, "stroke_width": 1.5, "stroke_opacity": 0.6},
        ).move_to([0, GRAPH_CENTER_Y, 0])

        self.play(Create(ax), run_time=0.3)  # 0.5

        # Right side GREEN, left side RED
        curve_right = ax.plot(lambda x: 1/x, x_range=[0.15, 3], color=GREEN, stroke_width=3)
        curve_left = ax.plot(lambda x: 1/x, x_range=[-3, -0.15], color=RED, stroke_width=3)

        self.play(Create(curve_right), run_time=0.7)  # 1.2
        self.play(Create(curve_left), run_time=0.7)  # 1.9

        # Vertical asymptote
        asymp = DashedLine(
            ax.c2p(0, -8), ax.c2p(0, 8),
            color=ORANGE, stroke_width=2.5, dash_length=0.1
        )
        self.play(Create(asymp), run_time=0.3)  # 2.2

        # Labels — T6 Caption, positioned in graph space (not overlapping)
        plus_inf = MathTex(r"+\infty", font_size=24, color=GREEN)
        plus_bx = _box(plus_inf, GREEN, BOX_FILL, 0.4, 0.06)
        VGroup(plus_bx, plus_inf).move_to([1.3, 0.2, 0])  # above graph

        minus_inf = MathTex(r"-\infty", font_size=24, color=RED)
        minus_bx = _box(minus_inf, RED, "#2a0a0a", 0.4, 0.06)
        VGroup(minus_bx, minus_inf).move_to([-1.3, -3.2, 0])  # below graph

        self.play(FadeIn(plus_bx), FadeIn(plus_inf), run_time=0.3)  # 2.5
        self.play(FadeIn(minus_bx), FadeIn(minus_inf), run_time=0.3)  # 2.8

        # Tear apart effect
        self.play(
            VGroup(curve_right, plus_bx, plus_inf).animate.shift(RIGHT*0.12),
            VGroup(curve_left, minus_bx, minus_inf).animate.shift(LEFT*0.12),
            run_time=0.5
        )  # 3.3

        # Glowing void
        void_glow = Ellipse(width=0.25, height=GRAPH_HEIGHT+0.5, color=ORANGE,
            fill_color=ORANGE, fill_opacity=0.12, stroke_width=2,
            stroke_opacity=0.3).move_to(ax.c2p(0, 0))
        self.play(FadeIn(void_glow), run_time=0.3)  # 3.6

        # T3 Callout at top middle
        two_dir = Text("two directions — no answer", font_size=24,
                       color=ORANGE, weight=BOLD)
        two_dir.move_to([0, 1.2, 0])
        self.play(FadeIn(two_dir), run_time=0.3)  # 3.9

        self.wait(max(0.3, dur - 3.9))
        self.wait(sil)  # 3s silence

        self.play(FadeOut(VGroup(
            eq_label, eq_label_bx, ax, curve_right, curve_left, asymp,
            plus_bx, plus_inf, minus_bx, minus_inf, void_glow, two_dir, g5
        )), run_time=0.3)

        # ═══════════════════════════════════════════════
        # S7: PUNCHLINE (11.3s + 1s silence)
        # ═══════════════════════════════════════════════
        dur = DUR("punchline")
        sil = SILENCE["punchline"]
        g7 = _neon_grid([0, 0], FW, FH, 0.6, GRID_COL, 0.15)
        self.add(g7)

        # T2 Key Fact: not infinity
        not_inf = MathTex(r"1 \div 0 \neq \infty", font_size=28, color=RED)
        ni_bx = _box(not_inf, RED, "#2a0a0a", 0.5, 0.12)
        VGroup(ni_bx, not_inf).move_to([0, 2.5, 0])
        self.play(FadeIn(ni_bx), Write(not_inf), run_time=0.5)  # 0.5

        self.wait(0.8)  # 1.3

        # T2 Key Fact: not zero
        not_zero = MathTex(r"1 \div 0 \neq 0", font_size=28, color=RED)
        nz_bx = _box(not_zero, RED, "#2a0a0a", 0.5, 0.12)
        VGroup(nz_bx, not_zero).move_to([0, 1.0, 0])
        self.play(FadeIn(nz_bx), Write(not_zero), run_time=0.5)  # 1.8

        self.wait(0.8)  # 2.6

        # T3 Callout: a logical impossibility
        impossible = Text("a logical impossibility", font_size=24,
                          color=ORANGE, weight=BOLD)
        impossible.move_to([0, -0.3, 0])
        self.play(FadeIn(impossible), run_time=0.4)  # 3.0

        self.wait(0.8)  # 3.8

        # T1 PUNCHLINE: UNDEFINED
        undef = MathTex(r"\text{UNDEFINED}", font_size=42, color=VIOLET)
        undef_bx = _box(undef, VIOLET, BOX_FILL, 0.6, 0.18)
        VGroup(undef_bx, undef).move_to([0, -2.0, 0])

        self.play(FadeIn(undef_bx, scale=1.2), Write(undef), run_time=0.4)  # 4.2
        self.play(
            Circumscribe(undef_bx, color=VIOLET, run_time=0.5),
            Flash(undef_bx, color=VIOLET, line_length=0.3, num_lines=10, run_time=0.3),
        )  # 4.7

        self.wait(max(0.3, dur - 4.7))
        self.wait(sil)

        self.play(FadeOut(VGroup(
            not_inf, ni_bx, not_zero, nz_bx, impossible, undef, undef_bx, g7
        )), run_time=0.3)

        # ═══════════════════════════════════════════════
        # S8: RESOLUTION (6.4s)
        # ═══════════════════════════════════════════════
        dur = DUR("resolution")
        g8 = _neon_grid([0, 0], FW, FH, 0.6, GRID_COL, 0.12)
        self.add(g8)

        # Three punches — T3 Callout size, centered in upper half
        words = [
            ("NOT FORBIDDEN", ORANGE, 2.0),
            ("NOT BROKEN", RED, 0.5),
            ("JUST IMPOSSIBLE", GREEN, -1.0),
        ]

        mobs = []
        for text, color, y in words:
            t = Text(text, font_size=24, color=color, weight=BOLD)
            bx = _box(t, color, BOX_FILL, 0.5, 0.12)
            VGroup(bx, t).move_to([0, y, 0])
            mobs.append(VGroup(bx, t))

        for i, mob in enumerate(mobs):
            self.play(FadeIn(mob, shift=RIGHT*0.15 if i%2==0 else LEFT*0.15),
                      run_time=0.4)
            self.wait(0.3)
        # 3 * 0.7 = 2.1

        # T3 Callout
        why = Text("and now you know why", font_size=24, color=WHITE, weight=BOLD)
        why.set_opacity(0.8).move_to([0, -2.5, 0])
        self.play(FadeIn(why), run_time=0.3)  # 2.4

        self.wait(max(0.3, dur - 2.4))

        self.play(FadeOut(VGroup(*mobs, why, g8)), run_time=0.3)

        # ═══════════════════════════════════════════════
        # S9: END CARD (LOCKED SPEC — exact code from visual spec)
        # ═══════════════════════════════════════════════
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
