"""
Riemann Integration — FINAL v5
===============================
Visual animations from locked v3 + scene-based TTS + DUR timing model.
Lissajous end card rotated 90°. Background music via ffmpeg.

∫₀³ x² dx = 9. Right-endpoint Riemann sums.
Steps: 4 → 20 → 50 → 200 → ∞ → anatomy → Σ → ∫

Render:
  cd ~/Desktop/Orbital/orbital_factory && source venv/bin/activate
  PATH="/Library/TeX/texbin:$PATH" manim render prototypes/riemann_final_v5.py RiemannFinalV5 \
    -o riemann_final_v5.mp4 --format mp4 -r 1080,1920 --frame_rate 60 --flush_cache
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
EXTRA_HOLD = 0.5

with open("output/tts/riemann_scenes/manifest.json") as f:
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


class RiemannFinalV5(Scene):
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

        # ── Shared math ──
        fn = lambda x: x**2
        a, b = 0, 3

        def riemann_sum(n):
            dx = (b - a) / n
            return sum(fn(a + i * dx) * dx for i in range(1, n + 1))

        # ═══ SCENE 1: HOOK (DUR ~6.9s) ═══════════════════════════════
        # "You've seen this symbol before. But what does it actually mean?
        #  It's just adding up area."
        dur = DUR("hook"); t = 0

        integral_big = MathTex(r"\int_0^3 x^2 \, dx",
                               font_size=48, color=CYAN).move_to([0, 0.5, 0])

        self.add_sound(AUDIO("hook"))

        # "You've seen this symbol before."
        self.play(Write(integral_big), run_time=1.2); t += 1.2
        self.wait(1.5); t += 1.5  # Let it land

        # "But what does it actually mean?"
        meaning = Text("What does it\nactually mean?", font_size=22,
                        color=WHITE, line_spacing=1.3).move_to([0, -1.2, 0])
        self.play(Write(meaning), run_time=0.8); t += 0.8
        self.wait(1.0); t += 1.0

        # "It's just adding up area."
        answer = Text("It's just adding up area.", font_size=22,
                       color=GREEN, weight=BOLD).move_to([0, -2.5, 0])
        self.play(Write(answer), run_time=0.6); t += 0.6

        self.wait(max(0.3, dur - t))
        self.wait(EXTRA_HOLD)
        self.play(FadeOut(integral_big, meaning, answer), run_time=0.4)

        # ═══ SCENE 2: THE PROBLEM (DUR ~9.6s) ════════════════════════
        # "Here's the curve. Here's the area. How do you measure
        #  something with a curved edge? You can't use a rectangle... or can you?"
        dur = DUR("problem"); t = 0

        axes = Axes(
            x_range=[-0.3, 3.8, 1], y_range=[-0.5, 10, 2],
            x_length=3.2, y_length=3.5,
            axis_config={"color": GREY_B, "include_numbers": True,
                         "font_size": 11, "numbers_to_exclude": [0]},
            tips=False,
        )
        grid = NumberPlane(
            x_range=[-0.3, 3.8, 1], y_range=[-0.5, 10, 2],
            x_length=3.2, y_length=3.5,
            background_line_style={"stroke_color": VIOLET, "stroke_opacity": 0.15,
                                   "stroke_width": 0.8},
            faded_line_style={"stroke_color": CYAN, "stroke_opacity": 0.06,
                              "stroke_width": 0.4},
        )
        grid.move_to(axes.get_center())
        curve = axes.plot(fn, x_range=[0, 3.1], color=CYAN, stroke_width=3)
        fn_label = MathTex("f(x) = x^2", font_size=18, color=CYAN)

        graph_group = VGroup(grid, axes, curve)
        graph_group.move_to([0, GRAPH_CENTER_Y, 0])
        fn_label.next_to(axes.c2p(1.2, 9), UP, buff=0.1)
        area_shade = axes.get_area(curve, x_range=[a, b], color=CYAN, opacity=0.2)

        self.add_sound(AUDIO("problem"))

        # "Here's the curve. Here's the area."
        self.play(FadeIn(graph_group), run_time=0.5); t += 0.5
        self.play(Create(curve), Write(fn_label), run_time=0.8); t += 0.8
        self.play(FadeIn(area_shade), run_time=0.8); t += 0.8
        self.wait(1.5); t += 1.5

        # "How do you measure something with a curved edge?"
        question = _make_text_box("How do you measure\nsomething with a curved edge?")
        question.move_to([0, MATH_CENTER_Y + 1.0, 0])
        self.play(Write(question), run_time=0.8); t += 0.8
        self.wait(2.0); t += 2.0

        # "You can't use a rectangle... or can you?"
        or_can = Text("You can't use a rectangle...\nor can you?", font_size=20,
                       color=ORANGE, line_spacing=1.3).move_to([0, MATH_CENTER_Y - 0.5, 0])
        self.play(Write(or_can), run_time=0.8); t += 0.8

        self.wait(max(0.3, dur - t))
        self.wait(EXTRA_HOLD)
        self.play(FadeOut(area_shade, question, or_can), run_time=0.3)

        # ═══ SCENE 3: FIRST ATTEMPT — 4 RECTS (DUR ~12.9s) ══════════
        # "Idea: fill the area with rectangles. Four rectangles. Quick and dirty.
        #  Sum comes out to about 12.66. You can see the overshoot."
        dur = DUR("first_attempt"); t = 0

        def make_rects(n, color=VIOLET, opacity=0.5):
            dx = (b - a) / n
            rects = VGroup()
            for i in range(n):
                x_left = a + i * dx
                x_right = x_left + dx
                h = fn(x_right)
                bl = axes.c2p(x_left, 0)
                tr = axes.c2p(x_right, h)
                r = Rectangle(
                    width=tr[0] - bl[0], height=max(tr[1] - bl[1], 0.001),
                    fill_color=color, fill_opacity=opacity,
                    stroke_color=WHITE, stroke_width=max(1.5 - n * 0.005, 0.3),
                    stroke_opacity=0.8
                )
                r.move_to([(bl[0]+tr[0])/2, (bl[1]+tr[1])/2, 0])
                rects.add(r)
            return rects

        rects = make_rects(4)
        sum_val = riemann_sum(4)

        n_text = Text("n = 4 rectangles", font_size=18, color=WHITE).move_to([0, 2.8, 0])
        sum_text = MathTex(f"\\text{{Sum}} \\approx {sum_val:.2f}",
                           font_size=24, color=ORANGE).move_to([0, 2.2, 0])

        self.add_sound(AUDIO("first_attempt"))

        # "Idea: fill the area with rectangles."
        self.wait(1.0); t += 1.0  # Let voice say "Idea..."
        self.play(FadeIn(rects, lag_ratio=0.15), run_time=1.2); t += 1.2

        # "Four rectangles. Rough estimate."
        self.play(Write(n_text), run_time=0.4); t += 0.4
        self.wait(1.5); t += 1.5

        # "Sum comes out to about 12.66."
        self.play(Write(sum_text), run_time=0.5); t += 0.5
        self.wait(2.0); t += 2.0

        # "You can see the overshoot."
        overshoot = Text("You can see the overshoot.", font_size=20,
                          color=ORANGE).move_to([0, 1.6, 0])
        self.play(Write(overshoot), run_time=0.6); t += 0.6

        self.wait(max(0.3, dur - t))
        self.wait(EXTRA_HOLD)

        # ═══ SCENE 4: BUILDUP 50→200 (DUR ~15.1s) ═══════════════════
        # "Fifty rectangles. 9.27. Two hundred rectangles. 9.07.
        #  Barely any overshoot. What if we just... keep going?"
        dur = DUR("buildup"); t = 0

        self.add_sound(AUDIO("buildup"))

        # 50 rectangles — "Fifty rectangles. The curve is almost filled. 9.27."
        rects_50 = make_rects(50, opacity=0.4)
        sum_50 = riemann_sum(50)
        new_n2 = Text("n = 50", font_size=18, color=WHITE).move_to([0, 2.8, 0])
        new_sum2 = MathTex(f"\\text{{Sum}} \\approx {sum_50:.2f}",
                           font_size=24, color=ORANGE).move_to([0, 2.2, 0])

        self.play(
            FadeOut(overshoot),
            Transform(rects, rects_50),
            Transform(n_text, new_n2),
            Transform(sum_text, new_sum2),
            run_time=1.5
        ); t += 1.5
        self.wait(2.5); t += 2.5

        # 200 rectangles — "Two hundred rectangles. 9.07."
        rects_200 = make_rects(200, opacity=0.35)
        sum_200 = riemann_sum(200)
        new_n3 = Text("n = 200", font_size=18, color=WHITE).move_to([0, 2.8, 0])
        new_sum3 = MathTex(f"\\text{{Sum}} \\approx {sum_200:.2f}",
                           font_size=24, color=ORANGE).move_to([0, 2.2, 0])

        self.play(
            Transform(rects, rects_200),
            Transform(n_text, new_n3),
            Transform(sum_text, new_sum3),
            run_time=2.0
        ); t += 2.0
        self.wait(1.5); t += 1.5

        # "Barely any overshoot."
        barely = Text("Barely any overshoot.", font_size=20,
                       color=GREEN).move_to([0, 1.6, 0])
        self.play(Write(barely), run_time=0.5); t += 0.5
        self.wait(2.0); t += 2.0

        # "What if we just... keep going?"
        keep_going = Text("What if we just... keep going?", font_size=20,
                           color=WHITE).move_to([0, 1.0, 0])
        self.play(Write(keep_going), run_time=0.6); t += 0.6

        self.wait(max(0.3, dur - t))
        self.wait(EXTRA_HOLD)

        # ═══ SCENE 5: PAYOFF — n → ∞ (DUR ~5.4s) ════════════════════
        # "Infinite rectangles. The sum becomes exact. Nine. Perfectly."
        dur = DUR("payoff"); t = 0

        area_final = axes.get_area(curve, x_range=[a, b], color=CYAN, opacity=0.4)
        inf_text = Text("n → ∞", font_size=26, color=GREEN,
                         weight=BOLD).move_to([0, 2.8, 0])
        exact = MathTex(r"= 9", font_size=36, color=GREEN).move_to([0, 2.0, 0])

        self.add_sound(AUDIO("payoff"))

        # "Infinite rectangles. The sum becomes exact."
        self.play(
            FadeOut(barely, keep_going),
            Transform(rects, area_final),
            Transform(n_text, inf_text),
            Transform(sum_text, exact),
            run_time=2.5, rate_func=smooth
        ); t += 2.5
        self.play(Flash(axes.c2p(1.5, 2), color=GREEN, num_lines=10), run_time=0.5); t += 0.5

        # "Nine. Perfectly."
        self.wait(max(0.3, dur - t))
        self.wait(2.0)  # Extended silence beat — let it LAND

        # ═══ SCENE 6: BRIDGE (DUR ~5.1s) ═════════════════════════════
        # "But what does the math actually look like? Let's look at one rectangle."
        dur = DUR("bridge"); t = 0

        self.play(FadeOut(rects, n_text, sum_text), run_time=0.4); t += 0.4

        self.add_sound(AUDIO("bridge"))

        bridge = _make_text_box("But what does the math\nactually look like?")
        bridge.move_to([0, MATH_CENTER_Y + 1.0, 0])
        self.play(Write(bridge), run_time=0.8); t += 0.8
        self.wait(max(0.3, dur - t - 0.3))
        self.play(FadeOut(bridge), run_time=0.3)
        self.wait(EXTRA_HOLD)

        # ═══ SCENE 7: ANATOMY (DUR ~19.2s) ═══════════════════════════
        # "This height? That's f(xᵢ). This width? That's Δx.
        #  Area = height × width. f(xᵢ) · Δx."
        dur = DUR("anatomy"); t = 0

        # One highlighted rectangle
        anatomy_title = Text("One rectangle:", font_size=22, color=WHITE,
                              weight=BOLD).move_to([0, 2.8, 0])

        x_sample = 2.0
        dx_val = 0.75
        bl = axes.c2p(x_sample, 0)
        tr = axes.c2p(x_sample + dx_val, fn(x_sample + dx_val))

        demo_rect = Rectangle(
            width=tr[0] - bl[0], height=tr[1] - bl[1],
            fill_color=VIOLET, fill_opacity=0.5,
            stroke_color=WHITE, stroke_width=2,
        )
        demo_rect.move_to([(bl[0]+tr[0])/2, (bl[1]+tr[1])/2, 0])

        self.add_sound(AUDIO("anatomy"))

        self.play(Write(anatomy_title), FadeIn(demo_rect), run_time=0.6); t += 0.6
        self.wait(1.0); t += 1.0

        # "This height? That's f(xᵢ)."
        height_brace = BraceBetweenPoints(
            axes.c2p(x_sample + dx_val, 0),
            axes.c2p(x_sample + dx_val, fn(x_sample + dx_val)),
            direction=RIGHT, color=CYAN, buff=0.05
        )
        height_label = MathTex(r"f(x_i)", font_size=22, color=CYAN)
        height_label.next_to(height_brace, RIGHT, buff=0.08)
        height_note = Text("= height", font_size=14, color=CYAN)
        height_note.next_to(height_label, DOWN, buff=0.05)

        self.play(FadeIn(height_brace), Write(height_label), run_time=0.8); t += 0.8
        self.play(Write(height_note), run_time=0.3); t += 0.3
        self.wait(2.5); t += 2.5  # "The value of the function at that point"

        # "This width? That's Δx."
        width_brace = BraceBetweenPoints(
            axes.c2p(x_sample, 0),
            axes.c2p(x_sample + dx_val, 0),
            direction=DOWN, color=ORANGE, buff=0.05
        )
        width_label = MathTex(r"\Delta x", font_size=22, color=ORANGE)
        width_label.next_to(width_brace, DOWN, buff=0.08)
        width_note = Text("= width", font_size=14, color=ORANGE)
        width_note.next_to(width_label, DOWN, buff=0.05)

        self.play(FadeIn(width_brace), Write(width_label), run_time=0.8); t += 0.8
        self.play(Write(width_note), run_time=0.3); t += 0.3
        self.wait(2.5); t += 2.5  # "The size of the slice"

        # "Area = height × width. f(xᵢ) · Δx."
        area_eq = MathTex(r"\text{Area}", r"=", r"f(x_i)", r"\cdot", r"\Delta x",
                          font_size=24, color=WHITE).move_to([0, 2.2, 0])
        area_eq[2].set_color(CYAN)
        area_eq[4].set_color(ORANGE)

        self.play(FadeOut(anatomy_title), Write(area_eq), run_time=0.8); t += 0.8
        self.wait(max(0.3, dur - t))
        self.wait(EXTRA_HOLD)

        self.play(
            FadeOut(demo_rect, height_brace, height_label, height_note,
                    width_brace, width_label, width_note, area_eq),
            run_time=0.4
        )

        # ═══ SCENE 8: BUILD THE SUM (DUR ~12.0s) ═════════════════════
        # "Now stack them together. Sigma — add them all.
        #  f(xᵢ) — height. Times Δx — width."
        dur = DUR("build_sum"); t = 0

        rects_show = make_rects(20, opacity=0.4)

        self.add_sound(AUDIO("build_sum"))

        # "Now stack them together."
        self.play(FadeIn(rects_show, lag_ratio=0.02), run_time=0.6); t += 0.6

        stack_text = Text("Stack them all:", font_size=22, color=WHITE,
                           weight=BOLD).move_to([0, 2.8, 0])
        self.play(Write(stack_text), run_time=0.4); t += 0.4
        self.wait(1.5); t += 1.5

        # "Sigma — add them all."
        sigma = MathTex(r"\sum_{i=1}^{n}", font_size=30, color=GREEN)
        fxi = MathTex(r"f(x_i)", font_size=30, color=CYAN)
        dx_sym = MathTex(r"\Delta x", font_size=30, color=ORANGE)
        sigma.move_to([-0.9, 2.0, 0])
        fxi.next_to(sigma, RIGHT, buff=0.12)
        dx_sym.next_to(fxi, RIGHT, buff=0.08)

        self.play(Write(sigma), run_time=0.6); t += 0.6
        self.wait(1.5); t += 1.5  # "Sigma means add them all"

        # "f(xᵢ) — height of each rectangle."
        self.play(Write(fxi), run_time=0.5); t += 0.5
        self.wait(1.5); t += 1.5

        # "Times Δx — width of each slice."
        self.play(Write(dx_sym), run_time=0.5); t += 0.5

        self.wait(max(0.3, dur - t))
        self.wait(EXTRA_HOLD)

        self.play(FadeOut(rects_show, stack_text), run_time=0.3)

        # ═══ SCENE 9: THE CONNECTION — Σ → ∫ (DUR ~12.7s) ════════════
        # "Let n → ∞. Σ becomes ∫. f(xᵢ) → f(x). Δx → dx."
        dur = DUR("connection"); t = 0

        sum_group = VGroup(sigma, fxi, dx_sym)
        self.play(
            FadeOut(graph_group, fn_label),
            sum_group.animate.move_to([0, 2.5, 0]),
            run_time=0.6
        ); t += 0.6

        self.add_sound(AUDIO("connection"))

        # "Now let n go to infinity."
        let_n = Text("Let n → ∞", font_size=22, color=WHITE,
                       weight=BOLD).move_to([0, 1.5, 0])
        self.play(Write(let_n), run_time=0.6); t += 0.6
        self.wait(2.0); t += 2.0

        # Color-coded integral
        integral_final = MathTex(
            r"\int_0^3", r"f(x)", r"\, dx",
            font_size=40, color=WHITE
        ).move_to([0, 0.0, 0])
        integral_final[0].set_color(GREEN)
        integral_final[1].set_color(CYAN)
        integral_final[2].set_color(ORANGE)

        # "Sigma becomes the integral sign."
        self.play(Write(integral_final[0]), run_time=0.8); t += 0.8
        t1 = MathTex(r"\sum \to \int", font_size=18, color=GREEN).move_to([-1.1, -1.0, 0])
        self.play(Write(t1), run_time=0.5); t += 0.5
        self.wait(1.0); t += 1.0

        # "f(xᵢ) becomes f(x)."
        self.play(Write(integral_final[1]), run_time=0.8); t += 0.8
        t2 = MathTex(r"f(x_i) \to f(x)", font_size=18, color=CYAN).move_to([0, -1.0, 0])
        self.play(Write(t2), run_time=0.5); t += 0.5
        self.wait(1.0); t += 1.0

        # "Δx becomes dx."
        self.play(Write(integral_final[2]), run_time=0.8); t += 0.8
        t3 = MathTex(r"\Delta x \to dx", font_size=18, color=ORANGE).move_to([1.1, -1.0, 0])
        self.play(Write(t3), run_time=0.5); t += 0.5

        self.wait(max(0.3, dur - t))
        self.wait(EXTRA_HOLD)

        # ═══ SCENE 10: PUNCHLINE (DUR ~3.9s) ═════════════════════════
        # "That's the same idea. Just infinitely precise."
        dur = DUR("punchline"); t = 0

        self.play(FadeOut(sum_group, let_n, t1, t2, t3), run_time=0.4); t += 0.4
        self.play(integral_final.animate.move_to([0, 0.5, 0]), run_time=0.3); t += 0.3

        self.add_sound(AUDIO("punchline"))

        # "That's the same idea."
        same_idea = Text("Same idea.", font_size=24, color=WHITE,
                          weight=BOLD).move_to([0, 2.2, 0])
        self.play(Write(same_idea), run_time=0.6); t += 0.6

        # "Just infinitely precise."
        precise = Text("Just infinitely precise.", font_size=24,
                         color=GREEN, weight=BOLD).move_to([0, 1.5, 0])
        self.play(Write(precise), run_time=0.8); t += 0.8
        self.play(Circumscribe(integral_final, color=VIOLET, buff=0.15), run_time=0.8); t += 0.8

        self.wait(max(0.3, dur - t))
        self.wait(2.0)  # Extended hold — let it resonate

        self.play(FadeOut(same_idea, precise, integral_final), run_time=0.4)

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
