"""
Orbital — Channel Promo Showcase v3 (16:9 Landscape)
=====================================================
MAINFRAME × ORBITAL collab promo for Clayton's MAINFRAME channel.

Changes from v2:
  - ACT 1: MAINFRAME × ORBITAL collab intro (both logos)
  - Slogan: "Watch it click." (replaces "Math that clicks.")
  - Descriptor: "The why behind the math." (replaces "What if math actually made sense?")
  - 9-course grid (added Real Analysis, Abstract Algebra, Number Theory)
  - @orbital-solver on CTA

Render:
  cd ~/Desktop/Orbital/orbital_factory && source venv/bin/activate
  PATH="/Library/TeX/texbin:$PATH" manim render prototypes/promo_showcase_v3.py PromoShowcaseV3 \
    -o promo_showcase_v3.mp4 --format mp4 -r 1920,1080 --frame_rate 60 --flush_cache
"""
from manim import *
import numpy as np

config.frame_width = 14.2
config.frame_height = 8.0

# ── BRAND COLORS ──
VIOLET = "#8B5CF6"
CYAN = "#22D3EE"
GREEN = "#39FF14"
ORANGE = "#F97316"
BOX_FILL = "#1a1130"
END_CYAN = "#00E5FF"
MAINFRAME_CYAN = "#00FFFF"  # Bright neon cyan for MAINFRAME brand
FW = 14.2
FH = 8.0


def _make_gear(radius, n_teeth, color, center, tooth_len=0.14, sw=2.5):
    parts = []
    circle = Circle(radius=radius, color=color, stroke_width=sw,
                    fill_color=BOX_FILL, fill_opacity=0.4).move_to(center)
    parts.append(circle)
    parts.append(Dot(radius=0.06, color=color, fill_opacity=0.8).move_to(center))
    for i in range(n_teeth):
        a = i * TAU / n_teeth
        ip = np.array(center) + radius * np.array([np.cos(a), np.sin(a), 0])
        op = np.array(center) + (radius + tooth_len) * np.array([np.cos(a), np.sin(a), 0])
        perp = np.array([-np.sin(a), np.cos(a), 0])
        tw = 0.08
        tooth = Polygon(ip + perp * tw, ip - perp * tw, op - perp * tw * 0.7, op + perp * tw * 0.7,
                        color=color, stroke_width=sw - 0.5, fill_color=color, fill_opacity=0.3)
        parts.append(tooth)
    return VGroup(*parts)


def _make_machine(label, sublabel, color, center, width=3.0, height=1.4):
    box = RoundedRectangle(width=width, height=height, color=color,
                           fill_color=BOX_FILL, fill_opacity=0.7,
                           stroke_width=2.5, corner_radius=0.12).move_to(center)
    lbl = Text(label, font_size=30, color=color, weight=BOLD).move_to(box.get_center() + UP * 0.2)
    sub = MathTex(sublabel, font_size=24, color=WHITE).set_opacity(0.8).move_to(box.get_center() + DOWN * 0.25)
    return VGroup(box, lbl, sub)


def _make_mainframe_logo(center, scale=1.0):
    """Recreate MAINFRAME logo essence: connected neon circuit nodes."""
    nodes_pos = [
        np.array([-1.2, 0.8, 0]),   # top left
        np.array([0.0, 1.2, 0]),     # top center
        np.array([1.2, 0.8, 0]),     # top right
        np.array([-0.8, -0.2, 0]),   # mid left
        np.array([0.0, 0.0, 0]),     # center (main hub)
        np.array([0.8, -0.2, 0]),    # mid right
        np.array([-0.4, -1.0, 0]),   # bottom left
        np.array([0.4, -1.0, 0]),    # bottom right
    ]
    # Scale and offset
    nodes_pos = [p * scale + np.array([*center, 0]) if len(center) == 2
                 else p * scale + np.array(center) for p in nodes_pos]

    # Connections (circuit board style)
    connections = [
        (0, 1), (1, 2), (0, 3), (3, 4), (4, 5), (2, 5),
        (3, 6), (4, 6), (4, 7), (5, 7), (1, 4),
    ]

    lines = VGroup()
    for i, j in connections:
        glow = Line(nodes_pos[i], nodes_pos[j], color=MAINFRAME_CYAN,
                    stroke_width=4, stroke_opacity=0.2)
        core = Line(nodes_pos[i], nodes_pos[j], color=MAINFRAME_CYAN,
                    stroke_width=1.5, stroke_opacity=0.8)
        lines.add(glow, core)

    dots = VGroup()
    for p in nodes_pos:
        glow = Dot(radius=0.12 * scale, color=MAINFRAME_CYAN, fill_opacity=0.2).move_to(p)
        core = Dot(radius=0.06 * scale, color=MAINFRAME_CYAN, fill_opacity=0.9).move_to(p)
        dots.add(glow, core)

    # Center node bigger
    center_glow = Dot(radius=0.18 * scale, color=MAINFRAME_CYAN, fill_opacity=0.3).move_to(nodes_pos[4])
    center_dot = Dot(radius=0.09 * scale, color=MAINFRAME_CYAN, fill_opacity=1.0).move_to(nodes_pos[4])
    dots.add(center_glow, center_dot)

    return VGroup(lines, dots)


class PromoShowcaseV3(Scene):
    def construct(self):
        self.camera.background_color = BLACK

        # ── Persistent border ──
        border = Rectangle(width=FW - 0.2, height=FH - 0.2, color=VIOLET,
                           stroke_width=2.5, stroke_opacity=0.7, fill_opacity=0).move_to(ORIGIN)
        border_glow = Rectangle(width=FW - 0.15, height=FH - 0.15, color=VIOLET,
                                stroke_width=6, stroke_opacity=0.12, fill_opacity=0).move_to(ORIGIN)
        self.add(border_glow, border)
        wm = Text("ORBITAL", font_size=12, color=WHITE, weight=BOLD)
        wm.set_opacity(0.35).move_to([-FW / 2 + 0.7, -FH / 2 + 0.25, 0])
        self.add(wm)

        # ═════════════════════════════════════════════════════
        # ACT 1: MAINFRAME × ORBITAL COLLAB INTRO (6s)
        # ═════════════════════════════════════════════════════

        # -- MAINFRAME side (left) --
        mf_logo = _make_mainframe_logo([-3.5, 0.5], scale=1.2)
        mf_text = Text("MAINFRAME", font_size=36, color=MAINFRAME_CYAN, weight=BOLD)
        mf_text.move_to([-3.5, -1.2, 0])
        mf_glow = mf_text.copy().set_opacity(0.25).scale(1.03)

        # -- × symbol --
        collab_x = Text("×", font_size=60, color=WHITE, weight=BOLD)
        collab_x.move_to([0, 0, 0])

        # -- ORBITAL side (right) --
        _A, _B = 1.4, 1.0
        orb_liss_glow = ParametricFunction(
            lambda t: np.array([_A * np.sin(2 * t) + 3.5, _B * np.sin(3 * t) + 0.5, 0]),
            t_range=[0, TAU, 0.01],
            color=END_CYAN, stroke_width=8, stroke_opacity=0.2
        )
        orb_liss_core = ParametricFunction(
            lambda t: np.array([_A * np.sin(2 * t) + 3.5, _B * np.sin(3 * t) + 0.5, 0]),
            t_range=[0, TAU, 0.01],
            color=END_CYAN, stroke_width=2.5, stroke_opacity=1.0
        )
        orb_text = Text("ORBITAL", font_size=36, color=END_CYAN, weight=BOLD)
        orb_text.move_to([3.5, -1.2, 0])
        orb_glow = orb_text.copy().set_opacity(0.25).scale(1.03)

        # Animate: MAINFRAME fades in from left
        self.play(
            FadeIn(mf_logo, shift=RIGHT * 0.3),
            FadeIn(VGroup(mf_glow, mf_text), shift=RIGHT * 0.3),
            run_time=0.8
        )
        self.wait(0.3)

        # × appears
        self.play(FadeIn(collab_x, scale=0.5), run_time=0.3)

        # ORBITAL fades in from right
        self.play(
            Create(orb_liss_core, run_time=0.8),
            FadeIn(orb_liss_glow, run_time=0.6),
            FadeIn(VGroup(orb_glow, orb_text), shift=LEFT * 0.3),
            run_time=0.8
        )
        self.wait(0.8)

        # Pulse both logos together
        self.play(
            Flash(mf_logo[1][-1], color=MAINFRAME_CYAN, line_length=0.3, num_lines=8, run_time=0.4),
            Circumscribe(VGroup(orb_liss_core), color=END_CYAN, run_time=0.5),
            collab_x.animate.set_color(VIOLET),
            run_time=0.5
        )
        self.wait(0.5)

        # Fade out collab intro
        collab_all = VGroup(mf_logo, mf_glow, mf_text, collab_x,
                            orb_liss_glow, orb_liss_core, orb_glow, orb_text)
        self.play(FadeOut(collab_all, shift=UP * 0.5), run_time=0.5)
        self.wait(0.2)

        # ═════════════════════════════════════════════════════
        # ACT 2: TAGLINE SLAM (3s)
        # ═════════════════════════════════════════════════════
        tagline_main = Text("The why behind the math.",
                            font_size=44, color=WHITE, weight=BOLD)
        self.play(FadeIn(tagline_main, scale=0.9), run_time=0.4)
        self.wait(1.5)
        self.play(
            tagline_main.animate.set_color(GREEN),
            Circumscribe(tagline_main, color=GREEN, run_time=0.6),
        )
        self.wait(0.5)
        self.play(FadeOut(tagline_main, shift=LEFT * 2), run_time=0.4)

        # ═════════════════════════════════════════════════════
        # ACT 3: GEAR SHOWCASE (5s)
        # ═════════════════════════════════════════════════════
        g1 = _make_gear(1.2, 14, VIOLET, [-2.0, 0, 0], 0.22, 3)
        g2 = _make_gear(0.85, 10, CYAN, [0.5, 0, 0], 0.18, 3)
        g3 = _make_gear(0.6, 8, ORANGE, [2.3, 0.8, 0], 0.14, 2.5)

        gear_label = Text("Everything connects.", font_size=28, color=WHITE)
        gear_label.set_opacity(0.7).move_to([0, -2.5, 0])

        self.play(FadeIn(g1), FadeIn(g2), FadeIn(g3), run_time=0.4)
        self.play(
            Rotate(g1, PI / 2, about_point=[-2.0, 0, 0]),
            Rotate(g2, -PI / 1.8, about_point=[0.5, 0, 0]),
            Rotate(g3, PI / 1.5, about_point=[2.3, 0.8, 0]),
            FadeIn(gear_label),
            run_time=2.0
        )
        self.wait(1.0)
        self.play(
            Rotate(g1, PI / 3, about_point=[-2.0, 0, 0]),
            Rotate(g2, -PI / 2.5, about_point=[0.5, 0, 0]),
            Rotate(g3, PI / 2, about_point=[2.3, 0.8, 0]),
            run_time=1.5
        )
        self.play(FadeOut(VGroup(g1, g2, g3, gear_label)), run_time=0.4)

        # ═════════════════════════════════════════════════════
        # ACT 4: FUNCTION MACHINE PIPELINE (8s)
        # ═════════════════════════════════════════════════════
        m1 = _make_machine("TRIPLE", r"u = 3x", ORANGE, [-3, 0, 0])
        m2 = _make_machine("SQUARE", r"y = u^2", CYAN, [3, 0, 0])
        pipe = Arrow(m1[0].get_right() + RIGHT * 0.1, m2[0].get_left() + LEFT * 0.1,
                     color=WHITE, stroke_width=3, buff=0, max_tip_length_to_length_ratio=0.15)

        self.play(FadeIn(m1), run_time=0.3)
        self.play(Create(pipe), run_time=0.3)
        self.play(FadeIn(m2), run_time=0.3)
        self.wait(0.3)

        num2 = MathTex("2", font_size=48, color=GREEN)
        c2 = Circle(radius=0.4, color=GREEN, fill_color=GREEN, fill_opacity=0.15, stroke_width=2)
        n2_grp = VGroup(c2, num2).move_to([-5.5, 0, 0])

        num6 = MathTex("6", font_size=48, color=ORANGE)
        c6 = Circle(radius=0.4, color=ORANGE, fill_color=ORANGE, fill_opacity=0.15, stroke_width=2)
        n6_grp = VGroup(c6, num6).move_to(m1.get_center())

        num36 = MathTex("36", font_size=44, color=CYAN)
        c36 = Circle(radius=0.4, color=CYAN, fill_color=CYAN, fill_opacity=0.15, stroke_width=2)
        n36_grp = VGroup(c36, num36).move_to(m2.get_center())

        self.play(FadeIn(n2_grp, scale=0.5), run_time=0.2)
        self.play(n2_grp.animate.move_to(m1.get_center()), run_time=0.6)
        self.play(
            FadeOut(n2_grp), FadeIn(n6_grp, scale=1.3),
            Flash(m1[0], color=ORANGE, line_length=0.4, num_lines=12, run_time=0.3),
            run_time=0.4
        )
        self.play(n6_grp.animate.move_to(pipe.get_center()), run_time=0.3)
        self.play(n6_grp.animate.move_to(m2.get_center()), run_time=0.3)
        self.play(
            FadeOut(n6_grp), FadeIn(n36_grp, scale=1.3),
            Flash(m2[0], color=CYAN, line_length=0.4, num_lines=12, run_time=0.3),
            run_time=0.4
        )
        self.play(n36_grp.animate.move_to([5.5, 0, 0]), run_time=0.5)

        product = MathTex(r"3 \times 12 = 36", font_size=42, color=WHITE)
        product[0][0].set_color(ORANGE)
        product[0][2:4].set_color(CYAN)
        product[0][5:7].set_color(GREEN)
        product.move_to([0, -2.2, 0])
        self.play(FadeOut(n36_grp), Write(product), run_time=0.5)
        self.wait(1.0)
        self.play(FadeOut(VGroup(m1, m2, pipe, product)), run_time=0.4)

        # ═════════════════════════════════════════════════════
        # ACT 5: RIEMANN SUM (6s)
        # ═════════════════════════════════════════════════════
        r_axes = Axes(
            x_range=[0, 4, 1], y_range=[0, 5, 1],
            x_length=8, y_length=4.5, tips=False,
            axis_config={"color": WHITE, "stroke_width": 1.5, "stroke_opacity": 0.5},
        ).move_to([0, 0, 0])

        r_curve = r_axes.plot(lambda x: 0.3 * x ** 2 + 0.5, x_range=[0.2, 3.8],
                              color=VIOLET, stroke_width=3)

        self.play(Create(r_axes, run_time=0.4), Create(r_curve, run_time=0.5))

        def _make_rects(n, color, opacity=0.4):
            rects = VGroup()
            dx = 3.6 / n
            for i in range(n):
                x_val = 0.2 + i * dx
                y_val = 0.3 * x_val ** 2 + 0.5
                rect = Rectangle(
                    width=r_axes.x_length * dx / 4,
                    height=r_axes.y_length * y_val / 5,
                    color=color, fill_color=color, fill_opacity=opacity,
                    stroke_width=1.5,
                )
                rect.move_to(r_axes.c2p(x_val + dx / 2, y_val / 2))
                rects.add(rect)
            return rects

        rects4 = _make_rects(4, CYAN, 0.3)
        rects8 = _make_rects(8, CYAN, 0.35)
        rects16 = _make_rects(16, CYAN, 0.4)

        self.play(FadeIn(rects4), run_time=0.5)
        self.wait(0.6)
        self.play(ReplacementTransform(rects4, rects8), run_time=0.6)
        self.wait(0.6)
        self.play(ReplacementTransform(rects8, rects16), run_time=0.6)
        self.wait(0.8)

        integral_label = MathTex(r"\int_0^4 f(x)\, dx", font_size=36, color=CYAN)
        integral_label.move_to([4.5, 2.0, 0])
        self.play(Write(integral_label), run_time=0.4)
        self.wait(0.5)
        self.play(FadeOut(VGroup(r_axes, r_curve, rects16, integral_label)), run_time=0.4)

        # ═════════════════════════════════════════════════════
        # ACT 6: GRAPH + TANGENT LINE (6s)
        # ═════════════════════════════════════════════════════
        axes = Axes(
            x_range=[-1, 5, 1], y_range=[-1, 8, 2],
            x_length=8, y_length=5, tips=False,
            axis_config={"color": WHITE, "stroke_width": 1.5, "stroke_opacity": 0.5},
        ).move_to([0, 0.2, 0])

        curve = axes.plot(lambda x: 0.3 * x ** 2 + 0.5, x_range=[0, 4.5],
                          color=VIOLET, stroke_width=3)
        curve_label = MathTex(r"f(x) = 0.3x^2 + 0.5", font_size=22, color=VIOLET)
        curve_label.next_to(curve, UR, buff=0.3)

        self.play(Create(axes, run_time=0.5), Create(curve, run_time=0.8))
        self.play(FadeIn(curve_label), run_time=0.3)

        x_tracker = ValueTracker(1.0)

        def get_tangent():
            x = x_tracker.get_value()
            y = 0.3 * x ** 2 + 0.5
            slope = 0.6 * x
            dx = 1.5
            p1 = axes.c2p(x - dx, y - slope * dx)
            p2 = axes.c2p(x + dx, y + slope * dx)
            return Line(p1, p2, color=GREEN, stroke_width=2.5)

        tangent = always_redraw(get_tangent)
        dot = always_redraw(
            lambda: Dot(
                axes.c2p(x_tracker.get_value(),
                         0.3 * x_tracker.get_value() ** 2 + 0.5),
                color=GREEN, radius=0.08
            ).set_glow_factor(0.8)
        )

        self.add(tangent, dot)
        self.play(x_tracker.animate.set_value(4.0), run_time=3.0, rate_func=smooth)
        self.wait(0.5)
        self.play(x_tracker.animate.set_value(2.0), run_time=1.5, rate_func=smooth)
        self.wait(0.3)
        self.play(FadeOut(VGroup(axes, curve, curve_label, tangent, dot)), run_time=0.4)

        # ═════════════════════════════════════════════════════
        # ACT 7: ALGEBRA CASCADE (5s)
        # ═════════════════════════════════════════════════════
        steps = [
            r"x^2 + 6x + 9 = 0",
            r"(x + 3)^2 = 0",
            r"x + 3 = 0",
            r"x = -3",
        ]
        colors = [WHITE, CYAN, CYAN, GREEN]

        prev_mob = None
        step_mobs = []
        for j, (s, c) in enumerate(zip(steps, colors)):
            eq = MathTex(s, font_size=48, color=c)
            eq.move_to([0, 0, 0])
            if prev_mob:
                self.play(
                    prev_mob.animate.set_opacity(0.3).shift(UP * 1.2),
                    Write(eq),
                    run_time=0.5
                )
            else:
                self.play(Write(eq), run_time=0.5)
            self.wait(0.5)
            step_mobs.append(eq)
            prev_mob = eq

        answer_box = SurroundingRectangle(
            prev_mob, color=GREEN, fill_color=BOX_FILL,
            fill_opacity=0.6, buff=0.2, corner_radius=0.1, stroke_width=2.5,
        )
        self.play(Create(answer_box), run_time=0.3)
        self.play(Circumscribe(answer_box, color=GREEN, run_time=0.5))
        self.wait(0.5)

        self.play(
            *[FadeOut(m) for m in self.mobjects if m not in [border, border_glow, wm]],
            run_time=0.4
        )

        # ═════════════════════════════════════════════════════
        # ACT 8: TOPIC GRID — 9 COURSES (5s)
        # ═════════════════════════════════════════════════════
        topics = [
            ("Calculus", VIOLET),
            ("Precalculus", CYAN),
            ("Algebra", ORANGE),
            ("Statistics", GREEN),
            ("Linear Algebra", "#FF6B9D"),
            ("Discrete Math", "#FFD700"),
            ("Real Analysis", END_CYAN),
            ("Abstract Algebra", "#C084FC"),
            ("Number Theory", "#FB923C"),
        ]

        grid = VGroup()
        for topic, color in topics:
            txt = Text(topic, font_size=26, color=color, weight=BOLD)
            box = SurroundingRectangle(txt, color=color, fill_color=BOX_FILL,
                                       fill_opacity=0.5, buff=0.18, corner_radius=0.08,
                                       stroke_width=2)
            card = VGroup(box, txt)
            grid.add(card)

        grid.arrange_in_grid(rows=3, cols=3, buff=0.4)
        grid.move_to([0, 0.3, 0])

        for card in grid:
            self.play(FadeIn(card, scale=0.8), run_time=0.15)
            self.wait(0.1)

        self.wait(1.5)

        self.play(
            *[Indicate(card, color=card[1].color, scale_factor=1.05) for card in grid],
            run_time=0.6
        )
        self.wait(0.5)
        self.play(FadeOut(grid), run_time=0.4)

        # ═════════════════════════════════════════════════════
        # ACT 9: SUBSCRIBE CTA (5s)
        # ═════════════════════════════════════════════════════
        cta_line1 = Text("Watch it click.",
                         font_size=42, color=WHITE, weight=BOLD)
        cta_line1.move_to([0, 1.5, 0])

        cta_line2 = Text("Subscribe to Orbital.",
                         font_size=44, color=END_CYAN, weight=BOLD)
        cta_line2.move_to([0, 0.0, 0])

        handle = Text("@orbital-solver", font_size=28, color=END_CYAN)
        handle.set_opacity(0.7)
        handle.next_to(cta_line2, DOWN, buff=0.25)

        subtitle = Text("The why behind the math.", font_size=24, color=WHITE)
        subtitle.set_opacity(0.5)
        subtitle.next_to(handle, DOWN, buff=0.35)

        self.play(Write(cta_line1), run_time=0.6)
        self.wait(0.4)
        self.play(FadeIn(cta_line2, shift=UP * 0.2), run_time=0.5)
        self.play(FadeIn(handle), run_time=0.3)
        self.play(FadeIn(subtitle), run_time=0.3)

        cta_box = SurroundingRectangle(
            VGroup(cta_line2, handle), color=END_CYAN, fill_color=BOX_FILL,
            fill_opacity=0.4, buff=0.25, corner_radius=0.1, stroke_width=2.5,
        )
        self.play(Create(cta_box), run_time=0.3)
        self.play(Circumscribe(VGroup(cta_box, cta_line2), color=END_CYAN, run_time=0.6))
        self.wait(1.2)

        self.play(FadeOut(VGroup(cta_line1, cta_line2, handle, subtitle, cta_box)), run_time=0.4)

        # ═════════════════════════════════════════════════════
        # END CARD: Lissajous + wordmark + new tagline
        # ═════════════════════════════════════════════════════
        _A2, _B2 = 2.0, 1.5
        liss_glow2 = ParametricFunction(
            lambda t: np.array([_A2 * np.sin(2 * t), _B2 * np.sin(3 * t), 0]),
            t_range=[0, TAU, 0.01],
            color=END_CYAN, stroke_width=10, stroke_opacity=0.2
        )
        liss_core2 = ParametricFunction(
            lambda t: np.array([_A2 * np.sin(2 * t), _B2 * np.sin(3 * t), 0]),
            t_range=[0, TAU, 0.01],
            color=END_CYAN, stroke_width=3, stroke_opacity=1.0
        )
        logo2 = VGroup(liss_glow2, liss_core2).move_to([0, 0.5, 0])
        wordmark2 = Text("ORBITAL", font_size=48, color=END_CYAN, weight=BOLD)
        wordmark2.next_to(logo2, DOWN, buff=0.4)
        wm_glow2 = wordmark2.copy().set_opacity(0.3).scale(1.03)
        tagline2 = Text("Watch it click.", font_size=24, color=WHITE)
        tagline2.set_opacity(0.6)
        tagline2.next_to(wordmark2, DOWN, buff=0.2)

        end = VGroup(logo2, wm_glow2, wordmark2, tagline2)
        end.move_to([0, 0, 0])

        self.play(Create(liss_core2, run_time=1.0), FadeIn(liss_glow2, run_time=0.8))
        self.play(FadeIn(VGroup(wm_glow2, wordmark2), shift=UP * 0.2), run_time=0.4)
        self.play(FadeIn(tagline2), run_time=0.3)
        self.wait(2.0)
        self.play(FadeOut(end), run_time=0.5)
