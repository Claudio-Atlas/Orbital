"""
Emotion Marker Utilities
========================
Fish Audio uses inline markers like (excited) or (calm) to control emotion.
These markers are NOT spoken - they're control signals.

For timing calculations, we need to strip them out.
For TTS, we keep them in.
"""

import re
from typing import Tuple

# All Fish Audio emotion markers (64+)
# These are stripped before timing calculation but kept for TTS
EMOTION_PATTERN = re.compile(
    r'\('
    r'(?:'
    # Basic emotions (24)
    r'angry|sad|excited|surprised|satisfied|delighted|'
    r'scared|worried|upset|nervous|frustrated|depressed|'
    r'empathetic|embarrassed|disgusted|moved|proud|relaxed|'
    r'grateful|confident|interested|curious|confused|joyful|'
    # Advanced emotions (25)
    r'disdainful|unhappy|anxious|hysterical|indifferent|'
    r'impatient|guilty|scornful|panicked|furious|reluctant|'
    r'keen|disapproving|negative|denying|astonished|serious|'
    r'sarcastic|conciliative|comforting|sincere|sneering|'
    r'hesitating|yielding|painful|awkward|amused|'
    # Tone markers (5)
    r'in a hurry tone|shouting|screaming|whispering|soft tone|'
    # Audio effects (10)
    r'laughing|chuckling|sobbing|crying loudly|sighing|'
    r'panting|groaning|crowd laughing|background laughter|audience laughing|'
    # Common teaching emotions we'll use
    r'calm|encouraging|thoughtful|cheerful|warm|patient|gentle'
    r')'
    r'\)\s*',
    re.IGNORECASE
)


def strip_emotion_markers(text: str) -> str:
    """
    Remove all Fish Audio emotion markers from text.
    
    Use this for:
    - Timing calculations (chars → minutes)
    - Manim animation duration
    - Display to user (if showing transcript)
    
    Args:
        text: Narration text possibly containing emotion markers
        
    Returns:
        Text with all emotion markers removed
        
    Example:
        >>> strip_emotion_markers("(excited) And the answer is five!")
        "And the answer is five!"
    """
    return EMOTION_PATTERN.sub('', text).strip()


def count_spoken_chars(text: str) -> int:
    """
    Count characters that will actually be spoken (excluding emotion markers).
    
    Args:
        text: Narration text possibly containing emotion markers
        
    Returns:
        Character count of spoken text only
    """
    return len(strip_emotion_markers(text))


def count_total_narration_chars(steps: list) -> Tuple[int, int]:
    """
    Count narration characters from a list of steps.
    
    Args:
        steps: List of step dicts with 'narration' keys
        
    Returns:
        Tuple of (spoken_chars, total_chars_with_markers)
        
    Example:
        >>> steps = [{"narration": "(calm) Let's begin..."}, ...]
        >>> spoken, total = count_total_narration_chars(steps)
        >>> print(f"Spoken: {spoken}, Total: {total}")
    """
    spoken_chars = 0
    total_chars = 0
    
    for step in steps:
        narration = step.get("narration", "")
        total_chars += len(narration)
        spoken_chars += count_spoken_chars(narration)
    
    return spoken_chars, total_chars


# Recommended emotions for math tutoring videos
TEACHING_EMOTIONS = {
    "intro": "(calm)",           # Starting explanations
    "question": "(curious)",      # Posing questions
    "reveal": "(excited)",        # Showing answers
    "encourage": "(encouraging)", # When it's tricky
    "warning": "(thoughtful)",    # Common mistakes
    "conclusion": "(satisfied)",  # Wrapping up
    "celebrate": "(cheerful)",    # Final answer
}


if __name__ == "__main__":
    # Test the utilities
    test_cases = [
        "(excited) And the answer is five!",
        "(calm) Let's think about this. (curious) What do we know?",
        "No emotions here, just plain text.",
        "(laughing) That's a great question! (thoughtful) Let me explain...",
    ]
    
    for text in test_cases:
        stripped = strip_emotion_markers(text)
        print(f"Original: {text}")
        print(f"Stripped: {stripped}")
        print(f"Chars: {len(text)} → {len(stripped)}")
        print()
