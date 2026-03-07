"""
Meridian Math × Orbital — District Promo V4 (FINAL)
====================================================
Proper timing. Fewer scenes, better execution. Audio embedded via add_sound().

Audio: meridian_promo_v4.mp3 (~65s, Hale, stability=0.38, style=0.55, speed=0.93)
Music: bg_synthwave.mp3 mixed via ffmpeg post-render

3-second pre-roll (music only, intro visual), then TTS starts.
Total video: ~68s

Render:
  cd ~/Desktop/Orbital/orbital_factory && source venv/bin/activate
  PATH="/Library/TeX/texbin:$PATH" manim render prototypes/meridian_promo_v4.py MeridianPromoV4 \
    -o meridian_promo_v4.mp4 --format mp4 -r 1920,1080 --frame_rate 60 --flush_cache
"""
from manim import *
import numpy as np
import random

config.frame_width = 14.2
config.frame_height = 8.0

VIOLET = "#8B5CF6"
CYAN = "#22D3EE"
GREEN = "#39FF14"
ORANGE = "#F97316"
M_BLUE = "#3B82F6"
M_TEAL = "#14B8A6"
WARM = "#F8FAFC"
BOX = "#1a1130"
GRID = "#1a1a3a"
E_CYAN = "#00E5FF"
RED = "#EF4444"
FW, FH = 14.2, 8.0

TTS = "output/tts/meridian_promo_v4.mp3"


def _grid(fw=20, fh=14, sp=0.8):
    g = VGroup()
    for x in np.arange(-fw/2, fw/2+.1, sp):
        g.add(Line([x,-fh/2,0],[x,fh/2,0], color=GRID, stroke_width=0.5, stroke_opacity=0.15))
    for y in np.arange(-fh/2, fh/2+.1, sp):
        g.add(Line([-fw/2,y,0],[fw/2,y,0], color=GRID, stroke_width=0.5, stroke_opacity=0.15))
    return g


def _gear(r, n, color, c, tl=0.14, sw=2.5):
    p = [Circle(radius=r, color=color, stroke_width=sw, fill_color=BOX, fill_opacity=0.4).move_to(c),
         Dot(radius=0.06, color=color, fill_opacity=0.8).move_to(c)]
    for i in range(n):
        a = i*TAU/n
        ca = np.array(c)
        ip = ca + r*np.array([np.cos(a), np.sin(a), 0])
        op = ca + (r+tl)*np.array([np.cos(a), np.sin(a), 0])
        pp = np.array([-np.sin(a), np.cos(a), 0])
        tw = 0.08
        p.append(Polygon(ip+pp*tw, ip-pp*tw, op-pp*tw*.7, op+pp*tw*.7,
                         color=color, stroke_width=sw-.5, fill_color=color, fill_opacity=0.3))
    return VGroup(*p)


class MeridianPromoV4(MovingCameraScene):
    def construct(self):
        self.camera.background_color = BLACK
        self.camera.frame.set(width=FW, height=FH)

        bg = _grid()
        self.add(bg)

        # Border
        def _b():
            cf = self.camera.frame
            return Rectangle(width=cf.width-.2, height=cf.height-.2, color=M_BLUE,
                             stroke_width=2.5, stroke_opacity=0.6, fill_opacity=0).move_to(cf.get_center())
        def _bg():
            cf = self.camera.frame
            return Rectangle(width=cf.width-.15, height=cf.height-.15, color=M_BLUE,
                             stroke_width=6, stroke_opacity=0.1, fill_opacity=0).move_to(cf.get_center())
        def _wm():
            cf = self.camera.frame
            t = Text("MERIDIAN × ORBITAL", font_size=11, color=WHITE, weight=BOLD).set_opacity(0.3)
            t.move_to([cf.get_center()[0]-cf.width/2+1, cf.get_center()[1]-cf.height/2+.25, 0])
            return t

        self.add(always_redraw(_bg), always_redraw(_b), always_redraw(_wm))

        # ══════════════════════════════════════════
        # PRE-ROLL: Collab intro (0-3s, no voice)
        # ══════════════════════════════════════════

        mer = Text("MERIDIAN", font_size=48, color=M_BLUE, weight=BOLD).move_to([-3, 0, 0])
        cx = Text("×", font_size=56, color=WHITE, weight=BOLD).move_to(ORIGIN)
        _A, _B = 0.9, 0.65
        liss = ParametricFunction(lambda t: np.array([_A*np.sin(2*t)+3, _B*np.sin(3*t), 0]),
                                   t_range=[0, TAU, .01], color=E_CYAN, stroke_width=2.5)
        liss_g = ParametricFunction(lambda t: np.array([_A*np.sin(2*t)+3, _B*np.sin(3*t), 0]),
                                     t_range=[0, TAU, .01], color=E_CYAN, stroke_width=8, stroke_opacity=.15)
        orb = Text("ORBITAL", font_size=48, color=E_CYAN, weight=BOLD).move_to([3, -1.1, 0])

        self.play(FadeIn(mer, shift=RIGHT*.2), FadeIn(cx, scale=.3),
                  Create(liss), FadeIn(liss_g), FadeIn(orb, shift=LEFT*.2), run_time=1.2)
        self.play(Flash(ORIGIN, color=VIOLET, line_length=.6, num_lines=16, run_time=.3),
                  cx.animate.set_color(VIOLET), run_time=.3)
        self.wait(0.8)
        intro_all = Group(mer, cx, liss, liss_g, orb)
        self.play(FadeOut(intro_all, shift=UP*.4), run_time=.4)

        # ══════════════════════════════════════════
        # START AUDIO at t≈3.0s
        # ══════════════════════════════════════════
        self.add_sound(TTS)

        # ══════════════════════════════════════════
        # ACT 1: Different Paces (0-5s of audio)
        # "Every student learns at a different pace.
        #  The problem is, most math programs don't."
        # ══════════════════════════════════════════

        line = Line([-5.5,0,0],[5.5,0,0], color=WHITE, stroke_width=2, stroke_opacity=.4)
        ticks = VGroup(*[Line([x,-.12,0],[x,.12,0], color=WHITE, stroke_width=1.5, stroke_opacity=.3)
                         for x in range(-5,6)])

        dot_a = Dot([-4.5,0,0], color=GREEN, radius=.18).set_glow_factor(.8)
        dot_b = Dot([-4.5,0,0], color=M_BLUE, radius=.18).set_glow_factor(.8)
        dot_c = Dot([-4.5,0,0], color=ORANGE, radius=.18).set_glow_factor(.8)
        la = Text("A", font_size=20, color=GREEN, weight=BOLD).next_to(dot_a, UP, .3)
        lb = Text("B", font_size=20, color=M_BLUE, weight=BOLD).next_to(dot_b, UP, .6)
        lc = Text("C", font_size=20, color=ORANGE, weight=BOLD).next_to(dot_c, UP, .9)

        self.play(Create(line), FadeIn(ticks), run_time=.5)
        self.play(FadeIn(dot_a), FadeIn(dot_b), FadeIn(dot_c),
                  FadeIn(la), FadeIn(lb), FadeIn(lc), run_time=.4)
        self.play(
            dot_a.animate.move_to([4.5,0,0]), la.animate.move_to([4.5,.48,0]),
            dot_b.animate.move_to([1.5,0,0]), lb.animate.move_to([1.5,.78,0]),
            dot_c.animate.move_to([-1,0,0]),  lc.animate.move_to([-1,1.08,0]),
            run_time=3.0, rate_func=smooth)

        # Hold — audio is still saying "most math programs don't"
        self.wait(1.1)

        act1 = VGroup(line, ticks, dot_a, dot_b, dot_c, la, lb, lc)
        # Don't fade yet — transitions into Act 2

        # ══════════════════════════════════════════
        # ACT 2: Domino / Missed Step (5-12s of audio)
        # "One textbook. One speed. And if you miss
        #  a step, good luck catching up."
        # ══════════════════════════════════════════

        self.play(FadeOut(act1, shift=UP*.3), run_time=.4)

        # 6 lesson blocks
        blocks = VGroup()
        for i, lbl in enumerate(["1.1","1.2","1.3","1.4","1.5","1.6"]):
            bx = RoundedRectangle(width=1.5, height=2.0, corner_radius=.08,
                                   color=WHITE, fill_color=BOX, fill_opacity=.7, stroke_width=2)
            tx = Text(lbl, font_size=22, color=WHITE)
            blocks.add(VGroup(bx, tx).move_to([-5 + i*2, 0, 0]))

        self.play(*[FadeIn(b, shift=UP*.2) for b in blocks], run_time=.6)
        self.wait(1.0)  # "One textbook. One speed."

        # Block 3 goes red
        self.play(
            blocks[2][0].animate.set_color(RED).set_fill(RED, .3),
            blocks[2][1].animate.set_color(RED),
            Flash(blocks[2].get_center(), color=RED, line_length=.5, num_lines=12),
            run_time=.4)
        self.wait(0.4)  # "And if you miss a step,"

        # Chain reaction — blocks 3+ topple
        for i in range(2, 6):
            self.play(
                Rotate(blocks[i], PI/5, about_point=blocks[i].get_bottom()),
                blocks[i].animate.set_opacity(.15 if i > 2 else .3),
                run_time=.2)

        q = Text("?", font_size=72, color=RED, weight=BOLD).move_to([2, 0, 0])
        self.play(FadeIn(q, scale=.3), run_time=.3)
        self.wait(1.2)  # "good luck catching up."

        self.play(FadeOut(VGroup(blocks, q)), run_time=.4)

        # ══════════════════════════════════════════
        # ACT 3: Meridian Reveal (12-15s of audio)
        # "We built Meridian to fix that."
        # ══════════════════════════════════════════

        mer_logo = Text("MERIDIAN", font_size=72, color=M_BLUE, weight=BOLD)
        mer_sub = Text("M A T H", font_size=22, color=M_TEAL, weight=BOLD).set_opacity(.8)
        mer_sub.next_to(mer_logo, DOWN, .25)

        self.play(FadeIn(mer_logo, scale=1.1),
                  Flash(ORIGIN, color=M_BLUE, line_length=.8, num_lines=20, run_time=.4),
                  run_time=.5)
        self.play(FadeIn(mer_sub), run_time=.3)
        self.play(Circumscribe(mer_logo, color=M_TEAL, run_time=.6))

        # Gears — "everything connects" (runs during silence gap before pillars)
        self.wait(0.3)
        self.play(FadeOut(VGroup(mer_logo, mer_sub), shift=UP*.3), run_time=.3)

        g1 = _gear(1.3, 14, M_BLUE, [-2.2, 0, 0], .24, 3)
        g2 = _gear(.9, 10, M_TEAL, [.4, 0, 0], .2, 3)
        g3 = _gear(.65, 8, ORANGE, [2.5, .9, 0], .16, 2.5)

        self.play(FadeIn(g1), FadeIn(g2), FadeIn(g3), run_time=.3)
        self.play(
            Rotate(g1, PI/2, about_point=[-2.2,0,0]),
            Rotate(g2, -PI/1.8, about_point=[.4,0,0]),
            Rotate(g3, PI/1.5, about_point=[2.5,.9,0]),
            run_time=1.5)
        self.play(FadeOut(VGroup(g1, g2, g3)), run_time=.3)

        # ══════════════════════════════════════════
        # ACT 4: Four Pillars (15-27s of audio)
        # "Complete math programs...adapts to EVERY student."
        # This is 12 seconds — take our time
        # ══════════════════════════════════════════

        pillars_data = [
            ("📖", "Digital\nTextbook", M_BLUE),
            ("🎬", "Video\nLessons", VIOLET),
            ("✏️", "Practice\nProblems", ORANGE),
            ("🤖", "AI\nTutor", M_TEAL),
        ]

        pgrp = VGroup()
        for emoji, label, color in pillars_data:
            bx = RoundedRectangle(width=2.6, height=3.2, corner_radius=.12,
                                   color=color, fill_color=BOX, fill_opacity=.75, stroke_width=2.5)
            ic = Text(emoji, font_size=48).move_to(bx.get_center() + UP*.5)
            lb = Text(label, font_size=20, color=color, weight=BOLD).move_to(bx.get_center() + DOWN*.6)
            pgrp.add(VGroup(bx, ic, lb))
        pgrp.arrange(RIGHT, buff=.5).move_to(ORIGIN)

        # Appear one at a time — ~1s per pillar
        for card in pgrp:
            self.play(FadeIn(card, shift=UP*.3, scale=.9), run_time=.6)
            self.wait(.6)

        # Connect
        conn = Line(pgrp[0].get_bottom()+DOWN*.3, pgrp[-1].get_bottom()+DOWN*.3,
                     color=M_TEAL, stroke_width=3)
        conn_txt = Text("ONE PLATFORM", font_size=24, color=M_TEAL, weight=BOLD)
        conn_txt.next_to(conn, DOWN, .15)
        self.play(Create(conn), FadeIn(conn_txt), run_time=.5)

        # Pulse
        self.play(*[Indicate(c, color=c[0].color, scale_factor=1.03) for c in pgrp], run_time=.5)
        self.wait(1.5)  # Hold while "adapts to EVERY student" finishes

        self.play(FadeOut(VGroup(pgrp, conn, conn_txt)), run_time=.4)

        # Quick Riemann sum montage — shows off our rendering
        r_ax = Axes(x_range=[0, 2*PI+.5, PI/2], y_range=[-1.5,1.5,.5],
                    x_length=10, y_length=5, tips=False,
                    axis_config={"color":WHITE,"stroke_width":1.5,"stroke_opacity":.5})
        r_cv = r_ax.plot(lambda x: np.sin(x), x_range=[0,2*PI], color=VIOLET, stroke_width=3)

        def _rects(n, op=.4):
            rs = VGroup()
            dx = 2*PI/n
            for i in range(n):
                x = i*dx; y = np.sin(x+dx/2)
                h = r_ax.y_length*abs(y)/3.0; w = r_ax.x_length*dx/(2*PI+.5)
                c = CYAN if y >= 0 else ORANGE
                r = Rectangle(width=w, height=h, color=c, fill_color=c, fill_opacity=op, stroke_width=1.2)
                cx = r_ax.c2p(x+dx/2, 0)
                r.move_to(cx + (UP if y >= 0 else DOWN)*h/2)
                rs.add(r)
            return rs

        self.play(Create(r_ax, run_time=.3), Create(r_cv, run_time=.5), run_time=.5)
        r8 = _rects(8, .3); r20 = _rects(20, .35); r40 = _rects(40, .4)
        self.play(FadeIn(r8), run_time=.3)
        self.play(ReplacementTransform(r8, r20), run_time=.3)
        self.play(ReplacementTransform(r20, r40), run_time=.3)
        self.wait(.2)
        self.play(FadeOut(VGroup(r_ax, r_cv, r40)), run_time=.3)

        # ══════════════════════════════════════════
        # ACT 5: AI Tutor Demo (27-34s of audio)
        # "When a student gets stuck...no falling through the cracks."
        # ══════════════════════════════════════════

        prob = MathTex(r"3x + 7 = 22", font_size=56, color=WHITE).move_to([0, 2.8, 0])
        stuck = Text("Student is stuck", font_size=20, color=ORANGE, weight=BOLD)
        stuck.set_opacity(.8).next_to(prob, UP, .25)
        prob_glow = SurroundingRectangle(prob, color=RED, fill_color=RED, fill_opacity=.05,
                                          buff=.2, corner_radius=.1, stroke_width=2)

        self.play(Write(prob), FadeIn(stuck), Create(prob_glow), run_time=.5)
        self.wait(.5)

        panel = RoundedRectangle(width=9, height=4.5, corner_radius=.15,
                                  color=M_TEAL, fill_color=BOX, fill_opacity=.85, stroke_width=2).move_to([0,-.8,0])
        badge = VGroup(
            RoundedRectangle(width=1.6, height=.4, corner_radius=.1,
                              color=M_TEAL, fill_color=M_TEAL, fill_opacity=.2, stroke_width=1.5),
            Text("AI Tutor", font_size=14, color=M_TEAL, weight=BOLD))
        badge[1].move_to(badge[0])
        badge.move_to(panel.get_top() + DOWN*.35 + LEFT*3)

        m1 = Text("What operation undoes adding 7?", font_size=20, color=WARM).move_to([-.3,.2,0])
        s1 = MathTex(r"3x + 7 - 7 = 22 - 7", font_size=38, color=CYAN).move_to([0,-.4,0])
        s2 = MathTex(r"3x = 15", font_size=38, color=CYAN).move_to([0,-1.1,0])
        m2 = Text("Now divide both sides by 3!", font_size=20, color=WARM).move_to([0,-1.7,0])
        s3 = MathTex(r"x = 5", font_size=48, color=GREEN).move_to([0,-2.4,0])

        self.play(FadeIn(panel), FadeIn(badge), run_time=.3)
        self.play(FadeIn(m1, shift=LEFT*.3), run_time=.4)
        self.wait(.3)
        self.play(Write(s1), run_time=.5)
        self.wait(.3)
        self.play(Write(s2), run_time=.4)
        self.play(FadeIn(m2, shift=LEFT*.3), run_time=.3)
        self.wait(.3)
        self.play(Write(s3), run_time=.3)
        abox = SurroundingRectangle(s3, color=GREEN, fill_color=GREEN, fill_opacity=.1,
                                     buff=.15, corner_radius=.08, stroke_width=2.5)
        self.play(Create(abox),
                  Flash(s3.get_center(), color=GREEN, line_length=.5, num_lines=14),
                  prob_glow.animate.set_color(GREEN), run_time=.4)

        solved = Text("Solved!", font_size=20, color=GREEN, weight=BOLD).move_to(stuck)
        self.play(FadeOut(stuck), FadeIn(solved), run_time=.2)
        self.wait(1.0)  # "No judgment. No falling through the cracks."

        self.play(FadeOut(VGroup(prob, solved, prob_glow, panel, badge,
                                  m1, s1, s2, m2, s3, abox)), run_time=.4)

        # ══════════════════════════════════════════
        # ACT 6: Teacher Dashboard (34-43s of audio)
        # "Teachers get real-time dashboards..."
        # ══════════════════════════════════════════

        df = RoundedRectangle(width=12, height=6, corner_radius=.15,
                               color=M_BLUE, fill_color=BOX, fill_opacity=.85, stroke_width=2).move_to(ORIGIN)
        dt = Text("Teacher Dashboard", font_size=28, color=M_BLUE, weight=BOLD)
        dt.move_to(df.get_top() + DOWN*.4)
        live = VGroup(
            Circle(radius=.08, color=GREEN, fill_color=GREEN, fill_opacity=.8),
            Text("LIVE", font_size=12, color=GREEN, weight=BOLD)
        ).arrange(RIGHT, buff=.1).move_to(df.get_top() + DOWN*.4 + RIGHT*4)

        students = ["Alex","Maria","James","Sofia","Tyler","Emma","Noah"]
        prog = [.95,.82,.41,.91,.28,.73,.60]
        cols = [GREEN, M_TEAL, ORANGE, GREEN, RED, M_TEAL, M_BLUE]

        bars = VGroup(); nms = VGroup(); pts = VGroup()
        for i, (nm, p, c) in enumerate(zip(students, prog, cols)):
            x = -5 + i*1.5; h = p*3.5
            bar = Rectangle(width=1, height=h, color=c, fill_color=c, fill_opacity=.5, stroke_width=2)
            bar.move_to([x, -1.2+h/2, 0])
            n = Text(nm, font_size=11, color=WHITE).set_opacity(.7).move_to([x,-1.6,0])
            pt = Text(f"{int(p*100)}%", font_size=14, color=c, weight=BOLD).next_to(bar, UP, .08)
            bars.add(bar); nms.add(n); pts.add(pt)

        self.play(FadeIn(df), FadeIn(dt), FadeIn(live), run_time=.3)
        self.play(*[GrowFromEdge(b, DOWN) for b in bars], run_time=1.0)
        self.play(FadeIn(nms), FadeIn(pts), run_time=.4)
        self.wait(1.0)

        # Alerts on struggling students
        aj = SurroundingRectangle(VGroup(bars[2], nms[2]), color=ORANGE, stroke_width=2.5, buff=.08)
        at = SurroundingRectangle(VGroup(bars[4], nms[4]), color=RED, stroke_width=2.5, buff=.08)
        atxt = Text("⚠ Needs attention", font_size=14, color=RED, weight=BOLD).move_to([4, 2, 0])

        self.play(Create(aj), Create(at), FadeIn(atxt), run_time=.5)
        # Pulse alerts
        self.play(aj.animate.set_stroke(opacity=.3), at.animate.set_stroke(opacity=.3), run_time=.3)
        self.play(aj.animate.set_stroke(opacity=1), at.animate.set_stroke(opacity=1), run_time=.3)
        self.wait(2.0)  # "not just a grade at the end of the unit."

        self.play(FadeOut(VGroup(df, dt, live, bars, nms, pts, aj, at, atxt)), run_time=.4)

        # ══════════════════════════════════════════
        # ACT 7: Course Spectrum (43-49s of audio)
        # "Pre-Algebra through Calculus."
        # ══════════════════════════════════════════

        courses = [("Pre-Algebra","#6366F1"),("Algebra 1","#8B5CF6"),("Geometry","#A855F7"),
                   ("Algebra 2","#C084FC"),("Precalculus",M_TEAL),("Calculus",M_BLUE)]

        cards = VGroup()
        for nm, c in courses:
            bx = RoundedRectangle(width=1.9, height=1.1, corner_radius=.1,
                                   color=c, fill_color=BOX, fill_opacity=.65, stroke_width=2.5)
            tx = Text(nm, font_size=15, color=c, weight=BOLD).move_to(bx)
            cards.add(VGroup(bx, tx))
        cards.arrange(RIGHT, buff=.2).move_to([0,.5,0])

        carrows = VGroup()
        for i in range(len(cards)-1):
            carrows.add(Arrow(cards[i].get_right(), cards[i+1].get_left(),
                              color=WHITE, stroke_width=1.5, stroke_opacity=.4,
                              buff=.05, max_tip_length_to_length_ratio=.3))

        for i, card in enumerate(cards):
            a = [FadeIn(card, shift=RIGHT*.2, scale=.9)]
            if i > 0: a.append(Create(carrows[i-1]))
            self.play(*a, run_time=.2)

        pl = Line(cards[0].get_bottom()+DOWN*.5, cards[-1].get_bottom()+DOWN*.5,
                  color=M_TEAL, stroke_width=3)
        ptx = Text("ONE PLATFORM", font_size=24, color=M_TEAL, weight=BOLD).next_to(pl, DOWN, .15)
        self.play(Create(pl), FadeIn(ptx), run_time=.4)
        self.play(*[Indicate(c, color=c[0].color, scale_factor=1.04) for c in cards], run_time=.5)
        self.wait(1.5)  # "Every course built on one platform."

        self.play(FadeOut(VGroup(cards, carrows, pl, ptx)), run_time=.3)

        # ══════════════════════════════════════════
        # ACT 8: Not Bolted On (49-56s of audio)
        # "Not a textbook with a website bolted on."
        # ══════════════════════════════════════════

        self.camera.frame.set(width=FW).move_to(ORIGIN)

        div = Line([0,-3.5,0],[0,3.5,0], color=WHITE, stroke_width=1.5, stroke_opacity=.3)
        ol = Text("Traditional", font_size=24, color=RED, weight=BOLD).move_to([-3.5,3,0])
        nl = Text("Meridian", font_size=24, color=M_TEAL, weight=BOLD).move_to([3.5,3,0])

        old = VGroup()
        for i, nm in enumerate(["Textbook","Website","Videos","Grading"]):
            bx = RoundedRectangle(width=2.4, height=.65, corner_radius=.06,
                                   color="#444", fill_color="#0a0a0a", fill_opacity=.5, stroke_width=1.5)
            tx = Text(nm, font_size=15, color="#666")
            old.add(VGroup(bx, tx).move_to([-3.5+(i%2)*.2, 1.8-i*.95, 0]))

        new = VGroup()
        ncols = [M_BLUE, VIOLET, ORANGE, M_TEAL]
        for i, (nm, c) in enumerate(zip(["Textbook","Videos","Problems","AI Tutor"], ncols)):
            bx = RoundedRectangle(width=2.4, height=.65, corner_radius=.06,
                                   color=c, fill_color=BOX, fill_opacity=.6, stroke_width=2.5)
            tx = Text(nm, font_size=15, color=c, weight=BOLD)
            new.add(VGroup(bx, tx).move_to([3.5, 1.8-i*.95, 0]))

        nconn = VGroup(*[Line(new[i].get_bottom(), new[i+1].get_top(),
                              color=M_TEAL, stroke_width=2, stroke_opacity=.6) for i in range(3)])

        self.play(FadeIn(div), FadeIn(ol), FadeIn(nl),
                  *[FadeIn(b, shift=DOWN*.15) for b in old],
                  *[FadeIn(b, shift=DOWN*.15) for b in new], run_time=.5)
        self.play(*[Create(c) for c in nconn], run_time=.3)
        self.wait(.5)

        xo = Text("✗", font_size=80, color=RED).set_opacity(.5).move_to([-3.5,-.5,0])
        ck = Text("✓", font_size=80, color=GREEN).set_opacity(.5).move_to([3.5,-.5,0])
        self.play(FadeIn(xo, scale=.5), FadeIn(ck, scale=.5), run_time=.3)
        self.wait(2.5)  # "A complete system built by educators..."

        self.play(FadeOut(VGroup(div, ol, old, nl, new, nconn, xo, ck)), run_time=.4)

        # ══════════════════════════════════════════
        # ACT 9: Emotional Closer (56-61s of audio)
        # "Because every student deserves a program
        #  that actually meets them where they are."
        # ══════════════════════════════════════════

        c1 = Text("Every student.", font_size=56, color=WHITE, weight=BOLD).move_to([0,1.2,0])
        c2 = Text("Every level.", font_size=56, color=M_TEAL, weight=BOLD).move_to([0,0,0])
        c3 = Text("One program that adapts.", font_size=56, color=M_BLUE, weight=BOLD).move_to([0,-1.2,0])

        self.play(FadeIn(c1, shift=UP*.2), run_time=.5)
        self.wait(.5)
        self.play(FadeIn(c2, shift=UP*.2), run_time=.5)
        self.wait(.5)
        self.play(FadeIn(c3, shift=UP*.2), run_time=.5)
        self.wait(.5)
        self.play(Circumscribe(VGroup(c1,c2,c3), color=M_TEAL, run_time=.7),
                  bg.animate.set_opacity(.35))
        self.play(bg.animate.set_opacity(.15), run_time=.3)
        self.play(FadeOut(VGroup(c1,c2,c3)), run_time=.4)

        # ══════════════════════════════════════════
        # ACT 10: End Card (61-65s+ of audio)
        # "Meridian Math. Mathematics for every student."
        # ══════════════════════════════════════════

        _A2, _B2 = 2.0, 1.4
        lg = ParametricFunction(lambda t: np.array([_A2*np.sin(2*t), _B2*np.sin(3*t)+.8, 0]),
                                 t_range=[0, TAU, .01], color=M_BLUE, stroke_width=10, stroke_opacity=.15)
        lc = ParametricFunction(lambda t: np.array([_A2*np.sin(2*t), _B2*np.sin(3*t)+.8, 0]),
                                 t_range=[0, TAU, .01], color=M_BLUE, stroke_width=2.5, stroke_opacity=.8)

        en = Text("MERIDIAN MATH", font_size=56, color=M_BLUE, weight=BOLD).move_to([0,-1,0])
        et = Text("Mathematics for every student.", font_size=28, color=WARM).set_opacity(.7)
        et.next_to(en, DOWN, .3)
        eu = Text("meridian-math.org", font_size=24, color=M_TEAL, weight=BOLD).next_to(et, DOWN, .4)

        eb = SurroundingRectangle(VGroup(en, et, eu), color=M_BLUE, fill_color=BOX, fill_opacity=.4,
                                   buff=.45, corner_radius=.12, stroke_width=2)

        self.play(Create(lc, run_time=.8), FadeIn(lg, run_time=.6))
        self.play(FadeIn(eb), FadeIn(en, scale=.95), run_time=.4)
        self.play(FadeIn(et, shift=UP*.1), run_time=.3)
        self.play(FadeIn(eu), run_time=.2)
        self.play(Circumscribe(eb, color=M_BLUE, run_time=.7))
        self.wait(4.0)  # Hold on end card

        self.play(FadeOut(Group(*self.mobjects)), run_time=.5)
