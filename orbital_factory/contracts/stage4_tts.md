# Stage 4: Text-to-Speech — Contract
**Owner:** Fourier
**Last Updated:** 2026-03-02

---

## Purpose
Convert the narration text from all script steps into a single combined audio track with proper timing, ready for Stage 5 (Manim render).

## Key Design: Single-Call SSML Approach

Instead of making one API call per step (21 calls for a 21-step video = slow and expensive), we batch all narration into **1-3 API calls** using SSML breaks between steps.

### What is SSML?
SSML (Speech Synthesis Markup Language) is XML markup that controls TTS output:
```xml
<speak>
  Step one narration here.
  <break time="2.0s"/>
  Step two narration here.
  <break time="1.5s"/>
  Step three narration here.
</speak>
```

The `<break>` tags insert silence between steps. We then use the **timestamps API** to get character-level timing, and split the audio at the break points using pydub.

### Why 1-3 Calls Instead of 1?
ElevenLabs has a **5,000 character limit** per request. A typical 20-step script is ~3,000-8,000 characters of narration. So:
- Short videos (quick detail): 1 call
- Standard videos: 2 calls
- Detailed videos: 2-3 calls

## Provider Abstraction

The TTS system MUST be provider-agnostic. All provider-specific logic lives behind a common interface so we can swap providers without touching the pipeline.

### TTS Provider Interface

```python
class TTSProvider:
    """Abstract base for TTS providers."""
    
    name: str                    # "elevenlabs", "fish_audio", "openai", etc.
    max_chars: int               # Per-request character limit
    supports_ssml: bool          # Can it handle <break> tags?
    supports_timestamps: bool    # Can it return word/char timing?
    
    def generate(
        self,
        text: str,               # Plain text or SSML
        voice_id: str,
        output_path: str,
        speed: float = 1.0,
    ) -> TTSResult:
        """Generate audio for the given text."""
        ...
    
    def generate_with_timestamps(
        self,
        text: str,
        voice_id: str,
        output_path: str,
        speed: float = 1.0,
    ) -> TTSResultWithTimestamps:
        """Generate audio + character-level timestamps."""
        ...
```

```python
@dataclass
class TTSResult:
    audio_path: str              # Path to output mp3/wav
    duration_ms: int             # Total audio duration
    cost_estimate: float         # Estimated cost of this call

@dataclass
class TTSResultWithTimestamps:
    audio_path: str
    duration_ms: int
    cost_estimate: float
    timestamps: list[dict]       # [{char_index, time_ms}, ...]
```

### Supported Providers

| Provider | Status | Voice | SSML | Timestamps | Cost/1K chars |
|----------|--------|-------|------|------------|---------------|
| **ElevenLabs** | ✅ Active | Allison (tutorial), Hale (marketing) | ✅ `<break>` | ✅ `with-timestamps` | $0.08-0.10/1K chars |
| **Fish Audio** | ❌ Blocked (needs business bank) | TBD | ❌ | ❌ | ~$0.015 |
| **OpenAI TTS** | 🔜 Planned | nova, alloy, etc. | ❌ | ❌ | ~$0.015 |
| **Local (Piper)** | 🔜 Future (Mac Mini #2) | Custom | ❌ | ❌ | Free |

### Fallback Strategy
If the primary provider fails:
1. Retry once with same provider
2. Fall back to next provider in priority list
3. If all fail, flag for manual intervention

### Provider Selection
```python
# In pipeline config
tts_config = {
    "provider": "elevenlabs",          # Active provider
    "fallback": "openai",              # Fallback provider
    "voice_id": "5jVVMAv2LzffTcLGarKh",  # Allison (tutorial)
    "marketing_voice_id": "wWWn96OtTHu1sn8SRGEr",  # Hale
    "speed": 1.0,
}
```

## Process

### Step 1: Extract Narration
From the revised script, extract all `narration` fields in step order:
```python
narrations = [step["narration"] for step in script["steps"]]
```

### Step 2: Build SSML Chunks
Group narrations into chunks that fit within the provider's character limit.

```python
def build_ssml_chunks(narrations, max_chars=5000, break_time="1.5s"):
    chunks = []
    current = "<speak>"
    for i, text in enumerate(narrations):
        addition = f'{text} <break time="{break_time}"/>'
        if len(current) + len(addition) > max_chars - 10:
            current += "</speak>"
            chunks.append(current)
            current = f"<speak>{addition}"
        else:
            current += addition
    current += "</speak>"
    chunks.append(current)
    return chunks
```

**Break times by step type:**
| Step Type | Break After |
|-----------|------------|
| text, math, mixed | 1.5s |
| transform | 1.0s |
| box (final answer) | 2.0s |
| graph, diagram | 2.0s |
| intro/outro | 3.0s |

### Step 3: Generate Audio
For each chunk, call the provider's `generate_with_timestamps()`.

### Step 4: Split by Step
Using timestamps from the API response, split the combined audio at break points to get individual step audio segments.

```python
from pydub import AudioSegment

def split_audio_by_timestamps(audio_path, break_positions_ms):
    audio = AudioSegment.from_mp3(audio_path)
    segments = []
    prev = 0
    for pos in break_positions_ms:
        segments.append(audio[prev:pos])
        prev = pos
    segments.append(audio[prev:])
    return segments
```

### Step 5: Build Combined Track
Concatenate step audio segments with inter-step silence (configurable):

```python
def build_combined_audio(segments, inter_step_silence_ms=800, final_hold_ms=3000):
    silence = AudioSegment.silent(duration=inter_step_silence_ms)
    combined = AudioSegment.empty()
    for i, seg in enumerate(segments):
        combined += seg
        if i < len(segments) - 1:
            combined += silence
    combined += AudioSegment.silent(duration=final_hold_ms)
    combined.export("output/combined_audio.mp3", format="mp3", bitrate="192k")
    return combined
```

### Step 6: Generate Timing Map
Output a timing map that tells Stage 5 (Manim) when each step's audio starts:

```json
{
  "step_timings": [
    {"step": 0, "start_ms": 0, "duration_ms": 4200},
    {"step": 1, "start_ms": 5000, "duration_ms": 6100},
    {"step": 2, "start_ms": 11900, "duration_ms": 3800}
  ],
  "total_duration_ms": 232000
}
```

## Input

From Stage 3:
```json
{
  "revised_script": "<script JSON with narration fields>",
  "verification": { ... },
  "tts_config": {
    "provider": "elevenlabs",
    "voice_id": "5jVVMAv2LzffTcLGarKh",
    "speed": 1.0
  }
}
```

## Output

To Stage 5:
```json
{
  "revised_script": "<unchanged>",
  "verification": { ... },
  "audio": {
    "combined_path": "output/{slug}_combined_audio.mp3",
    "step_segments": ["output/audio/step_00.mp3", ...],
    "timing_map": { ... },
    "total_duration_ms": 232000,
    "provider_used": "elevenlabs",
    "voice_used": "Allison",
    "api_calls": 2,
    "total_chars": 4200
  }
}
```

## Voice Profiles

| Profile | Voice | Provider | Voice ID | Settings | Use Case |
|---------|-------|----------|----------|----------|----------|
| **Tutorial** | Allison | ElevenLabs | `5jVVMAv2LzffTcLGarKh` | stability: 0.7, similarity: 0.75 | Math walkthrough videos |
| **Marketing** | Hale | ElevenLabs | `wWWn96OtTHu1sn8SRGEr` | stability: 0.55, similarity: 0.65, style: 0.25, speed: 0.8 | Sizzle reels, promos |

**LOCKED (Clayton approved 2026-03-02):** Hale marketing voice settings. Generate all lines in ONE call for consistent tone.

## Cost Estimate

| Detail Level | ~Chars | API Calls | Cost (ElevenLabs) |
|---|---|---|---|
| Quick (90s) | ~1,500 | 1 | ~$0.12 |
| Standard (3-4min) | ~3,500 | 1 | ~$0.28 |
| Detailed (6+min) | ~7,000 | 2 | ~$0.56 |

## Known Issues

- **Manim `add_sound()` is unreliable** for multiple audio clips. ALWAYS use ffmpeg post-merge (Stage 5 handles this).
- **ElevenLabs 5,000 char limit** — chunking logic must handle gracefully.
- **Fish Audio blocked** on business bank account — revisit when account is set up.

---

## Future: Proof Templates (from Stage 3)
*Noted for future optimization:* Build reusable Lean templates for common calc problems (derivative, integral, intersection verification) to reduce Opus calls at scale.

---

## Integration Notes

- Stage 4 receives: revised script + verification metadata from Stage 3
- Stage 4 outputs to: Stage 5 (Manim) with combined audio + timing map
- Step timing map is critical — Stage 5 uses it to sync animations with narration
- Provider can be swapped in config without touching pipeline logic
