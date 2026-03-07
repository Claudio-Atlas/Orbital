"""
Why the Chain Rule Works (It's Just Multiplication) — v2
=========================================================
REAL Circle-approved. Function machine pipeline with animated flow.
Example: (3x)² at x=2. Gears/machines visual metaphor.
55-60s target. Every scene has motion.

Render:
  cd ~/Desktop/Orbital/orbital_factory && source venv/bin/activate
  PATH="/Library/TeX/texbin:$PATH" manim render prototypes/chain_rule_v2.py ChainRuleV2 \
    -o chain_rule_v2.mp4 --format mp4 -r 1080,1920 --frame_rate 60 --flush_cache
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

# ── LOCKED FONT SIZES ──
FS_PUNCHLINE = 42
FS_KEY_FACT = 28
FS_CALLOUT = 24
FS_TITLE = 26
FS_EQUATION = 30
FS_CAPTION = 24
FS_WATERMARK = 10
FS_MACHINE_LABEL = 20
FS_RATE_LABEL = 18
FS_NUMBER = 36

# ── TTS ──
with open("output/tts/chain_rule_v2_scenes/manifest.json") as f:
    _manifest = json.load(f)
    MANIFEST = {s["scene"]: s for s in _manifest}

def AUDIO(scene): return MANIFEST[scene]["audio_path"]
def DUR(scene): return MANIFEST[scene]["duration"]

def _clamp(mob, max_w=None):
    if max_w is None: max_w = MAX_WIDTH
    if mob.width > max_w: mob.scale(max_w / mob.width)
    return mob

def _make_machine(label, sublabel, color, x_pos, y_pos, width=1.6, height=1.2):
    """Build a function machine: rounded box with label + sublabel."""
    box = RoundedRectangle(
        width=width, height=height,
        color=color, fill_color=BOX_FILL,
        fill_opacity=0.7, stroke_width=2.5, corner_radius=0.12,
    )
    box.move_to([x_pos, y_pos, 0])
    
    # Machine label (what it does)
    lbl = Text(label, font_size=FS_MACHINE_LABEL, color=color, weight=BOLD)
    lbl.move_to(box.get_center() + UP * 0.15)
    
    # Sublabel (the function)
    sub = MathTex(sublabel, font_size=FS_RATE_LABEL, color=WHITE)
    sub.set_opacity(0.7)
    sub.move_to(box.get_center() + DOWN * 0.2)
    
    # Input/output ports (small circles)
    in_port = Dot(radius=0.06, color=color).move_to(box.get_left())
    out_port = Dot(radius=0.06, color=color).move_to(box.get_right())
    
    return VGroup(box, lbl, sub, in_port, out_port)

def _make_number_dot(value, color=CYAN, size=FS_NUMBER):
    """A number inside a glowing circle — flows through the pipeline."""
    num = MathTex(str(value), font_size=size, color=color)
    circle = Circle(radius=0.3, color=color, fill_color=color, fill_opacity=0.15, stroke_width=1.5)
    circle.move_to(num.get_center())
    return VGroup(circle, num)


class ChainRuleV2(Scene):
    def construct(self):
        self.camera.background_color = BLACK

        # ── PERSISTENT: Border + Watermark ──
        border = Rectangle(
            width=FRAME_W - 0.15, height=FRAME_H - 0.15,
            color=VIOLET, stroke_width=2.5, stroke_opacity=0.7, fill_opacity=0,
        ).move_to(ORIGIN)
        border_glow = Rectangle(
            width=FRAME_W - 0.10, height=FRAME_H - 0.10,
            color=VIOLET, stroke_width=6, stroke_opacity=0.15, fill_opacity=0,
        ).move_to(ORIGIN)
        self.add(border_glow, border)
        wm = Text("ORBITAL", font_size=FS_WATERMARK, color=WHITE, weight=BOLD)
        wm.set_opacity(0.35).move_to([-FRAME_W/2 + 0.5, -FRAME_H/2 + 0.2, 0])
        self.add(wm)

        # ═══════════════════════════════════════════════════════════
        # SCENE 1: HOOK (4s) — Motion, not static text
        # ═══════════════════════════════════════════════════════════
        dur = DUR("hook")

        # Two spinning gear outlines to show "connected rates"
        gear1 = Circle(radius=0.5, color=VIOLET, stroke_width=3)
        gear1.move_to([-0.6, MATH_CENTER_Y + 1.0, 0])
        gear2 = Circle(radius=0.35, color=CYAN, stroke_width=3)
        gear2.move_to([0.5, MATH_CENTER_Y + 1.0, 0])
        
        # Gear teeth (simple lines radiating)
        teeth1 = VGroup(*[
            Line(gear1.get_center() + 0.5 * np.array([np.cos(a), np.sin(a), 0]),
                 gear1.get_center() + 0.62 * np.array([np.cos(a), np.sin(a), 0]),
                 color=VIOLET, stroke_width=2)
            for a in np.linspace(0, TAU, 8, endpoint=False)
        ])
        teeth2 = VGroup(*[
            Line(gear2.get_center() + 0.35 * np.array([np.cos(a), np.sin(a), 0]),
                 gear2.get_center() + 0.45 * np.array([np.cos(a), np.sin(a), 0]),
                 color=CYAN, stroke_width=2)
            for a in np.linspace(0, TAU, 6, endpoint=False)
        ])
        g1_group = VGroup(gear1, teeth1)
        g2_group = VGroup(gear2, teeth2)

        # The scary formula — flash it briefly
        scary = MathTex(
            r"\frac{d}{dx}[f(g(x))] = f'(g(x)) \cdot g'(x)",
            font_size=FS_CAPTION, color=WHITE
        )
        scary.set_opacity(0.4)
        _clamp(scary)
        scary.move_to([0, MATH_CENTER_Y - 0.5, 0])

        self.add_sound(AUDIO("hook"))
        # Gears appear and start rotating
        self.play(
            FadeIn(g1_group), FadeIn(g2_group),
            run_time=0.4
        )
        self.play(
            Rotate(g1_group, angle=PI/3, about_point=gear1.get_center()),
            Rotate(g2_group, angle=-PI/2.5, about_point=gear2.get_center()),
            FadeIn(scary),
            run_time=1.2
        )
        
        # Hook text slams in
        hook_text = Text("Just multiplication.", font_size=FS_CALLOUT, color=GREEN, weight=BOLD)
        _clamp(hook_text)
        hook_text.move_to([0, MATH_CENTER_Y - 1.5, 0])
        self.play(FadeIn(hook_text, shift=UP * 0.2), run_time=0.3)
        
        self.wait(max(0.3, dur - 0.4 - 1.2 - 0.3))

        hook_all = VGroup(g1_group, g2_group, scary, hook_text)

        # ═══════════════════════════════════════════════════════════
        # SCENE 2: COMPOSITION (13s) — Show TWO machines
        # ═══════════════════════════════════════════════════════════
        dur = DUR("composition")

        self.play(FadeOut(hook_all, shift=UP * 0.3), run_time=0.4)

        # The expression that hides two functions
        expr = MathTex(r"(3x)^2", font_size=FS_PUNCHLINE, color=WHITE)
        _clamp(expr)
        expr.move_to([0, 3.0, 0])
        
        self.add_sound(AUDIO("composition"))
        self.play(Write(expr), run_time=0.6)
        self.wait(1.0)

        # Decompose: highlight the 3x (inner) and the ²  (outer)
        inner_highlight = SurroundingRectangle(
            expr[0][1:3],  # "3x" part
            color=ORANGE, stroke_width=2, buff=0.05, corner_radius=0.05
        )
        inner_label = Text("Machine 1", font_size=14, color=ORANGE)
        inner_label.next_to(inner_highlight, DOWN, buff=0.1)
        
        outer_highlight = SurroundingRectangle(
            expr[0],  # whole thing with the square
            color=CYAN, stroke_width=2, buff=0.08, corner_radius=0.05
        )
        outer_label = Text("Machine 2", font_size=14, color=CYAN)
        outer_label.next_to(outer_highlight, UP, buff=0.1)

        self.play(Create(inner_highlight), FadeIn(inner_label), run_time=0.5)
        self.wait(0.8)
        self.play(Create(outer_highlight), FadeIn(outer_label), run_time=0.5)
        self.wait(0.5)

        # Build the two-machine pipeline
        PIPE_Y = 0.3
        machine1 = _make_machine("TRIPLE", r"3x", ORANGE, -0.9, PIPE_Y)
        machine2 = _make_machine("SQUARE", r"u^2", CYAN, 0.9, PIPE_Y)
        
        # Arrow between machines
        pipe_arrow = Arrow(
            machine1[0].get_right() + RIGHT * 0.08,
            machine2[0].get_left() + LEFT * 0.08,
            color=WHITE, stroke_width=2, buff=0,
            max_tip_length_to_length_ratio=0.3,
        )

        # Input arrow
        in_arrow = Arrow(
            LEFT * 1.8 + UP * PIPE_Y,
            machine1[0].get_left() + LEFT * 0.08,
            color=WHITE, stroke_width=2, buff=0,
            max_tip_length_to_length_ratio=0.3,
        )
        in_label = MathTex("x", font_size=FS_CAPTION, color=WHITE)
        in_label.next_to(in_arrow, LEFT, buff=0.05)

        # Output arrow
        out_arrow = Arrow(
            machine2[0].get_right() + RIGHT * 0.08,
            RIGHT * 1.8 + UP * PIPE_Y,
            color=WHITE, stroke_width=2, buff=0,
            max_tip_length_to_length_ratio=0.3,
        )
        out_label = MathTex("y", font_size=FS_CAPTION, color=WHITE)
        out_label.next_to(out_arrow, RIGHT, buff=0.05)

        # Animate pipeline building
        self.play(
            FadeOut(VGroup(inner_highlight, inner_label, outer_highlight, outer_label)),
            expr.animate.scale(0.7).move_to([0, 3.2, 0]).set_opacity(0.5),
            run_time=0.4
        )
        self.play(
            Create(in_arrow), FadeIn(in_label),
            FadeIn(machine1),
            run_time=0.5
        )
        self.play(
            Create(pipe_arrow),
            run_time=0.3
        )
        self.play(
            FadeIn(machine2),
            Create(out_arrow), FadeIn(out_label),
            run_time=0.5
        )

        # Animate a number flowing through!
        num_2 = _make_number_dot(2, WHITE)
        num_2.move_to(in_label.get_center())
        
        num_6 = _make_number_dot(6, ORANGE)
        num_6.move_to(machine1.get_center())
        
        num_36 = _make_number_dot(36, CYAN)
        num_36.move_to(machine2.get_center())

        self.play(FadeIn(num_2, scale=0.5), run_time=0.2)
        self.play(num_2.animate.move_to(machine1.get_center()), run_time=0.5)
        self.play(FadeOut(num_2), FadeIn(num_6, scale=1.3), run_time=0.3)
        self.play(num_6.animate.move_to(pipe_arrow.get_center()), run_time=0.3)
        self.play(num_6.animate.move_to(machine2.get_center()), run_time=0.3)
        self.play(FadeOut(num_6), FadeIn(num_36, scale=1.3), run_time=0.3)
        self.play(num_36.animate.move_to(out_label.get_center() + LEFT * 0.3), run_time=0.3)
        
        # Result caption
        flow_caption = MathTex(
            r"2 \xrightarrow{\times 3} 6 \xrightarrow{(\;)^2} 36",
            font_size=FS_CAPTION, color=WHITE
        )
        _clamp(flow_caption)
        flow_caption.move_to([0, PIPE_Y - 1.3, 0])
        self.play(FadeOut(num_36), Write(flow_caption), run_time=0.5)
        
        self.wait(max(0.3, dur - 0.4 - 0.6 - 1.0 - 0.5 - 0.8 - 0.5 - 0.4 - 0.4 - 0.5 - 0.3 - 0.5 - 0.2 - 0.5 - 0.3 - 0.3 - 0.3 - 0.3 - 0.3 - 0.5))

        pipeline_all = VGroup(machine1, machine2, pipe_arrow, in_arrow, out_arrow, 
                              in_label, out_label, flow_caption, expr)

        # ═══════════════════════════════════════════════════════════
        # SCENE 3: RATE 1 — Tripling machine's rate (7s)
        # ═══════════════════════════════════════════════════════════
        dur = DUR("rate1")

        # Highlight machine 1
        m1_glow = SurroundingRectangle(
            machine1[0], color=ORANGE, stroke_width=3, buff=0.05, 
            corner_radius=0.15, fill_color=ORANGE, fill_opacity=0.08
        )
        
        rate1_text = MathTex(
            r"\text{Rate: } \times 3",
            font_size=FS_KEY_FACT, color=ORANGE
        )
        rate1_text.move_to([0, PIPE_Y - 2.2, 0])
        
        # Show the nudge: small arrow with Δx
        nudge_in = MathTex(r"\Delta x", font_size=FS_RATE_LABEL, color=GREEN)
        nudge_in.next_to(machine1[0], LEFT, buff=0.4)
        nudge_out = MathTex(r"3 \cdot \Delta x", font_size=FS_RATE_LABEL, color=GREEN)
        nudge_out.next_to(machine1[0], RIGHT, buff=0.15)

        self.add_sound(AUDIO("rate1"))
        self.play(Create(m1_glow), run_time=0.3)
        self.play(
            machine2.animate.set_opacity(0.3),
            pipe_arrow.animate.set_opacity(0.3),
            out_arrow.animate.set_opacity(0.3),
            out_label.animate.set_opacity(0.3),
            flow_caption.animate.set_opacity(0.3),
            run_time=0.3
        )
        self.play(FadeIn(nudge_in, shift=RIGHT * 0.2), run_time=0.3)
        self.play(
            nudge_in.animate.move_to(machine1.get_center()),
            run_time=0.4
        )
        self.play(
            FadeOut(nudge_in),
            FadeIn(nudge_out, shift=RIGHT * 0.2),
            run_time=0.3
        )
        self.play(Write(rate1_text), run_time=0.5)
        self.wait(max(0.3, dur - 0.3 - 0.3 - 0.3 - 0.4 - 0.3 - 0.5))
        self.wait(0.5)

        # ═══════════════════════════════════════════════════════════
        # SCENE 4: RATE 2 — Squaring machine's rate at u=6 (9s)
        # ═══════════════════════════════════════════════════════════
        dur = DUR("rate2")

        # Restore machine 2, dim machine 1
        m2_glow = SurroundingRectangle(
            machine2[0], color=CYAN, stroke_width=3, buff=0.05,
            corner_radius=0.15, fill_color=CYAN, fill_opacity=0.08
        )
        
        rate2_text = MathTex(
            r"\text{Rate at } u\!=\!6\text{: } \times 12",
            font_size=FS_KEY_FACT, color=CYAN
        )
        rate2_text.move_to([0, PIPE_Y - 2.9, 0])

        # Derivative explanation
        rate2_why = MathTex(
            r"\frac{d}{du}[u^2] = 2u = 2(6) = 12",
            font_size=FS_RATE_LABEL, color=CYAN
        )
        rate2_why.set_opacity(0.7)
        rate2_why.move_to([0, PIPE_Y - 3.4, 0])
        _clamp(rate2_why)

        self.add_sound(AUDIO("rate2"))
        self.play(
            FadeOut(m1_glow),
            FadeOut(nudge_out),
            machine1.animate.set_opacity(0.3),
            machine2.animate.set_opacity(1.0),
            pipe_arrow.animate.set_opacity(1.0),
            Create(m2_glow),
            run_time=0.4
        )
        
        # Nudge entering machine 2
        nudge2_in = MathTex(r"\Delta u", font_size=FS_RATE_LABEL, color=GREEN)
        nudge2_in.next_to(machine2[0], LEFT, buff=0.15)
        nudge2_out = MathTex(r"12 \cdot \Delta u", font_size=FS_RATE_LABEL, color=GREEN)
        nudge2_out.next_to(machine2[0], RIGHT, buff=0.15)
        
        self.play(FadeIn(nudge2_in, shift=RIGHT * 0.2), run_time=0.3)
        self.play(
            nudge2_in.animate.move_to(machine2.get_center()),
            run_time=0.4
        )
        self.play(
            FadeOut(nudge2_in),
            FadeIn(nudge2_out, shift=RIGHT * 0.2),
            run_time=0.3
        )
        self.play(Write(rate2_text), run_time=0.5)
        self.play(FadeIn(rate2_why), run_time=0.4)
        self.wait(max(0.3, dur - 0.4 - 0.3 - 0.4 - 0.3 - 0.5 - 0.4))
        self.wait(0.5)

        # ═══════════════════════════════════════════════════════════
        # SCENE 5: MULTIPLY — The moment (11s)
        # ═══════════════════════════════════════════════════════════
        dur = DUR("multiply")

        # Restore everything, clear nudges
        self.play(
            FadeOut(m2_glow), FadeOut(nudge2_out), FadeOut(rate2_why),
            machine1.animate.set_opacity(1.0),
            machine2.animate.set_opacity(1.0),
            pipe_arrow.animate.set_opacity(1.0),
            out_arrow.animate.set_opacity(1.0),
            out_label.animate.set_opacity(1.0),
            flow_caption.animate.set_opacity(0.0),
            run_time=0.4
        )

        self.add_sound(AUDIO("multiply"))

        # Animated pulse: green dot flows through both machines
        pulse = Dot(radius=0.12, color=GREEN).set_glow_factor(1.0)
        pulse.move_to(in_label.get_center())
        self.add(pulse)

        # Flow through machine 1
        self.play(pulse.animate.move_to(machine1[0].get_left()), run_time=0.4)
        # Inside machine 1 — pulse grows (×3)
        self.play(
            pulse.animate.move_to(machine1[0].get_right()).scale(1.5),
            rate1_text.animate.set_color(GREEN),
            Flash(machine1[0], color=ORANGE, line_length=0.2, num_lines=8, run_time=0.4),
            run_time=0.6
        )
        rate1_text.set_color(ORANGE)

        # Flow to machine 2
        self.play(pulse.animate.move_to(machine2[0].get_left()), run_time=0.3)
        # Inside machine 2 — pulse grows MORE (×12)
        self.play(
            pulse.animate.move_to(machine2[0].get_right()).scale(1.8),
            rate2_text.animate.set_color(GREEN),
            Flash(machine2[0], color=CYAN, line_length=0.2, num_lines=8, run_time=0.4),
            run_time=0.6
        )
        rate2_text.set_color(CYAN)
        
        # Pulse exits
        self.play(
            pulse.animate.move_to(out_label.get_center()),
            run_time=0.3
        )
        self.play(FadeOut(pulse), run_time=0.2)

        # The product — BIG
        product = MathTex(r"3", r"\times", r"12", r"=", r"36",
                         font_size=FS_PUNCHLINE, color=WHITE)
        product[0].set_color(ORANGE)
        product[2].set_color(CYAN)
        product[4].set_color(GREEN)
        _clamp(product)
        product.move_to([0, PIPE_Y - 2.0, 0])

        product_box = SurroundingRectangle(
            product, color=BOX_BORDER, fill_color=BOX_FILL,
            fill_opacity=0.6, buff=0.25, corner_radius=0.1, stroke_width=2,
        )
        
        self.play(FadeIn(product_box), Write(product), run_time=0.8)
        self.play(
            product[4].animate.scale(1.3),
            run_time=0.3
        )
        self.play(product[4].animate.scale(1/1.3), run_time=0.2)
        
        self.wait(max(0.5, dur - 0.4 - 0.4 - 0.6 - 0.3 - 0.6 - 0.3 - 0.2 - 0.8 - 0.3 - 0.2))
        self.wait(1.0)  # LET IT BREATHE

        # ═══════════════════════════════════════════════════════════
        # SCENE 6: FORMULA — earned, not given (6s)
        # ═══════════════════════════════════════════════════════════
        dur = DUR("formula")

        # Fade pipeline, keep rates and product
        self.play(
            FadeOut(VGroup(machine1, machine2, pipe_arrow, in_arrow, out_arrow,
                          in_label, out_label, expr, flow_caption)),
            rate1_text.animate.move_to([-0.9, 2.0, 0]),
            rate2_text.animate.move_to([0.9, 2.0, 0]),
            VGroup(product_box, product).animate.move_to([0, 0.8, 0]),
            run_time=0.5
        )

        self.add_sound(AUDIO("formula"))

        # The formula — appears piece by piece
        formula = MathTex(
            r"\frac{dy}{dx}", r"=",
            r"\underbrace{2u}_{f'(u)}", r"\cdot",
            r"\underbrace{3}_{g'(x)}",
            font_size=FS_EQUATION, color=WHITE
        )
        _clamp(formula)
        formula.move_to([0, -0.8, 0])
        
        # Color the parts
        formula[2].set_color(CYAN)
        formula[4].set_color(ORANGE)

        self.play(Write(formula[0]), Write(formula[1]), run_time=0.4)  # dy/dx =
        self.play(Write(formula[2]), run_time=0.5)  # f'(u)
        self.play(Write(formula[3]), Write(formula[4]), run_time=0.5)  # · g'(x)
        
        self.wait(max(0.3, dur - 0.5 - 0.4 - 0.5 - 0.5))
        self.wait(0.5)

        # ═══════════════════════════════════════════════════════════
        # SCENE 7: PUNCHLINE (6s) — Music drops, silence
        # ═══════════════════════════════════════════════════════════
        dur = DUR("punchline")

        # Dim everything
        self.play(
            FadeOut(rate1_text), FadeOut(rate2_text),
            FadeOut(product_box), FadeOut(product),
            formula.animate.set_opacity(0.3).shift(UP * 0.5),
            run_time=0.4
        )

        self.add_sound(AUDIO("punchline"))

        punch = MathTex(
            r"\text{Two machines. Two rates. Multiply.}",
            font_size=FS_KEY_FACT, color=GREEN
        )
        _clamp(punch, MAX_WIDTH * 0.9)
        punch_box = SurroundingRectangle(
            punch, color=BOX_BORDER, fill_color=BOX_FILL,
            fill_opacity=0.6, buff=0.3, corner_radius=0.1, stroke_width=2,
        )
        punch_group = VGroup(punch_box, punch)
        punch_group.move_to([0, MATH_CENTER_Y - 0.3, 0])

        thats_it = Text("That's the whole chain rule.", font_size=FS_CALLOUT, color=CYAN, weight=BOLD)
        _clamp(thats_it)
        thats_it.move_to([0, MATH_CENTER_Y - 1.4, 0])

        self.play(FadeIn(punch_group), run_time=0.6)
        self.play(Circumscribe(punch_group, color=GREEN, run_time=0.5))
        self.wait(0.8)
        self.play(Write(thats_it), run_time=0.5)
        self.wait(max(0.5, dur - 0.4 - 0.6 - 0.5 - 0.8 - 0.5))
        self.wait(1.5)  # SILENCE — let it land

        # ═══════════════════════════════════════════════════════════
        # END CARD
        # ═══════════════════════════════════════════════════════════
        self.play(
            FadeOut(VGroup(formula, punch_group, thats_it)),
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
        self.play(FadeIn(VGroup(wm_glow, wordmark), shift=UP * 0.2), run_time=0.4)
        self.wait(1.2)
        self.play(FadeOut(end_card), run_time=0.3)
