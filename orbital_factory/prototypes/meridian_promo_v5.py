"""
Meridian Math × Orbital — District Promo V5
============================================
Per-segment audio via add_sound(). Proven timing model.
More detail, slower animations, text overlays.

Render:
  cd ~/Desktop/Orbital/orbital_factory && source venv/bin/activate
  PATH="/Library/TeX/texbin:$PATH" manim render prototypes/meridian_promo_v5.py MeridianPromoV5 \
    -o meridian_promo_v5.mp4 --format mp4 -r 1920,1080 --frame_rate 60 --flush_cache
"""
from manim import *
import numpy as np

config.frame_width = 14.2
config.frame_height = 8.0

# ── Brand Colors ──
VIOLET = "#8B5CF6"
CYAN = "#22D3EE"
GREEN = "#39FF14"
ORANGE = "#F97316"
M_BLUE = "#3B82F6"
M_TEAL = "#14B8A6"
WARM = "#F8FAFC"
BOX = "#1a1130"
GRID_C = "#1a1a3a"
E_CYAN = "#00E5FF"
RED = "#EF4444"
SURFACE = "#0d0a14"
FW, FH = 14.2, 8.0

# ── Text Hierarchy (from settings.json) ──
# Tier 1 Punchline: fs=42, BOLD, GREEN, MathTex + purple box
# Tier 2 Key Fact:  fs=28, BOLD, CYAN, MathTex + purple box
# Tier 3 Callout:   fs=24, BOLD, GREEN, Text
# Tier 4 Title:     fs=26, BOLD, VIOLET, Text
# Tier 5 Equation:  fs=30, WHITE, MathTex raw
# Tier 6 Caption:   fs=24, CYAN, MathTex

ANIMATION_RATIO = 0.35
EXTRA_HOLD = 0.5

SEG = "output/tts/meridian_v5_segments/"


def _grid(fw=20, fh=14, sp=0.8):
    g = VGroup()
    for x in np.arange(-fw/2, fw/2+.1, sp):
        g.add(Line([x,-fh/2,0],[x,fh/2,0], color=GRID_C, stroke_width=0.5, stroke_opacity=0.12))
    for y in np.arange(-fh/2, fh/2+.1, sp):
        g.add(Line([-fw/2,y,0],[fw/2,y,0], color=GRID_C, stroke_width=0.5, stroke_opacity=0.12))
    return g


def _purple_box(mob, buff=0.2, opacity=0.6):
    return SurroundingRectangle(mob, color=VIOLET, fill_color=BOX, fill_opacity=opacity,
                                 buff=buff, corner_radius=0.1, stroke_width=2.5)


def _student_silhouette(color, label, x, y=0):
    """Simple student icon: head circle + body trapezoid."""
    head = Circle(radius=0.18, color=color, fill_color=color, fill_opacity=0.7, stroke_width=1.5)
    head.move_to([x, y+0.55, 0])
    body = Polygon([x-0.22, y+0.3, 0], [x+0.22, y+0.3, 0],
                   [x+0.32, y-0.15, 0], [x-0.32, y-0.15, 0],
                   color=color, fill_color=color, fill_opacity=0.4, stroke_width=1.5)
    lbl = Text(label, font_size=16, color=color, weight=BOLD).move_to([x, y-0.45, 0])
    return VGroup(head, body, lbl)


def _gear(r, n, color, c, tl=0.14, sw=2.5):
    parts = [Circle(radius=r, color=color, stroke_width=sw, fill_color=BOX, fill_opacity=0.4).move_to(c),
             Dot(radius=0.06, color=color, fill_opacity=0.8).move_to(c)]
    for i in range(n):
        a = i * TAU / n
        ca = np.array(c)
        ip = ca + r * np.array([np.cos(a), np.sin(a), 0])
        op = ca + (r + tl) * np.array([np.cos(a), np.sin(a), 0])
        pp = np.array([-np.sin(a), np.cos(a), 0])
        tw = 0.08
        parts.append(Polygon(ip+pp*tw, ip-pp*tw, op-pp*tw*.7, op+pp*tw*.7,
                              color=color, stroke_width=sw-.5, fill_color=color, fill_opacity=0.3))
    return VGroup(*parts)


def _textbook_cover(label, color, w=1.2, h=1.8):
    """A detailed textbook with spine, title area, decorative line."""
    # Main cover
    cover = RoundedRectangle(width=w, height=h, corner_radius=0.06,
                              color=color, fill_color=color, fill_opacity=0.15, stroke_width=2)
    # Spine
    spine = Rectangle(width=0.12, height=h, color=color, fill_color=color,
                       fill_opacity=0.3, stroke_width=1).move_to(cover.get_left() + RIGHT*0.06)
    # Title bar
    tbar = Rectangle(width=w*0.7, height=0.22, color=color, fill_color=color,
                      fill_opacity=0.25, stroke_width=0).move_to(cover.get_center() + UP*0.3)
    # Section label
    ttx = Text(label, font_size=14, color=color, weight=BOLD).move_to(tbar)
    # Decorative line
    dline = Line(cover.get_center() + LEFT*w*0.3 + DOWN*0.15,
                 cover.get_center() + RIGHT*w*0.3 + DOWN*0.15,
                 color=color, stroke_width=1, stroke_opacity=0.5)
    # Bottom publisher line
    pub = Text("MERIDIAN", font_size=8, color=color).set_opacity(0.4)
    pub.move_to(cover.get_bottom() + UP*0.2)
    return VGroup(cover, spine, tbar, ttx, dline, pub)


class MeridianPromoV5(MovingCameraScene):
    def construct(self):
        self.camera.background_color = BLACK
        self.camera.frame.set(width=FW, height=FH)

        bg = _grid()
        self.add(bg)

        # ── Persistent border + watermark ──
        def _b():
            cf = self.camera.frame
            return Rectangle(width=cf.width-.2, height=cf.height-.2, color=M_BLUE,
                             stroke_width=2.5, stroke_opacity=0.5, fill_opacity=0).move_to(cf.get_center())
        def _bg():
            cf = self.camera.frame
            return Rectangle(width=cf.width-.15, height=cf.height-.15, color=M_BLUE,
                             stroke_width=6, stroke_opacity=0.08, fill_opacity=0).move_to(cf.get_center())
        def _wm():
            cf = self.camera.frame
            t = Text("MERIDIAN × ORBITAL", font_size=11, color=WHITE, weight=BOLD).set_opacity(0.3)
            t.move_to([cf.get_center()[0] - cf.width/2 + 1.2,
                       cf.get_center()[1] - cf.height/2 + 0.25, 0])
            return t

        self.add(always_redraw(_bg), always_redraw(_b), always_redraw(_wm))

        # ════════════════════════════════════════════════════════
        # PRE-ROLL: Collab Intro (3s, no voice, music starts)
        # ════════════════════════════════════════════════════════

        mer = Text("MERIDIAN", font_size=52, color=M_BLUE, weight=BOLD).move_to([-3, 0, 0])
        math_t = Text("MATH", font_size=28, color=M_TEAL, weight=BOLD).next_to(mer, DOWN, 0.15)
        cx = Text("×", font_size=56, color=WHITE, weight=BOLD).move_to(ORIGIN)
        _A, _B = 0.9, 0.65
        liss = ParametricFunction(lambda t: np.array([_A*np.sin(2*t)+3, _B*np.sin(3*t), 0]),
                                   t_range=[0, TAU, .01], color=E_CYAN, stroke_width=2.5)
        liss_g = ParametricFunction(lambda t: np.array([_A*np.sin(2*t)+3, _B*np.sin(3*t), 0]),
                                     t_range=[0, TAU, .01], color=E_CYAN, stroke_width=8, stroke_opacity=.15)
        orb = Text("ORBITAL", font_size=52, color=E_CYAN, weight=BOLD).move_to([3, -1.1, 0])

        self.play(FadeIn(mer, shift=RIGHT*.3), FadeIn(math_t, shift=RIGHT*.3),
                  FadeIn(cx, scale=.3),
                  Create(liss), FadeIn(liss_g), FadeIn(orb, shift=LEFT*.3), run_time=1.5)
        self.play(Flash(ORIGIN, color=VIOLET, line_length=.6, num_lines=16, run_time=.4),
                  cx.animate.set_color(VIOLET), run_time=.4)
        self.wait(0.6)
        intro_all = Group(mer, math_t, cx, liss, liss_g, orb)
        self.play(FadeOut(intro_all, shift=UP*.4), run_time=0.5)

        # ════════════════════════════════════════════════════════
        # SCENE 1 + 2: Student Pace / Programs Don't
        # s01 (2.02s): "Every student learns at a different pace."
        # s02 (2.33s): "The problem is, most math programs don't."
        # ════════════════════════════════════════════════════════

        # Number line with more detail
        line = Line([-6, -1.5, 0], [6, -1.5, 0], color=WHITE, stroke_width=2.5, stroke_opacity=0.5)
        ticks = VGroup()
        tick_labels = ["Ch 1", "Ch 2", "Ch 3", "Ch 4", "Ch 5", "Ch 6", "Ch 7", "Ch 8"]
        for i, lbl in enumerate(tick_labels):
            x = -5.5 + i * 1.5
            ticks.add(Line([x, -1.62, 0], [x, -1.38, 0], color=WHITE, stroke_width=1.5, stroke_opacity=0.4))
            ticks.add(Text(lbl, font_size=12, color=WHITE).set_opacity(0.35).move_to([x, -1.85, 0]))

        # Student silhouettes
        st_a = _student_silhouette(GREEN, "Alex", -5, 0)
        st_b = _student_silhouette(M_BLUE, "Maria", -5, 0)
        st_c = _student_silhouette(ORANGE, "Tyler", -5, 0)
        # Offset vertically so they don't overlap
        st_b.shift(UP * 0.15)
        st_c.shift(UP * 0.3)

        # Title overlay — Tier 4 style
        t1 = Text("Every student learns differently.", font_size=26,
                   color=VIOLET, weight=BOLD).move_to([0, 3.0, 0])
        t1_box = _purple_box(t1, buff=0.15, opacity=0.4)

        self.add_sound(SEG + "s01_every_student.mp3")
        self.play(Create(line), FadeIn(ticks), run_time=0.4)
        self.play(FadeIn(st_a, shift=UP*.2), FadeIn(st_b, shift=UP*.2),
                  FadeIn(st_c, shift=UP*.2), run_time=0.3)
        self.play(FadeIn(t1_box), FadeIn(t1), run_time=0.3)

        # Slow deliberate movement — students moving at different speeds
        self.play(
            st_a.animate.move_to([4.5, 0, 0]),
            st_b.animate.move_to([1.0, 0.15, 0]),
            st_c.animate.move_to([-1.5, 0.3, 0]),
            run_time=2.0, rate_func=smooth)
        self.wait(EXTRA_HOLD)

        # s02: "The problem is, most math programs don't."
        self.add_sound(SEG + "s02_problem_is.mp3")

        # Curriculum pace line sweeps through
        pace_line = DashedLine([-6, -0.8, 0], [6, -0.8, 0], color=RED,
                                stroke_width=3, dash_length=0.15)
        pace_label = Text("CURRICULUM PACE", font_size=16, color=RED, weight=BOLD)
        pace_label.next_to(pace_line, UP, 0.15).set_x(4)

        self.play(FadeOut(t1), FadeOut(t1_box), run_time=0.2)
        t2 = Text("Most programs move at ONE speed.", font_size=24,
                   color=RED, weight=BOLD).move_to([0, 3.0, 0])
        t2_box = _purple_box(t2, buff=0.15, opacity=0.4)
        self.play(FadeIn(t2_box), FadeIn(t2), run_time=0.2)

        self.play(Create(pace_line), FadeIn(pace_label), run_time=0.5)
        # Maria and Tyler fade/fall behind
        self.play(st_b.animate.set_opacity(0.3), st_c.animate.set_opacity(0.2),
                  st_c.animate.shift(DOWN*0.3), run_time=1.0)
        self.wait(EXTRA_HOLD)

        scene12 = VGroup(line, ticks, st_a, st_b, st_c, pace_line, pace_label, t2, t2_box)

        # ════════════════════════════════════════════════════════
        # SCENE 3: Domino Effect
        # s03 (1.00s): "One textbook."
        # s04 (0.93s): "One speed."
        # s05 (0.85s): "And if you miss a step,"
        # s06 (0.89s): "good luck catching up."
        # ════════════════════════════════════════════════════════

        self.play(FadeOut(scene12, shift=UP*0.3), run_time=0.4)

        # Detailed textbook covers as dominoes
        books = VGroup()
        book_labels = ["1.1", "1.2", "1.3", "1.4", "1.5", "1.6"]
        book_cols = [M_BLUE, M_BLUE, M_BLUE, M_BLUE, M_BLUE, M_BLUE]
        for i, (lbl, col) in enumerate(zip(book_labels, book_cols)):
            bk = _textbook_cover(f"Section {lbl}", col, w=1.5, h=2.2)
            bk.move_to([-5.5 + i * 2.1, 0.5, 0])
            books.add(bk)

        # Student silhouettes below each book
        studs = VGroup()
        stud_cols = [GREEN, M_TEAL, ORANGE, ORANGE, RED, RED]
        stud_names = ["✓", "✓", "?", "✗", "✗", "✗"]
        for i, (sc, sn) in enumerate(zip(stud_cols, stud_names)):
            s = Text(sn, font_size=28, color=sc, weight=BOLD).move_to([-5.5 + i*2.1, -1.5, 0])
            studs.add(s)

        self.add_sound(SEG + "s03_one_textbook.mp3")
        self.play(*[FadeIn(b, shift=UP*0.2) for b in books], run_time=0.5)
        self.wait(0.5)

        self.add_sound(SEG + "s04_one_speed.mp3")
        # Speed arrow
        spd = Arrow([-6, -2.5, 0], [6, -2.5, 0], color=RED, stroke_width=2.5, buff=0)
        spd_t = Text("ONE SPEED →", font_size=18, color=RED, weight=BOLD).next_to(spd, UP, 0.1).set_x(3)
        self.play(GrowArrow(spd), FadeIn(spd_t), run_time=0.5)
        self.wait(0.4)

        self.add_sound(SEG + "s05_miss_a_step.mp3")
        # Section 1.3 goes red — student missed this
        self.play(
            books[2][0].animate.set_color(RED).set_fill(RED, 0.2),
            books[2][3].animate.set_color(RED),
            Flash(books[2].get_center(), color=RED, line_length=0.5, num_lines=12),
            FadeIn(studs[2]),
            run_time=0.4)
        self.wait(0.4)

        self.add_sound(SEG + "s06_good_luck.mp3")
        # Domino topple — each book rotates and students show ✗
        for i in range(3, 6):
            self.play(
                Rotate(books[i], PI/6, about_point=books[i].get_bottom()),
                books[i].animate.set_opacity(0.25),
                FadeIn(studs[i]),
                run_time=0.15)

        # "Left behind" silhouettes fade
        behind = _student_silhouette(RED, "", -2, -1.5)
        behind2 = _student_silhouette(ORANGE, "", 0, -1.5)
        behind.set_opacity(0.3)
        behind2.set_opacity(0.2)
        self.play(FadeIn(behind), FadeIn(behind2), run_time=0.2)
        self.wait(EXTRA_HOLD)

        scene3 = VGroup(books, studs, spd, spd_t, behind, behind2)
        self.play(FadeOut(scene3, shift=DOWN*0.3), run_time=0.4)

        # ════════════════════════════════════════════════════════
        # SCENE 4: Meridian Reveal + Gears with Math
        # s07 (1.97s): "We built Meridian to fix that."
        # ════════════════════════════════════════════════════════

        self.add_sound(SEG + "s07_built_meridian.mp3")

        mer_logo = Text("MERIDIAN", font_size=72, color=M_BLUE, weight=BOLD)
        mer_sub = Text("M A T H", font_size=24, color=M_TEAL, weight=BOLD).set_opacity(0.8)
        mer_sub.next_to(mer_logo, DOWN, 0.25)
        logo_grp = VGroup(mer_logo, mer_sub)

        self.play(FadeIn(mer_logo, scale=1.05),
                  Flash(ORIGIN, color=M_BLUE, line_length=0.8, num_lines=20, run_time=0.5),
                  run_time=0.5)
        self.play(FadeIn(mer_sub), run_time=0.3)
        self.play(Circumscribe(mer_logo, color=M_TEAL, run_time=0.5))
        self.wait(0.3)
        self.play(logo_grp.animate.scale(0.5).move_to([0, 3.2, 0]), run_time=0.4)

        # Gears with math symbols flowing through
        g1 = _gear(1.8, 16, M_BLUE, [-3.5, -0.3, 0], 0.28, 3)
        g2 = _gear(1.2, 12, M_TEAL, [0.3, -0.3, 0], 0.22, 3)
        g3 = _gear(0.85, 10, ORANGE, [3.0, 0.8, 0], 0.18, 2.5)
        g4 = _gear(0.6, 8, VIOLET, [4.5, -0.8, 0], 0.14, 2)

        # Math symbols orbiting the gears
        syms = VGroup()
        sym_texts = [r"\int", r"\Sigma", r"\pi", r"\infty", r"\sqrt{x}", r"\Delta", r"\theta", r"\lambda"]
        sym_colors = [CYAN, GREEN, ORANGE, M_TEAL, VIOLET, M_BLUE, CYAN, GREEN]
        for i, (s, c) in enumerate(zip(sym_texts, sym_colors)):
            t = MathTex(s, font_size=28, color=c).set_opacity(0.6)
            angle = i * TAU / len(sym_texts)
            t.move_to([3*np.cos(angle), 2*np.sin(angle), 0])
            syms.add(t)

        self.play(FadeIn(g1), FadeIn(g2), FadeIn(g3), FadeIn(g4),
                  *[FadeIn(s, scale=0.5) for s in syms], run_time=0.4)
        self.play(
            Rotate(g1, PI/2, about_point=[-3.5, -0.3, 0]),
            Rotate(g2, -PI/1.5, about_point=[0.3, -0.3, 0]),
            Rotate(g3, PI/1.3, about_point=[3.0, 0.8, 0]),
            Rotate(g4, -PI, about_point=[4.5, -0.8, 0]),
            *[s.animate.shift(RIGHT*0.8 + UP*0.3) for s in syms],
            run_time=1.5)
        self.wait(EXTRA_HOLD)

        gears_all = VGroup(g1, g2, g3, g4, syms)
        self.play(FadeOut(gears_all), FadeOut(logo_grp), run_time=0.4)

        # ════════════════════════════════════════════════════════
        # SCENE 5: Four Pillars (detailed) + Background Riemann
        # s08 (11.50s): "Complete math programs with digital textbooks,
        #   video walkthroughs, thousands of practice problems,
        #   and a personal AI tutor that adapts to EVERY student."
        # ════════════════════════════════════════════════════════

        self.add_sound(SEG + "s08_complete_programs.mp3")

        # Subtle Riemann sum in the background
        bg_ax = Axes(x_range=[0, 2*PI+.5, PI/2], y_range=[-1.5, 1.5, .5],
                     x_length=12, y_length=5, tips=False,
                     axis_config={"color": WHITE, "stroke_width": 1, "stroke_opacity": 0.08})
        bg_cv = bg_ax.plot(lambda x: np.sin(x), x_range=[0, 2*PI],
                           color=VIOLET, stroke_width=1.5, stroke_opacity=0.12)
        bg_rects = VGroup()
        n_rects = 30
        dx = 2*PI/n_rects
        for i in range(n_rects):
            x = i*dx; y = np.sin(x+dx/2)
            h = 5*abs(y)/3.0; w = 12*dx/(2*PI+.5)
            c = CYAN if y >= 0 else ORANGE
            r = Rectangle(width=w, height=h, color=c, fill_color=c, fill_opacity=0.04, stroke_width=0.5, stroke_opacity=0.1)
            cx_p = bg_ax.c2p(x+dx/2, 0)
            r.move_to(cx_p + (UP if y >= 0 else DOWN)*h/2)
            bg_rects.add(r)

        self.play(FadeIn(bg_ax), FadeIn(bg_cv), FadeIn(bg_rects), run_time=0.3)

        # Pillar cards — much more detailed
        def _pillar_card(emoji, title, subtitle, color, features):
            bx = RoundedRectangle(width=2.8, height=4.0, corner_radius=0.12,
                                   color=color, fill_color=BOX, fill_opacity=0.8, stroke_width=2.5)
            # Glow
            glow = RoundedRectangle(width=2.8, height=4.0, corner_radius=0.12,
                                     color=color, fill_opacity=0, stroke_width=6, stroke_opacity=0.12)
            ic = Text(emoji, font_size=42).move_to(bx.get_center() + UP*1.2)
            ttl = Text(title, font_size=20, color=color, weight=BOLD).move_to(bx.get_center() + UP*0.45)
            sub = Text(subtitle, font_size=13, color=WARM).set_opacity(0.6).move_to(bx.get_center() + UP*0.1)
            # Feature bullets
            feats = VGroup()
            for j, f in enumerate(features):
                ft = Text(f"• {f}", font_size=11, color=WARM).set_opacity(0.5)
                ft.move_to(bx.get_center() + DOWN*(0.4 + j*0.3) + LEFT*0.3)
                ft.align_to(bx.get_left() + RIGHT*0.35, LEFT)
                feats.add(ft)
            return VGroup(bx, glow, ic, ttl, sub, feats)

        p1 = _pillar_card("TXT", "Digital Textbook", "Interactive content",
                           M_BLUE, ["Full curriculum", "Searchable", "Mobile-ready"])
        p2 = _pillar_card("VID", "Video Lessons", "Step-by-step",
                           VIOLET, ["Every concept", "Rewindable", "Clear visuals"])
        p3 = _pillar_card("PRB", "Practice Problems", "Auto-graded",
                           ORANGE, ["1000s of problems", "Instant feedback", "Adaptive difficulty"])
        p4 = _pillar_card("AI", "AI Tutor", "Personalized help",
                           M_TEAL, ["Meets students where they are", "Step-by-step hints", "24/7 available"])

        pillars = VGroup(p1, p2, p3, p4).arrange(RIGHT, buff=0.4).move_to([0, -0.2, 0])

        # Appear one at a time with proper timing
        for i, card in enumerate(pillars):
            self.play(FadeIn(card, shift=UP*0.4, scale=0.92), run_time=0.6)
            # Subtle glow pulse on appear
            self.play(card[1].animate.set_stroke(opacity=0.3), run_time=0.15)
            self.play(card[1].animate.set_stroke(opacity=0.12), run_time=0.15)
            self.wait(0.3)

        # Connect them
        conn = Line(pillars[0].get_bottom()+DOWN*0.4, pillars[-1].get_bottom()+DOWN*0.4,
                     color=M_TEAL, stroke_width=3)
        conn_dots = VGroup(*[Dot(pillars[i].get_bottom()+DOWN*0.4, color=M_TEAL, radius=0.06) for i in range(4)])
        conn_txt = Text("ONE INTEGRATED PLATFORM", font_size=22, color=M_TEAL, weight=BOLD)
        conn_txt.next_to(conn, DOWN, 0.15)

        self.play(Create(conn), FadeIn(conn_dots), FadeIn(conn_txt), run_time=0.5)

        # "adapts to EVERY student" — Tier 1 punchline
        every = Text("Adapts to EVERY student", font_size=36, color=GREEN, weight=BOLD)
        every.move_to([0, 3.2, 0])
        every_box = _purple_box(every, buff=0.18)
        self.play(FadeIn(every_box), FadeIn(every), run_time=0.4)
        self.play(*[Indicate(c, color=c[0].color, scale_factor=1.03) for c in pillars], run_time=0.5)
        self.wait(1.5)

        scene5 = VGroup(pillars, conn, conn_dots, conn_txt, every, every_box,
                          bg_ax, bg_cv, bg_rects)
        self.play(FadeOut(scene5), run_time=0.4)

        # ════════════════════════════════════════════════════════
        # SCENE 6: AI Tutor Demo (polished)
        # s09 (1.07s): "...AI tutor that adapts..." (continuation)
        # s10 (2.28s): "When a student gets stuck, the AI tutor
        #              meets them right where they are."
        # s11 (0.84s): "Step by step."
        # s12 (0.66s): "No judgment."
        # s13 (1.31s): "No falling through the cracks."
        # ════════════════════════════════════════════════════════

        # Panel frame
        panel_frame = RoundedRectangle(width=11, height=5.5, corner_radius=0.15,
                                        color=M_TEAL, fill_color=BOX, fill_opacity=0.85, stroke_width=2.5)
        panel_glow = RoundedRectangle(width=11, height=5.5, corner_radius=0.15,
                                       color=M_TEAL, fill_opacity=0, stroke_width=8, stroke_opacity=0.1)
        panel_frame.move_to([0, -0.3, 0])
        panel_glow.move_to([0, -0.3, 0])

        # AI badge
        badge = VGroup(
            RoundedRectangle(width=1.8, height=0.45, corner_radius=0.1,
                              color=M_TEAL, fill_color=M_TEAL, fill_opacity=0.2, stroke_width=1.5),
            Text("AI Tutor", font_size=14, color=M_TEAL, weight=BOLD))
        badge[1].move_to(badge[0])
        badge.move_to(panel_frame.get_top() + DOWN*0.4 + LEFT*3.5)

        # Problem at top
        prob = MathTex(r"3x + 7 = 22", font_size=52, color=WHITE).move_to([0, 2.8, 0])
        stuck_ind = Text("⚠ Student stuck here", font_size=16, color=ORANGE, weight=BOLD)
        stuck_ind.next_to(prob, RIGHT, 0.5)

        self.add_sound(SEG + "s09_ai_tutor_adapts.mp3")
        self.play(Write(prob), run_time=0.3)
        self.play(FadeIn(stuck_ind, shift=LEFT*0.2), run_time=0.2)
        self.wait(0.4)

        self.add_sound(SEG + "s10_every_student2.mp3")
        self.play(FadeIn(panel_frame), FadeIn(panel_glow), FadeIn(badge), run_time=0.3)

        # Step-by-step solution walkthrough
        hint1 = Text("What operation undoes adding 7?", font_size=18, color=WARM).set_opacity(0.8)
        hint1.move_to([-2, 0.6, 0])
        self.play(FadeIn(hint1, shift=LEFT*0.3), run_time=0.4)
        self.wait(0.3)

        step1 = MathTex(r"3x + 7 - 7 = 22 - 7", font_size=36, color=CYAN).move_to([0, 0, 0])
        self.play(Write(step1), run_time=0.5)
        self.wait(0.2)

        step2 = MathTex(r"3x = 15", font_size=40, color=CYAN).move_to([0, -0.7, 0])
        self.play(Write(step2), run_time=0.4)

        self.add_sound(SEG + "s11_step_by_step.mp3")
        hint2 = Text("Now divide both sides by 3!", font_size=18, color=WARM).set_opacity(0.8)
        hint2.move_to([-1.5, -1.4, 0])
        self.play(FadeIn(hint2, shift=LEFT*0.3), run_time=0.3)
        self.wait(0.3)

        answer = MathTex(r"x = 5", font_size=48, color=GREEN).move_to([0, -2.1, 0])
        ans_box = _purple_box(answer, buff=0.15, opacity=0.5)
        self.play(Write(answer), Create(ans_box), run_time=0.3)

        self.add_sound(SEG + "s12_no_judgment.mp3")
        self.play(Flash(answer.get_center(), color=GREEN, line_length=0.5, num_lines=14),
                  run_time=0.3)
        # Replace stuck indicator with solved
        solved = Text("✓ Solved!", font_size=16, color=GREEN, weight=BOLD).move_to(stuck_ind)
        self.play(FadeOut(stuck_ind), FadeIn(solved), run_time=0.2)
        self.wait(0.3)

        self.add_sound(SEG + "s13_no_cracks.mp3")
        # Text overlay — Tier 3 callout
        no_cracks = Text("No falling through the cracks.", font_size=24,
                          color=GREEN, weight=BOLD).move_to([0, 3.2, 0])
        nc_box = _purple_box(no_cracks, buff=0.12, opacity=0.4)
        self.play(FadeIn(nc_box), FadeIn(no_cracks), run_time=0.3)
        self.wait(0.8)

        scene6 = VGroup(panel_frame, panel_glow, badge, prob, solved,
                          hint1, step1, step2, hint2, answer, ans_box, no_cracks, nc_box)
        self.play(FadeOut(scene6), run_time=0.4)

        # ════════════════════════════════════════════════════════
        # SCENE 7: Teacher Dashboard (STAYS ON SCREEN)
        # s14 (4.61s): "Teachers get real-time dashboards showing
        #              exactly where each student needs help,"
        # s15 (1.93s): "not just a grade at the end of the unit."
        # ════════════════════════════════════════════════════════

        self.add_sound(SEG + "s14_dashboards.mp3")

        # Dashboard frame
        df = RoundedRectangle(width=12.5, height=6.5, corner_radius=0.15,
                               color=M_BLUE, fill_color=BOX, fill_opacity=0.85, stroke_width=2.5)
        df_glow = RoundedRectangle(width=12.5, height=6.5, corner_radius=0.15,
                                    color=M_BLUE, fill_opacity=0, stroke_width=8, stroke_opacity=0.1)
        dt = Text("Teacher Dashboard", font_size=30, color=M_BLUE, weight=BOLD)
        dt.move_to(df.get_top() + DOWN*0.45)

        # Live indicator
        live_dot = Circle(radius=0.08, color=GREEN, fill_color=GREEN, fill_opacity=0.8)
        live_txt = Text("LIVE", font_size=12, color=GREEN, weight=BOLD)
        live = VGroup(live_dot, live_txt).arrange(RIGHT, buff=0.1)
        live.move_to(df.get_top() + DOWN*0.45 + RIGHT*4.5)

        # Class period label
        period = Text("Period 3 — Algebra 1", font_size=14, color=WARM).set_opacity(0.5)
        period.move_to(df.get_top() + DOWN*0.8)

        # Student bars with avatars
        students = [
            ("Alex", 0.95, GREEN, "A"),
            ("Maria", 0.82, M_TEAL, "M"),
            ("James", 0.41, ORANGE, "J"),
            ("Sofia", 0.91, GREEN, "S"),
            ("Tyler", 0.28, RED, "T"),
            ("Emma", 0.73, M_TEAL, "E"),
            ("Noah", 0.60, M_BLUE, "N"),
        ]

        bars = VGroup(); names = VGroup(); pcts = VGroup(); avatars = VGroup()
        for i, (nm, p, c, init) in enumerate(students):
            x = -5.2 + i * 1.5
            h = p * 3.2

            # Avatar circle
            av = Circle(radius=0.25, color=c, fill_color=c, fill_opacity=0.2, stroke_width=1.5)
            av_txt = Text(init, font_size=14, color=c, weight=BOLD)
            av_txt.move_to(av)
            av_grp = VGroup(av, av_txt).move_to([x, 2.6, 0])
            avatars.add(av_grp)

            # Bar
            bar = Rectangle(width=1.0, height=h, color=c, fill_color=c, fill_opacity=0.45, stroke_width=2)
            bar.move_to([x, -0.8 + h/2, 0])
            bars.add(bar)

            # Name
            n = Text(nm, font_size=12, color=WARM).set_opacity(0.6).move_to([x, -1.2, 0])
            names.add(n)

            # Percentage
            pt = Text(f"{int(p*100)}%", font_size=15, color=c, weight=BOLD)
            pt.next_to(bar, UP, 0.08)
            pcts.add(pt)

        self.play(FadeIn(df), FadeIn(df_glow), FadeIn(dt), FadeIn(live), FadeIn(period), run_time=0.4)
        self.play(*[FadeIn(a, scale=0.8) for a in avatars], run_time=0.3)
        self.play(*[GrowFromEdge(b, DOWN) for b in bars], run_time=1.0)
        self.play(FadeIn(names), FadeIn(pcts), run_time=0.4)
        self.wait(0.5)

        # Alert highlights on struggling students
        alert_j = SurroundingRectangle(VGroup(bars[2], names[2], avatars[2]),
                                        color=ORANGE, stroke_width=2.5, buff=0.12, corner_radius=0.08)
        alert_t = SurroundingRectangle(VGroup(bars[4], names[4], avatars[4]),
                                        color=RED, stroke_width=2.5, buff=0.12, corner_radius=0.08)
        atxt = Text("⚠ Needs attention", font_size=16, color=RED, weight=BOLD)
        atxt.move_to([4.5, 2.0, 0])
        atxt2 = Text("⚠ At risk", font_size=16, color=ORANGE, weight=BOLD)
        atxt2.move_to([4.5, 1.5, 0])

        self.play(Create(alert_j), Create(alert_t), FadeIn(atxt), FadeIn(atxt2), run_time=0.5)

        # Pulse alerts
        self.play(alert_j.animate.set_stroke(opacity=0.3), alert_t.animate.set_stroke(opacity=0.3), run_time=0.3)
        self.play(alert_j.animate.set_stroke(opacity=1), alert_t.animate.set_stroke(opacity=1), run_time=0.3)

        # s15 plays while dashboard is STILL visible
        self.add_sound(SEG + "s15_not_just_grade.mp3")

        # Tier 3 callout text overlay
        not_grade = Text("Not just a grade. Real-time insight.", font_size=24,
                          color=CYAN, weight=BOLD).move_to([0, -3.0, 0])
        ng_box = _purple_box(not_grade, buff=0.12, opacity=0.4)
        self.play(FadeIn(ng_box), FadeIn(not_grade), run_time=0.3)
        self.wait(2.0)

        scene7 = VGroup(df, df_glow, dt, live, period, bars, names, pcts, avatars,
                          alert_j, alert_t, atxt, atxt2, not_grade, ng_box)
        self.play(FadeOut(scene7), run_time=0.4)

        # ════════════════════════════════════════════════════════
        # SCENE 8: Course Pyramid
        # s16 (1.55s): "Pre-Algebra through Calculus."
        # s17 (2.01s): "Every course built on one platform."
        # ════════════════════════════════════════════════════════

        self.add_sound(SEG + "s16_prealg_calc.mp3")

        # Building blocks forming a pyramid
        courses_pyr = [
            # Bottom row (foundation)
            [("Pre-Algebra", "#6366F1", -2.5, -2.0), ("Algebra 1", "#8B5CF6", 0, -2.0), ("Geometry", "#A855F7", 2.5, -2.0)],
            # Middle row
            [("Algebra 2", "#C084FC", -1.25, -0.3), ("Precalculus", M_TEAL, 1.25, -0.3)],
            # Top
            [("Calculus", M_BLUE, 0, 1.4)],
        ]

        pyr_blocks = VGroup()
        for row in courses_pyr:
            for nm, c, x, y in row:
                bx = RoundedRectangle(width=2.2, height=1.3, corner_radius=0.08,
                                       color=c, fill_color=BOX, fill_opacity=0.65, stroke_width=2.5)
                glow = RoundedRectangle(width=2.2, height=1.3, corner_radius=0.08,
                                         color=c, fill_opacity=0, stroke_width=5, stroke_opacity=0.1)
                tx = Text(nm, font_size=16, color=c, weight=BOLD)
                blk = VGroup(bx, glow, tx).move_to([x, y, 0])
                pyr_blocks.add(blk)

        # Build from bottom up
        for i in range(3):  # bottom row
            self.play(FadeIn(pyr_blocks[i], shift=UP*0.3, scale=0.9), run_time=0.15)
        self.wait(0.2)

        self.add_sound(SEG + "s17_one_platform.mp3")

        for i in range(3, 5):  # middle row
            self.play(FadeIn(pyr_blocks[i], shift=UP*0.3, scale=0.9), run_time=0.15)
        self.play(FadeIn(pyr_blocks[5], shift=UP*0.3, scale=0.9), run_time=0.2)

        # Crown it
        crown_txt = Text("ONE PLATFORM", font_size=28, color=M_TEAL, weight=BOLD).move_to([0, 2.8, 0])
        crown_box = _purple_box(crown_txt, buff=0.15)
        self.play(FadeIn(crown_box), FadeIn(crown_txt), run_time=0.3)
        self.play(*[Indicate(b, color=b[0].color, scale_factor=1.04) for b in pyr_blocks], run_time=0.5)
        self.wait(0.8)

        scene8 = VGroup(pyr_blocks, crown_txt, crown_box)
        self.play(FadeOut(scene8), run_time=0.4)

        # ════════════════════════════════════════════════════════
        # SCENE 9: Not Bolted On (polished)
        # s18 (2.16s): "Not a textbook with a website bolted on."
        # s19 (2.91s): "A complete system built by educators
        #              who have been in the classroom."
        # ════════════════════════════════════════════════════════

        self.add_sound(SEG + "s18_not_bolted.mp3")

        div = Line([0, -3.5, 0], [0, 3.0, 0], color=WHITE, stroke_width=1.5, stroke_opacity=0.2)

        # Traditional side — messier, disconnected
        ol = Text("Traditional", font_size=26, color=RED, weight=BOLD).move_to([-3.5, 3.0, 0])
        old_items = VGroup()
        old_labels = ["Textbook", "Separate\nWebsite", "YouTube\nVideos", "Manual\nGrading"]
        for i, lbl in enumerate(old_labels):
            bx = RoundedRectangle(width=2.6, height=0.85, corner_radius=0.06,
                                   color="#444", fill_color="#0a0a0a", fill_opacity=0.5, stroke_width=1.5)
            tx = Text(lbl.replace(chr(10), ' '), font_size=13, color="#777")
            old_items.add(VGroup(bx, tx).move_to([-3.5 + (i%2)*0.3, 1.8 - i*1.0, 0]))

        # Disconnected lines between old items
        disc = VGroup()
        for i in range(len(old_items)-1):
            dl = DashedLine(old_items[i].get_bottom(), old_items[i+1].get_top(),
                            color="#444", stroke_width=1, dash_length=0.1)
            disc.add(dl)

        # Meridian side — connected, polished
        nl = Text("Meridian", font_size=26, color=M_TEAL, weight=BOLD).move_to([3.5, 3.0, 0])
        new_items = VGroup()
        new_data = [("Textbook", M_BLUE), ("Videos", VIOLET),
                    ("Problems", ORANGE), ("AI Tutor", M_TEAL)]
        for i, (lbl, c) in enumerate(new_data):
            bx = RoundedRectangle(width=2.6, height=0.85, corner_radius=0.06,
                                   color=c, fill_color=BOX, fill_opacity=0.6, stroke_width=2.5)
            glow = RoundedRectangle(width=2.6, height=0.85, corner_radius=0.06,
                                     color=c, fill_opacity=0, stroke_width=5, stroke_opacity=0.08)
            tx = Text(lbl, font_size=14, color=c, weight=BOLD)
            new_items.add(VGroup(bx, glow, tx).move_to([3.5, 1.8 - i*1.0, 0]))

        nconn = VGroup(*[Line(new_items[i].get_bottom(), new_items[i+1].get_top(),
                              color=M_TEAL, stroke_width=2.5, stroke_opacity=0.7) for i in range(3)])

        self.play(FadeIn(div), FadeIn(ol), FadeIn(nl),
                  *[FadeIn(b, shift=DOWN*0.15) for b in old_items],
                  *[FadeIn(b, shift=DOWN*0.15) for b in new_items],
                  *[Create(d) for d in disc], run_time=0.5)
        self.play(*[Create(c) for c in nconn], run_time=0.3)

        xo = Text("✗", font_size=72, color=RED, weight=BOLD).set_opacity(0.6).move_to([-3.5, -2.2, 0])
        ck = Text("✓", font_size=72, color=GREEN, weight=BOLD).set_opacity(0.6).move_to([3.5, -2.2, 0])
        self.play(FadeIn(xo, scale=0.5), FadeIn(ck, scale=0.5), run_time=0.3)
        self.wait(0.8)

        self.add_sound(SEG + "s19_complete_system.mp3")
        # Callout
        sys_txt = Text("Built by educators. For educators.", font_size=24,
                        color=GREEN, weight=BOLD).move_to([0, -3.2, 0])
        sys_box = _purple_box(sys_txt, buff=0.12, opacity=0.4)
        self.play(FadeIn(sys_box), FadeIn(sys_txt), run_time=0.3)
        self.wait(2.2)

        scene9 = VGroup(div, ol, nl, old_items, new_items, disc, nconn, xo, ck, sys_txt, sys_box)
        self.play(FadeOut(scene9), run_time=0.4)

        # ════════════════════════════════════════════════════════
        # SCENE 10: Emotional Closer
        # s20 (3.94s): "Because every student deserves a program
        #              that actually meets them where they are."
        # ════════════════════════════════════════════════════════

        self.add_sound(SEG + "s20_every_deserves.mp3")

        # Three text lines with visual weight — Tier 1 style
        c1 = Text("Every student.", font_size=52, color=WHITE, weight=BOLD).move_to([0, 1.5, 0])
        c2 = Text("Every level.", font_size=52, color=M_TEAL, weight=BOLD).move_to([0, 0, 0])
        c3 = Text("One program that adapts.", font_size=52, color=M_BLUE, weight=BOLD).move_to([0, -1.5, 0])

        # Boxes behind each
        c1_box = _purple_box(c1, buff=0.15, opacity=0.3)
        c2_box = _purple_box(c2, buff=0.15, opacity=0.3)
        c3_box = _purple_box(c3, buff=0.15, opacity=0.3)

        self.play(FadeIn(c1_box), FadeIn(c1, shift=UP*0.2), run_time=0.5)
        self.wait(0.4)
        self.play(FadeIn(c2_box), FadeIn(c2, shift=UP*0.2), run_time=0.5)
        self.wait(0.4)
        self.play(FadeIn(c3_box), FadeIn(c3, shift=UP*0.2), run_time=0.5)
        self.wait(0.4)

        # Subtle student silhouettes returning — the "meeting them" visual
        ret_students = VGroup()
        ret_colors = [GREEN, M_BLUE, ORANGE, M_TEAL, VIOLET]
        for i, c in enumerate(ret_colors):
            s = _student_silhouette(c, "", -4 + i*2, -3.0)
            s.set_opacity(0.25)
            ret_students.add(s)
        self.play(*[FadeIn(s, shift=UP*0.2) for s in ret_students], run_time=0.4)

        self.play(Circumscribe(VGroup(c1_box, c2_box, c3_box), color=M_TEAL, run_time=0.7))
        self.wait(0.3)

        scene10 = VGroup(c1, c2, c3, c1_box, c2_box, c3_box, ret_students)
        self.play(FadeOut(scene10), run_time=0.4)

        # ════════════════════════════════════════════════════════
        # SCENE 11: End Card (HOLDS until audio done)
        # s21 (0.73s): "Meridian Math."
        # s22 (1.77s): "Mathematics for every student."
        # ════════════════════════════════════════════════════════

        self.add_sound(SEG + "s21_meridian_math.mp3")

        _A2, _B2 = 2.2, 1.5
        lg = ParametricFunction(lambda t: np.array([_A2*np.sin(2*t), _B2*np.sin(3*t)+0.8, 0]),
                                 t_range=[0, TAU, .01], color=M_BLUE, stroke_width=10, stroke_opacity=0.12)
        lc = ParametricFunction(lambda t: np.array([_A2*np.sin(2*t), _B2*np.sin(3*t)+0.8, 0]),
                                 t_range=[0, TAU, .01], color=M_BLUE, stroke_width=2.5, stroke_opacity=0.8)

        en = Text("MERIDIAN MATH", font_size=60, color=M_BLUE, weight=BOLD).move_to([0, -0.8, 0])
        et = Text("Mathematics for every student.", font_size=28, color=WARM).set_opacity(0.7)
        et.next_to(en, DOWN, 0.35)
        eu = Text("meridian-math.org", font_size=26, color=M_TEAL, weight=BOLD).next_to(et, DOWN, 0.45)

        eb = SurroundingRectangle(VGroup(en, et, eu), color=M_BLUE, fill_color=BOX, fill_opacity=0.5,
                                   buff=0.5, corner_radius=0.12, stroke_width=2.5)
        eb_glow = SurroundingRectangle(VGroup(en, et, eu), color=M_BLUE, fill_opacity=0,
                                        buff=0.5, corner_radius=0.12, stroke_width=8, stroke_opacity=0.1)

        self.play(Create(lc, run_time=0.8), FadeIn(lg, run_time=0.6))
        self.play(FadeIn(eb), FadeIn(eb_glow), FadeIn(en, scale=0.95), run_time=0.4)

        self.add_sound(SEG + "s22_tagline.mp3")
        self.play(FadeIn(et, shift=UP*0.1), run_time=0.3)
        self.play(FadeIn(eu), run_time=0.2)
        self.play(Circumscribe(eb, color=M_BLUE, run_time=0.7))

        # HOLD on end card — this is the key fix
        self.wait(8.0)

        self.play(FadeOut(Group(*self.mobjects)), run_time=1.0)
