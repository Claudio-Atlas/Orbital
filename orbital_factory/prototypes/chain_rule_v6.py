"""
Why the Chain Rule Works (It's Just Multiplication) — v6
=========================================================
Full formula walkthrough with TTS for every step.
3 formula scenes: general → specific derivative → plug in x=2.
All text large. Nothing cramped. Each step explained.

Render:
  cd ~/Desktop/Orbital/orbital_factory && source venv/bin/activate
  PATH="/Library/TeX/texbin:$PATH" manim render prototypes/chain_rule_v6.py ChainRuleV6 \
    -o chain_rule_v6.mp4 --format mp4 -r 1080,1920 --frame_rate 60 --flush_cache
"""
from manim import *
import numpy as np
import json

config.frame_width = 4.5
config.frame_height = 8.0

# ── LOCKED VISUAL SPEC ──
VIOLET = "#8B5CF6"
CYAN = "#22D3EE"
GREEN = "#39FF14"
ORANGE = "#F97316"
BOX_BORDER = "#8B5CF6"
BOX_FILL = "#1a1130"
END_CYAN = "#00E5FF"
FRAME_W = 4.5
FRAME_H = 8.0
MAX_WIDTH = FRAME_W * 0.82

# ── FONT SIZES ──
FS_PUNCHLINE = 42
FS_KEY_FACT = 28
FS_CALLOUT = 24
FS_TITLE = 26
FS_EQUATION = 30
FS_CAPTION = 24
FS_WATERMARK = 10

# ── TTS ──
with open("output/tts/chain_rule_v6_scenes/manifest.json") as f:
    _manifest = json.load(f)
    MANIFEST = {s["scene"]: s for s in _manifest}

def AUDIO(scene): return MANIFEST[scene]["audio_path"]
def DUR(scene): return MANIFEST[scene]["duration"]

def _clamp(mob, max_w=None):
    if max_w is None: max_w = MAX_WIDTH
    if mob.width > max_w: mob.scale(max_w / mob.width)
    return mob


def _make_gear(radius, n_teeth, color, center, tooth_len=0.14, stroke_w=2.5):
    parts = []
    circle = Circle(radius=radius, color=color, stroke_width=stroke_w,
                    fill_color=BOX_FILL, fill_opacity=0.4)
    circle.move_to(center)
    parts.append(circle)
    center_dot = Dot(radius=0.06, color=color, fill_opacity=0.8).move_to(center)
    parts.append(center_dot)
    for i in range(n_teeth):
        angle = i * TAU / n_teeth
        inner_pt = np.array(center) + radius * np.array([np.cos(angle), np.sin(angle), 0])
        outer_pt = np.array(center) + (radius + tooth_len) * np.array([np.cos(angle), np.sin(angle), 0])
        perp = np.array([-np.sin(angle), np.cos(angle), 0])
        tw = 0.08
        tooth = Polygon(
            inner_pt + perp*tw, inner_pt - perp*tw,
            outer_pt - perp*tw*0.7, outer_pt + perp*tw*0.7,
            color=color, stroke_width=stroke_w-0.5, fill_color=color, fill_opacity=0.3
        )
        parts.append(tooth)
    return VGroup(*parts)


def _make_machine_vert(label, sublabel, color, center, width=2.8, height=1.1):
    box = RoundedRectangle(
        width=width, height=height, color=color, fill_color=BOX_FILL,
        fill_opacity=0.7, stroke_width=2.5, corner_radius=0.12,
    )
    box.move_to(center)
    lbl = Text(label, font_size=26, color=color, weight=BOLD)
    lbl.move_to(box.get_center() + UP * 0.15)
    sub = MathTex(sublabel, font_size=22, color=WHITE)
    sub.set_opacity(0.8)
    sub.move_to(box.get_center() + DOWN * 0.22)
    in_port = Dot(radius=0.07, color=color).move_to(box.get_top())
    out_port = Dot(radius=0.07, color=color).move_to(box.get_bottom())
    return VGroup(box, lbl, sub, in_port, out_port)


def _number_bubble(value, color=CYAN, fs=FS_KEY_FACT):
    num = MathTex(str(value), font_size=fs, color=color)
    circ = Circle(radius=0.35, color=color, fill_color=color, fill_opacity=0.15, stroke_width=1.5)
    circ.move_to(num.get_center())
    return VGroup(circ, num)


class ChainRuleV6(Scene):
    def construct(self):
        self.camera.background_color = BLACK

        # ── Border + Watermark ──
        border = Rectangle(
            width=FRAME_W-0.15, height=FRAME_H-0.15,
            color=VIOLET, stroke_width=2.5, stroke_opacity=0.7, fill_opacity=0,
        ).move_to(ORIGIN)
        border_glow = Rectangle(
            width=FRAME_W-0.10, height=FRAME_H-0.10,
            color=VIOLET, stroke_width=6, stroke_opacity=0.15, fill_opacity=0,
        ).move_to(ORIGIN)
        self.add(border_glow, border)
        wm = Text("ORBITAL", font_size=FS_WATERMARK, color=WHITE, weight=BOLD)
        wm.set_opacity(0.35).move_to([-FRAME_W/2+0.5, -FRAME_H/2+0.2, 0])
        self.add(wm)

        # ═════════════════════════════════════════════════════
        # SCENE 1: HOOK (5s)
        # ═════════════════════════════════════════════════════
        dur = DUR("hook")

        gear1 = _make_gear(0.8, 12, VIOLET, [-0.55, 2.5, 0], tooth_len=0.17)
        gear2 = _make_gear(0.55, 8, CYAN, [0.75, 2.5, 0], tooth_len=0.14)

        scary = MathTex(
            r"\frac{d}{dx}[f(g(x))] = f'(g(x)) \cdot g'(x)",
            font_size=FS_CALLOUT, color=WHITE
        )
        _clamp(scary)
        scary.move_to([0, 0.6, 0])
        scary_box = SurroundingRectangle(
            scary, color=BOX_BORDER, fill_color=BOX_FILL,
            fill_opacity=0.6, buff=0.2, corner_radius=0.1, stroke_width=2.5,
        )
        hook_text = Text("Just multiplication.", font_size=FS_KEY_FACT, color=GREEN, weight=BOLD)
        _clamp(hook_text)
        hook_text.move_to([0, -0.5, 0])

        self.add_sound(AUDIO("hook"))
        self.play(FadeIn(gear1), FadeIn(gear2), run_time=0.3)
        self.play(
            Rotate(gear1, PI/3, about_point=[-0.55, 2.5, 0]),
            Rotate(gear2, -PI/2.2, about_point=[0.75, 2.5, 0]),
            run_time=1.2
        )
        self.play(FadeIn(scary_box), Write(scary), run_time=0.6)
        self.wait(0.5)
        self.play(FadeIn(hook_text, shift=UP*0.2), run_time=0.3)
        self.wait(max(0.5, dur - 2.9))

        # ═════════════════════════════════════════════════════
        # SCENE 2: COMPOSITION (12s)
        # ═════════════════════════════════════════════════════
        dur = DUR("composition")
        self.play(FadeOut(VGroup(gear1, gear2, scary, scary_box, hook_text)), run_time=0.5)

        expr = MathTex(r"(3x)^2", font_size=60, color=WHITE)
        _clamp(expr, MAX_WIDTH * 0.6)
        expr.move_to([0, 3.0, 0])

        self.add_sound(AUDIO("composition"))
        self.play(Write(expr), run_time=0.6)
        self.wait(1.5)

        inner_hl = SurroundingRectangle(
            expr[0][1:3], color=ORANGE, stroke_width=2.5, buff=0.06, corner_radius=0.05
        )
        inner_lbl = Text("Step 1: Triple", font_size=18, color=ORANGE, weight=BOLD)
        inner_lbl.next_to(inner_hl, DOWN, buff=0.2)
        outer_hl = SurroundingRectangle(
            expr[0], color=CYAN, stroke_width=2.5, buff=0.1, corner_radius=0.05
        )
        outer_lbl = Text("Step 2: Square", font_size=18, color=CYAN, weight=BOLD)
        outer_lbl.next_to(outer_hl, UP, buff=0.2)

        self.play(Create(inner_hl), FadeIn(inner_lbl), run_time=0.5)
        self.wait(1.0)
        self.play(Create(outer_hl), FadeIn(outer_lbl), run_time=0.5)
        self.wait(1.0)

        # Vertical pipeline
        M1_Y = 0.8
        M2_Y = -1.2
        machine1 = _make_machine_vert("TRIPLE", r"u = 3x", ORANGE, [0, M1_Y, 0])
        machine2 = _make_machine_vert("SQUARE", r"y = u^2", CYAN, [0, M2_Y, 0])
        pipe_arrow = Arrow(
            machine1[0].get_bottom() + DOWN*0.1, machine2[0].get_top() + UP*0.1,
            color=WHITE, stroke_width=2.5, buff=0, max_tip_length_to_length_ratio=0.2,
        )
        in_arrow = Arrow(
            [0, M1_Y + 1.1, 0], machine1[0].get_top() + UP*0.1,
            color=WHITE, stroke_width=2, buff=0, max_tip_length_to_length_ratio=0.2,
        )
        in_label = MathTex("x", font_size=FS_CAPTION, color=WHITE)
        in_label.next_to(in_arrow, UP, buff=0.08)
        out_arrow = Arrow(
            machine2[0].get_bottom() + DOWN*0.1, [0, M2_Y - 1.1, 0],
            color=WHITE, stroke_width=2, buff=0, max_tip_length_to_length_ratio=0.2,
        )
        out_label = MathTex("y", font_size=FS_CAPTION, color=WHITE)
        out_label.next_to(out_arrow, DOWN, buff=0.08)

        self.play(
            FadeOut(VGroup(inner_hl, inner_lbl, outer_hl, outer_lbl)),
            expr.animate.move_to([0, 3.3, 0]).set_opacity(0.6),
            run_time=0.5
        )
        self.play(Create(in_arrow), FadeIn(in_label), FadeIn(machine1), run_time=0.6)
        self.play(Create(pipe_arrow), run_time=0.3)
        self.play(FadeIn(machine2), Create(out_arrow), FadeIn(out_label), run_time=0.6)
        self.wait(max(0.3, dur - 8.1))

        # ═════════════════════════════════════════════════════
        # SCENE 3: PICK X=2 (5s)
        # ═════════════════════════════════════════════════════
        dur = DUR("pick_x")
        self.add_sound(AUDIO("pick_x"))

        pick_text = MathTex(r"x = 2", font_size=FS_PUNCHLINE, color=GREEN)
        pick_text.next_to(in_arrow, RIGHT, buff=0.35)
        self.play(Write(pick_text), run_time=0.5)
        self.play(Circumscribe(pick_text, color=GREEN, run_time=0.5))
        self.wait(max(0.5, dur - 1.0))

        # ═════════════════════════════════════════════════════
        # SCENE 4: FLOW THROUGH (8s)
        # ═════════════════════════════════════════════════════
        dur = DUR("flow")
        self.add_sound(AUDIO("flow"))

        num2 = _number_bubble(2, GREEN, FS_KEY_FACT)
        num2.move_to(in_label.get_center())
        num6 = _number_bubble(6, ORANGE, FS_KEY_FACT)
        num6.move_to(machine1.get_center())
        num36 = _number_bubble(36, CYAN, FS_KEY_FACT)
        num36.move_to(machine2.get_center())

        self.play(FadeIn(num2, scale=0.5), run_time=0.3)
        self.play(num2.animate.move_to(machine1.get_center()), run_time=0.6)
        self.play(
            FadeOut(num2), FadeIn(num6, scale=1.3),
            Flash(machine1[0], color=ORANGE, line_length=0.3, num_lines=10, run_time=0.3),
            run_time=0.5
        )
        calc1 = MathTex(r"3(2) = 6", font_size=20, color=ORANGE)
        calc1.next_to(machine1[0], DOWN, buff=0.15).shift(LEFT * 0.8)
        self.play(FadeIn(calc1), run_time=0.3)
        self.wait(0.5)

        self.play(num6.animate.move_to(pipe_arrow.get_center()), run_time=0.3)
        self.play(num6.animate.move_to(machine2.get_center()), run_time=0.3)
        self.play(
            FadeOut(num6), FadeIn(num36, scale=1.3),
            Flash(machine2[0], color=CYAN, line_length=0.3, num_lines=10, run_time=0.3),
            run_time=0.5
        )
        calc2 = MathTex(r"6^2 = 36", font_size=20, color=CYAN)
        calc2.next_to(machine2[0], DOWN, buff=0.15).shift(LEFT * 0.8)
        self.play(FadeIn(calc2), run_time=0.3)
        self.play(num36.animate.move_to(out_label.get_center()), run_time=0.4)
        self.play(FadeOut(num36), run_time=0.2)
        self.wait(max(0.3, dur - 4.2))
        self.play(FadeOut(calc1), FadeOut(calc2), FadeOut(pick_text), run_time=0.3)

        # ═════════════════════════════════════════════════════
        # SCENE 5: RATE 1 (8s)
        # ═════════════════════════════════════════════════════
        dur = DUR("rate1")
        m1_glow = SurroundingRectangle(
            machine1[0], color=ORANGE, stroke_width=3, buff=0.1,
            corner_radius=0.15, fill_color=ORANGE, fill_opacity=0.08
        )
        self.add_sound(AUDIO("rate1"))
        self.play(
            Create(m1_glow),
            machine2.animate.set_opacity(0.2),
            pipe_arrow.animate.set_opacity(0.2),
            out_arrow.animate.set_opacity(0.2),
            out_label.animate.set_opacity(0.2),
            run_time=0.4
        )
        rate1_eq = MathTex(r"\frac{d}{dx}[3x] = 3", font_size=FS_CALLOUT, color=ORANGE)
        rate1_eq.move_to([0, M1_Y - 1.0, 0])
        _clamp(rate1_eq)
        rate1_label = Text("Every nudge to x gets tripled", font_size=16, color=WHITE)
        rate1_label.set_opacity(0.7)
        rate1_label.move_to([0, M1_Y - 1.5, 0])
        self.play(Write(rate1_eq), run_time=0.6)
        self.wait(0.5)
        self.play(FadeIn(rate1_label), run_time=0.3)

        rate1_badge = MathTex(r"\times 3", font_size=22, color=ORANGE)
        rate1_badge_box = SurroundingRectangle(
            rate1_badge, color=ORANGE, fill_color=BOX_FILL,
            fill_opacity=0.8, buff=0.08, corner_radius=0.06, stroke_width=1.5,
        )
        rate1_badge_grp = VGroup(rate1_badge_box, rate1_badge)
        rate1_badge_grp.move_to(machine1[0].get_corner(UR) + DL * 0.25)
        self.play(FadeIn(rate1_badge_grp), run_time=0.3)
        self.wait(max(1.0, dur - 2.1))

        # ═════════════════════════════════════════════════════
        # SCENE 6: RATE 2 (13s)
        # ═════════════════════════════════════════════════════
        dur = DUR("rate2")
        self.play(
            FadeOut(m1_glow), FadeOut(rate1_eq), FadeOut(rate1_label),
            machine1.animate.set_opacity(0.2),
            machine2.animate.set_opacity(1.0),
            pipe_arrow.animate.set_opacity(1.0),
            run_time=0.4
        )
        m2_glow = SurroundingRectangle(
            machine2[0], color=CYAN, stroke_width=3, buff=0.1,
            corner_radius=0.15, fill_color=CYAN, fill_opacity=0.08
        )
        self.add_sound(AUDIO("rate2"))
        self.play(Create(m2_glow), run_time=0.3)

        deriv_line1 = MathTex(r"\frac{d}{du}[u^2] = 2u", font_size=FS_CALLOUT, color=CYAN)
        deriv_line1.move_to([0, M2_Y - 1.2, 0])
        _clamp(deriv_line1)
        self.play(Write(deriv_line1), run_time=0.7)
        self.wait(1.0)

        # Show where u comes from
        u_reminder = MathTex(r"u = 3x", font_size=20, color=WHITE)
        u_reminder.set_opacity(0.6)
        u_reminder.move_to([0, M2_Y - 1.8, 0])
        self.play(FadeIn(u_reminder), run_time=0.3)
        self.wait(0.3)

        # At x=2, u=6
        at_x2_line = MathTex(r"\text{at } x = 2: \quad u = 3(2) = 6", font_size=20, color=GREEN)
        at_x2_line.move_to([0, M2_Y - 2.2, 0])
        _clamp(at_x2_line)
        self.play(Write(at_x2_line), run_time=0.5)
        self.wait(0.5)

        # So 2(6) = 12
        deriv_line2 = MathTex(r"2(6) = 12", font_size=FS_CALLOUT, color=CYAN)
        deriv_line2.move_to([0, M2_Y - 2.8, 0])
        _clamp(deriv_line2)
        self.play(Write(deriv_line2), run_time=0.7)
        self.wait(0.8)

        rate2_badge = MathTex(r"\times 12", font_size=22, color=CYAN)
        rate2_badge_box = SurroundingRectangle(
            rate2_badge, color=CYAN, fill_color=BOX_FILL,
            fill_opacity=0.8, buff=0.08, corner_radius=0.06, stroke_width=1.5,
        )
        rate2_badge_grp = VGroup(rate2_badge_box, rate2_badge)
        rate2_badge_grp.move_to(machine2[0].get_corner(UR) + DL * 0.25)
        self.play(FadeIn(rate2_badge_grp), run_time=0.3)

        amplify_label = Text("At x = 2: amplified by 12", font_size=16, color=GREEN)
        amplify_label.set_opacity(0.8)
        amplify_label.move_to([0, M2_Y - 3.3, 0])
        self.play(FadeIn(amplify_label), run_time=0.3)
        self.wait(max(1.0, dur - 4.5))

        # ═════════════════════════════════════════════════════
        # SCENE 7: MULTIPLY (13s) — The big moment
        # ═════════════════════════════════════════════════════
        dur = DUR("multiply")
        self.play(
            FadeOut(m2_glow), FadeOut(deriv_line1), FadeOut(deriv_line2),
            FadeOut(amplify_label), FadeOut(u_reminder), FadeOut(at_x2_line),
            machine1.animate.set_opacity(1.0),
            machine2.animate.set_opacity(1.0),
            pipe_arrow.animate.set_opacity(1.0),
            out_arrow.animate.set_opacity(1.0),
            out_label.animate.set_opacity(1.0),
            run_time=0.5
        )

        self.add_sound(AUDIO("multiply"))
        self.wait(0.3)

        # Green pulse
        pulse = Dot(radius=0.15, color=GREEN).set_glow_factor(1.2)
        pulse.move_to(in_label.get_center())
        trail = TracedPath(pulse.get_center, stroke_color=GREEN, stroke_width=2, stroke_opacity=0.3)
        self.add(pulse, trail)

        self.play(pulse.animate.move_to(machine1.get_center()), run_time=0.7)
        self.play(
            pulse.animate.scale(1.5),
            Flash(machine1[0], color=ORANGE, line_length=0.3, num_lines=10, run_time=0.4),
            run_time=0.5
        )
        scale1_txt = MathTex(r"\times 3", font_size=FS_KEY_FACT, color=ORANGE)
        scale1_txt.next_to(machine1[0], DOWN, buff=0.12).shift(LEFT * 0.8)
        self.play(FadeIn(scale1_txt, shift=DOWN*0.1), run_time=0.3)

        self.play(pulse.animate.move_to(machine2.get_center()), run_time=0.7)
        self.play(
            pulse.animate.scale(1.5),
            Flash(machine2[0], color=CYAN, line_length=0.3, num_lines=10, run_time=0.4),
            run_time=0.5
        )
        scale2_txt = MathTex(r"\times 12", font_size=FS_KEY_FACT, color=CYAN)
        scale2_txt.next_to(machine2[0], DOWN, buff=0.12).shift(LEFT * 0.8)
        at_x2_note = MathTex(r"\text{at } x = 2", font_size=18, color=GREEN)
        at_x2_note.next_to(scale2_txt, DOWN, buff=0.1)
        self.play(FadeIn(scale2_txt, shift=DOWN*0.1), FadeIn(at_x2_note), run_time=0.3)

        self.play(pulse.animate.move_to(out_label.get_center()), run_time=0.4)
        self.play(
            Flash(pulse, color=GREEN, line_length=0.3, num_lines=12, run_time=0.4),
            FadeOut(pulse), FadeOut(trail),
            run_time=0.4
        )
        self.play(FadeOut(scale1_txt), FadeOut(scale2_txt), FadeOut(at_x2_note), run_time=0.2)

        product = MathTex(r"3", r"\times", r"12", r"=", r"36",
                         font_size=FS_PUNCHLINE, color=WHITE)
        product[0].set_color(ORANGE)
        product[2].set_color(CYAN)
        product[4].set_color(GREEN)
        _clamp(product)
        product.move_to([0, M2_Y - 1.5, 0])
        product_box = SurroundingRectangle(
            product, color=BOX_BORDER, fill_color=BOX_FILL,
            fill_opacity=0.6, buff=0.25, corner_radius=0.1, stroke_width=2.5,
        )
        self.play(FadeIn(product_box), Write(product), run_time=0.8)
        self.wait(0.3)
        self.play(product[4].animate.scale(1.3), run_time=0.25)
        self.play(product[4].animate.scale(1/1.3), run_time=0.2)
        self.wait(max(1.5, dur - 6.55))

        # ═════════════════════════════════════════════════════
        # SCENE 8: FORMULA GENERAL (6s) — "derivative of outside × inside"
        # ═════════════════════════════════════════════════════
        dur = DUR("formula_general")

        # Clear pipeline, keep product at top
        self.play(
            FadeOut(VGroup(machine1, machine2, pipe_arrow, in_arrow, out_arrow,
                          in_label, out_label, expr, rate1_badge_grp, rate2_badge_grp)),
            VGroup(product_box, product).animate.move_to([0, 2.8, 0]),
            run_time=0.6
        )

        self.add_sound(AUDIO("formula_general"))

        # General formula — BIG and clear
        f_eq = MathTex(r"\frac{dy}{dx}", font_size=FS_EQUATION, color=WHITE)
        f_equals = MathTex(r"=", font_size=FS_EQUATION, color=WHITE)
        f_outer = MathTex(r"f'(g(x))", font_size=FS_EQUATION, color=CYAN)
        f_dot = MathTex(r"\cdot", font_size=FS_EQUATION, color=WHITE)
        f_inner = MathTex(r"g'(x)", font_size=FS_EQUATION, color=ORANGE)

        f_row = VGroup(f_eq, f_equals, f_outer, f_dot, f_inner).arrange(RIGHT, buff=0.1)
        _clamp(f_row)
        f_row.move_to([0, 1.0, 0])

        f_box = SurroundingRectangle(
            f_row, color=BOX_BORDER, fill_color=BOX_FILL,
            fill_opacity=0.6, buff=0.2, corner_radius=0.1, stroke_width=2.5,
        )

        # Labels ABOVE with arrows
        outer_tag = Text("outside rate", font_size=16, color=CYAN, weight=BOLD)
        outer_tag.next_to(f_outer, UP, buff=0.45)
        outer_arr = Arrow(outer_tag.get_bottom(), f_outer.get_top() + UP*0.08,
                         color=CYAN, stroke_width=1.5, buff=0.05,
                         max_tip_length_to_length_ratio=0.3)
        inner_tag = Text("inside rate", font_size=16, color=ORANGE, weight=BOLD)
        inner_tag.next_to(f_inner, UP, buff=0.45)
        inner_arr = Arrow(inner_tag.get_bottom(), f_inner.get_top() + UP*0.08,
                         color=ORANGE, stroke_width=1.5, buff=0.05,
                         max_tip_length_to_length_ratio=0.3)

        self.play(FadeIn(f_box), run_time=0.3)
        self.play(Write(f_eq), Write(f_equals), run_time=0.4)
        self.play(
            Write(f_outer),
            FadeIn(outer_tag), Create(outer_arr),
            run_time=0.6
        )
        self.play(Write(f_dot), run_time=0.15)
        self.play(
            Write(f_inner),
            FadeIn(inner_tag), Create(inner_arr),
            run_time=0.6
        )
        self.wait(max(0.5, dur - 2.05))

        # ═════════════════════════════════════════════════════
        # SCENE 9: FORMULA SPECIFIC (14s) — Apply to (3x)²
        # Each step narrated and shown BIG
        # ═════════════════════════════════════════════════════
        dur = DUR("formula_specific")

        # Dim the general formula, keep it visible
        self.play(
            FadeOut(outer_tag), FadeOut(inner_tag),
            FadeOut(outer_arr), FadeOut(inner_arr),
            VGroup(f_box, f_row).animate.set_opacity(0.35).move_to([0, 1.6, 0]),
            run_time=0.4
        )

        self.add_sound(AUDIO("formula_specific"))
        self.wait(0.3)

        # "For (3x)², the outside is u²"
        # First show the u = 3x connection
        u_connection = MathTex(r"\text{where } u = 3x", font_size=22, color=WHITE)
        u_connection.set_opacity(0.7)
        u_connection.move_to([0, 0.7, 0])
        self.play(FadeIn(u_connection), run_time=0.3)
        self.wait(0.3)

        outside_title = Text("Outside function:", font_size=20, color=CYAN, weight=BOLD)
        outside_title.move_to([0, 0.2, 0])
        outside_fn = MathTex(r"f(u) = u^2", font_size=FS_KEY_FACT, color=CYAN)
        outside_fn.move_to([0, -0.3, 0])
        outside_deriv = MathTex(r"f'(u) = 2u", font_size=FS_KEY_FACT, color=CYAN)
        outside_deriv.move_to([0, -0.9, 0])
        outside_applied = MathTex(r"= 2(3x)", font_size=FS_KEY_FACT, color=CYAN)
        outside_applied.move_to([0, -1.5, 0])

        self.play(Write(outside_title), run_time=0.3)
        self.play(Write(outside_fn), run_time=0.5)
        self.wait(0.5)
        self.play(Write(outside_deriv), run_time=0.5)
        self.wait(0.5)
        self.play(Write(outside_applied), run_time=0.5)
        self.wait(0.8)

        # "The inside is 3x"
        inside_title = Text("Inside function:", font_size=20, color=ORANGE, weight=BOLD)
        inside_title.move_to([0, -2.3, 0])
        inside_fn = MathTex(r"g(x) = 3x", font_size=FS_KEY_FACT, color=ORANGE)
        inside_fn.move_to([0, -2.8, 0])
        inside_deriv = MathTex(r"g'(x) = 3", font_size=FS_KEY_FACT, color=ORANGE)
        inside_deriv.move_to([0, -3.3, 0])

        self.play(Write(inside_title), run_time=0.3)
        self.play(Write(inside_fn), run_time=0.5)
        self.wait(0.5)
        self.play(Write(inside_deriv), run_time=0.5)
        self.wait(max(0.5, dur - 6.6))

        specific_all = VGroup(u_connection, outside_title, outside_fn, outside_deriv, outside_applied,
                              inside_title, inside_fn, inside_deriv)

        # ═════════════════════════════════════════════════════
        # SCENE 10: FORMULA PLUG-IN (9s) — x=2 → 36
        # ═════════════════════════════════════════════════════
        dur = DUR("formula_plugin")

        # Clear specific and product, bring back general formula at top
        self.play(
            FadeOut(specific_all),
            FadeOut(VGroup(product_box, product)),
            VGroup(f_box, f_row).animate.set_opacity(1.0).move_to([0, 3.0, 0]),
            run_time=0.5
        )

        self.add_sound(AUDIO("formula_plugin"))

        # The combined derivative — BIG, with room below
        combined = MathTex(
            r"\frac{dy}{dx}", r"=", r"2(3x)", r"\cdot", r"3",
            font_size=FS_KEY_FACT, color=WHITE
        )
        combined[2].set_color(CYAN)
        combined[4].set_color(ORANGE)
        _clamp(combined)
        combined.move_to([0, 1.5, 0])

        combined_box = SurroundingRectangle(
            combined, color=BOX_BORDER, fill_color=BOX_FILL,
            fill_opacity=0.6, buff=0.2, corner_radius=0.1, stroke_width=2,
        )

        self.play(FadeIn(combined_box), Write(combined), run_time=0.7)
        self.wait(0.8)

        # Plug in x = 2
        plugin_label = MathTex(r"\text{Plug in } x = 2:", font_size=22, color=GREEN)
        plugin_label.move_to([0, 0.5, 0])

        plugin_math = MathTex(
            r"= 2(3 \cdot 2) \cdot 3",
            font_size=FS_KEY_FACT, color=WHITE
        )
        plugin_math.move_to([0, -0.2, 0])
        _clamp(plugin_math)

        plugin_step2 = MathTex(
            r"= 2(6) \cdot 3",
            font_size=FS_KEY_FACT, color=WHITE
        )
        plugin_step2.move_to([0, -0.9, 0])

        plugin_result = MathTex(
            r"=", r"36",
            font_size=FS_PUNCHLINE, color=WHITE
        )
        plugin_result[1].set_color(GREEN)
        plugin_result.move_to([0, -1.8, 0])

        self.play(Write(plugin_label), run_time=0.4)
        self.wait(0.3)
        self.play(Write(plugin_math), run_time=0.5)
        self.wait(0.5)
        self.play(Write(plugin_step2), run_time=0.5)
        self.wait(0.3)
        self.play(Write(plugin_result), run_time=0.4)
        
        # Flash the 36 — connects back to the machines
        self.play(
            Circumscribe(plugin_result[1], color=GREEN, run_time=0.5),
        )
        self.wait(max(0.5, dur - 5.4))

        formula_all = VGroup(f_box, f_row,
                            combined_box, combined,
                            plugin_label, plugin_math, plugin_step2, plugin_result)

        # ═════════════════════════════════════════════════════
        # SCENE 11: GENERALIZATION (9s)
        # ═════════════════════════════════════════════════════
        dur = DUR("generalize")
        self.play(FadeOut(formula_all), run_time=0.5)

        self.add_sound(AUDIO("generalize"))

        ex1 = MathTex(r"\sin(x^2)", font_size=FS_EQUATION, color=CYAN)
        ex2 = MathTex(r"e^{\cos x}", font_size=FS_EQUATION, color=ORANGE)
        ex3 = MathTex(r"\sqrt{1 + x^3}", font_size=FS_EQUATION, color=GREEN)
        examples = VGroup(ex1, ex2, ex3).arrange(DOWN, buff=0.6)
        examples.move_to([0, 0.8, 0])
        gen_label = Text("Two functions. Two rates. Multiply.",
                        font_size=18, color=WHITE, weight=BOLD)
        gen_label.set_opacity(0.7)
        gen_label.move_to([0, -0.8, 0])

        self.play(Write(ex1), run_time=0.5)
        self.wait(0.8)
        self.play(Write(ex2), run_time=0.5)
        self.wait(0.8)
        self.play(Write(ex3), run_time=0.5)
        self.wait(0.5)
        self.play(FadeIn(gen_label), run_time=0.3)
        self.wait(max(0.5, dur - 3.9))
        self.play(FadeOut(VGroup(examples, gen_label)), run_time=0.4)

        # ═════════════════════════════════════════════════════
        # SCENE 12: PUNCHLINE (3s + silence)
        # ═════════════════════════════════════════════════════
        dur = DUR("punchline")
        self.add_sound(AUDIO("punchline"))

        punch = Text("Two machines.\nTwo rates.\nMultiply.",
                     font_size=FS_KEY_FACT + 4, color=GREEN, weight=BOLD,
                     line_spacing=1.5)
        _clamp(punch, MAX_WIDTH * 0.85)
        punch.move_to([0, 0.5, 0])
        punch_box = SurroundingRectangle(
            punch, color=BOX_BORDER, fill_color=BOX_FILL,
            fill_opacity=0.6, buff=0.35, corner_radius=0.1, stroke_width=2.5,
        )
        self.play(FadeIn(punch_box), FadeIn(punch), run_time=0.5)
        self.play(Circumscribe(punch_box, color=GREEN, run_time=0.6))
        self.wait(max(0.5, dur - 1.1))
        self.wait(2.0)  # SILENCE

        # ═════════════════════════════════════════════════════
        # END CARD
        # ═════════════════════════════════════════════════════
        self.play(FadeOut(VGroup(punch_box, punch)), run_time=0.4)

        _A, _B = 1.2, 0.95
        liss_glow = ParametricFunction(
            lambda t: np.array([_A*np.sin(2*t), _B*np.sin(3*t), 0]),
            t_range=[0, TAU, 0.02],
            color=END_CYAN, stroke_width=8, stroke_opacity=0.2
        )
        liss_core = ParametricFunction(
            lambda t: np.array([_A*np.sin(2*t), _B*np.sin(3*t), 0]),
            t_range=[0, TAU, 0.02],
            color=END_CYAN, stroke_width=2, stroke_opacity=1.0
        )
        logo = VGroup(liss_glow, liss_core).move_to([0, 0.5, 0])
        wordmark = Text("ORBITAL", font_size=22, color=END_CYAN, weight=BOLD)
        wordmark.next_to(logo, DOWN, buff=0.3)
        wm_glow = wordmark.copy().set_opacity(0.3).scale(1.05)
        end_card = VGroup(logo, wm_glow, wordmark)
        end_card.move_to(ORIGIN)

        self.play(Create(liss_core, run_time=0.8), FadeIn(liss_glow, run_time=0.6))
        self.play(FadeIn(VGroup(wm_glow, wordmark), shift=UP*0.2), run_time=0.4)
        self.wait(1.5)
        self.play(FadeOut(end_card), run_time=0.3)
