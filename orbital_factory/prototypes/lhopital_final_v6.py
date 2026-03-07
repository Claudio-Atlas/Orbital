"""
L'Hôpital's Rule — FINAL v6
============================
Fixes from v5:
  - Setup TTS now names both functions
  - Animations spread across DUR (no front-loading)
  - Reduced EXTRA_HOLD to 0.5s for tighter transitions

Render:
  cd ~/Desktop/Orbital/orbital_factory && source venv/bin/activate
  PATH="/Library/TeX/texbin:$PATH" manim render prototypes/lhopital_final_v6.py LHopitalFinalV6 \
    -o lhopital_final_v6.mp4 --format mp4 -r 1080,1920 --frame_rate 60 --flush_cache
"""
from manim import *
import numpy as np
import json, os

config.frame_width = 4.5
config.frame_height = 8.0

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
BOX_SCALE = 0.65
MATH_CENTER_Y = 1.2
GRAPH_CENTER_Y = -1.5
EXTRA_HOLD = 0.5  # Tighter than v5's 0.8

with open("output/tts/lhopital_scenes/manifest.json") as f:
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
    inner = Text(text_str, font_size=20, color=WHITE, line_spacing=1.3)
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


class LHopitalFinalV6(Scene):
    def construct(self):
        self.camera.background_color = BLACK

        # ── Persistent chrome ──
        border = Rectangle(width=FRAME_W - 0.15, height=FRAME_H - 0.15,
                           color=VIOLET, stroke_width=2.5, stroke_opacity=0.7, fill_opacity=0)
        border_glow = Rectangle(width=FRAME_W - 0.10, height=FRAME_H - 0.10,
                                color=VIOLET, stroke_width=6, stroke_opacity=0.15, fill_opacity=0)
        self.add(border_glow, border)
        wm = Text("ORBITAL", font_size=10, color=WHITE, weight=BOLD).set_opacity(0.35)
        wm.move_to([-FRAME_W/2 + 0.5, -FRAME_H/2 + 0.2, 0])
        self.add(wm)

        f_func = lambda x: 2 * np.sin(x - 3)
        g_func = lambda x: x - 3

        # ═══ SCENE 1: HOOK (DUR ~9.2s) ═══════════════════════════════
        # Voice: "You've been using this rule without knowing WHY it works.
        #         But nobody told you the reason. Here's the actual proof."
        dur = DUR("hook")
        t = 0  # track time within scene

        rule_tex = MathTex(
            r"\lim_{x \to a} \frac{f(x)}{g(x)} = \lim_{x \to a} \frac{f'(x)}{g'(x)}",
            font_size=30, color=WHITE
        ).move_to([0, 1.0, 0])
        lhop_label = Text("L'Hôpital's Rule", font_size=22, color=VIOLET,
                          weight=BOLD).move_to([0, -0.1, 0])
        proof_text = Text("Here's the actual proof.", font_size=24, color=GREEN,
                          weight=BOLD).move_to([0, -1.2, 0])

        self.add_sound(AUDIO("hook"))

        # "You've been using this rule..." → show the rule
        self.play(Write(rule_tex), run_time=1.5); t += 1.5
        self.play(Write(lhop_label), run_time=0.5); t += 0.5
        self.wait(1.5); t += 1.5  # Let voice finish first sentence

        # "But nobody told you the reason." → indicate
        self.play(Indicate(rule_tex, color=ORANGE), run_time=1.0); t += 1.0
        self.wait(1.5); t += 1.5  # Pause before "Here's the actual proof"

        # "Here's the actual proof."
        self.play(Write(proof_text), run_time=0.8); t += 0.8
        self.wait(max(0.3, dur - t)); t = dur
        self.wait(EXTRA_HOLD)

        self.play(FadeOut(rule_tex, lhop_label, proof_text), run_time=0.4)

        # ═══ SCENE 2: SETUP (DUR ~19.5s) ═════════════════════════════
        # Voice: "Here are two functions. f of x equals 2 sine of x minus 3.
        #         And g of x equals x minus 3. At x equals 3, both hit zero.
        #         So the limit gives you zero over zero. That is not a number.
        #         That is a warning sign."
        dur = DUR("setup"); t = 0

        axes = Axes(
            x_range=[-0.5, 5.5, 1], y_range=[-2.5, 3, 1],
            x_length=3.4, y_length=3.2,
            axis_config={"color": GREY_B, "include_numbers": True,
                         "font_size": 12, "numbers_to_exclude": [0]},
            tips=False,
        )
        grid = NumberPlane(
            x_range=[-0.5, 5.5, 1], y_range=[-2.5, 3, 1],
            x_length=3.4, y_length=3.2,
            background_line_style={"stroke_color": VIOLET, "stroke_opacity": 0.15,
                                   "stroke_width": 0.8},
            faded_line_style={"stroke_color": CYAN, "stroke_opacity": 0.06,
                              "stroke_width": 0.4},
        )
        grid.move_to(axes.get_center())

        curve_f = axes.plot(f_func, x_range=[0.5, 5.0], color=CYAN, stroke_width=3)
        curve_g = axes.plot(g_func, x_range=[0.5, 5.0], color=ORANGE, stroke_width=3)

        f_label = MathTex(r"f(x)\!=\!2\sin(x\!-\!3)", font_size=13, color=CYAN)
        g_label = MathTex(r"g(x)\!=\!x\!-\!3", font_size=13, color=ORANGE)

        zero_dot = Dot(axes.c2p(3, 0), color=GREEN, radius=0.04)
        graph_group = VGroup(grid, axes, curve_f, curve_g, zero_dot)
        graph_group.move_to([0, GRAPH_CENTER_Y, 0])

        f_label.next_to(axes.c2p(4.5, f_func(4.5)), UP, buff=0.15)
        g_label.next_to(axes.c2p(4.5, g_func(4.5)), DOWN, buff=0.15)

        self.add_sound(AUDIO("setup"))

        # "Here are two functions." → show graph
        self.play(FadeIn(VGroup(grid, axes)), run_time=0.5); t += 0.5
        self.wait(0.8); t += 0.8  # Let voice say "Here are two functions"

        # "f of x equals 2 sine of x minus 3" → draw f curve + label
        self.play(Create(curve_f), Write(f_label), run_time=1.2); t += 1.2
        self.wait(2.0); t += 2.0  # Let voice finish naming f

        # "And g of x equals x minus 3" → draw g curve + label
        self.play(Create(curve_g), Write(g_label), run_time=1.2); t += 1.2
        self.wait(2.0); t += 2.0  # Let voice finish naming g

        # "At x equals 3, both hit zero." → reveal dot
        zero_dot.set_opacity(0)
        zero_label = MathTex("x = 3", font_size=18, color=GREEN)
        zero_label.next_to(zero_dot, DOWN + LEFT, buff=0.1)
        self.play(zero_dot.animate.set_opacity(1).scale(2.5), Write(zero_label), run_time=0.6); t += 0.6
        self.play(Flash(zero_dot.get_center(), color=GREEN, num_lines=8), run_time=0.5); t += 0.5
        self.wait(1.5); t += 1.5

        # "So the limit gives you zero over zero." → show 0/0
        zero_zero = MathTex(r"\frac{f(3)}{g(3)} = \frac{0}{0}", font_size=28,
                            color=WHITE).move_to([0, MATH_CENTER_Y + 1.0, 0])
        self.play(Write(zero_zero), run_time=0.8); t += 0.8
        self.wait(2.0); t += 2.0  # Let voice say "zero over zero"

        # "That is not a number. That is a warning sign." → indicate + warning
        self.play(Indicate(zero_zero, color=RED), run_time=0.8); t += 0.8
        warning = Text("⚠", font_size=36)
        warning.next_to(zero_zero, RIGHT, buff=0.2)
        self.play(FadeIn(warning, scale=1.5), run_time=0.5); t += 0.5

        self.wait(max(0.3, dur - t))
        self.wait(EXTRA_HOLD)

        self.play(FadeOut(zero_zero, warning), run_time=0.3)

        # ═══ SCENE 3: ZOOM (DUR ~9.3s) ═══════════════════════════════
        # Voice: "Now zoom in. Right to that point. Every smooth curve,
        #         up close, looks like a straight line. That is the key."
        dur = DUR("zoom"); t = 0

        self.play(
            FadeOut(f_label, g_label, zero_label),
            zero_dot.animate.scale(1/2.5),
            run_time=0.2
        ); t += 0.2

        self.add_sound(AUDIO("zoom"))

        # "Now zoom in. Right to that point."
        zoom_center = axes.c2p(3, 0)
        self.play(
            graph_group.animate.scale(3.0, about_point=zoom_center)
                       .shift(-zoom_center + np.array([0, -1.0, 0])),
            run_time=2.5,
            rate_func=smooth
        ); t += 2.5
        self.wait(1.0); t += 1.0  # Let "right to that point" land

        # "Every smooth curve, up close, looks like a straight line."
        insight_box = _make_text_box("Up close, every smooth curve\nlooks like a straight line.")
        insight_box.move_to([0, MATH_CENTER_Y + 1.0, 0])
        self.play(Write(insight_box), run_time=1.0); t += 1.0
        self.wait(2.5); t += 2.5  # Let voice finish + "That is the key"

        self.wait(max(0.3, dur - t))
        self.wait(EXTRA_HOLD)

        self.play(FadeOut(graph_group, insight_box), run_time=0.4)

        # ═══ SCENE 4: TANGENT (DUR ~18.1s) ═══════════════════════════
        # Voice: "So replace each function with its tangent line.
        #         Near x=3, f(x) acts like its tangent line. f'(3)·(x-3).
        #         Same thing for g. g'(3)·(x-3)."
        dur = DUR("tangent"); t = 0

        axes2 = Axes(
            x_range=[2, 4, 0.5], y_range=[-1.5, 2, 0.5],
            x_length=3.4, y_length=3.5,
            axis_config={"color": GREY_B, "include_numbers": True, "font_size": 14},
            tips=False,
        )
        grid2 = NumberPlane(
            x_range=[2, 4, 0.5], y_range=[-1.5, 2, 0.5],
            x_length=3.4, y_length=3.5,
            background_line_style={"stroke_color": VIOLET, "stroke_opacity": 0.15, "stroke_width": 0.8},
            faded_line_style={"stroke_color": CYAN, "stroke_opacity": 0.06, "stroke_width": 0.4},
        )
        grid2.move_to(axes2.get_center())

        curve_f2 = axes2.plot(f_func, x_range=[2, 4], color=CYAN, stroke_width=3)
        curve_g2 = axes2.plot(g_func, x_range=[2, 4], color=ORANGE, stroke_width=3)
        zero_dot2 = Dot(axes2.c2p(3, 0), color=GREEN, radius=0.08)

        graph2 = VGroup(grid2, axes2, curve_f2, curve_g2, zero_dot2)
        graph2.move_to([0, GRAPH_CENTER_Y, 0])

        f_tang = DashedLine(
            axes2.c2p(2.3, 2*(2.3-3)), axes2.c2p(3.7, 2*(3.7-3)),
            color=CYAN, stroke_width=3, dash_length=0.06
        )
        g_tang = DashedLine(
            axes2.c2p(2.3, 1*(2.3-3)), axes2.c2p(3.7, 1*(3.7-3)),
            color=ORANGE, stroke_width=3, dash_length=0.06
        )

        self.add_sound(AUDIO("tangent"))

        # "So replace each function with its tangent line."
        self.play(FadeIn(graph2), run_time=0.4); t += 0.4
        self.wait(1.0); t += 1.0
        self.play(Create(f_tang), run_time=0.8); t += 0.8
        self.play(Create(g_tang), run_time=0.8); t += 0.8
        self.wait(1.5); t += 1.5  # Let first sentence finish

        # "Near x=3, f(x) acts like its tangent line. f'(3)·(x-3)."
        approx_f = MathTex(r"f(x) \approx f'(3) \cdot (x\!-\!3)", font_size=22,
                           color=CYAN).move_to([0, MATH_CENTER_Y + 1.0, 0])
        val_f = MathTex(r"= 2(x\!-\!3)", font_size=22, color=CYAN)
        val_f.next_to(approx_f, DOWN, buff=0.15)

        self.play(Write(approx_f), run_time=1.0); t += 1.0
        self.wait(1.5); t += 1.5  # Voice says formula
        self.play(Write(val_f), run_time=0.8); t += 0.8
        self.wait(2.0); t += 2.0  # Let it sink in

        # "Same thing for g. g'(3)·(x-3)."
        approx_g = MathTex(r"g(x) \approx g'(3) \cdot (x\!-\!3)", font_size=22,
                           color=ORANGE).move_to([0, MATH_CENTER_Y - 0.5, 0])
        val_g = MathTex(r"= 1(x\!-\!3)", font_size=22, color=ORANGE)
        val_g.next_to(approx_g, DOWN, buff=0.15)

        self.play(Write(approx_g), run_time=0.8); t += 0.8
        self.wait(1.0); t += 1.0
        self.play(Write(val_g), run_time=0.8); t += 0.8

        self.wait(max(0.3, dur - t))
        self.wait(EXTRA_HOLD)

        self.play(
            FadeOut(approx_f, val_f, approx_g, val_g, graph2, f_tang, g_tang),
            run_time=0.4
        )

        # ═══ SCENE 5: CANCEL (DUR ~21.1s) ════════════════════════════
        # Voice: "Now write the fraction. f'(3)·(x-3) over g'(3)·(x-3).
        #         See that? Same thing on top AND bottom. It cancels.
        #         You're left with f'(3)/g'(3). Two over one. That's two."
        dur = DUR("cancel"); t = 0

        self.add_sound(AUDIO("cancel"))

        # "Now write the fraction."
        frac_title = Text("The fraction becomes:", font_size=20,
                          color=WHITE).move_to([0, 3.0, 0])
        self.play(Write(frac_title), run_time=0.5); t += 0.5
        self.wait(0.8); t += 0.8

        # "f'(3)·(x-3)..."
        ratio_num = MathTex(r"f'(3)", r"\cdot", r"(x\!-\!3)", font_size=30, color=WHITE)
        ratio_num.move_to([0, 2.0, 0])
        frac_line = Line(LEFT*1.3, RIGHT*1.3, color=WHITE, stroke_width=2)
        frac_line.move_to([0, 1.6, 0])
        ratio_den = MathTex(r"g'(3)", r"\cdot", r"(x\!-\!3)", font_size=30, color=WHITE)
        ratio_den.move_to([0, 1.2, 0])

        self.play(Write(ratio_num), run_time=0.8); t += 0.8
        self.wait(0.5); t += 0.5

        # "...over g'(3)·(x-3)."
        self.play(Create(frac_line), run_time=0.3); t += 0.3
        self.play(Write(ratio_den), run_time=0.8); t += 0.8
        self.wait(1.5); t += 1.5  # Let voice catch up

        # "See that? Same thing on top AND bottom."
        self.play(
            ratio_num[2].animate.set_color(ORANGE),
            ratio_den[2].animate.set_color(ORANGE),
            run_time=0.5
        ); t += 0.5
        same_text = Text("Same thing top and bottom!", font_size=20, color=ORANGE,
                         weight=BOLD).move_to([0, 0.4, 0])
        self.play(
            Write(same_text),
            Indicate(ratio_num[2], color=ORANGE, scale_factor=1.3),
            Indicate(ratio_den[2], color=ORANGE, scale_factor=1.3),
            run_time=1.0
        ); t += 1.0
        self.wait(1.5); t += 1.5  # Let "same thing on top AND bottom" land

        # "It cancels."
        strike_top = Line(ratio_num[2].get_left() + DOWN*0.15,
                          ratio_num[2].get_right() + UP*0.15, color=RED, stroke_width=3)
        strike_bot = Line(ratio_den[2].get_left() + DOWN*0.15,
                          ratio_den[2].get_right() + UP*0.15, color=RED, stroke_width=3)
        self.play(Create(strike_top), Create(strike_bot), run_time=0.6); t += 0.6
        self.wait(1.5); t += 1.5  # Let "It cancels" land with impact

        # "You're left with f'(3)/g'(3)."
        self.play(
            FadeOut(ratio_num[1], ratio_num[2], strike_top,
                    ratio_den[1], ratio_den[2], strike_bot,
                    frac_title, same_text),
            run_time=0.5
        ); t += 0.5
        self.play(
            ratio_num[0].animate.move_to([0, 2.0, 0]),
            ratio_den[0].animate.move_to([0, 1.2, 0]),
            frac_line.animate.set_width(1.2).move_to([0, 1.6, 0]),
            run_time=0.5
        ); t += 0.5
        self.wait(2.0); t += 2.0  # Let voice finish "f-prime of 3 over g-prime of 3"

        # "Two over one. That's two."
        result = MathTex(r"= \frac{2}{1} = 2", font_size=32, color=GREEN)
        result.move_to([0, 0.3, 0])
        self.play(Write(result), run_time=0.8); t += 0.8
        self.play(Circumscribe(result, color=GREEN), run_time=0.6); t += 0.6

        self.wait(max(0.3, dur - t))
        self.wait(EXTRA_HOLD)

        # ═══ SCENE 6: GENERALIZE (DUR ~6.9s) ═════════════════════════
        # Voice: "This works at any shared zero. That's L'Hôpital's Rule —
        #         at least for zero over zero."
        dur = DUR("generalize"); t = 0

        self.add_sound(AUDIO("generalize"))

        # "This works at any shared zero." → morph 3 → a
        gen_num = MathTex(r"f'(a)", font_size=30, color=WHITE)
        gen_den = MathTex(r"g'(a)", font_size=30, color=WHITE)
        gen_num.move_to(ratio_num[0].get_center())
        gen_den.move_to(ratio_den[0].get_center())

        self.play(
            Transform(ratio_num[0], gen_num),
            Transform(ratio_den[0], gen_den),
            FadeOut(result),
            run_time=1.0
        ); t += 1.0
        self.wait(1.5); t += 1.5  # "This works at any shared zero"

        # "That's L'Hôpital's Rule — at least for zero over zero."
        rule_name = Text("L'Hôpital's Rule", font_size=24, color=VIOLET,
                         weight=BOLD).move_to([0, -0.3, 0])
        qualifier = Text("(for 0/0 form)", font_size=18, color=GREY_B).move_to([0, -0.8, 0])
        self.play(Write(rule_name), run_time=0.8); t += 0.8
        self.play(Write(qualifier), run_time=0.5); t += 0.5

        self.wait(max(0.3, dur - t))
        self.wait(EXTRA_HOLD)

        self.play(
            FadeOut(ratio_num[0], ratio_den[0], frac_line, rule_name, qualifier),
            run_time=0.4
        )

        # ═══ SCENE 7: PUNCHLINE (DUR ~15.6s) ═════════════════════════
        # Voice: "Near a shared zero, functions become tangent lines.
        #         The x minus a is always in both — so it always dies.
        #         f over g becomes f-prime over g-prime.
        #         Not magic. Just zoom."
        dur = DUR("punchline"); t = 0

        self.add_sound(AUDIO("punchline"))

        # "Near a shared zero, functions become tangent lines."
        punch1 = _make_text_box("Near a shared zero,\nfunctions become tangent lines.")
        punch1.move_to([0, 2.2, 0])
        self.play(Write(punch1), run_time=1.0); t += 1.0
        self.wait(2.5); t += 2.5

        # "The x minus a is always in both — so it always dies."
        punch2 = Text("(x − a) is ALWAYS in both\n→ it always cancels",
                       font_size=20, color=ORANGE, weight=BOLD,
                       line_spacing=1.3).move_to([0, 0.5, 0])
        self.play(Write(punch2), run_time=1.0); t += 1.0
        self.wait(2.5); t += 2.5

        # "f over g becomes f-prime over g-prime."
        final_rule = MathTex(
            r"\frac{f(x)}{g(x)} \to \frac{f'(a)}{g'(a)}", font_size=36, color=WHITE
        ).move_to([0, -1.2, 0])
        self.play(Write(final_rule), run_time=1.0); t += 1.0
        self.play(Circumscribe(final_rule, color=VIOLET, buff=0.15), run_time=0.8); t += 0.8
        self.wait(1.5); t += 1.5

        # "Not magic. Just zoom."
        self.play(FadeOut(punch1, punch2, final_rule), run_time=0.5); t += 0.5
        closer = Text("Not magic.\nJust zoom.", font_size=32, color=GREEN,
                       weight=BOLD, line_spacing=1.4).move_to([0, 0.5, 0])
        self.play(Write(closer), run_time=1.0); t += 1.0

        self.wait(max(0.3, dur - t))
        self.wait(1.5)  # Extra hold on mic-drop closer

        self.play(FadeOut(closer), run_time=0.4)

        # ═══ END CARD — Lissajous rotated 90° ═════════════════════════
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
