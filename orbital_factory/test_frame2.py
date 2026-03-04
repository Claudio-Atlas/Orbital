"""
Test Frame 2: Understanding 9:16 Manim coordinates properly.

Key insight: At 1080x1920, Manim keeps frame_height=8.0 and sets
frame_width = 8.0 * (1080/1920) = 4.5 units wide.

So the usable canvas is ~4.5 units wide × 8.0 units tall.
65% of 4.5 = 2.925 units max width for content.
"""
from manim import *

config.frame_width = 8.0 * (1080/1920)  # = 4.5
config.frame_height = 8.0

class TestFrame2(Scene):
    def construct(self):
        self.camera.background_color = "#000000"
        
        fw = config.frame_width   # should be 4.5
        fh = config.frame_height  # should be 8.0
        
        # Draw safe zone (65% width, 70% height — avoid TikTok UI)
        safe_w = fw * 0.65  # ~2.925
        safe_h = fh * 0.70  # ~5.6
        safe_rect = Rectangle(
            width=safe_w, height=safe_h,
            color=GREY, stroke_width=1, stroke_opacity=0.3,
        )
        self.add(safe_rect)
        
        # Debug info
        debug = Text(f"Frame: {fw:.2f} x {fh:.2f}", font_size=16, color=GREY)
        debug.to_edge(UP, buff=0.2)
        self.add(debug)
        
        # Zone markers
        # Zone A (top context): Y = 2.5 to 3.5
        zone_a = Rectangle(width=safe_w, height=1.0, color=BLUE, stroke_width=1, stroke_opacity=0.2, fill_opacity=0.05, fill_color=BLUE)
        zone_a.move_to([0, 3.0, 0])
        zone_a_label = Text("Zone A", font_size=12, color=BLUE).move_to(zone_a.get_corner(UL) + RIGHT*0.4 + DOWN*0.15)
        self.add(zone_a, zone_a_label)
        
        # Zone B (math): Y = 0.5 to 2.0
        zone_b = Rectangle(width=safe_w, height=1.5, color=GREEN, stroke_width=1, stroke_opacity=0.2, fill_opacity=0.05, fill_color=GREEN)
        zone_b.move_to([0, 1.25, 0])
        zone_b_label = Text("Zone B (Math)", font_size=12, color=GREEN).move_to(zone_b.get_corner(UL) + RIGHT*0.6 + DOWN*0.15)
        self.add(zone_b, zone_b_label)
        
        # Zone C (graph hero): Y = -3.0 to 0.0
        zone_c = Rectangle(width=safe_w, height=3.0, color=TEAL, stroke_width=1, stroke_opacity=0.2, fill_opacity=0.05, fill_color=TEAL)
        zone_c.move_to([0, -1.5, 0])
        zone_c_label = Text("Zone C (Graph)", font_size=12, color=TEAL).move_to(zone_c.get_corner(UL) + RIGHT*0.6 + DOWN*0.15)
        self.add(zone_c, zone_c_label)
        
        # THE EQUATION — must fit in Zone B
        max_content_width = safe_w * 0.90  # 90% of safe zone width
        
        eq = MathTex(r"f(x) = 3x^2 + 2x - 5", color=WHITE)
        if eq.width > max_content_width:
            eq.scale(max_content_width / eq.width)
        eq.move_to([0, 1.25, 0])  # Center of Zone B
        self.add(eq)
        
        # Width debug
        width_info = Text(f"Eq: {eq.width:.2f} / Max: {max_content_width:.2f}", font_size=14, color=YELLOW)
        width_info.next_to(eq, DOWN, buff=0.3)
        self.add(width_info)
        
        # A small graph in Zone C to test proportions
        axes = Axes(
            x_range=[-3, 4, 1],
            y_range=[-6, 20, 4],
            x_length=safe_w * 0.85,  # 85% of safe width
            y_length=2.5,  # fits in Zone C
            axis_config={"color": WHITE, "include_numbers": True, "font_size": 14},
        )
        axes.move_to([0, -1.5, 0])  # Center of Zone C
        
        graph = axes.plot(lambda x: 3*x**2 + 2*x - 5, color="#22D3EE")
        graph_label = MathTex(r"f(x)", color="#22D3EE", font_size=20)
        graph_label.next_to(graph, UR, buff=0.1)
        
        self.add(axes, graph, graph_label)
        
        self.wait(3)
