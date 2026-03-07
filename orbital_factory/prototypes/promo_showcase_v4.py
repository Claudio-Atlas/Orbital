"""
Orbital — Channel Promo Showcase v4 (16:9 Landscape)
=====================================================
MAINFRAME × ORBITAL collab promo. Major upgrades from v3:
  - Actual MAINFRAME logo (ImageMobject)
  - Subtle animated background grid
  - sin(x) Riemann sum (above AND below x-axis)
  - Camera movements (MovingCameraScene) — zoom/pan between acts
  - More polish and effects

Render:
  cd ~/Desktop/Orbital/orbital_factory && source venv/bin/activate
  PATH="/Library/TeX/texbin:$PATH" manim render prototypes/promo_showcase_v4.py PromoShowcaseV4 \
    -o promo_showcase_v4.mp4 --format mp4 -r 1920,1080 --frame_rate 60 --flush_cache
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
MAINFRAME_CYAN = "#00FFFF"
GRID_COLOR = "#1a1a3a"
FW = 14.2
FH = 8.0

LOGO_PATH = "assets/images/mainframe_logo.png"


def _make_bg_grid(fw=14.2, fh=8.0, spacing=0.8, color=GRID_COLOR, sw=0.5, opacity=0.3):
    """Create a subtle background grid."""
    lines = VGroup()
    # Vertical lines
    x = -fw / 2
    while x <= fw / 2:
        l = Line([x, -fh / 2, 0], [x, fh / 2, 0], color=color,
                 stroke_width=sw, stroke_opacity=opacity)
        lines.add(l)
        x += spacing
    # Horizontal lines
    y = -fh / 2
    while y <= fh / 2:
        l = Line([-fw / 2, y, 0], [fw / 2, y, 0], color=color,
                 stroke_width=sw, stroke_opacity=opacity)
        lines.add(l)
        y += spacing
    return lines


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


class PromoShowcaseV4(MovingCameraScene):
    def construct(self):
        self.camera.background_color = BLACK
        self.camera.frame.set(width=FW, height=FH)

        # ── Background grid (persistent, subtle) ──
        bg_grid = _make_bg_grid(fw=20, fh=14, spacing=0.8,
                                color=GRID_COLOR, sw=0.5, opacity=0.15)
        self.add(bg_grid)

        # ── Camera-following border + watermark ──
        # These redraw every frame to stay locked to the camera viewport
        def _get_border():
            cf = self.camera.frame
            w = cf.get_width() - 0.2
            h = cf.get_height() - 0.2
            return Rectangle(width=w, height=h, color=VIOLET,
                             stroke_width=2.5, stroke_opacity=0.7,
                             fill_opacity=0).move_to(cf.get_center())

        def _get_border_glow():
            cf = self.camera.frame
            w = cf.get_width() - 0.15
            h = cf.get_height() - 0.15
            return Rectangle(width=w, height=h, color=VIOLET,
                             stroke_width=6, stroke_opacity=0.12,
                             fill_opacity=0).move_to(cf.get_center())

        def _get_watermark():
            cf = self.camera.frame
            cx, cy = cf.get_center()[0], cf.get_center()[1]
            hw, hh = cf.get_width() / 2, cf.get_height() / 2
            t = Text("ORBITAL", font_size=12, color=WHITE, weight=BOLD)
            t.set_opacity(0.35)
            t.move_to([cx - hw + 0.7, cy - hh + 0.25, 0])
            return t

        border = always_redraw(_get_border)
        border_glow = always_redraw(_get_border_glow)
        wm = always_redraw(_get_watermark)
        self.add(border_glow, border, wm)

        # ═════════════════════════════════════════════════════
        # ACT 1: MAINFRAME × ORBITAL COLLAB INTRO (7s)
        # Camera starts slightly zoomed in, pulls back
        # ═════════════════════════════════════════════════════

        # Start zoomed in slightly
        self.camera.frame.set(width=FW * 0.85)

        # -- MAINFRAME logo (actual image) --
        mf_img = ImageMobject(LOGO_PATH)
        mf_img.set_height(2.8)
        mf_img.move_to([-3.2, 0.3, 0])

        mf_text = Text("MAINFRAME", font_size=32, color=MAINFRAME_CYAN, weight=BOLD)
        mf_text.move_to([-3.2, -1.5, 0])
        mf_glow = mf_text.copy().set_opacity(0.3).scale(1.03)

        # -- × symbol --
        collab_x = Text("×", font_size=60, color=WHITE, weight=BOLD)
        collab_x.move_to([0, 0, 0])

        # -- ORBITAL Lissajous --
        _A, _B = 1.3, 0.95
        orb_liss_glow = ParametricFunction(
            lambda t: np.array([_A * np.sin(2 * t) + 3.2, _B * np.sin(3 * t) + 0.3, 0]),
            t_range=[0, TAU, 0.01],
            color=END_CYAN, stroke_width=8, stroke_opacity=0.2
        )
        orb_liss_core = ParametricFunction(
            lambda t: np.array([_A * np.sin(2 * t) + 3.2, _B * np.sin(3 * t) + 0.3, 0]),
            t_range=[0, TAU, 0.01],
            color=END_CYAN, stroke_width=2.5, stroke_opacity=1.0
        )
        orb_text = Text("ORBITAL", font_size=32, color=END_CYAN, weight=BOLD)
        orb_text.move_to([3.2, -1.5, 0])
        orb_glow = orb_text.copy().set_opacity(0.3).scale(1.03)

        # MAINFRAME fades in
        self.play(
            FadeIn(mf_img, shift=RIGHT * 0.3),
            FadeIn(VGroup(mf_glow, mf_text), shift=RIGHT * 0.3),
            run_time=0.8
        )
        self.wait(0.3)

        # × appears
        self.play(FadeIn(collab_x, scale=0.5), run_time=0.3)

        # ORBITAL fades in + camera pulls back to full frame
        self.play(
            Create(orb_liss_core, run_time=0.8),
            FadeIn(orb_liss_glow, run_time=0.6),
            FadeIn(VGroup(orb_glow, orb_text), shift=LEFT * 0.3),
            self.camera.frame.animate.set(width=FW),
            run_time=1.0
        )
        self.wait(0.6)

        # Pulse both
        self.play(
            Flash(mf_img.get_center(), color=MAINFRAME_CYAN, line_length=0.5, num_lines=10, run_time=0.4),
            Circumscribe(orb_liss_core, color=END_CYAN, run_time=0.5),
            collab_x.animate.set_color(VIOLET),
            run_time=0.5
        )
        self.wait(0.5)

        # Grid pulses during transition
        self.play(
            bg_grid.animate.set_opacity(0.35),
            run_time=0.3
        )
        self.play(
            bg_grid.animate.set_opacity(0.15),
            run_time=0.3
        )

        collab_all = Group(mf_img, mf_glow, mf_text, collab_x,
                           orb_liss_glow, orb_liss_core, orb_glow, orb_text)
        self.play(FadeOut(collab_all, shift=UP * 0.5), run_time=0.5)
        self.wait(0.2)

        # ═════════════════════════════════════════════════════
        # ACT 2: TAGLINE SLAM (3s)
        # Camera shifts slightly right for dynamism
        # ═════════════════════════════════════════════════════
        tagline_main = Text("The why behind the math.",
                            font_size=44, color=WHITE, weight=BOLD)
        self.play(
            FadeIn(tagline_main, scale=0.9),
            self.camera.frame.animate.shift(RIGHT * 0.3),
            run_time=0.5
        )
        self.wait(1.2)
        self.play(
            tagline_main.animate.set_color(GREEN),
            Circumscribe(tagline_main, color=GREEN, run_time=0.6),
        )
        self.wait(0.4)
        self.play(
            FadeOut(tagline_main, shift=LEFT * 2),
            self.camera.frame.animate.move_to(ORIGIN),
            run_time=0.4
        )

        # ═════════════════════════════════════════════════════
        # ACT 3: GEAR SHOWCASE (5s)
        # Camera zooms into gears slightly
        # ═════════════════════════════════════════════════════
        g1 = _make_gear(1.2, 14, VIOLET, [-2.0, 0, 0], 0.22, 3)
        g2 = _make_gear(0.85, 10, CYAN, [0.5, 0, 0], 0.18, 3)
        g3 = _make_gear(0.6, 8, ORANGE, [2.3, 0.8, 0], 0.14, 2.5)

        gear_label = Text("Everything connects.", font_size=28, color=WHITE)
        gear_label.set_opacity(0.7).move_to([0, -2.5, 0])

        self.play(
            FadeIn(g1), FadeIn(g2), FadeIn(g3),
            self.camera.frame.animate.set(width=FW * 0.9).shift(UP * 0.3),
            run_time=0.5
        )
        self.play(
            Rotate(g1, PI / 2, about_point=[-2.0, 0, 0]),
            Rotate(g2, -PI / 1.8, about_point=[0.5, 0, 0]),
            Rotate(g3, PI / 1.5, about_point=[2.3, 0.8, 0]),
            FadeIn(gear_label),
            run_time=2.0
        )
        self.wait(0.8)
        self.play(
            Rotate(g1, PI / 3, about_point=[-2.0, 0, 0]),
            Rotate(g2, -PI / 2.5, about_point=[0.5, 0, 0]),
            Rotate(g3, PI / 2, about_point=[2.3, 0.8, 0]),
            run_time=1.2
        )
        self.play(
            FadeOut(VGroup(g1, g2, g3, gear_label)),
            self.camera.frame.animate.set(width=FW).move_to(ORIGIN),
            run_time=0.4
        )

        # ═════════════════════════════════════════════════════
        # ACT 4: FUNCTION MACHINE PIPELINE (7s)
        # Camera pans left-to-right following the number
        # ═════════════════════════════════════════════════════
        m1 = _make_machine("TRIPLE", r"u = 3x", ORANGE, [-3, 0, 0])
        m2 = _make_machine("SQUARE", r"y = u^2", CYAN, [3, 0, 0])
        pipe = Arrow(m1[0].get_right() + RIGHT * 0.1, m2[0].get_left() + LEFT * 0.1,
                     color=WHITE, stroke_width=3, buff=0, max_tip_length_to_length_ratio=0.15)

        # Start camera slightly left
        self.camera.frame.move_to(LEFT * 1.5)
        self.play(FadeIn(m1), run_time=0.3)
        self.play(Create(pipe), run_time=0.3)
        self.play(
            FadeIn(m2),
            self.camera.frame.animate.move_to(ORIGIN),
            run_time=0.4
        )
        self.wait(0.2)

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
        self.play(
            n2_grp.animate.move_to(m1.get_center()),
            self.camera.frame.animate.shift(LEFT * 0.5),
            run_time=0.5
        )
        self.play(
            FadeOut(n2_grp), FadeIn(n6_grp, scale=1.3),
            Flash(m1[0], color=ORANGE, line_length=0.4, num_lines=12, run_time=0.3),
            run_time=0.4
        )
        self.play(
            n6_grp.animate.move_to(pipe.get_center()),
            self.camera.frame.animate.move_to(ORIGIN),
            run_time=0.3
        )
        self.play(
            n6_grp.animate.move_to(m2.get_center()),
            self.camera.frame.animate.shift(RIGHT * 0.5),
            run_time=0.3
        )
        self.play(
            FadeOut(n6_grp), FadeIn(n36_grp, scale=1.3),
            Flash(m2[0], color=CYAN, line_length=0.4, num_lines=12, run_time=0.3),
            run_time=0.4
        )
        self.play(
            n36_grp.animate.move_to([5.5, 0, 0]),
            self.camera.frame.animate.move_to(ORIGIN),
            run_time=0.5
        )

        product = MathTex(r"3 \times 12 = 36", font_size=42, color=WHITE)
        product[0][0].set_color(ORANGE)
        product[0][2:4].set_color(CYAN)
        product[0][5:7].set_color(GREEN)
        product.move_to([0, -2.2, 0])
        self.play(FadeOut(n36_grp), Write(product), run_time=0.5)
        self.wait(0.8)
        self.play(FadeOut(VGroup(m1, m2, pipe, product)), run_time=0.4)

        # ═════════════════════════════════════════════════════
        # ACT 5: RIEMANN SUM — sin(x) above & below (7s)
        # Camera zooms in on the curve
        # ═════════════════════════════════════════════════════
        r_axes = Axes(
            x_range=[0, 2 * PI + 0.5, PI / 2], y_range=[-1.5, 1.5, 0.5],
            x_length=10, y_length=5,
            tips=False,
            axis_config={"color": WHITE, "stroke_width": 1.5, "stroke_opacity": 0.5},
        ).move_to([0, 0, 0])

        # x-axis labels
        x_labels = VGroup(
            MathTex(r"\pi", font_size=18, color=WHITE).set_opacity(0.6).move_to(r_axes.c2p(PI, -0.25)),
            MathTex(r"2\pi", font_size=18, color=WHITE).set_opacity(0.6).move_to(r_axes.c2p(2 * PI, -0.25)),
        )

        r_curve = r_axes.plot(lambda x: np.sin(x), x_range=[0, 2 * PI],
                              color=VIOLET, stroke_width=3)

        curve_label = MathTex(r"f(x) = \sin(x)", font_size=24, color=VIOLET)
        curve_label.move_to([4.0, 2.0, 0])

        # Zoom in slightly
        self.play(
            Create(r_axes, run_time=0.4),
            Create(r_curve, run_time=0.6),
            FadeIn(x_labels),
            FadeIn(curve_label),
            self.camera.frame.animate.set(width=FW * 0.92),
            run_time=0.6
        )

        def _make_sin_rects(n, color_pos=CYAN, color_neg=ORANGE, opacity=0.4):
            rects = VGroup()
            dx = 2 * PI / n
            for i in range(n):
                x_val = i * dx
                y_val = np.sin(x_val + dx / 2)  # midpoint
                rect_h = r_axes.y_length * abs(y_val) / 3.0
                rect_w = r_axes.x_length * dx / (2 * PI + 0.5)
                color = color_pos if y_val >= 0 else color_neg
                rect = Rectangle(
                    width=rect_w, height=rect_h,
                    color=color, fill_color=color, fill_opacity=opacity,
                    stroke_width=1.2,
                )
                # Position: center x at midpoint, bottom at axis (or top at axis for negative)
                cx = r_axes.c2p(x_val + dx / 2, 0)
                if y_val >= 0:
                    rect.move_to(cx + UP * rect_h / 2)
                else:
                    rect.move_to(cx + DOWN * rect_h / 2)
                rects.add(rect)
            return rects

        rects6 = _make_sin_rects(6, CYAN, ORANGE, 0.3)
        rects12 = _make_sin_rects(12, CYAN, ORANGE, 0.35)
        rects24 = _make_sin_rects(24, CYAN, ORANGE, 0.4)

        self.play(FadeIn(rects6), run_time=0.5)
        self.wait(0.5)
        self.play(ReplacementTransform(rects6, rects12), run_time=0.6)
        self.wait(0.5)
        self.play(ReplacementTransform(rects12, rects24), run_time=0.6)
        self.wait(0.6)

        integral_label = MathTex(r"\int_0^{2\pi} \sin(x)\, dx = 0", font_size=30, color=WHITE)
        integral_label.move_to([4.5, -1.8, 0])
        # Color the = 0 green (surprise!)
        integral_label[0][-1].set_color(GREEN)

        self.play(Write(integral_label), run_time=0.5)
        self.wait(0.5)

        # Grid pulse during transition
        self.play(
            bg_grid.animate.set_opacity(0.3),
            run_time=0.2
        )

        self.play(
            FadeOut(VGroup(r_axes, r_curve, rects24, integral_label, x_labels, curve_label)),
            bg_grid.animate.set_opacity(0.15),
            self.camera.frame.animate.set(width=FW).move_to(ORIGIN),
            run_time=0.4
        )

        # ═════════════════════════════════════════════════════
        # ACT 6: GRAPH + TANGENT LINE (6s)
        # Camera tracks the dot as it slides
        # ═════════════════════════════════════════════════════
        axes = Axes(
            x_range=[-1, 5, 1], y_range=[-1, 8, 2],
            x_length=8, y_length=5, tips=False,
            axis_config={"color": WHITE, "stroke_width": 1.5, "stroke_opacity": 0.5},
        ).move_to([0, 0.2, 0])

        curve = axes.plot(lambda x: 0.3 * x ** 2 + 0.5, x_range=[0, 4.5],
                          color=VIOLET, stroke_width=3)
        c_label = MathTex(r"f(x) = 0.3x^2 + 0.5", font_size=22, color=VIOLET)
        c_label.next_to(curve, UR, buff=0.3)

        self.play(Create(axes, run_time=0.5), Create(curve, run_time=0.8))
        self.play(FadeIn(c_label), run_time=0.3)

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

        # Camera follows the dot's horizontal position slightly
        self.play(
            x_tracker.animate.set_value(4.0),
            self.camera.frame.animate.shift(RIGHT * 0.6 + UP * 0.4),
            run_time=3.0, rate_func=smooth
        )
        self.wait(0.3)
        self.play(
            x_tracker.animate.set_value(2.0),
            self.camera.frame.animate.move_to(ORIGIN),
            run_time=1.5, rate_func=smooth
        )
        self.wait(0.2)
        self.play(FadeOut(VGroup(axes, curve, c_label, tangent, dot)), run_time=0.4)

        # ═════════════════════════════════════════════════════
        # ACT 7: ALGEBRA CASCADE (5s)
        # Camera shifts down following the steps
        # ═════════════════════════════════════════════════════
        steps = [
            r"x^2 + 6x + 9 = 0",
            r"(x + 3)^2 = 0",
            r"x + 3 = 0",
            r"x = -3",
        ]
        colors = [WHITE, CYAN, CYAN, GREEN]
        y_positions = [1.5, 0.5, -0.5, -1.5]

        step_mobs = []
        for j, (s, c, yp) in enumerate(zip(steps, colors, y_positions)):
            eq = MathTex(s, font_size=48, color=c)
            eq.move_to([0, yp, 0])
            eq.set_opacity(0)
            step_mobs.append(eq)

        # Reveal one by one with camera tracking down
        for j, eq in enumerate(step_mobs):
            anims = [eq.animate.set_opacity(1)]
            if j > 0:
                anims.append(self.camera.frame.animate.shift(DOWN * 0.25))
            self.play(*anims, run_time=0.4)
            self.wait(0.4)

        answer_box = SurroundingRectangle(
            step_mobs[-1], color=GREEN, fill_color=BOX_FILL,
            fill_opacity=0.6, buff=0.2, corner_radius=0.1, stroke_width=2.5,
        )
        self.play(Create(answer_box), run_time=0.3)
        self.play(Circumscribe(answer_box, color=GREEN, run_time=0.5))
        self.wait(0.4)

        self.play(
            *[FadeOut(m) for m in step_mobs],
            FadeOut(answer_box),
            self.camera.frame.animate.move_to(ORIGIN),
            run_time=0.4
        )

        # ═════════════════════════════════════════════════════
        # ACT 8: TOPIC GRID — 9 COURSES (6s)
        # Camera pulls back to reveal full grid
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
            txt = Text(topic, font_size=24, color=color, weight=BOLD)
            box = SurroundingRectangle(txt, color=color, fill_color=BOX_FILL,
                                       fill_opacity=0.5, buff=0.18, corner_radius=0.08,
                                       stroke_width=2)
            card = VGroup(box, txt)
            grid.add(card)

        grid.arrange_in_grid(rows=3, cols=3, buff=0.4)
        grid.move_to([0, 0, 0])

        # Start zoomed in, pull back as cards appear
        self.camera.frame.set(width=FW * 0.7)
        for i, card in enumerate(grid):
            anims = [FadeIn(card, scale=0.8)]
            if i == 2:
                anims.append(self.camera.frame.animate.set(width=FW * 0.85))
            elif i == 5:
                anims.append(self.camera.frame.animate.set(width=FW * 0.95))
            elif i == 8:
                anims.append(self.camera.frame.animate.set(width=FW))
            self.play(*anims, run_time=0.18)
            self.wait(0.08)

        self.wait(1.0)

        # All cards pulse with grid flash
        self.play(
            *[Indicate(card, color=card[1].color, scale_factor=1.05) for card in grid],
            bg_grid.animate.set_opacity(0.4),
            run_time=0.6
        )
        self.play(bg_grid.animate.set_opacity(0.15), run_time=0.3)
        self.wait(0.3)
        self.play(FadeOut(grid), run_time=0.4)

        # ═════════════════════════════════════════════════════
        # ACT 9: SUBSCRIBE CTA (5s)
        # ═════════════════════════════════════════════════════
        self.camera.frame.set(width=FW).move_to(ORIGIN)

        cta_line1 = Text("Watch it click.",
                         font_size=44, color=WHITE, weight=BOLD)
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
        # END CARD: Lissajous + wordmark + tagline
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
