"""
"Why eˣ Is Its Own Derivative" — Orbital Short v1
===================================================
The y-value IS the slope. Everywhere. Always.

Visual spec: LOCKED from L'Hôpital v6
  - 4.5×8.0 Manim units, 1080×1920 @60fps
  - Purple border, ORBITAL watermark
  - Scene-based TTS (Allison), bg_synthwave at 12%

Render:
  cd ~/Desktop/Orbital/orbital_factory && source venv/bin/activate
  PATH="/Library/TeX/texbin:$PATH" manim render prototypes/ex_derivative_v1.py ExDerivativeV1 \
    -o ex_derivative_v1.mp4 --format mp4 -r 1080,1920 --frame_rate 60 --flush_cache
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

FW = 4.5
FH = 8.0
MATH_SCALE = 0.85
BOX_SCALE = 0.65
MATH_CENTER_Y = 1.2
GRAPH_CENTER_Y = -1.8

# Load TTS manifest for timing
MANIFEST_PATH = "output/tts/ex_derivative_scenes/manifest.json"
try:
    with open(MANIFEST_PATH) as f:
        manifest = json.load(f)
    TTS = {s["id"]: s["duration"] for s in manifest["scenes"]}
except:
    TTS = {
        "hook": 4.7, "derivative_reminder": 9.5, "the_claim": 8.7,
        "proof_watch": 7.9, "contrast_2x": 6.8, "contrast_3x": 5.2,
        "the_answer": 9.8, "punchline": 12.2,
    }


def _make_box(mob, color=VIOLET, fill=BOX_FILL, opacity=0.6):
    return SurroundingRectangle(
        mob, color=color, fill_color=fill, fill_opacity=opacity,
        buff=0.12, corner_radius=0.1, stroke_width=2.5
    )


def _make_axes(x_range, y_range, x_len, y_len, center):
    return Axes(
        x_range=x_range, y_range=y_range,
        x_length=x_len, y_length=y_len,
        tips=False,
        axis_config={"color": WHITE, "stroke_width": 1.2, "stroke_opacity": 0.4},
    ).move_to(center)


class ExDerivativeV1(Scene):
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
        # SCENE 1: HOOK (4.7s)
        # "This function's derivative is itself."
        # ═══════════════════════════════════════════════
        hook_eq = MathTex(r"\frac{d}{dx}\left[e^x\right] = e^x",
                          font_size=36, color=WHITE)
        hook_eq.move_to([0, 1.5, 0])
        hook_box = _make_box(hook_eq, VIOLET)

        hook_text = Text("derivative is itself?", font_size=20,
                         color=CYAN, weight=BOLD)
        hook_text.move_to([0, 0.2, 0])

        # Arrow looping back
        arrow = CurvedArrow(
            hook_eq.get_right() + RIGHT * 0.1 + UP * 0.3,
            hook_eq.get_right() + RIGHT * 0.1 + DOWN * 0.3,
            color=GREEN, stroke_width=2.5, angle=-PI
        )

        self.play(FadeIn(hook_box), Write(hook_eq), run_time=0.4)
        self.play(Create(arrow), FadeIn(hook_text), run_time=0.4)

        fill_time = max(0, TTS["hook"] - 1.2)
        self.wait(fill_time)

        self.play(FadeOut(VGroup(hook_eq, hook_box, hook_text, arrow)), run_time=0.3)

        # ═══════════════════════════════════════════════
        # SCENE 2: DERIVATIVE REMINDER (9.5s)
        # "The derivative is just the slope of the tangent line"
        # ═══════════════════════════════════════════════
        title = Text("What's a derivative?", font_size=22, color=VIOLET, weight=BOLD)
        title.move_to([0, 3.2, 0])
        self.play(FadeIn(title), run_time=0.3)

        # Simple curve with tangent
        ax_r = _make_axes([0, 4, 1], [0, 4, 1], 3.5, 2.8, [0, 0.8, 0])
        curve_r = ax_r.plot(lambda x: 0.25 * x ** 2 + 0.5, x_range=[0.2, 3.8],
                            color=VIOLET, stroke_width=2.5)
        self.play(Create(ax_r, run_time=0.3), Create(curve_r, run_time=0.5))

        # Tangent at x=2
        x_val = 2.5
        y_val = 0.25 * x_val ** 2 + 0.5
        slope = 0.5 * x_val
        dot_r = Dot(ax_r.c2p(x_val, y_val), color=GREEN, radius=0.06).set_glow_factor(0.6)
        dx = 0.8
        tang = Line(
            ax_r.c2p(x_val - dx, y_val - slope * dx),
            ax_r.c2p(x_val + dx, y_val + slope * dx),
            color=GREEN, stroke_width=2.5
        )

        slope_label = Text("slope", font_size=16, color=GREEN, weight=BOLD)
        slope_label.next_to(tang, RIGHT, buff=0.1)

        self.play(FadeIn(dot_r), Create(tang), run_time=0.4)
        self.play(FadeIn(slope_label), run_time=0.3)

        # "= rate of change" caption
        caption = Text("= instantaneous rate of change", font_size=14, color=WHITE)
        caption.set_opacity(0.7).move_to([0, -1.5, 0])
        self.play(FadeIn(caption), run_time=0.3)

        fill_time = max(0, TTS["derivative_reminder"] - 2.5)
        self.wait(fill_time)

        self.play(FadeOut(VGroup(title, ax_r, curve_r, dot_r, tang,
                                  slope_label, caption)), run_time=0.3)

        # ═══════════════════════════════════════════════
        # SCENE 3: THE CLAIM — slope = height on eˣ (8.7s)
        # ═══════════════════════════════════════════════
        claim_title = Text("On eˣ, something wild happens", font_size=18,
                           color=VIOLET, weight=BOLD)
        claim_title.move_to([0, 3.5, 0])
        self.play(FadeIn(claim_title), run_time=0.3)

        ax_e = _make_axes([0, 3.5, 1], [0, 10, 2], 3.2, 3.5, [0, 0.3, 0])
        curve_e = ax_e.plot(lambda x: np.exp(x), x_range=[0, 2.3],
                            color=CYAN, stroke_width=2.5)
        label_e = MathTex(r"e^x", font_size=20, color=CYAN)
        label_e.next_to(curve_e, UR, buff=0.1)

        self.play(Create(ax_e, run_time=0.3), Create(curve_e, run_time=0.5))
        self.play(FadeIn(label_e), run_time=0.2)

        # Show at one point: x = 1
        x_pt = 1.0
        y_pt = np.exp(x_pt)  # ≈ 2.718
        slope_pt = np.exp(x_pt)  # same!
        dot_e = Dot(ax_e.c2p(x_pt, y_pt), color=GREEN, radius=0.06).set_glow_factor(0.6)

        # Height label (left)
        h_val = Text(f"height = {y_pt:.1f}", font_size=14, color=CYAN, weight=BOLD)
        h_val.move_to([0, -2.0, 0])

        # Slope label (right)
        s_val = Text(f"slope = {slope_pt:.1f}", font_size=14, color=GREEN, weight=BOLD)
        s_val.move_to([0, -2.6, 0])

        # Height line (vertical dashed)
        h_line = DashedLine(ax_e.c2p(x_pt, 0), ax_e.c2p(x_pt, y_pt),
                            color=CYAN, stroke_width=1.5, dash_length=0.08)

        # Tangent
        dx_t = 0.6
        tang_e = Line(
            ax_e.c2p(x_pt - dx_t, y_pt - slope_pt * dx_t),
            ax_e.c2p(x_pt + dx_t, y_pt + slope_pt * dx_t),
            color=GREEN, stroke_width=2.5
        )

        self.play(FadeIn(dot_e), Create(h_line), Create(tang_e), run_time=0.4)
        self.play(FadeIn(h_val), FadeIn(s_val), run_time=0.3)

        # They match! Green pulse
        match_text = Text("THEY MATCH", font_size=16, color=GREEN, weight=BOLD)
        match_text.move_to([0, -3.3, 0])
        self.play(
            FadeIn(match_text, scale=1.3),
            Flash(dot_e, color=GREEN, line_length=0.3, num_lines=8, run_time=0.3),
            run_time=0.4
        )

        fill_time = max(0, TTS["the_claim"] - 2.5)
        self.wait(fill_time)

        # Keep axes but clear labels for next scene
        self.play(FadeOut(VGroup(claim_title, h_val, s_val, match_text,
                                  h_line, tang_e, dot_e, label_e)), run_time=0.3)

        # ═══════════════════════════════════════════════
        # SCENE 4: THE PROOF — Sliding dot with live labels (7.9s + 2s silence)
        # ═══════════════════════════════════════════════
        proof_title = Text("Watch them stay equal", font_size=18,
                           color=GREEN, weight=BOLD)
        proof_title.move_to([0, 3.5, 0])
        self.play(FadeIn(proof_title), run_time=0.2)

        label_e2 = MathTex(r"e^x", font_size=20, color=CYAN)
        label_e2.move_to([1.4, 2.8, 0])
        self.add(label_e2)

        x_track = ValueTracker(0.3)

        # Dynamic dot
        dot_dyn = always_redraw(
            lambda: Dot(
                ax_e.c2p(x_track.get_value(), np.exp(x_track.get_value())),
                color=GREEN, radius=0.06
            ).set_glow_factor(0.6)
        )

        # Dynamic tangent
        def _get_tang():
            x = x_track.get_value()
            y = np.exp(x)
            s = np.exp(x)
            d = 0.5
            return Line(
                ax_e.c2p(x - d, y - s * d),
                ax_e.c2p(x + d, y + s * d),
                color=GREEN, stroke_width=2.5
            )
        tang_dyn = always_redraw(_get_tang)

        # Dynamic height line
        def _get_hline():
            x = x_track.get_value()
            return DashedLine(
                ax_e.c2p(x, 0), ax_e.c2p(x, np.exp(x)),
                color=CYAN, stroke_width=1.2, dash_length=0.06
            )
        hline_dyn = always_redraw(_get_hline)

        # Dynamic labels
        def _get_height_label():
            x = x_track.get_value()
            y = np.exp(x)
            t = Text(f"height = {y:.1f}", font_size=14, color=CYAN, weight=BOLD)
            t.move_to([0, -2.0, 0])
            return t
        h_label_dyn = always_redraw(_get_height_label)

        def _get_slope_label():
            x = x_track.get_value()
            s = np.exp(x)
            t = Text(f"slope  = {s:.1f}", font_size=14, color=GREEN, weight=BOLD)
            t.move_to([0, -2.6, 0])
            return t
        s_label_dyn = always_redraw(_get_slope_label)

        self.add(dot_dyn, tang_dyn, hline_dyn, h_label_dyn, s_label_dyn)

        # Slide from x=0.3 to x=2.2
        self.play(
            x_track.animate.set_value(2.2),
            run_time=TTS["proof_watch"] - 1.0,
            rate_func=smooth
        )

        # Green flash at the end
        self.play(
            Flash(dot_dyn, color=GREEN, line_length=0.3, num_lines=10, run_time=0.3),
            run_time=0.3
        )

        # 2s silence beat
        self.wait(2.0)

        # Clear for contrast
        self.play(FadeOut(VGroup(proof_title, label_e2, ax_e, curve_e,
                                  dot_dyn, tang_dyn, hline_dyn,
                                  h_label_dyn, s_label_dyn)), run_time=0.3)

        # ═══════════════════════════════════════════════
        # SCENE 5: CONTRAST — 2ˣ (6.8s)
        # ═══════════════════════════════════════════════
        c2_title = MathTex(r"2^x", font_size=28, color=ORANGE)
        c2_title.move_to([0, 3.5, 0])

        ax_2 = _make_axes([0, 3.5, 1], [0, 10, 2], 3.2, 3.5, [0, 0.3, 0])
        curve_2 = ax_2.plot(lambda x: 2 ** x, x_range=[0, 3.3],
                            color=ORANGE, stroke_width=2.5)

        self.play(FadeIn(c2_title), Create(ax_2, run_time=0.3), Create(curve_2, run_time=0.4))

        # Show at x = 2: height = 4.0, slope = 2.8
        x_2 = 2.0
        y_2 = 2 ** x_2  # 4.0
        s_2 = (2 ** x_2) * np.log(2)  # ≈ 2.77

        dot_2 = Dot(ax_2.c2p(x_2, y_2), color=ORANGE, radius=0.06)
        dx_2 = 0.5
        tang_2 = Line(
            ax_2.c2p(x_2 - dx_2, y_2 - s_2 * dx_2),
            ax_2.c2p(x_2 + dx_2, y_2 + s_2 * dx_2),
            color=ORANGE, stroke_width=2.5
        )
        h_line_2 = DashedLine(ax_2.c2p(x_2, 0), ax_2.c2p(x_2, y_2),
                               color=ORANGE, stroke_width=1.2, dash_length=0.06)

        h_2_label = Text(f"height = {y_2:.1f}", font_size=14, color=ORANGE, weight=BOLD)
        h_2_label.move_to([0, -2.0, 0])
        s_2_label = Text(f"slope  = {s_2:.1f}", font_size=14, color=ORANGE, weight=BOLD)
        s_2_label.move_to([0, -2.6, 0])

        self.play(FadeIn(dot_2), Create(tang_2), Create(h_line_2), run_time=0.3)
        self.play(FadeIn(h_2_label), FadeIn(s_2_label), run_time=0.3)

        # Red X
        no_match = MathTex(r"\neq", font_size=36, color="#FF4444")
        no_match.move_to([0, -3.2, 0])
        self.play(FadeIn(no_match, scale=1.5), run_time=0.3)

        fill_time = max(0, TTS["contrast_2x"] - 2.0)
        self.wait(fill_time)

        self.play(FadeOut(VGroup(c2_title, ax_2, curve_2, dot_2, tang_2,
                                  h_line_2, h_2_label, s_2_label, no_match)), run_time=0.3)

        # ═══════════════════════════════════════════════
        # SCENE 6: CONTRAST — 3ˣ (5.2s)
        # ═══════════════════════════════════════════════
        c3_title = MathTex(r"3^x", font_size=28, color=CYAN)
        c3_title.move_to([0, 3.5, 0])

        ax_3 = _make_axes([0, 3.5, 1], [0, 10, 2], 3.2, 3.5, [0, 0.3, 0])
        curve_3 = ax_3.plot(lambda x: 3 ** x, x_range=[0, 2.1],
                            color=CYAN, stroke_width=2.5)

        self.play(FadeIn(c3_title), Create(ax_3, run_time=0.3), Create(curve_3, run_time=0.4))

        # Show at x = 1.5: height ≈ 5.2, slope ≈ 5.7
        x_3 = 1.5
        y_3 = 3 ** x_3
        s_3 = (3 ** x_3) * np.log(3)

        dot_3 = Dot(ax_3.c2p(x_3, y_3), color=CYAN, radius=0.06)
        dx_3 = 0.4
        tang_3 = Line(
            ax_3.c2p(x_3 - dx_3, y_3 - s_3 * dx_3),
            ax_3.c2p(x_3 + dx_3, y_3 + s_3 * dx_3),
            color=CYAN, stroke_width=2.5
        )
        h_line_3 = DashedLine(ax_3.c2p(x_3, 0), ax_3.c2p(x_3, y_3),
                               color=CYAN, stroke_width=1.2, dash_length=0.06)

        h_3_label = Text(f"height = {y_3:.1f}", font_size=14, color=CYAN, weight=BOLD)
        h_3_label.move_to([0, -2.0, 0])
        s_3_label = Text(f"slope  = {s_3:.1f}", font_size=14, color=CYAN, weight=BOLD)
        s_3_label.move_to([0, -2.6, 0])

        self.play(FadeIn(dot_3), Create(tang_3), Create(h_line_3), run_time=0.3)
        self.play(FadeIn(h_3_label), FadeIn(s_3_label), run_time=0.3)

        no_match_3 = MathTex(r"\neq", font_size=36, color="#FF4444")
        no_match_3.move_to([0, -3.2, 0])
        self.play(FadeIn(no_match_3, scale=1.5), run_time=0.3)

        fill_time = max(0, TTS["contrast_3x"] - 1.8)
        self.wait(fill_time)

        self.play(FadeOut(VGroup(c3_title, ax_3, curve_3, dot_3, tang_3,
                                  h_line_3, h_3_label, s_3_label, no_match_3)), run_time=0.3)

        # ═══════════════════════════════════════════════
        # SCENE 7: THE ANSWER — e is the base (9.8s + 2s silence)
        # ═══════════════════════════════════════════════
        ans_title = Text("Only one base works", font_size=20, color=GREEN, weight=BOLD)
        ans_title.move_to([0, 3.5, 0])
        self.play(FadeIn(ans_title), run_time=0.2)

        # Number line: 2 — e — 3
        nl = NumberLine(x_range=[1.5, 3.5, 0.5], length=3.5,
                        color=WHITE, stroke_width=1.5,
                        include_numbers=False, include_tip=False)
        nl.move_to([0, 2.5, 0])

        n2 = MathTex("2", font_size=18, color=ORANGE).next_to(nl.n2p(2), DOWN, buff=0.12)
        n3 = MathTex("3", font_size=18, color=CYAN).next_to(nl.n2p(3), DOWN, buff=0.12)
        ne = MathTex(r"e \approx 2.718", font_size=16, color=GREEN)
        ne.next_to(nl.n2p(2.718), UP, buff=0.12)

        e_dot = Dot(nl.n2p(2.718), color=GREEN, radius=0.08).set_glow_factor(0.8)

        self.play(Create(nl), FadeIn(n2), FadeIn(n3), run_time=0.4)
        self.play(FadeIn(e_dot, scale=0.5), FadeIn(ne), run_time=0.4)
        self.play(Flash(e_dot, color=GREEN, line_length=0.2, num_lines=8, run_time=0.3))

        # eˣ graph with sliding dot again
        ax_final = _make_axes([0, 3.5, 1], [0, 10, 2], 3.2, 2.8, [0, -0.8, 0])
        curve_final = ax_final.plot(lambda x: np.exp(x), x_range=[0, 2.3],
                                     color=GREEN, stroke_width=2.5)
        label_final = MathTex(r"e^x", font_size=20, color=GREEN)
        label_final.move_to([1.3, 0.8, 0])

        self.play(Create(ax_final, run_time=0.3), Create(curve_final, run_time=0.4))
        self.play(FadeIn(label_final), run_time=0.2)

        # Quick slide with matching labels
        x_t2 = ValueTracker(0.5)

        dot_f = always_redraw(
            lambda: Dot(
                ax_final.c2p(x_t2.get_value(), np.exp(x_t2.get_value())),
                color=GREEN, radius=0.06
            ).set_glow_factor(0.6)
        )
        def _get_tang_f():
            x = x_t2.get_value()
            y = np.exp(x)
            d = 0.4
            return Line(
                ax_final.c2p(x - d, y - y * d),
                ax_final.c2p(x + d, y + y * d),
                color=GREEN, stroke_width=2
            )
        tang_f = always_redraw(_get_tang_f)

        def _get_match_label():
            x = x_t2.get_value()
            y = np.exp(x)
            t = Text(f"height = slope = {y:.1f}", font_size=13, color=GREEN, weight=BOLD)
            t.move_to([0, -2.8, 0])
            return t
        match_lbl = always_redraw(_get_match_label)

        self.add(dot_f, tang_f, match_lbl)
        self.play(x_t2.animate.set_value(2.0), run_time=3.0, rate_func=smooth)

        # 2s silence
        self.wait(2.0)

        self.play(FadeOut(VGroup(ans_title, nl, n2, n3, ne, e_dot,
                                  ax_final, curve_final, label_final,
                                  dot_f, tang_f, match_lbl)), run_time=0.3)

        # ═══════════════════════════════════════════════
        # SCENE 8: PUNCHLINE (12.2s + 2.5s silence)
        # ═══════════════════════════════════════════════
        punch_eq = MathTex(r"\frac{d}{dx}\left[e^x\right] = e^x",
                           font_size=42, color=GREEN)
        punch_eq.move_to([0, 1.0, 0])
        punch_box = _make_box(punch_eq, GREEN, BOX_FILL, 0.6)

        punch_text = Text("The slope was always the height.",
                          font_size=16, color=WHITE, weight=BOLD)
        punch_text.set_opacity(0.8)
        punch_text.move_to([0, -0.5, 0])

        reason = Text("That's why the function doesn't change.",
                      font_size=14, color=CYAN)
        reason.set_opacity(0.6)
        reason.move_to([0, -1.2, 0])

        self.play(FadeIn(punch_box), Write(punch_eq), run_time=0.6)
        self.wait(1.0)
        self.play(FadeIn(punch_text), run_time=0.4)
        self.play(FadeIn(reason), run_time=0.3)

        self.play(
            Circumscribe(punch_box, color=GREEN, run_time=0.6),
        )

        # 2.5s silence
        self.wait(max(0, TTS["punchline"] - 3.5))
        self.wait(2.5)

        self.play(FadeOut(VGroup(punch_eq, punch_box, punch_text, reason)), run_time=0.4)

        # ═══════════════════════════════════════════════
        # SCENE 9: END CARD (3s)
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

        self.play(Create(liss_core, run_time=0.8), FadeIn(liss_glow, run_time=0.6))
        self.play(FadeIn(wordmark, shift=UP * 0.1), run_time=0.3)
        self.play(FadeIn(tagline), run_time=0.2)
        self.wait(1.5)
        self.play(FadeOut(VGroup(logo, wordmark, tagline)), run_time=0.3)
