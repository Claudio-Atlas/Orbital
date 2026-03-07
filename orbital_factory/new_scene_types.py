"""
new_scene_types.py — Forge Delivery for Orbital Visual Pipeline
===============================================================
Implements TWO new scene types from Iris's approved Visual Brief:

  1. permutation_display  — N colored blocks on a shelf swap positions to
                            form every arrangement. Each arrangement stamps
                            as a small row on the right. Count label at end.

  2. empty_shelf          — The same shelf, empty. Punchline for "one way to
                            arrange nothing." Glow pulse, then "1", then caption.

─────────────────────────────────────────────────────────────────────────────
HOW TO ADD TO scene_short.py
─────────────────────────────────────────────────────────────────────────────
scene_short.py builds a giant f-string (scene_code = f\'\'\'...\'\'\'). The step
handlers live INSIDE that f-string. This means ALL literal Python braces must
be doubled when pasting:

  { → {{     } → }}

Only the generator substitutions ({_fw}, {_fh}, etc.) stay single-braced.

STEPS:
  1. Copy the STEP TYPE CODE BLOCK into the for-loop in SyncedShortScene.construct(),
     BEFORE the "# ── CONTENT STEP ──" fallthrough comment.
  2. No new helper functions are required — only standard Manim primitives and
     the existing _clamp() function.
  3. Update visual_library.md with the catalog entries at the bottom of this file.

─────────────────────────────────────────────────────────────────────────────
TESTING (standalone — no scene_short.py modification needed)
─────────────────────────────────────────────────────────────────────────────
Run test_new_types_standalone.py:
  cd ~/Desktop/Orbital/orbital_factory
  source venv/bin/activate
  manim test_new_types_standalone.py TestPermutationDisplay -p --quality l
  manim test_new_types_standalone.py TestEmptyShelf -p --quality l

Or run both via:
  python3 run_new_types_test.py
"""

# ═════════════════════════════════════════════════════════════════════════════
# SECTION 1 — STEP TYPE: permutation_display
# ═════════════════════════════════════════════════════════════════════════════
#
# Paste this block into SyncedShortScene.construct() BEFORE the content step
# fallthrough. Comes after the existing step handlers (e.g. "trace_dot").
#
# When inserting into the f-string, double every { and } that is Python syntax:
#   {"key": val}   →  {{"key": val}}
#   [x for x ...]  →  leave as-is (no braces)
#   f"{var}"       →  f"{{var}}"   (but avoid nested f-strings; use format)
# ─────────────────────────────────────────────────────────────────────────────

PERMUTATION_DISPLAY_CODE = '''
# ── PERMUTATION DISPLAY (colored blocks shuffle on a shelf; arrangements stamp to the right) ──
if stype == "permutation_display":
    from itertools import permutations as _iterperms

    duration   = step.get("duration", 14.0)
    audio_path = step.get("audio_path", "")
    perm_cfg   = step.get("permutation_display", {})

    objects      = perm_cfg.get("objects", [
        {"label": "A", "color": "#22D3EE"},
        {"label": "B", "color": "#39FF14"},
        {"label": "C", "color": "#9333EA"},
    ])
    perms_input  = perm_cfg.get("permutations", "all")
    show_count   = perm_cfg.get("show_count", True)
    shelf_vis    = perm_cfg.get("shelf_visible", True)
    speed        = perm_cfg.get("speed", "normal")

    n = len(objects)
    if perms_input == "all":
        perms = list(_iterperms(range(n)))
    else:
        perms = [tuple(p) for p in perms_input]

    speed_map = {"slow": 0.55, "normal": 0.32, "fast": 0.15}
    swap_time = speed_map.get(speed, 0.32)

    # ── Layout ──────────────────────────────────────────────────────────────
    # Main shelf occupies left ~55% of frame; right ~30% is the stamp column.
    # Shift main shelf center slightly left to balance visually.
    block_w = max(0.38, min(0.85, (FRAME_W * 0.52 - 0.10 * max(n - 1, 0)) / max(n, 1)))
    block_h = 0.62
    gap     = 0.10

    total_main_w  = n * block_w + (n - 1) * gap
    shelf_center_x = -FRAME_W * 0.12  # slight left offset

    slot_x = [
        shelf_center_x - total_main_w / 2 + block_w / 2 + k * (block_w + gap)
        for k in range(n)
    ]
    shelf_y = MATH_CENTER_Y - block_h / 2 - 0.08

    # Stamp column — flush to right edge
    s_sc          = 0.38
    stamp_bw      = block_w * s_sc
    stamp_bh      = block_h * s_sc
    stamp_gap_w   = gap * s_sc
    stamp_row_w   = n * stamp_bw + (n - 1) * stamp_gap_w
    stamp_col_x   = FRAME_W / 2 - stamp_row_w / 2 - 0.12
    stamp_start_y = min(MATH_CENTER_Y + 1.6, FRAME_H / 2 - 0.4)  # clamp top

    # Dynamically shrink row spacing if too many perms to fit vertically
    raw_row_h = stamp_bh + 0.09
    available_h = stamp_start_y - (-FRAME_H / 2 + 0.5)
    if len(perms) > 0:
        stamp_row_h = min(raw_row_h, available_h / len(perms))
    else:
        stamp_row_h = raw_row_h

    # ── Shelf bar ────────────────────────────────────────────────────────────
    shelf_bar = Line(
        [slot_x[0]  - block_w / 2 - 0.15, shelf_y, 0],
        [slot_x[-1] + block_w / 2 + 0.15, shelf_y, 0],
        color=WHITE, stroke_opacity=0.30, stroke_width=2,
    )

    # ── Build one VGroup block mob per object ────────────────────────────────
    block_for_obj = {}
    for obj_idx, obj in enumerate(objects):
        font_sz = max(14, int(block_w * 28))
        rect = RoundedRectangle(
            corner_radius=0.10,
            width=block_w, height=block_h,
            fill_color=obj["color"], fill_opacity=0.88,
            stroke_color=WHITE, stroke_width=1.5, stroke_opacity=0.50,
        )
        lbl = Text(obj["label"], font_size=font_sz, color=WHITE, weight=BOLD)
        block_for_obj[obj_idx] = VGroup(rect, lbl)

    # Place blocks at initial permutation positions
    initial_perm = perms[0]
    for slot_k, obj_idx in enumerate(initial_perm):
        block_for_obj[obj_idx].move_to([slot_x[slot_k], MATH_CENTER_Y, 0])

    # Slot-tracking dicts
    current_perm     = list(initial_perm)
    current_slot_of  = {obj_idx: slot_k for slot_k, obj_idx in enumerate(initial_perm)}

    # ── Timing model: audio → fade previous → fade in shelf + blocks ─────────
    had_previous = previous is not None

    if audio_path and os.path.exists(audio_path):
        self.add_sound(audio_path)

    if previous is not None:
        self.play(FadeOut(previous, shift=UP * 0.3), run_time=0.3)
        self.wait(0.15)

    if shelf_vis:
        self.play(FadeIn(shelf_bar), run_time=0.35)

    block_list = list(block_for_obj.values())
    self.play(*[FadeIn(b, scale=0.85) for b in block_list], run_time=0.55)

    # ── Cycle through each permutation ───────────────────────────────────────
    all_stamps  = []
    count_mob   = None

    for perm_idx, target_perm in enumerate(perms):
        # Brief pause so viewer can "read" the current arrangement
        self.wait(max(0.15, swap_time * 0.8))

        # Stamp current arrangement as a small row to the right
        row_y = stamp_start_y - perm_idx * stamp_row_h
        row_y = max(-FRAME_H / 2 + 0.35, row_y)   # overflow guard

        stamp_items = []
        for slot_k in range(n):
            obj_idx = current_perm[slot_k]
            obj     = objects[obj_idx]
            sr = RoundedRectangle(
                corner_radius=0.04,
                width=stamp_bw, height=stamp_bh,
                fill_color=obj["color"], fill_opacity=0.60,
                stroke_color=WHITE, stroke_width=0.7, stroke_opacity=0.35,
            )
            sx = (stamp_col_x - stamp_row_w / 2 + stamp_bw / 2
                  + slot_k * (stamp_bw + stamp_gap_w))
            if stamp_bw >= 0.20:
                sl = Text(obj["label"], font_size=7, color=WHITE)
                si = VGroup(sr, sl)
            else:
                si = sr
            si.move_to([sx, row_y, 0])
            stamp_items.append(si)

        stamp_row = VGroup(*stamp_items)
        all_stamps.append(stamp_row)
        self.play(FadeIn(stamp_row, scale=0.88), run_time=0.28)

        # Slide blocks to next permutation (simultaneous moves)
        if perm_idx < len(perms) - 1:
            next_perm  = perms[perm_idx + 1]
            move_anims = []
            for tgt_slot, obj_idx in enumerate(next_perm):
                if current_slot_of[obj_idx] != tgt_slot:
                    move_anims.append(
                        block_for_obj[obj_idx].animate.move_to(
                            [slot_x[tgt_slot], MATH_CENTER_Y, 0]
                        )
                    )
            if move_anims:
                self.play(*move_anims,
                          run_time=max(0.28, swap_time * n),
                          rate_func=smooth)

            # Update slot tracking
            for tgt_slot, obj_idx in enumerate(next_perm):
                current_slot_of[obj_idx] = tgt_slot
            current_perm = list(next_perm)

    # ── Count label ("6 ways", "2 ways", "1 way") ────────────────────────────
    if show_count:
        n_ways  = len(perms)
        count_y = stamp_start_y - n_ways * stamp_row_h - 0.20
        count_y = max(-FRAME_H / 2 + 0.45, count_y)
        way_str = "way" if n_ways == 1 else "ways"
        count_mob = Text(
            str(n_ways) + " " + way_str,
            font_size=20, color=WHITE,
        ).move_to([stamp_col_x, count_y, 0])
        self.play(FadeIn(count_mob, shift=UP * 0.12), run_time=0.45)

    # ── Hold remaining duration ───────────────────────────────────────────────
    anim_spent = (
        (0.30 + 0.15 if had_previous else 0)         # fadeout previous
        + (0.35 if shelf_vis else 0)                 # shelf fade-in
        + 0.55                                       # block fade-in
        + len(perms) * (max(0.15, swap_time * 0.8) + 0.28)   # per-perm
        + (len(perms) - 1) * max(0.28, swap_time * n)         # transitions
        + (0.45 if show_count else 0)                          # count label
    )
    self.wait(max(0.5, duration - anim_spent))

    if i < len(steps) - 1:
        self.wait(EXTRA_HOLD)

    # Package everything as `previous` so next step can fade it out cleanly
    blocks_grp = VGroup(*block_list)
    stamp_grp  = VGroup(*all_stamps) if all_stamps else VGroup()
    prev_parts = [blocks_grp, stamp_grp]
    if shelf_vis:
        prev_parts.insert(0, shelf_bar)
    if count_mob:
        prev_parts.append(count_mob)
    previous = VGroup(*prev_parts)
    continue
'''

# ═════════════════════════════════════════════════════════════════════════════
# SECTION 2 — STEP TYPE: empty_shelf
# ═════════════════════════════════════════════════════════════════════════════
#
# Paste this block immediately AFTER the permutation_display block, still
# before the content fallthrough.
# ─────────────────────────────────────────────────────────────────────────────

EMPTY_SHELF_CODE = '''
# ── EMPTY SHELF (punchline: one way to arrange nothing) ──
if stype == "empty_shelf":
    duration   = step.get("duration", 8.0)
    audio_path = step.get("audio_path", "")
    es_cfg     = step.get("empty_shelf", {})

    shelf_style    = es_cfg.get("shelf_style", "bar")        # reserved for future styles
    glow_enabled   = es_cfg.get("glow", True)
    glow_color_hex = es_cfg.get("glow_color", "#22D3EE")
    caption_text   = es_cfg.get("caption", None)
    pause_dur      = es_cfg.get("pause_duration", 1.0)

    # ── Build shelf (same proportions as permutation_display) ────────────────
    shelf_w = FRAME_W * 0.50
    # Vertically center slightly above math center for breathing room
    shelf_y = MATH_CENTER_Y - 0.35

    shelf_bar = Line(
        [-shelf_w / 2, shelf_y, 0],
        [ shelf_w / 2, shelf_y, 0],
        color=WHITE, stroke_opacity=0.30, stroke_width=2,
    )

    # ── Timing model: audio → fade previous → show shelf ─────────────────────
    had_previous = previous is not None

    if audio_path and os.path.exists(audio_path):
        self.add_sound(audio_path)

    if previous is not None:
        self.play(FadeOut(previous, shift=UP * 0.3), run_time=0.3)
        self.wait(0.15)

    self.play(FadeIn(shelf_bar), run_time=0.40)

    # ── Stillness (configurable pause before glow) ────────────────────────────
    self.wait(max(0.2, pause_dur))

    # ── Glow pulse radiating outward from shelf ───────────────────────────────
    if glow_enabled:
        # Start: a flat ellipse sitting on the shelf
        glow_start = Ellipse(
            width=shelf_w * 0.55, height=0.18,
            fill_color=glow_color_hex, fill_opacity=0.30,
            stroke_opacity=0,
        )
        glow_start.move_to([0, shelf_y, 0])

        # End: expanded, fully transparent (gives the "radiating outward" look)
        glow_end = Ellipse(
            width=shelf_w * 2.0, height=0.75,
            fill_color=glow_color_hex, fill_opacity=0.00,
            stroke_opacity=0,
        )
        glow_end.move_to([0, shelf_y, 0])

        self.add(glow_start)
        # Transform morphs width, height, and opacity simultaneously
        self.play(Transform(glow_start, glow_end), run_time=0.72, rate_func=smooth)
        self.remove(glow_start)

    # ── Count label "1" fades in below shelf ─────────────────────────────────
    count_y   = shelf_y - 0.58
    count_mob = Text("1", font_size=52, color=WHITE, weight=BOLD)
    count_mob.move_to([0, count_y, 0])
    self.play(FadeIn(count_mob, shift=UP * 0.15), run_time=0.50)

    # ── Optional caption writes in below count ────────────────────────────────
    all_mobs     = [shelf_bar, count_mob]
    caption_mob  = None

    if caption_text:
        cap_y       = count_y - 0.65
        caption_mob = Text(caption_text, font_size=18, color=WHITE)
        caption_mob.set_opacity(0.72)
        _clamp(caption_mob)
        caption_mob.move_to([0, cap_y, 0])
        self.play(Write(caption_mob), run_time=0.65)
        all_mobs.append(caption_mob)

    # ── Hold remaining ────────────────────────────────────────────────────────
    anim_spent = (
        (0.30 + 0.15 if had_previous else 0)         # fadeout previous
        + 0.40                                       # shelf fade-in
        + max(0.2, pause_dur)                        # silence
        + (0.72 if glow_enabled else 0)              # glow pulse
        + 0.50                                       # count fade-in
        + (0.65 if caption_text else 0)              # caption write
    )
    self.wait(max(0.5, duration - anim_spent))

    if i < len(steps) - 1:
        self.wait(EXTRA_HOLD)

    previous = VGroup(*all_mobs)
    continue
'''

# ═════════════════════════════════════════════════════════════════════════════
# SECTION 3 — F-STRING ESCAPING REFERENCE
# ═════════════════════════════════════════════════════════════════════════════
#
# The code above is written as clean Python (single braces).
# When pasting into scene_short.py's  scene_code = f\'\'\'...\'\'\'  block,
# you MUST double every Python-syntax brace:
#
#   Python dict:   {"key": val}          →  {{"key": val}}
#   Set literal:   {1, 2, 3}             →  {{1, 2, 3}}
#   f-string:      f"{var}"              →  f"{{var}}"   or use .format()
#   Format:        "{:.2f}".format(x)    →  "{:.2f}".format(x)  ← FINE as-is
#                                            (only the outer f\'\'\'...\'\'\'  matters)
#
# List comprehensions, function calls, and indexing DO NOT use { }:
#   [x for x in range(n)]  →  no escaping needed
#   obj["label"]            →  obj["label"]  ← these quotes are fine
#
# QUICK FIND-AND-REPLACE STRATEGY (in your editor):
#   1. Paste the block verbatim.
#   2. Regex replace:  (?<!\{)\{(?!\{)   →  {{    (opens not already doubled)
#   3. Regex replace:  (?<!\})\}(?!\})   →  }}    (closes not already doubled)
#   4. Then fix any generator-substitution variables that got doubled:
#      {{_fw}} → {_fw}, {{_fh}} → {_fh}, etc.
#   Step 4 is only relevant if you copy from a file that MIXED substitutions
#   with step-handler code — which this file does NOT do.
#
# RECOMMENDATION: the two blocks above contain ZERO f-string substitutions
# (no {_fw}, {_mcy} etc.). So you can safely double ALL braces with no fixup.

# ═════════════════════════════════════════════════════════════════════════════
# SECTION 4 — LIBRARY CATALOG ENTRIES
# ═════════════════════════════════════════════════════════════════════════════
#
# Add these two rows to the table in visual_library.md:
#
# | # | Type | Description | Config Fields | Example Use |
# |---|------|-------------|---------------|-------------|
# | 15 | `permutation_display` | N colored blocks on a shelf slide into every arrangement. Each completed arrangement stamps as a mini-row to the right. Count label appears after all shown. | `permutation_display.objects[]` ({label,color}), `permutation_display.permutations` ("all" or list of index-lists), `permutation_display.show_count` (bool), `permutation_display.shelf_visible` (bool), `permutation_display.speed` ("slow"/"normal"/"fast") | "How many ways can 3 items be ordered?" |
# | 16 | `empty_shelf` | Empty shelf bar — the punchline for "one way to arrange nothing." Shelf appears, pauses in silence, a cyan glow pulses outward, count "1" fades in, optional caption writes in. | `empty_shelf.glow` (bool), `empty_shelf.glow_color` (hex), `empty_shelf.caption` (str or null), `empty_shelf.pause_duration` (float, default 1.0), `empty_shelf.shelf_style` ("bar") | "0! = 1 — the empty arrangement" |

# ═════════════════════════════════════════════════════════════════════════════
# SECTION 5 — TEST MANIFEST (for reference; saved separately as JSON)
# ═════════════════════════════════════════════════════════════════════════════

TEST_MANIFEST = [
    {
        "type": "text",
        "content": r"3\ \text{objects: how many orders?}",
        "duration": 3.5,
        "audio_path": ""
    },
    {
        "type": "permutation_display",
        "content": "",
        "duration": 16.0,
        "audio_path": "",
        "permutation_display": {
            "objects": [
                {"label": "A", "color": "#22D3EE"},
                {"label": "B", "color": "#39FF14"},
                {"label": "C", "color": "#9333EA"}
            ],
            "permutations": "all",
            "show_count": True,
            "shelf_visible": True,
            "speed": "normal"
        }
    },
    {
        "type": "text",
        "content": r"\text{What about arranging nothing?}",
        "duration": 3.5,
        "audio_path": ""
    },
    {
        "type": "empty_shelf",
        "content": "",
        "duration": 8.0,
        "audio_path": "",
        "empty_shelf": {
            "shelf_style": "bar",
            "glow": True,
            "glow_color": "#22D3EE",
            "caption": "The empty arrangement",
            "pause_duration": 1.0
        }
    }
]

# ═════════════════════════════════════════════════════════════════════════════
# SECTION 6 — STANDALONE TEST SCENE
# ═════════════════════════════════════════════════════════════════════════════
#
# Run with:
#   manim new_scene_types.py TestPermutationDisplay -p --quality l
#   manim new_scene_types.py TestEmptyShelf -p --quality l
#   manim new_scene_types.py TestBothTypes -p --quality l

try:
    from manim import *
    import os as _os
    import numpy as _np

    # ── Same constants as portrait scene_short.py generates ──────────────────
    ORBITAL_CYAN   = "#22D3EE"
    NEON_GREEN     = "#39FF14"
    BOX_BORDER     = "#8B5CF6"
    BOX_FILL       = "#1a1130"
    LABEL_COLOR    = "#22D3EE"
    FRAME_W        = 4.5
    FRAME_H        = 8.0
    MAX_WIDTH      = FRAME_W * 0.82
    MATH_SCALE     = 0.85
    BOX_SCALE      = 0.65
    GRAPH_WIDTH    = 3.4
    GRAPH_HEIGHT   = 2.8
    MATH_CENTER_Y  = 1.2
    GRAPH_CENTER_Y = -1.8
    ZONE_A_Y       = 2.5
    ANIMATION_RATIO = 0.35
    EXTRA_HOLD      = 0.5

    def _clamp(mob, max_w=None):
        if max_w is None:
            max_w = MAX_WIDTH
        if mob.width > max_w:
            mob.scale(max_w / mob.width)
        return mob

    # ─────────────────────────────────────────────────────────────────────────
    class TestPermutationDisplay(Scene):
        """Tests permutation_display with 3 objects, all permutations."""

        def construct(self):
            self.camera.background_color = "#000000"

            # Border (same as generated scenes)
            border = Rectangle(
                width=FRAME_W - 0.15, height=FRAME_H - 0.15,
                color="#8B5CF6", stroke_width=2.5, stroke_opacity=0.7,
                fill_opacity=0,
            )
            self.add(border)

            # ── Minimal intro step ────────────────────────────────────────────
            intro = Text("Permutation Display", font_size=28, color=WHITE)
            intro.move_to([0, MATH_CENTER_Y + 1.8, 0])
            self.play(Write(intro), run_time=1.0)
            self.wait(1.0)
            self.play(FadeOut(intro, shift=UP * 0.3), run_time=0.3)

            previous = None

            # ── Step: permutation_display ─────────────────────────────────────
            from itertools import permutations as _iterperms

            objects     = [
                {"label": "A", "color": "#22D3EE"},
                {"label": "B", "color": "#39FF14"},
                {"label": "C", "color": "#9333EA"},
            ]
            perms_input = "all"
            show_count  = True
            shelf_vis   = True
            speed       = "normal"
            duration    = 16.0
            audio_path  = ""

            n = len(objects)
            if perms_input == "all":
                perms = list(_iterperms(range(n)))
            else:
                perms = [tuple(p) for p in perms_input]

            speed_map = {"slow": 0.55, "normal": 0.32, "fast": 0.15}
            swap_time = speed_map.get(speed, 0.32)

            # Layout
            block_w = max(0.38, min(0.85, (FRAME_W * 0.52 - 0.10 * max(n - 1, 0)) / max(n, 1)))
            block_h = 0.62
            gap     = 0.10
            total_main_w  = n * block_w + (n - 1) * gap
            shelf_center_x = -FRAME_W * 0.12
            slot_x = [
                shelf_center_x - total_main_w / 2 + block_w / 2 + k * (block_w + gap)
                for k in range(n)
            ]
            shelf_y = MATH_CENTER_Y - block_h / 2 - 0.08

            s_sc        = 0.38
            stamp_bw    = block_w * s_sc
            stamp_bh    = block_h * s_sc
            stamp_gap_w = gap * s_sc
            stamp_row_w = n * stamp_bw + (n - 1) * stamp_gap_w
            stamp_col_x = FRAME_W / 2 - stamp_row_w / 2 - 0.12
            stamp_start_y = min(MATH_CENTER_Y + 1.6, FRAME_H / 2 - 0.4)
            raw_row_h   = stamp_bh + 0.09
            available_h = stamp_start_y - (-FRAME_H / 2 + 0.5)
            stamp_row_h = min(raw_row_h, available_h / max(len(perms), 1))

            shelf_bar = Line(
                [slot_x[0]  - block_w / 2 - 0.15, shelf_y, 0],
                [slot_x[-1] + block_w / 2 + 0.15, shelf_y, 0],
                color=WHITE, stroke_opacity=0.30, stroke_width=2,
            )

            block_for_obj = {}
            for obj_idx, obj in enumerate(objects):
                font_sz = max(14, int(block_w * 28))
                rect = RoundedRectangle(
                    corner_radius=0.10,
                    width=block_w, height=block_h,
                    fill_color=obj["color"], fill_opacity=0.88,
                    stroke_color=WHITE, stroke_width=1.5, stroke_opacity=0.50,
                )
                lbl = Text(obj["label"], font_size=font_sz, color=WHITE, weight=BOLD)
                block_for_obj[obj_idx] = VGroup(rect, lbl)

            initial_perm = perms[0]
            for slot_k, obj_idx in enumerate(initial_perm):
                block_for_obj[obj_idx].move_to([slot_x[slot_k], MATH_CENTER_Y, 0])

            current_perm    = list(initial_perm)
            current_slot_of = {obj_idx: slot_k for slot_k, obj_idx in enumerate(initial_perm)}

            had_previous = previous is not None

            # Audio (none in test)
            if audio_path and _os.path.exists(audio_path):
                self.add_sound(audio_path)

            if previous is not None:
                self.play(FadeOut(previous, shift=UP * 0.3), run_time=0.3)
                self.wait(0.15)

            if shelf_vis:
                self.play(FadeIn(shelf_bar), run_time=0.35)

            block_list = list(block_for_obj.values())
            self.play(*[FadeIn(b, scale=0.85) for b in block_list], run_time=0.55)

            all_stamps = []
            count_mob  = None

            for perm_idx, target_perm in enumerate(perms):
                self.wait(max(0.15, swap_time * 0.8))

                row_y = stamp_start_y - perm_idx * stamp_row_h
                row_y = max(-FRAME_H / 2 + 0.35, row_y)

                stamp_items = []
                for slot_k in range(n):
                    obj_idx = current_perm[slot_k]
                    obj     = objects[obj_idx]
                    sr = RoundedRectangle(
                        corner_radius=0.04,
                        width=stamp_bw, height=stamp_bh,
                        fill_color=obj["color"], fill_opacity=0.60,
                        stroke_color=WHITE, stroke_width=0.7, stroke_opacity=0.35,
                    )
                    sx = (stamp_col_x - stamp_row_w / 2 + stamp_bw / 2
                          + slot_k * (stamp_bw + stamp_gap_w))
                    if stamp_bw >= 0.20:
                        sl = Text(obj["label"], font_size=7, color=WHITE)
                        si = VGroup(sr, sl)
                    else:
                        si = sr
                    si.move_to([sx, row_y, 0])
                    stamp_items.append(si)

                stamp_row = VGroup(*stamp_items)
                all_stamps.append(stamp_row)
                self.play(FadeIn(stamp_row, scale=0.88), run_time=0.28)

                if perm_idx < len(perms) - 1:
                    next_perm  = perms[perm_idx + 1]
                    move_anims = []
                    for tgt_slot, obj_idx in enumerate(next_perm):
                        if current_slot_of[obj_idx] != tgt_slot:
                            move_anims.append(
                                block_for_obj[obj_idx].animate.move_to(
                                    [slot_x[tgt_slot], MATH_CENTER_Y, 0]
                                )
                            )
                    if move_anims:
                        self.play(*move_anims,
                                  run_time=max(0.28, swap_time * n),
                                  rate_func=smooth)
                    for tgt_slot, obj_idx in enumerate(next_perm):
                        current_slot_of[obj_idx] = tgt_slot
                    current_perm = list(next_perm)

            if show_count:
                n_ways  = len(perms)
                count_y = stamp_start_y - n_ways * stamp_row_h - 0.20
                count_y = max(-FRAME_H / 2 + 0.45, count_y)
                way_str = "way" if n_ways == 1 else "ways"
                count_mob = Text(
                    str(n_ways) + " " + way_str,
                    font_size=20, color=WHITE,
                ).move_to([stamp_col_x, count_y, 0])
                self.play(FadeIn(count_mob, shift=UP * 0.12), run_time=0.45)

            self.wait(2.0)

            # End card
            blocks_grp = VGroup(*block_list)
            stamp_grp  = VGroup(*all_stamps) if all_stamps else VGroup()
            prev_parts = [blocks_grp, stamp_grp]
            if shelf_vis:
                prev_parts.insert(0, shelf_bar)
            if count_mob:
                prev_parts.append(count_mob)
            self.play(FadeOut(VGroup(*prev_parts)), run_time=0.5)

    # ─────────────────────────────────────────────────────────────────────────
    class TestEmptyShelf(Scene):
        """Tests empty_shelf: pause → glow → count '1' → caption."""

        def construct(self):
            self.camera.background_color = "#000000"

            border = Rectangle(
                width=FRAME_W - 0.15, height=FRAME_H - 0.15,
                color="#8B5CF6", stroke_width=2.5, stroke_opacity=0.7,
                fill_opacity=0,
            )
            self.add(border)

            previous = None

            # ── Step: empty_shelf ─────────────────────────────────────────────
            glow_enabled   = True
            glow_color_hex = "#22D3EE"
            caption_text   = "The empty arrangement"
            pause_dur      = 1.0
            audio_path     = ""
            duration       = 8.0

            shelf_w  = FRAME_W * 0.50
            shelf_y  = MATH_CENTER_Y - 0.35

            shelf_bar = Line(
                [-shelf_w / 2, shelf_y, 0],
                [ shelf_w / 2, shelf_y, 0],
                color=WHITE, stroke_opacity=0.30, stroke_width=2,
            )

            had_previous = previous is not None

            if audio_path and _os.path.exists(audio_path):
                self.add_sound(audio_path)

            if previous is not None:
                self.play(FadeOut(previous, shift=UP * 0.3), run_time=0.3)
                self.wait(0.15)

            self.play(FadeIn(shelf_bar), run_time=0.40)
            self.wait(max(0.2, pause_dur))

            if glow_enabled:
                glow_start = Ellipse(
                    width=shelf_w * 0.55, height=0.18,
                    fill_color=glow_color_hex, fill_opacity=0.30,
                    stroke_opacity=0,
                )
                glow_start.move_to([0, shelf_y, 0])
                glow_end = Ellipse(
                    width=shelf_w * 2.0, height=0.75,
                    fill_color=glow_color_hex, fill_opacity=0.00,
                    stroke_opacity=0,
                )
                glow_end.move_to([0, shelf_y, 0])
                self.add(glow_start)
                self.play(Transform(glow_start, glow_end), run_time=0.72, rate_func=smooth)
                self.remove(glow_start)

            count_y   = shelf_y - 0.58
            count_mob = Text("1", font_size=52, color=WHITE, weight=BOLD)
            count_mob.move_to([0, count_y, 0])
            self.play(FadeIn(count_mob, shift=UP * 0.15), run_time=0.50)

            all_mobs    = [shelf_bar, count_mob]
            caption_mob = None

            if caption_text:
                cap_y       = count_y - 0.65
                caption_mob = Text(caption_text, font_size=18, color=WHITE)
                caption_mob.set_opacity(0.72)
                _clamp(caption_mob)
                caption_mob.move_to([0, cap_y, 0])
                self.play(Write(caption_mob), run_time=0.65)
                all_mobs.append(caption_mob)

            self.wait(2.0)
            self.play(FadeOut(VGroup(*all_mobs)), run_time=0.5)

    # ─────────────────────────────────────────────────────────────────────────
    class TestBothTypes(Scene):
        """Full sequence: intro text → permutation_display → empty_shelf."""

        def construct(self):
            self.camera.background_color = "#000000"

            border = Rectangle(
                width=FRAME_W - 0.15, height=FRAME_H - 0.15,
                color="#8B5CF6", stroke_width=2.5, stroke_opacity=0.7,
                fill_opacity=0,
            )
            self.add(border)

            wm = Text("ORBITAL", font_size=10, color=WHITE, weight=BOLD)
            wm.set_opacity(0.35)
            wm.move_to([-FRAME_W / 2 + 0.5, -FRAME_H / 2 + 0.2, 0])
            self.add(wm)

            previous = None

            # ── Step 1: intro text ────────────────────────────────────────────
            step1 = Text("3 objects — how many orders?",
                         font_size=24, color=WHITE)
            _clamp(step1)
            step1.move_to([0, MATH_CENTER_Y, 0])
            self.play(Write(step1), run_time=1.2)
            self.wait(2.0)
            previous = step1

            # ── Step 2: permutation_display ───────────────────────────────────
            from itertools import permutations as _iterperms

            objects = [
                {"label": "A", "color": "#22D3EE"},
                {"label": "B", "color": "#39FF14"},
                {"label": "C", "color": "#9333EA"},
            ]
            perms       = list(_iterperms(range(3)))
            show_count  = True
            shelf_vis   = True
            speed       = "fast"   # faster for full-pipeline test
            duration    = 20.0
            audio_path  = ""

            n = 3
            speed_map = {"slow": 0.55, "normal": 0.32, "fast": 0.15}
            swap_time = speed_map.get(speed, 0.32)

            block_w = max(0.38, min(0.85, (FRAME_W * 0.52 - 0.10 * (n - 1)) / n))
            block_h = 0.62
            gap     = 0.10
            total_main_w  = n * block_w + (n - 1) * gap
            shelf_center_x = -FRAME_W * 0.12
            slot_x = [
                shelf_center_x - total_main_w / 2 + block_w / 2 + k * (block_w + gap)
                for k in range(n)
            ]
            shelf_y = MATH_CENTER_Y - block_h / 2 - 0.08

            s_sc        = 0.38
            stamp_bw    = block_w * s_sc
            stamp_bh    = block_h * s_sc
            stamp_gap_w = gap * s_sc
            stamp_row_w = n * stamp_bw + (n - 1) * stamp_gap_w
            stamp_col_x = FRAME_W / 2 - stamp_row_w / 2 - 0.12
            stamp_start_y = min(MATH_CENTER_Y + 1.6, FRAME_H / 2 - 0.4)
            raw_row_h   = stamp_bh + 0.09
            available_h = stamp_start_y - (-FRAME_H / 2 + 0.5)
            stamp_row_h = min(raw_row_h, available_h / max(len(perms), 1))

            shelf_bar = Line(
                [slot_x[0]  - block_w / 2 - 0.15, shelf_y, 0],
                [slot_x[-1] + block_w / 2 + 0.15, shelf_y, 0],
                color=WHITE, stroke_opacity=0.30, stroke_width=2,
            )
            block_for_obj = {}
            for obj_idx, obj in enumerate(objects):
                font_sz = max(14, int(block_w * 28))
                rect = RoundedRectangle(
                    corner_radius=0.10, width=block_w, height=block_h,
                    fill_color=obj["color"], fill_opacity=0.88,
                    stroke_color=WHITE, stroke_width=1.5, stroke_opacity=0.50,
                )
                lbl = Text(obj["label"], font_size=font_sz, color=WHITE, weight=BOLD)
                block_for_obj[obj_idx] = VGroup(rect, lbl)

            initial_perm = perms[0]
            for slot_k, obj_idx in enumerate(initial_perm):
                block_for_obj[obj_idx].move_to([slot_x[slot_k], MATH_CENTER_Y, 0])

            current_perm    = list(initial_perm)
            current_slot_of = {obj_idx: slot_k for slot_k, obj_idx in enumerate(initial_perm)}

            if previous is not None:
                self.play(FadeOut(previous, shift=UP * 0.3), run_time=0.3)
                self.wait(0.15)

            self.play(FadeIn(shelf_bar), run_time=0.35)
            block_list = list(block_for_obj.values())
            self.play(*[FadeIn(b, scale=0.85) for b in block_list], run_time=0.55)

            all_stamps = []
            count_mob  = None

            for perm_idx, target_perm in enumerate(perms):
                self.wait(max(0.15, swap_time * 0.8))
                row_y = stamp_start_y - perm_idx * stamp_row_h
                row_y = max(-FRAME_H / 2 + 0.35, row_y)
                stamp_items = []
                for slot_k in range(n):
                    obj_idx = current_perm[slot_k]
                    obj     = objects[obj_idx]
                    sr = RoundedRectangle(
                        corner_radius=0.04, width=stamp_bw, height=stamp_bh,
                        fill_color=obj["color"], fill_opacity=0.60,
                        stroke_color=WHITE, stroke_width=0.7, stroke_opacity=0.35,
                    )
                    sx = (stamp_col_x - stamp_row_w / 2 + stamp_bw / 2
                          + slot_k * (stamp_bw + stamp_gap_w))
                    if stamp_bw >= 0.20:
                        sl = Text(obj["label"], font_size=7, color=WHITE)
                        si = VGroup(sr, sl)
                    else:
                        si = sr
                    si.move_to([sx, row_y, 0])
                    stamp_items.append(si)
                stamp_row = VGroup(*stamp_items)
                all_stamps.append(stamp_row)
                self.play(FadeIn(stamp_row, scale=0.88), run_time=0.28)
                if perm_idx < len(perms) - 1:
                    next_perm  = perms[perm_idx + 1]
                    move_anims = []
                    for tgt_slot, obj_idx in enumerate(next_perm):
                        if current_slot_of[obj_idx] != tgt_slot:
                            move_anims.append(
                                block_for_obj[obj_idx].animate.move_to(
                                    [slot_x[tgt_slot], MATH_CENTER_Y, 0]
                                )
                            )
                    if move_anims:
                        self.play(*move_anims,
                                  run_time=max(0.28, swap_time * n),
                                  rate_func=smooth)
                    for tgt_slot, obj_idx in enumerate(next_perm):
                        current_slot_of[obj_idx] = tgt_slot
                    current_perm = list(next_perm)

            if show_count:
                n_ways  = len(perms)
                count_y = stamp_start_y - n_ways * stamp_row_h - 0.20
                count_y = max(-FRAME_H / 2 + 0.45, count_y)
                way_str = "way" if n_ways == 1 else "ways"
                count_mob = Text(
                    str(n_ways) + " " + way_str, font_size=20, color=WHITE,
                ).move_to([stamp_col_x, count_y, 0])
                self.play(FadeIn(count_mob, shift=UP * 0.12), run_time=0.45)

            self.wait(1.0)

            # Package as previous for empty_shelf
            blocks_grp = VGroup(*block_list)
            stamp_grp  = VGroup(*all_stamps) if all_stamps else VGroup()
            prev_parts = [shelf_bar, blocks_grp, stamp_grp]
            if count_mob:
                prev_parts.append(count_mob)
            previous = VGroup(*prev_parts)

            # ── Step 3: empty_shelf ───────────────────────────────────────────
            glow_enabled   = True
            glow_color_hex = "#22D3EE"
            caption_text   = "The empty arrangement"
            pause_dur      = 1.0
            audio_path     = ""

            shelf_w2 = FRAME_W * 0.50
            shelf_y2 = MATH_CENTER_Y - 0.35
            shelf_bar2 = Line(
                [-shelf_w2 / 2, shelf_y2, 0],
                [ shelf_w2 / 2, shelf_y2, 0],
                color=WHITE, stroke_opacity=0.30, stroke_width=2,
            )

            if previous is not None:
                self.play(FadeOut(previous, shift=UP * 0.3), run_time=0.3)
                self.wait(0.15)

            self.play(FadeIn(shelf_bar2), run_time=0.40)
            self.wait(max(0.2, pause_dur))

            if glow_enabled:
                glow_start = Ellipse(
                    width=shelf_w2 * 0.55, height=0.18,
                    fill_color=glow_color_hex, fill_opacity=0.30,
                    stroke_opacity=0,
                )
                glow_start.move_to([0, shelf_y2, 0])
                glow_end = Ellipse(
                    width=shelf_w2 * 2.0, height=0.75,
                    fill_color=glow_color_hex, fill_opacity=0.00,
                    stroke_opacity=0,
                )
                glow_end.move_to([0, shelf_y2, 0])
                self.add(glow_start)
                self.play(Transform(glow_start, glow_end), run_time=0.72, rate_func=smooth)
                self.remove(glow_start)

            count_y2   = shelf_y2 - 0.58
            count_mob2 = Text("1", font_size=52, color=WHITE, weight=BOLD)
            count_mob2.move_to([0, count_y2, 0])
            self.play(FadeIn(count_mob2, shift=UP * 0.15), run_time=0.50)

            all_mobs = [shelf_bar2, count_mob2]
            if caption_text:
                cap_y       = count_y2 - 0.65
                caption_mob = Text(caption_text, font_size=18, color=WHITE)
                caption_mob.set_opacity(0.72)
                _clamp(caption_mob)
                caption_mob.move_to([0, cap_y, 0])
                self.play(Write(caption_mob), run_time=0.65)
                all_mobs.append(caption_mob)

            self.wait(2.5)
            self.play(FadeOut(VGroup(*all_mobs)), run_time=0.5)


except ImportError:
    # manim not in path — this is fine when imported as a library
    pass


# ═════════════════════════════════════════════════════════════════════════════
# SECTION 7 — DESIGN NOTES AND GOTCHAS
# ═════════════════════════════════════════════════════════════════════════════
#
# permutation_display:
#   • Recommended: n ≤ 4 objects. For n=4, 4! = 24 perms — stamps get tiny
#     but still legible. For n=5+ (120 perms), provide a subset via perms[].
#   • The slot_x list is immutable after build. Blocks are tracked by their
#     object index (not slot index), so multi-way simultaneous moves never
#     "fight" over the same slot.
#   • Text() is used for block labels (not MathTex) because MathTex strips
#     leading/trailing spaces and doesn't render single letters cleanly at
#     small sizes.
#   • stamp_row_h auto-shrinks if len(perms) would push rows off screen.
#   • In landscape mode: FRAME_W=14.2, MATH_CENTER_Y=1.5 — blocks will be
#     larger and stamps will have more horizontal room. No code changes needed.
#
# empty_shelf:
#   • The glow uses Transform between two Ellipse objects (start → end).
#     Manim interpolates fill_opacity, width, height simultaneously.
#     After the Transform, glow_start is removed (it was morphed in-place).
#   • shelf_style="bar" is the only implemented style. Reserved for future
#     variants (e.g. "dotted", "double").
#   • caption_text can be None to skip the caption entirely. The step still
#     shows shelf + glow + count.
#   • pause_duration creates genuine stillness (no animation) between the
#     shelf appearing and the glow — this is the "held breath" moment.
#
# Both types:
#   • Follow the mandatory timing model: audio → fade previous → animate →
#     hold → EXTRA_HOLD. The `had_previous` flag captures the pre-step state
#     so anim_spent calculations remain accurate.
#   • FRAME_W, FRAME_H, MATH_CENTER_Y are already defined in the generated
#     scene — both portrait and landscape values are injected by the generator.
#     No hardcoded values in the step handlers.
#   • _clamp() is already available in the generated scene.
