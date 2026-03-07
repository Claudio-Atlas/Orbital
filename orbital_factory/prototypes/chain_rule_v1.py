"""
Why the Chain Rule Works (It's Just Multiplication) — v1
=========================================================
Locked visual spec from L'Hôpital v6. Explicit font_size everywhere.
New scene type: rate_chain (nodes + arrows + pulse dot)

Render:
  cd ~/Desktop/Orbital/orbital_factory && source venv/bin/activate
  PATH="/Library/TeX/texbin:$PATH" manim render prototypes/chain_rule_v1.py ChainRuleV1 \
    -o chain_rule_v1.mp4 --format mp4 -r 1080,1920 --frame_rate 60 --flush_cache
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
MATH_CENTER_Y = 1.2
EXTRA_HOLD = 0.5
ANIMATION_RATIO = 0.35

# ── LOCKED FONT SIZES ──
FS_PUNCHLINE = 42
FS_KEY_FACT = 28
FS_CALLOUT = 24
FS_TITLE = 26
FS_EQUATION = 30
FS_CAPTION = 24
FS_WATERMARK = 10

# ── TTS ──
with open("output/tts/chain_rule_scenes/manifest.json") as f:
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

def _make_box(content_mob, label_text=None, buff=0.2):
    """Make a purple box around existing mobject."""
    box_rect = SurroundingRectangle(
        content_mob, color=BOX_BORDER, fill_color=BOX_FILL,
        fill_opacity=0.6, buff=buff, corner_radius=0.1, stroke_width=2,
    )
    if label_text:
        lbl = Text(label_text, color=CYAN, font_size=14)
        lbl.next_to(box_rect, UP, buff=0.1)
        return VGroup(box_rect, lbl, content_mob)
    return VGroup(box_rect, content_mob)


class ChainRuleV1(Scene):
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

        # ═══════════════════════════════════════════════════════════
        # SCENE 1: HOOK
        # ═══════════════════════════════════════════════════════════
        dur = DUR("hook")

        line1 = MathTex(
            r"\text{The chain rule}", r"\text{ isn't a formula.}",
            font_size=FS_PUNCHLINE, color=GREEN
        )
        line2 = MathTex(
            r"\text{It's just rates}", r"\text{ multiplying.}",
            font_size=FS_PUNCHLINE, color=GREEN
        )
        hook_content = VGroup(line1, line2).arrange(DOWN, buff=0.2)
        _clamp(hook_content, MAX_WIDTH * 0.85)
        hook_box = SurroundingRectangle(
            hook_content, color=BOX_BORDER, fill_color=BOX_FILL,
            fill_opacity=0.6, buff=0.3, corner_radius=0.1, stroke_width=2,
        )
        hook_group = VGroup(hook_box, hook_content)
        hook_group.move_to([0, MATH_CENTER_Y, 0])

        self.add_sound(AUDIO("hook"))
        self.play(Write(line1), run_time=0.8)
        self.wait(0.3)
        self.play(Write(line2), run_time=0.8)
        self.play(FadeIn(hook_box), run_time=0.3)
        self.wait(max(0.3, dur - 0.8 - 0.3 - 0.8 - 0.3))
        self.wait(EXTRA_HOLD)

        # ═══════════════════════════════════════════════════════════
        # SCENE 2: SETUP
        # ═══════════════════════════════════════════════════════════
        dur = DUR("setup")

        g_func = MathTex(r"g(x) = 2x", font_size=FS_EQUATION, color=WHITE)
        f_func = MathTex(r"f(u) = 3u", font_size=FS_EQUATION, color=WHITE)
        funcs = VGroup(g_func, f_func).arrange(RIGHT, buff=0.5)
        _clamp(funcs)
        funcs.move_to([0, MATH_CENTER_Y, 0])

        self.add_sound(AUDIO("setup"))
        self.play(FadeOut(hook_group, shift=UP * 0.3), run_time=0.3)
        self.play(Write(g_func), run_time=0.5)
        self.play(Write(f_func), run_time=0.5)
        self.wait(max(0.3, dur - 0.3 - 0.5 - 0.5))
        self.wait(EXTRA_HOLD)

        # ═══════════════════════════════════════════════════════════
        # SCENE 3: RATES
        # ═══════════════════════════════════════════════════════════
        dur = DUR("rates")

        g_deriv = MathTex(r"g'(x) = 2", font_size=FS_CAPTION, color=CYAN)
        g_deriv.next_to(g_func, DOWN, buff=0.25)
        f_deriv = MathTex(r"f'(u) = 3", font_size=FS_CAPTION, color=CYAN)
        f_deriv.next_to(f_func, DOWN, buff=0.25)

        rate_label_g = MathTex(r"\text{rate: } \times 2", font_size=20, color=ORANGE)
        rate_label_g.next_to(g_deriv, DOWN, buff=0.15)
        rate_label_f = MathTex(r"\text{rate: } \times 3", font_size=20, color=ORANGE)
        rate_label_f.next_to(f_deriv, DOWN, buff=0.15)

        self.add_sound(AUDIO("rates"))
        self.play(FadeIn(g_deriv), run_time=0.4)
        self.play(FadeIn(rate_label_g), run_time=0.3)
        self.wait(1.5)
        self.play(FadeIn(f_deriv), run_time=0.4)
        self.play(FadeIn(rate_label_f), run_time=0.3)
        self.wait(max(0.3, dur - 0.4 - 0.3 - 1.5 - 0.4 - 0.3))
        self.wait(EXTRA_HOLD)

        setup_group = VGroup(g_func, f_func, g_deriv, f_deriv, rate_label_g, rate_label_f)

        # ═══════════════════════════════════════════════════════════
        # SCENE 4: CHAIN (rate_chain — NEW TYPE)
        # ═══════════════════════════════════════════════════════════
        dur = DUR("chain")

        self.play(FadeOut(setup_group, shift=UP * 0.3), run_time=0.4)

        # Build the chain: [x] →(×2)→ [g] →(×3)→ [f]
        NODE_W = 0.7
        NODE_H = 0.5
        ARROW_LEN = 0.8
        CHAIN_Y = MATH_CENTER_Y + 0.3

        def make_node(label, x_pos):
            rect = RoundedRectangle(
                width=NODE_W, height=NODE_H,
                color=VIOLET, fill_color=BOX_FILL,
                fill_opacity=0.6, stroke_width=2, corner_radius=0.08,
            )
            lbl = MathTex(label, font_size=FS_KEY_FACT, color=WHITE)
            lbl.move_to(rect.get_center())
            grp = VGroup(rect, lbl)
            grp.move_to([x_pos, CHAIN_Y, 0])
            return grp

        x_node = make_node("x", -1.5)
        g_node = make_node("g", 0)
        f_node = make_node("f", 1.5)

        arrow1 = Arrow(
            x_node.get_right(), g_node.get_left(),
            color=WHITE, stroke_width=2, buff=0.08,
            max_tip_length_to_length_ratio=0.2,
        )
        arrow2 = Arrow(
            g_node.get_right(), f_node.get_left(),
            color=WHITE, stroke_width=2, buff=0.08,
            max_tip_length_to_length_ratio=0.2,
        )

        rate1 = MathTex(r"\times 2", font_size=20, color=ORANGE)
        rate1.next_to(arrow1, UP, buff=0.08)
        rate2 = MathTex(r"\times 3", font_size=20, color=ORANGE)
        rate2.next_to(arrow2, UP, buff=0.08)

        # u = g(x) label on the arrow
        u_label = MathTex(r"u = g(x)", font_size=14, color=CYAN)
        u_label.set_opacity(0.7)
        u_label.next_to(arrow1, DOWN, buff=0.08)

        self.add_sound(AUDIO("chain"))
        # Build chain left to right
        self.play(FadeIn(x_node), run_time=0.3)
        self.play(Create(arrow1), run_time=0.3)
        self.play(FadeIn(g_node), Write(rate1), FadeIn(u_label), run_time=0.4)
        self.play(Create(arrow2), run_time=0.3)
        self.play(FadeIn(f_node), Write(rate2), run_time=0.4)

        # Pulse dot traveling the chain
        chain_group = VGroup(x_node, arrow1, g_node, arrow2, f_node, rate1, rate2, u_label)

        pulse = Dot(radius=0.08, color=CYAN).set_glow_factor(0.8)
        pulse.move_to(x_node.get_center())
        self.add(pulse)

        # Travel x → g
        self.play(pulse.animate.move_to(g_node.get_center()), run_time=0.8, rate_func=smooth)
        self.play(rate1.animate.set_color(CYAN), run_time=0.15)
        self.play(rate1.animate.set_color(ORANGE), run_time=0.15)

        # Travel g → f
        self.play(pulse.animate.move_to(f_node.get_center()), run_time=0.8, rate_func=smooth)
        self.play(rate2.animate.set_color(CYAN), run_time=0.15)
        self.play(rate2.animate.set_color(ORANGE), run_time=0.15)

        self.play(FadeOut(pulse), run_time=0.2)
        self.wait(max(0.3, dur - 0.3 - 0.3 - 0.4 - 0.3 - 0.4 - 0.8 - 0.3 - 0.8 - 0.3 - 0.2))
        self.wait(EXTRA_HOLD)

        # ═══════════════════════════════════════════════════════════
        # SCENE 5: MULTIPLY
        # ═══════════════════════════════════════════════════════════
        dur = DUR("multiply")

        product = MathTex(r"2", r"\times", r"3", r"=", r"6",
                         font_size=FS_PUNCHLINE, color=WHITE)
        product[4].set_color(GREEN)  # "6" in green
        _clamp(product)
        product.move_to([0, MATH_CENTER_Y - 1.2, 0])

        result_box_content = MathTex(
            r"\text{f changes } 6\times \text{ as fast as } x",
            font_size=FS_KEY_FACT, color=CYAN
        )
        _clamp(result_box_content, MAX_WIDTH * 0.85)
        result_box = SurroundingRectangle(
            result_box_content, color=BOX_BORDER, fill_color=BOX_FILL,
            fill_opacity=0.6, buff=0.2, corner_radius=0.1, stroke_width=2,
        )
        result_group = VGroup(result_box, result_box_content)
        result_group.move_to([0, MATH_CENTER_Y - 2.3, 0])

        self.add_sound(AUDIO("multiply"))
        self.play(Write(product), run_time=0.6)
        self.play(product[4].animate.scale(1.3), run_time=0.3)
        self.play(product[4].animate.scale(1/1.3), run_time=0.2)
        self.play(FadeIn(result_group), run_time=0.4)
        self.wait(max(0.3, dur - 0.6 - 0.3 - 0.2 - 0.4))
        self.wait(EXTRA_HOLD)

        # ═══════════════════════════════════════════════════════════
        # SCENE 6: FORMULA (TransformMatchingTex)
        # ═══════════════════════════════════════════════════════════
        dur = DUR("formula")

        # Fade chain and result, keep product
        self.play(
            FadeOut(chain_group),
            FadeOut(result_group),
            run_time=0.3
        )

        # Move product to center
        self.play(product.animate.move_to([0, MATH_CENTER_Y + 0.5, 0]), run_time=0.3)

        # The chain rule formula
        chain_formula = MathTex(
            r"\frac{df}{dx}", r"=",
            r"\frac{df}{dg}", r"\cdot",
            r"\frac{dg}{dx}",
            font_size=FS_EQUATION, color=WHITE
        )
        _clamp(chain_formula)
        chain_formula.move_to([0, MATH_CENTER_Y + 0.5, 0])

        self.add_sound(AUDIO("formula"))
        self.play(ReplacementTransform(product, chain_formula), run_time=1.0)

        # Highlight the individual derivatives
        self.play(
            chain_formula[2].animate.set_color(ORANGE),  # df/dg
            chain_formula[4].animate.set_color(ORANGE),  # dg/dx
            run_time=0.3
        )
        self.wait(max(0.1, dur - 1.0 - 0.3 - 0.3 - 0.3))

        # ═══════════════════════════════════════════════════════════
        # SCENE 7: INSIGHT
        # ═══════════════════════════════════════════════════════════
        dur = DUR("insight")

        # Dim formula
        self.play(chain_formula.animate.set_opacity(0.35), run_time=0.3)

        punch_text = MathTex(
            r"\text{Rates of change multiply.}",
            font_size=FS_PUNCHLINE, color=GREEN
        )
        _clamp(punch_text, MAX_WIDTH * 0.85)
        punch_box = SurroundingRectangle(
            punch_text, color=BOX_BORDER, fill_color=BOX_FILL,
            fill_opacity=0.6, buff=0.3, corner_radius=0.1, stroke_width=2,
        )
        punch_group = VGroup(punch_box, punch_text)
        punch_group.move_to([0, MATH_CENTER_Y - 0.8, 0])

        sub_text = MathTex(
            r"\text{That's the whole chain rule.}",
            font_size=FS_CAPTION, color=CYAN
        )
        _clamp(sub_text)
        sub_text.next_to(punch_group, DOWN, buff=0.3)

        self.add_sound(AUDIO("insight"))
        self.play(FadeIn(punch_group), run_time=0.6)
        self.play(Circumscribe(punch_group, color=GREEN), run_time=0.5)
        self.wait(0.5)
        self.play(Write(sub_text), run_time=0.5)
        self.wait(max(0.3, dur - 0.3 - 0.6 - 0.5 - 0.5 - 0.5))
        self.wait(EXTRA_HOLD)

        # ═══════════════════════════════════════════════════════════
        # END CARD
        # ═══════════════════════════════════════════════════════════
        self.play(
            FadeOut(chain_formula),
            FadeOut(punch_group),
            FadeOut(sub_text),
            run_time=0.4
        )

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
        end_card.move_to([0, 0, 0])

        self.play(Create(liss_core, run_time=0.8), FadeIn(liss_glow, run_time=0.6))
        self.play(FadeIn(VGroup(wm_glow, wordmark), shift=UP*0.2), run_time=0.4)
        self.wait(1.2)
        self.play(FadeOut(end_card), run_time=0.3)
