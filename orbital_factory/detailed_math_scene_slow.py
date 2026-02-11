"""
Orbital VideoFactory - Detailed Math Scene (SLOW VERSION - 0.75x)
Shows all intermediate steps with slower pacing
"""

from manim import *

# Orbital brand colors
ORBITAL_VIOLET = "#8B5CF6"
ORBITAL_CYAN = "#22D3EE"


class SolveLinearEquationSlow(Scene):
    """
    Solve 2x + 5 = 11 showing ALL intermediate steps.
    SLOW VERSION - 0.75x pace (animations ~1.33x longer)
    """
    
    def construct(self):
        self.camera.background_color = "#000000"
        
        # Step 1: Initial equation
        eq1 = MathTex("2x + 5", "=", "11", color=WHITE)
        eq1.scale(1.6)
        
        self.play(Write(eq1), run_time=2.7)  # Was 2
        self.wait(1.5)  # Was 1
        
        # Step 2: Show -5 on both sides
        minus5_left = MathTex("-5", color=ORBITAL_CYAN)
        minus5_right = MathTex("-5", color=ORBITAL_CYAN)
        minus5_left.scale(1.2)
        minus5_right.scale(1.2)
        minus5_left.next_to(eq1[0], DOWN, buff=0.4)
        minus5_right.next_to(eq1[2], DOWN, buff=0.4)
        
        self.play(
            Write(minus5_left),
            Write(minus5_right),
            run_time=1.3  # Was 1
        )
        self.wait(1.2)  # Was 0.8
        
        # Step 3: Transform to simplified equation
        eq2 = MathTex("2x + 5 - 5", "=", "11 - 5", color=WHITE)
        eq2.scale(1.6)
        
        self.play(
            FadeOut(minus5_left),
            FadeOut(minus5_right),
            TransformMatchingTex(eq1, eq2),
            run_time=1.6  # Was 1.2
        )
        self.wait(1.2)  # Was 0.8
        
        # Step 4: Show result of subtraction
        eq3 = MathTex("2x", "=", "6", color=WHITE)
        eq3.scale(1.6)
        
        self.play(
            TransformMatchingTex(eq2, eq3),
            run_time=1.6  # Was 1.2
        )
        self.wait(1.5)  # Was 1
        
        # Step 5: Show ÷2 on both sides
        div2_left = MathTex(r"\div 2", color=ORBITAL_CYAN)
        div2_right = MathTex(r"\div 2", color=ORBITAL_CYAN)
        div2_left.scale(1.2)
        div2_right.scale(1.2)
        div2_left.next_to(eq3[0], DOWN, buff=0.4)
        div2_right.next_to(eq3[2], DOWN, buff=0.4)
        
        self.play(
            Write(div2_left),
            Write(div2_right),
            run_time=1.3  # Was 1
        )
        self.wait(1.2)  # Was 0.8
        
        # Step 6: Show division written out
        eq4 = MathTex(r"\frac{2x}{2}", "=", r"\frac{6}{2}", color=WHITE)
        eq4.scale(1.6)
        
        self.play(
            FadeOut(div2_left),
            FadeOut(div2_right),
            TransformMatchingTex(eq3, eq4),
            run_time=1.6  # Was 1.2
        )
        self.wait(1.2)  # Was 0.8
        
        # Step 7: Final answer
        eq5 = MathTex("x", "=", "3", color=WHITE)
        eq5.scale(1.8)
        
        self.play(
            TransformMatchingTex(eq4, eq5),
            run_time=1.6  # Was 1.2
        )
        
        # Highlight the answer
        box = SurroundingRectangle(eq5, color=ORBITAL_VIOLET, buff=0.3)
        self.play(Create(box), run_time=1.1)  # Was 0.8
        
        self.wait(3)  # Was 2 - longer hold on final answer
        
        # Fade out
        self.play(
            FadeOut(eq5),
            FadeOut(box),
            run_time=0.7  # Was 0.5
        )


if __name__ == "__main__":
    print("Render with: manim -ql detailed_math_scene_slow.py SolveLinearEquationSlow")
