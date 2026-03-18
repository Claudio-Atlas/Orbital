"""Animated mapping diagram — two oval sets with arrows showing input→output relationships."""
from manim import *


def build_mapping_diagram(domain_label, range_label, mappings,
                          is_function=True, title="",
                          cyan="#22D3EE", violet="#8B5CF6",
                          green="#39FF14", crimson="#FF4444"):
    """
    Animated set-mapping diagram.

    Args:
        domain_label: Label for domain set (e.g., "A" or "People")
        range_label: Label for range set (e.g., "B" or "Numbers")
        mappings: List of (input, [output1, output2, ...]) tuples
            e.g., [("x", ["y"]), ("3", ["1", "2"])]  # second is NOT a function
        is_function: If True, show green check; if False, show red X
        title: Optional title text above

    Returns (group, animate_fn)
    """
    # Oval sets
    domain_oval = Ellipse(width=2.8, height=4.0, color=cyan,
        fill_color=cyan, fill_opacity=0.05, stroke_width=2)
    range_oval = Ellipse(width=2.8, height=4.0, color=violet,
        fill_color=violet, fill_opacity=0.05, stroke_width=2)

    domain_oval.move_to(LEFT*3)
    range_oval.move_to(RIGHT*3)

    # Set labels
    d_label = Text(domain_label, font_size=20, color=cyan, weight=BOLD)
    d_label.next_to(domain_oval, UP, buff=0.2)
    r_label = Text(range_label, font_size=20, color=violet, weight=BOLD)
    r_label.next_to(range_oval, UP, buff=0.2)

    # Build elements
    domain_dots = VGroup()
    range_dots = VGroup()
    arrows = VGroup()
    domain_labels = VGroup()
    range_labels = VGroup()

    # Collect all unique range values
    all_range_vals = []
    for _, outputs in mappings:
        for o in outputs:
            if o not in all_range_vals:
                all_range_vals.append(o)

    # Position domain elements
    n_domain = len(mappings)
    for i, (inp, _) in enumerate(mappings):
        y = 1.2 - i * (2.4 / max(1, n_domain - 1)) if n_domain > 1 else 0
        pos = LEFT*3 + UP*y
        dot = Dot(pos, color=cyan, radius=0.08)
        label = Text(str(inp), font_size=14, color=WHITE)
        label.next_to(dot, LEFT, buff=0.15)
        domain_dots.add(dot)
        domain_labels.add(label)

    # Position range elements
    n_range = len(all_range_vals)
    range_positions = {}
    for i, val in enumerate(all_range_vals):
        y = 1.2 - i * (2.4 / max(1, n_range - 1)) if n_range > 1 else 0
        pos = RIGHT*3 + UP*y
        dot = Dot(pos, color=violet, radius=0.08)
        label = Text(str(val), font_size=14, color=WHITE)
        label.next_to(dot, RIGHT, buff=0.15)
        range_dots.add(dot)
        range_labels.add(label)
        range_positions[val] = pos

    # Build arrows
    for i, (inp, outputs) in enumerate(mappings):
        start = domain_dots[i].get_center()
        for out_val in outputs:
            if out_val in range_positions:
                end = range_positions[out_val]
                color = cyan if len(outputs) == 1 else crimson
                arrow = Arrow(start, end, buff=0.15, color=color,
                    stroke_width=2, max_tip_length_to_length_ratio=0.15)
                arrows.add(arrow)

    # Result indicator
    if is_function:
        indicator = Text("✓ Function", font_size=22, color=green, weight=BOLD)
    else:
        indicator = Text("✗ Not a Function", font_size=22, color=crimson, weight=BOLD)
    indicator.move_to(DOWN*2.8)

    # Optional title
    title_mob = None
    if title:
        title_mob = Text(title, font_size=18, color="#888888")
        title_mob.move_to(UP*3.2)

    grp = VGroup(domain_oval, range_oval, d_label, r_label,
        domain_dots, range_dots, domain_labels, range_labels,
        arrows, indicator)
    if title_mob:
        grp.add(title_mob)

    def animate(scene, dur):
        t = 0

        if title_mob:
            scene.play(FadeIn(title_mob), run_time=0.2); t += 0.2

        # Ovals appear
        scene.play(
            Create(domain_oval), Create(range_oval),
            FadeIn(d_label), FadeIn(r_label),
            run_time=0.5); t += 0.5

        # Domain elements appear
        scene.play(
            *[FadeIn(d, scale=2) for d in domain_dots],
            *[FadeIn(l) for l in domain_labels],
            run_time=0.4); t += 0.4

        # Range elements appear
        scene.play(
            *[FadeIn(d, scale=2) for d in range_dots],
            *[FadeIn(l) for l in range_labels],
            run_time=0.4); t += 0.4

        # Arrows appear one by one
        per_arrow = max(0.3, (dur - t - 2.0) / max(1, len(arrows)))
        for arrow in arrows:
            scene.play(Create(arrow), run_time=min(0.4, per_arrow))
            t += min(0.4, per_arrow)
            if per_arrow > 0.5:
                scene.wait(per_arrow - 0.4)
                t += per_arrow - 0.4

        # Show result
        scene.play(FadeIn(indicator, scale=1.3), run_time=0.4); t += 0.4

        # Hold
        scene.wait(max(0.5, dur - t - 0.5))
        scene.play(FadeOut(grp), run_time=0.4)
        scene.wait(0.3)

    return grp, animate
