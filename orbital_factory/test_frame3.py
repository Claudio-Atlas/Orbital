"""
Test Frame 3: Fixed zones, clipped graph, better proportions.
Frame: 4.5 wide × 8.0 tall (9:16)
"""
from manim import *
import numpy as np

config.frame_width = 8.0 * (1080/1920)  # 4.5
config.frame_height = 8.0

class TestFrame3(Scene):
    def construct(self):
        self.camera.background_color = "#000000"
        
        fw = config.frame_width   # 4.5
        fh = config.frame_height  # 8.0
        
        # Safe content width: 75% of frame (leave room for TikTok buttons on right)
        safe_w = fw * 0.75  # 3.375
        content_max_w = safe_w * 0.92  # 3.105 — max width for any content
        
        # ═══ ZONE A: Hook/Context (top) ═══
        # Y: 2.8 to 3.6
        hook = Text("solve this 👇", font_size=24, color=WHITE)
        hook.move_to([0, 3.2, 0])
        self.add(hook)
        
        # ═══ ZONE B: Math Work (middle) ═══
        # Y: 0.8 to 2.5
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
        
        # ═══ ZONE C: Graph HERO (bottom) ═══
        # Y: -3.5 to -0.2
        graph_w = safe_w * 0.90  # graph width
        graph_h = 2.8  # graph height
        
        axes = Axes(
            x_range=[-3, 4, 1],
            y_range=[-8, 22, 5],
            x_length=graph_w,
            y_length=graph_h,
            axis_config={"color": GREY_B, "include_numbers": True, "font_size": 12,
                         "numbers_to_exclude": [0]},
            tips=False,
        )
        axes.move_to([0, -1.8, 0])
        
        # Plot with clipping — restrict x range to avoid bleeding
        graph = axes.plot(lambda x: 3*x**2 + 2*x - 5, x_range=[-2.8, 3.5], color="#22D3EE", stroke_width=2.5)
        
        # Clip graph to axes bounds
        clip_rect = Rectangle(width=graph_w + 0.1, height=graph_h + 0.1)
        clip_rect.move_to(axes.get_center())
        graph.set_clip_path(clip_rect)
        
        graph_label = MathTex(r"f(x)", color="#22D3EE", font_size=18)
        # Place label inside the axes area
        graph_label.move_to(axes.c2p(3, 15))
        
        self.add(axes, graph, graph_label)
        
        # ═══ WATERMARK ═══
        watermark = Text("ORBITAL", font_size=12, color=WHITE, weight=BOLD)
        watermark.set_opacity(0.4)
        watermark.move_to([fw/2 - 0.5, -fh/2 + 0.3, 0])
        self.add(watermark)
        
        # Debug: show content width
        debug = Text(f"Content max: {content_max_w:.2f} | Eq: {eq.width:.2f}", font_size=10, color=GREY)
        debug.to_edge(DOWN, buff=0.15)
        self.add(debug)
        
        self.wait(3)
