"""
Meridian Press — District Promo (16:9 Landscape)
=================================================
School district pitch. Visuals synced to Hale voiceover.
Adapted from Orbital promo showcase style.

Render:
  cd ~/Desktop/Orbital/orbital_factory && source venv/bin/activate
  PATH="/Library/TeX/texbin:$PATH" manim render prototypes/meridian_promo_v1.py MeridianPromoV1 \
    -o meridian_promo_v1.mp4 --format mp4 -r 1920,1080 --frame_rate 60 --flush_cache
"""
from manim import *
import numpy as np

config.frame_width = 14.2
config.frame_height = 8.0

# ── BRAND COLORS (Meridian: professional but modern) ──
VIOLET = "#8B5CF6"
CYAN = "#22D3EE"
GREEN = "#39FF14"
ORANGE = "#F97316"
MERIDIAN_BLUE = "#3B82F6"
MERIDIAN_TEAL = "#14B8A6"
WARM_WHITE = "#F8FAFC"
BOX_FILL = "#0f1729"
GRID_COLOR = "#1a1a3a"
END_CYAN = "#00E5FF"
SOFT_RED = "#EF4444"
GOLD = "#FBBF24"
FW = 14.2
FH = 8.0


def _make_bg_grid(fw=14.2, fh=8.0, spacing=0.8, color=GRID_COLOR, sw=0.5, opacity=0.15):
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


class MeridianPromoV1(MovingCameraScene):
    def construct(self):
        self.camera.background_color = BLACK
        self.camera.frame.set(width=FW, height=FH)

        bg_grid = _make_bg_grid(fw=20, fh=14)
        self.add(bg_grid)

        # Persistent border
        def _get_border():
            cf = self.camera.frame
            w, h = cf.get_width() - 0.2, cf.get_height() - 0.2
            return Rectangle(width=w, height=h, color=MERIDIAN_BLUE,
                             stroke_width=2, stroke_opacity=0.5,
                             fill_opacity=0).move_to(cf.get_center())

        border = always_redraw(_get_border)
        self.add(border)

        # ═══════════════════════════════════════════
        # ACT 1: DIFFERENT PACES (8s)
        # "Every student learns at a different pace.
        #  The problem is, most math programs don't."
        # ═══════════════════════════════════════════

        # Three dots moving along a number line at different speeds
        line = Line([-5, 0, 0], [5, 0, 0], color=WHITE, stroke_width=2, stroke_opacity=0.4)
        
        # Tick marks on the line
        ticks = VGroup()
        for x in range(-4, 5):
            tick = Line([x, -0.15, 0], [x, 0.15, 0], color=WHITE, stroke_width=1.5, stroke_opacity=0.3)
            ticks.add(tick)
        
        # Three student dots — different sizes, colors, speeds
        dot_fast = Dot([-4, 0, 0], color=GREEN, radius=0.15).set_glow_factor(0.6)
        dot_mid = Dot([-4, 0, 0], color=MERIDIAN_BLUE, radius=0.15).set_glow_factor(0.6)
        dot_slow = Dot([-4, 0, 0], color=ORANGE, radius=0.15).set_glow_factor(0.6)
        
        label_fast = Text("Student A", font_size=16, color=GREEN).next_to(dot_fast, UP, buff=0.3)
        label_mid = Text("Student B", font_size=16, color=MERIDIAN_BLUE).next_to(dot_mid, UP, buff=0.6)
        label_slow = Text("Student C", font_size=16, color=ORANGE).next_to(dot_slow, UP, buff=0.9)

        self.play(Create(line), FadeIn(ticks), run_time=0.8)
        self.play(
            FadeIn(dot_fast), FadeIn(dot_mid), FadeIn(dot_slow),
            FadeIn(label_fast), FadeIn(label_mid), FadeIn(label_slow),
            run_time=0.6
        )

        # Move them at different speeds
        self.play(
            dot_fast.animate.move_to([4, 0, 0]),
            dot_mid.animate.move_to([1, 0, 0]),
            dot_slow.animate.move_to([-1, 0, 0]),
            label_fast.animate.move_to([4, 0.45, 0]),
            label_mid.animate.move_to([1, 0.75, 0]),
            label_slow.animate.move_to([-1, 1.05, 0]),
            run_time=4.0, rate_func=smooth
        )
        self.wait(1.0)

        # Show the problem: a rigid "curriculum pace" line sweeps through
        pace_line = DashedLine([-4, -1.5, 0], [-4, 1.5, 0], color=SOFT_RED,
                               stroke_width=3, dash_length=0.15)
        pace_label = Text("Curriculum Pace", font_size=18, color=SOFT_RED)
        pace_label.next_to(pace_line, DOWN, buff=0.2)
        
        self.play(FadeIn(pace_line), FadeIn(pace_label), run_time=0.5)
        self.play(
            pace_line.animate.move_to([1, 0, 0]),
            pace_label.animate.move_to([1, -1.7, 0]),
            run_time=3.0, rate_func=linear
        )

        # Student C now has an X — they're behind
        x_mark = Text("✗", font_size=32, color=SOFT_RED)
        x_mark.move_to(dot_slow.get_center() + DOWN * 0.5)
        self.play(FadeIn(x_mark, scale=1.5), run_time=0.4)
        self.wait(1.2)

        self.wait(1.0)
        act1_all = VGroup(line, ticks, dot_fast, dot_mid, dot_slow,
                          label_fast, label_mid, label_slow,
                          pace_line, pace_label, x_mark)
        self.play(FadeOut(act1_all, shift=UP * 0.5), run_time=0.5)

        # ═══════════════════════════════════════════
        # ACT 2: ONE TEXTBOOK, ONE SPEED (6s)
        # "One textbook. One speed. And if you miss
        #  a step, good luck catching up."
        # ═══════════════════════════════════════════

        # Show a single rigid path with gaps
        path_points = [[-5, 0, 0], [-2.5, 1, 0], [0, 0, 0], [2.5, -1, 0], [5, 0, 0]]

        # Draw steps as connected boxes
        steps = VGroup()
        step_labels = ["1.1", "1.2", "1.3", "1.4", "1.5"]
        for i, (label, pos) in enumerate(zip(step_labels, [[-4, 0, 0], [-2, 0, 0], [0, 0, 0], [2, 0, 0], [4, 0, 0]])):
            box = RoundedRectangle(width=1.4, height=0.8, corner_radius=0.08,
                                   color=WHITE, fill_color=BOX_FILL, fill_opacity=0.6,
                                   stroke_width=2, stroke_opacity=0.6)
            txt = Text(label, font_size=22, color=WHITE)
            grp = VGroup(box, txt).move_to(pos)
            steps.add(grp)

        arrows = VGroup()
        for i in range(len(steps) - 1):
            arr = Arrow(steps[i].get_right(), steps[i + 1].get_left(),
                        color=WHITE, stroke_width=2, stroke_opacity=0.4,
                        buff=0.1, max_tip_length_to_length_ratio=0.2)
            arrows.add(arr)

        self.play(
            *[FadeIn(s, shift=UP * 0.2) for s in steps],
            run_time=0.8
        )
        self.play(*[Create(a) for a in arrows], run_time=0.6)
        self.wait(0.8)

        # "Miss a step" — step 1.3 goes red, crumbles
        missed = steps[2]
        self.play(
            missed[0].animate.set_color(SOFT_RED).set_fill(SOFT_RED, 0.3),
            missed[1].animate.set_color(SOFT_RED),
            Flash(missed.get_center(), color=SOFT_RED, line_length=0.4, num_lines=8),
            run_time=0.6
        )

        # Steps after the missed one fade/gray out
        self.play(
            steps[3].animate.set_opacity(0.2),
            steps[4].animate.set_opacity(0.2),
            arrows[2].animate.set_opacity(0.1),
            arrows[3].animate.set_opacity(0.1),
            run_time=1.0
        )

        gap_text = Text("?", font_size=48, color=SOFT_RED, weight=BOLD)
        gap_text.move_to(steps[2].get_center())
        self.play(FadeIn(gap_text, scale=0.5), FadeOut(missed[1]), run_time=0.5)
        self.wait(2.0)

        self.wait(1.0)
        act2_all = VGroup(steps, arrows, gap_text)
        self.play(FadeOut(act2_all), run_time=0.5)

        # ═══════════════════════════════════════════
        # ACT 3: MERIDIAN LOGO REVEAL (3s)
        # "We built Meridian to fix that."
        # ═══════════════════════════════════════════

        # Clean, bold text reveal
        meridian_text = Text("MERIDIAN", font_size=64, color=MERIDIAN_BLUE, weight=BOLD)
        meridian_sub = Text("P R E S S", font_size=20, color=WARM_WHITE,
                            weight=BOLD).set_opacity(0.7)
        meridian_sub.next_to(meridian_text, DOWN, buff=0.2)

        # Horizontal line accents
        line_l = Line([-3.5, 0, 0], [-1.5, 0, 0], color=MERIDIAN_TEAL, stroke_width=2)
        line_r = Line([1.5, 0, 0], [3.5, 0, 0], color=MERIDIAN_TEAL, stroke_width=2)
        lines_accent = VGroup(line_l, line_r).move_to(meridian_text.get_center())

        logo_grp = VGroup(meridian_text, meridian_sub)
        logo_grp.move_to(ORIGIN)

        self.play(
            FadeIn(meridian_text, scale=0.95),
            run_time=0.6
        )
        self.play(
            FadeIn(meridian_sub, shift=UP * 0.1),
            run_time=0.3
        )
        self.play(
            Circumscribe(meridian_text, color=MERIDIAN_BLUE, run_time=0.6),
            bg_grid.animate.set_opacity(0.3),
            run_time=0.6
        )
        self.play(bg_grid.animate.set_opacity(0.15), run_time=0.3)
        self.wait(1.0)
        self.play(FadeOut(logo_grp, shift=UP * 0.3), run_time=0.4)

        # ═══════════════════════════════════════════
        # ACT 4: FOUR PILLARS (8s)
        # "Complete math programs with digital textbooks,
        #  video walkthroughs, thousands of practice
        #  problems, and a personal AI tutor..."
        # ═══════════════════════════════════════════

        pillars = [
            ("📖", "Digital\nTextbook", MERIDIAN_BLUE),
            ("🎬", "Video\nLessons", VIOLET),
            ("✏️", "Practice\nProblems", ORANGE),
            ("🤖", "AI\nTutor", MERIDIAN_TEAL),
        ]

        pillar_grp = VGroup()
        for emoji_str, label, color in pillars:
            # Box
            box = RoundedRectangle(width=2.4, height=2.8, corner_radius=0.12,
                                   color=color, fill_color=BOX_FILL, fill_opacity=0.7,
                                   stroke_width=2.5)
            # Icon (use text as placeholder for emoji)
            icon = Text(emoji_str, font_size=48)
            icon.move_to(box.get_center() + UP * 0.5)
            # Label
            lbl = Text(label, font_size=20, color=color, weight=BOLD)
            lbl.move_to(box.get_center() + DOWN * 0.5)
            card = VGroup(box, icon, lbl)
            pillar_grp.add(card)

        pillar_grp.arrange(RIGHT, buff=0.5)
        pillar_grp.move_to(ORIGIN)

        # Reveal one by one
        for i, card in enumerate(pillar_grp):
            self.play(
                FadeIn(card, shift=UP * 0.3, scale=0.9),
                run_time=0.6
            )
            self.wait(0.4)

        self.wait(1.0)

        # Connect them with a glowing line underneath
        connect_line = Line(
            pillar_grp[0].get_bottom() + DOWN * 0.3,
            pillar_grp[-1].get_bottom() + DOWN * 0.3,
            color=MERIDIAN_TEAL, stroke_width=3
        )
        connect_label = Text("One Platform", font_size=22, color=MERIDIAN_TEAL, weight=BOLD)
        connect_label.next_to(connect_line, DOWN, buff=0.15)

        self.play(Create(connect_line), FadeIn(connect_label), run_time=0.6)
        self.wait(1.5)

        # Pulse all pillars
        self.play(
            *[Indicate(card, color=card[0].color, scale_factor=1.03) for card in pillar_grp],
            run_time=0.6
        )
        self.wait(0.5)
        self.play(FadeOut(VGroup(pillar_grp, connect_line, connect_label)), run_time=0.5)

        # ═══════════════════════════════════════════
        # ACT 5: AI TUTOR IN ACTION (8s)
        # "When a student gets stuck, the AI tutor
        #  meets them right where they are."
        # ═══════════════════════════════════════════

        # Show a math problem with step-by-step AI help
        problem = MathTex(r"3x + 7 = 22", font_size=52, color=WHITE)
        problem.move_to([0, 2.5, 0])
        prob_label = Text("Student is stuck here:", font_size=18, color=ORANGE)
        prob_label.set_opacity(0.7).next_to(problem, UP, buff=0.3)

        self.play(FadeIn(prob_label), Write(problem), run_time=0.6)
        self.wait(0.5)

        # AI tutor chat bubbles
        bubble_bg = RoundedRectangle(width=8, height=4.5, corner_radius=0.15,
                                      color=MERIDIAN_TEAL, fill_color=BOX_FILL,
                                      fill_opacity=0.8, stroke_width=2)
        bubble_bg.move_to([0, -0.8, 0])

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

        self.play(FadeIn(bubble_bg), FadeIn(ai_label), run_time=0.5)
        self.play(FadeIn(msg1, shift=LEFT * 0.3), run_time=0.5)
        self.wait(0.6)
        self.play(Write(step1), run_time=0.7)
        self.wait(0.5)
        self.play(Write(step2), run_time=0.5)
        self.play(FadeIn(msg2, shift=LEFT * 0.3), run_time=0.5)
        self.wait(0.5)
        self.play(
            Write(step3),
            Flash(step3.get_center(), color=GREEN, line_length=0.5, num_lines=10),
            run_time=0.6
        )

        answer_box = SurroundingRectangle(step3, color=GREEN, fill_color=GREEN,
                                           fill_opacity=0.1, buff=0.15, corner_radius=0.08,
                                           stroke_width=2)
        self.play(Create(answer_box), run_time=0.4)
        self.wait(1.5)

        act5_all = VGroup(problem, prob_label, bubble_bg, ai_label,
                          msg1, step1, step2, msg2, step3, answer_box)
        self.play(FadeOut(act5_all), run_time=0.4)

        # ═══════════════════════════════════════════
        # ACT 6: TEACHER DASHBOARD (7s)
        # "Teachers get real-time dashboards showing
        #  exactly where each student needs help"
        # ═══════════════════════════════════════════

        dash_title = Text("Teacher Dashboard", font_size=28, color=MERIDIAN_BLUE, weight=BOLD)
        dash_title.move_to([0, 3.2, 0])

        # Mock dashboard — bar chart of student progress
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

            n = Text(name, font_size=14, color=WHITE).set_opacity(0.7)
            n.move_to([x, -2.0, 0])

            p = Text(f"{int(prog * 100)}%", font_size=16, color=col, weight=BOLD)
            p.next_to(bar, UP, buff=0.1)

            bars.add(bar)
            names.add(n)
            pcts.add(p)

        self.play(FadeIn(dash_title), run_time=0.3)
        self.play(
            *[GrowFromEdge(bar, DOWN) for bar in bars],
            run_time=0.8
        )
        self.play(FadeIn(names), FadeIn(pcts), run_time=0.4)
        self.wait(0.5)

        # Highlight the struggling students
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

        self.play(
            Create(alert_james), Create(alert_tyler),
            FadeIn(needs_help),
            Create(arrow_j), Create(arrow_t),
            run_time=0.8
        )
        self.wait(2.5)

        act6_all = VGroup(dash_title, bars, names, pcts,
                          alert_james, alert_tyler, needs_help, arrow_j, arrow_t)
        self.play(FadeOut(act6_all), run_time=0.4)

        # ═══════════════════════════════════════════
        # ACT 7: COURSE SPECTRUM (5s)
        # "Pre-Algebra through Calculus.
        #  Every course built on one platform."
        # ═══════════════════════════════════════════

        courses = [
            ("Pre-Algebra", "#6366F1"),
            ("Algebra 1", "#8B5CF6"),
            ("Geometry", "#A855F7"),
            ("Algebra 2", "#C084FC"),
            ("Precalculus", MERIDIAN_TEAL),
            ("Calculus", MERIDIAN_BLUE),
        ]

        course_cards = VGroup()
        for name, color in courses:
            box = RoundedRectangle(width=1.8, height=1.0, corner_radius=0.08,
                                   color=color, fill_color=BOX_FILL, fill_opacity=0.6,
                                   stroke_width=2.5)
            txt = Text(name, font_size=14, color=color, weight=BOLD)
            txt.move_to(box.get_center())
            course_cards.add(VGroup(box, txt))

        course_cards.arrange(RIGHT, buff=0.25)
        course_cards.move_to([0, 0.5, 0])

        # Connecting arrows
        c_arrows = VGroup()
        for i in range(len(course_cards) - 1):
            arr = Arrow(course_cards[i].get_right(), course_cards[i + 1].get_left(),
                        color=WHITE, stroke_width=1.5, stroke_opacity=0.4,
                        buff=0.05, max_tip_length_to_length_ratio=0.3)
            c_arrows.add(arr)

        platform_line = Line(
            course_cards[0].get_bottom() + DOWN * 0.5,
            course_cards[-1].get_bottom() + DOWN * 0.5,
            color=MERIDIAN_TEAL, stroke_width=3
        )
        platform_text = Text("ONE PLATFORM", font_size=22, color=MERIDIAN_TEAL, weight=BOLD)
        platform_text.next_to(platform_line, DOWN, buff=0.15)

        # Animate in from left to right
        self.camera.frame.set(width=FW * 0.85)
        for i, card in enumerate(course_cards):
            anims = [FadeIn(card, shift=RIGHT * 0.2, scale=0.9)]
            if i > 0:
                anims.append(Create(c_arrows[i - 1]))
            if i == 2:
                anims.append(self.camera.frame.animate.set(width=FW * 0.92))
            elif i == 4:
                anims.append(self.camera.frame.animate.set(width=FW))
            self.play(*anims, run_time=0.3)

        self.play(Create(platform_line), FadeIn(platform_text), run_time=0.5)
        self.wait(2.0)

        self.play(
            *[Indicate(card, color=card[0].color, scale_factor=1.05) for card in course_cards],
            run_time=0.6
        )
        self.wait(0.5)
        self.play(FadeOut(VGroup(course_cards, c_arrows, platform_line, platform_text)), run_time=0.4)

        # ═══════════════════════════════════════════
        # ACT 8: NOT BOLTED ON (5s)
        # "Not a textbook with a website bolted on."
        # ═══════════════════════════════════════════

        self.camera.frame.set(width=FW).move_to(ORIGIN)

        # Left side: "Old Way" — disconnected boxes
        old_label = Text("Traditional", font_size=22, color=SOFT_RED, weight=BOLD)
        old_label.move_to([-3.5, 3.0, 0])

        old_boxes = VGroup()
        old_items = [("Textbook", "#555"), ("Website", "#555"),
                     ("Videos", "#555"), ("Grading", "#555")]
        for i, (name, col) in enumerate(old_items):
            box = RoundedRectangle(width=2.2, height=0.7, corner_radius=0.06,
                                   color=col, fill_color="#111", fill_opacity=0.5,
                                   stroke_width=1.5)
            txt = Text(name, font_size=16, color="#888")
            grp = VGroup(box, txt).move_to([-3.5, 1.5 - i * 1.0, 0])
            old_boxes.add(grp)

        # Disconnected — no arrows, just scattered
        old_boxes[1].shift(RIGHT * 0.3)
        old_boxes[3].shift(LEFT * 0.2)

        # Right side: "Meridian" — connected system
        new_label = Text("Meridian", font_size=22, color=MERIDIAN_TEAL, weight=BOLD)
        new_label.move_to([3.5, 3.0, 0])

        new_items = [("Textbook", MERIDIAN_BLUE), ("Videos", VIOLET),
                     ("Problems", ORANGE), ("AI Tutor", MERIDIAN_TEAL)]
        new_boxes = VGroup()
        for i, (name, col) in enumerate(new_items):
            box = RoundedRectangle(width=2.2, height=0.7, corner_radius=0.06,
                                   color=col, fill_color=BOX_FILL, fill_opacity=0.6,
                                   stroke_width=2.5)
            txt = Text(name, font_size=16, color=col, weight=BOLD)
            grp = VGroup(box, txt).move_to([3.5, 1.5 - i * 1.0, 0])
            new_boxes.add(grp)

        # Connected lines between new boxes
        new_connections = VGroup()
        for i in range(len(new_boxes) - 1):
            conn = Line(new_boxes[i].get_bottom(), new_boxes[i + 1].get_top(),
                        color=MERIDIAN_TEAL, stroke_width=2, stroke_opacity=0.6)
            new_connections.add(conn)

        # VS divider
        vs_text = Text("vs", font_size=32, color=WHITE, weight=BOLD).set_opacity(0.4)
        vs_text.move_to(ORIGIN)

        self.play(
            FadeIn(old_label), FadeIn(new_label),
            *[FadeIn(b, shift=DOWN * 0.2) for b in old_boxes],
            *[FadeIn(b, shift=DOWN * 0.2) for b in new_boxes],
            FadeIn(vs_text),
            run_time=0.6
        )
        self.play(*[Create(c) for c in new_connections], run_time=0.4)
        self.wait(0.5)

        # X out old way
        x_old = Text("✗", font_size=80, color=SOFT_RED).set_opacity(0.6)
        x_old.move_to([-3.5, 0, 0])
        # Check new way
        check_new = Text("✓", font_size=80, color=GREEN).set_opacity(0.6)
        check_new.move_to([3.5, 0, 0])

        self.play(FadeIn(x_old, scale=0.5), FadeIn(check_new, scale=0.5), run_time=0.5)
        self.wait(2.5)

        act8_all = VGroup(old_label, old_boxes, new_label, new_boxes,
                          new_connections, vs_text, x_old, check_new)
        self.play(FadeOut(act8_all), run_time=0.4)

        # ═══════════════════════════════════════════
        # ACT 9: EMOTIONAL CLOSER (4s)
        # "Because every student deserves a program
        #  that actually meets them where they are."
        # ═══════════════════════════════════════════

        closer1 = Text("Every student.", font_size=48, color=WHITE, weight=BOLD)
        closer2 = Text("Every level.", font_size=48, color=MERIDIAN_TEAL, weight=BOLD)
        closer3 = Text("One program that adapts.", font_size=48, color=MERIDIAN_BLUE, weight=BOLD)

        closer1.move_to([0, 1.2, 0])
        closer2.move_to([0, 0, 0])
        closer3.move_to([0, -1.2, 0])

        self.play(FadeIn(closer1, shift=UP * 0.2), run_time=0.6)
        self.wait(0.8)
        self.play(FadeIn(closer2, shift=UP * 0.2), run_time=0.6)
        self.wait(0.8)
        self.play(FadeIn(closer3, shift=UP * 0.2), run_time=0.6)
        self.wait(1.0)

        self.play(
            Circumscribe(VGroup(closer1, closer2, closer3), color=MERIDIAN_TEAL, run_time=0.8),
            bg_grid.animate.set_opacity(0.3),
        )
        self.play(bg_grid.animate.set_opacity(0.15), run_time=0.4)
        self.wait(0.5)
        self.play(FadeOut(VGroup(closer1, closer2, closer3)), run_time=0.5)

        # ═══════════════════════════════════════════
        # ACT 10: END CARD (4s)
        # "Meridian Press. Mathematics for every student."
        # ═══════════════════════════════════════════

        end_meridian = Text("MERIDIAN PRESS", font_size=56, color=MERIDIAN_BLUE, weight=BOLD)
        end_tagline = Text("Mathematics for every student.", font_size=28, color=WARM_WHITE)
        end_tagline.set_opacity(0.7)
        end_tagline.next_to(end_meridian, DOWN, buff=0.4)

        end_url = Text("meridian-press.com", font_size=22, color=MERIDIAN_TEAL)
        end_url.next_to(end_tagline, DOWN, buff=0.5)

        end_box = SurroundingRectangle(
            VGroup(end_meridian, end_tagline),
            color=MERIDIAN_BLUE, fill_color=BOX_FILL, fill_opacity=0.4,
            buff=0.4, corner_radius=0.12, stroke_width=2
        )

        self.play(
            FadeIn(end_box),
            FadeIn(end_meridian, scale=0.95),
            run_time=0.6
        )
        self.play(FadeIn(end_tagline, shift=UP * 0.1), run_time=0.4)
        self.play(FadeIn(end_url), run_time=0.4)
        self.play(Circumscribe(end_box, color=MERIDIAN_BLUE, run_time=0.8))
        self.wait(4.0)

        self.play(FadeOut(VGroup(end_box, end_meridian, end_tagline, end_url, bg_grid, border)),
                  run_time=0.5)
