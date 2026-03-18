"""
Orbital Engine — Global Configuration
All visual constants, colors, and locked settings.
"""
from pathlib import Path

# ── Paths ──
ENGINE_DIR = str(Path(__file__).parent)
VENV_PYTHON = str(Path(__file__).parent.parent / "orbital_longform" / "venv" / "bin" / "python3")
BG_MUSIC = str(Path.home() / "Desktop" / "Orbital-Shorts-Gen1" / "assets" / "audio" / "bg_synthwave.mp3")
TEXTBOOK_DIR = str(Path.home() / "Desktop" / "Axiom-Reader" / "content" / "precalculus")

# ── Colors (LOCKED) ──
ORBITAL_CYAN = "#22D3EE"
END_CYAN = "#00E5FF"
NEON_GREEN = "#39FF14"
GOLD = "#D6BC82"
CRIMSON = "#8C2232"
VIOLET = "#8B5CF6"
AXIOM_TEXT = "#E0E0E0"
BOX_FILL = "#13121f"
BOX_STROKE = "#252530"
BG_BLACK = "#000000"
PROGRESS_BG = "#333333"
GRID_COLOR = "#1a1a3a"

# ── Layout Presets ──
# These define the spatial grid for every scene.
# Think of each frame as a poster — every zone has a purpose.
#
# LANDSCAPE (16:9, 14.2 × 8.0 Manim units):
#
#   ┌──────────────────────────────────────────────────┐
#   │ margin_top (0.5)                                 │
#   │  ┌──────────────────────────────────────────┐    │
#   │  │          HEADER ZONE (y: 3.0 to 3.5)     │    │
#   │  │  Section badge, title, step labels        │    │
#   │  ├──────────────────────────────────────────┤    │
#   │  │                                          │    │
#   │  │         CONTENT ZONE (y: -2.5 to 2.5)    │    │
#   │  │  Full: one element centered              │    │
#   │  │  Split: left panel + right panel         │    │
#   │  │  Graph: axes centered, fill the zone     │    │
#   │  │                                          │    │
#   │  ├──────────────────────────────────────────┤    │
#   │  │         FOOTER ZONE (y: -3.0 to -3.5)    │    │
#   │  │  Result badges, verdicts, notes           │    │
#   │  └──────────────────────────────────────────┘    │
#   │ margin_bottom (0.5) — watermark lives here       │
#   └──────────────────────────────────────────────────┘
#
# All content stays within safe_x: [-6.5, 6.5] and safe_y: [-3.5, 3.5]
# That's the "poster" — nothing outside it.

LAYOUTS = {
    "short": {
        "frame_w": 4.5,    "frame_h": 8.0,
        "pixel_w": 1080,   "pixel_h": 1920,
        "fps": 60,
        # Spatial zones
        "safe_x": 1.8,          # Content stays within [-1.8, 1.8]
        "safe_y": 3.4,          # Content stays within [-3.4, 3.4]
        "header_y": 3.0,        # Top of header zone
        "content_top": 2.5,     # Top of content zone
        "content_bottom": -2.5, # Bottom of content zone
        "content_center_y": 0.0,
        "footer_y": -3.0,       # Result badges / verdicts
        # Graph
        "graph_width": 3.4,
        "graph_height": 2.8,
        "graph_center": [0, -0.5],
        # Split layout (left/right panels)
        "split_left_x": -1.0,
        "split_right_x": 1.0,
        "split_width": 1.6,     # Width of each panel
        # Typography
        "eq_font_size": 26,
        "note_font_size": 14,
        "title_font_size": 24,
        "wm_font_size": 10,
        # Axes styling (matches proven shorts)
        "axis_color": "#999999",       # Muted grey, NOT white
        "axis_stroke_width": 1.2,      # Thin
        "axis_font_size": 12,
        "curve_stroke_width": 2.5,     # Prominent
        "tick_size": 0.06,
    },
    "landscape": {
        "frame_w": 14.2,   "frame_h": 8.0,
        "pixel_w": 1920,   "pixel_h": 1080,
        "fps": 60,
        # Spatial zones
        "safe_x": 6.5,          # Content stays within [-6.5, 6.5]
        "safe_y": 3.5,          # Content stays within [-3.5, 3.5]
        "header_y": 3.2,        # Top of header zone
        "content_top": 2.8,     # Top of content zone
        "content_bottom": -2.8, # Bottom of content zone
        "content_center_y": 0.0,# Vertical center of content
        "footer_y": -3.2,       # Result badges / verdicts
        # Graph (LARGE — fills content zone)
        "graph_width": 10.0,    # Nearly full width (was 6.0 — way too small)
        "graph_height": 5.0,    # Tall enough to be the star
        "graph_center": [0, 0], # Centered on screen
        # Split layout (left/right panels, e.g. definition + visual)
        "split_left_x": -3.5,   # Center of left panel
        "split_right_x": 3.5,   # Center of right panel
        "split_width": 5.5,     # Width of each panel
        # Typography
        "eq_font_size": 42,
        "note_font_size": 22,
        "title_font_size": 36,
        "wm_font_size": 14,
        # Axes styling (matches proven shorts)
        "axis_color": "#888888",       # Muted grey, thin, subtle
        "axis_stroke_width": 1.2,      # Thin — axes are NOT the star
        "axis_font_size": 14,          # Small number labels
        "curve_stroke_width": 3.0,     # The curve IS the star
        "tick_size": 0.08,
    },
}

# ── Timing Constants (LOCKED) ──
EXTRA_HOLD = 0.5         # Breathing room between steps

# ── Text Hierarchy (LOCKED — from Production Bible) ──
# These are the ONLY text sizes allowed. No arbitrary font_size values.
# MathTex for ALL math/display. Text() ONLY for watermark, box labels, titles, callouts.
TEXT_TIERS = {
    #  tier    font_size  color       method     when
    1: {"name": "punchline",  "font_size": 42, "color": "#39FF14", "method": "MathTex", "boxed": True,  "desc": "Final answer, big reveal"},
    2: {"name": "key_fact",   "font_size": 28, "color": "#22D3EE", "method": "MathTex", "boxed": True,  "desc": "Definitions, theorems"},
    3: {"name": "callout",    "font_size": 24, "color": "#FFFFFF", "method": "Text",    "boxed": False, "desc": "Takeaway statements (BOLD)"},
    4: {"name": "title",      "font_size": 26, "color": "#8B5CF6", "method": "Text",    "boxed": False, "desc": "Section headers (BOLD)"},
    5: {"name": "equation",   "font_size": 30, "color": "#FFFFFF", "method": "MathTex", "boxed": False, "desc": "Long math expressions"},
    6: {"name": "caption",    "font_size": 24, "color": "#22D3EE", "method": "MathTex", "boxed": False, "desc": "Labels, annotations"},
    7: {"name": "counter",    "font_size": 22, "color": "#FFFFFF", "method": "MathTex", "boxed": False, "desc": "Rarely — only when tight"},
}
# Short expressions (< 4 chars) → ALWAYS box them (tier 1 or 2), never raw
# Purple box: fill_color="#1a1130", fill_opacity=0.8, stroke_color=VIOLET, stroke_width=1.5, corner_radius=0.08

# ── Alive Standard (LOCKED — from Production Bible) ──
# Nothing static. Nothing linear. Everything breathes.
ALIVE = {
    "glow":  {"stroke_width": 6, "opacity": 0.15, "when": "Behind EVERY key mobject"},
    "bloom": {"peak": 0.35, "rest": 0.15, "dur": 0.2, "when": "Key reveals, 'oh' moments"},
    "sparks": {"radius": 0.03, "opacity": 0.6, "when": "Formula reveals, convergence"},
    "dim":   {"opacity_range": (0.15, 0.3), "when": "Background/inactive elements"},
    "easing": "smooth",  # EVERYTHING. Nothing linear.
}
# Alive fillers for holds > 2s:
#   Option 1: Glow pulse cycle (boxed content) — peak 0.25, rest 0.15, up 0.3s, down 0.7s
#   Option 2: Subtle drift (standalone equations) — shift UP*0.05, there_and_back
#   Option 3: Opacity breathe (background) — 1.0 → 0.6 → 1.0

# ── Dynamic Motion Standard (LOCKED — from Production Bible) ──
# "If the math moves, the visual moves."
# Static equations explain. Moving visuals CONVINCE.
# Anti-pattern: showing a static boxed equation when the concept involves movement.

# ── Branding (LOCKED) ──
BRANDING = {
    "school": "MERIDIAN MATH × ORBITAL",  # NOT "Coastal Alabama"
    "watermark": "ORBITAL",
    "tagline": "Watch it click.",
    "watermark_opacity": 0.25,
    "watermark_font_size": {"short": 10, "landscape": 14},
}

# ── Graph Standard (LOCKED — from Welcome Videos) ──
# Axes: nearly invisible, NOT the star
# Curves: prominent, the STAR
# Grid: hand-made neon lines OR very faint NumberPlane
GRAPH_STYLE = {
    "axis_color": "#333333",       # Nearly invisible
    "axis_stroke_width": 1,        # Thin
    "axis_opacity": 1.0,           # Full but dark color makes it subtle
    "axis_font_size": 12,
    "axis_numbers_exclude": [0],
    "curve_stroke_width": 3,       # The star
    "neon_grid_color": VIOLET,
    "neon_grid_stroke_width": 0.3,
    "neon_grid_opacity": 0.2,
    "neon_grid_spacing": 0.6,
    "tracer_color": NEON_GREEN,
    "tracer_radius": 0.08,
    "tracer_glow_factor": 2.0,
}

# ── TTS Profiles ──
ELEVENLABS_MODEL = "eleven_turbo_v2_5"
ALLISON_VOICE_ID = "5jVVMAv2LzffTcLGarKh"
TTS_OUTPUT_FORMAT = "mp3_44100_128"
TTS_NORMALIZE_DB = -26.0

TTS_PROFILES = {
    "short": {
        "stability": 0.50,
        "similarity_boost": 0.75,
        "style": 0.30,
        "speed": 0.97,
        "description": "Punchy, high energy, hook-oriented",
    },
    "lesson": {
        "stability": 0.50,
        "similarity_boost": 0.75,
        "style": 0.25,
        "speed": 0.90,
        "description": "Patient tutorial pace, 'let me show you'",
    },
    "problem": {
        "stability": 0.50,
        "similarity_boost": 0.75,
        "style": 0.20,
        "speed": 0.93,
        "description": "Focused, step-by-step, minimal preamble",
    },
    "longform": {
        "stability": 0.55,
        "similarity_boost": 0.75,
        "style": 0.25,
        "speed": 0.87,
        "description": "Conversational lecture, pauses for emphasis",
    },
}

# ── Audio Mix (LOCKED) ──
BG_VOLUME = 0.12
BG_FADE_IN = 2.0
BG_FADE_OUT = 3.0

# ── Video Type Metadata ──
VIDEO_TYPES = {
    "short": {
        "label": "YouTube Short",
        "layout": "short",
        "duration_range": (45, 90),
        "tts_profile": "short",
    },
    "lesson": {
        "label": "Lesson Video",
        "layout": "landscape",
        "duration_range": (180, 480),
        "tts_profile": "lesson",
        "sub_types": ["A", "B", "C"],
    },
    "problem": {
        "label": "Problem Walkthrough",
        "layout": "landscape",
        "duration_range": (60, 180),
        "tts_profile": "problem",
    },
    "longform": {
        "label": "Long-form Lecture",
        "layout": "landscape",
        "duration_range": (600, 1800),
        "tts_profile": "longform",
    },
}

# ── Topic Categories ──
TOPICS = {
    "functions":    {"label": "Functions",               "chapters": [1]},
    "polynomial":   {"label": "Polynomials",             "chapters": [2]},
    "rational":     {"label": "Rational Functions",      "chapters": [3]},
    "exponential":  {"label": "Exponential & Logarithmic", "chapters": [4, 5]},
    "trigonometry": {"label": "Trigonometry",            "chapters": [6, 7, 8]},
    "algebra":      {"label": "Algebra Fundamentals",    "chapters": []},
    "calculus":     {"label": "Calculus",                "chapters": []},
    "graphs":       {"label": "Graph Tools",             "chapters": []},
}
