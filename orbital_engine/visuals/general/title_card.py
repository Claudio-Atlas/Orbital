"""Animated title card with section number, title, video type badge, and accent lines."""
from manim import *


def build_title_card(section, title, video_label, school="COASTAL ALABAMA",
                     cyan="#22D3EE", violet="#8B5CF6"):
    """
    Returns (group, animate_fn).
    animate_fn(scene) plays the intro and returns elapsed time.
    """
    sec_text = Text(f"SECTION {section}", font_size=24, color=violet, weight=BOLD)
    title_text = Text(title, font_size=48, color=cyan, weight=BOLD)
    if title_text.width > 11:
        title_text.scale(11 / title_text.width)
    title_text.next_to(sec_text, DOWN, buff=0.3)

    ll = Line(ORIGIN, LEFT*3.5, color=cyan, stroke_width=2)
    lr = Line(ORIGIN, RIGHT*3.5, color=cyan, stroke_width=2)
    ll.next_to(title_text, LEFT, buff=0.3)
    lr.next_to(title_text, RIGHT, buff=0.3)

    badge_bg = RoundedRectangle(width=3.5, height=0.65, corner_radius=0.1,
        fill_color=violet, fill_opacity=0.85, stroke_width=0)
    badge_text = Text(video_label, font_size=20, color=WHITE, weight=BOLD)
    badge = VGroup(badge_bg, badge_text)
    badge.next_to(title_text, DOWN, buff=0.5)

    school_text = Text(school, font_size=12, color="#555555", weight=BOLD)
    school_text.next_to(badge, DOWN, buff=0.5)

    grp = VGroup(sec_text, title_text, ll, lr, badge, school_text).move_to(ORIGIN)

    def animate(scene, dur):
        t = 0
        scene.play(FadeIn(sec_text, shift=UP*0.3), run_time=0.4); t += 0.4
        scene.play(
            FadeIn(title_text, shift=UP*0.2, scale=0.9),
            Create(ll), Create(lr), run_time=0.5); t += 0.5
        scene.play(FadeIn(badge, shift=UP*0.2), FadeIn(school_text), run_time=0.3); t += 0.3
        scene.wait(max(0.3, dur - t - 0.5))
        scene.play(FadeOut(grp, shift=UP*0.3), run_time=0.4)
        scene.wait(0.3)

    return grp, animate
