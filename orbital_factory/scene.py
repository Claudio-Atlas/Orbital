"""
Orbital VideoFactory - Manim Scene Generator
Renders math steps with write-on animation
"""

from manim import *
import json
import os

class MathStepScene(Scene):
    """
    Renders a single math step with write-on animation.
    Designed to be called per-step, then composited with audio.
    """
    
    def __init__(self, latex_content: str, **kwargs):
        self.latex_content = latex_content
        super().__init__(**kwargs)
    
    def construct(self):
        # Set background to black (Orbital brand)
        self.camera.background_color = BLACK
        
        # Create the math text
        math = MathTex(self.latex_content, color=WHITE)
        math.scale(1.5)
        
        # Write-on animation
        self.play(Write(math), run_time=2)
        self.wait(0.5)


class FullProblemScene(Scene):
    """
    Renders a full problem from JSON script.
    Each step writes on, waits, then transitions to next.
    """
    
    def __init__(self, script_path: str = None, **kwargs):
        self.script_path = script_path
        super().__init__(**kwargs)
    
    def construct(self):
        self.camera.background_color = BLACK
        
        # Load script if provided
        if self.script_path and os.path.exists(self.script_path):
            with open(self.script_path) as f:
                script = json.load(f)
            steps = script.get("steps", [])
        else:
            # Default test steps
            steps = [
                {"latex": "2x + 5 = 11"},
                {"latex": "2x = 6"},
                {"latex": "x = 3"}
            ]
        
        previous_math = None
        
        for i, step in enumerate(steps):
            latex = step.get("latex", "")
            
            # Create math object
            math = MathTex(latex, color=WHITE)
            math.scale(1.5)
            
            if previous_math is None:
                # First step: write on
                self.play(Write(math), run_time=2)
            else:
                # Subsequent steps: transform from previous
                self.play(
                    ReplacementTransform(previous_math, math),
                    run_time=1.5
                )
            
            # Hold for reading
            self.wait(1)
            
            previous_math = math
        
        # Final hold
        self.wait(2)


class OrbitalMathScene(Scene):
    """
    Production-ready Orbital-branded math scene.
    Black background, white math, subtle glow effect.
    """
    
    def __init__(self, steps: list = None, **kwargs):
        self.steps = steps or []
        super().__init__(**kwargs)
    
    def construct(self):
        self.camera.background_color = "#000000"
        
        if not self.steps:
            # Demo mode
            self.steps = [
                {"narration": "Let's solve 2x + 5 = 11", "latex": "2x + 5 = 11"},
                {"narration": "Subtract 5 from both sides", "latex": "2x = 6"},
                {"narration": "Divide by 2", "latex": "x = 3"},
            ]
        
        previous = None
        
        for step in self.steps:
            latex = step.get("latex", "")
            
            # Main math text
            math = MathTex(latex, color=WHITE)
            math.scale(1.8)
            
            # Optional: subtle glow (Orbital brand)
            # glow = math.copy()
            # glow.set_color("#8B5CF6")
            # glow.set_opacity(0.3)
            
            if previous is None:
                self.play(Write(math), run_time=2.5)
            else:
                self.play(
                    FadeOut(previous, shift=UP * 0.5),
                    run_time=0.5
                )
                self.play(Write(math), run_time=2)
            
            self.wait(1.5)
            previous = math
        
        self.wait(2)
        self.play(FadeOut(previous))


# CLI entry point for testing
if __name__ == "__main__":
    import sys
    
    # Quick test render
    print("Rendering test scene...")
    print("Run with: manim -pql scene.py FullProblemScene")
