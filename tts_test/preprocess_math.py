"""
Math Narration Preprocessor
Fixes common TTS pronunciation issues before sending to any TTS engine.
"""

import re

def preprocess_math_narration(text: str) -> str:
    """
    Fix common math pronunciation issues for TTS engines.
    Run this on narration text BEFORE sending to TTS.
    """
    
    # Differential notation - must be spelled out
    # "du" → "d u", "dx" → "d x", etc.
    differentials = ['du', 'dx', 'dy', 'dt', 'dz', 'dw', 'dr', 'dθ']
    for diff in differentials:
        # Match as whole word or at word boundary
        pattern = rf'\b{diff}\b'
        replacement = f"{diff[0]} {diff[1]}"
        text = re.sub(pattern, replacement, text, flags=re.IGNORECASE)
    
    # Also handle "with respect to u" patterns
    text = re.sub(r'respect to ([a-z])\b', r'respect to \1', text)
    
    # Common math terms that TTS might mispronounce
    replacements = {
        # Logs
        r'\bln\b': 'natural log',
        r'\blog\b': 'log',
        
        # Trig (usually fine, but ensure consistency)
        r'\bsin\b': 'sine',
        r'\bcos\b': 'cosine', 
        r'\btan\b': 'tangent',
        r'\bsec\b': 'secant',
        r'\bcsc\b': 'cosecant',
        r'\bcot\b': 'cotangent',
        
        # Greek letters (if written as text)
        r'\btheta\b': 'theta',
        r'\balpha\b': 'alpha',
        r'\bbeta\b': 'beta',
        r'\bgamma\b': 'gamma',
        r'\bdelta\b': 'delta',
        r'\bpi\b': 'pie',
        
        # Operators
        r'\bwrt\b': 'with respect to',
        r'\bw\.r\.t\.?\b': 'with respect to',
        
        # Notation - handle variables with exponents
        r'([a-z])\^2\b': r'\1 squared',
        r'([a-z])\^3\b': r'\1 cubed',
        r'([a-z])\^4\b': r'\1 to the fourth',
        r'([a-z])\^5\b': r'\1 to the fifth',
    }
    
    for pattern, replacement in replacements.items():
        text = re.sub(pattern, replacement, text, flags=re.IGNORECASE)
    
    # Clean up any double spaces
    text = re.sub(r'\s+', ' ', text).strip()
    
    return text


def test_preprocessor():
    """Test cases for the preprocessor."""
    
    test_cases = [
        ("Let u equal x squared, then du equals 2x dx.", 
         "Let u equal x squared, then d u equals 2x d x."),
        
        ("The integral of ln(x) dx",
         "The integral of natural log(x) d x"),
        
        ("Find the derivative wrt x",
         "Find the derivative with respect to x"),
        
        ("du equals 3x^2 dx",
         "d u equals 3x squared d x"),
    ]
    
    print("Testing math narration preprocessor:\n")
    
    all_passed = True
    for original, expected in test_cases:
        result = preprocess_math_narration(original)
        passed = result == expected
        status = "✅" if passed else "❌"
        
        print(f"{status} Input:    {original}")
        print(f"   Output:   {result}")
        if not passed:
            print(f"   Expected: {expected}")
            all_passed = False
        print()
    
    return all_passed


if __name__ == "__main__":
    test_preprocessor()
