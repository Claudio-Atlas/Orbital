"""
Orbital Problem Parser
======================
Uses LLM to convert a math problem into step-by-step JSON for video generation.
Supports: GPT-4o, DeepSeek-R1
"""

import os
import json
from openai import OpenAI

# Import sanitization (protects against prompt injection)
from utils.sanitize import sanitize_problem_input, sanitize_image_input

# === PROVIDER CONFIG ===
# Set ORBITAL_PROVIDER to "deepseek" or "openai" (default: deepseek)
PROVIDER = os.environ.get("ORBITAL_PROVIDER", "deepseek").lower()

# Lazy initialization to avoid crashes on missing keys
client = None
openai_client = None
MODEL = None

def get_client():
    """Get the main LLM client (DeepSeek or OpenAI)"""
    global client, MODEL
    if client is None:
        if PROVIDER == "deepseek":
            api_key = os.environ.get("DEEPSEEK_API_KEY")
            if not api_key:
                raise ValueError("DEEPSEEK_API_KEY not set")
            client = OpenAI(
                api_key=api_key,
                base_url="https://api.deepseek.com"
            )
            MODEL = "deepseek-chat"  # DeepSeek-V3 (fast, cheap, great at math)
            print("🧠 Using DeepSeek-V3")
        else:
            api_key = os.environ.get("OPENAI_API_KEY")
            if not api_key:
                raise ValueError("OPENAI_API_KEY not set")
            client = OpenAI(api_key=api_key)
            MODEL = "gpt-4o"
            print("🧠 Using GPT-4o")
    return client, MODEL

def get_openai_client():
    """Get OpenAI client for vision tasks (image parsing)"""
    global openai_client
    if openai_client is None:
        api_key = os.environ.get("OPENAI_API_KEY")
        if not api_key:
            raise ValueError("OPENAI_API_KEY not set - required for image parsing")
        openai_client = OpenAI(api_key=api_key)
    return openai_client

SYSTEM_PROMPT = """You are a patient math tutor creating step-by-step video explanations for students who need to SEE every calculation.

Given a math problem, break it down into very detailed steps. Show ALL intermediate work — never skip arithmetic or algebra.

Return ONLY valid JSON in this exact format:
{
  "meta": {
    "topic": "Brief topic name",
    "difficulty": "easy|medium|hard",
    "latex": "The original problem in LaTeX notation (for verification display)"
  },
  "steps": [
    {
      "narration": "Spoken explanation (conversational, like talking to a student)",
      "latex": "LaTeX math expression to display"
    }
  ]
}

CRITICAL RULES — READ CAREFULLY:

1. SHOW ALL WORK: Never skip intermediate calculations. If you multiply 2 × 3, show "2 × 3 = 6" not just "6".

2. For derivatives using power rule, ALWAYS show:
   - The rule being applied: "bring down the exponent and reduce by one"
   - The multiplication: "3 times 2 gives us 6"
   - The full transformation: "3x² becomes 3 · 2 · x^(2-1) = 6x"

3. For algebra, show BOTH sides of every operation:
   - "Add 5 to both sides: 2x - 5 + 5 = 11 + 5"
   - "This gives us 2x = 16"

4. Numbers in narration: Write as words ("two x squared" not "2x²")

5. Be conversational: "Let's..." "Now we..." "Notice that..."

6. Each step = ONE operation. Don't combine multiple operations.

EXAMPLE — "Find the derivative of 2x³ + 5x":
{
  "meta": {"topic": "Derivatives using Power Rule", "difficulty": "easy", "latex": "\\\\frac{d}{dx}(2x^3 + 5x)"},
  "steps": [
    {"narration": "Let's find the derivative of two x cubed plus five x.", "latex": "f(x) = 2x^3 + 5x"},
    {"narration": "We'll use the power rule: bring down the exponent as a coefficient, then reduce the exponent by one.", "latex": "\\\\text{Power Rule: } \\\\frac{d}{dx}(x^n) = n \\\\cdot x^{n-1}"},
    {"narration": "For two x cubed, we bring down the three and multiply it by the two.", "latex": "2x^3 \\\\rightarrow 2 \\\\cdot 3 \\\\cdot x^{3-1}"},
    {"narration": "Two times three is six, and three minus one is two. So we get six x squared.", "latex": "2 \\\\cdot 3 \\\\cdot x^{3-1} = 6x^2"},
    {"narration": "For five x, remember that x is the same as x to the first power.", "latex": "5x = 5x^1"},
    {"narration": "Bring down the one and multiply by five. One times five is five.", "latex": "5x^1 \\\\rightarrow 5 \\\\cdot 1 \\\\cdot x^{1-1}"},
    {"narration": "And x to the zero power is just one, so we get five.", "latex": "5 \\\\cdot 1 \\\\cdot x^0 = 5 \\\\cdot 1 = 5"},
    {"narration": "Putting it all together, the derivative is six x squared plus five.", "latex": "f'(x) = 6x^2 + 5"}
  ]
}

Remember: Students are watching because they're confused. Show EVERY step. More steps = better understanding.
"""


def parse_problem(problem_text: str) -> dict:
    """
    Convert a math problem into step-by-step JSON.
    
    Args:
        problem_text: The math problem (e.g., "Solve 2x + 5 = 11")
        
    Returns:
        dict with 'meta' and 'steps' keys
    """
    # Sanitize input before sending to AI
    sanitized_problem, warning = sanitize_problem_input(problem_text)
    if warning:
        print(f"[Sanitizer] Warning: {warning}")
    
    llm_client, model = get_client()
    
    response = llm_client.chat.completions.create(
        model=model,
        messages=[
            {"role": "system", "content": SYSTEM_PROMPT},
            {"role": "user", "content": f"Create a step-by-step video script for this problem:\n\n{sanitized_problem}"}
        ],
        temperature=0.3,  # Lower = more consistent
    )
    
    content = response.choices[0].message.content
    
    # DeepSeek-R1 sometimes wraps JSON in markdown code blocks
    if content.startswith("```"):
        # Extract JSON from code block
        lines = content.split("\n")
        json_lines = []
        in_block = False
        for line in lines:
            if line.startswith("```json"):
                in_block = True
                continue
            elif line.startswith("```"):
                in_block = False
                continue
            elif in_block:
                json_lines.append(line)
        content = "\n".join(json_lines)
    
    result = json.loads(content)
    
    # Validate structure
    if "steps" not in result:
        raise ValueError("Parser did not return steps")
    
    if len(result["steps"]) == 0:
        raise ValueError("Parser returned empty steps")
    
    # Add default meta if missing
    if "meta" not in result:
        result["meta"] = {"topic": "Math Problem", "difficulty": "medium"}
    
    return result


def parse_problem_from_image(image_base64: str) -> tuple[dict, str]:
    """
    Extract a math problem from an image and convert to steps.
    Uses GPT-4o Vision for image understanding.
    
    Args:
        image_base64: Base64-encoded image data
        
    Returns:
        tuple of (dict with 'meta' and 'steps' keys, extracted problem text)
    """
    
    # Sanitize image input first
    sanitized_image = sanitize_image_input(image_base64)
    
    # First, extract the problem from the image (always use OpenAI for vision)
    vision_client = get_openai_client()
    extract_response = vision_client.chat.completions.create(
        model="gpt-4o",
        messages=[
            {
                "role": "user",
                "content": [
                    {
                        "type": "text",
                        "text": "Extract the math problem from this image. Return ONLY the problem text, nothing else. If there are multiple problems, return only the first one."
                    },
                    {
                        "type": "image_url",
                        "image_url": {
                            "url": f"data:image/jpeg;base64,{sanitized_image}"
                        }
                    }
                ]
            }
        ],
        max_tokens=500
    )
    
    problem_text = extract_response.choices[0].message.content.strip()
    
    # Now parse it into steps (uses configured provider)
    return parse_problem(problem_text), problem_text


if __name__ == "__main__":
    # Test the parser
    import sys
    
    if len(sys.argv) > 1:
        problem = " ".join(sys.argv[1:])
    else:
        problem = "Solve for x: 3x - 7 = 14"
    
    print(f"Problem: {problem}\n")
    
    result = parse_problem(problem)
    print(json.dumps(result, indent=2))
