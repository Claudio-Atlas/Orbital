"""
Meridian Math × Orbital — District Promo V6
============================================
IRON TIMING DISCIPLINE. Every segment:
  1. add_sound(segment) — audio starts
  2. Animations fit WITHIN audio duration
  3. wait(remaining) — pad to fill audio
  4. wait(EXTRA_HOLD) — breathing room
  NO EXCEPTIONS. NO OVERLAP.

Segment durations (from split):
  s01=2.02  s02=2.33  s03=1.00  s04=0.93  s05=0.85  s06=0.89
  s07=1.97  s08=11.50 s09=1.07  s10=2.28  s11=0.84  s12=0.66
  s13=1.31  s14=4.61  s15=1.93  s16=1.55  s17=2.01  s18=2.16
  s19=2.91  s20=3.94  s21=0.73  s22=1.77

Render:
  cd ~/Desktop/Orbital/orbital_factory && source venv/bin/activate
  PATH="/Library/TeX/texbin:$PATH" manim render prototypes/meridian_promo_v6.py MeridianPromoV6 \
    -o meridian_promo_v6.mp4 --format mp4 -r 1920,1080 --frame_rate 60 --flush_cache
"""
from manim import *
import numpy as np

config.frame_width = 14.2
config.frame_height = 8.0

# ── Brand Colors (from settings.json) ──
VIOLET = "#8B5CF6"
CYAN = "#22D3EE"
GREEN = "#39FF14"
ORANGE = "#F97316"
M_BLUE = "#3B82F6"
M_TEAL = "#14B8A6"
WARM = "#F8FAFC"
BOX_FILL = "#1a1130"
GRID_C = "#1a1a3a"
E_CYAN = "#00E5FF"
RED = "#EF4444"
FW, FH = 14.2, 8.0

EXTRA_HOLD = 0.5
SEG = "output/tts/meridian_v5_segments/"

# ── Segment durations (measured) ──
DUR = {
    "s01": 2.02, "s02": 2.33, "s03": 1.00, "s04": 0.93,
    "s05": 0.85, "s06": 0.89, "s07": 1.97, "s08": 11.50,
    "s09": 1.07, "s10": 2.28, "s11": 0.84, "s12": 0.66,
    "s13": 1.31, "s14": 4.61, "s15": 1.93, "s16": 1.55,
    "s17": 2.01, "s18": 2.16, "s19": 2.91, "s20": 3.94,
    "s21": 0.73, "s22": 1.77,
}


def _grid():
    g = VGroup()
    for x in np.arange(-10, 10.1, 0.8):
        g.add(Line([x, -7, 0], [x, 7, 0], color=GRID_C, stroke_width=0.5, stroke_opacity=0.12))
    for y in np.arange(-7, 7.1, 0.8):
        g.add(Line([-10, y, 0], [10, y, 0], color=GRID_C, stroke_width=0.5, stroke_opacity=0.12))
    return g


def _purple_box(mob, buff=0.2, opacity=0.6):
    """Standard Orbital purple box (from settings.json)."""
    return SurroundingRectangle(mob, color=VIOLET, fill_color=BOX_FILL, fill_opacity=opacity,
                                 buff=buff, corner_radius=0.08, stroke_width=2.5)


def _student(color, label, x, y=0):
    """Student silhouette icon."""
    head = Circle(radius=0.18, color=color, fill_color=color, fill_opacity=0.7, stroke_width=1.5)
    head.move_to([x, y + 0.55, 0])
    body = Polygon([x - 0.22, y + 0.3, 0], [x + 0.22, y + 0.3, 0],
                   [x + 0.32, y - 0.15, 0], [x - 0.32, y - 0.15, 0],
                   color=color, fill_color=color, fill_opacity=0.4, stroke_width=1.5)
    lbl = Text(label, font_size=16, color=color, weight=BOLD).move_to([x, y - 0.45, 0])
    return VGroup(head, body, lbl)


def _textbook(label, color, w=1.2, h=1.8):
    """Detailed textbook cover with spine."""
    cover = RoundedRectangle(width=w, height=h, corner_radius=0.06,
                              color=color, fill_color=color, fill_opacity=0.15, stroke_width=2)
    spine = Rectangle(width=0.12, height=h, color=color, fill_color=color,
                       fill_opacity=0.3, stroke_width=1).move_to(cover.get_left() + RIGHT * 0.06)
    tbar = Rectangle(width=w * 0.7, height=0.22, color=color, fill_color=color,
                      fill_opacity=0.25, stroke_width=0).move_to(cover.get_center() + UP * 0.3)
    ttx = Text(label, font_size=14, color=color, weight=BOLD).move_to(tbar)
    dline = Line(cover.get_center() + LEFT * w * 0.3 + DOWN * 0.15,
                 cover.get_center() + RIGHT * w * 0.3 + DOWN * 0.15,
                 color=color, stroke_width=1, stroke_opacity=0.5)
    pub = Text("MERIDIAN", font_size=8, color=color).set_opacity(0.4)
    pub.move_to(cover.get_bottom() + UP * 0.2)
    return VGroup(cover, spine, tbar, ttx, dline, pub)


def _gear(r, n, color, c, tl=0.14, sw=2.5):
    parts = [Circle(radius=r, color=color, stroke_width=sw, fill_color=BOX_FILL, fill_opacity=0.4).move_to(c),
             Dot(radius=0.06, color=color, fill_opacity=0.8).move_to(c)]
    for i in range(n):
        a = i * TAU / n
        ca = np.array(c)
        ip = ca + r * np.array([np.cos(a), np.sin(a), 0])
        op = ca + (r + tl) * np.array([np.cos(a), np.sin(a), 0])
        pp = np.array([-np.sin(a), np.cos(a), 0])
        tw = 0.08
        parts.append(Polygon(ip + pp * tw, ip - pp * tw, op - pp * tw * .7, op + pp * tw * .7,
                              color=color, stroke_width=sw - .5, fill_color=color, fill_opacity=0.3))
    return VGroup(*parts)


class MeridianPromoV6College(MovingCameraScene):
    def construct(self):
        self.camera.background_color = BLACK
        self.camera.frame.set(width=FW, height=FH)

        bg = _grid()
        self.add(bg)

        # ── Persistent frame ──
        border = Rectangle(width=FW - 0.2, height=FH - 0.2, color=M_BLUE,
                           stroke_width=2.5, stroke_opacity=0.5, fill_opacity=0)
        border_glow = Rectangle(width=FW - 0.15, height=FH - 0.15, color=M_BLUE,
                                stroke_width=6, stroke_opacity=0.08, fill_opacity=0)
        wm = Text("MERIDIAN", font_size=11, color=WHITE, weight=BOLD).set_opacity(0.3)
        wm.move_to([-FW / 2 + 1, -FH / 2 + 0.25, 0])
        self.add(border_glow, border, wm)

        # ════════════════════════════════════════════════════════
        # PRE-ROLL (3s, no voice)
        # ════════════════════════════════════════════════════════
        mer = Text("MERIDIAN", font_size=52, color=M_BLUE, weight=BOLD).move_to([-3, 0.2, 0])
        math_t = Text("MATH", font_size=28, color=M_TEAL, weight=BOLD).next_to(mer, DOWN, 0.15)
        cx = Text("x", font_size=48, color=WHITE, weight=BOLD).move_to(ORIGIN)
        _A, _B = 0.9, 0.65
        liss = ParametricFunction(lambda t: np.array([_A * np.sin(2 * t) + 3, _B * np.sin(3 * t), 0]),
                                   t_range=[0, TAU, .01], color=E_CYAN, stroke_width=2.5)
        liss_g = ParametricFunction(lambda t: np.array([_A * np.sin(2 * t) + 3, _B * np.sin(3 * t), 0]),
                                     t_range=[0, TAU, .01], color=E_CYAN, stroke_width=8, stroke_opacity=.15)
        orb = Text("ORBITAL", font_size=52, color=E_CYAN, weight=BOLD).move_to([3, -1.1, 0])

        self.play(FadeIn(mer, shift=RIGHT * .3), FadeIn(math_t, shift=RIGHT * .3),
                  FadeIn(cx, scale=.3), Create(liss), FadeIn(liss_g),
                  FadeIn(orb, shift=LEFT * .3), run_time=1.5)  # 1.5s
        self.wait(1.0)  # 2.5s total
        intro = Group(mer, math_t, cx, liss, liss_g, orb)
        self.play(FadeOut(intro, shift=UP * .4), run_time=0.5)  # 3.0s total

        # ════════════════════════════════════════════════════════
        # SCENE 1: s01 + s02 — Student pace + programs don't
        # s01 (2.02s): "Every student learns at a different pace."
        # s02 (2.33s): "The problem is, most math programs don't."
        # ════════════════════════════════════════════════════════

        # Build visual (NO timeline cost)
        line = Line([-6, -1.5, 0], [6, -1.5, 0], color=WHITE, stroke_width=2.5, stroke_opacity=0.5)
        ticks = VGroup()
        for i, lbl in enumerate(["Ch 1", "Ch 2", "Ch 3", "Ch 4", "Ch 5", "Ch 6", "Ch 7", "Ch 8"]):
            x = -5.5 + i * 1.5
            ticks.add(Line([x, -1.62, 0], [x, -1.38, 0], color=WHITE, stroke_width=1.5, stroke_opacity=0.4))
            ticks.add(Text(lbl, font_size=12, color=WHITE).set_opacity(0.35).move_to([x, -1.85, 0]))
        st_a = _student(GREEN, "Alex", -5, 0)
        st_b = _student(M_BLUE, "Maria", -5, 0.15)
        st_c = _student(ORANGE, "Tyler", -5, 0.3)

        # ── s01: 2.02s ──
        self.add_sound(SEG + "s01_every_student.mp3")
        self.play(Create(line), FadeIn(ticks), run_time=0.4)  # 0.4s
        self.play(FadeIn(st_a, shift=UP * .2), FadeIn(st_b, shift=UP * .2),
                  FadeIn(st_c, shift=UP * .2), run_time=0.3)  # 0.7s
        # anim_time so far: 0.7s. remaining = 2.02 - 0.7 = 1.32s
        self.wait(1.32)
        self.wait(EXTRA_HOLD)

        # ── s02: 2.33s ──
        self.add_sound(SEG + "s02_problem_is.mp3")
        # Students move at different speeds — this IS the visual for s02
        self.play(
            st_a.animate.move_to([4.5, 0, 0]),
            st_b.animate.move_to([1.0, 0.15, 0]),
            st_c.animate.move_to([-1.5, 0.3, 0]),
            run_time=2.0)  # 2.0s
        # remaining = 2.33 - 2.0 = 0.33s
        self.wait(0.33)
        self.wait(EXTRA_HOLD)

        scene1 = VGroup(line, ticks, st_a, st_b, st_c)
        self.play(FadeOut(scene1, shift=UP * 0.3), run_time=0.4)

        # ════════════════════════════════════════════════════════
        # SCENE 2: s03 + s04 + s05 + s06 — Domino effect
        # s03 (1.00s): "One textbook."
        # s04 (0.93s): "One speed."
        # s05 (0.85s): "And if you miss a step,"
        # s06 (0.89s): "good luck catching up."
        # ════════════════════════════════════════════════════════

        # Build books (NO timeline cost)
        books = VGroup()
        for i, lbl in enumerate(["1.1", "1.2", "1.3", "1.4", "1.5", "1.6"]):
            bk = _textbook(f"Sec {lbl}", M_BLUE, w=1.5, h=2.2)
            bk.move_to([-5.5 + i * 2.1, 0.5, 0])
            books.add(bk)

        # ── s03: 1.00s — "One textbook." ──
        self.add_sound(SEG + "s03_one_textbook.mp3")
        self.play(*[FadeIn(b, shift=UP * 0.2) for b in books], run_time=0.5)  # 0.5s
        # remaining = 1.00 - 0.5 = 0.5s
        self.wait(0.5)
        self.wait(EXTRA_HOLD)

        # ── s04: 0.93s — "One speed." ──
        self.add_sound(SEG + "s04_one_speed.mp3")
        spd = Arrow([-6, -1.5, 0], [6, -1.5, 0], color=RED, stroke_width=2.5, buff=0)
        spd_t = Text("ONE SPEED", font_size=18, color=RED, weight=BOLD).next_to(spd, UP, 0.1).set_x(3)
        self.play(GrowArrow(spd), FadeIn(spd_t), run_time=0.5)  # 0.5s
        # remaining = 0.93 - 0.5 = 0.43s
        self.wait(0.43)
        self.wait(EXTRA_HOLD)

        # ── s05: 0.85s — "And if you miss a step," ──
        self.add_sound(SEG + "s05_miss_a_step.mp3")
        self.play(
            books[2][0].animate.set_color(RED).set_fill(RED, 0.2),
            books[2][3].animate.set_color(RED),
            Flash(books[2].get_center(), color=RED, line_length=0.5, num_lines=12),
            run_time=0.4)  # 0.4s
        # remaining = 0.85 - 0.4 = 0.45s
        self.wait(0.45)
        self.wait(EXTRA_HOLD)

        # ── s06: 0.89s — "good luck catching up." ──
        self.add_sound(SEG + "s06_good_luck.mp3")
        # Domino topple
        for i in range(3, 6):
            self.play(
                Rotate(books[i], PI / 6, about_point=books[i].get_bottom()),
                books[i].animate.set_opacity(0.2),
                run_time=0.12)  # 0.12s each = 0.36s total
        # remaining = 0.89 - 0.36 = 0.53s
        self.wait(0.53)
        self.wait(EXTRA_HOLD)

        self.play(FadeOut(VGroup(books, spd, spd_t)), run_time=0.4)

        # ════════════════════════════════════════════════════════
        # SCENE 3: s07 — Meridian reveal + gears
        # s07 (1.97s): "We built Meridian to fix that."
        # ════════════════════════════════════════════════════════

        mer_logo = Text("MERIDIAN", font_size=72, color=M_BLUE, weight=BOLD)
        mer_sub = Text("M A T H", font_size=24, color=M_TEAL, weight=BOLD).set_opacity(0.8)
        mer_sub.next_to(mer_logo, DOWN, 0.25)

        self.add_sound(SEG + "s07_built_meridian.mp3")
        self.play(FadeIn(mer_logo, scale=1.05),
                  Flash(ORIGIN, color=M_BLUE, line_length=0.8, num_lines=20),
                  run_time=0.5)  # 0.5s
        self.play(FadeIn(mer_sub), run_time=0.3)  # 0.8s
        # remaining = 1.97 - 0.8 = 1.17s
        self.wait(1.17)
        self.wait(EXTRA_HOLD)

        self.play(FadeOut(VGroup(mer_logo, mer_sub)), run_time=0.4)

        # Gears with math symbols (plays during the natural pause before s08)
        g1 = _gear(1.8, 16, M_BLUE, [-3.5, -0.3, 0], 0.28, 3)
        g2 = _gear(1.2, 12, M_TEAL, [0.3, -0.3, 0], 0.22, 3)
        g3 = _gear(0.85, 10, ORANGE, [3.0, 0.8, 0], 0.18, 2.5)
        g4 = _gear(0.6, 8, VIOLET, [4.5, -0.8, 0], 0.14, 2)

        syms = VGroup()
        sym_data = [r"\int", r"\Sigma", r"\pi", r"\infty",
                    r"\sqrt{x}", r"\Delta", r"\theta", r"\lambda"]
        sym_cols = [CYAN, GREEN, ORANGE, M_TEAL, VIOLET, M_BLUE, CYAN, GREEN]
        for i, (s, c) in enumerate(zip(sym_data, sym_cols)):
            t = MathTex(s, font_size=28, color=c).set_opacity(0.6)
            angle = i * TAU / len(sym_data)
            t.move_to([3 * np.cos(angle), 2 * np.sin(angle), 0])
            syms.add(t)

        self.play(FadeIn(g1), FadeIn(g2), FadeIn(g3), FadeIn(g4),
                  *[FadeIn(s, scale=0.5) for s in syms], run_time=0.4)
        self.play(
            Rotate(g1, PI / 2, about_point=[-3.5, -0.3, 0]),
            Rotate(g2, -PI / 1.5, about_point=[0.3, -0.3, 0]),
            Rotate(g3, PI / 1.3, about_point=[3.0, 0.8, 0]),
            Rotate(g4, -PI, about_point=[4.5, -0.8, 0]),
            *[s.animate.shift(RIGHT * 0.8 + UP * 0.3) for s in syms],
            run_time=1.2)
        self.play(FadeOut(VGroup(g1, g2, g3, g4, syms)), run_time=0.4)

        # ════════════════════════════════════════════════════════
        # SCENE 4: s08 — Four Pillars (11.50s — lots of time!)
        # "Complete math programs with digital textbooks,
        #  video walkthroughs, thousands of practice problems,
        #  and a personal AI tutor that adapts to EVERY student."
        # ════════════════════════════════════════════════════════

        # Subtle Riemann sum background
        bg_ax = Axes(x_range=[0, 2 * PI + .5, PI / 2], y_range=[-1.5, 1.5, .5],
                     x_length=12, y_length=5, tips=False,
                     axis_config={"color": WHITE, "stroke_width": 1, "stroke_opacity": 0.06})
        bg_cv = bg_ax.plot(lambda x: np.sin(x), x_range=[0, 2 * PI],
                           color=VIOLET, stroke_width=1.5, stroke_opacity=0.08)
        bg_rects = VGroup()
        for i in range(30):
            dx = 2 * PI / 30
            x = i * dx
            y = np.sin(x + dx / 2)
            h = 5 * abs(y) / 3.0
            w = 12 * dx / (2 * PI + .5)
            c = CYAN if y >= 0 else ORANGE
            r = Rectangle(width=w, height=h, color=c, fill_color=c, fill_opacity=0.03,
                          stroke_width=0.5, stroke_opacity=0.08)
            cx_p = bg_ax.c2p(x + dx / 2, 0)
            r.move_to(cx_p + (UP if y >= 0 else DOWN) * h / 2)
            bg_rects.add(r)
        bg_riemann = VGroup(bg_ax, bg_cv, bg_rects)
        self.add(bg_riemann)

        # Build pillar cards
        def _pillar(abbrev, title, subtitle, color, features):
            bx = RoundedRectangle(width=2.8, height=4.0, corner_radius=0.12,
                                   color=color, fill_color=BOX_FILL, fill_opacity=0.8, stroke_width=2.5)
            glow = RoundedRectangle(width=2.8, height=4.0, corner_radius=0.12,
                                     color=color, fill_opacity=0, stroke_width=6, stroke_opacity=0.12)
            ic = Text(abbrev, font_size=36, color=color, weight=BOLD).move_to(bx.get_center() + UP * 1.2)
            ttl = Text(title, font_size=20, color=color, weight=BOLD).move_to(bx.get_center() + UP * 0.45)
            sub = Text(subtitle, font_size=13, color=WARM).set_opacity(0.6).move_to(bx.get_center() + UP * 0.1)
            feats = VGroup()
            for j, f in enumerate(features):
                ft = Text(f"  {f}", font_size=11, color=WARM).set_opacity(0.5)
                ft.move_to(bx.get_center() + DOWN * (0.4 + j * 0.28))
                ft.align_to(bx.get_left() + RIGHT * 0.35, LEFT)
                feats.add(ft)
            return VGroup(bx, glow, ic, ttl, sub, feats)

        p1 = _pillar("TXT", "Digital Textbook", "Interactive content",
                      M_BLUE, ["Full curriculum", "Searchable", "Mobile-ready"])
        p2 = _pillar("VID", "Video Lessons", "Step-by-step",
                      VIOLET, ["Every concept", "Rewindable", "Clear visuals"])
        p3 = _pillar("PRB", "Practice Problems", "Auto-graded",
                      ORANGE, ["1000s of problems", "Instant feedback", "Adaptive"])
        p4 = _pillar("AI", "AI Tutor", "Personalized help",
                      M_TEAL, ["Meets students where they are", "Step-by-step hints", "24/7 available"])
        pillars = VGroup(p1, p2, p3, p4).arrange(RIGHT, buff=0.4).move_to([0, -0.2, 0])

        # ── s08: 11.50s ──
        self.add_sound(SEG + "s08_complete_programs.mp3")

        # Appear one at a time: 4 cards x 1.2s each = 4.8s
        for card in pillars:
            self.play(FadeIn(card, shift=UP * 0.4, scale=0.92), run_time=0.7)  # 0.7s
            self.wait(0.5)  # 0.5s — total 1.2s per card
        # 4.8s elapsed

        # Connect them: 0.5s
        conn = Line(pillars[0].get_bottom() + DOWN * 0.4, pillars[-1].get_bottom() + DOWN * 0.4,
                     color=M_TEAL, stroke_width=3)
        conn_dots = VGroup(*[Dot(pillars[i].get_bottom() + DOWN * 0.4, color=M_TEAL, radius=0.06) for i in range(4)])
        conn_txt = Text("ONE INTEGRATED PLATFORM", font_size=22, color=M_TEAL, weight=BOLD)
        conn_txt.next_to(conn, DOWN, 0.15)
        self.play(Create(conn), FadeIn(conn_dots), FadeIn(conn_txt), run_time=0.5)  # 5.3s

        # Punchline text — Tier 1 style
        every = Text("Adapts to EVERY student", font_size=36, color=GREEN, weight=BOLD)
        every.move_to([0, 3.2, 0])
        every_box = _purple_box(every, buff=0.18)
        self.play(FadeIn(every_box), FadeIn(every), run_time=0.4)  # 5.7s

        # Pulse all cards
        self.play(*[Indicate(c, color=c[0].color, scale_factor=1.03) for c in pillars], run_time=0.5)  # 6.2s

        # remaining = 11.50 - 6.2 = 5.3s — HOLD and let the voice finish
        self.wait(5.3)
        self.wait(EXTRA_HOLD)

        self.play(FadeOut(VGroup(pillars, conn, conn_dots, conn_txt, every, every_box, bg_riemann)),
                  run_time=0.4)

        # ════════════════════════════════════════════════════════
        # SCENE 5: s09 + s10 + s11 + s12 + s13 — AI Tutor Demo
        # s09 (1.07s): continuation / transition
        # s10 (2.28s): "When a student gets stuck, the AI tutor
        #              meets them right where they are."
        # s11 (0.84s): "Step by step."
        # s12 (0.66s): "No judgment."
        # s13 (1.31s): "No falling through the cracks."
        # ════════════════════════════════════════════════════════

        # Build panel (NO timeline cost)
        panel = RoundedRectangle(width=11, height=5.5, corner_radius=0.15,
                                  color=M_TEAL, fill_color=BOX_FILL, fill_opacity=0.85, stroke_width=2.5)
        panel_glow = RoundedRectangle(width=11, height=5.5, corner_radius=0.15,
                                       color=M_TEAL, fill_opacity=0, stroke_width=8, stroke_opacity=0.1)
        panel.move_to([0, -0.3, 0])
        panel_glow.move_to([0, -0.3, 0])
        badge_bx = RoundedRectangle(width=1.8, height=0.45, corner_radius=0.1,
                                     color=M_TEAL, fill_color=M_TEAL, fill_opacity=0.2, stroke_width=1.5)
        badge_tx = Text("AI Tutor", font_size=14, color=M_TEAL, weight=BOLD)
        badge_tx.move_to(badge_bx)
        badge = VGroup(badge_bx, badge_tx).move_to(panel.get_top() + DOWN * 0.4 + LEFT * 3.5)
        prob = MathTex(r"3x + 7 = 22", font_size=52, color=WHITE).move_to([0, 2.8, 0])

        # ── s09: 1.07s — transition, show problem ──
        self.add_sound(SEG + "s09_ai_tutor_adapts.mp3")
        self.play(Write(prob), run_time=0.5)  # 0.5s
        # remaining = 1.07 - 0.5 = 0.57s
        self.wait(0.57)
        self.wait(EXTRA_HOLD)

        # ── s10: 2.28s — "When a student gets stuck..." ──
        self.add_sound(SEG + "s10_every_student2.mp3")
        stuck = Text("Student stuck here", font_size=16, color=ORANGE, weight=BOLD)
        stuck.next_to(prob, RIGHT, 0.5)
        self.play(FadeIn(panel), FadeIn(panel_glow), FadeIn(badge),
                  FadeIn(stuck, shift=LEFT * 0.2), run_time=0.5)  # 0.5s
        hint1 = Text("What operation undoes adding 7?", font_size=18, color=WARM).set_opacity(0.8)
        hint1.move_to([-2, 0.6, 0])
        self.play(FadeIn(hint1, shift=LEFT * 0.3), run_time=0.4)  # 0.9s
        step1 = MathTex(r"3x + 7 - 7 = 22 - 7", font_size=36, color=CYAN).move_to([0, 0, 0])
        self.play(Write(step1), run_time=0.5)  # 1.4s
        # remaining = 2.28 - 1.4 = 0.88s
        self.wait(0.88)
        self.wait(EXTRA_HOLD)

        # ── s11: 0.84s — "Step by step." ──
        self.add_sound(SEG + "s11_step_by_step.mp3")
        step2 = MathTex(r"3x = 15", font_size=40, color=CYAN).move_to([0, -0.7, 0])
        self.play(Write(step2), run_time=0.4)  # 0.4s
        # remaining = 0.84 - 0.4 = 0.44s
        self.wait(0.44)
        self.wait(EXTRA_HOLD)

        # ── s12: 0.66s — "No judgment." ──
        self.add_sound(SEG + "s12_no_judgment.mp3")
        hint2 = Text("Now divide both sides by 3!", font_size=18, color=WARM).set_opacity(0.8)
        hint2.move_to([-1.5, -1.4, 0])
        self.play(FadeIn(hint2, shift=LEFT * 0.3), run_time=0.3)  # 0.3s
        # remaining = 0.66 - 0.3 = 0.36s
        self.wait(0.36)
        self.wait(EXTRA_HOLD)

        # ── s13: 1.31s — "No falling through the cracks." ──
        self.add_sound(SEG + "s13_no_cracks.mp3")
        answer = MathTex(r"x = 5", font_size=48, color=GREEN).move_to([0, -2.1, 0])
        ans_box = _purple_box(answer, buff=0.15, opacity=0.5)
        self.play(Write(answer), Create(ans_box), run_time=0.4)  # 0.4s
        self.play(Flash(answer.get_center(), color=GREEN, line_length=0.5, num_lines=14),
                  run_time=0.3)  # 0.7s
        solved = Text("Solved!", font_size=16, color=GREEN, weight=BOLD).move_to(stuck)
        self.play(FadeOut(stuck), FadeIn(solved), run_time=0.2)  # 0.9s
        # remaining = 1.31 - 0.9 = 0.41s
        self.wait(0.41)
        self.wait(EXTRA_HOLD)

        self.play(FadeOut(VGroup(panel, panel_glow, badge, prob, solved,
                                  hint1, step1, step2, hint2, answer, ans_box)), run_time=0.4)

        # ════════════════════════════════════════════════════════
        # SCENE 6: s14 + s15 — Teacher Dashboard
        # s14 (4.61s): "Teachers get real-time dashboards showing
        #              exactly where each student needs help,"
        # s15 (1.93s): "not just a grade at the end of the unit."
        # Dashboard STAYS on screen through BOTH segments.
        # ════════════════════════════════════════════════════════

        # Build dashboard (NO timeline cost)
        df = RoundedRectangle(width=12.5, height=6.5, corner_radius=0.15,
                               color=M_BLUE, fill_color=BOX_FILL, fill_opacity=0.85, stroke_width=2.5)
        df_glow = RoundedRectangle(width=12.5, height=6.5, corner_radius=0.15,
                                    color=M_BLUE, fill_opacity=0, stroke_width=8, stroke_opacity=0.1)
        dt = Text("Teacher Dashboard", font_size=30, color=M_BLUE, weight=BOLD)
        dt.move_to(df.get_top() + DOWN * 0.45)
        live_d = Circle(radius=0.08, color=GREEN, fill_color=GREEN, fill_opacity=0.8)
        live_t = Text("LIVE", font_size=12, color=GREEN, weight=BOLD)
        live = VGroup(live_d, live_t).arrange(RIGHT, buff=0.1).move_to(df.get_top() + DOWN * 0.45 + RIGHT * 4.5)
        period = Text("Period 3 - Algebra 1", font_size=14, color=WARM).set_opacity(0.5)
        period.move_to(df.get_top() + DOWN * 0.8)

        students_data = [
            ("Alex", 0.95, GREEN, "A"), ("Maria", 0.82, M_TEAL, "M"),
            ("James", 0.41, ORANGE, "J"), ("Sofia", 0.91, GREEN, "S"),
            ("Tyler", 0.28, RED, "T"), ("Emma", 0.73, M_TEAL, "E"),
            ("Noah", 0.60, M_BLUE, "N"),
        ]
        bars = VGroup()
        names = VGroup()
        pcts = VGroup()
        avatars = VGroup()
        for i, (nm, p, c, init) in enumerate(students_data):
            x = -5.2 + i * 1.5
            h = p * 3.2
            av = Circle(radius=0.25, color=c, fill_color=c, fill_opacity=0.2, stroke_width=1.5)
            av_t = Text(init, font_size=14, color=c, weight=BOLD).move_to(av)
            avatars.add(VGroup(av, av_t).move_to([x, 2.6, 0]))
            bar = Rectangle(width=1.0, height=h, color=c, fill_color=c, fill_opacity=0.45, stroke_width=2)
            bar.move_to([x, -0.8 + h / 2, 0])
            bars.add(bar)
            names.add(Text(nm, font_size=12, color=WARM).set_opacity(0.6).move_to([x, -1.2, 0]))
            pt = Text(f"{int(p * 100)}%", font_size=15, color=c, weight=BOLD)
            pt.next_to(bar, UP, 0.08)
            pcts.add(pt)

        # ── s14: 4.61s ──
        self.add_sound(SEG + "s14_dashboards.mp3")
        self.play(FadeIn(df), FadeIn(df_glow), FadeIn(dt), FadeIn(live), FadeIn(period),
                  run_time=0.4)  # 0.4s
        self.play(*[FadeIn(a, scale=0.8) for a in avatars], run_time=0.3)  # 0.7s
        self.play(*[GrowFromEdge(b, DOWN) for b in bars], run_time=1.0)  # 1.7s
        self.play(FadeIn(names), FadeIn(pcts), run_time=0.4)  # 2.1s
        # Alert highlights
        alert_j = SurroundingRectangle(VGroup(bars[2], names[2], avatars[2]),
                                        color=ORANGE, stroke_width=2.5, buff=0.12, corner_radius=0.08)
        alert_t = SurroundingRectangle(VGroup(bars[4], names[4], avatars[4]),
                                        color=RED, stroke_width=2.5, buff=0.12, corner_radius=0.08)
        atxt = Text("Needs attention", font_size=16, color=RED, weight=BOLD).move_to([4.5, 2.0, 0])
        atxt2 = Text("At risk", font_size=16, color=ORANGE, weight=BOLD).move_to([4.5, 1.5, 0])
        self.play(Create(alert_j), Create(alert_t), FadeIn(atxt), FadeIn(atxt2), run_time=0.5)  # 2.6s
        # remaining = 4.61 - 2.6 = 2.01s
        self.wait(2.01)
        self.wait(EXTRA_HOLD)

        # ── s15: 1.93s — Dashboard STAYS, text overlay appears ──
        self.add_sound(SEG + "s15_not_just_grade.mp3")
        not_grade = Text("Not just a grade. Real-time insight.", font_size=24,
                          color=CYAN, weight=BOLD).move_to([0, -3.0, 0])
        ng_box = _purple_box(not_grade, buff=0.12, opacity=0.4)
        self.play(FadeIn(ng_box), FadeIn(not_grade), run_time=0.4)  # 0.4s
        # remaining = 1.93 - 0.4 = 1.53s
        self.wait(1.53)
        self.wait(EXTRA_HOLD)

        dash_all = VGroup(df, df_glow, dt, live, period, bars, names, pcts, avatars,
                           alert_j, alert_t, atxt, atxt2, not_grade, ng_box)
        self.play(FadeOut(dash_all), run_time=0.4)

        # ════════════════════════════════════════════════════════
        # SCENE 7: s16 + s17 — Course Pyramid
        # s16 (1.55s): "Pre-Algebra through Calculus."
        # s17 (2.01s): "Every course built on one platform."
        # ════════════════════════════════════════════════════════

        # Build pyramid (NO timeline cost) — COLLEGE VERSION
        pyr_data = [
            # Bottom row: 4 courses
            [("Precalculus", "#6366F1", -3.6, -2.5),
             ("Calc I", "#7C3AED", -1.2, -2.5),
             ("Calc II", "#8B5CF6", 1.2, -2.5),
             ("Calc III", "#A855F7", 3.6, -2.5)],
            # Row 2: 3 courses
            [("Diff Equations", "#C084FC", -2.4, -1.0),
             ("Linear Algebra", M_TEAL, 0, -1.0),
             ("Number Theory", ORANGE, 2.4, -1.0)],
            # Row 3: 2 courses
            [("Numerical Analysis", M_BLUE, -1.2, 0.5),
             ("Abstract Algebra", VIOLET, 1.2, 0.5)],
            # Top: 1 course
            [("Analysis", E_CYAN, 0, 2.0)],
        ]
        # Smaller blocks to fit 4 wide
        pyr_blocks = VGroup()
        for row in pyr_data:
            for nm, c, x, y in row:
                bx = RoundedRectangle(width=2.1, height=1.1, corner_radius=0.08,
                                       color=c, fill_color=BOX_FILL, fill_opacity=0.65, stroke_width=2.5)
                glow = RoundedRectangle(width=2.1, height=1.1, corner_radius=0.08,
                                         color=c, fill_opacity=0, stroke_width=5, stroke_opacity=0.1)
                tx = Text(nm, font_size=13, color=c, weight=BOLD)
                pyr_blocks.add(VGroup(bx, glow, tx).move_to([x, y, 0]))

        # ── s16: college version uses s16_prealg_calc_college.mp3 (2.14s) ──
        self.add_sound(SEG + "s16_prealg_calc_college.mp3")
        # Bottom row (4 blocks): 0.12 * 4 = 0.48s
        for i in range(4):
            self.play(FadeIn(pyr_blocks[i], shift=UP * 0.3, scale=0.9), run_time=0.12)
        # Row 2 (3 blocks): 0.12 * 3 = 0.36s → total 0.84s
        for i in range(4, 7):
            self.play(FadeIn(pyr_blocks[i], shift=UP * 0.3, scale=0.9), run_time=0.12)
        # Row 3 (2 blocks): 0.12 * 2 = 0.24s → total 1.08s
        for i in range(7, 9):
            self.play(FadeIn(pyr_blocks[i], shift=UP * 0.3, scale=0.9), run_time=0.12)
        # Top: 0.2s → total 1.28s
        self.play(FadeIn(pyr_blocks[9], shift=UP * 0.3, scale=0.9), run_time=0.2)
        # remaining = 2.14 - 1.28 = 0.86s
        self.wait(0.86)
        self.wait(EXTRA_HOLD)

        # ── s17: 2.01s ──
        self.add_sound(SEG + "s17_one_platform.mp3")
        crown = Text("ONE PLATFORM", font_size=28, color=M_TEAL, weight=BOLD).move_to([0, 2.8, 0])
        crown_box = _purple_box(crown, buff=0.15)
        self.play(FadeIn(crown_box), FadeIn(crown), run_time=0.4)  # 0.4s
        self.play(*[Indicate(b, color=b[0].color, scale_factor=1.04) for b in pyr_blocks],
                  run_time=0.5)  # 0.9s
        # remaining = 2.01 - 0.9 = 1.11s
        self.wait(1.11)
        self.wait(EXTRA_HOLD)

        self.play(FadeOut(VGroup(pyr_blocks, crown, crown_box)), run_time=0.4)

        # ════════════════════════════════════════════════════════
        # SCENE 8: s18 + s19 — Not bolted on
        # s18 (2.16s): "Not a textbook with a website bolted on."
        # s19 (2.91s): "A complete system built by educators
        #              who have been in the classroom."
        # ════════════════════════════════════════════════════════

        # Build comparison (NO timeline cost)
        div = Line([0, -3.5, 0], [0, 3.0, 0], color=WHITE, stroke_width=1.5, stroke_opacity=0.2)
        ol = Text("Traditional", font_size=26, color=RED, weight=BOLD).move_to([-3.5, 3.0, 0])
        old_items = VGroup()
        for i, lbl in enumerate(["Textbook", "Separate Website", "YouTube Videos", "Manual Grading"]):
            bx = RoundedRectangle(width=2.6, height=0.85, corner_radius=0.06,
                                   color="#444", fill_color="#0a0a0a", fill_opacity=0.5, stroke_width=1.5)
            tx = Text(lbl, font_size=13, color="#777")
            old_items.add(VGroup(bx, tx).move_to([-3.5 + (i % 2) * 0.3, 1.8 - i * 1.0, 0]))
        disc = VGroup(*[DashedLine(old_items[i].get_bottom(), old_items[i + 1].get_top(),
                                    color="#444", stroke_width=1, dash_length=0.1) for i in range(3)])

        nl = Text("Meridian", font_size=26, color=M_TEAL, weight=BOLD).move_to([3.5, 3.0, 0])
        new_items = VGroup()
        new_data = [("Textbook", M_BLUE), ("Videos", VIOLET), ("Problems", ORANGE), ("AI Tutor", M_TEAL)]
        for i, (lbl, c) in enumerate(new_data):
            bx = RoundedRectangle(width=2.6, height=0.85, corner_radius=0.06,
                                   color=c, fill_color=BOX_FILL, fill_opacity=0.6, stroke_width=2.5)
            glow = RoundedRectangle(width=2.6, height=0.85, corner_radius=0.06,
                                     color=c, fill_opacity=0, stroke_width=5, stroke_opacity=0.08)
            tx = Text(lbl, font_size=14, color=c, weight=BOLD)
            new_items.add(VGroup(bx, glow, tx).move_to([3.5, 1.8 - i * 1.0, 0]))
        nconn = VGroup(*[Line(new_items[i].get_bottom(), new_items[i + 1].get_top(),
                              color=M_TEAL, stroke_width=2.5, stroke_opacity=0.7) for i in range(3)])

        # ── s18: 2.16s ──
        self.add_sound(SEG + "s18_not_bolted.mp3")
        self.play(FadeIn(div), FadeIn(ol), FadeIn(nl),
                  *[FadeIn(b, shift=DOWN * 0.15) for b in old_items],
                  *[FadeIn(b, shift=DOWN * 0.15) for b in new_items],
                  *[Create(d) for d in disc], run_time=0.6)  # 0.6s
        self.play(*[Create(c) for c in nconn], run_time=0.3)  # 0.9s
        xo = Text("X", font_size=72, color=RED, weight=BOLD).set_opacity(0.6).move_to([-3.5, -2.2, 0])
        ck = Text("OK", font_size=48, color=GREEN, weight=BOLD).set_opacity(0.6).move_to([3.5, -2.2, 0])
        self.play(FadeIn(xo, scale=0.5), FadeIn(ck, scale=0.5), run_time=0.3)  # 1.2s
        # remaining = 2.16 - 1.2 = 0.96s
        self.wait(0.96)
        self.wait(EXTRA_HOLD)

        # ── s19: 2.91s — "A complete system built by educators..." ──
        self.add_sound(SEG + "s19_complete_system.mp3")
        sys_txt = Text("Built by educators. For educators.", font_size=24,
                        color=GREEN, weight=BOLD).move_to([0, -3.2, 0])
        sys_box = _purple_box(sys_txt, buff=0.12, opacity=0.4)
        self.play(FadeIn(sys_box), FadeIn(sys_txt), run_time=0.4)  # 0.4s
        # remaining = 2.91 - 0.4 = 2.51s
        self.wait(2.51)
        self.wait(EXTRA_HOLD)

        self.play(FadeOut(VGroup(div, ol, nl, old_items, new_items, disc, nconn, xo, ck,
                                  sys_txt, sys_box)), run_time=0.4)

        # ════════════════════════════════════════════════════════
        # SCENE 9: s20 — Emotional closer
        # s20 (3.94s): "Because every student deserves a program
        #              that actually meets them where they are."
        # ════════════════════════════════════════════════════════

        c1 = Text("Every student.", font_size=52, color=WHITE, weight=BOLD).move_to([0, 1.5, 0])
        c2 = Text("Every level.", font_size=52, color=M_TEAL, weight=BOLD).move_to([0, 0, 0])
        c3 = Text("One program that adapts.", font_size=52, color=M_BLUE, weight=BOLD).move_to([0, -1.5, 0])
        c1_box = _purple_box(c1, buff=0.15, opacity=0.3)
        c2_box = _purple_box(c2, buff=0.15, opacity=0.3)
        c3_box = _purple_box(c3, buff=0.15, opacity=0.3)

        self.add_sound(SEG + "s20_every_deserves.mp3")
        self.play(FadeIn(c1_box), FadeIn(c1, shift=UP * 0.2), run_time=0.5)  # 0.5s
        self.wait(0.4)  # 0.9s
        self.play(FadeIn(c2_box), FadeIn(c2, shift=UP * 0.2), run_time=0.5)  # 1.4s
        self.wait(0.4)  # 1.8s
        self.play(FadeIn(c3_box), FadeIn(c3, shift=UP * 0.2), run_time=0.5)  # 2.3s
        # remaining = 3.94 - 2.3 = 1.64s
        self.wait(1.64)
        self.wait(EXTRA_HOLD)

        self.play(FadeOut(VGroup(c1, c2, c3, c1_box, c2_box, c3_box)), run_time=0.4)

        # ════════════════════════════════════════════════════════
        # SCENE 10: s21 + s22 — End Card (HOLD)
        # s21 (0.73s): "Meridian Math."
        # s22 (1.77s): "Mathematics for every student."
        # ════════════════════════════════════════════════════════

        _A2, _B2 = 2.2, 1.5
        lg = ParametricFunction(lambda t: np.array([_A2 * np.sin(2 * t), _B2 * np.sin(3 * t) + 0.8, 0]),
                                 t_range=[0, TAU, .01], color=M_BLUE, stroke_width=10, stroke_opacity=0.12)
        lc = ParametricFunction(lambda t: np.array([_A2 * np.sin(2 * t), _B2 * np.sin(3 * t) + 0.8, 0]),
                                 t_range=[0, TAU, .01], color=M_BLUE, stroke_width=2.5, stroke_opacity=0.8)
        en = Text("MERIDIAN MATH", font_size=60, color=M_BLUE, weight=BOLD).move_to([0, -0.8, 0])
        et = Text("Mathematics for every student.", font_size=28, color=WARM).set_opacity(0.7)
        et.next_to(en, DOWN, 0.35)
        eu = Text("meridian-math.org", font_size=26, color=M_TEAL, weight=BOLD).next_to(et, DOWN, 0.45)
        eb = SurroundingRectangle(VGroup(en, et, eu), color=M_BLUE, fill_color=BOX_FILL, fill_opacity=0.5,
                                   buff=0.5, corner_radius=0.12, stroke_width=2.5)
        eb_glow = SurroundingRectangle(VGroup(en, et, eu), color=M_BLUE, fill_opacity=0,
                                        buff=0.5, corner_radius=0.12, stroke_width=8, stroke_opacity=0.1)

        # ── s21: 0.73s ──
        self.add_sound(SEG + "s21_meridian_math.mp3")
        self.play(Create(lc, run_time=0.4), FadeIn(lg, run_time=0.3))  # 0.4s
        # remaining = 0.73 - 0.4 = 0.33s
        self.wait(0.33)
        self.wait(EXTRA_HOLD)

        # ── s22: 1.77s ──
        self.add_sound(SEG + "s22_tagline.mp3")
        self.play(FadeIn(eb), FadeIn(eb_glow), FadeIn(en, scale=0.95), run_time=0.4)  # 0.4s
        self.play(FadeIn(et, shift=UP * 0.1), run_time=0.3)  # 0.7s
        self.play(FadeIn(eu), run_time=0.2)  # 0.9s
        # remaining = 1.77 - 0.9 = 0.87s
        self.wait(0.87)
        self.wait(EXTRA_HOLD)

        # Final hold — let it breathe
        self.wait(3.0)
        self.play(FadeOut(Group(*self.mobjects)), run_time=1.0)
