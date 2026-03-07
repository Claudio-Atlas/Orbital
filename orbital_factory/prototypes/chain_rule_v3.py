"""
Why the Chain Rule Works (It's Just Multiplication) — v3
=========================================================
Fixes from v2 review:
- Better gears (bigger, more teeth)
- Hook formula gets purple box + higher opacity
- Bigger machines, bigger text, NO overlaps anywhere
- (3x)² larger
- All text overlaps fixed — proper clear before new content
- Slower pacing, more breathing room
- Punchline scene: formula fully faded before punch text

Render:
  cd ~/Desktop/Orbital/orbital_factory && source venv/bin/activate
  PATH="/Library/TeX/texbin:$PATH" manim render prototypes/chain_rule_v3.py ChainRuleV3 \
    -o chain_rule_v3.mp4 --format mp4 -r 1080,1920 --frame_rate 60 --flush_cache
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

# ── LOCKED FONT SIZES ──
FS_PUNCHLINE = 42
FS_KEY_FACT = 28
FS_CALLOUT = 24
FS_TITLE = 26
FS_EQUATION = 30
FS_CAPTION = 24
FS_WATERMARK = 10

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


def _make_gear(radius, n_teeth, color, center, tooth_len=0.14, stroke_w=3):
    """Build a proper gear: circle + radiating teeth (trapezoid-ish)."""
    gear_parts = []
    # Main circle
    circle = Circle(radius=radius, color=color, stroke_width=stroke_w,
                    fill_color=BOX_FILL, fill_opacity=0.4)
    circle.move_to(center)
    gear_parts.append(circle)
    
    # Center dot
    center_dot = Dot(radius=0.06, color=color, fill_opacity=0.8).move_to(center)
    gear_parts.append(center_dot)
    
    # Teeth — wider rectangles radiating out
    for i in range(n_teeth):
        angle = i * TAU / n_teeth
        inner_pt = np.array(center) + radius * np.array([np.cos(angle), np.sin(angle), 0])
        outer_pt = np.array(center) + (radius + tooth_len) * np.array([np.cos(angle), np.sin(angle), 0])
        
        # Make a small rectangle tooth
        perp = np.array([-np.sin(angle), np.cos(angle), 0])
        tooth_width = 0.08
        p1 = inner_pt + perp * tooth_width
        p2 = inner_pt - perp * tooth_width
        p3 = outer_pt - perp * tooth_width * 0.7
        p4 = outer_pt + perp * tooth_width * 0.7
        tooth = Polygon(p1, p2, p3, p4, color=color, stroke_width=stroke_w - 0.5,
                        fill_color=color, fill_opacity=0.3)
        gear_parts.append(tooth)
    
    return VGroup(*gear_parts)


def _make_machine(label, sublabel, color, x_pos, y_pos, width=1.7, height=1.4):
    """Build a function machine: rounded box with label + sublabel. BIGGER than v2."""
    box = RoundedRectangle(
        width=width, height=height,
        color=color, fill_color=BOX_FILL,
        fill_opacity=0.7, stroke_width=2.5, corner_radius=0.12,
    )
    box.move_to([x_pos, y_pos, 0])
    
    lbl = Text(label, font_size=24, color=color, weight=BOLD)
    lbl.move_to(box.get_center() + UP * 0.22)
    
    sub = MathTex(sublabel, font_size=22, color=WHITE)
    sub.set_opacity(0.8)
    sub.move_to(box.get_center() + DOWN * 0.25)
    
    in_port = Dot(radius=0.07, color=color).move_to(box.get_left())
    out_port = Dot(radius=0.07, color=color).move_to(box.get_right())
    
    return VGroup(box, lbl, sub, in_port, out_port)


def _make_number_dot(value, color=CYAN, size=38):
    """A number inside a glowing circle — flows through the pipeline."""
    num = MathTex(str(value), font_size=size, color=color)
    circle = Circle(radius=0.35, color=color, fill_color=color, fill_opacity=0.15, stroke_width=1.5)
    circle.move_to(num.get_center())
    return VGroup(circle, num)


class ChainRuleV3(Scene):
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
        # SCENE 1: HOOK (5s) — Big gears + boxed formula
        # ═══════════════════════════════════════════════════════════
        dur = DUR("hook")

        # Two interlocking gears — BIGGER and more detailed
        gear1 = _make_gear(
            radius=0.7, n_teeth=10, color=VIOLET,
            center=[-0.5, 2.2, 0], tooth_len=0.16, stroke_w=2.5
        )
        gear2 = _make_gear(
            radius=0.5, n_teeth=8, color=CYAN,
            center=[0.7, 2.2, 0], tooth_len=0.13, stroke_w=2.5
        )

        # The scary formula — IN A PURPLE BOX, visible
        scary = MathTex(
            r"\frac{d}{dx}[f(g(x))] = f'(g(x)) \cdot g'(x)",
            font_size=FS_CALLOUT, color=WHITE
        )
        _clamp(scary)
        scary.move_to([0, 0.5, 0])
        
        scary_box = SurroundingRectangle(
            scary, color=BOX_BORDER, fill_color=BOX_FILL,
            fill_opacity=0.6, buff=0.2, corner_radius=0.1, stroke_width=2,
        )

        # Hook text
        hook_text = Text("Just multiplication.", font_size=FS_KEY_FACT, color=GREEN, weight=BOLD)
        _clamp(hook_text)
        hook_text.move_to([0, -0.5, 0])

        self.add_sound(AUDIO("hook"))
        
        # Gears spin in
        self.play(FadeIn(gear1), FadeIn(gear2), run_time=0.3)
        self.play(
            Rotate(gear1, angle=PI/3, about_point=[-0.5, 2.2, 0]),
            Rotate(gear2, angle=-PI/2.2, about_point=[0.7, 2.2, 0]),
            run_time=1.0
        )
        # Formula + box slam in
        self.play(FadeIn(scary_box), Write(scary), run_time=0.5)
        self.wait(0.3)
        # Hook text
        self.play(FadeIn(hook_text, shift=UP * 0.2), run_time=0.3)
        
        remaining = dur - (0.3 + 1.0 + 0.5 + 0.3 + 0.3)
        self.wait(max(0.5, remaining))

        hook_all = VGroup(gear1, gear2, scary, scary_box, hook_text)

        # ═══════════════════════════════════════════════════════════
        # SCENE 2: COMPOSITION (13s) — Show TWO machines, BIG
        # ═══════════════════════════════════════════════════════════
        dur = DUR("composition")

        self.play(FadeOut(hook_all, shift=UP * 0.3), run_time=0.5)

        # The expression — BIG
        expr = MathTex(r"(3x)^2", font_size=FS_PUNCHLINE + 8, color=WHITE)
        _clamp(expr, MAX_WIDTH * 0.7)
        expr.move_to([0, 2.8, 0])
        
        self.add_sound(AUDIO("composition"))
        self.play(Write(expr), run_time=0.6)
        self.wait(1.2)

        # Decompose: highlight inner (3x) and outer (²)
        inner_highlight = SurroundingRectangle(
            expr[0][1:3],  # "3x"
            color=ORANGE, stroke_width=2.5, buff=0.06, corner_radius=0.05
        )
        inner_label = Text("Machine 1", font_size=18, color=ORANGE, weight=BOLD)
        inner_label.next_to(inner_highlight, DOWN, buff=0.15)
        
        outer_highlight = SurroundingRectangle(
            expr[0],  # whole expression
            color=CYAN, stroke_width=2.5, buff=0.1, corner_radius=0.05
        )
        outer_label = Text("Machine 2", font_size=18, color=CYAN, weight=BOLD)
        outer_label.next_to(outer_highlight, UP, buff=0.15)

        self.play(Create(inner_highlight), FadeIn(inner_label), run_time=0.5)
        self.wait(1.0)
        self.play(Create(outer_highlight), FadeIn(outer_label), run_time=0.5)
        self.wait(0.8)

        # Build two-machine pipeline — CENTERED VERTICALLY, bigger
        PIPE_Y = -0.2
        machine1 = _make_machine("TRIPLE", r"3x", ORANGE, -0.95, PIPE_Y)
        machine2 = _make_machine("SQUARE", r"u^2", CYAN, 0.95, PIPE_Y)
        
        pipe_arrow = Arrow(
            machine1[0].get_right() + RIGHT * 0.1,
            machine2[0].get_left() + LEFT * 0.1,
            color=WHITE, stroke_width=2.5, buff=0, max_tip_length_to_length_ratio=0.25,
        )
        in_arrow = Arrow(
            LEFT * 1.9 + UP * PIPE_Y,
            machine1[0].get_left() + LEFT * 0.1,
            color=WHITE, stroke_width=2, buff=0, max_tip_length_to_length_ratio=0.25,
        )
        in_label = MathTex("x", font_size=FS_CAPTION, color=WHITE)
        in_label.next_to(in_arrow, LEFT, buff=0.08)
        out_arrow = Arrow(
            machine2[0].get_right() + RIGHT * 0.1,
            RIGHT * 1.9 + UP * PIPE_Y,
            color=WHITE, stroke_width=2, buff=0, max_tip_length_to_length_ratio=0.25,
        )
        out_label = MathTex("y", font_size=FS_CAPTION, color=WHITE)
        out_label.next_to(out_arrow, RIGHT, buff=0.08)

        # Transition: shrink expr to top, clear highlights, build pipeline
        self.play(
            FadeOut(VGroup(inner_highlight, inner_label, outer_highlight, outer_label)),
            expr.animate.scale(0.65).move_to([0, 3.2, 0]).set_opacity(0.5),
            run_time=0.5
        )
        self.play(
            Create(in_arrow), FadeIn(in_label),
            FadeIn(machine1),
            run_time=0.6
        )
        self.play(Create(pipe_arrow), run_time=0.3)
        self.play(
            FadeIn(machine2),
            Create(out_arrow), FadeIn(out_label),
            run_time=0.6
        )
        self.wait(0.3)

        # Animate number flowing through
        num_2 = _make_number_dot(2, WHITE, 38)
        num_2.move_to(in_label.get_center())
        num_6 = _make_number_dot(6, ORANGE, 38)
        num_6.move_to(machine1.get_center())
        num_36 = _make_number_dot(36, CYAN, 36)
        num_36.move_to(machine2.get_center())

        self.play(FadeIn(num_2, scale=0.5), run_time=0.3)
        self.play(num_2.animate.move_to(machine1.get_center()), run_time=0.6)
        self.play(
            FadeOut(num_2),
            FadeIn(num_6, scale=1.3),
            Flash(machine1[0], color=ORANGE, line_length=0.2, num_lines=8, run_time=0.3),
            run_time=0.4
        )
        self.play(num_6.animate.move_to(pipe_arrow.get_center()), run_time=0.3)
        self.play(num_6.animate.move_to(machine2.get_center()), run_time=0.3)
        self.play(
            FadeOut(num_6),
            FadeIn(num_36, scale=1.3),
            Flash(machine2[0], color=CYAN, line_length=0.2, num_lines=8, run_time=0.3),
            run_time=0.4
        )
        self.play(num_36.animate.move_to(out_label.get_center() + LEFT * 0.3), run_time=0.3)
        
        # Flow summary — positioned BELOW pipeline with clearance
        flow_caption = MathTex(
            r"2 \xrightarrow{\times 3} 6 \xrightarrow{(\;)^2} 36",
            font_size=FS_CAPTION, color=WHITE
        )
        _clamp(flow_caption)
        flow_caption.move_to([0, PIPE_Y - 1.5, 0])
        self.play(FadeOut(num_36), Write(flow_caption), run_time=0.5)
        
        remaining = dur - (0.5 + 0.6 + 1.2 + 0.5 + 1.0 + 0.5 + 0.8 + 0.5 + 0.6 + 0.3 + 0.6 + 0.3 + 0.3 + 0.6 + 0.4 + 0.3 + 0.3 + 0.4 + 0.3 + 0.5)
        self.wait(max(0.3, remaining))

        # ═══════════════════════════════════════════════════════════
        # SCENE 3: RATE 1 — Tripling machine's rate (7s)
        # ═══════════════════════════════════════════════════════════
        dur = DUR("rate1")

        # CLEAR flow caption first to avoid overlap
        self.play(FadeOut(flow_caption), run_time=0.3)

        # Highlight machine 1, dim machine 2
        m1_glow = SurroundingRectangle(
            machine1[0], color=ORANGE, stroke_width=3, buff=0.08,
            corner_radius=0.15, fill_color=ORANGE, fill_opacity=0.08
        )

        self.add_sound(AUDIO("rate1"))
        self.play(
            Create(m1_glow),
            machine2.animate.set_opacity(0.25),
            pipe_arrow.animate.set_opacity(0.25),
            out_arrow.animate.set_opacity(0.25),
            out_label.animate.set_opacity(0.25),
            run_time=0.4
        )

        # Nudge animation
        nudge_label = Text("nudge x →", font_size=16, color=GREEN)
        nudge_label.next_to(machine1[0], LEFT, buff=0.25)
        result_label = Text("→ 3× bigger", font_size=16, color=GREEN)
        result_label.next_to(machine1[0], RIGHT, buff=0.15)

        self.play(FadeIn(nudge_label, shift=RIGHT * 0.15), run_time=0.4)
        self.wait(0.3)
        self.play(FadeIn(result_label, shift=RIGHT * 0.15), run_time=0.4)
        
        # Rate label — WELL BELOW pipeline
        rate1_text = MathTex(
            r"\text{Rate: } \times 3",
            font_size=FS_KEY_FACT, color=ORANGE
        )
        rate1_text.move_to([0, PIPE_Y - 1.5, 0])
        
        rate1_box = SurroundingRectangle(
            rate1_text, color=ORANGE, fill_color=BOX_FILL,
            fill_opacity=0.4, buff=0.15, corner_radius=0.08, stroke_width=1.5,
        )
        
        self.play(FadeIn(rate1_box), Write(rate1_text), run_time=0.5)
        
        remaining = dur - (0.3 + 0.4 + 0.4 + 0.3 + 0.4 + 0.5)
        self.wait(max(0.5, remaining))

        # ═══════════════════════════════════════════════════════════
        # SCENE 4: RATE 2 — Squaring machine's rate at u=6 (9s)
        # ═══════════════════════════════════════════════════════════
        dur = DUR("rate2")

        # Clear rate 1 nudge labels, switch focus to machine 2
        self.play(
            FadeOut(m1_glow), FadeOut(nudge_label), FadeOut(result_label),
            machine1.animate.set_opacity(0.25),
            machine2.animate.set_opacity(1.0),
            pipe_arrow.animate.set_opacity(1.0),
            run_time=0.4
        )

        m2_glow = SurroundingRectangle(
            machine2[0], color=CYAN, stroke_width=3, buff=0.08,
            corner_radius=0.15, fill_color=CYAN, fill_opacity=0.08
        )

        self.add_sound(AUDIO("rate2"))
        self.play(Create(m2_glow), run_time=0.3)

        # Nudge into machine 2
        nudge2_label = Text("nudge u →", font_size=16, color=GREEN)
        nudge2_label.next_to(machine2[0], LEFT, buff=0.15)
        result2_label = Text("→ 12× bigger", font_size=16, color=GREEN)
        result2_label.next_to(machine2[0], RIGHT, buff=0.12)

        self.play(FadeIn(nudge2_label, shift=RIGHT * 0.15), run_time=0.4)
        self.wait(0.3)
        self.play(FadeIn(result2_label, shift=RIGHT * 0.15), run_time=0.4)

        # Rate 2 label — BELOW rate 1 with spacing
        rate2_text = MathTex(
            r"\text{Rate at } u\!=\!6\text{: } \times 12",
            font_size=FS_KEY_FACT, color=CYAN
        )
        rate2_text.move_to([0, PIPE_Y - 2.3, 0])
        
        rate2_box = SurroundingRectangle(
            rate2_text, color=CYAN, fill_color=BOX_FILL,
            fill_opacity=0.4, buff=0.15, corner_radius=0.08, stroke_width=1.5,
        )

        # Why 12? Show the derivative
        rate2_why = MathTex(
            r"\frac{d}{du}[u^2] = 2u = 2(6) = 12",
            font_size=20, color=CYAN
        )
        rate2_why.set_opacity(0.7)
        rate2_why.move_to([0, PIPE_Y - 3.0, 0])
        _clamp(rate2_why)

        self.play(FadeIn(rate2_box), Write(rate2_text), run_time=0.5)
        self.wait(0.4)
        self.play(FadeIn(rate2_why), run_time=0.4)
        
        remaining = dur - (0.4 + 0.3 + 0.4 + 0.3 + 0.4 + 0.5 + 0.4 + 0.4)
        self.wait(max(0.5, remaining))

        # ═══════════════════════════════════════════════════════════
        # SCENE 5: MULTIPLY — The moment (11s) — BIGGEST SCENE
        # ═══════════════════════════════════════════════════════════
        dur = DUR("multiply")

        # CLEAR everything except machines and rate boxes
        self.play(
            FadeOut(m2_glow), FadeOut(nudge2_label), FadeOut(result2_label),
            FadeOut(rate2_why),
            machine1.animate.set_opacity(1.0),
            machine2.animate.set_opacity(1.0),
            pipe_arrow.animate.set_opacity(1.0),
            out_arrow.animate.set_opacity(1.0),
            out_label.animate.set_opacity(1.0),
            # Move rate boxes up to flank the pipeline
            VGroup(rate1_box, rate1_text).animate.move_to([-0.95, PIPE_Y - 1.3, 0]),
            VGroup(rate2_box, rate2_text).animate.move_to([0.95, PIPE_Y - 1.3, 0]),
            run_time=0.5
        )

        self.add_sound(AUDIO("multiply"))

        # Animated GREEN pulse flows through the full pipeline
        pulse = Dot(radius=0.15, color=GREEN).set_glow_factor(1.2)
        pulse.move_to(in_label.get_center())
        trail = TracedPath(pulse.get_center, stroke_color=GREEN, stroke_width=2, stroke_opacity=0.4)
        self.add(pulse, trail)

        # Flow through machine 1
        self.play(pulse.animate.move_to(machine1[0].get_center()), run_time=0.6)
        self.play(
            pulse.animate.scale(1.5),
            Flash(machine1[0], color=ORANGE, line_length=0.25, num_lines=10, run_time=0.4),
            rate1_text.animate.set_color(GREEN),
            run_time=0.5
        )
        rate1_text.set_color(ORANGE)  # Reset color after flash

        # Flow through pipe to machine 2
        self.play(pulse.animate.move_to(machine2[0].get_center()), run_time=0.6)
        self.play(
            pulse.animate.scale(1.5),
            Flash(machine2[0], color=CYAN, line_length=0.25, num_lines=10, run_time=0.4),
            rate2_text.animate.set_color(GREEN),
            run_time=0.5
        )
        rate2_text.set_color(CYAN)

        # Pulse exits with a burst
        self.play(pulse.animate.move_to(out_label.get_center()), run_time=0.4)
        self.play(
            Flash(pulse, color=GREEN, line_length=0.3, num_lines=12, run_time=0.4),
            FadeOut(pulse), FadeOut(trail),
            run_time=0.5
        )

        # THE PRODUCT — big, centered, below everything, with proper spacing
        # First clear rate boxes to make room
        self.play(
            FadeOut(VGroup(rate1_box, rate1_text, rate2_box, rate2_text)),
            run_time=0.3
        )

        product = MathTex(r"3", r"\times", r"12", r"=", r"36",
                         font_size=FS_PUNCHLINE, color=WHITE)
        product[0].set_color(ORANGE)
        product[2].set_color(CYAN)
        product[4].set_color(GREEN)
        _clamp(product)
        product.move_to([0, PIPE_Y - 1.6, 0])

        product_box = SurroundingRectangle(
            product, color=BOX_BORDER, fill_color=BOX_FILL,
            fill_opacity=0.6, buff=0.25, corner_radius=0.1, stroke_width=2.5,
        )

        self.play(FadeIn(product_box), Write(product), run_time=0.8)
        self.wait(0.3)
        # Pulse the 36
        self.play(product[4].animate.scale(1.4), run_time=0.25)
        self.play(product[4].animate.scale(1/1.4), run_time=0.2)
        
        remaining = dur - (0.5 + 0.6 + 0.5 + 0.6 + 0.5 + 0.4 + 0.5 + 0.3 + 0.8 + 0.3 + 0.25 + 0.2)
        self.wait(max(1.0, remaining))  # LET IT BREATHE

        # ═══════════════════════════════════════════════════════════
        # SCENE 6: FORMULA — earned, not given (6s)
        # ═══════════════════════════════════════════════════════════
        dur = DUR("formula")

        # FULLY CLEAR the pipeline — clean slate for formula
        self.play(
            FadeOut(VGroup(machine1, machine2, pipe_arrow, in_arrow, out_arrow,
                          in_label, out_label, expr)),
            VGroup(product_box, product).animate.move_to([0, 2.0, 0]),
            run_time=0.5
        )

        self.add_sound(AUDIO("formula"))

        # The formula — built piece by piece, centered with no overlap
        formula_outer = MathTex(r"f'(g(x))", font_size=FS_EQUATION, color=CYAN)
        formula_dot = MathTex(r"\cdot", font_size=FS_EQUATION, color=WHITE)
        formula_inner = MathTex(r"g'(x)", font_size=FS_EQUATION, color=ORANGE)
        formula_eq = MathTex(r"\frac{dy}{dx} =", font_size=FS_EQUATION, color=WHITE)
        
        # Arrange horizontally
        formula_group = VGroup(formula_eq, formula_outer, formula_dot, formula_inner)
        formula_group.arrange(RIGHT, buff=0.12)
        _clamp(formula_group)
        formula_group.move_to([0, 0.2, 0])
        
        formula_box = SurroundingRectangle(
            formula_group, color=BOX_BORDER, fill_color=BOX_FILL,
            fill_opacity=0.6, buff=0.2, corner_radius=0.1, stroke_width=2.5,
        )

        # Labels below
        outer_tag = Text("outside rate", font_size=14, color=CYAN)
        outer_tag.next_to(formula_outer, DOWN, buff=0.25)
        inner_tag = Text("inside rate", font_size=14, color=ORANGE)
        inner_tag.next_to(formula_inner, DOWN, buff=0.25)

        self.play(FadeIn(formula_box), run_time=0.3)
        self.play(Write(formula_eq), run_time=0.4)
        self.play(Write(formula_outer), FadeIn(outer_tag), run_time=0.5)
        self.play(Write(formula_dot), run_time=0.15)
        self.play(Write(formula_inner), FadeIn(inner_tag), run_time=0.5)
        
        remaining = dur - (0.5 + 0.3 + 0.4 + 0.5 + 0.15 + 0.5)
        self.wait(max(0.5, remaining))

        # ═══════════════════════════════════════════════════════════
        # SCENE 7: PUNCHLINE (6s) — Clean, no overlap
        # ═══════════════════════════════════════════════════════════
        dur = DUR("punchline")

        # FULLY CLEAR formula and product — nothing left
        self.play(
            FadeOut(VGroup(product_box, product)),
            FadeOut(VGroup(formula_box, formula_group, outer_tag, inner_tag)),
            run_time=0.5
        )

        self.add_sound(AUDIO("punchline"))

        # Punchline — centered, clean, large
        punch = Text("Two machines.\nTwo rates.\nMultiply.",
                     font_size=FS_KEY_FACT, color=GREEN, weight=BOLD,
                     line_spacing=1.4)
        _clamp(punch, MAX_WIDTH * 0.85)
        punch.move_to([0, 1.2, 0])
        
        punch_box = SurroundingRectangle(
            punch, color=BOX_BORDER, fill_color=BOX_FILL,
            fill_opacity=0.6, buff=0.3, corner_radius=0.1, stroke_width=2.5,
        )

        thats_it = Text("That's the whole chain rule.",
                        font_size=FS_CALLOUT, color=CYAN, weight=BOLD)
        _clamp(thats_it)
        thats_it.move_to([0, -0.6, 0])

        self.play(FadeIn(punch_box), FadeIn(punch), run_time=0.5)
        self.play(Circumscribe(punch_box, color=GREEN, run_time=0.6))
        self.wait(1.0)
        self.play(Write(thats_it), run_time=0.5)
        
        remaining = dur - (0.5 + 0.5 + 0.6 + 1.0 + 0.5)
        self.wait(max(1.0, remaining))
        self.wait(1.5)  # EXTRA SILENCE — music drops, let it land

        # ═══════════════════════════════════════════════════════════
        # END CARD — Lissajous
        # ═══════════════════════════════════════════════════════════
        self.play(FadeOut(VGroup(punch_box, punch, thats_it)), run_time=0.4)

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
        self.play(FadeIn(VGroup(wm_glow, wordmark), shift=UP * 0.2), run_time=0.4)
        self.wait(1.5)
        self.play(FadeOut(end_card), run_time=0.3)
