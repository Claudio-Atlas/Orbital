"""
Meridian Press × Orbital — District Promo V2 (16:9 Landscape)
=============================================================
FULL production quality. Includes:
  - Meridian × Orbital collab intro
  - Animated background grid (persistent)
  - Camera movements (MovingCameraScene)
  - Gear showcase, Riemann sums, tangent lines, algebra cascades
  - Four pillars, AI tutor demo, teacher dashboard
  - Course spectrum, comparison, emotional closer
  - End card with Lissajous

Audio: ~85s at Hale locked settings (speed 0.8)
  Section 1 (0-18s): "Every student...catching up" → Acts 1+2
  Section 2 (18-27s): "We built Meridian...fix that" + intro to pillars → Act 3
  Section 3 (27-44s): "Complete programs...EVERY student" → Act 4 (pillars + math showcase)
  Section 4 (44-55s): "When student gets stuck...cracks" → Act 5 (AI tutor)
  Section 5 (55-65s): "Teachers get dashboards...unit" → Act 6 (dashboard)
  Section 6 (65-73s): "Pre-Algebra through Calculus...platform" + "Not bolted on" → Acts 7+8
  Section 7 (73-80s): "Because every student..." → Act 9
  Section 8 (80-85s): "Meridian Press. Mathematics for every student." → Act 10

Render:
  cd ~/Desktop/Orbital/orbital_factory && source venv/bin/activate
  PATH="/Library/TeX/texbin:$PATH" manim render prototypes/meridian_promo_v2.py MeridianPromoV2 \
    -o meridian_promo_v2.mp4 --format mp4 -r 1920,1080 --frame_rate 60 --flush_cache
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
MERIDIAN_BLUE = "#3B82F6"
MERIDIAN_TEAL = "#14B8A6"
WARM_WHITE = "#F8FAFC"
BOX_FILL = "#1a1130"
GRID_COLOR = "#1a1a3a"
END_CYAN = "#00E5FF"
SOFT_RED = "#EF4444"
FW = 14.2
FH = 8.0


def _make_bg_grid(fw=20, fh=14, spacing=0.8, color=GRID_COLOR, sw=0.5, opacity=0.15):
    lines = VGroup()
    x = -fw / 2
    while x <= fw / 2:
        lines.add(Line([x, -fh / 2, 0], [x, fh / 2, 0], color=color,
                       stroke_width=sw, stroke_opacity=opacity))
        x += spacing
    y = -fh / 2
    while y <= fh / 2:
        lines.add(Line([-fw / 2, y, 0], [fw / 2, y, 0], color=color,
                       stroke_width=sw, stroke_opacity=opacity))
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


class MeridianPromoV2(MovingCameraScene):
    def construct(self):
        self.camera.background_color = BLACK
        self.camera.frame.set(width=FW, height=FH)

        # ── Persistent background grid ──
        bg_grid = _make_bg_grid()
        self.add(bg_grid)

        # ── Camera-following border ──
        def _get_border():
            cf = self.camera.frame
            w = cf.width - 0.2
            h = cf.height - 0.2
            return Rectangle(width=w, height=h, color=MERIDIAN_BLUE,
                             stroke_width=2.5, stroke_opacity=0.6,
                             fill_opacity=0).move_to(cf.get_center())

        def _get_border_glow():
            cf = self.camera.frame
            w = cf.width - 0.15
            h = cf.height - 0.15
            return Rectangle(width=w, height=h, color=MERIDIAN_BLUE,
                             stroke_width=6, stroke_opacity=0.12,
                             fill_opacity=0).move_to(cf.get_center())

        def _get_watermark():
            cf = self.camera.frame
            cx, cy = cf.get_center()[0], cf.get_center()[1]
            hw, hh = cf.width / 2, cf.height / 2
            t = Text("MERIDIAN × ORBITAL", font_size=12, color=WHITE, weight=BOLD)
            t.set_opacity(0.3)
            t.move_to([cx - hw + 1.0, cy - hh + 0.25, 0])
            return t

        border = always_redraw(_get_border)
        border_glow = always_redraw(_get_border_glow)
        wm = always_redraw(_get_watermark)
        self.add(border_glow, border, wm)

        # ═════════════════════════════════════════════
        # ACT 0: MERIDIAN × ORBITAL COLLAB INTRO (5s)
        # ═════════════════════════════════════════════
        self.camera.frame.set(width=FW * 0.85)

        # MERIDIAN text logo (left)
        mer_text = Text("MERIDIAN", font_size=42, color=MERIDIAN_BLUE, weight=BOLD)
        mer_sub = Text("P R E S S", font_size=14, color=MERIDIAN_TEAL, weight=BOLD)
        mer_sub.set_opacity(0.7)
        mer_text.move_to([-3.2, 0.2, 0])
        mer_sub.next_to(mer_text, DOWN, buff=0.15)
        mer_glow = mer_text.copy().set_opacity(0.25).scale(1.03)

        # × symbol
        collab_x = Text("×", font_size=60, color=WHITE, weight=BOLD)
        collab_x.move_to([0, 0.1, 0])

        # ORBITAL Lissajous (right)
        _A, _B = 1.1, 0.8
        orb_liss_glow = ParametricFunction(
            lambda t: np.array([_A * np.sin(2 * t) + 3.2, _B * np.sin(3 * t) + 0.2, 0]),
            t_range=[0, TAU, 0.01],
            color=END_CYAN, stroke_width=8, stroke_opacity=0.2
        )
        orb_liss_core = ParametricFunction(
            lambda t: np.array([_A * np.sin(2 * t) + 3.2, _B * np.sin(3 * t) + 0.2, 0]),
            t_range=[0, TAU, 0.01],
            color=END_CYAN, stroke_width=2.5, stroke_opacity=1.0
        )
        orb_text = Text("ORBITAL", font_size=42, color=END_CYAN, weight=BOLD)
        orb_text.move_to([3.2, -1.3, 0])
        orb_glow = orb_text.copy().set_opacity(0.25).scale(1.03)

        # Fade in Meridian
        self.play(
            FadeIn(VGroup(mer_glow, mer_text), shift=RIGHT * 0.3),
            FadeIn(mer_sub, shift=RIGHT * 0.3),
            run_time=0.8
        )
        self.wait(0.3)
        self.play(FadeIn(collab_x, scale=0.5), run_time=0.3)

        # Orbital fades in + camera pulls back
        self.play(
            Create(orb_liss_core, run_time=0.8),
            FadeIn(orb_liss_glow, run_time=0.6),
            FadeIn(VGroup(orb_glow, orb_text), shift=LEFT * 0.3),
            self.camera.frame.animate.set(width=FW),
            run_time=1.0
        )
        self.wait(0.5)

        # Flash both
        self.play(
            Flash(mer_text.get_center(), color=MERIDIAN_BLUE, line_length=0.5, num_lines=10, run_time=0.4),
            Circumscribe(orb_liss_core, color=END_CYAN, run_time=0.5),
            collab_x.animate.set_color(VIOLET),
            run_time=0.5
        )

        # Grid pulse
        self.play(bg_grid.animate.set_opacity(0.35), run_time=0.2)
        self.play(bg_grid.animate.set_opacity(0.15), run_time=0.2)
        self.wait(0.3)

        collab_all = Group(mer_glow, mer_text, mer_sub, collab_x,
                           orb_liss_glow, orb_liss_core, orb_glow, orb_text)
        self.play(FadeOut(collab_all, shift=UP * 0.5), run_time=0.5)

        # ═════════════════════════════════════════════
        # ACT 1: DIFFERENT PACES — 3 students (0-10s audio)
        # "Every student learns at a different pace.
        #  The problem is, most math programs don't."
        # ═════════════════════════════════════════════

        # Number line with student dots
        line = Line([-5.5, 0, 0], [5.5, 0, 0], color=WHITE, stroke_width=2, stroke_opacity=0.4)
        ticks = VGroup()
        for x in range(-5, 6):
            ticks.add(Line([x, -0.12, 0], [x, 0.12, 0], color=WHITE, stroke_width=1.5, stroke_opacity=0.3))

        dot_fast = Dot([-4.5, 0, 0], color=GREEN, radius=0.18).set_glow_factor(0.8)
        dot_mid = Dot([-4.5, 0, 0], color=MERIDIAN_BLUE, radius=0.18).set_glow_factor(0.8)
        dot_slow = Dot([-4.5, 0, 0], color=ORANGE, radius=0.18).set_glow_factor(0.8)

        l_fast = Text("Student A", font_size=18, color=GREEN, weight=BOLD).next_to(dot_fast, UP, buff=0.3)
        l_mid = Text("Student B", font_size=18, color=MERIDIAN_BLUE, weight=BOLD).next_to(dot_mid, UP, buff=0.6)
        l_slow = Text("Student C", font_size=18, color=ORANGE, weight=BOLD).next_to(dot_slow, UP, buff=0.9)

        self.play(Create(line), FadeIn(ticks), run_time=0.6)
        self.play(FadeIn(dot_fast), FadeIn(dot_mid), FadeIn(dot_slow),
                  FadeIn(l_fast), FadeIn(l_mid), FadeIn(l_slow), run_time=0.5)

        self.play(
            dot_fast.animate.move_to([4.5, 0, 0]),
            dot_mid.animate.move_to([1.5, 0, 0]),
            dot_slow.animate.move_to([-1.0, 0, 0]),
            l_fast.animate.move_to([4.5, 0.48, 0]),
            l_mid.animate.move_to([1.5, 0.78, 0]),
            l_slow.animate.move_to([-1.0, 1.08, 0]),
            run_time=3.5, rate_func=smooth
        )
        self.wait(0.8)

        # Curriculum pace line sweeps
        pace = DashedLine([-4, -1.5, 0], [-4, 1.5, 0], color=SOFT_RED,
                          stroke_width=3, dash_length=0.15)
        pace_lbl = Text("Curriculum Pace", font_size=18, color=SOFT_RED, weight=BOLD)
        pace_lbl.next_to(pace, DOWN, buff=0.2)

        self.play(FadeIn(pace), FadeIn(pace_lbl), run_time=0.4)
        self.play(
            pace.animate.move_to([1.5, 0, 0]),
            pace_lbl.animate.move_to([1.5, -1.7, 0]),
            run_time=2.5, rate_func=linear
        )

        x_mark = Text("✗", font_size=36, color=SOFT_RED, weight=BOLD)
        x_mark.move_to(dot_slow.get_center() + DOWN * 0.5)
        self.play(FadeIn(x_mark, scale=1.5), run_time=0.4)
        self.wait(1.5)

        act1 = VGroup(line, ticks, dot_fast, dot_mid, dot_slow,
                       l_fast, l_mid, l_slow, pace, pace_lbl, x_mark)
        self.play(FadeOut(act1, shift=UP * 0.5), run_time=0.5)

        # ═════════════════════════════════════════════
        # ACT 2: ONE TEXTBOOK, ONE SPEED (10-18s audio)
        # + Gear showcase showing "everything connects"
        # ═════════════════════════════════════════════

        steps = VGroup()
        step_labels = ["1.1", "1.2", "1.3", "1.4", "1.5"]
        for i, label in enumerate(step_labels):
            x = -4 + i * 2
            box = RoundedRectangle(width=1.4, height=0.8, corner_radius=0.08,
                                   color=WHITE, fill_color=BOX_FILL, fill_opacity=0.6,
                                   stroke_width=2, stroke_opacity=0.6)
            txt = Text(label, font_size=22, color=WHITE)
            steps.add(VGroup(box, txt).move_to([x, 0.5, 0]))

        arrows = VGroup()
        for i in range(len(steps) - 1):
            arrows.add(Arrow(steps[i].get_right(), steps[i + 1].get_left(),
                             color=WHITE, stroke_width=2, stroke_opacity=0.4,
                             buff=0.1, max_tip_length_to_length_ratio=0.2))

        self.play(*[FadeIn(s, shift=UP * 0.2) for s in steps], run_time=0.6)
        self.play(*[Create(a) for a in arrows], run_time=0.4)
        self.wait(0.6)

        # Step 1.3 goes red — missed
        missed = steps[2]
        self.play(
            missed[0].animate.set_color(SOFT_RED).set_fill(SOFT_RED, 0.3),
            missed[1].animate.set_color(SOFT_RED),
            Flash(missed.get_center(), color=SOFT_RED, line_length=0.4, num_lines=8),
            run_time=0.5
        )
        self.play(
            steps[3].animate.set_opacity(0.2), steps[4].animate.set_opacity(0.2),
            arrows[2].animate.set_opacity(0.1), arrows[3].animate.set_opacity(0.1),
            run_time=0.8
        )

        gap_text = Text("?", font_size=48, color=SOFT_RED, weight=BOLD)
        gap_text.move_to(missed.get_center())
        self.play(FadeIn(gap_text, scale=0.5), FadeOut(missed[1]), run_time=0.5)
        self.wait(2.5)

        self.play(FadeOut(VGroup(steps, arrows, gap_text)), run_time=0.4)

        # ═════════════════════════════════════════════
        # ACT 3: MERIDIAN REVEAL + GEAR SHOWCASE (18-27s)
        # "We built Meridian to fix that."
        # ═════════════════════════════════════════════

        mer_reveal = Text("MERIDIAN", font_size=64, color=MERIDIAN_BLUE, weight=BOLD)
        mer_reveal_sub = Text("P R E S S", font_size=20, color=WARM_WHITE, weight=BOLD)
        mer_reveal_sub.set_opacity(0.7).next_to(mer_reveal, DOWN, buff=0.2)
        logo_grp = VGroup(mer_reveal, mer_reveal_sub).move_to(ORIGIN)

        self.play(FadeIn(mer_reveal, scale=0.95), run_time=0.6)
        self.play(FadeIn(mer_reveal_sub, shift=UP * 0.1), run_time=0.3)
        self.play(
            Circumscribe(mer_reveal, color=MERIDIAN_BLUE, run_time=0.6),
            bg_grid.animate.set_opacity(0.3),
            run_time=0.6
        )
        self.play(bg_grid.animate.set_opacity(0.15), run_time=0.3)
        self.wait(0.5)
        self.play(FadeOut(logo_grp, shift=UP * 0.3), run_time=0.4)

        # Gears — "everything connects"
        g1 = _make_gear(1.2, 14, MERIDIAN_BLUE, [-2.0, 0, 0], 0.22, 3)
        g2 = _make_gear(0.85, 10, MERIDIAN_TEAL, [0.5, 0, 0], 0.18, 3)
        g3 = _make_gear(0.6, 8, ORANGE, [2.3, 0.8, 0], 0.14, 2.5)

        gear_label = Text("Everything connects.", font_size=28, color=WHITE)
        gear_label.set_opacity(0.7).move_to([0, -2.5, 0])

        self.play(FadeIn(g1), FadeIn(g2), FadeIn(g3),
                  self.camera.frame.animate.set(width=FW * 0.9).shift(UP * 0.3),
                  run_time=0.5)
        self.play(
            Rotate(g1, PI / 2, about_point=[-2.0, 0, 0]),
            Rotate(g2, -PI / 1.8, about_point=[0.5, 0, 0]),
            Rotate(g3, PI / 1.5, about_point=[2.3, 0.8, 0]),
            FadeIn(gear_label),
            run_time=2.0
        )
        self.wait(0.5)
        self.play(
            FadeOut(VGroup(g1, g2, g3, gear_label)),
            self.camera.frame.animate.set(width=FW).move_to(ORIGIN),
            run_time=0.4
        )

        # ═════════════════════════════════════════════
        # ACT 4: FOUR PILLARS + MATH SHOWCASE (27-44s)
        # "Complete math programs with digital textbooks,
        #  video walkthroughs, thousands of practice
        #  problems, and a personal AI tutor..."
        # ═════════════════════════════════════════════

        pillars = [
            ("📖", "Digital\nTextbook", MERIDIAN_BLUE),
            ("🎬", "Video\nLessons", VIOLET),
            ("✏️", "Practice\nProblems", ORANGE),
            ("🤖", "AI\nTutor", MERIDIAN_TEAL),
        ]

        pillar_grp = VGroup()
        for emoji_str, label, color in pillars:
            box = RoundedRectangle(width=2.4, height=2.8, corner_radius=0.12,
                                   color=color, fill_color=BOX_FILL, fill_opacity=0.7,
                                   stroke_width=2.5)
            icon = Text(emoji_str, font_size=48).move_to(box.get_center() + UP * 0.5)
            lbl = Text(label, font_size=20, color=color, weight=BOLD).move_to(box.get_center() + DOWN * 0.5)
            pillar_grp.add(VGroup(box, icon, lbl))

        pillar_grp.arrange(RIGHT, buff=0.5).move_to(ORIGIN)

        for card in pillar_grp:
            self.play(FadeIn(card, shift=UP * 0.3, scale=0.9), run_time=0.5)
            self.wait(0.3)

        connect_line = Line(pillar_grp[0].get_bottom() + DOWN * 0.3,
                            pillar_grp[-1].get_bottom() + DOWN * 0.3,
                            color=MERIDIAN_TEAL, stroke_width=3)
        connect_label = Text("One Platform", font_size=22, color=MERIDIAN_TEAL, weight=BOLD)
        connect_label.next_to(connect_line, DOWN, buff=0.15)

        self.play(Create(connect_line), FadeIn(connect_label), run_time=0.5)
        self.wait(0.8)
        self.play(
            *[Indicate(card, color=card[0].color, scale_factor=1.03) for card in pillar_grp],
            run_time=0.5
        )
        self.wait(0.3)
        self.play(FadeOut(VGroup(pillar_grp, connect_line, connect_label)), run_time=0.4)

        # ── MATH SHOWCASE: Riemann Sum (shows off our rendering) ──
        r_axes = Axes(
            x_range=[0, 2 * PI + 0.5, PI / 2], y_range=[-1.5, 1.5, 0.5],
            x_length=10, y_length=5, tips=False,
            axis_config={"color": WHITE, "stroke_width": 1.5, "stroke_opacity": 0.5},
        )
        r_curve = r_axes.plot(lambda x: np.sin(x), x_range=[0, 2 * PI],
                              color=VIOLET, stroke_width=3)
        curve_label = MathTex(r"f(x) = \sin(x)", font_size=24, color=VIOLET)
        curve_label.move_to([4.0, 2.0, 0])

        self.play(Create(r_axes, run_time=0.4), Create(r_curve, run_time=0.6),
                  FadeIn(curve_label),
                  self.camera.frame.animate.set(width=FW * 0.92),
                  run_time=0.6)

        def _make_sin_rects(n, color_pos=CYAN, color_neg=ORANGE, opacity=0.4):
            rects = VGroup()
            dx = 2 * PI / n
            for i in range(n):
                x_val = i * dx
                y_val = np.sin(x_val + dx / 2)
                rect_h = r_axes.y_length * abs(y_val) / 3.0
                rect_w = r_axes.x_length * dx / (2 * PI + 0.5)
                color = color_pos if y_val >= 0 else color_neg
                rect = Rectangle(width=rect_w, height=rect_h, color=color,
                                 fill_color=color, fill_opacity=opacity, stroke_width=1.2)
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

        self.play(FadeIn(rects6), run_time=0.4)
        self.wait(0.3)
        self.play(ReplacementTransform(rects6, rects12), run_time=0.5)
        self.wait(0.3)
        self.play(ReplacementTransform(rects12, rects24), run_time=0.5)
        self.wait(0.5)

        self.play(
            FadeOut(VGroup(r_axes, r_curve, rects24, curve_label)),
            self.camera.frame.animate.set(width=FW).move_to(ORIGIN),
            run_time=0.4
        )

        # ═════════════════════════════════════════════
        # ACT 5: AI TUTOR + TANGENT LINE (44-55s)
        # "When a student gets stuck..."
        # ═════════════════════════════════════════════

        problem = MathTex(r"3x + 7 = 22", font_size=52, color=WHITE).move_to([0, 2.5, 0])
        prob_label = Text("Student is stuck:", font_size=18, color=ORANGE)
        prob_label.set_opacity(0.7).next_to(problem, UP, buff=0.3)

        self.play(FadeIn(prob_label), Write(problem), run_time=0.6)
        self.wait(0.4)

        bubble_bg = RoundedRectangle(width=8, height=4.5, corner_radius=0.15,
                                      color=MERIDIAN_TEAL, fill_color=BOX_FILL,
                                      fill_opacity=0.8, stroke_width=2).move_to([0, -0.8, 0])

        ai_label = Text("AI Tutor", font_size=16, color=MERIDIAN_TEAL, weight=BOLD)
        ai_label.move_to(bubble_bg.get_top() + DOWN * 0.3 + LEFT * 2.5)

        msg1 = Text("What operation undoes adding 7?", font_size=20, color=WARM_WHITE)
        msg1.move_to(bubble_bg.get_center() + UP * 0.8 + LEFT * 0.5)

        step1 = MathTex(r"3x + 7 - 7 = 22 - 7", font_size=36, color=CYAN)
        step1.move_to(bubble_bg.get_center() + UP * 0.1)

        step2 = MathTex(r"3x = 15", font_size=36, color=CYAN)
        step2.move_to(bubble_bg.get_center() + DOWN * 0.6)

        msg2 = Text("Now divide both sides by 3!", font_size=20, color=WARM_WHITE)
        msg2.move_to(bubble_bg.get_center() + DOWN * 1.3)

        step3 = MathTex(r"x = 5", font_size=44, color=GREEN)
        step3.move_to(bubble_bg.get_center() + DOWN * 2.0)

        self.play(FadeIn(bubble_bg), FadeIn(ai_label), run_time=0.4)
        self.play(FadeIn(msg1, shift=LEFT * 0.3), run_time=0.4)
        self.wait(0.4)
        self.play(Write(step1), run_time=0.6)
        self.wait(0.3)
        self.play(Write(step2), run_time=0.4)
        self.play(FadeIn(msg2, shift=LEFT * 0.3), run_time=0.4)
        self.wait(0.3)
        self.play(Write(step3),
                  Flash(step3.get_center(), color=GREEN, line_length=0.5, num_lines=10),
                  run_time=0.5)

        answer_box = SurroundingRectangle(step3, color=GREEN, fill_color=GREEN,
                                           fill_opacity=0.1, buff=0.15, corner_radius=0.08, stroke_width=2)
        self.play(Create(answer_box), run_time=0.3)
        self.wait(0.8)

        self.play(FadeOut(VGroup(problem, prob_label, bubble_bg, ai_label,
                                 msg1, step1, step2, msg2, step3, answer_box)), run_time=0.4)

        # ── TANGENT LINE showcase (shows off our scene generators) ──
        axes = Axes(
            x_range=[-1, 5, 1], y_range=[-1, 8, 2],
            x_length=8, y_length=5, tips=False,
            axis_config={"color": WHITE, "stroke_width": 1.5, "stroke_opacity": 0.5},
        ).move_to([0, 0.2, 0])

        curve = axes.plot(lambda x: 0.3 * x ** 2 + 0.5, x_range=[0, 4.5],
                          color=VIOLET, stroke_width=3)
        c_label = MathTex(r"f(x) = 0.3x^2 + 0.5", font_size=22, color=VIOLET)
        c_label.next_to(curve, UR, buff=0.3)

        self.play(Create(axes, run_time=0.4), Create(curve, run_time=0.6))
        self.play(FadeIn(c_label), run_time=0.2)

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

        self.play(x_tracker.animate.set_value(4.0),
                  self.camera.frame.animate.shift(RIGHT * 0.5 + UP * 0.3),
                  run_time=2.0, rate_func=smooth)
        self.play(x_tracker.animate.set_value(2.0),
                  self.camera.frame.animate.move_to(ORIGIN),
                  run_time=1.0, rate_func=smooth)
        self.play(FadeOut(VGroup(axes, curve, c_label, tangent, dot)), run_time=0.3)

        # ═════════════════════════════════════════════
        # ACT 6: TEACHER DASHBOARD (55-65s)
        # "Teachers get real-time dashboards..."
        # ═════════════════════════════════════════════

        dash_title = Text("Teacher Dashboard", font_size=28, color=MERIDIAN_BLUE, weight=BOLD)
        dash_title.move_to([0, 3.2, 0])

        students = ["Alex", "Maria", "James", "Sofia", "Tyler"]
        progress = [0.92, 0.78, 0.45, 0.88, 0.31]
        colors_p = [GREEN, MERIDIAN_TEAL, ORANGE, MERIDIAN_TEAL, SOFT_RED]

        bars = VGroup()
        names = VGroup()
        pcts = VGroup()
        for i, (name, prog, col) in enumerate(zip(students, progress, colors_p)):
            x = -4 + i * 2
            bar_h = prog * 4
            bar = Rectangle(width=1.2, height=bar_h, color=col,
                             fill_color=col, fill_opacity=0.5, stroke_width=2)
            bar.move_to([x, -1.5 + bar_h / 2, 0])
            n = Text(name, font_size=14, color=WHITE).set_opacity(0.7).move_to([x, -2.0, 0])
            p = Text(f"{int(prog * 100)}%", font_size=16, color=col, weight=BOLD)
            p.next_to(bar, UP, buff=0.1)
            bars.add(bar)
            names.add(n)
            pcts.add(p)

        self.play(FadeIn(dash_title), run_time=0.3)
        self.play(*[GrowFromEdge(bar, DOWN) for bar in bars], run_time=0.8)
        self.play(FadeIn(names), FadeIn(pcts), run_time=0.4)
        self.wait(0.5)

        alert_james = SurroundingRectangle(VGroup(bars[2], names[2]),
                                            color=ORANGE, stroke_width=2.5, buff=0.1)
        alert_tyler = SurroundingRectangle(VGroup(bars[4], names[4]),
                                            color=SOFT_RED, stroke_width=2.5, buff=0.1)
        needs_help = Text("Needs attention", font_size=16, color=SOFT_RED, weight=BOLD)
        needs_help.move_to([3, 2.5, 0])
        arrow_j = Arrow(needs_help.get_left(), bars[2].get_top() + UP * 0.4,
                         color=ORANGE, stroke_width=2, buff=0.1)
        arrow_t = Arrow(needs_help.get_right() + DOWN * 0.1, bars[4].get_top() + UP * 0.4,
                         color=SOFT_RED, stroke_width=2, buff=0.1)

        self.play(Create(alert_james), Create(alert_tyler),
                  FadeIn(needs_help), Create(arrow_j), Create(arrow_t), run_time=0.6)
        self.wait(2.0)

        self.play(FadeOut(VGroup(dash_title, bars, names, pcts,
                                 alert_james, alert_tyler, needs_help, arrow_j, arrow_t)), run_time=0.4)

        # ═════════════════════════════════════════════
        # ACT 7: COURSE SPECTRUM + ALGEBRA CASCADE (65-73s)
        # "Pre-Algebra through Calculus."
        # "Not a textbook with a website bolted on."
        # ═════════════════════════════════════════════

        courses = [
            ("Pre-Algebra", "#6366F1"), ("Algebra 1", "#8B5CF6"),
            ("Geometry", "#A855F7"), ("Algebra 2", "#C084FC"),
            ("Precalculus", MERIDIAN_TEAL), ("Calculus", MERIDIAN_BLUE),
        ]

        course_cards = VGroup()
        for name, color in courses:
            box = RoundedRectangle(width=1.8, height=1.0, corner_radius=0.08,
                                   color=color, fill_color=BOX_FILL, fill_opacity=0.6, stroke_width=2.5)
            txt = Text(name, font_size=14, color=color, weight=BOLD).move_to(box.get_center())
            course_cards.add(VGroup(box, txt))

        course_cards.arrange(RIGHT, buff=0.25).move_to([0, 0.5, 0])

        c_arrows = VGroup()
        for i in range(len(course_cards) - 1):
            c_arrows.add(Arrow(course_cards[i].get_right(), course_cards[i + 1].get_left(),
                               color=WHITE, stroke_width=1.5, stroke_opacity=0.4,
                               buff=0.05, max_tip_length_to_length_ratio=0.3))

        platform_line = Line(course_cards[0].get_bottom() + DOWN * 0.5,
                             course_cards[-1].get_bottom() + DOWN * 0.5,
                             color=MERIDIAN_TEAL, stroke_width=3)
        platform_text = Text("ONE PLATFORM", font_size=22, color=MERIDIAN_TEAL, weight=BOLD)
        platform_text.next_to(platform_line, DOWN, buff=0.15)

        for i, card in enumerate(course_cards):
            anims = [FadeIn(card, shift=RIGHT * 0.2, scale=0.9)]
            if i > 0:
                anims.append(Create(c_arrows[i - 1]))
            self.play(*anims, run_time=0.2)

        self.play(Create(platform_line), FadeIn(platform_text), run_time=0.4)
        self.wait(0.5)
        self.play(*[Indicate(card, color=card[0].color, scale_factor=1.05) for card in course_cards],
                  run_time=0.5)
        self.wait(0.3)
        self.play(FadeOut(VGroup(course_cards, c_arrows, platform_line, platform_text)), run_time=0.4)

        # ── ALGEBRA CASCADE (shows off our algebra solver scene) ──
        alg_steps = [r"x^2 + 6x + 9 = 0", r"(x + 3)^2 = 0", r"x + 3 = 0", r"x = -3"]
        alg_colors = [WHITE, CYAN, CYAN, GREEN]
        alg_y = [1.5, 0.5, -0.5, -1.5]

        step_mobs = []
        for s, c, yp in zip(alg_steps, alg_colors, alg_y):
            eq = MathTex(s, font_size=48, color=c).move_to([0, yp, 0]).set_opacity(0)
            step_mobs.append(eq)

        for j, eq in enumerate(step_mobs):
            anims = [eq.animate.set_opacity(1)]
            if j > 0:
                anims.append(self.camera.frame.animate.shift(DOWN * 0.2))
            self.play(*anims, run_time=0.35)
            self.wait(0.2)

        alg_box = SurroundingRectangle(step_mobs[-1], color=GREEN, fill_color=BOX_FILL,
                                        fill_opacity=0.6, buff=0.2, corner_radius=0.1, stroke_width=2.5)
        self.play(Create(alg_box), run_time=0.3)
        self.play(Circumscribe(alg_box, color=GREEN, run_time=0.4))
        self.wait(0.3)

        self.play(*[FadeOut(m) for m in step_mobs], FadeOut(alg_box),
                  self.camera.frame.animate.move_to(ORIGIN), run_time=0.4)

        # ═════════════════════════════════════════════
        # ACT 8: COMPARISON — Traditional vs Meridian (quick)
        # ═════════════════════════════════════════════

        self.camera.frame.set(width=FW).move_to(ORIGIN)

        old_label = Text("Traditional", font_size=22, color=SOFT_RED, weight=BOLD).move_to([-3.5, 3.0, 0])
        old_items = [("Textbook", "#555"), ("Website", "#555"),
                     ("Videos", "#555"), ("Grading", "#555")]
        old_boxes = VGroup()
        for i, (name, col) in enumerate(old_items):
            box = RoundedRectangle(width=2.2, height=0.7, corner_radius=0.06,
                                   color=col, fill_color="#111", fill_opacity=0.5, stroke_width=1.5)
            txt = Text(name, font_size=16, color="#888")
            grp = VGroup(box, txt).move_to([-3.5, 1.5 - i * 1.0, 0])
            old_boxes.add(grp)
        old_boxes[1].shift(RIGHT * 0.3)
        old_boxes[3].shift(LEFT * 0.2)

        new_label = Text("Meridian", font_size=22, color=MERIDIAN_TEAL, weight=BOLD).move_to([3.5, 3.0, 0])
        new_items = [("Textbook", MERIDIAN_BLUE), ("Videos", VIOLET),
                     ("Problems", ORANGE), ("AI Tutor", MERIDIAN_TEAL)]
        new_boxes = VGroup()
        for i, (name, col) in enumerate(new_items):
            box = RoundedRectangle(width=2.2, height=0.7, corner_radius=0.06,
                                   color=col, fill_color=BOX_FILL, fill_opacity=0.6, stroke_width=2.5)
            txt = Text(name, font_size=16, color=col, weight=BOLD)
            new_boxes.add(VGroup(box, txt).move_to([3.5, 1.5 - i * 1.0, 0]))

        new_connections = VGroup()
        for i in range(len(new_boxes) - 1):
            new_connections.add(Line(new_boxes[i].get_bottom(), new_boxes[i + 1].get_top(),
                                     color=MERIDIAN_TEAL, stroke_width=2, stroke_opacity=0.6))

        vs_text = Text("vs", font_size=32, color=WHITE, weight=BOLD).set_opacity(0.4).move_to(ORIGIN)

        self.play(FadeIn(old_label), FadeIn(new_label),
                  *[FadeIn(b, shift=DOWN * 0.2) for b in old_boxes],
                  *[FadeIn(b, shift=DOWN * 0.2) for b in new_boxes],
                  FadeIn(vs_text), run_time=0.6)
        self.play(*[Create(c) for c in new_connections], run_time=0.3)
        self.wait(0.4)

        x_old = Text("✗", font_size=80, color=SOFT_RED).set_opacity(0.6).move_to([-3.5, 0, 0])
        check_new = Text("✓", font_size=80, color=GREEN).set_opacity(0.6).move_to([3.5, 0, 0])
        self.play(FadeIn(x_old, scale=0.5), FadeIn(check_new, scale=0.5), run_time=0.4)
        self.wait(1.5)

        self.play(FadeOut(VGroup(old_label, old_boxes, new_label, new_boxes,
                                 new_connections, vs_text, x_old, check_new)), run_time=0.4)

        # ═════════════════════════════════════════════
        # ACT 9: EMOTIONAL CLOSER (73-80s)
        # "Because every student deserves..."
        # ═════════════════════════════════════════════

        closer1 = Text("Every student.", font_size=52, color=WHITE, weight=BOLD).move_to([0, 1.2, 0])
        closer2 = Text("Every level.", font_size=52, color=MERIDIAN_TEAL, weight=BOLD).move_to([0, 0, 0])
        closer3 = Text("One program that adapts.", font_size=52, color=MERIDIAN_BLUE, weight=BOLD).move_to([0, -1.2, 0])

        self.play(FadeIn(closer1, shift=UP * 0.2), run_time=0.6)
        self.wait(0.6)
        self.play(FadeIn(closer2, shift=UP * 0.2), run_time=0.6)
        self.wait(0.6)
        self.play(FadeIn(closer3, shift=UP * 0.2), run_time=0.6)
        self.wait(0.8)

        self.play(
            Circumscribe(VGroup(closer1, closer2, closer3), color=MERIDIAN_TEAL, run_time=0.8),
            bg_grid.animate.set_opacity(0.35),
        )
        self.play(bg_grid.animate.set_opacity(0.15), run_time=0.3)
        self.wait(0.3)
        self.play(FadeOut(VGroup(closer1, closer2, closer3)), run_time=0.4)

        # ═════════════════════════════════════════════
        # ACT 10: END CARD with Lissajous (80-85s)
        # "Meridian Press. Mathematics for every student."
        # ═════════════════════════════════════════════

        # Lissajous
        _A2, _B2 = 1.8, 1.3
        liss_glow = ParametricFunction(
            lambda t: np.array([_A2 * np.sin(2 * t), _B2 * np.sin(3 * t) + 0.8, 0]),
            t_range=[0, TAU, 0.01],
            color=MERIDIAN_BLUE, stroke_width=10, stroke_opacity=0.15
        )
        liss_core = ParametricFunction(
            lambda t: np.array([_A2 * np.sin(2 * t), _B2 * np.sin(3 * t) + 0.8, 0]),
            t_range=[0, TAU, 0.01],
            color=MERIDIAN_BLUE, stroke_width=2.5, stroke_opacity=0.8
        )

        end_meridian = Text("MERIDIAN PRESS", font_size=56, color=MERIDIAN_BLUE, weight=BOLD)
        end_tagline = Text("Mathematics for every student.", font_size=28, color=WARM_WHITE)
        end_tagline.set_opacity(0.7)
        end_url = Text("meridian-press.com", font_size=22, color=MERIDIAN_TEAL)

        end_meridian.move_to([0, -1.0, 0])
        end_tagline.next_to(end_meridian, DOWN, buff=0.3)
        end_url.next_to(end_tagline, DOWN, buff=0.4)

        end_box = SurroundingRectangle(
            VGroup(end_meridian, end_tagline, end_url),
            color=MERIDIAN_BLUE, fill_color=BOX_FILL, fill_opacity=0.4,
            buff=0.4, corner_radius=0.12, stroke_width=2
        )

        self.play(Create(liss_core, run_time=1.0), FadeIn(liss_glow, run_time=0.8))
        self.play(FadeIn(end_box), FadeIn(end_meridian, scale=0.95), run_time=0.5)
        self.play(FadeIn(end_tagline, shift=UP * 0.1), run_time=0.3)
        self.play(FadeIn(end_url), run_time=0.3)
        self.play(Circumscribe(end_box, color=MERIDIAN_BLUE, run_time=0.8))
        self.wait(12.0)

        self.play(FadeOut(VGroup(end_box, end_meridian, end_tagline, end_url,
                                 liss_glow, liss_core, bg_grid, border, border_glow, wm)), run_time=0.8)
