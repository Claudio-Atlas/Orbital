"""
Orbital Verification Gate
Uses DeepSeek-Prover-V2-7B to formalize proofs, Lean 4 + Mathlib to verify them.

Usage:
    python verify_proof.py "Every group of order 15 is cyclic"
    python verify_proof.py --file scripts/group_order_15.json

Returns exit code 0 if verified, 1 if rejected.
"""

import subprocess
import sys
import json
import os
import re
import tempfile
import argparse

OLLAMA_URL = "http://localhost:11434/api/generate"
LEAN_VERIFIER_DIR = os.path.join(os.path.dirname(__file__), "lean_verifier")
ELAN_PATH = os.path.expanduser("~/.elan/bin")

FORMALIZE_PROMPT = """You are a formal mathematics expert. Given a mathematical claim, write a complete Lean 4 proof.

Rules:
- Start with `import Mathlib`
- Use Mathlib tactics (norm_num, simp, ring, omega, exact?, apply?, etc.)
- Do NOT use `sorry` — the proof must be complete
- Do NOT include any explanation, only Lean 4 code
- If you cannot prove it, say CANNOT_FORMALIZE

Claim: {claim}

```lean4
import Mathlib

"""

def ask_deepseek_prover(claim: str, attempts: int = 3) -> str | None:
    """Ask DeepSeek-Prover-V2-7B to formalize a claim into Lean 4."""
    import urllib.request
    
    prompt = FORMALIZE_PROMPT.format(claim=claim)
    
    for attempt in range(attempts):
        payload = json.dumps({
            "model": "deepseek-prover-v2",
            "prompt": prompt,
            "stream": False,
            "options": {
                "temperature": 0.1 * (attempt + 1),  # increase temp on retries
                "num_predict": 4096
            }
        }).encode()
        
        req = urllib.request.Request(
            OLLAMA_URL,
            data=payload,
            headers={"Content-Type": "application/json"}
        )
        
        try:
            with urllib.request.urlopen(req, timeout=180) as resp:
                result = json.loads(resp.read())
                code = result.get("response", "")
                
                if "CANNOT_FORMALIZE" in code:
                    print(f"  Attempt {attempt + 1}: Model says it cannot formalize this claim")
                    continue
                
                if "sorry" in code:
                    print(f"  Attempt {attempt + 1}: Model used 'sorry' (incomplete proof), retrying...")
                    continue
                
                # Extract lean code if wrapped in code blocks
                lean_match = re.search(r'```(?:lean4?)?\n(.*?)```', code, re.DOTALL)
                if lean_match:
                    code = lean_match.group(1)
                
                # Ensure it starts with import
                if not code.strip().startswith("import"):
                    code = "import Mathlib\n\n" + code
                
                return code.strip()
                
        except Exception as e:
            print(f"  Attempt {attempt + 1}: Error calling DeepSeek Prover: {e}")
            continue
    
    return None


def _run_lean(lean_code: str, timeout: int = 120) -> tuple[bool, str]:
    """Run Lean 4 on code. Returns (success, output)."""
    test_file = os.path.join(LEAN_VERIFIER_DIR, "Verifier", "_PipelineCheck.lean")
    
    try:
        with open(test_file, "w") as f:
            f.write(lean_code)
        
        env = os.environ.copy()
        env["PATH"] = ELAN_PATH + ":" + env.get("PATH", "")
        
        result = subprocess.run(
            ["lake", "env", "lean", "Verifier/_PipelineCheck.lean"],
            cwd=LEAN_VERIFIER_DIR,
            capture_output=True,
            text=True,
            timeout=timeout,
            env=env
        )
        
        output = (result.stderr or result.stdout).strip()
        
        if result.returncode == 0:
            # Check for exact? suggestions in output
            return True, output
        else:
            return False, output
            
    except subprocess.TimeoutExpired:
        return False, "Lean verification timed out"
    except Exception as e:
        return False, f"Lean error: {e}"
    finally:
        if os.path.exists(test_file):
            os.remove(test_file)


def verify_with_lean(lean_code: str) -> tuple[bool, str]:
    """
    Run Lean 4 on the code with exact? fallback.
    
    If the initial proof fails (e.g. hallucinated lemma name), automatically
    retries with exact?/apply? tactics to let Lean search Mathlib for the
    correct lemma. This adds a few seconds but catches cases where the prover
    model guesses wrong names.
    """
    
    # Guard against empty code (prevents false positives)
    stripped = lean_code.strip()
    if not stripped or stripped == "import Mathlib":
        return False, "Empty proof code — nothing to verify"
    
    # First try: run the proof as-is
    success, output = _run_lean(lean_code)
    if success:
        return True, "Proof verified successfully"
    
    # Check if failure is due to unknown identifier (hallucinated name)
    if "unknownIdentifier" in output or "Unknown identifier" in output or "unknown identifier" in output:
        print("  🔄 Hallucinated lemma name detected — trying exact? fallback...")
        
        # Replace the failing tactic line with exact?
        # Strategy: find lines with the hallucinated name and replace with exact?
        import re
        
        lines = lean_code.split("\n")
        # Find which identifier was hallucinated
        id_match = re.search(r"Unknown (?:identifier|constant) [`']([^`']+)", output)
        bad_name = id_match.group(1) if id_match else None
        
        if bad_name:
            # Replace lines containing the bad name with exact?
            new_lines = []
            for line in lines:
                if bad_name in line:
                    # Preserve indentation
                    indent = len(line) - len(line.lstrip())
                    new_lines.append(" " * indent + "exact?")
                else:
                    new_lines.append(line)
            
            exact_code = "\n".join(new_lines)
            success2, output2 = _run_lean(exact_code, timeout=60)
            
            if "Try this:" in output2:
                # exact? found the real lemma — extract and verify
                suggestion_match = re.search(r"exact (.+)", output2)
                if suggestion_match:
                    real_tactic = suggestion_match.group(1).strip()
                    print(f"  💡 Lean found: exact {real_tactic}")
                    
                    # Replace exact? with the real tactic
                    final_lines = []
                    for line in new_lines:
                        if line.strip() == "exact?":
                            indent = len(line) - len(line.lstrip())
                            final_lines.append(" " * indent + f"exact {real_tactic}")
                        else:
                            final_lines.append(line)
                    
                    final_code = "\n".join(final_lines)
                    success3, output3 = _run_lean(final_code)
                    if success3:
                        return True, f"Proof verified (auto-corrected: {bad_name} → {real_tactic})"
        
        # Also try apply? as a broader fallback
        fallback_lines = []
        for line in lines:
            if bad_name and bad_name in line:
                indent = len(line) - len(line.lstrip())
                fallback_lines.append(" " * indent + "apply?")
            else:
                fallback_lines.append(line)
        
        apply_code = "\n".join(fallback_lines)
        success4, output4 = _run_lean(apply_code, timeout=60)
        
        if "Try this:" in output4:
            suggestion_match = re.search(r"(exact|apply) (.+)", output4)
            if suggestion_match:
                real_tactic = suggestion_match.group(0).strip()
                print(f"  💡 Lean found: {real_tactic}")
                
                final_lines = []
                for line in fallback_lines:
                    if line.strip() == "apply?":
                        indent = len(line) - len(line.lstrip())
                        final_lines.append(" " * indent + real_tactic)
                    else:
                        final_lines.append(line)
                
                final_code = "\n".join(final_lines)
                success5, output5 = _run_lean(final_code)
                if success5:
                    return True, f"Proof verified (auto-corrected via apply?)"
    
    return False, output


def extract_claims_from_script(script_path: str) -> list[str]:
    """Extract mathematical claims from an Orbital proof script JSON."""
    with open(script_path) as f:
        script = json.load(f)
    
    claims = []
    
    # Look for the main theorem/claim
    if "theorem" in script:
        claims.append(script["theorem"])
    
    # Look for step-level claims
    for step in script.get("steps", []):
        if step.get("type") in ("claim", "theorem", "lemma"):
            claims.append(step.get("text", step.get("content", "")))
    
    # If no structured claims, try the title/description
    if not claims:
        title = script.get("title", script.get("name", ""))
        if title:
            claims.append(title)
    
    return [c for c in claims if c]


def main():
    parser = argparse.ArgumentParser(description="Orbital Proof Verification Gate")
    parser.add_argument("claim", nargs="?", help="Mathematical claim to verify")
    parser.add_argument("--file", "-f", help="Path to Orbital script JSON")
    parser.add_argument("--lean-only", help="Path to a .lean file to verify directly")
    parser.add_argument("--verbose", "-v", action="store_true")
    args = parser.parse_args()
    
    # Mode 1: Direct Lean file verification
    if args.lean_only:
        print(f"🔍 Verifying Lean file: {args.lean_only}")
        with open(args.lean_only) as f:
            code = f.read()
        success, output = verify_with_lean(code)
        if success:
            print("✅ VERIFIED")
        else:
            print(f"❌ REJECTED\n{output}")
        sys.exit(0 if success else 1)
    
    # Mode 2: Script file
    if args.file:
        claims = extract_claims_from_script(args.file)
        if not claims:
            print("⚠️  No verifiable claims found in script")
            sys.exit(1)
    elif args.claim:
        claims = [args.claim]
    else:
        parser.print_help()
        sys.exit(1)
    
    # Verify each claim
    all_passed = True
    results = []
    
    for i, claim in enumerate(claims, 1):
        print(f"\n{'='*60}")
        print(f"Claim {i}/{len(claims)}: {claim}")
        print(f"{'='*60}")
        
        # Step 1: Formalize with DeepSeek Prover
        print("\n📐 Formalizing with DeepSeek-Prover-V2-7B...")
        lean_code = ask_deepseek_prover(claim)
        
        if lean_code is None:
            print("❌ Could not formalize claim after 3 attempts")
            results.append({"claim": claim, "status": "formalization_failed"})
            all_passed = False
            continue
        
        if args.verbose:
            print(f"\nGenerated Lean code:\n{lean_code}\n")
        
        # Step 2: Verify with Lean 4
        print("🔍 Verifying with Lean 4 + Mathlib...")
        success, output = verify_with_lean(lean_code)
        
        if success:
            print("✅ VERIFIED — proof is mathematically valid")
            results.append({"claim": claim, "status": "verified", "lean_code": lean_code})
        else:
            print(f"❌ REJECTED — Lean found errors:")
            print(f"   {output[:500]}")
            results.append({"claim": claim, "status": "rejected", "error": output})
            all_passed = False
    
    # Summary
    print(f"\n{'='*60}")
    print(f"VERIFICATION SUMMARY")
    print(f"{'='*60}")
    verified = sum(1 for r in results if r["status"] == "verified")
    print(f"  {verified}/{len(results)} claims verified")
    
    if all_passed:
        print("  ✅ ALL CLAIMS VERIFIED — safe to proceed to rendering")
    else:
        print("  ❌ SOME CLAIMS FAILED — do NOT render this proof")
    
    sys.exit(0 if all_passed else 1)


if __name__ == "__main__":
    main()
