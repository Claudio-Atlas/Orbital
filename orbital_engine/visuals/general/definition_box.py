"""Styled definition box with violet accent bar, term highlight, and content with proper MathTex."""
from manim import *


def build_definition_box(term, content_lines, cyan="#22D3EE", violet="#8B5CF6",
                         box_fill="#13121f", box_stroke="#252530"):
    """
    Build a definition box.

    Args:
        term: The defined term (displayed large, in cyan)
        content_lines: List of (type, text) tuples:
            ("text", "plain text")
            ("math", "x^2 + 1")
            ("text_emphasis", "important point")

    Returns (group, animate_fn)
    """
    box = RoundedRectangle(width=10, height=4.5, corner_radius=0.15,
        fill_color=box_fill, fill_opacity=0.9,
        stroke_color=box_stroke, stroke_width=1)
    box_glow = RoundedRectangle(width=10.1, height=4.6, corner_radius=0.15,
        fill_opacity=0, stroke_color=violet, stroke_width=6, stroke_opacity=0.1)

    top_bar = Line(
        box.get_corner(UL) + RIGHT*0.15,
        box.get_corner(UR) + LEFT*0.15,
        color=violet, stroke_width=3)

    def_label = Text("Definition", font_size=14, color=violet, weight=BOLD)
    def_label.move_to(box.get_top() + DOWN*0.35 + LEFT*3.5)

    term_mob = Text(term, font_size=36, color=cyan, weight=BOLD)
    term_mob.move_to(box.get_center() + UP*1.0)

    # Build content mobjects
    content_mobs = VGroup()
    for line_type, line_text in content_lines:
        if line_type == "math":
            try:
                m = MathTex(line_text, font_size=22, color=WHITE)
                content_mobs.add(m)
            except Exception:
                content_mobs.add(Text(line_text[:50], font_size=16, color=WHITE))
        elif line_type == "text_emphasis":
            content_mobs.add(Text(line_text, font_size=16, color=cyan))
        else:
            content_mobs.add(Text(line_text, font_size=16, color="#E0E0E0"))

    content_mobs.arrange(DOWN, buff=0.15, center=True)
    if content_mobs.width > 8.5:
        content_mobs.scale(8.5 / content_mobs.width)
    content_mobs.move_to(box.get_center() + DOWN*0.3)

    grp = VGroup(box_glow, box, top_bar, def_label, term_mob, content_mobs).move_to(ORIGIN)

    def animate(scene, dur):
        t = 0
        scene.play(FadeIn(box_glow), FadeIn(box), Create(top_bar),
            FadeIn(def_label), run_time=0.5); t += 0.5
        scene.play(FadeIn(term_mob, shift=UP*0.2, scale=0.9), run_time=0.4); t += 0.4
        scene.play(FadeIn(content_mobs, shift=UP*0.15), run_time=0.5); t += 0.5

        # Alive filler: glow pulse
        remaining = dur - t - 0.5
        cycles = int(remaining / 1.4)
        for _ in range(min(cycles, 5)):
            scene.play(box_glow.animate.set_stroke(opacity=0.2), run_time=0.6)
            scene.play(box_glow.animate.set_stroke(opacity=0.1), run_time=0.6)
            t += 1.2
        scene.wait(max(0.3, dur - t - 0.5))
        scene.play(FadeOut(grp), run_time=0.4)
        scene.wait(0.3)

    return grp, animate
