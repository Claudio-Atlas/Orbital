"""
Test Frame 4: Three fixes applied.
1. No debug text
2. Watermark + graph label shifted left to avoid TikTok buttons
3. Parabola clipped to Zone C via restricted x_range + y_range
"""
from manim import *
import numpy as np

config.frame_width = 8.0 * (1080/1920)  # 4.5
config.frame_height = 8.0

class TestFrame4(Scene):
    def construct(self):
        self.camera.background_color = "#000000"
        
        fw = config.frame_width   # 4.5
        fh = config.frame_height  # 8.0
        
        safe_w = fw * 0.75  # 3.375
        content_max_w = safe_w * 0.92  # 3.105
        
        # ═══ ZONE A: Hook ═══
        hook = Text("solve this 👇", font_size=24, color=WHITE)
        hook.move_to([0, 3.2, 0])
        self.add(hook)
        
        # ═══ ZONE B: Math ═══
        eq = MathTex(r"f(x) = 3x^2 + 2x - 5", color=WHITE, font_size=36)
        if eq.width > content_max_w:
            eq.scale(content_max_w / eq.width)
        eq.move_to([0, 1.8, 0])
        self.add(eq)
        
        # Power rule box
        rule_inner = MathTex(r"\frac{d}{dx}[x^n] = nx^{n-1}", color=WHITE, font_size=28)
        if rule_inner.width > content_max_w * 0.85:
            rule_inner.scale(content_max_w * 0.85 / rule_inner.width)
        rule_box = SurroundingRectangle(
            rule_inner, color="#8B5CF6", buff=0.15,
            stroke_width=2, corner_radius=0.08,
            fill_color="#1a1130", fill_opacity=0.6,
        )
        rule_label = Text("Power Rule", font_size=14, color="#22D3EE")
        rule_group = VGroup(rule_box, rule_inner)
        rule_group.move_to([0, 1.0, 0])
        rule_label.next_to(rule_box, UP, buff=0.08)
        self.add(rule_group, rule_label)
        
        # ═══ ZONE C: Graph HERO ═══
        graph_w = safe_w * 0.90
        graph_h = 2.8
        graph_center_y = -1.8
        
        # Clamp y_range so the curve doesn't visually escape the axes
        axes = Axes(
            x_range=[-3, 3, 1],
            y_range=[-7, 25, 5],
            x_length=graph_w,
            y_length=graph_h,
            axis_config={"color": GREY_B, "include_numbers": True, "font_size": 12,
                         "numbers_to_exclude": [0, -5]},
            tips=False,
        )
        axes.move_to([0, graph_center_y, 0])
        
        # Restrict x_range of the plot so the curve stays within axes bounds
        # y = 3x² + 2x - 5, solve for y=22: x ≈ 2.5, so cap at x=2.7
        graph = axes.plot(
            lambda x: 3*x**2 + 2*x - 5, 
            x_range=[-2.8, 2.8],  # Clipped to stay within axes y_range of 25
            color="#22D3EE", 
            stroke_width=2.5,
        )
        
        # FIX 2: Graph label shifted left (away from TikTok buttons)
        graph_label = MathTex(r"f(x)", color="#22D3EE", font_size=18)
        graph_label.move_to(axes.c2p(-2.2, 18))
        
        self.add(axes, graph, graph_label)
        
        # ═══ FIX 2: WATERMARK shifted left ═══
        watermark = Text("ORBITAL", font_size=12, color=WHITE, weight=BOLD)
        watermark.set_opacity(0.4)
        # Shift left from far-right to avoid TikTok share/comment buttons
        watermark.move_to([-fw/2 + 0.6, -fh/2 + 0.3, 0])
        self.add(watermark)
        
        self.wait(3)
