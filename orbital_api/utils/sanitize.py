"""
Input Sanitization
==================
Protects the AI from prompt injection and malicious inputs.

This module validates and cleans user input BEFORE sending to AI APIs.

Threat Model:
1. Prompt Injection - "Ignore previous instructions and..."
2. Jailbreak Attempts - Trying to make AI bypass safety
3. Cost Attacks - Extremely long inputs to waste API credits
4. Non-Math Content - Requests that aren't math problems
5. Script Injection - HTML/JS that could cause issues
"""

import re
from typing import Tuple, Optional
from fastapi import HTTPException


# ============================================
# Configuration
# ============================================

MAX_PROBLEM_LENGTH = 2000  # Characters
MAX_LINES = 20  # Maximum line breaks
MIN_PROBLEM_LENGTH = 3  # Minimum to be a real problem

# Patterns that suggest prompt injection
INJECTION_PATTERNS = [
    # Direct instruction overrides
    r"ignore\s+(all\s+)?(previous|prior|above)?\s*(instructions?|prompts?|rules?)",
    r"ignore\s+all\s+rules?",
    r"disregard\s+(all\s+)?(previous|prior|above)",
    r"forget\s+(everything|all|what)\s+(you|i)\s+(said|told|know)",
    r"new\s+instructions?:",
    r"system\s*prompt",
    r"you\s+are\s+now",
    r"act\s+as\s+(if|a)",
    r"pretend\s+(you|to)\s+(are|be)",
    r"roleplay\s+as",
    
    # Jailbreak patterns
    r"do\s+anything\s+now",
    r"dan\s+mode",
    r"developer\s+mode",
    r"jailbreak",
    r"bypass\s+(filter|safety|restriction)",
    
    # Information extraction
    r"(what|show|tell|reveal|display)\s+(me\s+)?(your|the)\s+(system|initial|original)\s+(prompt|instructions?)",
    r"repeat\s+(your|the)\s+(system|initial)\s+(prompt|instructions?)",
    r"(api|secret)\s*key",
    
    # Output manipulation
    r"respond\s+(only\s+)?with",
    r"output\s+(only|just)",
    r"print\s+(only|just)",
]

# Compile patterns for efficiency
COMPILED_INJECTION_PATTERNS = [
    re.compile(pattern, re.IGNORECASE) 
    for pattern in INJECTION_PATTERNS
]

# Patterns that suggest this isn't a math problem
NON_MATH_PATTERNS = [
    r"write\s+(me\s+)?(a|an)\s+(story|essay|poem|article|code|script|email)",
    r"(hack|attack|exploit|steal)",
    r"(password|credit\s*card|ssn|social\s*security)",
    r"(kill|murder|harm|hurt|attack)\s+(someone|people|a\s+person)",
]

COMPILED_NON_MATH_PATTERNS = [
    re.compile(pattern, re.IGNORECASE)
    for pattern in NON_MATH_PATTERNS
]

# Characters/patterns to strip (but not reject)
STRIP_PATTERNS = [
    (r"<script[^>]*>.*?</script>", ""),  # Script tags
    (r"<[^>]+>", ""),  # HTML tags
    (r"javascript:", ""),  # JS protocol
    (r"on\w+\s*=", ""),  # Event handlers
]


# ============================================
# Normalization (for bypass protection)
# ============================================

def normalize_for_detection(text: str) -> str:
    """
    Normalize text to catch bypass attempts.
    - Converts Unicode lookalikes to ASCII  
    - Lowercases
    - Returns BOTH the normal text AND a space-stripped version for checking
    
    Note: We check both the normal text and a version with spaces removed
    to catch "i g n o r e" style bypasses.
    """
    import unicodedata
    
    # Normalize Unicode (NFKC converts lookalikes to standard forms)
    text = unicodedata.normalize('NFKC', text)
    
    return text.lower()


def check_injection_patterns(text: str) -> bool:
    """
    Check for injection patterns in both normal and space-collapsed text.
    Returns True if injection detected.
    """
    normalized = normalize_for_detection(text)
    
    # Also create a version with no spaces (catches "i g n o r e")
    no_spaces = normalized.replace(' ', '')
    
    # Check normal text with normal patterns
    for pattern in COMPILED_INJECTION_PATTERNS:
        if pattern.search(normalized):
            return True
    
    # Check no-spaces text with space-optional patterns
    # Convert \s+ to optional/empty for no-space matching
    for pattern_str in INJECTION_PATTERNS:
        # Replace \s+ with nothing for the no-space version
        no_space_pattern_str = re.sub(r'\\s\+', '', pattern_str)
        no_space_pattern_str = re.sub(r'\\s\*', '', no_space_pattern_str)
        try:
            no_space_pattern = re.compile(no_space_pattern_str, re.IGNORECASE)
            if no_space_pattern.search(no_spaces):
                return True
        except re.error:
            # Skip invalid patterns
            pass
    
    return False


# ============================================
# Main Sanitization Function
# ============================================

def sanitize_problem_input(problem: str) -> Tuple[str, Optional[str]]:
    """
    Sanitize user problem input before sending to AI.
    
    Args:
        problem: Raw user input
        
    Returns:
        Tuple of (sanitized_problem, warning_message)
        - sanitized_problem: Cleaned input safe to send to AI
        - warning_message: Optional warning (None if clean)
        
    Raises:
        HTTPException: If input is rejected (malicious or invalid)
    """
    
    if not problem:
        raise HTTPException(400, "Problem text is required")
    
    # Strip whitespace
    problem = problem.strip()
    
    # Check minimum length
    if len(problem) < MIN_PROBLEM_LENGTH:
        raise HTTPException(400, "Problem is too short. Please enter a complete math problem.")
    
    # Check maximum length
    if len(problem) > MAX_PROBLEM_LENGTH:
        raise HTTPException(
            400, 
            f"Problem is too long ({len(problem)} chars). Maximum is {MAX_PROBLEM_LENGTH} characters."
        )
    
    # Check line count (prevents wall-of-text attacks)
    line_count = problem.count('\n') + 1
    if line_count > MAX_LINES:
        raise HTTPException(
            400,
            f"Problem has too many lines ({line_count}). Maximum is {MAX_LINES} lines."
        )
    
    # Check for prompt injection patterns (using normalized text + space-stripped for bypass protection)
    if check_injection_patterns(problem):
        # Log this for security monitoring
        print(f"[SECURITY] Blocked prompt injection attempt in: {problem[:100]}...")
        raise HTTPException(
            400,
            "Your input contains patterns that aren't allowed. Please enter a valid math problem."
        )
    
    # Check for non-math content
    for pattern in COMPILED_NON_MATH_PATTERNS:
        if pattern.search(problem):
            raise HTTPException(
                400,
                "This doesn't look like a math problem. Please enter a mathematical question."
            )
    
    # Strip potentially dangerous content (but don't reject)
    warning = None
    cleaned = problem
    for pattern, replacement in STRIP_PATTERNS:
        if re.search(pattern, cleaned, re.IGNORECASE):
            cleaned = re.sub(pattern, replacement, cleaned, flags=re.IGNORECASE)
            warning = "Some formatting was removed from your input."
    
    # Normalize whitespace
    cleaned = re.sub(r'\s+', ' ', cleaned).strip()
    
    # Final sanity check
    if len(cleaned) < MIN_PROBLEM_LENGTH:
        raise HTTPException(
            400,
            "After cleaning, the problem is too short. Please enter a valid math problem."
        )
    
    return cleaned, warning


def sanitize_image_input(image_b64: str) -> str:
    """
    Sanitize base64 image input.
    
    Args:
        image_b64: Base64-encoded image data
        
    Returns:
        Validated base64 string
        
    Raises:
        HTTPException: If image is invalid
    """
    
    if not image_b64:
        raise HTTPException(400, "Image data is required")
    
    # Remove data URL prefix if present
    if image_b64.startswith("data:"):
        # Extract the base64 part
        if ";base64," in image_b64:
            image_b64 = image_b64.split(";base64,")[1]
        else:
            raise HTTPException(400, "Invalid image format")
    
    # Check length (rough size limit: ~10MB base64 = ~7.5MB image)
    MAX_IMAGE_SIZE = 10 * 1024 * 1024  # 10MB base64
    if len(image_b64) > MAX_IMAGE_SIZE:
        raise HTTPException(400, "Image is too large. Maximum size is ~7.5MB.")
    
    # Validate it's actually base64
    import base64
    try:
        decoded = base64.b64decode(image_b64, validate=True)
    except Exception:
        raise HTTPException(400, "Invalid base64 image data")
    
    # Check for minimum size (avoid tiny/empty images)
    if len(decoded) < 100:
        raise HTTPException(400, "Image is too small or empty")
    
    # Check magic bytes for valid image formats
    valid_headers = [
        b'\x89PNG',  # PNG
        b'\xff\xd8\xff',  # JPEG
        b'GIF87a',  # GIF
        b'GIF89a',  # GIF
        b'RIFF',  # WebP (starts with RIFF)
    ]
    
    is_valid = any(decoded.startswith(header) for header in valid_headers)
    if not is_valid:
        raise HTTPException(400, "Invalid image format. Supported: PNG, JPEG, GIF, WebP")
    
    return image_b64


# ============================================
# Utility Functions
# ============================================

def looks_like_math(text: str) -> bool:
    """
    Heuristic check if text looks like a math problem.
    
    This is a soft check - we don't reject based on this alone,
    but it can be used for warnings or logging.
    """
    
    # Math indicators
    math_patterns = [
        r'\d',  # Has numbers
        r'[+\-*/=<>]',  # Has operators
        r'[xyz]',  # Has common variables
        r'\b(solve|find|calculate|compute|evaluate|simplify|factor|derive|integrate)\b',
        r'\b(equation|function|polynomial|derivative|integral|limit|sum|product)\b',
        r'\b(sin|cos|tan|log|ln|sqrt|abs)\b',
        r'[²³√∫∑∏]',  # Math symbols
        r'\^',  # Exponent
        r'\\frac|\\sqrt|\\int',  # LaTeX
    ]
    
    for pattern in math_patterns:
        if re.search(pattern, text, re.IGNORECASE):
            return True
    
    return False


def estimate_complexity(problem: str) -> str:
    """
    Estimate the complexity of a math problem.
    Used for cost estimation and routing.
    
    Returns: "simple", "medium", or "complex"
    """
    
    # Complexity indicators
    complex_patterns = [
        r'\bprove\b',
        r'\binduction\b',
        r'\bintegral\b',
        r'\bderivative\b',
        r'\blimit\b',
        r'\bmatrix\b',
        r'\bvector\b',
        r'\bdifferential\b',
        r'\bpartial\b',
    ]
    
    medium_patterns = [
        r'\bsolve\s+for\b',
        r'\bfactor\b',
        r'\bsimplify\b',
        r'\bquadratic\b',
        r'\bpolynomial\b',
    ]
    
    text_lower = problem.lower()
    
    for pattern in complex_patterns:
        if re.search(pattern, text_lower):
            return "complex"
    
    for pattern in medium_patterns:
        if re.search(pattern, text_lower):
            return "medium"
    
    return "simple"
