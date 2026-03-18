"""Step-by-step equation building with color-highlighted substitution and transforms."""
from manim import *


def build_equation_steps(steps, title="", cyan="#22D3EE", gold="#D6BC82",
                         green="#39FF14"):
    """
    Animate equations appearing line by line, with optional transforms.

    Args:
        steps: List of dicts:
            {"latex": "x^2 + 1 = 0", "note": "Given equation"}
            {"latex": "x^2 = -1", "note": "Subtract 1", "highlight": [0,3]}
            {"transform_from": 0}  # Transform from step index 0
        title: Optional header text

    Returns (group, animate_fn)
    """
    def animate(scene, dur):
        t = 0
        all_mobs = VGroup()

        # Title
        if title:
            header_bg = RoundedRectangle(width=11, height=0.7, corner_radius=0.1,
                fill_color=gold, fill_opacity=0.12,
                stroke_color=gold, stroke_width=1.5)
            header_text = Text(title, font_size=22, color=gold, weight=BOLD)
            header = VGroup(header_bg, header_text).move_to(UP*3.2)
            scene.play(FadeIn(header, shift=DOWN*0.2), run_time=0.3); t += 0.3
            all_mobs.add(header)

        per_step = max(0.8, (dur - 1.5) / max(1, len(steps)))
        eq_mobs = []

        for i, step in enumerate(steps):
            latex = step.get("latex", "")
            note = step.get("note", "")
            y_pos = 2.0 - i * 1.0

            if not latex:
                continue

            try:
                eq = MathTex(latex, font_size=32, color=WHITE)
            except Exception:
                eq = Text(latex[:50], font_size=20, color=WHITE)

            eq.move_to([0, y_pos, 0])

            # Note to the right
            note_mob = None
            if note:
                note_mob = Text(note, font_size=14, color=cyan)
                note_mob.next_to(eq, RIGHT, buff=0.5)

            # Check if this is a transform
            transform_from = step.get("transform_from", None)
            if transform_from is not None and transform_from < len(eq_mobs):
                source = eq_mobs[transform_from]
                scene.play(TransformMatchingTex(source.copy(), eq), run_time=0.6)
                t += 0.6
            else:
                scene.play(FadeIn(eq, shift=UP*0.15), run_time=0.4)
                t += 0.4

            if note_mob:
                scene.play(FadeIn(note_mob, shift=LEFT*0.2), run_time=0.2)
                t += 0.2
                all_mobs.add(note_mob)

            eq_mobs.append(eq)
            all_mobs.add(eq)
            scene.wait(max(0.2, per_step - 0.6)); t += per_step - 0.6

        # Highlight the final result
        if eq_mobs:
            final = eq_mobs[-1]
            box = SurroundingRectangle(final, color=green, buff=0.15,
                corner_radius=0.08, stroke_width=2)
            scene.play(Create(box), run_time=0.3); t += 0.3
            all_mobs.add(box)

        scene.wait(max(0.3, dur - t - 0.5))
        scene.play(FadeOut(all_mobs), run_time=0.4)
        scene.wait(0.3)

    return None, animate
