# CLAUDE.md — Orbital Solver

## ⛔ GATE CHECK — Complete Before Every Code Edit

**Do not write or modify code until you've completed this:**

```
GATE CHECK:
- Branch: [current branch, or "creating <type>/<desc>"]
- Auth required: [yes/no — is this endpoint/page protected?]
- Payment involved: [yes/no — does this touch money, minutes, or Stripe?]
- User input: [what needs validation/sanitization, or "none"]
- Rate limit: [could this be abused? what limit applies?]
- AI API call: [yes/no — cost implications?]
- Database change: [table/column affected, or "none"]
- Tests needed: [which test files, or "none — no logic change"]
- Impact areas: [list from Change Impact Checklist]
```

**Skip gate only for:** answering questions, reading files, running non-edit commands.

---

## ⛔ PAYMENT GATE — Before ANY Stripe/Money Code

**Mandatory for anything touching payments, minutes, or billing:**

```
PAYMENT GATE:
- Webhook verified: [yes — signature checked / no — explain why]
- Idempotency: [how do we prevent double-processing?]
- Failure mode: [what happens if this fails mid-operation?]
- Rollback: [can we undo if something goes wrong?]
- Audit trail: [is this logged in minute_transactions?]
- Edge cases: [insufficient balance? refund? subscription cancel?]
```

**Never skip this gate for payment code. Never.**

---

## ⛔ POST-TEST GATE — After Running Tests

### If tests PASS:

1. Run RED TEAM protocol on new code (mandatory)
2. Report findings
3. Fix weaknesses
4. Only then mark complete

### If tests FAIL:

```
TEST FAILURE ANALYSIS:
- Failed test: [name]
- Expected: [what test expected]
- Actual: [what happened]
- Root cause: [implementation bug / test bug / needs investigation]
- Proposed action: [fix implementation / request approval to modify test]
```

**Default assumption: Test failures are implementation bugs, not test bugs.**

---

## Before Writing New Code — STOP

### 1. Search First

```bash
# Check for existing patterns
grep -r "pattern" src/
grep -r "function" src/lib/

# Check for existing components
ls src/components/

# Check for existing API routes
ls src/app/api/
```

### 2. For User Input — Know the Risk

| Input Type | Risk | Required |
|------------|------|----------|
| Problem text | Prompt injection | Sanitize before AI |
| Image upload | Malformed data | Validate format/size |
| URL params | Injection | Validate/escape |
| Form fields | XSS | React auto-escapes, but validate |

### 3. For API Endpoints — Know the Pattern

```typescript
// EVERY protected endpoint must:
export async function POST(request: Request) {
  // 1. Validate auth
  const user = await getUser(request);
  if (!user) return unauthorized();
  
  // 2. Rate limit check
  if (await isRateLimited(user.id)) return tooManyRequests();
  
  // 3. Validate input
  const body = await validateInput(request);
  
  // 4. Business logic
  // ...
  
  // 5. Audit log (for sensitive operations)
  await logAction(user.id, 'action_name', details);
}
```

### 4. For Database Operations — Know the Type

| Operation | Requirement |
|-----------|-------------|
| Read own data | RLS handles it |
| Write own data | RLS handles it |
| Deduct minutes | Transaction + row lock |
| Credit minutes | Idempotency check first |
| Cross-table update | Transaction required |

### 5. Code Standards

- **TypeScript strict** — No `any` types without justification
- **Error boundaries** — Catch and handle, never swallow
- **Loading states** — Always show feedback
- **Mobile-first** — Tailwind responsive classes
- **No hardcoded values** — Use constants/env vars
- **Descriptive names** — `handleVideoGeneration` not `doIt`

---

## Hard Rules — Never Break

### Architecture
- ✅ Supabase for auth + user data
- ✅ FastAPI for video processing
- ✅ Celery + Redis for job queue
- ✅ Cloudflare R2 for video storage
- ❌ Never store videos in Supabase
- ❌ Never call AI APIs from frontend
- ❌ Never expose service keys to client

### Security
- ✅ JWT validation on EVERY protected endpoint
- ✅ Rate limiting on EVERY authenticated endpoint
- ✅ Input sanitization before ANY AI call
- ✅ Stripe webhook signature verification
- ❌ Never trust client-side balance checks
- ❌ Never log sensitive data (keys, tokens, PII)
- ❌ Never disable RLS in production

### Payments
- ✅ Webhook is source of truth for credits
- ✅ Idempotency on ALL credit operations
- ✅ Transaction for minute deduction
- ✅ Audit trail in minute_transactions
- ❌ Never credit minutes from client request alone
- ❌ Never deduct before job success confirmation
- ❌ Never modify payment code without PAYMENT GATE

### Testing
- ✅ Test failures = implementation bugs (default)
- ✅ Red team after writing tests
- ✅ Test edge cases: zero, negative, boundary
- ❌ Never modify tests to make them pass without analysis
- ❌ Never skip red team without explicit permission

---

## Trigger Words

| Word | Action |
|------|--------|
| **"deploy"** | Run Ship Checklist, deploy to Vercel/Railway |
| **"audit"** | Full security + architecture review against PERSONAS |
| **"red team"** | Adversarial security review (see protocol) |
| **"spiral"** | Identify drift, correct course in 1-2 bullets |
| **"ask personas"** | Score change against all personas |
| **"cost"** | Analyze AI API cost impact of change |
| **"gate"** | Re-read this file, state 3 relevant rules |
| **"payment check"** | Full PAYMENT GATE analysis |

---

## Red Team Protocol

**Mandatory after any security-relevant code. Triggered by "red team".**

### For API Endpoints — Ask:

1. **Can an unauthenticated user access this?**
   - What if they forge/omit the JWT?
   - What if the token is expired?

2. **Can a user access another user's data?**
   - What if they change the user_id in the request?
   - What if they guess another job_id?

3. **Can this be abused at scale?**
   - What if they call it 1000x per second?
   - What's the cost to us? (AI API calls, compute)

4. **What's the worst silent failure?**
   - Could money be lost without anyone noticing?
   - Could videos be generated without payment?

### For Payment Code — Ask:

1. **Can they get free minutes?**
   - Replay the webhook?
   - Call credit endpoint directly?
   - Race condition between check and deduct?

2. **Can they drain the system?**
   - Generate videos without sufficient balance?
   - Refund exploit?

3. **Is the audit trail complete?**
   - Could money move without a record?
   - Could we investigate a dispute?

### For Input Handling — Ask:

1. **What happens with malicious input?**
   - SQL injection patterns?
   - Prompt injection for AI?
   - Script tags for XSS?

2. **What happens with malformed input?**
   - Missing fields?
   - Wrong types?
   - Overflow values?

### Output Format:

```
RED TEAM REPORT:
- Attack: [what could go wrong]
- Exploit: [how an attacker would do it]
- Mitigation: [specific fix required]

[repeat for each finding]

Status: [VULNERABLE — issues found / SECURE — no issues found]
```

---

## Change Impact Checklist

### Frontend (`orbital_site/`)

| Area | File(s) |
|------|---------|
| Auth state | `src/lib/auth.tsx`, `useAuth` hook |
| API calls | `src/lib/api.ts` |
| Types | `src/types/` |
| Components | `src/components/` |
| Pages | `src/app/` |
| Styles | `tailwind.config.js`, globals |

### Backend (`orbital_api/`)

| Area | File(s) |
|------|---------|
| API routes | `main.py`, `routes/` |
| Auth | `utils/auth.py` |
| Payments | `routes/payments.py` |
| Task queue | `celery_app.py`, `tasks.py` |
| Job storage | `jobs.py` |
| Problem parsing | `parser.py` |

### Database (Supabase)

| Area | Table(s) |
|------|----------|
| User data | `profiles` |
| Jobs | `video_jobs` |
| Payments | `purchases` |
| Audit | `minute_transactions` |

---

## Ship Checklist

When I say **"deploy"**:

### Frontend (Vercel)
1. `npm run build` — must pass
2. `npm run lint` — must pass
3. Test critical flows manually:
   - [ ] Login/signup works
   - [ ] Dashboard loads
   - [ ] Pricing modal requires auth
4. Commit with descriptive message
5. Push to main (auto-deploys)
6. Verify on production URL

### Backend (Railway)
1. `pip install -r requirements.txt` — no errors
2. Test endpoints locally:
   - [ ] `/health` returns 200
   - [ ] `/parse` requires auth
   - [ ] `/solve` requires auth
3. Check environment variables are set
4. Push to main
5. Verify deployment logs
6. Test production endpoint

### Database Changes
1. Test migration locally first
2. Backup production data (if applicable)
3. Run migration
4. Verify RLS policies still work
5. Test affected features

---

## AI Behavior

- **Ask before guessing** — If unclear, clarify first
- **Gate before coding** — Always complete GATE CHECK
- **Search before writing** — Check if it exists
- **Minimal changes** — No drive-by refactoring
- **Small patches** — No full-file rewrites
- **Concise explanations** — Implementation-focused
- **Never "fix" tests** — Fix implementation or ask first
- **Red team security code** — Automatic, not optional
- **Payment paranoia** — Always PAYMENT GATE

---

## Project Context

### What Orbital Is
AI-powered math video generator. Users submit problems, system generates step-by-step tutorial videos with narration and animation.

### Business Model
Minutes-based pricing. Users buy minute packages, each video deducts from balance based on duration.

### Architecture Summary
```
Frontend (Next.js/Vercel)
    ↓
Auth (Supabase)
    ↓
API (FastAPI/Railway) → Queue (Redis) → Workers (Celery)
    ↓                                        ↓
Payments (Stripe)                    Video Factory (Manim + Fish Audio)
    ↓                                        ↓
Database (Supabase)                  Storage (Cloudflare R2)
```

### Key Files
- Frontend entry: `orbital_site/src/app/page.tsx`
- API entry: `orbital_api/main.py`
- Auth: `orbital_api/utils/auth.py`
- Payments: `orbital_api/routes/payments.py`
- Tasks: `orbital_api/tasks.py`
- Architecture: `ORBITAL-ARCHITECTURE.md`

---

## Debugging

For API issues:
```bash
# Check health
curl http://localhost:8002/health

# Check with auth
curl -H "Authorization: Bearer <token>" http://localhost:8002/jobs
```

For frontend issues:
- Open browser DevTools → Network tab
- Check for failed requests
- Check console for errors

For Celery issues:
```bash
# Check queue depth
redis-cli LLEN celery

# Check worker status
celery -A celery_app inspect active
```
