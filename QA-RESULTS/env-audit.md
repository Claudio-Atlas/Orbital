# Orbital Environment Variables Audit

**Generated:** 2025-01-27
**Auditor:** QA Subagent

---

## Summary

| Service | File | Variables | Status |
|---------|------|-----------|--------|
| orbital_site (Next.js) | `.env.local` | 3 | ✅ All set |
| orbital_api (FastAPI) | `.env` | 18 | ⚠️ Some empty |

---

## orbital_site/.env.local (Next.js Frontend)

### NEXT_PUBLIC_ Variables (Client-Exposed)

| Variable | Status | Required | Notes |
|----------|--------|----------|-------|
| `NEXT_PUBLIC_SUPABASE_URL` | ✅ Set | **YES** | Supabase project URL |
| `NEXT_PUBLIC_SUPABASE_ANON_KEY` | ✅ Set | **YES** | Supabase anon/public key |
| `NEXT_PUBLIC_API_URL` | ✅ Set | **YES** | Currently `http://localhost:8002` |

### ⚠️ Production Issue
- `NEXT_PUBLIC_API_URL` is set to `localhost` - **MUST change for production**
- Should point to deployed API URL (Railway, Fly.io, etc.)

---

## orbital_api/.env (FastAPI Backend)

### Supabase

| Variable | Status | Required | Notes |
|----------|--------|----------|-------|
| `SUPABASE_URL` | ✅ Set | **YES** | Supabase project URL |
| `SUPABASE_ANON_KEY` | ✅ Set | **YES** | For client-level operations |
| `SUPABASE_SERVICE_KEY` | ✅ Set | **YES** | For admin operations (RLS bypass) |

### AI Providers

| Variable | Status | Required | Notes |
|----------|--------|----------|-------|
| `OPENAI_API_KEY` | ❌ Empty | **YES** (if using OpenAI TTS) | For TTS generation |
| `DEEPSEEK_API_KEY` | ✅ Set | **YES** | For script generation |
| `ORBITAL_PROVIDER` | ✅ Set (`deepseek`) | No | Default: deepseek |
| `TTS_PROVIDER` | ✅ Set (`openai`) | No | Default: openai |

### Stripe (Payments)

| Variable | Status | Required | Notes |
|----------|--------|----------|-------|
| `STRIPE_SECRET_KEY` | ✅ Set | **YES** | Test mode key detected |
| `STRIPE_WEBHOOK_SECRET` | ❌ Empty | **YES** (for webhooks) | Needed for payment verification |
| `STRIPE_PRICE_STARTER` | ✅ Set | **YES** | One-time $9 |
| `STRIPE_PRICE_STANDARD` | ✅ Set | **YES** | One-time $29 |
| `STRIPE_PRICE_PRO` | ✅ Set | **YES** | One-time $79 |
| `STRIPE_PRICE_STARTER_SUB` | ✅ Set | **YES** | Subscription $9/mo |
| `STRIPE_PRICE_STANDARD_SUB` | ✅ Set | **YES** | Subscription $29/mo |
| `STRIPE_PRICE_PRO_SUB` | ✅ Set | **YES** | Subscription $79/mo |

### Cloudflare R2 (Video Storage)

| Variable | Status | Required | Notes |
|----------|--------|----------|-------|
| `R2_ACCOUNT_ID` | ❌ Empty | **YES** (for video) | Required for video uploads |
| `R2_ACCESS_KEY_ID` | ❌ Empty | **YES** (for video) | R2 API token |
| `R2_SECRET_ACCESS_KEY` | ❌ Empty | **YES** (for video) | R2 API secret |
| `R2_BUCKET_NAME` | ✅ Set | **YES** | `orbital-videos` |

---

## 🚨 Critical Issues

1. **OPENAI_API_KEY is empty** - TTS will fail if `TTS_PROVIDER=openai`
2. **STRIPE_WEBHOOK_SECRET is empty** - Webhooks won't be verified
3. **R2 credentials missing** - Video storage won't work
4. **API URL is localhost** - Frontend can't reach API in production

---

## ✅ Vercel Deployment Checklist (orbital_site)

### Required Variables

```
NEXT_PUBLIC_SUPABASE_URL=https://pqwhfiuvcsjfevjwljml.supabase.co
NEXT_PUBLIC_SUPABASE_ANON_KEY=<supabase-anon-key>
NEXT_PUBLIC_API_URL=<production-api-url>
```

### Steps

- [ ] Add `NEXT_PUBLIC_SUPABASE_URL` (same as local)
- [ ] Add `NEXT_PUBLIC_SUPABASE_ANON_KEY` (same as local)
- [ ] Add `NEXT_PUBLIC_API_URL` → **Change to production API URL**
- [ ] Verify all are added to **ALL environments** (Production, Preview, Development)

---

## ✅ Backend Deployment Checklist (Railway/Fly.io)

### Required Variables

```
SUPABASE_URL=https://pqwhfiuvcsjfevjwljml.supabase.co
SUPABASE_ANON_KEY=<supabase-anon-key>
SUPABASE_SERVICE_KEY=<supabase-service-key>
DEEPSEEK_API_KEY=<deepseek-key>
OPENAI_API_KEY=<openai-key>
STRIPE_SECRET_KEY=<stripe-secret>
STRIPE_WEBHOOK_SECRET=<stripe-webhook-secret>
STRIPE_PRICE_STARTER=price_xxx
STRIPE_PRICE_STANDARD=price_xxx
STRIPE_PRICE_PRO=price_xxx
STRIPE_PRICE_STARTER_SUB=price_xxx
STRIPE_PRICE_STANDARD_SUB=price_xxx
STRIPE_PRICE_PRO_SUB=price_xxx
R2_ACCOUNT_ID=<cloudflare-account-id>
R2_ACCESS_KEY_ID=<r2-access-key>
R2_SECRET_ACCESS_KEY=<r2-secret>
R2_BUCKET_NAME=orbital-videos
ORBITAL_PROVIDER=deepseek
TTS_PROVIDER=openai
```

### Steps

- [ ] Add all Supabase vars (3)
- [ ] Add AI keys: `DEEPSEEK_API_KEY`, `OPENAI_API_KEY`
- [ ] Add all Stripe vars (8 total)
- [ ] Set up Cloudflare R2 bucket and add credentials (4)
- [ ] Set provider configs (2)
- [ ] Configure Stripe webhook endpoint and get `STRIPE_WEBHOOK_SECRET`

---

## 🔐 Security Notes

- All `SUPABASE_SERVICE_KEY`, `STRIPE_SECRET_KEY`, `OPENAI_API_KEY`, `DEEPSEEK_API_KEY` are **server-only** secrets
- `NEXT_PUBLIC_*` variables are exposed to browser - only anon/public keys here
- Current setup correctly separates public vs secret keys

---

## Before Going Live

1. **Get OpenAI API key** - Required for TTS
2. **Set up Stripe webhooks** - Get webhook secret for payment verification
3. **Set up Cloudflare R2** - Create bucket, get credentials
4. **Change to production Stripe keys** - Currently using test keys (`sk_test_*`)
5. **Update API URL** - Point frontend to deployed backend URL
