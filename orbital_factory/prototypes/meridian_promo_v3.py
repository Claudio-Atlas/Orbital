"""
Meridian Math × Orbital — District Promo V3 (FINAL)
====================================================
THE performance piece. Audio embedded via self.add_sound() for perfect sync.
Every visual is custom, consuming, impressive. This lands the district.

Audio: meridian_promo_v3.mp3 (~65s, Hale, stability=0.42, style=0.45, speed=0.93)
Music: bg_synthwave.mp3 (mixed in post via ffmpeg — Manim can only add_sound one track)

Timing map (from silence detection):
  0.0-5.2:   "Every student learns...most math programs don't."
  6.4-12.4:  "One textbook. One speed...good luck catching up."
  13.6-15.8: "We built Meridian to fix that."
  17.2-29.8: "Complete math programs...adapts to EVERY student."
  30.4-38.8: "When a student gets stuck...falling through the cracks."
  39.4-45.5: "Teachers get real-time dashboards...end of the unit."
  46.1-50.1: "Pre-Algebra through Calculus...one platform."
  50.7-56.4: "Not a textbook...been in the classroom."
  57.0-60.8: "Because every student deserves...where they are."
  61.5-65.0: "Meridian Math. Mathematics for every student."

Render:
  cd ~/Desktop/Orbital/orbital_factory && source venv/bin/activate
  PATH="/Library/TeX/texbin:$PATH" manim render prototypes/meridian_promo_v3.py MeridianPromoV3 \
    -o meridian_promo_v3.mp4 --format mp4 -r 1920,1080 --frame_rate 60 --flush_cache
"""
from manim import *
import numpy as np
import random

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
GOLD = "#FBBF24"
PINK = "#EC4899"
FW = 14.2
FH = 8.0

TTS_PATH = "output/tts/meridian_promo_v3.mp3"


def _bg_grid(fw=20, fh=14, spacing=0.8, color=GRID_COLOR, sw=0.5, opacity=0.15):
    lines = VGroup()
    for x in np.arange(-fw/2, fw/2+0.1, spacing):
        lines.add(Line([x, -fh/2, 0], [x, fh/2, 0], color=color,
                       stroke_width=sw, stroke_opacity=opacity))
    for y in np.arange(-fh/2, fh/2+0.1, spacing):
        lines.add(Line([-fw/2, y, 0], [fw/2, y, 0], color=color,
                       stroke_width=sw, stroke_opacity=opacity))
    return lines


def _gear(radius, n_teeth, color, center, tooth_len=0.14, sw=2.5):
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
        tooth = Polygon(ip + perp*tw, ip - perp*tw, op - perp*tw*0.7, op + perp*tw*0.7,
                        color=color, stroke_width=sw-0.5, fill_color=color, fill_opacity=0.3)
        parts.append(tooth)
    return VGroup(*parts)


def _particle_burst(center, n=20, color=MERIDIAN_BLUE, radius=3.0):
    """Create expanding particle dots."""
    dots = VGroup()
    targets = VGroup()
    for _ in range(n):
        angle = random.uniform(0, TAU)
        dist = random.uniform(0.5, radius)
        d = Dot(center, radius=random.uniform(0.02, 0.06), color=color,
                fill_opacity=random.uniform(0.3, 0.8))
        t = Dot(center + dist * np.array([np.cos(angle), np.sin(angle), 0]),
                radius=0.01, fill_opacity=0)
        dots.add(d)
        targets.add(t)
    return dots, targets


class MeridianPromoV3(MovingCameraScene):
    def construct(self):
        self.camera.background_color = BLACK
        self.camera.frame.set(width=FW, height=FH)

        bg = _bg_grid()
        self.add(bg)

        # ── Persistent border + glow ──
        def _border():
            cf = self.camera.frame
            w, h = cf.width - 0.2, cf.height - 0.2
            return Rectangle(width=w, height=h, color=MERIDIAN_BLUE,
                             stroke_width=2.5, stroke_opacity=0.6,
                             fill_opacity=0).move_to(cf.get_center())
        def _glow():
            cf = self.camera.frame
            w, h = cf.width - 0.15, cf.height - 0.15
            return Rectangle(width=w, height=h, color=MERIDIAN_BLUE,
                             stroke_width=6, stroke_opacity=0.1,
                             fill_opacity=0).move_to(cf.get_center())
        def _wm():
            cf = self.camera.frame
            t = Text("MERIDIAN × ORBITAL", font_size=11, color=WHITE, weight=BOLD)
            t.set_opacity(0.3)
            t.move_to([cf.get_center()[0] - cf.width/2 + 1.0,
                        cf.get_center()[1] - cf.height/2 + 0.25, 0])
            return t

        self.add(always_redraw(_glow), always_redraw(_border), always_redraw(_wm))

        # ══════════════════════════════════════════════
        # EMBED AUDIO — perfect sync via add_sound
        # ══════════════════════════════════════════════
        self.add_sound(TTS_PATH)

        # ══════════════════════════════════════════════
        # ACT 0: MERIDIAN × ORBITAL COLLAB INTRO (0-2.0s)
        # Particle explosion → logo reveal
        # ══════════════════════════════════════════════

        # Particles burst outward from center
        p_dots, p_targets = _particle_burst(ORIGIN, n=30, color=MERIDIAN_BLUE, radius=4.0)
        p_dots2, p_targets2 = _particle_burst(ORIGIN, n=20, color=END_CYAN, radius=3.5)
        self.add(p_dots, p_dots2)

        # MERIDIAN text
        mer = Text("MERIDIAN", font_size=48, color=MERIDIAN_BLUE, weight=BOLD).move_to([-3.0, 0, 0])
        mer_glow = mer.copy().set_opacity(0.2).scale(1.04)
        # ×
        cx = Text("×", font_size=56, color=WHITE, weight=BOLD).move_to(ORIGIN)
        # ORBITAL with Lissajous
        _A, _B = 0.9, 0.65
        orb_liss = ParametricFunction(
            lambda t: np.array([_A*np.sin(2*t)+3.0, _B*np.sin(3*t), 0]),
            t_range=[0, TAU, 0.01], color=END_CYAN, stroke_width=2.5)
        orb_liss_g = ParametricFunction(
            lambda t: np.array([_A*np.sin(2*t)+3.0, _B*np.sin(3*t), 0]),
            t_range=[0, TAU, 0.01], color=END_CYAN, stroke_width=8, stroke_opacity=0.15)
        orb = Text("ORBITAL", font_size=48, color=END_CYAN, weight=BOLD).move_to([3.0, -1.1, 0])

        # Particles explode while logos fade in
        self.play(
            *[d.animate.move_to(t.get_center()).set_opacity(0) for d, t in zip(p_dots, p_targets)],
            *[d.animate.move_to(t.get_center()).set_opacity(0) for d, t in zip(p_dots2, p_targets2)],
            FadeIn(mer_glow), FadeIn(mer, shift=RIGHT*0.2),
            FadeIn(cx, scale=0.3),
            Create(orb_liss), FadeIn(orb_liss_g),
            FadeIn(orb, shift=LEFT*0.2),
            run_time=1.2
        )
        self.play(
            Flash(ORIGIN, color=VIOLET, line_length=0.6, num_lines=16, run_time=0.3),
            cx.animate.set_color(VIOLET),
            run_time=0.3
        )
        self.remove(p_dots, p_dots2, p_targets, p_targets2)
        self.wait(0.2)

        intro = Group(mer_glow, mer, cx, orb_liss, orb_liss_g, orb)
        self.play(FadeOut(intro, shift=UP*0.4), run_time=0.3)

        # ══════════════════════════════════════════════
        # ACT 1: DIFFERENT PACES (2.0-5.2s)
        # "Every student learns at a different pace.
        #  The problem is, most math programs don't."
        # Conveyor belt with equations, 3 students processing
        # ══════════════════════════════════════════════

        # Conveyor belt of equations
        equations = [r"2x+3=7", r"\frac{1}{2}+\frac{3}{4}", r"x^2-9=0",
                     r"3(x+2)=15", r"\sqrt{16}", r"2^5"]
        eq_mobs = VGroup()
        for i, eq in enumerate(equations):
            m = MathTex(eq, font_size=22, color=WHITE).set_opacity(0.6)
            box = SurroundingRectangle(m, color=VIOLET, fill_color=BOX_FILL,
                                        fill_opacity=0.5, buff=0.12, corner_radius=0.06, stroke_width=1.5)
            grp = VGroup(box, m).move_to([-6 + i*2.2, 2.5, 0])
            eq_mobs.add(grp)

        # Three students as circles with progress
        s_fast = VGroup(
            Circle(radius=0.5, color=GREEN, fill_color=GREEN, fill_opacity=0.15, stroke_width=2.5),
            Text("A", font_size=24, color=GREEN, weight=BOLD)
        ).move_to([-3, -1.0, 0])
        s_mid = VGroup(
            Circle(radius=0.5, color=MERIDIAN_BLUE, fill_color=MERIDIAN_BLUE, fill_opacity=0.15, stroke_width=2.5),
            Text("B", font_size=24, color=MERIDIAN_BLUE, weight=BOLD)
        ).move_to([0, -1.0, 0])
        s_slow = VGroup(
            Circle(radius=0.5, color=ORANGE, fill_color=ORANGE, fill_opacity=0.15, stroke_width=2.5),
            Text("C", font_size=24, color=ORANGE, weight=BOLD)
        ).move_to([3, -1.0, 0])

        # Progress bars under each student
        def _prog_bar(x, pct, color):
            bg = Rectangle(width=2, height=0.2, color="#333", fill_color="#111",
                           fill_opacity=0.6, stroke_width=1).move_to([x, -2.0, 0])
            fill = Rectangle(width=2*pct, height=0.2, color=color, fill_color=color,
                             fill_opacity=0.5, stroke_width=0)
            fill.move_to(bg.get_left() + RIGHT*pct, aligned_edge=LEFT)
            return VGroup(bg, fill)

        pb_fast = _prog_bar(-3, 0.92, GREEN)
        pb_mid = _prog_bar(0, 0.55, MERIDIAN_BLUE)
        pb_slow = _prog_bar(3, 0.25, ORANGE)

        checkmarks = VGroup()
        for i in range(5):
            c = Text("✓", font_size=16, color=GREEN).move_to([-4 + i*0.5, -0.3, 0])
            checkmarks.add(c)

        stack_red = VGroup()
        for i in range(3):
            eq = MathTex(equations[i], font_size=18, color=SOFT_RED).set_opacity(0.5)
            b = SurroundingRectangle(eq, color=SOFT_RED, fill_color="#1a0000",
                                      fill_opacity=0.4, buff=0.08, stroke_width=1.5)
            stack_red.add(VGroup(b, eq).move_to([3 + (i-1)*0.15, -0.2 - i*0.35, 0]))

        self.play(*[FadeIn(e, shift=DOWN*0.3) for e in eq_mobs],
                  FadeIn(s_fast), FadeIn(s_mid), FadeIn(s_slow),
                  run_time=0.5)
        self.play(
            # Equations flow right (conveyor)
            eq_mobs.animate.shift(RIGHT*3),
            FadeIn(pb_fast), FadeIn(pb_mid), FadeIn(pb_slow),
            run_time=1.2
        )
        # Show checkmarks on fast student, stack on slow
        self.play(FadeIn(checkmarks, lag_ratio=0.15),
                  FadeIn(stack_red, lag_ratio=0.2),
                  run_time=0.8)
        self.wait(0.3)

        act1 = VGroup(eq_mobs, s_fast, s_mid, s_slow, pb_fast, pb_mid, pb_slow,
                       checkmarks, stack_red)
        self.play(FadeOut(act1), run_time=0.3)

        # ══════════════════════════════════════════════
        # ACT 2: DOMINO EFFECT (6.4-12.4s)
        # "One textbook. One speed. And if you miss a
        #  step, good luck catching up."
        # Dominos fall in chain reaction
        # ══════════════════════════════════════════════

        # 8 dominos representing sequential topics
        topics = ["1.1", "1.2", "1.3", "1.4", "1.5", "1.6", "1.7", "1.8"]
        dominos = VGroup()
        for i, t in enumerate(topics):
            rect = RoundedRectangle(width=0.8, height=2.0, corner_radius=0.06,
                                     color=WHITE, fill_color=BOX_FILL, fill_opacity=0.7,
                                     stroke_width=2)
            lbl = Text(t, font_size=18, color=WHITE)
            d = VGroup(rect, lbl).move_to([-5.5 + i*1.5, 0, 0])
            dominos.add(d)

        self.play(*[FadeIn(d, shift=UP*0.3) for d in dominos], run_time=0.5)
        self.wait(0.5)

        # Domino 3 (index 2) turns red — the missed step
        self.play(
            dominos[2][0].animate.set_color(SOFT_RED).set_fill(SOFT_RED, 0.3),
            dominos[2][1].animate.set_color(SOFT_RED),
            Flash(dominos[2].get_center(), color=SOFT_RED, line_length=0.5, num_lines=12),
            run_time=0.4
        )
        self.wait(0.2)

        # Chain reaction — dominos 3-7 topple (rotate and fade)
        for i in range(2, len(dominos)):
            self.play(
                Rotate(dominos[i], PI/6, about_point=dominos[i].get_bottom()),
                dominos[i].animate.set_opacity(0.15 if i > 2 else 0.3),
                run_time=0.15
            )

        # "?" appears where knowledge collapsed
        collapse_q = Text("?", font_size=72, color=SOFT_RED, weight=BOLD)
        collapse_q.move_to([2, 0, 0])
        self.play(FadeIn(collapse_q, scale=0.3), run_time=0.3)
        self.wait(0.8)

        self.play(FadeOut(VGroup(dominos, collapse_q)), run_time=0.3)

        # ══════════════════════════════════════════════
        # ACT 3: MERIDIAN LOGO REVEAL + GEARS (13.6-17.0s)
        # "We built Meridian to fix that."
        # Particle implosion → logo appears → gears engage
        # ══════════════════════════════════════════════

        # Particles implode TO center
        imp_dots = VGroup()
        for _ in range(25):
            angle = random.uniform(0, TAU)
            dist = random.uniform(3, 5)
            d = Dot(dist * np.array([np.cos(angle), np.sin(angle), 0]),
                    radius=random.uniform(0.03, 0.07), color=MERIDIAN_BLUE,
                    fill_opacity=random.uniform(0.4, 0.9))
            imp_dots.add(d)

        mer_logo = Text("MERIDIAN", font_size=72, color=MERIDIAN_BLUE, weight=BOLD)
        mer_sub = Text("M A T H", font_size=22, color=MERIDIAN_TEAL, weight=BOLD)
        mer_sub.set_opacity(0.8).next_to(mer_logo, DOWN, buff=0.25)

        self.add(imp_dots)
        self.play(
            *[d.animate.move_to(ORIGIN).set_opacity(0) for d in imp_dots],
            run_time=0.5
        )
        self.remove(imp_dots)
        self.play(
            FadeIn(mer_logo, scale=1.1),
            Flash(ORIGIN, color=MERIDIAN_BLUE, line_length=0.8, num_lines=20, run_time=0.4),
            run_time=0.4
        )
        self.play(FadeIn(mer_sub), run_time=0.2)
        self.play(Circumscribe(mer_logo, color=MERIDIAN_TEAL, run_time=0.5))
        self.wait(0.3)
        self.play(FadeOut(VGroup(mer_logo, mer_sub), shift=UP*0.3), run_time=0.3)

        # Gear machine — three interlocking gears
        g1 = _gear(1.3, 14, MERIDIAN_BLUE, [-2.2, 0, 0], 0.24, 3)
        g2 = _gear(0.9, 10, MERIDIAN_TEAL, [0.4, 0, 0], 0.2, 3)
        g3 = _gear(0.65, 8, ORANGE, [2.5, 0.9, 0], 0.16, 2.5)
        g_label = Text("Every piece works together.", font_size=26, color=WHITE, weight=BOLD)
        g_label.set_opacity(0.8).move_to([0, -2.8, 0])

        self.play(FadeIn(g1), FadeIn(g2), FadeIn(g3), FadeIn(g_label), run_time=0.4)
        self.play(
            Rotate(g1, PI/2, about_point=[-2.2, 0, 0]),
            Rotate(g2, -PI/1.8, about_point=[0.4, 0, 0]),
            Rotate(g3, PI/1.5, about_point=[2.5, 0.9, 0]),
            run_time=1.5
        )
        self.play(FadeOut(VGroup(g1, g2, g3, g_label)), run_time=0.3)

        # ══════════════════════════════════════════════
        # ACT 4: FOUR PILLARS — EACH DEMOS ITSELF (17.0-29.8s)
        # "Complete math programs with digital textbooks,
        #  video walkthroughs, thousands of practice problems,
        #  and a personal AI tutor that adapts to EVERY student."
        # ══════════════════════════════════════════════

        # Pillar 1: TEXTBOOK — shows content flowing
        p1_box = RoundedRectangle(width=2.6, height=3.2, corner_radius=0.12,
                                   color=MERIDIAN_BLUE, fill_color=BOX_FILL,
                                   fill_opacity=0.8, stroke_width=2.5).move_to([-4.5, 0, 0])
        p1_title = Text("Digital\nTextbook", font_size=18, color=MERIDIAN_BLUE, weight=BOLD)
        p1_title.move_to(p1_box.get_top() + DOWN*0.4)
        # Mini content lines
        p1_lines = VGroup()
        for i in range(4):
            l = Line([-5.5, -0.3 - i*0.35, 0], [-3.5, -0.3 - i*0.35, 0],
                     color=MERIDIAN_BLUE, stroke_width=1.5, stroke_opacity=0.4)
            p1_lines.add(l)
        p1_eq = MathTex(r"f(x) = x^2", font_size=18, color=CYAN).move_to(p1_box.get_center() + DOWN*0.2)

        # Pillar 2: VIDEO — mini animation plays
        p2_box = RoundedRectangle(width=2.6, height=3.2, corner_radius=0.12,
                                   color=VIOLET, fill_color=BOX_FILL,
                                   fill_opacity=0.8, stroke_width=2.5).move_to([-1.5, 0, 0])
        p2_title = Text("Video\nLessons", font_size=18, color=VIOLET, weight=BOLD)
        p2_title.move_to(p2_box.get_top() + DOWN*0.4)
        # Mini play button
        p2_play = Triangle(color=VIOLET, fill_color=VIOLET, fill_opacity=0.6)
        p2_play.scale(0.3).rotate(-PI/6).move_to(p2_box.get_center())
        # Mini sine wave inside
        p2_wave = ParametricFunction(
            lambda t: np.array([-1.5 + 0.8*t, -0.5 + 0.3*np.sin(3*t), 0]),
            t_range=[0, 2, 0.01], color=VIOLET, stroke_width=2)

        # Pillar 3: PROBLEMS — checkmarks appear
        p3_box = RoundedRectangle(width=2.6, height=3.2, corner_radius=0.12,
                                   color=ORANGE, fill_color=BOX_FILL,
                                   fill_opacity=0.8, stroke_width=2.5).move_to([1.5, 0, 0])
        p3_title = Text("Practice\nProblems", font_size=18, color=ORANGE, weight=BOLD)
        p3_title.move_to(p3_box.get_top() + DOWN*0.4)
        p3_checks = VGroup()
        for i in range(3):
            row = VGroup(
                MathTex(f"{i+1}.", font_size=16, color=WHITE).set_opacity(0.6),
                Rectangle(width=1.2, height=0.25, color=ORANGE, fill_color=ORANGE,
                          fill_opacity=0.1, stroke_width=1),
                Text("✓", font_size=18, color=GREEN)
            ).arrange(RIGHT, buff=0.1).move_to([1.5, -0.1 - i*0.5, 0])
            # Hide checkmark initially
            row[2].set_opacity(0)
            p3_checks.add(row)

        # Pillar 4: AI TUTOR — chat bubbles
        p4_box = RoundedRectangle(width=2.6, height=3.2, corner_radius=0.12,
                                   color=MERIDIAN_TEAL, fill_color=BOX_FILL,
                                   fill_opacity=0.8, stroke_width=2.5).move_to([4.5, 0, 0])
        p4_title = Text("AI\nTutor", font_size=18, color=MERIDIAN_TEAL, weight=BOLD)
        p4_title.move_to(p4_box.get_top() + DOWN*0.4)
        # Mini chat bubbles
        p4_q = RoundedRectangle(width=1.8, height=0.4, corner_radius=0.08,
                                 color="#555", fill_color="#222", fill_opacity=0.6,
                                 stroke_width=1).move_to([4.5, -0.1, 0])
        p4_q_txt = Text("How do I solve this?", font_size=10, color=WHITE).set_opacity(0.7).move_to(p4_q)
        p4_a = RoundedRectangle(width=1.8, height=0.4, corner_radius=0.08,
                                 color=MERIDIAN_TEAL, fill_color=MERIDIAN_TEAL, fill_opacity=0.15,
                                 stroke_width=1.5).move_to([4.5, -0.7, 0])
        p4_a_txt = Text("Start by isolating x...", font_size=10, color=MERIDIAN_TEAL).move_to(p4_a)

        # Reveal pillars one at a time with internal demos
        # Pillar 1
        self.play(FadeIn(VGroup(p1_box, p1_title), shift=UP*0.4, scale=0.9), run_time=0.4)
        self.play(*[Create(l) for l in p1_lines], Write(p1_eq), run_time=0.5)
        self.wait(0.2)

        # Pillar 2
        self.play(FadeIn(VGroup(p2_box, p2_title), shift=UP*0.4, scale=0.9), run_time=0.4)
        self.play(FadeIn(p2_play, scale=0.5), run_time=0.2)
        self.play(FadeOut(p2_play), Create(p2_wave), run_time=0.5)
        self.wait(0.2)

        # Pillar 3
        self.play(FadeIn(VGroup(p3_box, p3_title), shift=UP*0.4, scale=0.9), run_time=0.4)
        self.play(FadeIn(p3_checks, lag_ratio=0.1), run_time=0.3)
        for row in p3_checks:
            self.play(row[2].animate.set_opacity(1),
                      Flash(row[2].get_center(), color=GREEN, line_length=0.2, num_lines=6, run_time=0.15),
                      run_time=0.2)

        # Pillar 4
        self.play(FadeIn(VGroup(p4_box, p4_title), shift=UP*0.4, scale=0.9), run_time=0.4)
        self.play(FadeIn(p4_q, shift=LEFT*0.2), FadeIn(p4_q_txt), run_time=0.3)
        self.play(FadeIn(p4_a, shift=LEFT*0.2), FadeIn(p4_a_txt), run_time=0.3)
        self.wait(0.3)

        # Connect all four with glowing line
        connect = Line(p1_box.get_bottom() + DOWN*0.4, p4_box.get_bottom() + DOWN*0.4,
                       color=MERIDIAN_TEAL, stroke_width=3)
        platform_txt = Text("ONE PLATFORM", font_size=24, color=MERIDIAN_TEAL, weight=BOLD)
        platform_txt.next_to(connect, DOWN, buff=0.15)
        self.play(Create(connect), FadeIn(platform_txt), run_time=0.4)

        # Pulse
        self.play(
            *[Indicate(b, color=b.color, scale_factor=1.02)
              for b in [p1_box, p2_box, p3_box, p4_box]],
            bg.animate.set_opacity(0.3), run_time=0.5
        )
        self.play(bg.animate.set_opacity(0.15), run_time=0.2)
        self.wait(0.3)

        all_pillars = VGroup(p1_box, p1_title, p1_lines, p1_eq,
                              p2_box, p2_title, p2_wave,
                              p3_box, p3_title, p3_checks,
                              p4_box, p4_title, p4_q, p4_q_txt, p4_a, p4_a_txt,
                              connect, platform_txt)
        self.play(FadeOut(all_pillars), run_time=0.4)

        # ══════════════════════════════════════════════
        # RAPID FIRE MATH SHOWCASE (inside Act 4 timing)
        # Riemann sum + tangent line montage
        # ══════════════════════════════════════════════

        # Riemann sum
        r_axes = Axes(x_range=[0, 2*PI+0.5, PI/2], y_range=[-1.5, 1.5, 0.5],
                      x_length=10, y_length=5, tips=False,
                      axis_config={"color": WHITE, "stroke_width": 1.5, "stroke_opacity": 0.5})
        r_curve = r_axes.plot(lambda x: np.sin(x), x_range=[0, 2*PI],
                              color=VIOLET, stroke_width=3)
        r_label = MathTex(r"\int_0^{2\pi}\sin(x)\,dx", font_size=28, color=VIOLET)
        r_label.move_to([4.5, 2.2, 0])

        def _sin_rects(n, op=0.4):
            rects = VGroup()
            dx = 2*PI/n
            for i in range(n):
                x = i*dx
                y = np.sin(x + dx/2)
                h = r_axes.y_length * abs(y) / 3.0
                w = r_axes.x_length * dx / (2*PI+0.5)
                c = CYAN if y >= 0 else ORANGE
                rect = Rectangle(width=w, height=h, color=c, fill_color=c,
                                 fill_opacity=op, stroke_width=1.2)
                cx = r_axes.c2p(x + dx/2, 0)
                rect.move_to(cx + (UP if y >= 0 else DOWN) * h/2)
                rects.add(rect)
            return rects

        self.play(Create(r_axes, run_time=0.3), Create(r_curve, run_time=0.5),
                  FadeIn(r_label), self.camera.frame.animate.set(width=FW*0.92), run_time=0.5)

        r6 = _sin_rects(6, 0.3)
        r16 = _sin_rects(16, 0.35)
        r32 = _sin_rects(32, 0.4)
        self.play(FadeIn(r6), run_time=0.3)
        self.play(ReplacementTransform(r6, r16), run_time=0.4)
        self.play(ReplacementTransform(r16, r32), run_time=0.4)
        self.wait(0.2)
        self.play(FadeOut(VGroup(r_axes, r_curve, r32, r_label)),
                  self.camera.frame.animate.set(width=FW).move_to(ORIGIN), run_time=0.3)

        # ══════════════════════════════════════════════
        # ACT 5: AI TUTOR DEMO (30.4-38.8s)
        # "When a student gets stuck, the AI tutor meets
        #  them right where they are."
        # ══════════════════════════════════════════════

        problem = MathTex(r"3x + 7 = 22", font_size=56, color=WHITE).move_to([0, 2.8, 0])
        stuck_label = Text("Student is stuck", font_size=20, color=ORANGE, weight=BOLD)
        stuck_label.set_opacity(0.8).next_to(problem, UP, buff=0.25)
        # Red glow around problem
        prob_glow = SurroundingRectangle(problem, color=SOFT_RED, fill_color=SOFT_RED,
                                          fill_opacity=0.05, buff=0.2, corner_radius=0.1,
                                          stroke_width=2)

        self.play(Write(problem), FadeIn(stuck_label), Create(prob_glow), run_time=0.5)
        self.wait(0.3)

        # AI tutor panel
        panel = RoundedRectangle(width=9, height=5, corner_radius=0.15,
                                  color=MERIDIAN_TEAL, fill_color=BOX_FILL,
                                  fill_opacity=0.85, stroke_width=2).move_to([0, -0.8, 0])
        ai_badge = VGroup(
            RoundedRectangle(width=1.6, height=0.4, corner_radius=0.1,
                              color=MERIDIAN_TEAL, fill_color=MERIDIAN_TEAL,
                              fill_opacity=0.2, stroke_width=1.5),
            Text("AI Tutor", font_size=14, color=MERIDIAN_TEAL, weight=BOLD)
        )
        ai_badge[1].move_to(ai_badge[0])
        ai_badge.move_to(panel.get_top() + DOWN*0.35 + LEFT*3)

        msg1 = Text("What operation undoes adding 7?", font_size=20, color=WARM_WHITE)
        msg1.move_to([-0.3, 0.2, 0])

        s1 = MathTex(r"3x + 7 - 7 = 22 - 7", font_size=38, color=CYAN).move_to([0, -0.4, 0])
        s2 = MathTex(r"3x = 15", font_size=38, color=CYAN).move_to([0, -1.1, 0])
        msg2 = Text("Now divide both sides by 3!", font_size=20, color=WARM_WHITE).move_to([0, -1.7, 0])
        s3 = MathTex(r"x = 5", font_size=48, color=GREEN).move_to([0, -2.4, 0])

        self.play(FadeIn(panel), FadeIn(ai_badge), run_time=0.3)
        self.play(FadeIn(msg1, shift=LEFT*0.3), run_time=0.3)
        self.wait(0.2)
        self.play(Write(s1), run_time=0.5)
        self.wait(0.2)
        self.play(Write(s2), run_time=0.4)
        self.play(FadeIn(msg2, shift=LEFT*0.3), run_time=0.3)
        self.wait(0.2)

        # Answer with celebration
        self.play(Write(s3), run_time=0.3)
        ans_box = SurroundingRectangle(s3, color=GREEN, fill_color=GREEN,
                                        fill_opacity=0.1, buff=0.15, corner_radius=0.08, stroke_width=2.5)
        self.play(
            Create(ans_box),
            Flash(s3.get_center(), color=GREEN, line_length=0.5, num_lines=14),
            # Problem glow turns green
            prob_glow.animate.set_color(GREEN),
            stuck_label.animate.set_color(GREEN),
            run_time=0.4
        )

        # Replace "stuck" with "solved!"
        solved = Text("Solved!", font_size=20, color=GREEN, weight=BOLD)
        solved.move_to(stuck_label)
        self.play(FadeOut(stuck_label), FadeIn(solved), run_time=0.2)
        self.wait(0.5)

        self.play(FadeOut(VGroup(problem, solved, prob_glow, panel, ai_badge,
                                  msg1, s1, s2, msg2, s3, ans_box)), run_time=0.4)

        # Tangent line showcase
        axes = Axes(x_range=[-1, 5, 1], y_range=[-1, 8, 2],
                    x_length=8, y_length=5, tips=False,
                    axis_config={"color": WHITE, "stroke_width": 1.5, "stroke_opacity": 0.5}).move_to([0, 0.2, 0])
        curve = axes.plot(lambda x: 0.3*x**2+0.5, x_range=[0, 4.5], color=VIOLET, stroke_width=3)
        c_label = MathTex(r"f'(x)", font_size=22, color=GREEN).move_to([5, 2, 0])

        self.play(Create(axes, run_time=0.3), Create(curve, run_time=0.5), FadeIn(c_label), run_time=0.5)

        xt = ValueTracker(0.5)
        tangent = always_redraw(lambda: Line(
            axes.c2p(xt.get_value()-1.5, 0.3*xt.get_value()**2+0.5 - 0.6*xt.get_value()*1.5),
            axes.c2p(xt.get_value()+1.5, 0.3*xt.get_value()**2+0.5 + 0.6*xt.get_value()*1.5),
            color=GREEN, stroke_width=2.5))
        dot = always_redraw(lambda: Dot(
            axes.c2p(xt.get_value(), 0.3*xt.get_value()**2+0.5),
            color=GREEN, radius=0.08).set_glow_factor(0.8))
        self.add(tangent, dot)
        self.play(xt.animate.set_value(4.0),
                  self.camera.frame.animate.shift(RIGHT*0.4+UP*0.3),
                  run_time=1.8, rate_func=smooth)
        self.play(xt.animate.set_value(2.0),
                  self.camera.frame.animate.move_to(ORIGIN),
                  run_time=0.8, rate_func=smooth)
        self.play(FadeOut(VGroup(axes, curve, c_label, tangent, dot)), run_time=0.3)

        # ══════════════════════════════════════════════
        # ACT 6: TEACHER DASHBOARD (39.4-45.5s)
        # "Teachers get real-time dashboards..."
        # Animated bars growing + pulsing alerts
        # ══════════════════════════════════════════════

        dash_frame = RoundedRectangle(width=12, height=6, corner_radius=0.15,
                                       color=MERIDIAN_BLUE, fill_color=BOX_FILL,
                                       fill_opacity=0.85, stroke_width=2).move_to(ORIGIN)
        dash_title = Text("Teacher Dashboard", font_size=28, color=MERIDIAN_BLUE, weight=BOLD)
        dash_title.move_to(dash_frame.get_top() + DOWN*0.4)
        # Real-time badge
        live = VGroup(
            Circle(radius=0.08, color=GREEN, fill_color=GREEN, fill_opacity=0.8),
            Text("LIVE", font_size=12, color=GREEN, weight=BOLD)
        ).arrange(RIGHT, buff=0.1).move_to(dash_frame.get_top() + DOWN*0.4 + RIGHT*4)

        students = ["Alex M.", "Maria R.", "James T.", "Sofia K.", "Tyler B.",
                     "Emma L.", "Noah P."]
        progress = [0.95, 0.82, 0.41, 0.91, 0.28, 0.73, 0.60]
        colors_p = [GREEN, MERIDIAN_TEAL, ORANGE, GREEN, SOFT_RED,
                    MERIDIAN_TEAL, MERIDIAN_BLUE]

        bars = VGroup()
        names = VGroup()
        pcts = VGroup()
        for i, (name, prog, col) in enumerate(zip(students, progress, colors_p)):
            x = -5 + i * 1.5
            bar_h = prog * 3.5
            bar = Rectangle(width=1.0, height=bar_h, color=col,
                             fill_color=col, fill_opacity=0.5, stroke_width=2)
            bar.move_to([x, -1.2 + bar_h/2, 0])
            n = Text(name, font_size=11, color=WHITE).set_opacity(0.7).move_to([x, -1.6, 0])
            p = Text(f"{int(prog*100)}%", font_size=14, color=col, weight=BOLD)
            p.next_to(bar, UP, buff=0.08)
            bars.add(bar)
            names.add(n)
            pcts.add(p)

        self.play(FadeIn(dash_frame), FadeIn(dash_title), FadeIn(live), run_time=0.3)
        self.play(*[GrowFromEdge(bar, DOWN) for bar in bars], run_time=0.8)
        self.play(FadeIn(names), FadeIn(pcts), run_time=0.3)

        # Pulse alerts on struggling students
        alert_j = SurroundingRectangle(VGroup(bars[2], names[2]),
                                        color=ORANGE, stroke_width=2.5, buff=0.08)
        alert_t = SurroundingRectangle(VGroup(bars[4], names[4]),
                                        color=SOFT_RED, stroke_width=2.5, buff=0.08)
        alert_txt = Text("⚠ Needs attention", font_size=14, color=SOFT_RED, weight=BOLD)
        alert_txt.move_to([4, 2.0, 0])

        self.play(Create(alert_j), Create(alert_t), FadeIn(alert_txt), run_time=0.5)
        # Pulse the alerts
        self.play(
            alert_j.animate.set_stroke(opacity=0.3),
            alert_t.animate.set_stroke(opacity=0.3),
            run_time=0.3
        )
        self.play(
            alert_j.animate.set_stroke(opacity=1),
            alert_t.animate.set_stroke(opacity=1),
            run_time=0.3
        )
        self.wait(0.5)

        self.play(FadeOut(VGroup(dash_frame, dash_title, live, bars, names, pcts,
                                  alert_j, alert_t, alert_txt)), run_time=0.4)

        # ══════════════════════════════════════════════
        # ACT 7: COURSE SPECTRUM + ALGEBRA CASCADE (46.1-53.3s)
        # "Pre-Algebra through Calculus. Every course."
        # "Not a textbook with a website bolted on."
        # ══════════════════════════════════════════════

        courses = [
            ("Pre-Algebra", "#6366F1"), ("Algebra 1", "#8B5CF6"),
            ("Geometry", "#A855F7"), ("Algebra 2", "#C084FC"),
            ("Precalculus", MERIDIAN_TEAL), ("Calculus", MERIDIAN_BLUE),
        ]

        cards = VGroup()
        for name, color in courses:
            box = RoundedRectangle(width=1.9, height=1.1, corner_radius=0.1,
                                   color=color, fill_color=BOX_FILL, fill_opacity=0.65,
                                   stroke_width=2.5)
            txt = Text(name, font_size=15, color=color, weight=BOLD).move_to(box)
            cards.add(VGroup(box, txt))

        cards.arrange(RIGHT, buff=0.2).move_to([0, 0.5, 0])

        c_arrows = VGroup()
        for i in range(len(cards)-1):
            c_arrows.add(Arrow(cards[i].get_right(), cards[i+1].get_left(),
                               color=WHITE, stroke_width=1.5, stroke_opacity=0.4,
                               buff=0.05, max_tip_length_to_length_ratio=0.3))

        p_line = Line(cards[0].get_bottom()+DOWN*0.5, cards[-1].get_bottom()+DOWN*0.5,
                      color=MERIDIAN_TEAL, stroke_width=3)
        p_text = Text("ONE PLATFORM", font_size=24, color=MERIDIAN_TEAL, weight=BOLD)
        p_text.next_to(p_line, DOWN, buff=0.15)

        for i, card in enumerate(cards):
            a = [FadeIn(card, shift=RIGHT*0.2, scale=0.9)]
            if i > 0: a.append(Create(c_arrows[i-1]))
            self.play(*a, run_time=0.15)

        self.play(Create(p_line), FadeIn(p_text), run_time=0.3)
        self.play(*[Indicate(c, color=c[0].color, scale_factor=1.04) for c in cards], run_time=0.4)
        self.wait(0.3)
        self.play(FadeOut(VGroup(cards, c_arrows, p_line, p_text)), run_time=0.3)

        # Algebra cascade
        alg = [r"x^2 + 6x + 9 = 0", r"(x+3)^2 = 0", r"x+3=0", r"x=-3"]
        alg_c = [WHITE, CYAN, CYAN, GREEN]
        alg_y = [1.5, 0.5, -0.5, -1.5]
        smobs = []
        for s, c, y in zip(alg, alg_c, alg_y):
            eq = MathTex(s, font_size=48, color=c).move_to([0, y, 0]).set_opacity(0)
            smobs.append(eq)
        for j, eq in enumerate(smobs):
            a = [eq.animate.set_opacity(1)]
            if j > 0: a.append(self.camera.frame.animate.shift(DOWN*0.15))
            self.play(*a, run_time=0.3)
            self.wait(0.15)
        ab = SurroundingRectangle(smobs[-1], color=GREEN, fill_color=BOX_FILL,
                                   fill_opacity=0.6, buff=0.2, corner_radius=0.1, stroke_width=2.5)
        self.play(Create(ab), Circumscribe(ab, color=GREEN, run_time=0.4), run_time=0.4)
        self.wait(0.2)
        self.play(*[FadeOut(m) for m in smobs], FadeOut(ab),
                  self.camera.frame.animate.move_to(ORIGIN), run_time=0.3)

        # ══════════════════════════════════════════════
        # ACT 8: COMPARISON (50.7-56.4s)
        # Split screen — boring vs alive
        # ══════════════════════════════════════════════

        self.camera.frame.set(width=FW).move_to(ORIGIN)

        # Divider
        div = Line([0, -3.5, 0], [0, 3.5, 0], color=WHITE, stroke_width=1.5, stroke_opacity=0.3)

        old_l = Text("Traditional", font_size=24, color=SOFT_RED, weight=BOLD).move_to([-3.5, 3.0, 0])
        new_l = Text("Meridian", font_size=24, color=MERIDIAN_TEAL, weight=BOLD).move_to([3.5, 3.0, 0])

        # Left: static, gray, boring
        old_items = VGroup()
        for i, name in enumerate(["Textbook", "Website", "Videos", "Grading"]):
            box = RoundedRectangle(width=2.4, height=0.65, corner_radius=0.06,
                                   color="#444", fill_color="#0a0a0a", fill_opacity=0.5, stroke_width=1.5)
            txt = Text(name, font_size=15, color="#666")
            grp = VGroup(box, txt).move_to([-3.5 + (i%2)*0.2, 1.8 - i*0.95, 0])
            old_items.add(grp)

        # Right: connected, alive, glowing
        new_items = VGroup()
        new_colors = [MERIDIAN_BLUE, VIOLET, ORANGE, MERIDIAN_TEAL]
        for i, (name, col) in enumerate(zip(["Textbook", "Videos", "Problems", "AI Tutor"], new_colors)):
            box = RoundedRectangle(width=2.4, height=0.65, corner_radius=0.06,
                                   color=col, fill_color=BOX_FILL, fill_opacity=0.6, stroke_width=2.5)
            txt = Text(name, font_size=15, color=col, weight=BOLD)
            grp = VGroup(box, txt).move_to([3.5, 1.8 - i*0.95, 0])
            new_items.add(grp)

        new_conn = VGroup()
        for i in range(3):
            new_conn.add(Line(new_items[i].get_bottom(), new_items[i+1].get_top(),
                              color=MERIDIAN_TEAL, stroke_width=2, stroke_opacity=0.6))

        self.play(FadeIn(div), FadeIn(old_l), FadeIn(new_l),
                  *[FadeIn(b, shift=DOWN*0.15) for b in old_items],
                  *[FadeIn(b, shift=DOWN*0.15) for b in new_items],
                  run_time=0.5)
        self.play(*[Create(c) for c in new_conn], run_time=0.3)

        x_old = Text("✗", font_size=80, color=SOFT_RED).set_opacity(0.5).move_to([-3.5, -0.5, 0])
        check = Text("✓", font_size=80, color=GREEN).set_opacity(0.5).move_to([3.5, -0.5, 0])
        self.play(FadeIn(x_old, scale=0.5), FadeIn(check, scale=0.5), run_time=0.3)
        self.wait(1.5)

        self.play(FadeOut(VGroup(div, old_l, old_items, new_l, new_items, new_conn, x_old, check)),
                  run_time=0.4)

        # ══════════════════════════════════════════════
        # ACT 9: EMOTIONAL CLOSER (57.0-60.8s)
        # "Because every student deserves a program
        #  that actually meets them where they are."
        # ══════════════════════════════════════════════

        c1 = Text("Every student.", font_size=56, color=WHITE, weight=BOLD).move_to([0, 1.2, 0])
        c2 = Text("Every level.", font_size=56, color=MERIDIAN_TEAL, weight=BOLD).move_to([0, 0, 0])
        c3 = Text("One program that adapts.", font_size=56, color=MERIDIAN_BLUE, weight=BOLD).move_to([0, -1.2, 0])

        self.play(FadeIn(c1, shift=UP*0.2), run_time=0.5)
        self.wait(0.4)
        self.play(FadeIn(c2, shift=UP*0.2), run_time=0.5)
        self.wait(0.4)
        self.play(FadeIn(c3, shift=UP*0.2), run_time=0.5)
        self.wait(0.3)

        self.play(
            Circumscribe(VGroup(c1, c2, c3), color=MERIDIAN_TEAL, run_time=0.7),
            bg.animate.set_opacity(0.35),
        )
        self.play(bg.animate.set_opacity(0.15), run_time=0.3)
        self.play(FadeOut(VGroup(c1, c2, c3)), run_time=0.4)

        # ══════════════════════════════════════════════
        # ACT 10: END CARD (61.5-65s)
        # "Meridian Math. Mathematics for every student."
        # Lissajous + logo + URL
        # ══════════════════════════════════════════════

        _A2, _B2 = 2.0, 1.4
        liss_g = ParametricFunction(
            lambda t: np.array([_A2*np.sin(2*t), _B2*np.sin(3*t)+0.8, 0]),
            t_range=[0, TAU, 0.01], color=MERIDIAN_BLUE, stroke_width=10, stroke_opacity=0.15)
        liss_c = ParametricFunction(
            lambda t: np.array([_A2*np.sin(2*t), _B2*np.sin(3*t)+0.8, 0]),
            t_range=[0, TAU, 0.01], color=MERIDIAN_BLUE, stroke_width=2.5, stroke_opacity=0.8)

        end_name = Text("MERIDIAN MATH", font_size=56, color=MERIDIAN_BLUE, weight=BOLD).move_to([0, -1.0, 0])
        end_tag = Text("Mathematics for every student.", font_size=28, color=WARM_WHITE)
        end_tag.set_opacity(0.7).next_to(end_name, DOWN, buff=0.3)
        end_url = Text("meridian-math.org", font_size=24, color=MERIDIAN_TEAL, weight=BOLD)
        end_url.next_to(end_tag, DOWN, buff=0.4)

        end_box = SurroundingRectangle(
            VGroup(end_name, end_tag, end_url),
            color=MERIDIAN_BLUE, fill_color=BOX_FILL, fill_opacity=0.4,
            buff=0.45, corner_radius=0.12, stroke_width=2)

        self.play(Create(liss_c, run_time=0.8), FadeIn(liss_g, run_time=0.6))
        self.play(FadeIn(end_box), FadeIn(end_name, scale=0.95), run_time=0.4)
        self.play(FadeIn(end_tag, shift=UP*0.1), run_time=0.3)
        self.play(FadeIn(end_url), run_time=0.2)
        self.play(Circumscribe(end_box, color=MERIDIAN_BLUE, run_time=0.7))
        self.wait(3.0)

        self.play(FadeOut(Group(*self.mobjects)), run_time=0.5)
