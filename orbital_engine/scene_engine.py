"""
Orbital Engine — Universal Scene (V5 — Bible-Compliant)
=========================================================
Uses visuals/standards.py for ALL text, boxing, glow, and graph primitives.
Every element follows the Production Bible. No exceptions.
"""
import json
import os
import sys
import numpy as np
from pathlib import Path
from manim import *

ENGINE_DIR = os.environ.get("ORBITAL_ENGINE_DIR", str(Path(__file__).parent))
sys.path.insert(0, ENGINE_DIR)

from config import LAYOUTS, EXTRA_HOLD, BRANDING
from tts.timestamper import find_trigger, find_word
from visuals.standards import (
    ORBITAL_CYAN, END_CYAN, NEON_GREEN, GOLD, CRIMSON, VIOLET,
    BOX_FILL, BOX_STROKE, AXIOM_TEXT,
    # Text tiers
    tier1_punchline, tier2_key_fact, tier3_callout, tier4_title,
    tier5_equation, tier6_caption, auto_box,
    # Alive standard
    make_glow, bloom, sparks, alive_hold,
    # Graph standard
    orbital_axes, neon_grid, trace_curve, orbital_graph,
    # Components
    definition_box, function_machine, animate_machine_example, spin_gears,
    mapping_arrow_trace, set_to_mapping_diagram,
    verdict_badge, show_verdict,
    # Environment cards
    env_card, animate_env_card, ENV_COLORS,
    env_definition, env_theorem, env_example, env_warning, env_tip, env_summary, env_property,
    # Chapter cards
    chapter_card, animate_chapter_card, CHAPTER_COLORS,
)


def load_manifest():
    path = os.environ.get("LESSON_MANIFEST",
        str(Path(ENGINE_DIR) / "scripts" / "test.json"))
    with open(path) as f:
        return json.load(f)


class EngineScene(Scene):
    def construct(self):
        self.camera.background_color = "#000000"
        self.manifest = load_manifest()

        vtype = self.manifest.get("video_type", "lesson")
        ln = "short" if vtype == "short" else "landscape"
        self.L = LAYOUTS[ln]

        config.frame_width = self.L["frame_w"]
        config.frame_height = self.L["frame_h"]
        FW, FH = self.L["frame_w"], self.L["frame_h"]

        # Spatial zones
        self.SX = self.L["safe_x"]
        self.HY = self.L["header_y"]
        self.CT = self.L["content_top"]
        self.CB = self.L["content_bottom"]
        self.CY = self.L["content_center_y"]
        self.FY = self.L["footer_y"]
        self.GW = self.L["graph_width"]
        self.GH = self.L["graph_height"]
        self.GC = self.L["graph_center"]
        self.SL = self.L["split_left_x"]
        self.SR = self.L["split_right_x"]
        self.SW = self.L["split_width"]

        self._build_chrome(FW, FH)

        self.previous = None
        steps = self.manifest.get("steps", [])
        for i, step in enumerate(steps):
            is_last = (i == len(steps) - 1)
            handler = getattr(self, f"_do_{step['visual_type']}", None)
            if handler:
                handler(step, is_last)
            else:
                self._do_generic(step, is_last)

    # ── Chrome ──

    def _build_chrome(self, FW, FH):
        from config import GRID_COLOR
        grid = VGroup()
        for x in np.arange(-FW/2, FW/2+0.1, 1.0):
            grid.add(Line([x,-FH/2,0],[x,FH/2,0],
                color=GRID_COLOR, stroke_width=0.4, stroke_opacity=0.15))
        for y in np.arange(-FH/2, FH/2+0.1, 1.0):
            grid.add(Line([-FW/2,y,0],[FW/2,y,0],
                color=GRID_COLOR, stroke_width=0.4, stroke_opacity=0.15))

        border = Rectangle(width=FW-0.2, height=FH-0.2,
            color=VIOLET, stroke_width=2, stroke_opacity=0.5, fill_opacity=0)
        glow = Rectangle(width=FW-0.15, height=FH-0.15,
            color=VIOLET, stroke_width=5, stroke_opacity=0.1, fill_opacity=0)

        A, B = 0.4, 0.3
        wm_curve = ParametricFunction(
            lambda t: np.array([A*np.sin(2*t), B*np.sin(3*t), 0]),
            t_range=[0,TAU,0.01], color=END_CYAN,
            stroke_width=1.5, stroke_opacity=0.25)
        wm_text = Text("ORBITAL", font_size=self.L["wm_font_size"],
            color=END_CYAN, weight=BOLD)
        wm_text.set_opacity(0.25)
        wm_text.next_to(wm_curve, RIGHT, buff=0.1)
        wm = VGroup(wm_curve, wm_text).move_to([FW/2-1.2, -FH/2+0.4, 0])

        self.add(VGroup(grid, glow, border, wm))

        sec = self.manifest.get("section", "")
        bb = RoundedRectangle(width=1.2, height=0.4, corner_radius=0.08,
            fill_color=VIOLET, fill_opacity=0.7, stroke_width=0)
        bl = Text(f"§{sec}", font_size=12, color=WHITE, weight=BOLD)
        self.sec_badge = VGroup(bb, bl).move_to([-FW/2+1.0, FH/2-0.4, 0])
        self.add(self.sec_badge)

    # ── Helpers ──

    def _start(self, step):
        ap = step.get("audio_path", "")
        dur = max(1.0, step.get("duration_ms", 3000) / 1000.0)
        words = step.get("word_timestamps", [])
        if self.previous is not None:
            self.play(FadeOut(self.previous, shift=UP*0.3), run_time=0.4)
            self.previous = None
        if ap and Path(ap).exists():
            self.add_sound(ap)
        return words, dur, 0.0

    def _end(self, mob, dur, t, is_last, glow=None):
        rem = max(0.2, dur - t)
        if rem > 2.0 and glow is not None:
            alive_hold(self, mob, glow, rem, style="glow_pulse")
        elif rem > 1.5 and mob is not None:
            alive_hold(self, mob, None, rem, style="drift")
        else:
            self.wait(rem)
        if not is_last:
            self.wait(EXTRA_HOLD)
        if glow:
            self.previous = VGroup(mob, glow) if mob else glow
        elif mob:
            self.previous = mob

    def _sync(self, target, current):
        gap = target - current
        if gap > 0.05:
            self.wait(gap)
            return target
        return current

    # ═══════════════════════════════════════════════════════
    # TITLE CARD
    # ═══════════════════════════════════════════════════════

    def _do_title_card(self, step, is_last):
        w, dur, t = self._start(step)
        d = step.get("visual_data", {})

        sec = tier4_title(f"SECTION {d.get('section', '')}")
        ttl = Text(d.get("title", ""), font_size=48, color=ORBITAL_CYAN, weight=BOLD)
        if ttl.width > self.SX*2 - 1:
            ttl.scale((self.SX*2 - 1) / ttl.width)
        ttl.next_to(sec, DOWN, buff=0.3)

        lw = min(3.0, self.SX - ttl.width/2 - 0.5)
        ll = Line(ORIGIN, LEFT*lw, color=ORBITAL_CYAN, stroke_width=2)
        lr = Line(ORIGIN, RIGHT*lw, color=ORBITAL_CYAN, stroke_width=2)
        ll.next_to(ttl, LEFT, buff=0.3)
        lr.next_to(ttl, RIGHT, buff=0.3)

        badge_bg = RoundedRectangle(width=3.5, height=0.65, corner_radius=0.1,
            fill_color=VIOLET, fill_opacity=0.85, stroke_width=0)
        badge_text = Text(d.get("video_label", ""), font_size=20, color=WHITE, weight=BOLD)
        badge = VGroup(badge_bg, badge_text).next_to(ttl, DOWN, buff=0.5)

        brand = Text(BRANDING["school"], font_size=12, color="#444444", weight=BOLD)
        brand.next_to(badge, DOWN, buff=0.5)

        grp = VGroup(sec, ttl, ll, lr, badge, brand).move_to([0, self.CY, 0])
        tg = make_glow(ttl, ORBITAL_CYAN, 8, 0.15)

        self.add(tg)
        self.play(FadeIn(sec, shift=UP*0.3), run_time=0.4); t += 0.4
        self.play(FadeIn(ttl, shift=UP*0.2, scale=0.9),
            Create(ll), Create(lr), run_time=0.5); t += 0.5
        bloom(self, ttl, ORBITAL_CYAN, radius=0.6); t += 0.2
        self.play(FadeIn(badge, shift=UP*0.2), FadeIn(brand), run_time=0.3); t += 0.3
        self._end(grp, dur, t, is_last, glow=tg)

    # ═══════════════════════════════════════════════════════
    # OBJECTIVES
    # ═══════════════════════════════════════════════════════

    def _do_objectives_list(self, step, is_last):
        w, dur, t = self._start(step)
        d = step.get("visual_data", {})
        objs = d.get("objectives", [])

        header = tier4_title("Learning Objectives")
        header.move_to([0, self.CT - 0.3, 0])
        div = Line(LEFT*4, RIGHT*4, color=VIOLET, stroke_width=1.5, stroke_opacity=0.5)
        div.next_to(header, DOWN, buff=0.15)
        self.play(FadeIn(header, shift=DOWN*0.2), Create(div), run_time=0.4); t += 0.4

        cues = ["understand", "identify", "evaluate", "determine", "work"]
        rows = VGroup()
        for i, txt in enumerate(objs):
            dot = Dot(color=ORBITAL_CYAN, radius=0.06).set_glow_factor(1.5)
            display = txt if len(txt) <= 55 else txt[:52] + "..."
            label = Text(display, font_size=18, color=WHITE)
            row = VGroup(dot, label).arrange(RIGHT, buff=0.15)
            row.move_to([0, self.CT - 1.2 - i*0.65, 0])
            row.align_to(LEFT*(self.SX - 0.5), LEFT)

            if i < len(cues) and w:
                ct = find_word(w, cues[i], after=t-0.5)
                if ct > 0: t = self._sync(ct - 0.2, t)

            self.play(FadeIn(dot, scale=2), FadeIn(label, shift=RIGHT*0.3),
                run_time=0.3); t += 0.3
            rows.add(row)

        self._end(VGroup(header, div, rows), dur, t, is_last)

    # ═══════════════════════════════════════════════════════
    # FUNCTION MACHINE (uses standards.py components)
    # ═══════════════════════════════════════════════════════

    def _do_function_machine(self, step, is_last):
        w, dur, t = self._start(step)
        d = step.get("visual_data", {})
        fn = d.get("func_name", "f")
        rule = d.get("rule_display", "x^2 + 1")
        examples = d.get("examples", [[3, 10], [-2, 5], [0, 1]])

        # Build machine from standards (now with gears!)
        grp, glow, machine, in_arr, out_arr, gear1, gear2 = function_machine(fn, rule, self.SX)
        grp.move_to([0, self.CY + 1.0, 0])
        glow.move_to(machine.get_center())

        # Sync to "machine" in audio
        tm = find_word(w, "machine", after=0) if w else 0
        if tm > 0: t = self._sync(tm - 0.6, t)

        self.add(glow)
        self.play(FadeIn(grp, shift=UP*0.2), run_time=0.5); t += 0.5
        bloom(self, machine, VIOLET, radius=0.6); t += 0.2

        # Example triggers
        triggers = [
            (["put", "in", "three"],    ["comes", "10"]),
            (["put", "in", "negative"], ["comes", "five"]),
            (["zero", "goes"],          ["one", "comes"]),
        ]

        notations = VGroup()
        for idx, (inp, outp) in enumerate(examples):
            in_trig = triggers[idx][0] if idx < len(triggers) else None
            out_trig = triggers[idx][1] if idx < len(triggers) else None

            if in_trig and w:
                cue = find_trigger(w, in_trig, after=t-1)
                if cue > 0: t = self._sync(cue - 0.3, t)

            notation, elapsed = animate_machine_example(
                self, machine, in_arr, out_arr, inp, outp, fn, t,
                gear1=gear1, gear2=gear2)
            t += elapsed
            notation.move_to([0, self.CB + 1.5 - idx*0.6, 0])
            notations.add(notation)

            # Sync to output cue for next wait
            if out_trig and w:
                cue = find_trigger(w, out_trig, after=t-1)
                if cue > 0: t = self._sync(cue + 0.5, t)

        self._end(VGroup(grp, notations), dur, t, is_last, glow=glow)

    # ═══════════════════════════════════════════════════════
    # DEFINITION BOX (split: text left, visual right)
    # ═══════════════════════════════════════════════════════

    def _do_definition_box(self, step, is_last):
        w, dur, t = self._start(step)
        d = step.get("visual_data", {})
        term = d.get("term", "")

        # LEFT: Definition box from standards
        left_grp, left_glow = definition_box(
            term=term,
            equation_tex=r"f : A \to B",
            key_phrase_parts=[
                ("each input", ORBITAL_CYAN),
                (r"\to", WHITE),
                ("exactly one output", GOLD),
            ],
            width=self.SW, height=4.0,
        )
        left_grp.move_to([self.SL, self.CY, 0])
        left_glow.move_to(left_grp.get_center())

        # RIGHT: Mini mapping diagram
        ow, oh = 2.0, 3.0
        d_ov = Ellipse(width=ow, height=oh, color=ORBITAL_CYAN,
            fill_color=ORBITAL_CYAN, fill_opacity=0.05, stroke_width=1.5).move_to(LEFT*1.5)
        r_ov = Ellipse(width=ow, height=oh, color=VIOLET,
            fill_color=VIOLET, fill_opacity=0.05, stroke_width=1.5).move_to(RIGHT*1.5)
        dt = tier6_caption(r"A"); dt.next_to(d_ov, UP, buff=0.12)
        rt = MathTex("B", font_size=24, color=VIOLET); rt.next_to(r_ov, UP, buff=0.12)

        dd, dl, rd, rl = VGroup(), VGroup(), VGroup(), VGroup()
        rp = {}
        for i, n in enumerate(["a","b","c"]):
            y = 0.7 - i*0.7
            p = LEFT*1.5 + UP*y
            dd.add(Dot(p, color=ORBITAL_CYAN, radius=0.06).set_glow_factor(1.5))
            lbl = Text(n, font_size=13, color=WHITE); lbl.next_to(dd[-1], LEFT, buff=0.1)
            dl.add(lbl)
        for i, n in enumerate(["1","2"]):
            y = 0.35 - i*0.7
            p = RIGHT*1.5 + UP*y
            rd.add(Dot(p, color=VIOLET, radius=0.06).set_glow_factor(1.5))
            lbl = Text(n, font_size=13, color=WHITE); lbl.next_to(rd[-1], RIGHT, buff=0.1)
            rl.add(lbl); rp[n] = p

        arrows = VGroup()
        for i, (inp, outp) in enumerate([("a","1"),("b","2"),("c","2")]):
            arr = Arrow(dd[i].get_center(), rp[outp], buff=0.1,
                color=ORBITAL_CYAN, stroke_width=1.5,
                max_tip_length_to_length_ratio=0.08, tip_length=0.12)
            arrows.add(arr)

        right_grp = VGroup(d_ov, r_ov, dt, rt, dd, dl, rd, rl, arrows)
        right_grp.move_to([self.SR, self.CY, 0])

        # ── SYNC ──
        tf = find_word(w, "formal", after=0) if w else 0
        if tf > 0: t = self._sync(tf - 0.3, t)

        # Box appears
        self.add(left_glow)
        box, top_bar, label, term_m, eq, key = left_grp[0], left_grp[1], left_grp[2], left_grp[3], left_grp[4], left_grp[5]
        self.play(FadeIn(box), Create(top_bar), FadeIn(label), run_time=0.4); t += 0.4

        # "function" → term with bloom
        tfn = find_word(w, "function", after=t-0.5) if w else t
        if tfn > 0: t = self._sync(tfn - 0.2, t)
        self.play(FadeIn(term_m, shift=UP*0.2, scale=0.9), run_time=0.3); t += 0.3
        bloom(self, term_m, ORBITAL_CYAN, radius=0.5); t += 0.2

        # "set A" → equation
        ts = find_word(w, "set", after=t-0.5) if w else t
        if ts > 0: t = self._sync(ts - 0.2, t)
        self.play(FadeIn(eq, shift=UP*0.1), run_time=0.3); t += 0.3

        # "assigns" → key phrase
        ta = find_word(w, "assigns", after=t-0.5) if w else t
        if ta > 0: t = self._sync(ta - 0.2, t)
        self.play(FadeIn(key, shift=UP*0.1), run_time=0.3); t += 0.3

        # "domain" → right panel builds
        td = find_word(w, "domain", after=t-0.5) if w else t
        if td > 0: t = self._sync(td - 0.3, t)
        self.play(Create(d_ov), Create(r_ov), FadeIn(dt), FadeIn(rt), run_time=0.4); t += 0.4
        self.play(
            *[FadeIn(d, scale=2) for d in dd], *[FadeIn(l) for l in dl],
            *[FadeIn(d, scale=2) for d in rd], *[FadeIn(l) for l in rl],
            run_time=0.35); t += 0.35

        for arr in arrows:
            mapping_arrow_trace(self, arr, run_time=0.25); t += 0.25

        # "exactly one" → bloom on key phrase
        te = find_word(w, "exactly", after=15.0) if w else -1
        if te > 0: t = self._sync(te - 0.2, t)
        bloom(self, key, GOLD, radius=0.5); t += 0.2

        self._end(VGroup(left_grp, right_grp), dur, t, is_last, glow=left_glow)

    # ═══════════════════════════════════════════════════════
    # MAPPING DIAGRAM
    # ═══════════════════════════════════════════════════════

    def _do_mapping_diagram(self, step, is_last):
        w, dur, t = self._start(step)
        d = step.get("visual_data", {})
        mappings = d.get("mappings", [])
        is_fn = d.get("is_function", True)
        title = d.get("title", "")

        title_mob = None
        if title:
            title_mob = tier4_title(title)
            title_mob.move_to([0, self.HY, 0])

        ow, oh, gap = 3.0, 4.2, 3.5
        d_ov = Ellipse(width=ow, height=oh, color=ORBITAL_CYAN,
            fill_color=ORBITAL_CYAN, fill_opacity=0.05, stroke_width=1.5).move_to(LEFT*gap)
        r_ov = Ellipse(width=ow, height=oh, color=VIOLET,
            fill_color=VIOLET, fill_opacity=0.05, stroke_width=1.5).move_to(RIGHT*gap)
        d_lbl = tier6_caption(d.get("domain_label", "A")); d_lbl.next_to(d_ov, UP, buff=0.15)
        r_lbl = MathTex(d.get("range_label", "B"), font_size=24, color=VIOLET)
        r_lbl.next_to(r_ov, UP, buff=0.15)

        all_rv = []
        for _, outs in mappings:
            for o in outs:
                if o not in all_rv: all_rv.append(o)

        uh = oh - 1.0
        dd, dl = VGroup(), VGroup()
        nd = len(mappings)
        for i, (inp, _) in enumerate(mappings):
            y = uh/2 - i*(uh/max(1,nd-1)) if nd > 1 else 0
            p = LEFT*gap + UP*y
            dd.add(Dot(p, color=ORBITAL_CYAN, radius=0.07).set_glow_factor(1.5))
            lbl = Text(str(inp), font_size=14, color=WHITE); lbl.next_to(dd[-1], LEFT, buff=0.12)
            dl.add(lbl)

        rd, rl, rpos = VGroup(), VGroup(), {}
        nr = len(all_rv)
        for i, val in enumerate(all_rv):
            y = uh/2 - i*(uh/max(1,nr-1)) if nr > 1 else 0
            p = RIGHT*gap + UP*y
            rd.add(Dot(p, color=VIOLET, radius=0.07).set_glow_factor(1.5))
            lbl = Text(str(val), font_size=14, color=WHITE); lbl.next_to(rd[-1], RIGHT, buff=0.12)
            rl.add(lbl); rpos[val] = p

        arrows = VGroup()
        for i, (inp, outs) in enumerate(mappings):
            start = dd[i].get_center()
            for ov in outs:
                if ov in rpos:
                    color = ORBITAL_CYAN if len(outs) == 1 else "#FF4444"
                    arrows.add(Arrow(start, rpos[ov], buff=0.12,
                        color=color, stroke_width=1.8,
                        max_tip_length_to_length_ratio=0.08, tip_length=0.12))

        verdict = verdict_badge(is_fn)
        verdict.move_to([0, self.FY, 0])

        parts = [d_ov, r_ov, d_lbl, r_lbl, dd, dl, rd, rl, arrows, verdict]
        if title_mob: parts.append(title_mob)
        grp = VGroup(*parts).move_to([0, self.CY, 0])

        # ── SYNC ──
        if title_mob:
            self.play(FadeIn(title_mob), run_time=0.2); t += 0.2

        tc = find_word(w, "mapping", after=0) if w else -1
        if tc <= 0 and w: tc = find_word(w, "test", after=0)
        if tc <= 0 and w: tc = find_word(w, "consider", after=0)
        if tc <= 0 and w: tc = find_word(w, "each", after=0)
        if tc > 0: t = self._sync(tc - 0.2, t)

        self.play(Create(d_ov), Create(r_ov), FadeIn(d_lbl), FadeIn(r_lbl),
            run_time=0.4); t += 0.4
        self.play(
            *[FadeIn(d, scale=2) for d in dd], *[FadeIn(l) for l in dl],
            run_time=0.35); t += 0.35
        self.play(
            *[FadeIn(d, scale=2) for d in rd], *[FadeIn(l) for l in rl],
            run_time=0.35); t += 0.35

        for arr in arrows:
            mapping_arrow_trace(self, arr, run_time=0.3); t += 0.3

        tv = find_word(w, "function", after=dur*0.6) if w else -1
        if tv <= 0 and w: tv = find_word(w, "fine", after=dur*0.5)
        if tv > 0: t = self._sync(tv - 0.2, t)
        t = show_verdict(self, verdict, t)

        self._end(grp, dur, t, is_last)

    def _do_example_mapping(self, step, is_last):
        self._do_mapping_diagram(step, is_last)

    # ═══════════════════════════════════════════════════════
    # VERTICAL LINE TEST
    # ═══════════════════════════════════════════════════════

    def _do_vertical_line_test(self, step, is_last):
        w, dur, t = self._start(step)
        d = step.get("visual_data", {})
        xr = d.get("x_range", [-1, 6, 1])
        yr = d.get("y_range", [-3, 3, 1])
        passes = d.get("passes", False)

        # Equation at header — tier 2 (key fact, boxed)
        eq_lbl = tier2_key_fact("y^2 = x")
        eq_lbl.move_to([0, self.HY, 0])

        # Graph — Bible standard
        ax = orbital_axes(xr, yr, self.GW, self.GH, [self.GC[0], self.GC[1], 0])
        gc = ax.get_center()
        ngrid = neon_grid([gc[0], gc[1]], self.GW/2, self.GH/2)

        # Both branches
        top_b = ax.plot(lambda x: x**0.5, x_range=[0.01, xr[1]-0.2],
            color=ORBITAL_CYAN, stroke_width=3)
        bot_b = ax.plot(lambda x: -(x**0.5), x_range=[0.01, xr[1]-0.2],
            color=ORBITAL_CYAN, stroke_width=3)

        # SYNC: "graph"
        tg = find_word(w, "graph", after=0) if w else 0
        if tg > 0: t = self._sync(tg - 0.3, t)

        self.play(FadeIn(eq_lbl), run_time=0.25); t += 0.25
        bloom(self, eq_lbl, ORBITAL_CYAN, radius=0.4); t += 0.2
        self.play(FadeIn(ngrid), FadeIn(ax), run_time=0.3); t += 0.3

        # "curve" → trace both branches
        tc = find_word(w, "curve", after=t-0.5) if w else t
        if tc > 0: t = self._sync(tc - 0.2, t)

        tracer_t = trace_curve(self, top_b, run_time=0.5); t += 0.74
        tracer_b = trace_curve(self, bot_b, run_time=0.5); t += 0.74

        # "sideways" → hold
        ts = find_word(w, "sideways", after=t-0.5) if w else -1
        if ts > 0: t = self._sync(ts + 1.0, t)

        # "sweep" → vertical line
        tsw = find_word(w, "sweep", after=t-0.5) if w else t
        if tsw > 0: t = self._sync(tsw - 0.2, t)

        xtrack = ValueTracker(0.3)
        vline = always_redraw(lambda: DashedLine(
            ax.c2p(xtrack.get_value(), yr[0]),
            ax.c2p(xtrack.get_value(), yr[1]),
            color=YELLOW, stroke_width=2, dash_length=0.1))
        tdot = always_redraw(lambda: Dot(
            ax.c2p(xtrack.get_value(),
                xtrack.get_value()**0.5 if xtrack.get_value() > 0 else 0),
            color=YELLOW, radius=0.08).set_glow_factor(2.0))
        bdot = always_redraw(lambda: Dot(
            ax.c2p(xtrack.get_value(),
                -(xtrack.get_value()**0.5) if xtrack.get_value() > 0 else 0),
            color=YELLOW, radius=0.08).set_glow_factor(2.0))
        self.add(vline, tdot, bdot)

        sweep_dur = 3.0
        th = find_word(w, "hits", after=t-0.5) if w else -1
        if th > 0: sweep_dur = max(2.0, (th - t) + 1.0)

        self.play(xtrack.animate.set_value(xr[1]-0.5),
            run_time=sweep_dur, rate_func=linear); t += sweep_dur

        # Freeze at clear intersection
        self.remove(vline, tdot, bdot)
        sx = 4.0
        fl = DashedLine(ax.c2p(sx, yr[0]), ax.c2p(sx, yr[1]),
            color=YELLOW, stroke_width=2, dash_length=0.1)
        ft = Dot(ax.c2p(sx, sx**0.5), color=YELLOW, radius=0.1).set_glow_factor(2.0)
        fb = Dot(ax.c2p(sx, -(sx**0.5)), color=YELLOW, radius=0.1).set_glow_factor(2.0)
        self.add(fl)
        self.play(FadeIn(ft, scale=2), FadeIn(fb, scale=2), run_time=0.3); t += 0.3

        # Labels — tier 6
        tl = tier6_caption(f"y = {sx**0.5:.1f}"); tl.next_to(ft, RIGHT, buff=0.12)
        bl_m = tier6_caption(f"y = -{sx**0.5:.1f}"); bl_m.next_to(fb, RIGHT, buff=0.12)
        self.play(FadeIn(tl), FadeIn(bl_m), run_time=0.2); t += 0.2

        # "fails" → verdict
        tf = find_word(w, "fails", after=t-1) if w else -1
        if tf > 0: t = self._sync(tf - 0.2, t)

        verdict = verdict_badge(passes,
            positive_text="✓ Passes VLT",
            negative_text="✗ Fails — Two y-values")
        verdict.move_to([0, self.FY, 0])
        t = show_verdict(self, verdict, t)

        tn = find_word(w, "not", after=t-0.5) if w else -1
        if tn > 0: t = self._sync(tn + 1.5, t)

        all_c = VGroup(eq_lbl, ngrid, ax, top_b, bot_b, fl, ft, fb,
            tl, bl_m, tracer_t, tracer_b, verdict)
        self._end(all_c, dur, t, is_last)

    # ═══════════════════════════════════════════════════════
    # ENVIRONMENT CARD (Axiom Reader visual language)
    # ═══════════════════════════════════════════════════════

    def _do_env_card(self, step, is_last):
        """
        Render an Axiom Reader-style environment card.
        
        visual_data:
            env_type: "definition" | "theorem" | "example" | "warning" | "tip" | "summary" | "property"
            title: Card title (e.g., "Function")
            number: Optional number (e.g., "1.1")
            lines: List of {"type": "text"|"math"|"bold", "content": "..."}
            width: Optional width override
            position: Optional [x, y] override
        """
        w, dur, t = self._start(step)
        d = step.get("visual_data", {})
        env_type = d.get("env_type", "definition")
        title = d.get("title", "")
        number = d.get("number", None)
        width = d.get("width", self.SW)
        pos = d.get("position", [0, self.CY])

        lines = [(l["type"], l["content"]) for l in d.get("lines", [])]

        grp, glow, content_mobs = env_card(env_type, title, lines, width, number)
        grp.move_to(pos)
        glow.move_to(grp[0].get_center())

        # Sync to first word cue if available
        cues = d.get("sync_words", [])
        if cues and w:
            cue_t = find_word(w, cues[0], after=0)
            if cue_t > 0:
                t = self._sync(cue_t - 0.3, t)

        t = animate_env_card(self, grp, glow, content_mobs, t)
        self._end(grp, dur, t, is_last, glow=glow)

    # ═══════════════════════════════════════════════════════
    # CHAPTER CARD (A/B/C section transitions)
    # ═══════════════════════════════════════════════════════

    def _do_chapter_card(self, step, is_last):
        """
        Render a chapter transition card for A/B/C sections.
        
        visual_data:
            chapter_type: "concepts" | "skills" | "extensions"
            section: Section number (e.g., "1.1")
            title: Subtitle/hook text
            duration: Optional hold duration override
        """
        w, dur, t = self._start(step)
        d = step.get("visual_data", {})
        chapter_type = d.get("chapter_type", "concepts")
        section = d.get("section", self.manifest.get("section", ""))
        title = d.get("title", "")
        card_dur = d.get("duration", min(dur, 4.0))

        # Clear previous before showing full-screen card
        if self.previous is not None:
            self.play(FadeOut(self.previous, shift=UP * 0.3), run_time=0.4)
            self.previous = None

        grp, glow, liss = chapter_card(section, title, chapter_type)
        t = animate_chapter_card(self, grp, glow, liss, duration=card_dur, t=t)

        # chapter_card handles its own fade out, so no previous to track
        rem = max(0, dur - t)
        if rem > 0.1:
            self.wait(rem)
        if not is_last:
            self.wait(EXTRA_HOLD)

    # ═══════════════════════════════════════════════════════
    # SET NOTATION → MAPPING DIAGRAM
    # ═══════════════════════════════════════════════════════

    def _do_set_to_mapping(self, step, is_last):
        """
        Animate set notation transforming into a mapping diagram.
        
        visual_data:
            domain: List of domain elements (e.g., [1, 2, 3])
            range: List of range elements (e.g., ["a", "b"])
            mappings: List of [domain_idx, range_idx] pairs
            is_function: bool — show verdict after
            title: Optional header text
        """
        w, dur, t = self._start(step)
        d = step.get("visual_data", {})
        domain = d.get("domain", [1, 2, 3])
        range_vals = d.get("range", ["a", "b"])
        raw_mappings = d.get("mappings", [[0, 0], [1, 1], [2, 1]])
        is_fn = d.get("is_function", True)
        title = d.get("title", "")

        mappings = [(m[0], m[1]) for m in raw_mappings]

        if title:
            title_mob = tier4_title(title)
            title_mob.move_to([0, self.HY, 0])
            self.play(FadeIn(title_mob, shift=DOWN * 0.2), run_time=0.3); t += 0.3

        # Sync to "set" or "notation" in audio
        tc = find_word(w, "set", after=0) if w else -1
        if tc <= 0 and w:
            tc = find_word(w, "elements", after=0)
        if tc > 0:
            t = self._sync(tc - 0.3, t)

        diagram, arrows, t = set_to_mapping_diagram(
            self, domain, range_vals, mappings, t,
            center=[0, self.CY - 0.3],
            oval_w=2.5, oval_h=3.5, gap=3.5)

        # Verdict
        tv = find_word(w, "function", after=dur * 0.5) if w else -1
        if tv > 0:
            t = self._sync(tv - 0.2, t)

        verdict = verdict_badge(is_fn)
        verdict.move_to([0, self.FY, 0])
        t = show_verdict(self, verdict, t)

        all_parts = VGroup(diagram, arrows, verdict)
        if title:
            all_parts.add(title_mob)
        self._end(all_parts, dur, t, is_last)

    # ═══════════════════════════════════════════════════════
    # CLOSE CARD
    # ═══════════════════════════════════════════════════════

    def _do_close_card(self, step, is_last):
        w, dur, t = self._start(step)
        d = step.get("visual_data", {})

        sweep = Line(LEFT*5, RIGHT*5, color=ORBITAL_CYAN, stroke_width=3)
        sweep.move_to([0, self.CY+1.2, 0])
        check = Text("✓", font_size=60, color=NEON_GREEN).move_to([0, self.CY+0.2, 0])
        done = tier3_callout(f"Section {d.get('section','')} Complete")
        done.move_to([0, self.CY-0.6, 0])
        nxt_text = Text(f"Next → {d.get('next_action','')}", font_size=20, color=ORBITAL_CYAN)
        nxt_text.move_to([0, self.CY-1.5, 0])
        tag = Text(BRANDING["tagline"], font_size=18, color="#666666")
        tag.move_to([0, self.CY-2.5, 0])

        self.play(Create(sweep), run_time=0.4); t += 0.4
        self.play(FadeIn(check, scale=1.5), run_time=0.3); t += 0.3
        bloom(self, check, NEON_GREEN, radius=0.6); t += 0.2
        self.play(FadeIn(done, shift=UP*0.2), run_time=0.3); t += 0.3
        self.play(FadeIn(nxt_text), run_time=0.3); t += 0.3
        self.play(FadeIn(tag), run_time=0.3); t += 0.3

        self._end(VGroup(sweep, check, done, nxt_text, tag), dur, t, is_last)

    # ═══════════════════════════════════════════════════════
    # OUTRO
    # ═══════════════════════════════════════════════════════

    def _do_outro(self, step, is_last):
        if self.previous:
            self.play(FadeOut(self.previous, shift=UP*0.3), run_time=0.4)
            self.previous = None
        self.remove(self.sec_badge)

        ap = step.get("audio_path", "")
        if ap and Path(ap).exists():
            self.add_sound(ap)

        A, B = 2.0, 1.5
        lg = ParametricFunction(
            lambda t: np.array([A*np.sin(2*t), B*np.sin(3*t), 0]),
            t_range=[0,TAU,0.01], color=END_CYAN, stroke_width=10, stroke_opacity=0.2)
        lc = ParametricFunction(
            lambda t: np.array([A*np.sin(2*t), B*np.sin(3*t), 0]),
            t_range=[0,TAU,0.01], color=END_CYAN, stroke_width=3, stroke_opacity=1.0)
        logo = VGroup(lg, lc).move_to([0, 0.5, 0])

        wm = Text("ORBITAL", font_size=48, color=END_CYAN, weight=BOLD)
        wg = wm.copy().set_opacity(0.3).scale(1.03)
        wm.next_to(logo, DOWN, buff=0.35); wg.move_to(wm.get_center())
        handle = Text(BRANDING["tagline"], font_size=22, color=WHITE)
        handle.set_opacity(0.5); handle.next_to(wm, DOWN, buff=0.3)

        self.play(Create(lc, run_time=1.0), FadeIn(lg, run_time=0.8))
        self.play(FadeIn(VGroup(wg, wm), shift=UP*0.2), run_time=0.4)
        self.play(FadeIn(handle), run_time=0.3)
        self.wait(1.2)
        self.play(lc.animate.set_stroke(opacity=0),
            lg.animate.set_stroke(opacity=0),
            FadeOut(VGroup(wg, wm, handle)), run_time=0.5)
        self.wait(0.3)

    def _do_generic(self, step, is_last):
        w, dur, t = self._start(step)
        self.wait(dur)
        if not is_last: self.wait(EXTRA_HOLD)
