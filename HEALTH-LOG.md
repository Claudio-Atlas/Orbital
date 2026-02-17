# HEALTH-LOG.md — Orbital Change Log

*Chronological log of all changes, deployments, and fixes.*

---

## 2026-02-17

### Session: Status Update

**Context:** Pre-session check-in, noting completed items.

#### ✅ Completed

| Time | Task | Details |
|------|------|---------|
| — | Custom domain connected | `orbitalsolver.io` live on Vercel |
| — | EIN obtained | Ready to wire Stripe |

#### Next Session Plan

1. **Wire Stripe webhook** — EIN ready, configure:
   - `STRIPE_SECRET_KEY` on Railway
   - `STRIPE_WEBHOOK_SECRET` on Railway
   - Test checkout → webhook → minute credit flow
2. **Set up Cloudflare R2** — Video storage
3. **Fish Audio API key** — Once business bank is ready

#### Production URLs

| Service | URL | Status |
|---------|-----|--------|
| Frontend | https://orbitalsolver.io | ✅ Live |
| API | https://orbital-production-7c22.up.railway.app | ✅ Live |

---

## 2026-02-14

### Session: Architecture Audit & P0 Fixes

**Context:** Initial audit revealed D+ grade with 3 hard vetoes (Security, Payment, DevOps).

#### ✅ Completed

| Time | Task | Details |
|------|------|---------|
| ~09:00 | Added CLAUDE.md + PERSONAS.md | Quality gates and expert persona system |
| ~09:30 | Created HEALTH.md | System health tracking |
| ~10:30 | **P0 #3: Rate Limiting** | Added Redis-backed rate limiting to all endpoints |
| ~11:00 | **P0 #4: Redis Provisioned** | Railway Redis service created |
| ~11:05 | **P0 #2: API Deployed** | FastAPI deployed to Railway |
| ~11:10 | **P0 #5: Worker Created** | Celery worker service created |
| ~11:30 | Cleaned up duplicates | Deleted orbital-api, 3 extra Redis instances |
| ~11:45 | Fixed railway.json | Removed hardcoded startCommand |
| ~11:55 | **P0 #5: Worker Running** | Celery worker confirmed running with 2 workers |
| ~12:00 | **P0 COMPLETE** | All P0 items done except Stripe (waiting bank/EIN) |
| ~12:30 | **P1 #9: Input Sanitization** | Prompt injection protection, bypass detection, RED TEAM passed |

#### 🔄 In Progress

| Task | Status | Notes |
|------|--------|-------|
| — | — | Waiting on bank/EIN for Stripe + Fish Audio |

#### ⏸️ On Hold (Waiting for Bank/EIN)

| Task | Blocker | ETA |
|------|---------|-----|
| P0 #1: Stripe webhook | Need business bank account | Today/Tomorrow |
| Fish Audio API key | Need business bank account | Today/Tomorrow |

#### Deployment URLs

| Service | URL | Status |
|---------|-----|--------|
| API | https://orbital-production-7c22.up.railway.app | ✅ Live |
| Health Check | https://orbital-production-7c22.up.railway.app/health | ✅ Responding |
| Worker | celery@railway (internal) | ✅ Running (2 workers) |
| Redis | redis.railway.internal:6379 | ✅ Running |

#### Environment Variables Set

**orbital-api:**
- SUPABASE_URL ✅
- SUPABASE_SERVICE_KEY ✅
- DEEPSEEK_API_KEY ✅
- REDIS_URL ✅
- CELERY_ENABLED=true ✅
- USE_SUPABASE_JOBS=true ✅
- TTS_PROVIDER=fish ✅
- ORBITAL_PROVIDER=deepseek ✅
- FISH_API_KEY ❌ (pending)

**orbital-worker:**
- Same as API
- RAILWAY_PROCESS_TYPE=worker ✅

#### Commits

| Hash | Message |
|------|---------|
| 14c9298 | Add Claude behavioral guidelines and expert personas |
| f06fb9e | Add HEALTH.md - system health tracking |
| 94782e2 | Add rate limiting to API endpoints |
| f8eec4d | Update HEALTH.md - rate limiting complete |
| bec66fb | Uncomment worker process in Procfile |
| bd61fcc | Add monitoring and alerting system (P1 #10) |

---

### Session: P1 #10 Monitoring/Alerting (12:00-12:30)

**Context:** Implementing basic monitoring and alerting as specified in P1 task list.

#### ✅ Completed

| Time | Task | Details |
|------|------|---------|
| ~12:10 | Created structured logger | `utils/logging.py` - JSON for Railway, console for local |
| ~12:15 | Created request middleware | `middleware/request_log.py` - timing, request IDs |
| ~12:20 | Created alerting system | `utils/alerts.py` - Discord/Slack webhooks |
| ~12:22 | Enhanced /health endpoint | Component checks for Redis, Supabase, Celery |
| ~12:25 | Wired existing code | Replaced print() with logger, added alerts |
| ~12:28 | RED TEAM passed | No security issues found |

#### Files Created/Modified

| File | Change |
|------|--------|
| `utils/logging.py` | NEW - Structured JSON logging |
| `utils/alerts.py` | NEW - Webhook alerting |
| `middleware/request_log.py` | NEW - Request logging middleware |
| `main.py` | Enhanced /health, added middleware |
| `utils/rate_limit.py` | Replaced print with logger |
| `utils/sanitize.py` | Added security event logging |
| `requirements.txt` | Added httpx |

#### Security Features

- Sensitive fields auto-redacted (tokens, keys, emails, problem content)
- User IDs masked to first 8 chars
- Request bodies never logged
- Alert rate limiting (60s cooldown per alert type)
- JSON escaping prevents log injection

#### To Configure Alerting

Set these env vars on Railway:
```
ALERT_WEBHOOK_URL=https://discord.com/api/webhooks/...
ALERT_LEVEL=ERROR
ALERT_ENABLED=true
```

---

### Session: P1 #6,7,8 Transactional Minutes (12:45-13:30)

**Context:** Building atomic, audited minutes system before Stripe webhook.

#### ✅ Completed

| Time | Task | Details |
|------|------|---------|
| ~12:50 | Checked Supabase state | profiles ✅, purchases ✅, minute_transactions ❌ |
| ~13:00 | Created SQL migration | `migrations/001_minute_transactions.sql` |
| ~13:05 | Clayton ran migration | Table + functions created |
| ~13:10 | Verified functions work | credit_minutes_safe, debit_minutes_safe |
| ~13:15 | Created Python wrapper | `utils/minutes.py` with async/sync functions |
| ~13:20 | Wired into tasks.py | Debit minutes on video completion |
| ~13:25 | Wired into payments.py | Use new credit function for webhook |
| ~13:28 | RED TEAM passed | No security issues |

#### Database Changes

| Object | Type | Purpose |
|--------|------|---------|
| `minute_transactions` | Table | Audit trail |
| `credit_minutes_safe()` | Function | Atomic credit + idempotency |
| `debit_minutes_safe()` | Function | Atomic debit + balance check |
| `get_minute_transactions()` | Function | User history |

#### Security Features

| Feature | How |
|---------|-----|
| Idempotency | reference_id checked before insert |
| Race prevention | FOR UPDATE row lock |
| Balance check | Server-side in transaction |
| Audit tamper-proof | RLS: users can only SELECT |

#### Commits

| Hash | Message |
|------|---------|
| 4a5ddca | Add transactional minutes system (P1 #6 + #7) |

---

## Score Progress

| Date | Overall | Security | Payment | DevOps | Notes |
|------|---------|----------|---------|--------|-------|
| 2026-02-14 AM | D+ | 5/10 | 3/10 | 4/10 | Initial audit |
| 2026-02-14 12:00 | C+ | 6/10 | 3/10 | 8/10 | P0 complete (except Stripe) |
| 2026-02-14 12:30 | B- | 7/10 | 3/10 | 8/10 | Input sanitization done |
| 2026-02-14 12:21 | B | 7/10 | 3/10 | 9/10 | P1 #10 Monitoring complete |
| 2026-02-14 13:30 | B+ | 8/10 | 8/10 | 9/10 | P1 #6,7,8 Transactional minutes |

---

## Template for Future Entries

```markdown
## YYYY-MM-DD

### Session: [Brief Description]

#### ✅ Completed
| Time | Task | Details |
|------|------|---------|

#### 🔄 In Progress
| Task | Status | Notes |
|------|--------|-------|

#### ⏸️ Blocked
| Task | Blocker | ETA |
|------|---------|-----|

#### Commits
| Hash | Message |
|------|---------|

#### Notes
- [Any important observations]
```
