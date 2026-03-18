"""Function machine animation — input goes in, rule applies, output comes out."""
from manim import *


def build_function_machine(func_name="f", rule_display="x^2 + 1",
                           examples=None,
                           cyan="#22D3EE", violet="#8B5CF6", gold="#D6BC82"):
    """
    Visual function machine: input → [box with rule] → output.

    Args:
        func_name: "f", "g", etc.
        rule_display: LaTeX for the rule shown inside the box
        examples: List of (input_val, output_val) to animate through
            e.g., [(3, 10), (-2, 5), (0, 1)]
    """
    if examples is None:
        examples = [(3, 10), (-2, 5), (0, 1)]

    def animate(scene, dur):
        t = 0

        # Machine box
        machine = RoundedRectangle(width=4, height=2.5, corner_radius=0.2,
            fill_color="#1a1130", fill_opacity=0.9,
            stroke_color=violet, stroke_width=2)

        # Rule inside
        rule_label = Text(f"{func_name}(x) =", font_size=18, color="#888888")
        try:
            rule_math = MathTex(rule_display, font_size=28, color=WHITE)
        except Exception:
            rule_math = Text(rule_display, font_size=22, color=WHITE)
        rule = VGroup(rule_label, rule_math).arrange(RIGHT, buff=0.2)
        rule.move_to(machine.get_center())

        # Input arrow (left)
        in_arrow = Arrow(LEFT*5, machine.get_left() + LEFT*0.1,
            color=cyan, stroke_width=3, buff=0)
        in_label = Text("Input", font_size=14, color=cyan)
        in_label.next_to(in_arrow, UP, buff=0.1)

        # Output arrow (right)
        out_arrow = Arrow(machine.get_right() + RIGHT*0.1, RIGHT*5,
            color=gold, stroke_width=3, buff=0)
        out_label = Text("Output", font_size=14, color=gold)
        out_label.next_to(out_arrow, UP, buff=0.1)

        # Machine label
        machine_label = Text(f"Function {func_name}", font_size=14,
            color=violet, weight=BOLD)
        machine_label.next_to(machine, UP, buff=0.15)

        scene.play(
            FadeIn(machine), FadeIn(rule), FadeIn(machine_label),
            Create(in_arrow), Create(out_arrow),
            FadeIn(in_label), FadeIn(out_label),
            run_time=0.6); t += 0.6

        # Animate examples
        per_ex = max(1.5, (dur - 2.0) / max(1, len(examples)))

        for inp, outp in examples:
            # Input value flies in
            inp_mob = MathTex(str(inp), font_size=30, color=cyan)
            inp_mob.move_to(LEFT*6)

            outp_mob = MathTex(str(outp), font_size=30, color=gold)
            outp_mob.move_to(machine.get_center())

            # Fly input in
            scene.play(inp_mob.animate.move_to(machine.get_left() + RIGHT*0.5),
                run_time=0.4); t += 0.4

            # Flash machine
            scene.play(
                machine.animate.set_stroke(color=cyan, width=3),
                FadeOut(inp_mob),
                run_time=0.2); t += 0.2

            scene.play(
                machine.animate.set_stroke(color=violet, width=2),
                run_time=0.1); t += 0.1

            # Output flies out
            scene.play(outp_mob.animate.move_to(RIGHT*5.5),
                run_time=0.4); t += 0.4

            # Show notation below
            notation = MathTex(f"{func_name}({inp}) = {outp}",
                font_size=22, color=WHITE)
            notation.move_to(DOWN*2.2)
            scene.play(FadeIn(notation, shift=UP*0.15), run_time=0.2); t += 0.2

            hold = max(0.2, per_ex - 1.3)
            scene.wait(hold); t += hold

            scene.play(FadeOut(outp_mob), FadeOut(notation), run_time=0.2); t += 0.2

        scene.wait(max(0.3, dur - t - 0.5))
        scene.play(FadeOut(VGroup(machine, rule, machine_label,
            in_arrow, out_arrow, in_label, out_label)), run_time=0.4)
        scene.wait(0.3)

    return None, animate
