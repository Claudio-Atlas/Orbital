"""
Orbital Pipeline Stress Test
=============================
Submits a variety of math problems to test the full pipeline.
Run: python3 stress_test.py [--count N] [--sequential]

Requires: .env with SUPABASE_URL and SUPABASE_SERVICE_KEY
"""

import argparse, time, uuid, json, os
from dotenv import load_dotenv
load_dotenv()
from supabase import create_client

SUPABASE_URL = os.environ["SUPABASE_URL"]
SUPABASE_KEY = os.environ["SUPABASE_SERVICE_KEY"]
USER_ID = "1eb3f6e9-dae8-4b89-a58f-c11ce85be61d"

PROBLEMS = [
    # Derivatives
    {"problem": "Find the derivative of f(x) = x^3 - 4x^2 + 7x - 2"},
    {"problem": "Find the derivative of f(x) = sin(x) * cos(x)"},
    {"problem": "Use the chain rule to find the derivative of f(x) = (3x + 1)^5"},
    {"problem": "Find the derivative of f(x) = ln(x^2 + 1)"},
    # Integrals
    {"problem": "Evaluate the integral of 2x + 3 with respect to x"},
    {"problem": "Evaluate the definite integral of x^2 from 0 to 3"},
    {"problem": "Evaluate the integral of sin(x) dx"},
    # Limits
    {"problem": "Find the limit of (x^2 - 1)/(x - 1) as x approaches 1"},
    {"problem": "Find the limit of sin(x)/x as x approaches 0"},
    # Algebra
    {"problem": "Solve the equation 2x^2 - 5x + 3 = 0"},
    {"problem": "Factor the expression x^3 - 8"},
    # Trig
    {"problem": "Verify the identity sin^2(x) + cos^2(x) = 1"},
    {"problem": "Solve 2sin(x) - 1 = 0 for x in [0, 2pi]"},
    # Applications
    {"problem": "Find the equation of the tangent line to f(x) = x^2 at x = 3"},
    {"problem": "Find the critical points of f(x) = x^3 - 3x + 2"},
    # Edge cases
    {"problem": "Find the derivative of f(x) = 5", "detail_level": "quick"},
    {"problem": "Evaluate the integral of 1/x dx"},
    {"problem": "Find the derivative of f(x) = e^(x^2)", "detail_level": "detailed"},
]

def submit_job(sb, prob):
    job_id = str(uuid.uuid4())
    sb.table("video_jobs").insert({
        "id": job_id, "user_id": USER_ID, "problem": prob["problem"],
        "detail_level": prob.get("detail_level", "standard"),
        "path": "ai_review", "lean_requested": False, "status": "queued",
    }).execute()
    return job_id

def check_job(sb, job_id):
    r = sb.table("video_jobs").select("status,stage_detail,error,duration_seconds,cost_total").eq("id", job_id).execute()
    return r.data[0] if r.data else None

def run(count=None, sequential=False):
    sb = create_client(SUPABASE_URL, SUPABASE_KEY)
    problems = PROBLEMS[:count] if count else PROBLEMS
    print(f"\n🧪 Stress Test — {len(problems)} problems, {'sequential' if sequential else 'batch'}\n{'='*60}")

    if sequential:
        results = []
        for i, prob in enumerate(problems):
            print(f"\n[{i+1}/{len(problems)}] {prob['problem'][:60]}...")
            job_id = submit_job(sb, prob)
            start = time.time()
            while True:
                time.sleep(5)
                s = check_job(sb, job_id)
                elapsed = time.time() - start
                if s["status"] == "complete":
                    print(f"  ✅ {elapsed:.0f}s — {s['duration_seconds']}s video, ${s['cost_total']}")
                    results.append({"problem": prob["problem"], "ok": True, "time": elapsed, "cost": s["cost_total"]}); break
                elif s["status"] == "failed":
                    print(f"  ❌ {elapsed:.0f}s — {s['error'][:80]}")
                    results.append({"problem": prob["problem"], "ok": False, "error": s["error"]}); break
                elif elapsed > 600:
                    print(f"  ⏰ Timeout"); results.append({"problem": prob["problem"], "ok": False, "error": "timeout"}); break
    else:
        jobs = [(submit_job(sb, p), p["problem"]) for p in problems]
        print(f"  Queued {len(jobs)} jobs. Monitoring...")
        results, pending, start = [], set(range(len(jobs))), time.time()
        while pending and time.time() - start < 1800:
            time.sleep(10)
            for idx in list(pending):
                s = check_job(sb, jobs[idx][0])
                if s["status"] == "complete":
                    print(f"  ✅ [{idx+1}] {jobs[idx][1][:40]}... ${s['cost_total']}")
                    results.append({"problem": jobs[idx][1], "ok": True, "cost": s["cost_total"]}); pending.discard(idx)
                elif s["status"] == "failed":
                    print(f"  ❌ [{idx+1}] {jobs[idx][1][:40]}... {s['error'][:60]}")
                    results.append({"problem": jobs[idx][1], "ok": False, "error": s["error"]}); pending.discard(idx)

    passed = sum(1 for r in results if r.get("ok"))
    total_cost = sum(r.get("cost", 0) for r in results)
    print(f"\n{'='*60}\n📊 {passed}/{len(results)} passed | ${total_cost:.2f} total cost")
    if any(not r.get("ok") for r in results):
        print("Failed:")
        for r in results:
            if not r.get("ok"): print(f"  - {r['problem'][:60]}... → {r.get('error','?')[:60]}")
    
    os.makedirs("logs", exist_ok=True)
    with open("logs/stress_test_results.json", "w") as f:
        json.dump({"ts": time.strftime("%Y-%m-%d %H:%M:%S"), "results": results}, f, indent=2)

if __name__ == "__main__":
    p = argparse.ArgumentParser()
    p.add_argument("--count", type=int)
    p.add_argument("--sequential", action="store_true")
    a = p.parse_args()
    run(count=a.count, sequential=a.sequential)
