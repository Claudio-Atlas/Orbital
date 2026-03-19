"""
Orbital Visual Standards — LOCKED
===================================
Reusable primitives that implement the Production Bible.
Every video uses these. No exceptions.

TEXT HIERARCHY: 7 tiers with specific sizes, colors, methods
ALIVE STANDARD: glow, bloom, sparks, dim, easing
GRAPH STANDARD: nearly invisible axes, neon grid, tracer dots
BOXING: purple boxes for key results

Import this everywhere:
    from visuals.standards import *
"""
import numpy as np
from manim import *

# ── Colors (re-export for convenience) ──
ORBITAL_CYAN = "#22D3EE"
END_CYAN     = "#00E5FF"
NEON_GREEN   = "#39FF14"
GOLD         = "#D6BC82"
CRIMSON      = "#8C2232"
VIOLET       = "#8B5CF6"
BOX_FILL     = "#1a1130"
BOX_STROKE   = "#252530"
AXIOM_TEXT   = "#E0E0E0"


# ═══════════════════════════════════════════════════════
# TEXT HIERARCHY — The 7 Tiers (Production Bible LOCKED)
# ═══════════════════════════════════════════════════════

def tier1_punchline(tex, **kwargs):
    """Tier 1: Final answer, big reveal. GREEN MathTex in purple box."""
    mob = MathTex(tex, font_size=42, color=NEON_GREEN, **kwargs)
    return _purple_box(mob)

def tier2_key_fact(tex, **kwargs):
    """Tier 2: Definitions, theorems. CYAN MathTex in purple box."""
    mob = MathTex(tex, font_size=28, color=ORBITAL_CYAN, **kwargs)
    return _purple_box(mob)

def tier3_callout(text, color=WHITE, **kwargs):
    """Tier 3: Takeaway statements. WHITE Text, BOLD."""
    return Text(text, font_size=24, color=color, weight=BOLD, **kwargs)

def tier4_title(text, **kwargs):
    """Tier 4: Section headers. VIOLET Text, BOLD."""
    return Text(text, font_size=26, color=VIOLET, weight=BOLD, **kwargs)

def tier5_equation(tex, **kwargs):
    """Tier 5: Long math expressions. WHITE MathTex."""
    return MathTex(tex, font_size=30, color=WHITE, **kwargs)

def tier6_caption(tex, **kwargs):
    """Tier 6: Labels, annotations. CYAN MathTex."""
    return MathTex(tex, font_size=24, color=ORBITAL_CYAN, **kwargs)

def tier7_counter(tex, **kwargs):
    """Tier 7: Counters. WHITE MathTex. Use rarely."""
    return MathTex(tex, font_size=22, color=WHITE, **kwargs)

def _purple_box(mob, buff=0.12):
    """Wrap a mobject in a purple box (Bible standard for tier 1 & 2)."""
    box = SurroundingRectangle(mob,
        color=VIOLET, fill_color=BOX_FILL, fill_opacity=0.8,
        buff=buff, corner_radius=0.08, stroke_width=1.5)
    return VGroup(box, mob)

def auto_box(tex, font_size=28, color=ORBITAL_CYAN):
    """Short expression auto-boxing: < 4 chars → always boxed."""
    mob = MathTex(tex, font_size=font_size, color=color)
    if len(tex.replace(" ", "").replace("\\", "")) < 4:
        return _purple_box(mob)
    return mob


# ═══════════════════════════════════════════════════════
# ALIVE STANDARD — Glow, Bloom, Sparks, Dim
# ═══════════════════════════════════════════════════════

def make_glow(mob, color=VIOLET, stroke_w=6, opacity=0.15):
    """Create a glow copy behind a mobject. Place it BEHIND the mob with scene.add()."""
    g = mob.copy()
    g.set_stroke(color=color, width=stroke_w, opacity=opacity)
    g.set_fill(opacity=0)
    return g


def bloom(scene, mob, color=NEON_GREEN, num_lines=8, radius=0.5):
    """Bloom effect on a key reveal — Flash + glow pulse."""
    scene.play(
        Flash(mob.get_center(), color=color, num_lines=num_lines,
            flash_radius=radius, line_length=0.15),
        run_time=0.2)


def sparks(scene, point, color=NEON_GREEN, count=12):
    """Sparks effect — tiny dots burst outward."""
    dots = VGroup(*[
        Dot(point, color=color, radius=0.03).set_opacity(0.6)
        for _ in range(count)
    ])
    targets = [
        point + np.array([
            np.cos(i * TAU/count) * 0.5,
            np.sin(i * TAU/count) * 0.5, 0
        ]) for i in range(count)
    ]
    scene.play(
        *[d.animate.move_to(t).set_opacity(0) for d, t in zip(dots, targets)],
        run_time=0.3, rate_func=rush_from)
    scene.remove(*dots)


def alive_hold(scene, mob, glow_mob, duration, style="glow_pulse"):
    """
    Keep a scene alive during a hold. Never just self.wait() for > 2s.
    
    Styles:
        glow_pulse: Glow breathes (best for boxed content)
        drift: Subtle position shift (best for standalone equations)
        breathe: Opacity oscillation (best for background elements)
    """
    if duration < 0.5:
        scene.wait(max(0.1, duration))
        return

    t = 0
    if style == "glow_pulse" and glow_mob is not None:
        cycles = min(int(duration / 1.0), 6)
        for _ in range(cycles):
            scene.play(glow_mob.animate.set_stroke(opacity=0.25),
                run_time=0.3, rate_func=smooth)
            scene.play(glow_mob.animate.set_stroke(opacity=0.15),
                run_time=0.7, rate_func=smooth)
            t += 1.0
    elif style == "drift" and mob is not None:
        scene.play(mob.animate.shift(UP * 0.05),
            run_time=duration * 0.5, rate_func=there_and_back)
        t += duration * 0.5
    elif style == "breathe" and mob is not None:
        scene.play(mob.animate.set_opacity(0.6),
            run_time=duration * 0.4, rate_func=smooth)
        scene.play(mob.animate.set_opacity(1.0),
            run_time=duration * 0.4, rate_func=smooth)
        t += duration * 0.8

    leftover = max(0.1, duration - t)
    scene.wait(leftover)


# ═══════════════════════════════════════════════════════
# GRAPH STANDARD — Nearly invisible axes, neon grid, tracer
# ═══════════════════════════════════════════════════════

def orbital_axes(x_range, y_range, x_length=10, y_length=5, center=ORIGIN):
    """
    Standard Orbital axes — #333, stroke 1, nearly invisible.
    The curve is the star, not the axes.
    """
    ax = Axes(
        x_range=x_range, y_range=y_range,
        x_length=x_length, y_length=y_length,
        axis_config={
            "color": "#333333",
            "stroke_width": 1,
            "include_numbers": True,
            "font_size": 12,
            "numbers_to_exclude": [0],
        },
        tips=False,
    )
    ax.move_to(center)
    return ax


def neon_grid(center, half_w, half_h, spacing=0.6):
    """
    Custom neon grid — violet lines, 0.3px, 0.2 opacity.
    Matches the welcome videos exactly.
    """
    cx, cy = center[0], center[1]
    g = VGroup()
    for dx in np.arange(-half_w, half_w + 0.01, spacing):
        g.add(Line([cx+dx, cy-half_h, 0], [cx+dx, cy+half_h, 0],
            color=VIOLET, stroke_width=0.3, stroke_opacity=0.2))
    for dy in np.arange(-half_h, half_h + 0.01, spacing):
        g.add(Line([cx-half_w, cy+dy, 0], [cx+half_w, cy+dy, 0],
            color=VIOLET, stroke_width=0.3, stroke_opacity=0.2))
    return g


def trace_curve(scene, curve, run_time=1.0):
    """
    Draw a curve with a glowing tracer dot leading it.
    Returns the tracer (caller should clean up or keep).
    """
    tracer = Dot(color=NEON_GREEN, radius=0.08).set_glow_factor(2.0)
    tracer.move_to(curve.get_start())
    scene.play(
        MoveAlongPath(tracer, curve),
        Create(curve),
        run_time=run_time, rate_func=smooth,
    )
    # Pulse at end
    scene.play(tracer.animate.scale(1.5), run_time=0.12)
    scene.play(tracer.animate.scale(1/1.5), run_time=0.12)
    return tracer


def orbital_graph(scene, ax, fn, x_range, color=ORBITAL_CYAN,
                  stroke_width=3, trace=True, trace_time=1.0):
    """
    Plot a function on Orbital axes with optional tracer.
    Returns (curve, tracer_or_None).
    """
    curve = ax.plot(fn, x_range=x_range, color=color, stroke_width=stroke_width)
    if trace:
        tracer = trace_curve(scene, curve, run_time=trace_time)
        return curve, tracer
    else:
        scene.play(Create(curve), run_time=trace_time)
        return curve, None


# ═══════════════════════════════════════════════════════
# DEFINITION BOX — Bible-compliant styled box
# ═══════════════════════════════════════════════════════

def definition_box(term, equation_tex, key_phrase_parts, width=5.5, height=4.0):
    """
    Build a Bible-compliant definition box.
    
    Args:
        term: The defined term (e.g., "Function")
        equation_tex: LaTeX equation (e.g., r"f : A \\to B")
        key_phrase_parts: List of (text, color) tuples for the key phrase
            e.g., [("each input", CYAN), ("→", WHITE), ("exactly one output", GOLD)]
    
    Returns: (box_group, glow)
    """
    box = RoundedRectangle(width=width, height=height, corner_radius=0.15,
        fill_color=BOX_FILL, fill_opacity=0.85,
        stroke_color=BOX_STROKE, stroke_width=1)
    top_bar = Line(
        box.get_corner(UL) + RIGHT*0.15,
        box.get_corner(UR) + LEFT*0.15,
        color=VIOLET, stroke_width=3)

    # "DEFINITION" label — tier 4 style
    label = Text("DEFINITION", font_size=12, color=VIOLET, weight=BOLD)
    label.move_to(box.get_top() + DOWN*0.3 + LEFT*(width/2 - 1.0))

    # Term — tier 2 style (cyan, bold)
    term_mob = Text(term, font_size=28, color=ORBITAL_CYAN, weight=BOLD)
    term_mob.move_to(box.get_center() + UP*1.0)

    # Equation — tier 5
    eq = MathTex(equation_tex, font_size=30, color=WHITE)
    eq.move_to(box.get_center() + UP*0.2)

    # Key phrase — colored parts
    key_parts = VGroup()
    for txt, col in key_phrase_parts:
        if txt.startswith("\\") or txt in ["\\to", "→"]:
            key_parts.add(MathTex(txt, font_size=22, color=col))
        else:
            key_parts.add(Text(txt, font_size=18, color=col, weight=BOLD))
    key_parts.arrange(RIGHT, buff=0.1)
    key_parts.move_to(box.get_center() + DOWN*0.6)

    grp = VGroup(box, top_bar, label, term_mob, eq, key_parts)

    # Glow
    glow = RoundedRectangle(width=width+0.1, height=height+0.1, corner_radius=0.15,
        fill_opacity=0, stroke_color=VIOLET, stroke_width=6, stroke_opacity=0.15)
    glow.move_to(box.get_center())

    return grp, glow


# ═══════════════════════════════════════════════════════
# FUNCTION MACHINE — Animated I/O box
# ═══════════════════════════════════════════════════════

def _build_gear(center, radius, n_teeth, color, tooth_len=0.14, sw=2.0):
    """Build a single gear with teeth (polygon-based, from gen1)."""
    parts = []
    circ = Circle(radius=radius, color=color, stroke_width=sw,
                  fill_color=BOX_FILL, fill_opacity=0.4).move_to(center)
    parts.append(circ)
    parts.append(Dot(radius=0.05, color=color, fill_opacity=0.8).move_to(center))
    for i in range(n_teeth):
        a = i * TAU / n_teeth
        c_arr = np.array(center)
        ip = c_arr + radius * np.array([np.cos(a), np.sin(a), 0])
        op = c_arr + (radius + tooth_len) * np.array([np.cos(a), np.sin(a), 0])
        perp = np.array([-np.sin(a), np.cos(a), 0])
        tw = 0.07
        tooth = Polygon(
            ip + perp*tw, ip - perp*tw,
            op - perp*tw*0.7, op + perp*tw*0.7,
            color=color, stroke_width=sw-0.5,
            fill_color=color, fill_opacity=0.25)
        parts.append(tooth)
    return VGroup(*parts)


def function_machine(fn_name="f", rule_tex="x^2 + 1", safe_x=6.5):
    """
    Build a function machine WITH interlocking gears.
    Returns (machine_group, glow, machine_rect, in_arrow, out_arrow, gear1, gear2).
    Caller animates examples separately using animate_machine_example().
    """
    machine = RoundedRectangle(width=5.0, height=2.8, corner_radius=0.2,
        fill_color=BOX_FILL, fill_opacity=0.9,
        stroke_color=VIOLET, stroke_width=2)
    glow = make_glow(machine, VIOLET, 8, 0.15)

    rule = MathTex(f"{fn_name}(x) = {rule_tex}",
        font_size=28, color=WHITE)
    rule.move_to(machine.get_center() + DOWN * 0.3)

    label = Text("FUNCTION", font_size=14, color=VIOLET, weight=BOLD)
    label.next_to(machine, UP, buff=0.12)

    # ── Interlocking gears inside the machine ──
    mc = machine.get_center()
    g1_center = [mc[0] - 0.55, mc[1] + 0.5, 0]
    g2_center = [mc[0] + 0.65, mc[1] + 0.5, 0]
    gear1 = _build_gear(g1_center, 0.55, 10, VIOLET, tooth_len=0.12, sw=1.8)
    gear2 = _build_gear(g2_center, 0.4, 7, ORBITAL_CYAN, tooth_len=0.10, sw=1.8)

    in_arrow = Arrow(LEFT*safe_x, machine.get_left() + LEFT*0.1,
        color=ORBITAL_CYAN, stroke_width=2.5, buff=0,
        max_tip_length_to_length_ratio=0.04)
    out_arrow = Arrow(machine.get_right() + RIGHT*0.1, RIGHT*safe_x,
        color=GOLD, stroke_width=2.5, buff=0,
        max_tip_length_to_length_ratio=0.04)

    in_lbl = tier6_caption(r"\text{input}")
    in_lbl.next_to(in_arrow, UP, buff=0.08)
    out_lbl = MathTex(r"\text{output}", font_size=24, color=GOLD)
    out_lbl.next_to(out_arrow, UP, buff=0.08)

    grp = VGroup(machine, rule, label, gear1, gear2, in_arrow, in_lbl, out_arrow, out_lbl)
    return grp, glow, machine, in_arrow, out_arrow, gear1, gear2


def spin_gears(scene, gear1, gear2, duration=0.6, revolutions=0.5):
    """Spin interlocking gears (opposite directions) inside the function machine."""
    g1c = gear1[0].get_center()
    g2c = gear2[0].get_center()
    scene.play(
        Rotate(gear1, angle=revolutions * TAU, about_point=g1c),
        Rotate(gear2, angle=-revolutions * TAU * 0.7, about_point=g2c),
        run_time=duration, rate_func=smooth)


def animate_machine_example(scene, machine, in_arrow, out_arrow,
                            inp_val, out_val, fn_name="f", t=0,
                            gear1=None, gear2=None):
    """
    Animate one input→output through the function machine.
    Returns (notation_mob, time_elapsed).
    
    Features:
    - Glowing input dot with value label
    - Dot travels along arrow with rush_into easing
    - Machine border FLASHES cyan on contact
    - GEARS SPIN while processing (if gear1/gear2 provided)
    - Glowing output dot emerges with rush_from easing
    - Output dot PULSES at end
    - Notation fades in below
    """
    # Glowing input dot + value
    inp_dot = Dot(color=ORBITAL_CYAN, radius=0.1).set_glow_factor(2.0)
    inp_mob = MathTex(str(inp_val), font_size=24, color=ORBITAL_CYAN)
    inp_dot.move_to(in_arrow.get_start())
    inp_mob.next_to(inp_dot, UP, buff=0.08)

    scene.play(FadeIn(inp_dot, scale=2), FadeIn(inp_mob), run_time=0.2); t += 0.2

    # Travel along arrow into machine
    scene.play(
        inp_dot.animate.move_to(machine.get_left() + RIGHT*0.3),
        inp_mob.animate.move_to(machine.get_left() + RIGHT*0.3 + UP*0.4),
        run_time=0.6, rate_func=rush_into); t += 0.6

    # Machine FLASHES + GEARS SPIN
    flash_anims = [
        machine.animate.set_stroke(color=ORBITAL_CYAN, width=4),
        FadeOut(inp_dot), FadeOut(inp_mob),
    ]
    scene.play(*flash_anims, run_time=0.15); t += 0.15

    # Gears spin while "processing"
    if gear1 is not None and gear2 is not None:
        g1c = gear1[0].get_center()
        g2c = gear2[0].get_center()
        scene.play(
            Rotate(gear1, angle=0.5 * TAU, about_point=g1c),
            Rotate(gear2, angle=-0.35 * TAU, about_point=g2c),
            machine.animate.set_stroke(color=VIOLET, width=2),
            run_time=0.5, rate_func=smooth); t += 0.5
    else:
        scene.play(
            machine.animate.set_stroke(color=VIOLET, width=2),
            run_time=0.15); t += 0.15

    # Output dot emerges
    out_dot = Dot(color=GOLD, radius=0.1).set_glow_factor(2.0)
    out_mob = MathTex(str(out_val), font_size=24, color=GOLD)
    out_dot.move_to(machine.get_right() + LEFT*0.3)
    out_mob.next_to(out_dot, UP, buff=0.08)

    scene.play(FadeIn(out_dot, scale=2), FadeIn(out_mob), run_time=0.15); t += 0.15

    # Travel out with rush_from
    scene.play(
        out_dot.animate.move_to(out_arrow.get_end()),
        out_mob.animate.move_to(out_arrow.get_end() + UP*0.4),
        run_time=0.5, rate_func=rush_from); t += 0.5

    # Pulse at end
    scene.play(out_dot.animate.scale(1.5), run_time=0.1)
    scene.play(out_dot.animate.scale(1/1.5), run_time=0.1); t += 0.2

    # Notation with bloom
    notation = tier2_key_fact(f"{fn_name}({inp_val}) = {out_val}")
    scene.play(FadeIn(notation, shift=UP*0.1),
        FadeOut(out_dot), FadeOut(out_mob), run_time=0.2)
    bloom(scene, notation, color=ORBITAL_CYAN, radius=0.4)
    t += 0.4

    return notation, t


# ═══════════════════════════════════════════════════════
# MAPPING DIAGRAM — Animated set diagram
# ═══════════════════════════════════════════════════════

def set_to_mapping_diagram(scene, domain_elements, range_elements,
                           mappings, t=0, center=ORIGIN,
                           oval_w=2.5, oval_h=3.5, gap=3.5):
    """
    Animate set notation → mapping diagram transformation.
    
    Shows A = {1, 2, 3} as text, then morphs elements into an oval diagram.
    
    Args:
        scene: Manim scene
        domain_elements: List of domain values (e.g., [1, 2, 3])
        range_elements: List of range values (e.g., ["a", "b"])
        mappings: List of (domain_idx, range_idx) pairs for arrows
        t: current time
        center: center position
        oval_w, oval_h: oval dimensions
        gap: horizontal gap between ovals
    
    Returns: (diagram_group, arrows, t)
    """
    # Phase 1: Show set notation
    d_str = ", ".join(str(e) for e in domain_elements)
    r_str = ", ".join(str(e) for e in range_elements)
    set_a = MathTex(r"A = \{" + d_str + r"\}", font_size=28, color=ORBITAL_CYAN)
    set_b = MathTex(r"B = \{" + r_str + r"\}", font_size=28, color=VIOLET)
    sets = VGroup(set_a, set_b).arrange(RIGHT, buff=1.5)
    sets.move_to(center + UP * 1.5)

    scene.play(FadeIn(set_a, shift=RIGHT * 0.3), run_time=0.3); t += 0.3
    scene.play(FadeIn(set_b, shift=LEFT * 0.3), run_time=0.3); t += 0.3
    scene.wait(0.5); t += 0.5

    # Phase 2: Build oval diagram below
    d_ov = Ellipse(width=oval_w, height=oval_h, color=ORBITAL_CYAN,
        fill_color=ORBITAL_CYAN, fill_opacity=0.05, stroke_width=1.5)
    d_ov.move_to(center + LEFT * gap/2)
    r_ov = Ellipse(width=oval_w, height=oval_h, color=VIOLET,
        fill_color=VIOLET, fill_opacity=0.05, stroke_width=1.5)
    r_ov.move_to(center + RIGHT * gap/2)

    d_lbl = Text("A", font_size=20, color=ORBITAL_CYAN, weight=BOLD)
    d_lbl.next_to(d_ov, UP, buff=0.12)
    r_lbl = Text("B", font_size=20, color=VIOLET, weight=BOLD)
    r_lbl.next_to(r_ov, UP, buff=0.12)

    # Create dots for each element
    d_dots, d_labels = VGroup(), VGroup()
    uh = oval_h - 1.0
    nd = len(domain_elements)
    for i, val in enumerate(domain_elements):
        y = uh/2 - i*(uh/max(1, nd-1)) if nd > 1 else 0
        p = d_ov.get_center() + UP * y
        dot = Dot(p, color=ORBITAL_CYAN, radius=0.07).set_glow_factor(1.5)
        lbl = Text(str(val), font_size=14, color=WHITE)
        lbl.next_to(dot, LEFT, buff=0.12)
        d_dots.add(dot)
        d_labels.add(lbl)

    r_dots, r_labels = VGroup(), VGroup()
    nr = len(range_elements)
    for i, val in enumerate(range_elements):
        y = uh/2 - i*(uh/max(1, nr-1)) if nr > 1 else 0
        p = r_ov.get_center() + UP * y
        dot = Dot(p, color=VIOLET, radius=0.07).set_glow_factor(1.5)
        lbl = Text(str(val), font_size=14, color=WHITE)
        lbl.next_to(dot, RIGHT, buff=0.12)
        r_dots.add(dot)
        r_labels.add(lbl)

    # Phase 2a: Ovals appear
    scene.play(Create(d_ov), Create(r_ov), FadeIn(d_lbl), FadeIn(r_lbl),
        run_time=0.4); t += 0.4

    # Phase 2b: Set notation elements TRANSFORM into dots
    # Each element from the set text flies to its dot position
    for i, dot in enumerate(d_dots):
        scene.play(FadeIn(dot, scale=2.0), FadeIn(d_labels[i]),
            run_time=0.2, rate_func=smooth)
        t += 0.2

    for i, dot in enumerate(r_dots):
        scene.play(FadeIn(dot, scale=2.0), FadeIn(r_labels[i]),
            run_time=0.2, rate_func=smooth)
        t += 0.2

    # Phase 2c: Fade out set notation text
    scene.play(FadeOut(sets, shift=UP * 0.3), run_time=0.3); t += 0.3

    # Phase 3: Draw arrows with tracer dots
    arrows = VGroup()
    for d_idx, r_idx in mappings:
        start = d_dots[d_idx].get_center()
        end = r_dots[r_idx].get_center()
        arr = Arrow(start, end, buff=0.12,
            color=ORBITAL_CYAN, stroke_width=1.8,
            max_tip_length_to_length_ratio=0.08, tip_length=0.12)
        arrows.add(arr)
        mapping_arrow_trace(scene, arr, run_time=0.25); t += 0.33

    diagram = VGroup(d_ov, r_ov, d_lbl, r_lbl, d_dots, d_labels, r_dots, r_labels)
    return diagram, arrows, t


def mapping_arrow_trace(scene, arrow, run_time=0.3):
    """Create an arrow with a glowing tracer dot traveling along it."""
    tracer = Dot(color=arrow.get_color(), radius=0.05).set_glow_factor(2.0)
    tracer.move_to(arrow.get_start())
    scene.play(
        Create(arrow),
        tracer.animate.move_to(arrow.get_end()),
        run_time=run_time, rate_func=smooth)
    # Brief flash at destination
    scene.play(tracer.animate.scale(1.3), run_time=0.08)
    scene.remove(tracer)


# ═══════════════════════════════════════════════════════
# VERDICT / RESULT BADGES
# ═══════════════════════════════════════════════════════

def verdict_badge(is_positive, positive_text="✓ Function",
                  negative_text="✗ Not a Function"):
    """Create a verdict badge with appropriate styling."""
    if is_positive:
        mob = tier3_callout(positive_text, color=NEON_GREEN)
    else:
        mob = tier3_callout(negative_text, color="#FF4444")
    return mob


def show_verdict(scene, mob, t=0):
    """Show a verdict with bloom effect."""
    color = NEON_GREEN if "✓" in mob.text else "#FF4444"
    scene.play(FadeIn(mob, scale=1.3), run_time=0.3)
    bloom(scene, mob, color=color, radius=0.5)
    return t + 0.5


# ═══════════════════════════════════════════════════════
# ENVIRONMENT CARDS — Axiom Reader visual language
# ═══════════════════════════════════════════════════════
# These match the Axiom Reader's styled environments exactly.
# Same colors, same icons, same structure — so students see
# consistent visual language across textbook AND video.

# Environment accent colors (from Axiom Reader CSS variables)
ENV_COLORS = {
    "definition": {"accent": "#8B5CF6", "bg": "#8B5CF60F", "icon": "◆", "label": "DEFINITION"},
    "theorem":    {"accent": "#34D399", "bg": "#34D3990F", "icon": "✦", "label": "THEOREM"},
    "example":    {"accent": "#F59E0B", "bg": "#F59E0B0F", "icon": "✎", "label": "EXAMPLE"},
    "warning":    {"accent": "#F87171", "bg": "#F871710F", "icon": "⚠", "label": "COMMON MISTAKE"},
    "tip":        {"accent": "#22D3EE", "bg": "#22D3EE0F", "icon": "💡", "label": "TIP"},
    "summary":    {"accent": "#38BDF8", "bg": "#38BDF80F", "icon": "≡", "label": "SUMMARY"},
    "proof":      {"accent": "#64748B", "bg": "#64748B0F", "icon": "∎", "label": "PROOF"},
    "property":   {"accent": "#34D399", "bg": "#34D3990F", "icon": "✦", "label": "PROPERTY"},
}


def env_card(env_type, title, lines, width=5.0, number=None):
    """
    Build an Axiom Reader-style environment card for video.

    Args:
        env_type: "definition", "theorem", "example", "warning", "tip", "summary", "proof", "property"
        title: Title text (e.g., "Function" for a definition)
        lines: List of (type, content) tuples:
            ("text", "plain text line")
            ("math", r"f : A \\to B")
            ("bold", "emphasized text")
        width: Card width
        number: Optional number (e.g., "1.1" → "Definition 1.1")

    Returns: (card_group, glow, content_mobs)
        card_group: The full card VGroup
        glow: Glow rectangle for alive_hold
        content_mobs: List of content mobjects (for staggered animation)
    """
    cfg = ENV_COLORS.get(env_type, ENV_COLORS["definition"])
    accent = cfg["accent"]
    icon = cfg["icon"]
    label_text = cfg["label"]

    # Card body
    card = RoundedRectangle(
        width=width, height=0.1,  # height set dynamically below
        corner_radius=0.12,
        fill_color=BOX_FILL, fill_opacity=0.85,
        stroke_color=BOX_STROKE, stroke_width=1,
    )

    # Top accent border (2px colored line)
    top_bar = Line(ORIGIN, RIGHT * (width - 0.3),
        color=accent, stroke_width=3)

    # Label: "◆ DEFINITION 1.1"
    label_str = f"{icon} {label_text}"
    if number:
        label_str += f" {number}"
    label = Text(label_str, font_size=10, color=accent, weight=BOLD)

    # Title (if provided)
    title_mob = None
    if title:
        title_mob = Text(title, font_size=22, color=WHITE, weight=BOLD)

    # Content lines
    content_mobs = []
    for line_type, content in lines:
        if line_type == "math":
            mob = MathTex(content, font_size=24, color=WHITE)
        elif line_type == "bold":
            mob = Text(content, font_size=16, color=accent, weight=BOLD)
        else:  # "text"
            mob = Text(content, font_size=14, color=AXIOM_TEXT)
        # Clamp width
        if mob.width > width - 0.6:
            mob.scale((width - 0.6) / mob.width)
        content_mobs.append(mob)

    # Layout everything vertically
    elements = [label]
    if title_mob:
        elements.append(title_mob)
    elements.extend(content_mobs)

    # Calculate height
    total_h = 0.4  # top padding
    for el in elements:
        total_h += el.height + 0.2
    total_h += 0.3  # bottom padding
    total_h = max(total_h, 1.5)

    # Resize card
    card = RoundedRectangle(
        width=width, height=total_h,
        corner_radius=0.12,
        fill_color=BOX_FILL, fill_opacity=0.85,
        stroke_color=BOX_STROKE, stroke_width=1,
    )

    # Position elements
    top_bar.move_to(card.get_top() + DOWN * 0.02)
    top_bar.align_to(card, LEFT).shift(RIGHT * 0.15)

    y = card.get_top()[1] - 0.35
    label.move_to([card.get_left()[0] + 0.3 + label.width/2, y, 0])
    y -= label.height/2 + 0.25

    if title_mob:
        title_mob.move_to([card.get_left()[0] + 0.3 + title_mob.width/2, y, 0])
        y -= title_mob.height/2 + 0.2

    for mob in content_mobs:
        mob.move_to([card.get_left()[0] + 0.3 + mob.width/2, y, 0])
        y -= mob.height/2 + 0.18

    # Glow
    glow = RoundedRectangle(
        width=width + 0.08, height=total_h + 0.08,
        corner_radius=0.12,
        fill_opacity=0, stroke_color=accent,
        stroke_width=6, stroke_opacity=0.15,
    )
    glow.move_to(card.get_center())

    # Assemble
    all_parts = [card, top_bar, label]
    if title_mob:
        all_parts.append(title_mob)
    all_parts.extend(content_mobs)
    grp = VGroup(*all_parts)

    return grp, glow, content_mobs


def animate_env_card(scene, grp, glow, content_mobs, t=0):
    """
    Animate an environment card with the full alive treatment.

    Sequence:
    1. Card body fades in (0.2s)
    2. Top accent bar draws left-to-right (0.3s)
    3. Label fades in (0.15s)
    4. Title fades in with bloom (0.3s)
    5. Each content line staggers in (0.2s each)
    6. Glow pulse on completion

    Returns: time elapsed
    """
    card, top_bar, label = grp[0], grp[1], grp[2]
    has_title = len(grp) > 3 + len(content_mobs)
    title_mob = grp[3] if has_title else None

    accent = top_bar.get_color()

    # Add glow behind
    scene.add(glow)

    # 1. Card body
    scene.play(FadeIn(card, shift=UP * 0.15), run_time=0.2); t += 0.2

    # 2. Top bar draws
    scene.play(Create(top_bar), run_time=0.3, rate_func=smooth); t += 0.3

    # 3. Label
    scene.play(FadeIn(label, shift=RIGHT * 0.2), run_time=0.15); t += 0.15

    # 4. Title with bloom
    if title_mob:
        scene.play(FadeIn(title_mob, shift=UP * 0.1), run_time=0.2); t += 0.2
        bloom(scene, title_mob, color=accent, radius=0.4); t += 0.2

    # 5. Content lines stagger
    for mob in content_mobs:
        scene.play(FadeIn(mob, shift=UP * 0.08), run_time=0.2, rate_func=smooth)
        t += 0.2

    # 6. Final glow pulse
    scene.play(
        glow.animate.set_stroke(opacity=0.25), run_time=0.2, rate_func=smooth)
    scene.play(
        glow.animate.set_stroke(opacity=0.15), run_time=0.3, rate_func=smooth)
    t += 0.5

    return t


def env_definition(title, lines, width=5.0, number=None):
    """Shortcut: Definition card (violet ◆)."""
    return env_card("definition", title, lines, width, number)

def env_theorem(title, lines, width=5.0, number=None):
    """Shortcut: Theorem card (emerald ✦)."""
    return env_card("theorem", title, lines, width, number)

def env_example(title, lines, width=5.0, number=None):
    """Shortcut: Example card (amber ✎)."""
    return env_card("example", title, lines, width, number)

def env_warning(title, lines, width=5.0, number=None):
    """Shortcut: Common Mistake card (red ⚠)."""
    return env_card("warning", title, lines, width, number)

def env_tip(title, lines, width=5.0, number=None):
    """Shortcut: Tip card (cyan 💡)."""
    return env_card("tip", title, lines, width, number)

def env_summary(title, lines, width=5.0, number=None):
    """Shortcut: Summary card (sky ≡)."""
    return env_card("summary", title, lines, width, number)

def env_property(title, lines, width=5.0, number=None):
    """Shortcut: Property card (emerald ✦)."""
    return env_card("property", title, lines, width, number)


# ═══════════════════════════════════════════════════════
# CHAPTER CARDS — A/B/C section transitions
# ═══════════════════════════════════════════════════════

CHAPTER_COLORS = {
    "concepts":   ORBITAL_CYAN,   # A — Concepts
    "skills":     NEON_GREEN,     # B — Skills
    "extensions": VIOLET,         # C — Extensions
}

CHAPTER_LABELS = {
    "concepts":   "CONCEPTS",
    "skills":     "SKILLS",
    "extensions": "EXTENSIONS",
}


def chapter_card(section, title, chapter_type="concepts"):
    """
    Build an animated chapter transition card (A/B/C sections).
    Styled like welcome video thumbnails.

    Args:
        section: Section number (e.g., "1.1")
        title: Section title or subtitle/hook
        chapter_type: "concepts", "skills", or "extensions"

    Returns: (card_group, glow, lissajous)
    """
    color = CHAPTER_COLORS.get(chapter_type, ORBITAL_CYAN)
    label = CHAPTER_LABELS.get(chapter_type, "CONCEPTS")

    # Section context
    sec = Text(f"§{section}", font_size=14, color="#666666", weight=BOLD)

    # Big chapter label
    main = Text(label, font_size=52, color=color, weight=BOLD)
    main_glow = main.copy().set_opacity(0.2).scale(1.02)

    # Decorative lines
    ll = Line(ORIGIN, LEFT * 2.5, color=color, stroke_width=2, stroke_opacity=0.6)
    lr = Line(ORIGIN, RIGHT * 2.5, color=color, stroke_width=2, stroke_opacity=0.6)

    # Subtitle/hook
    sub = Text(title, font_size=20, color=WHITE)
    if sub.width > 10:
        sub.scale(10 / sub.width)

    # Lissajous watermark
    A, B = 0.6, 0.4
    liss = ParametricFunction(
        lambda t: np.array([A * np.sin(2*t), B * np.sin(3*t), 0]),
        t_range=[0, TAU, 0.01],
        color=color, stroke_width=1.5, stroke_opacity=0.2,
    )

    # Brand
    brand = Text("MERIDIAN MATH × ORBITAL", font_size=10, color="#444444", weight=BOLD)

    # Layout
    sec.move_to([0, 2.5, 0])
    main.move_to([0, 0.8, 0])
    main_glow.move_to(main.get_center())
    ll.next_to(main, LEFT, buff=0.3)
    lr.next_to(main, RIGHT, buff=0.3)
    sub.move_to([0, -0.3, 0])
    liss.move_to([0, -1.8, 0])
    brand.move_to([0, -2.8, 0])

    # Glow behind main text
    glow = make_glow(main, color, 10, 0.15)

    grp = VGroup(sec, main_glow, main, ll, lr, sub, liss, brand)
    return grp, glow, liss


def animate_chapter_card(scene, grp, glow, liss, duration=3.0, t=0):
    """
    Animate a chapter transition card.

    Sequence:
    1. Section label fades in
    2. Main label scales in with bloom + glow
    3. Decorative lines draw outward
    4. Subtitle fades up
    5. Lissajous traces
    6. Brand fades in
    7. Hold with glow breathing
    8. Everything fades out

    Returns: time elapsed
    """
    sec, main_glow, main, ll, lr, sub, liss_curve, brand = \
        grp[0], grp[1], grp[2], grp[3], grp[4], grp[5], grp[6], grp[7]

    color = main.color

    scene.add(glow)

    # 1. Section
    scene.play(FadeIn(sec, shift=DOWN * 0.2), run_time=0.2); t += 0.2

    # 2. Main label
    scene.play(
        FadeIn(main, scale=0.8),
        FadeIn(main_glow),
        run_time=0.4, rate_func=smooth); t += 0.4
    bloom(scene, main, color=color, radius=0.8); t += 0.2

    # 3. Lines draw outward
    scene.play(Create(ll), Create(lr), run_time=0.3); t += 0.3

    # 4. Subtitle
    scene.play(FadeIn(sub, shift=UP * 0.15), run_time=0.3); t += 0.3

    # 5. Lissajous traces
    scene.play(Create(liss_curve), run_time=0.5, rate_func=smooth); t += 0.5

    # 6. Brand
    scene.play(FadeIn(brand), run_time=0.2); t += 0.2

    # 7. Hold with glow breathing
    hold = max(0.5, duration - t - 0.5)
    if hold > 0.5:
        alive_hold(scene, main, glow, hold, style="glow_pulse")
        t += hold

    # 8. Fade everything out
    scene.play(FadeOut(VGroup(grp, glow), shift=UP * 0.3), run_time=0.5); t += 0.5

    return t
