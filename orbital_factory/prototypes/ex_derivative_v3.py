"""
"Why eˣ Is Its Own Derivative" — Orbital Short v3
===================================================
Same visuals as v2 but with PROPER TTS-locked timing.
Each scene uses DUR(scene_id) from manifest and pads exactly.

Render:
  cd ~/Desktop/Orbital/orbital_factory && source venv/bin/activate
  PATH="/Library/TeX/texbin:$PATH" manim render prototypes/ex_derivative_v3.py ExDerivativeV3 \
    -o ex_derivative_v3.mp4 --format mp4 -r 1080,1920 --frame_rate 60 --flush_cache
"""
from manim import *
import numpy as np
import json

config.frame_width = 4.5
config.frame_height = 8.0

# ── BRAND COLORS (LOCKED) ──
VIOLET = "#8B5CF6"
CYAN = "#22D3EE"
GREEN = "#39FF14"
ORANGE = "#F97316"
BOX_FILL = "#1a1130"
END_CYAN = "#00E5FF"
GRID_COL = "#1a1a3a"

FW = 4.5
FH = 8.0

# ── TTS MANIFEST (exact durations) ──
with open("output/tts/ex_derivative_scenes/manifest.json") as f:
    _manifest = json.load(f)
    MANIFEST = {s["id"]: s for s in _manifest["scenes"]}

def DUR(scene_id):
    return MANIFEST[scene_id]["duration"]

# Silence beats after certain scenes
SILENCE = {
    "proof_watch": 2.0,
    "the_answer": 2.0,
    "punchline": 2.5,
}
END_CARD_DUR = 3.0


def _box(mob, color=VIOLET, fill=BOX_FILL, opacity=0.6, buff=0.12):
    return SurroundingRectangle(
        mob, color=color, fill_color=fill, fill_opacity=opacity,
        buff=buff, corner_radius=0.1, stroke_width=2.5
    )


def _neon_grid(center, w, h, spacing=0.5, color=GRID_COL, opacity=0.25):
    lines = VGroup()
    cx, cy = center[0], center[1]
    x = cx - w / 2
    while x <= cx + w / 2:
        lines.add(Line([x, cy - h / 2, 0], [x, cy + h / 2, 0],
                       color=color, stroke_width=0.5, stroke_opacity=opacity))
        x += spacing
    y = cy - h / 2
    while y <= cy + h / 2:
        lines.add(Line([cx - w / 2, y, 0], [cx + w / 2, y, 0],
                       color=color, stroke_width=0.5, stroke_opacity=opacity))
        y += spacing
    return lines


def _make_axes(x_range, y_range, x_len, y_len, center):
    return Axes(
        x_range=x_range, y_range=y_range,
        x_length=x_len, y_length=y_len,
        tips=False,
        axis_config={"color": VIOLET, "stroke_width": 1.5, "stroke_opacity": 0.6},
    ).move_to(center)


class ExDerivativeV3(Scene):
    def construct(self):
        self.camera.background_color = BLACK

        # ── Persistent border + watermark ──
        border = Rectangle(width=FW - 0.1, height=FH - 0.1, color=VIOLET,
                           stroke_width=2.5, stroke_opacity=0.7, fill_opacity=0)
        border_glow = Rectangle(width=FW - 0.05, height=FH - 0.05, color=VIOLET,
                                stroke_width=5, stroke_opacity=0.12, fill_opacity=0)
        self.add(border_glow, border)
        wm = Text("ORBITAL", font_size=10, color=WHITE, weight=BOLD)
        wm.set_opacity(0.35).move_to([-FW / 2 + 0.45, -FH / 2 + 0.2, 0])
        self.add(wm)

        # ═══════════════════════════════════════════════
        # SCENE 1: HOOK
        # DUR = 4.69s
        # ═══════════════════════════════════════════════
        dur = DUR("hook")

        hook_grid = _neon_grid([0, 0], FW, FH, 0.6, GRID_COL, 0.15)
        self.add(hook_grid)

        hook_eq = MathTex(r"\frac{d}{dx}\left[e^x\right] = e^x",
                          font_size=42, color=WHITE)
        hook_eq.move_to([0, 1.5, 0])
        hook_box = _box(hook_eq, VIOLET, buff=0.18)

        arrow = CurvedArrow(
            hook_eq.get_right() + RIGHT * 0.2 + UP * 0.4,
            hook_eq.get_right() + RIGHT * 0.2 + DOWN * 0.4,
            color=GREEN, stroke_width=3, angle=-PI
        )

        q_text = MathTex(r"\text{same function?}", font_size=28, color=CYAN)
        q_box = _box(q_text, CYAN, BOX_FILL, 0.5, 0.1)
        VGroup(q_box, q_text).move_to([0, -0.3, 0])

        bg_curve1 = FunctionGraph(
            lambda x: 0.3 * np.exp(0.6 * x), x_range=[-2.2, 2.2],
            color=VIOLET, stroke_width=1.5, stroke_opacity=0.15
        ).shift(DOWN * 2)
        bg_curve2 = FunctionGraph(
            lambda x: 0.2 * np.exp(0.5 * x), x_range=[-2.2, 2.2],
            color=CYAN, stroke_width=1, stroke_opacity=0.1
        ).shift(DOWN * 2.8)
        self.add(bg_curve1, bg_curve2)

        self.play(FadeIn(hook_box), Write(hook_eq), run_time=0.4)  # 0.4
        self.play(Create(arrow), run_time=0.3)                      # 0.7
        self.play(FadeIn(q_box), Write(q_text), run_time=0.3)       # 1.0
        self.play(arrow.animate.set_color(GREEN).scale(1.1), run_time=0.3)  # 1.3
        self.play(arrow.animate.scale(1 / 1.1), run_time=0.3)       # 1.6

        self.wait(max(0.3, dur - 1.6))  # pad to 4.69

        self.play(FadeOut(VGroup(hook_eq, hook_box, q_text, q_box, arrow,
                                  bg_curve1, bg_curve2, hook_grid)), run_time=0.3)

        # ═══════════════════════════════════════════════
        # SCENE 2: DERIVATIVE REMINDER
        # DUR = 9.47s
        # ═══════════════════════════════════════════════
        dur = DUR("derivative_reminder")

        title = Text("The derivative = slope at a point", font_size=16,
                      color=VIOLET, weight=BOLD)
        title_box = _box(title, VIOLET, BOX_FILL, 0.5, 0.08)
        VGroup(title_box, title).move_to([0, 3.3, 0])
        self.play(FadeIn(title_box), FadeIn(title), run_time=0.3)  # 0.3

        graph_grid = _neon_grid([0, 0.5], 3.8, 4.0, 0.5, GRID_COL, 0.2)
        self.play(FadeIn(graph_grid), run_time=0.2)  # 0.5

        ax_r = _make_axes([0, 4, 1], [0, 5, 1], 3.6, 3.8, [0, 0.5, 0])
        curve_r = ax_r.plot(lambda x: 0.3 * x ** 2 + 0.5, x_range=[0.1, 3.8],
                            color=VIOLET, stroke_width=3)
        self.play(Create(ax_r, run_time=0.3), Create(curve_r, run_time=0.5))  # 1.0

        x_rem = ValueTracker(1.0)

        def _get_tang_r():
            x = x_rem.get_value()
            y = 0.3 * x ** 2 + 0.5
            s = 0.6 * x
            d = 0.6
            return Line(
                ax_r.c2p(x - d, y - s * d),
                ax_r.c2p(x + d, y + s * d),
                color=GREEN, stroke_width=3
            )
        tang_r = always_redraw(_get_tang_r)

        dot_r = always_redraw(
            lambda: Dot(
                ax_r.c2p(x_rem.get_value(),
                         0.3 * x_rem.get_value() ** 2 + 0.5),
                color=GREEN, radius=0.07
            ).set_glow_factor(0.8)
        )

        def _get_slope_tag():
            x = x_rem.get_value()
            y = 0.3 * x ** 2 + 0.5
            s = 0.6 * x
            t = Text(f"slope = {s:.1f}", font_size=13, color=GREEN, weight=BOLD)
            pt = ax_r.c2p(x, y)
            t.next_to(pt, UR, buff=0.15)
            return t
        slope_tag = always_redraw(_get_slope_tag)

        self.add(tang_r, dot_r, slope_tag)
        self.play(x_rem.animate.set_value(3.2), run_time=3.0, rate_func=smooth)  # 4.0
        self.play(x_rem.animate.set_value(1.8), run_time=2.0, rate_func=smooth)  # 6.0

        cap = Text("rate of change at that exact point", font_size=13,
                    color=CYAN, weight=BOLD)
        cap_box = _box(cap, CYAN, BOX_FILL, 0.4, 0.08)
        VGroup(cap_box, cap).move_to([0, -2.5, 0])
        self.play(FadeIn(cap_box), FadeIn(cap), run_time=0.3)  # 6.3

        self.wait(max(0.3, dur - 6.3))  # pad to 9.47

        self.play(FadeOut(VGroup(title, title_box, graph_grid, ax_r, curve_r,
                                  tang_r, dot_r, slope_tag, cap, cap_box)), run_time=0.3)

        # ═══════════════════════════════════════════════
        # SCENE 3: THE CLAIM — eˣ slope = height
        # DUR = 8.68s
        # ═══════════════════════════════════════════════
        dur = DUR("the_claim")

        claim_title = Text("On eˣ, something wild happens", font_size=16,
                           color=GREEN, weight=BOLD)
        claim_box = _box(claim_title, GREEN, BOX_FILL, 0.5, 0.08)
        VGroup(claim_box, claim_title).move_to([0, 3.3, 0])
        self.play(FadeIn(claim_box), FadeIn(claim_title), run_time=0.3)  # 0.3

        g3_grid = _neon_grid([-0.3, 0.3], 3.0, 4.0, 0.5, GRID_COL, 0.2)
        self.play(FadeIn(g3_grid), run_time=0.2)  # 0.5

        ax_e = _make_axes([0, 2.5, 0.5], [0, 10, 2], 2.6, 3.8, [-0.3, 0.3, 0])
        curve_e = ax_e.plot(lambda x: np.exp(x), x_range=[0, 2.3],
                            color=CYAN, stroke_width=3)
        label_e = MathTex(r"e^x", font_size=22, color=CYAN)
        label_e.move_to([0.8, 2.8, 0])
        lbl_box = _box(label_e, CYAN, BOX_FILL, 0.4, 0.06)

        self.play(Create(ax_e, run_time=0.3), Create(curve_e, run_time=0.5))  # 1.0
        self.play(FadeIn(lbl_box), FadeIn(label_e), run_time=0.2)  # 1.2

        # Gauge tracks
        gauge_h_track = RoundedRectangle(
            width=0.28, height=3.2, color=CYAN,
            fill_color=BOX_FILL, fill_opacity=0.4,
            stroke_width=1.5, corner_radius=0.05
        ).move_to([1.65, 0.3, 0])
        gauge_s_track = RoundedRectangle(
            width=0.28, height=3.2, color=GREEN,
            fill_color=BOX_FILL, fill_opacity=0.4,
            stroke_width=1.5, corner_radius=0.05
        ).move_to([2.0, 0.3, 0])
        h_lbl = Text("H", font_size=11, color=CYAN, weight=BOLD).move_to([1.65, -1.5, 0])
        s_lbl = Text("S", font_size=11, color=GREEN, weight=BOLD).move_to([2.0, -1.5, 0])

        self.play(FadeIn(VGroup(gauge_h_track, gauge_s_track, h_lbl, s_lbl)), run_time=0.3)  # 1.5

        # Static point at x=1
        x_pt = 1.0
        y_pt = np.exp(x_pt)
        dot_e = Dot(ax_e.c2p(x_pt, y_pt), color=GREEN, radius=0.07).set_glow_factor(0.8)

        dx_t = 0.5
        tang_e = Line(
            ax_e.c2p(x_pt - dx_t, y_pt - y_pt * dx_t),
            ax_e.c2p(x_pt + dx_t, y_pt + y_pt * dx_t),
            color=GREEN, stroke_width=3
        )
        h_line = DashedLine(ax_e.c2p(x_pt, 0), ax_e.c2p(x_pt, y_pt),
                            color=CYAN, stroke_width=1.5, dash_length=0.06)

        self.play(FadeIn(dot_e), Create(tang_e), Create(h_line), run_time=0.4)  # 1.9

        # Gauge fills
        bar_h = y_pt / 10.0 * 3.2
        gauge_h_fill = RoundedRectangle(
            width=0.22, height=bar_h, color=CYAN,
            fill_color=CYAN, fill_opacity=0.5,
            stroke_width=0, corner_radius=0.04
        ).move_to([1.65, 0.3 - 3.2 / 2 + bar_h / 2, 0])

        gauge_s_fill = RoundedRectangle(
            width=0.22, height=bar_h, color=GREEN,
            fill_color=GREEN, fill_opacity=0.5,
            stroke_width=0, corner_radius=0.04
        ).move_to([2.0, 0.3 - 3.2 / 2 + bar_h / 2, 0])

        h_val = Text(f"{y_pt:.1f}", font_size=12, color=CYAN, weight=BOLD)
        h_val.next_to(gauge_h_fill, UP, buff=0.05)
        s_val = Text(f"{y_pt:.1f}", font_size=12, color=GREEN, weight=BOLD)
        s_val.next_to(gauge_s_fill, UP, buff=0.05)

        self.play(
            GrowFromEdge(gauge_h_fill, DOWN),
            GrowFromEdge(gauge_s_fill, DOWN),
            FadeIn(h_val), FadeIn(s_val),
            run_time=0.5
        )  # 2.4

        # Match indicator
        match_eq = MathTex(r"=", font_size=28, color=GREEN)
        match_eq.move_to([1.825, 0.3 - 3.2 / 2 + bar_h + 0.3, 0])
        self.play(
            FadeIn(match_eq, scale=1.5),
            Flash(dot_e, color=GREEN, line_length=0.25, num_lines=10, run_time=0.3),
            run_time=0.4
        )  # 2.8

        match_text = MathTex(r"\text{height} = \text{slope}", font_size=24, color=GREEN)
        match_bx = _box(match_text, GREEN, BOX_FILL, 0.5, 0.1)
        VGroup(match_bx, match_text).move_to([0, -2.8, 0])
        self.play(FadeIn(match_bx), Write(match_text), run_time=0.3)  # 3.1

        self.wait(max(0.3, dur - 3.1))  # pad to 8.68

        self.play(FadeOut(VGroup(
            claim_title, claim_box, dot_e, tang_e, h_line,
            gauge_h_fill, gauge_s_fill, h_val, s_val, match_eq,
            match_text, match_bx
        )), run_time=0.3)

        # ═══════════════════════════════════════════════
        # SCENE 4: SLIDING DOT — live gauges
        # DUR = 7.89s + 2.0s silence = 9.89s
        # ═══════════════════════════════════════════════
        dur = DUR("proof_watch")
        sil = SILENCE["proof_watch"]

        slide_title = Text("Watch them stay equal", font_size=16,
                           color=GREEN, weight=BOLD)
        slide_bx = _box(slide_title, GREEN, BOX_FILL, 0.5, 0.08)
        VGroup(slide_bx, slide_title).move_to([0, 3.3, 0])
        self.play(FadeIn(slide_bx), FadeIn(slide_title), run_time=0.2)  # 0.2

        x_track = ValueTracker(0.3)

        dot_dyn = always_redraw(
            lambda: Dot(
                ax_e.c2p(x_track.get_value(), np.exp(x_track.get_value())),
                color=GREEN, radius=0.07
            ).set_glow_factor(0.8)
        )

        def _get_tang():
            x = x_track.get_value()
            y = np.exp(x)
            d = 0.4
            return Line(
                ax_e.c2p(x - d, y - y * d),
                ax_e.c2p(x + d, y + y * d),
                color=GREEN, stroke_width=3
            )
        tang_dyn = always_redraw(_get_tang)

        def _get_hline():
            x = x_track.get_value()
            return DashedLine(
                ax_e.c2p(x, 0), ax_e.c2p(x, np.exp(x)),
                color=CYAN, stroke_width=1.2, dash_length=0.05
            )
        hline_dyn = always_redraw(_get_hline)

        # Dynamic gauge fills
        def _get_h_gauge():
            y = np.exp(x_track.get_value())
            h = min(y / 10.0 * 3.2, 3.15)
            r = RoundedRectangle(
                width=0.22, height=max(h, 0.05), color=CYAN,
                fill_color=CYAN, fill_opacity=0.5,
                stroke_width=0, corner_radius=0.04
            )
            r.move_to([1.65, 0.3 - 3.2 / 2 + max(h, 0.05) / 2, 0])
            return r
        h_gauge = always_redraw(_get_h_gauge)

        def _get_s_gauge():
            y = np.exp(x_track.get_value())
            h = min(y / 10.0 * 3.2, 3.15)
            r = RoundedRectangle(
                width=0.22, height=max(h, 0.05), color=GREEN,
                fill_color=GREEN, fill_opacity=0.5,
                stroke_width=0, corner_radius=0.04
            )
            r.move_to([2.0, 0.3 - 3.2 / 2 + max(h, 0.05) / 2, 0])
            return r
        s_gauge = always_redraw(_get_s_gauge)

        def _get_h_val():
            y = np.exp(x_track.get_value())
            h = min(y / 10.0 * 3.2, 3.15)
            t = Text(f"{y:.1f}", font_size=11, color=CYAN, weight=BOLD)
            t.move_to([1.65, 0.3 - 3.2 / 2 + h + 0.12, 0])
            return t
        h_val_dyn = always_redraw(_get_h_val)

        def _get_s_val():
            y = np.exp(x_track.get_value())
            h = min(y / 10.0 * 3.2, 3.15)
            t = Text(f"{y:.1f}", font_size=11, color=GREEN, weight=BOLD)
            t.move_to([2.0, 0.3 - 3.2 / 2 + h + 0.12, 0])
            return t
        s_val_dyn = always_redraw(_get_s_val)

        self.add(dot_dyn, tang_dyn, hline_dyn, h_gauge, s_gauge, h_val_dyn, s_val_dyn)

        # Slide — use most of the TTS duration for the animation
        slide_time = dur - 0.5  # 0.2 title + slide + 0.3 flash
        self.play(
            x_track.animate.set_value(2.2),
            run_time=slide_time,
            rate_func=smooth
        )  # ~7.59

        self.play(
            Flash(dot_dyn, color=GREEN, line_length=0.3, num_lines=12, run_time=0.3),
            run_time=0.3
        )  # ~7.89

        # Silence beat
        self.wait(sil)  # +2.0

        # Clear
        self.play(FadeOut(VGroup(
            slide_title, slide_bx, g3_grid, ax_e, curve_e, label_e, lbl_box,
            gauge_h_track, gauge_s_track, h_lbl, s_lbl,
            dot_dyn, tang_dyn, hline_dyn, h_gauge, s_gauge, h_val_dyn, s_val_dyn
        )), run_time=0.3)

        # ═══════════════════════════════════════════════
        # SCENE 5: CONTRAST 2ˣ
        # DUR = 6.78s
        # ═══════════════════════════════════════════════
        dur = DUR("contrast_2x")

        c2_grid = _neon_grid([0, 0.3], 3.8, 4.5, 0.5, GRID_COL, 0.2)
        self.play(FadeIn(c2_grid), run_time=0.15)  # 0.15

        c2_title = MathTex(r"2^x", font_size=32, color=ORANGE)
        c2_bx = _box(c2_title, ORANGE, BOX_FILL, 0.5, 0.1)
        VGroup(c2_bx, c2_title).move_to([0, 3.3, 0])
        self.play(FadeIn(c2_bx), FadeIn(c2_title), run_time=0.2)  # 0.35

        ax_2 = _make_axes([0, 3.5, 1], [0, 10, 2], 2.6, 3.5, [-0.3, 0.2, 0])
        curve_2 = ax_2.plot(lambda x: 2 ** x, x_range=[0, 3.3],
                            color=ORANGE, stroke_width=3)
        self.play(Create(ax_2, run_time=0.3), Create(curve_2, run_time=0.4))  # 0.75

        # Gauge tracks
        g2_ht = RoundedRectangle(width=0.28, height=3.0, color=ORANGE,
                                  fill_color=BOX_FILL, fill_opacity=0.4,
                                  stroke_width=1.5, corner_radius=0.05).move_to([1.65, 0.2, 0])
        g2_st = RoundedRectangle(width=0.28, height=3.0, color=ORANGE,
                                  fill_color=BOX_FILL, fill_opacity=0.4,
                                  stroke_width=1.5, corner_radius=0.05).move_to([2.0, 0.2, 0])
        g2_hl = Text("H", font_size=11, color=ORANGE, weight=BOLD).move_to([1.65, -1.4, 0])
        g2_sl = Text("S", font_size=11, color=ORANGE, weight=BOLD).move_to([2.0, -1.4, 0])
        self.play(FadeIn(VGroup(g2_ht, g2_st, g2_hl, g2_sl)), run_time=0.2)  # 0.95

        x_2 = 2.0
        y_2 = 2 ** x_2  # 4.0
        s_2 = y_2 * np.log(2)  # 2.77

        dot_2 = Dot(ax_2.c2p(x_2, y_2), color=ORANGE, radius=0.07)
        tang_2 = Line(
            ax_2.c2p(x_2 - 0.4, y_2 - s_2 * 0.4),
            ax_2.c2p(x_2 + 0.4, y_2 + s_2 * 0.4),
            color=ORANGE, stroke_width=3
        )
        hl_2 = DashedLine(ax_2.c2p(x_2, 0), ax_2.c2p(x_2, y_2),
                           color=ORANGE, stroke_width=1.2, dash_length=0.06)
        self.play(FadeIn(dot_2), Create(tang_2), Create(hl_2), run_time=0.3)  # 1.25

        # Gauge fills — DIFFERENT heights
        h_bar_2 = y_2 / 10 * 3.0
        s_bar_2 = s_2 / 10 * 3.0
        g2_hf = RoundedRectangle(width=0.22, height=h_bar_2, color=ORANGE,
                                  fill_color=ORANGE, fill_opacity=0.5,
                                  stroke_width=0, corner_radius=0.04)
        g2_hf.move_to([1.65, 0.2 - 3.0 / 2 + h_bar_2 / 2, 0])

        g2_sf = RoundedRectangle(width=0.22, height=s_bar_2, color=ORANGE,
                                  fill_color=ORANGE, fill_opacity=0.3,
                                  stroke_width=0, corner_radius=0.04)
        g2_sf.move_to([2.0, 0.2 - 3.0 / 2 + s_bar_2 / 2, 0])

        g2_hv = Text(f"{y_2:.1f}", font_size=12, color=ORANGE, weight=BOLD)
        g2_hv.next_to(g2_hf, UP, buff=0.05)
        g2_sv = Text(f"{s_2:.1f}", font_size=12, color=ORANGE, weight=BOLD)
        g2_sv.next_to(g2_sf, UP, buff=0.05)

        self.play(GrowFromEdge(g2_hf, DOWN), GrowFromEdge(g2_sf, DOWN),
                  FadeIn(g2_hv), FadeIn(g2_sv), run_time=0.4)  # 1.65

        neq_2 = MathTex(r"\neq", font_size=30, color="#FF4444")
        neq_2.move_to([1.825, 0.2 + 1.0, 0])
        neq_bx = _box(neq_2, "#FF4444", "#2a0a0a", 0.4, 0.06)
        self.play(FadeIn(neq_bx), FadeIn(neq_2, scale=1.5), run_time=0.3)  # 1.95

        lt_text = MathTex(r"\text{slope} < \text{height}", font_size=22, color=ORANGE)
        lt_bx = _box(lt_text, ORANGE, BOX_FILL, 0.5, 0.1)
        VGroup(lt_bx, lt_text).move_to([0, -2.8, 0])
        self.play(FadeIn(lt_bx), Write(lt_text), run_time=0.3)  # 2.25

        self.wait(max(0.3, dur - 2.25))  # pad to 6.78

        self.play(FadeOut(VGroup(
            c2_grid, c2_title, c2_bx, ax_2, curve_2, dot_2, tang_2, hl_2,
            g2_ht, g2_st, g2_hl, g2_sl, g2_hf, g2_sf, g2_hv, g2_sv,
            neq_2, neq_bx, lt_text, lt_bx
        )), run_time=0.3)

        # ═══════════════════════════════════════════════
        # SCENE 6: CONTRAST 3ˣ
        # DUR = 5.25s
        # ═══════════════════════════════════════════════
        dur = DUR("contrast_3x")

        c3_grid = _neon_grid([0, 0.3], 3.8, 4.5, 0.5, GRID_COL, 0.2)
        self.play(FadeIn(c3_grid), run_time=0.15)  # 0.15

        c3_title = MathTex(r"3^x", font_size=32, color=CYAN)
        c3_bx = _box(c3_title, CYAN, BOX_FILL, 0.5, 0.1)
        VGroup(c3_bx, c3_title).move_to([0, 3.3, 0])
        self.play(FadeIn(c3_bx), FadeIn(c3_title), run_time=0.2)  # 0.35

        ax_3 = _make_axes([0, 2.5, 0.5], [0, 10, 2], 2.6, 3.5, [-0.3, 0.2, 0])
        curve_3 = ax_3.plot(lambda x: 3 ** x, x_range=[0, 2.1],
                            color=CYAN, stroke_width=3)
        self.play(Create(ax_3, run_time=0.3), Create(curve_3, run_time=0.4))  # 0.75

        g3_ht = RoundedRectangle(width=0.28, height=3.0, color=CYAN,
                                  fill_color=BOX_FILL, fill_opacity=0.4,
                                  stroke_width=1.5, corner_radius=0.05).move_to([1.65, 0.2, 0])
        g3_st = RoundedRectangle(width=0.28, height=3.0, color=CYAN,
                                  fill_color=BOX_FILL, fill_opacity=0.4,
                                  stroke_width=1.5, corner_radius=0.05).move_to([2.0, 0.2, 0])
        g3_hl = Text("H", font_size=11, color=CYAN, weight=BOLD).move_to([1.65, -1.4, 0])
        g3_sl = Text("S", font_size=11, color=CYAN, weight=BOLD).move_to([2.0, -1.4, 0])
        self.play(FadeIn(VGroup(g3_ht, g3_st, g3_hl, g3_sl)), run_time=0.2)  # 0.95

        x_3 = 1.5
        y_3 = 3 ** x_3
        s_3 = y_3 * np.log(3)

        dot_3 = Dot(ax_3.c2p(x_3, y_3), color=CYAN, radius=0.07)
        tang_3 = Line(
            ax_3.c2p(x_3 - 0.35, y_3 - s_3 * 0.35),
            ax_3.c2p(x_3 + 0.35, y_3 + s_3 * 0.35),
            color=CYAN, stroke_width=3
        )
        hl_3 = DashedLine(ax_3.c2p(x_3, 0), ax_3.c2p(x_3, y_3),
                           color=CYAN, stroke_width=1.2, dash_length=0.06)
        self.play(FadeIn(dot_3), Create(tang_3), Create(hl_3), run_time=0.3)  # 1.25

        h_bar_3 = y_3 / 10 * 3.0
        s_bar_3 = min(s_3 / 10 * 3.0, 2.95)
        g3_hf = RoundedRectangle(width=0.22, height=h_bar_3, color=CYAN,
                                  fill_color=CYAN, fill_opacity=0.5,
                                  stroke_width=0, corner_radius=0.04)
        g3_hf.move_to([1.65, 0.2 - 3.0 / 2 + h_bar_3 / 2, 0])
        g3_sf = RoundedRectangle(width=0.22, height=s_bar_3, color=CYAN,
                                  fill_color=CYAN, fill_opacity=0.3,
                                  stroke_width=0, corner_radius=0.04)
        g3_sf.move_to([2.0, 0.2 - 3.0 / 2 + s_bar_3 / 2, 0])

        g3_hv = Text(f"{y_3:.1f}", font_size=12, color=CYAN, weight=BOLD)
        g3_hv.next_to(g3_hf, UP, buff=0.05)
        g3_sv = Text(f"{s_3:.1f}", font_size=12, color=CYAN, weight=BOLD)
        g3_sv.next_to(g3_sf, UP, buff=0.05)

        self.play(GrowFromEdge(g3_hf, DOWN), GrowFromEdge(g3_sf, DOWN),
                  FadeIn(g3_hv), FadeIn(g3_sv), run_time=0.4)  # 1.65

        neq_3 = MathTex(r"\neq", font_size=30, color="#FF4444")
        neq_3.move_to([1.825, 0.2 + 1.0, 0])
        neq_bx3 = _box(neq_3, "#FF4444", "#2a0a0a", 0.4, 0.06)
        self.play(FadeIn(neq_bx3), FadeIn(neq_3, scale=1.5), run_time=0.3)  # 1.95

        gt_text = MathTex(r"\text{slope} > \text{height}", font_size=22, color=CYAN)
        gt_bx = _box(gt_text, CYAN, BOX_FILL, 0.5, 0.1)
        VGroup(gt_bx, gt_text).move_to([0, -2.8, 0])
        self.play(FadeIn(gt_bx), Write(gt_text), run_time=0.3)  # 2.25

        self.wait(max(0.3, dur - 2.25))  # pad to 5.25

        self.play(FadeOut(VGroup(
            c3_grid, c3_title, c3_bx, ax_3, curve_3, dot_3, tang_3, hl_3,
            g3_ht, g3_st, g3_hl, g3_sl, g3_hf, g3_sf, g3_hv, g3_sv,
            neq_3, neq_bx3, gt_text, gt_bx
        )), run_time=0.3)

        # ═══════════════════════════════════════════════
        # SCENE 7: THE ANSWER — e ≈ 2.718
        # DUR = 9.75s + 2.0s silence = 11.75s
        # ═══════════════════════════════════════════════
        dur = DUR("the_answer")
        sil = SILENCE["the_answer"]

        ans_grid = _neon_grid([0, 0], FW, FH, 0.6, GRID_COL, 0.12)
        self.play(FadeIn(ans_grid), run_time=0.15)  # 0.15

        ans_title = Text("Only one base works", font_size=18, color=GREEN, weight=BOLD)
        ans_bx = _box(ans_title, GREEN, BOX_FILL, 0.5, 0.08)
        VGroup(ans_bx, ans_title).move_to([0, 3.3, 0])
        self.play(FadeIn(ans_bx), FadeIn(ans_title), run_time=0.2)  # 0.35

        # Number line
        nl = NumberLine(x_range=[1.5, 3.5, 0.5], length=3.2,
                        color=WHITE, stroke_width=1.5,
                        include_numbers=False, include_tip=False)
        nl.move_to([0, 2.2, 0])

        n2 = MathTex("2", font_size=20, color=ORANGE)
        n2_bx = _box(n2, ORANGE, BOX_FILL, 0.3, 0.04)
        VGroup(n2_bx, n2).next_to(nl.n2p(2), DOWN, buff=0.15)

        n3 = MathTex("3", font_size=20, color=CYAN)
        n3_bx = _box(n3, CYAN, BOX_FILL, 0.3, 0.04)
        VGroup(n3_bx, n3).next_to(nl.n2p(3), DOWN, buff=0.15)

        ne = MathTex(r"e \approx 2.718", font_size=18, color=GREEN)
        ne_bx = _box(ne, GREEN, BOX_FILL, 0.5, 0.06)
        VGroup(ne_bx, ne).next_to(nl.n2p(2.718), UP, buff=0.15)

        e_dot = Dot(nl.n2p(2.718), color=GREEN, radius=0.09).set_glow_factor(1.0)

        self.play(Create(nl), FadeIn(VGroup(n2_bx, n2)), FadeIn(VGroup(n3_bx, n3)),
                  run_time=0.4)  # 0.75
        self.play(FadeIn(e_dot, scale=0.5), FadeIn(VGroup(ne_bx, ne)), run_time=0.4)  # 1.15
        self.play(Flash(e_dot, color=GREEN, line_length=0.3, num_lines=10, run_time=0.3))  # 1.45

        # eˣ graph
        ax_f = _make_axes([0, 2.5, 0.5], [0, 10, 2], 2.6, 2.8, [-0.3, -0.8, 0])
        curve_f = ax_f.plot(lambda x: np.exp(x), x_range=[0, 2.3],
                             color=GREEN, stroke_width=3)
        f_grid = _neon_grid([-0.3, -0.8], 2.8, 3.0, 0.5, GRID_COL, 0.2)
        self.play(FadeIn(f_grid), Create(ax_f, run_time=0.3),
                  Create(curve_f, run_time=0.4))  # 1.85

        x_f = ValueTracker(0.5)
        dot_f = always_redraw(
            lambda: Dot(
                ax_f.c2p(x_f.get_value(), np.exp(x_f.get_value())),
                color=GREEN, radius=0.07
            ).set_glow_factor(0.8)
        )
        def _get_match():
            y = np.exp(x_f.get_value())
            t = MathTex(
                r"\text{height} = \text{slope} = " + f"{y:.1f}",
                font_size=18, color=GREEN
            )
            bx = _box(t, GREEN, BOX_FILL, 0.4, 0.08)
            VGroup(bx, t).move_to([0, -3.0, 0])
            return VGroup(bx, t)
        match_lbl = always_redraw(_get_match)

        self.add(dot_f, match_lbl)

        # Slide using remaining TTS time
        slide_dur = dur - 1.85  # ~7.9s of sliding
        self.play(x_f.animate.set_value(2.0), run_time=slide_dur, rate_func=smooth)

        # Silence beat
        self.wait(sil)  # +2.0

        self.play(FadeOut(VGroup(
            ans_grid, ans_title, ans_bx, nl, n2, n2_bx, n3, n3_bx,
            ne, ne_bx, e_dot, f_grid, ax_f, curve_f, dot_f, match_lbl
        )), run_time=0.3)

        # ═══════════════════════════════════════════════
        # SCENE 8: PUNCHLINE
        # DUR = 12.21s + 2.5s silence = 14.71s
        # ═══════════════════════════════════════════════
        dur = DUR("punchline")
        sil = SILENCE["punchline"]

        punch_grid = _neon_grid([0, 0], FW, FH, 0.6, GRID_COL, 0.15)
        self.play(FadeIn(punch_grid), run_time=0.15)  # 0.15

        punch_eq = MathTex(r"\frac{d}{dx}\left[e^x\right] = e^x",
                           font_size=42, color=GREEN)
        punch_eq.move_to([0, 1.5, 0])
        punch_box = _box(punch_eq, GREEN, BOX_FILL, 0.6, 0.18)

        self.play(FadeIn(punch_box), Write(punch_eq), run_time=0.6)  # 0.75
        self.play(Circumscribe(punch_box, color=GREEN, run_time=0.5))  # 1.25
        self.wait(1.0)  # 2.25

        r1 = Text("The slope was always the height.", font_size=16,
                   color=CYAN, weight=BOLD)
        r1_bx = _box(r1, CYAN, BOX_FILL, 0.4, 0.08)
        VGroup(r1_bx, r1).move_to([0, -0.3, 0])
        self.play(FadeIn(r1_bx), Write(r1), run_time=0.4)  # 2.65
        self.wait(0.5)  # 3.15

        r2 = Text("That's why the function doesn't change.", font_size=14,
                   color=VIOLET, weight=BOLD)
        r2_bx = _box(r2, VIOLET, BOX_FILL, 0.3, 0.06)
        VGroup(r2_bx, r2).move_to([0, -1.3, 0])
        self.play(FadeIn(r2_bx), Write(r2), run_time=0.4)  # 3.55
        self.wait(0.5)  # 4.05

        # Recap row
        recap_2 = MathTex(r"2^x: \text{slope} < \text{height}", font_size=16, color=ORANGE)
        rc2_bx = _box(recap_2, ORANGE, BOX_FILL, 0.3, 0.06)
        VGroup(rc2_bx, recap_2).move_to([0, -2.3, 0])

        recap_3 = MathTex(r"3^x: \text{slope} > \text{height}", font_size=16, color=CYAN)
        rc3_bx = _box(recap_3, CYAN, BOX_FILL, 0.3, 0.06)
        VGroup(rc3_bx, recap_3).move_to([0, -2.9, 0])

        recap_e = MathTex(r"e^x: \text{slope} = \text{height}", font_size=16, color=GREEN)
        rce_bx = _box(recap_e, GREEN, BOX_FILL, 0.5, 0.06)
        VGroup(rce_bx, recap_e).move_to([0, -3.5, 0])

        self.play(FadeIn(rc2_bx), Write(recap_2), run_time=0.3)  # 4.35
        self.play(FadeIn(rc3_bx), Write(recap_3), run_time=0.3)  # 4.65
        self.play(FadeIn(rce_bx), Write(recap_e), run_time=0.3)  # 4.95
        self.play(Circumscribe(rce_bx, color=GREEN, run_time=0.5))  # 5.45

        self.wait(max(0.5, dur - 5.45))  # pad to 12.21

        # Silence beat
        self.wait(sil)  # +2.5

        self.play(FadeOut(VGroup(
            punch_grid, punch_eq, punch_box, r1, r1_bx, r2, r2_bx,
            recap_2, rc2_bx, recap_3, rc3_bx, recap_e, rce_bx
        )), run_time=0.4)

        # ═══════════════════════════════════════════════
        # SCENE 9: END CARD (3.0s)
        # ═══════════════════════════════════════════════
        _A, _B = 1.2, 0.95
        liss_glow = ParametricFunction(
            lambda t: np.array([_A * np.sin(2 * t), _B * np.sin(3 * t), 0]),
            t_range=[0, TAU, 0.01],
            color=END_CYAN, stroke_width=6, stroke_opacity=0.2
        )
        liss_core = ParametricFunction(
            lambda t: np.array([_A * np.sin(2 * t), _B * np.sin(3 * t), 0]),
            t_range=[0, TAU, 0.01],
            color=END_CYAN, stroke_width=2, stroke_opacity=1.0
        )
        logo = VGroup(liss_glow, liss_core).move_to([0, 0.8, 0])
        wordmark = Text("ORBITAL", font_size=28, color=END_CYAN, weight=BOLD)
        wordmark.next_to(logo, DOWN, buff=0.3)
        tagline = Text("Watch it click.", font_size=14, color=WHITE)
        tagline.set_opacity(0.5).next_to(wordmark, DOWN, buff=0.15)

        end_grid = _neon_grid([0, 0], FW, FH, 0.8, GRID_COL, 0.1)
        self.add(end_grid)

        self.play(Create(liss_core, run_time=0.8), FadeIn(liss_glow, run_time=0.6))  # 0.8
        self.play(FadeIn(wordmark, shift=UP * 0.1), run_time=0.3)  # 1.1
        self.play(FadeIn(tagline), run_time=0.2)  # 1.3
        self.wait(1.5)  # 2.8
        self.play(FadeOut(VGroup(logo, wordmark, tagline, end_grid)), run_time=0.2)  # 3.0
