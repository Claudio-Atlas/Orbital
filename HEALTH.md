# HEALTH.md — Orbital System Health

*Last audit: 2026-02-14*
*Status: 🟡 PARTIALLY READY (P0 complete except Stripe, waiting on bank/EIN)*

---

## Quick Status

| Component | Status | Notes |
|-----------|--------|-------|
| Frontend | ✅ Live | Vercel: orbital-lime.vercel.app |
| Backend API | ✅ Live | Railway: orbital-production-7c22.up.railway.app |
| Workers | ✅ Live | Celery on Railway (2 workers, connected to Redis) |
| Redis | ✅ Running | Railway: redis.railway.internal:6379 |
| Database | ✅ Live | Supabase |
| Auth | ✅ Working | Supabase Auth |
| Payments | ⚠️ Partial | Checkout works, webhook missing (needs bank/EIN) |
| Video Storage | ❌ Not Set Up | R2 needed |
| Fish Audio | ❌ Missing Key | Needs business bank account |

---

## Persona Scores

| Persona | Score | Status | Blocking Issues |
|---------|-------|--------|-----------------|
| Security Engineer | 7/10 | ⚠️ Flag | ✅ Rate limiting + input sanitization done |
| Payment Specialist | 3/10 | ❌ VETO | No webhook, no audit trail |
| API Architect | 6/10 | ⚠️ Flag | No versioning |
| Performance Engineer | 6/10 | ⚠️ Flag | Render time > target |
| Math/AI Expert | 7/10 | ⚠️ Flag | No AI output verification |
| UX Designer | 7/10 | ⚠️ Flag | Error messages need polish |
| DevOps Engineer | 8/10 | ⚠️ Flag | ✅ Fully deployed! Still needs monitoring/alerting |
| Privacy Advocate | 6/10 | ⚠️ Flag | No retention policy |

**Overall: D+ (3 hard vetoes)**

---

## Priority Fix List

### P0 — Must Fix Before ANY Users

| # | Task | Status | Owner | Effort |
|---|------|--------|-------|--------|
| 1 | Implement Stripe webhook | ⏸️ HOLD | Waiting for bank/EIN | 2-3 hrs |
| 2 | Deploy backend to Railway | ✅ DONE | — | — |
| 3 | Add rate limiting | ✅ DONE | — | — |
| 4 | Provision Redis on Railway | ✅ DONE | — | — |
| 5 | Deploy Celery workers | ✅ DONE | — | — |

### P1 — Fix Before Real Money

| # | Task | Status | Owner | Effort |
|---|------|--------|-------|--------|
| 6 | Make minutes deduction transactional | 🔄 TODO | — | 2 hrs |
| 7 | Add minute_transactions audit table | 🔄 TODO | — | 1 hr |
| 8 | Add idempotency to webhook | ⏸️ HOLD | After #1 | 1 hr |
| 9 | Input sanitization for AI | ✅ DONE | — | — |
| 10 | Basic monitoring/alerting | 🔄 TODO | — | 3-4 hrs |

### P2 — Fix Before Scale

| # | Task | Status | Owner | Effort |
|---|------|--------|-------|--------|
| 11 | Set up Cloudflare R2 | 🔄 TODO | — | 2 hrs |
| 12 | API versioning | 🔄 TODO | — | 1 hr |
| 13 | Video retention policy | 🔄 TODO | — | 1 hr |
| 14 | Improve error messages | 🔄 TODO | — | 2 hrs |
| 15 | Accessibility audit | 🔄 TODO | — | 3 hrs |

---

## Architecture Overview

```
┌─────────────────────────────────────────────────────────────────┐
│                         FRONTEND                                 │
│                   (Next.js on Vercel)                           │
│                orbital-lime.vercel.app                          │
└────────────────────────┬────────────────────────────────────────┘
                         │
                         │ HTTPS + JWT
                         ▼
┌─────────────────────────────────────────────────────────────────┐
│                        SUPABASE                                  │
│                                                                  │
│  ┌─────────────┐    ┌─────────────────────────────────────┐    │
│  │    Auth     │    │           PostgreSQL                 │    │
│  │   (JWT)     │    │  • profiles                         │    │
│  └─────────────┘    │  • video_jobs                       │    │
│                      │  • purchases                        │    │
│                      │  • minute_transactions (TODO)       │    │
│                      └─────────────────────────────────────┘    │
└────────────────────────┬────────────────────────────────────────┘
                         │
                         │ Service key (backend only)
                         ▼
┌─────────────────────────────────────────────────────────────────┐
│                     RAILWAY (TODO: Deploy)                       │
│                                                                  │
│  ┌─────────────┐    ┌─────────────┐    ┌─────────────────┐     │
│  │  FastAPI    │───▶│   Redis     │───▶│  Celery Workers │     │
│  │  (API)      │    │  (Queue)    │    │  (Rendering)    │     │
│  └─────────────┘    └─────────────┘    └────────┬────────┘     │
│                                                  │              │
└──────────────────────────────────────────────────┼──────────────┘
                                                   │
                         ┌─────────────────────────┼─────────────┐
                         │                         │             │
                         ▼                         ▼             ▼
                  ┌────────────┐           ┌────────────┐  ┌──────────┐
                  │ DeepSeek/  │           │ Fish Audio │  │  Manim   │
                  │ OpenAI     │           │ (TTS)      │  │ (Video)  │
                  └────────────┘           └────────────┘  └──────────┘
                                                   │
                                                   ▼
                                          ┌────────────────┐
                                          │ Cloudflare R2  │
                                          │ (Video CDN)    │
                                          │ TODO: Set up   │
                                          └────────────────┘
```

---

## Environment Variables Needed

### Supabase (Already Set)
- `SUPABASE_URL` ✅
- `SUPABASE_SERVICE_KEY` ✅
- `NEXT_PUBLIC_SUPABASE_URL` ✅
- `NEXT_PUBLIC_SUPABASE_ANON_KEY` ✅

### AI Services (Already Set)
- `OPENAI_API_KEY` ✅
- `FISH_AUDIO_API_KEY` ✅

### Railway (TODO)
- `REDIS_URL` — From Railway Redis plugin
- `CELERY_ENABLED=true`
- `USE_SUPABASE_JOBS=true`

### Stripe (HOLD — waiting for bank/EIN)
- `STRIPE_SECRET_KEY`
- `STRIPE_WEBHOOK_SECRET`

### Cloudflare R2 (TODO)
- `R2_ACCESS_KEY_ID`
- `R2_SECRET_ACCESS_KEY`
- `R2_BUCKET`
- `R2_ENDPOINT`

---

## Database Tables

### Existing
- `profiles` — User data, minutes_balance
- `video_jobs` — Job tracking (TODO: may need to create)
- `purchases` — Payment records (TODO: may need to create)

### TODO
- `minute_transactions` — Audit trail for all minute changes

---

## Recent Changes

| Date | Change | Impact |
|------|--------|--------|
| 2026-02-14 | **Deployed to Railway** (P0 #2,4,5) | DevOps +3 |
| 2026-02-14 | Added rate limiting (P0 #3) | Security +1 |
| 2026-02-14 | Added CLAUDE.md + PERSONAS.md | Quality gates |
| 2026-02-14 | Scaffolded Celery task queue | Ready for deploy |
| 2026-02-14 | Added login modal on homepage | UX fix |
| 2026-02-12 | Fixed auth issues | Frontend working |

---

## Next Session Checklist

When resuming work:
1. Read this file for current status
2. Check P0 items — what's next?
3. Run `audit` if significant time has passed
4. Update this file after completing tasks

---

## Blockers

| Blocker | Waiting On | Affects |
|---------|------------|---------|
| Stripe setup | Bank account + EIN | P0 #1, P1 #8 |

---

## Useful Commands

```bash
# Local development
cd ~/Desktop/Orbital/orbital_api
source venv/bin/activate
python -m uvicorn main:app --port 8002

# Frontend
cd ~/Desktop/Orbital/orbital_site
npm run dev

# Check Supabase tables
# Use Supabase dashboard or TablePlus
```

---

*Update this file after completing any P0/P1 task.*
