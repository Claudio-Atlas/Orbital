"""Learning objectives list with bullet-by-bullet reveal and glow dots."""
from manim import *


def build_objectives(objectives, cyan="#22D3EE", violet="#8B5CF6"):
    """
    Args:
        objectives: List of objective strings

    Returns (group, animate_fn)
    """
    header = Text("🎯  Learning Objectives", font_size=30, color=violet, weight=BOLD)
    header.move_to(UP*2.8)

    divider = Line(LEFT*4, RIGHT*4, color=violet, stroke_width=1.5, stroke_opacity=0.5)
    divider.next_to(header, DOWN, buff=0.2)

    obj_mobs = VGroup()
    for i, obj_text in enumerate(objectives):
        dot = Dot(color=cyan, radius=0.06).set_glow_factor(1.5)
        display = obj_text if len(obj_text) <= 65 else obj_text[:62] + "..."
        text = Text(display, font_size=17, color=WHITE)
        row = VGroup(dot, text).arrange(RIGHT, buff=0.2)
        row.move_to(UP*(1.5 - i*0.8))
        row.align_to(LEFT*5, LEFT)
        obj_mobs.add(row)

    grp = VGroup(header, divider, obj_mobs)

    def animate(scene, dur):
        t = 0
        scene.play(FadeIn(header, shift=DOWN*0.2), Create(divider), run_time=0.4); t += 0.4

        per_obj = max(0.8, (dur - 1.5) / max(1, len(objectives)))

        for row in obj_mobs:
            dot, text = row[0], row[1]
            scene.play(FadeIn(dot, scale=2), FadeIn(text, shift=RIGHT*0.3), run_time=0.4)
            t += 0.4
            scene.wait(max(0.1, per_obj - 0.4)); t += per_obj - 0.4

        scene.wait(max(0.3, dur - t - 0.5))
        scene.play(FadeOut(grp), run_time=0.4)
        scene.wait(0.3)

    return grp, animate
