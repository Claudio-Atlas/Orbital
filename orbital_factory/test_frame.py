"""
Test Frame 1: Single equation, properly sized and centered on 9:16 canvas.
Goal: Verify the equation fits with breathing room on both sides.
"""
from manim import *

class TestFrame(Scene):
    def construct(self):
        self.camera.background_color = "#000000"
        
        # First: understand our canvas
        # At 1080x1920 (9:16), Manim's default frame is:
        #   width = 14.222 * (1080/1920) = 8.0 units wide
        #   height = 8.0 * (1920/1080) = 14.222 units tall
        # Actually let's just check:
        fw = config.frame_width
        fh = config.frame_height
        
        # Draw safe zone boundary so we can see it
        safe_rect = Rectangle(
            width=fw * 0.65,  # 65% of frame width
            height=fh * 0.7,  # 70% of frame height (avoid top/bottom TikTok UI)
            color=GREY,
            stroke_width=1,
            stroke_opacity=0.3,
        )
        self.add(safe_rect)
        
        # Show frame dimensions as debug text
        debug = Text(f"Frame: {fw:.1f} x {fh:.1f}", font_size=20, color=GREY)
        debug.to_edge(UP, buff=0.3)
        self.add(debug)
        
        # THE TEST: A calculus equation that must fit within 65% width
        eq = MathTex(r"f(x) = 3x^2 + 2x - 5", color=WHITE)
        
        # Scale to fit 65% of frame width with some padding
        max_width = fw * 0.60  # 60% to be safe
        if eq.width > max_width:
            eq.scale(max_width / eq.width)
        
        eq.move_to(ORIGIN)
        self.add(eq)
        
        # Show the equation width vs frame width
        width_info = Text(f"Eq width: {eq.width:.2f} / Max: {max_width:.2f}", font_size=18, color=YELLOW)
        width_info.next_to(eq, DOWN, buff=0.5)
        self.add(width_info)
        
        self.wait(3)
