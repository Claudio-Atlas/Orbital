# Orbital Solver — System Architecture

*Version: 1.0 | Last updated: 2026-02-14*
*Status: Pre-production audit document*

---

## Table of Contents

1. [Executive Summary](#executive-summary)
2. [System Overview](#system-overview)
3. [Component Architecture](#component-architecture)
4. [Data Flow](#data-flow)
5. [Database Design](#database-design)
6. [Authentication & Authorization](#authentication--authorization)
7. [Payment Processing](#payment-processing)
8. [Task Queue Architecture](#task-queue-architecture)
9. [Video Generation Pipeline](#video-generation-pipeline)
10. [API Specification](#api-specification)
11. [Security Considerations](#security-considerations)
12. [Error Handling](#error-handling)
13. [Scalability & Performance](#scalability--performance)
14. [Monitoring & Observability](#monitoring--observability)
15. [Infrastructure & Deployment](#infrastructure--deployment)
16. [Known Limitations & Technical Debt](#known-limitations--technical-debt)
17. [Open Questions](#open-questions)

---

## Executive Summary

**Orbital** is a SaaS application that generates step-by-step math tutorial videos using AI. Users submit math problems (text or image), the system parses them, generates narrated animations, and delivers video content.

**Business Model:** Minutes-based pricing. Users purchase minute packages; each video deducts from their balance based on duration.

**Tech Stack:**
- Frontend: Next.js 14 / React 19 / TypeScript / Tailwind
- Backend: FastAPI / Python 3.11
- Queue: Celery / Redis
- Database: Supabase (PostgreSQL)
- Auth: Supabase Auth (JWT)
- Payments: Stripe
- Video: Manim (animation) + Fish Audio (TTS)
- Storage: Cloudflare R2 (planned)
- Hosting: Vercel (frontend), Railway (backend)

---

## System Overview

### Architecture Diagram

```
┌─────────────────────────────────────────────────────────────────────────────────┐
│                                  INTERNET                                        │
└───────────────────────────────────┬─────────────────────────────────────────────┘
                                    │
                    ┌───────────────┴───────────────┐
                    │                               │
                    ▼                               ▼
        ┌───────────────────┐           ┌───────────────────┐
        │   Vercel CDN      │           │   Stripe          │
        │   (Frontend)      │           │   (Payments)      │
        │                   │           │                   │
        │ orbital-lime.     │           │ - Checkout        │
        │ vercel.app        │           │ - Webhooks        │
        └─────────┬─────────┘           └─────────┬─────────┘
                  │                               │
                  │    ┌──────────────────────────┘
                  │    │
                  ▼    ▼
        ┌───────────────────┐
        │   Supabase        │
        │                   │
        │ - Auth (JWT)      │
        │ - PostgreSQL      │
        │ - Row Level Sec   │
        └─────────┬─────────┘
                  │
                  │ JWT validation
                  ▼
        ┌───────────────────┐         ┌───────────────────┐
        │   Railway         │         │   Railway         │
        │   (API Server)    │◄───────►│   (Redis)         │
        │                   │         │                   │
        │ - FastAPI         │         │ - Job queue       │
        │ - Request handling│         │ - Result backend  │
        └─────────┬─────────┘         └─────────┬─────────┘
                  │                             │
                  │ Enqueue jobs                │ Dequeue jobs
                  │                             │
                  │         ┌───────────────────┘
                  │         │
                  │         ▼
                  │ ┌───────────────────┐
                  │ │   Railway         │
                  │ │   (Celery Workers)│
                  │ │                   │
                  │ │ - Video rendering │
                  │ │ - AI API calls    │
                  │ └─────────┬─────────┘
                  │           │
                  │           │ Upload videos
                  │           ▼
                  │ ┌───────────────────┐
                  │ │   Cloudflare R2   │
                  │ │   (Object Storage)│
                  │ │                   │
                  │ │ - Video files     │
                  │ │ - CDN delivery    │
                  │ └───────────────────┘
                  │
                  │ External AI APIs
                  ▼
        ┌───────────────────┐
        │   AI Services     │
        │                   │
        │ - DeepSeek/OpenAI │
        │ - Fish Audio      │
        └───────────────────┘
```

---

## Component Architecture

### 1. Frontend (Next.js)

| Attribute | Value |
|-----------|-------|
| Framework | Next.js 14 (App Router) |
| Runtime | Edge + Node.js |
| Styling | Tailwind CSS |
| State | React hooks, no global state manager |
| Auth | Supabase Auth client |
| Location | `~/Desktop/Orbital/orbital_site/` |

**Route Structure:**
```
/                   # Landing page (public)
/login              # Auth - login
/signup             # Auth - registration  
/forgot-password    # Auth - password reset
/reset-password     # Auth - password reset callback
/auth/callback      # OAuth callback handler
/dashboard          # Main solver UI (protected)
/videos             # User's video history (protected)
/settings           # Account settings (protected)
/purchases          # Purchase history (protected)
/terms              # Terms of service (public)
/privacy            # Privacy policy (public)
```

**Key Components:**
- `PricingModal` — Stripe checkout trigger (requires auth)
- `AuthProvider` — React context for auth state
- `useAuth` hook — Auth state + methods

**Build Output:** Static pages where possible, server-rendered for dynamic routes.

---

### 2. Backend API (FastAPI)

| Attribute | Value |
|-----------|-------|
| Framework | FastAPI 0.109+ |
| Python | 3.11 |
| ASGI Server | Uvicorn |
| Location | `~/Desktop/Orbital/orbital_api/` |

**File Structure:**
```
orbital_api/
├── main.py              # App entry, routes
├── parser.py            # Problem parsing (GPT/DeepSeek)
├── celery_app.py        # Celery configuration
├── tasks.py             # Background tasks
├── jobs.py              # Job storage abstraction
├── worker.py            # Worker entry point
├── routes/
│   └── payments.py      # Stripe endpoints
├── utils/
│   └── auth.py          # JWT validation
├── requirements.txt
├── Procfile             # Railway process definitions
└── .env                 # Environment variables (not in git)
```

**Middleware:**
- CORS (allowlist-based)
- No rate limiting currently (⚠️ **TODO**)

---

### 3. Task Queue (Celery + Redis)

| Attribute | Value |
|-----------|-------|
| Broker | Redis |
| Backend | Redis |
| Serialization | JSON |
| Concurrency | 2 tasks per worker |
| Task timeout | 10 minutes hard, 9 minutes soft |

**Queue Design:**
```
┌─────────────┐     ┌─────────────┐     ┌─────────────┐
│   default   │     │ video_render│     │   (future)  │
│   queue     │     │   queue     │     │   queues    │
└──────┬──────┘     └──────┬──────┘     └─────────────┘
       │                   │
       ▼                   ▼
  parse tasks         render tasks
  (lightweight)       (CPU-intensive)
```

**Task Guarantees:**
- `task_acks_late=True` — Acknowledge only after completion
- `task_reject_on_worker_lost=True` — Re-queue if worker crashes
- Results expire after 24 hours

---

### 4. Video Factory

**Pipeline Steps:**

| Step | Service | Input | Output | Duration |
|------|---------|-------|--------|----------|
| 1. Parse | DeepSeek/GPT-4 | Problem text | Structured JSON | ~2-5s |
| 2. Voice | Fish Audio | Narration text | MP3 audio | ~5-15s |
| 3. Animate | Manim | Steps JSON | MP4 video | ~20-60s |
| 4. Compose | FFmpeg | Audio + Video | Final MP4 | ~2-5s |

**Total estimated time:** 30-90 seconds per video

**Location:** `~/Desktop/Orbital/orbital_factory/`

---

## Data Flow

### Happy Path: Video Generation

```
┌──────┐          ┌──────┐          ┌──────┐          ┌──────┐          ┌──────┐
│ User │          │ FE   │          │ API  │          │Redis │          │Worker│
└──┬───┘          └──┬───┘          └──┬───┘          └──┬───┘          └──┬───┘
   │                 │                 │                 │                 │
   │ 1. Submit       │                 │                 │                 │
   │ problem         │                 │                 │                 │
   │────────────────►│                 │                 │                 │
   │                 │                 │                 │                 │
   │                 │ 2. POST /solve  │                 │                 │
   │                 │ + JWT token     │                 │                 │
   │                 │────────────────►│                 │                 │
   │                 │                 │                 │                 │
   │                 │                 │ 3. Validate JWT │                 │
   │                 │                 │ (Supabase)      │                 │
   │                 │                 │                 │                 │
   │                 │                 │ 4. Parse problem│                 │
   │                 │                 │ (DeepSeek)      │                 │
   │                 │                 │                 │                 │
   │                 │                 │ 5. Create job   │                 │
   │                 │                 │ record          │                 │
   │                 │                 │ (Supabase)      │                 │
   │                 │                 │                 │                 │
   │                 │                 │ 6. Queue task   │                 │
   │                 │                 │────────────────►│                 │
   │                 │                 │                 │                 │
   │                 │ 7. Return       │                 │                 │
   │                 │ job_id          │                 │                 │
   │                 │◄────────────────│                 │                 │
   │                 │                 │                 │                 │
   │                 │                 │                 │ 8. Dequeue      │
   │                 │                 │                 │────────────────►│
   │                 │                 │                 │                 │
   │                 │ 9. Poll         │                 │                 │
   │                 │ GET /job/{id}   │                 │                 │
   │                 │────────────────►│                 │                 │
   │                 │                 │                 │                 │
   │                 │ 10. Return      │                 │                 │
   │                 │ status:processing                 │ 11. Render      │
   │                 │◄────────────────│                 │ video           │
   │                 │                 │                 │                 │
   │                 │                 │                 │                 │
   │                 │                 │                 │ 12. Upload to   │
   │                 │                 │                 │ R2              │
   │                 │                 │                 │                 │
   │                 │                 │                 │ 13. Update job  │
   │                 │                 │                 │ (Supabase)      │
   │                 │                 │                 │                 │
   │                 │ 14. Poll        │                 │                 │
   │                 │ GET /job/{id}   │                 │                 │
   │                 │────────────────►│                 │                 │
   │                 │                 │                 │                 │
   │                 │ 15. Return      │                 │                 │
   │                 │ status:complete │                 │                 │
   │                 │ video_url       │                 │                 │
   │                 │◄────────────────│                 │                 │
   │                 │                 │                 │                 │
   │ 16. Play video  │                 │                 │                 │
   │◄────────────────│                 │                 │                 │
   │                 │                 │                 │                 │
```

---

## Database Design

### Supabase PostgreSQL Schema

```sql
-- =============================================
-- PROFILES: Extended user data
-- =============================================
CREATE TABLE profiles (
    id UUID PRIMARY KEY REFERENCES auth.users(id) ON DELETE CASCADE,
    email TEXT,
    full_name TEXT,
    avatar_url TEXT,
    minutes_balance NUMERIC(10,2) DEFAULT 0 NOT NULL,
    lifetime_minutes_purchased NUMERIC(10,2) DEFAULT 0,
    created_at TIMESTAMPTZ DEFAULT NOW() NOT NULL,
    updated_at TIMESTAMPTZ DEFAULT NOW() NOT NULL
);

-- Trigger to create profile on user signup
CREATE OR REPLACE FUNCTION handle_new_user()
RETURNS TRIGGER AS $$
BEGIN
    INSERT INTO public.profiles (id, email, full_name)
    VALUES (
        NEW.id,
        NEW.email,
        NEW.raw_user_meta_data->>'full_name'
    );
    RETURN NEW;
END;
$$ LANGUAGE plpgsql SECURITY DEFINER;

CREATE TRIGGER on_auth_user_created
    AFTER INSERT ON auth.users
    FOR EACH ROW EXECUTE FUNCTION handle_new_user();

-- RLS
ALTER TABLE profiles ENABLE ROW LEVEL SECURITY;

CREATE POLICY "Users can view own profile"
    ON profiles FOR SELECT
    USING (auth.uid() = id);

CREATE POLICY "Users can update own profile"
    ON profiles FOR UPDATE
    USING (auth.uid() = id);

-- =============================================
-- VIDEO_JOBS: Job tracking
-- =============================================
CREATE TABLE video_jobs (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    job_id TEXT UNIQUE NOT NULL,
    user_id UUID NOT NULL REFERENCES auth.users(id) ON DELETE CASCADE,
    
    -- Status
    status TEXT NOT NULL DEFAULT 'pending' 
        CHECK (status IN ('pending', 'processing', 'complete', 'failed', 'cancelled')),
    
    -- Problem data
    problem TEXT NOT NULL,
    problem_latex TEXT,
    steps JSONB,
    
    -- Result
    video_url TEXT,
    video_duration_seconds NUMERIC(10,2),
    minutes_charged NUMERIC(10,2),
    error TEXT,
    
    -- Tracking
    celery_task_id TEXT,
    created_at TIMESTAMPTZ DEFAULT NOW() NOT NULL,
    started_at TIMESTAMPTZ,
    completed_at TIMESTAMPTZ,
    
    -- Indexes defined below
    CONSTRAINT valid_completion CHECK (
        (status = 'complete' AND video_url IS NOT NULL) OR
        (status != 'complete')
    )
);

CREATE INDEX idx_video_jobs_user_id ON video_jobs(user_id);
CREATE INDEX idx_video_jobs_status ON video_jobs(status);
CREATE INDEX idx_video_jobs_created_at ON video_jobs(created_at DESC);
CREATE INDEX idx_video_jobs_job_id ON video_jobs(job_id);

-- RLS
ALTER TABLE video_jobs ENABLE ROW LEVEL SECURITY;

CREATE POLICY "Users can view own jobs"
    ON video_jobs FOR SELECT
    USING (auth.uid() = user_id);

CREATE POLICY "Service role can manage all jobs"
    ON video_jobs FOR ALL
    USING (auth.role() = 'service_role');

-- =============================================
-- PURCHASES: Payment history
-- =============================================
CREATE TABLE purchases (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    user_id UUID NOT NULL REFERENCES auth.users(id) ON DELETE CASCADE,
    
    -- Stripe data
    stripe_checkout_session_id TEXT UNIQUE,
    stripe_payment_intent_id TEXT,
    stripe_customer_id TEXT,
    stripe_subscription_id TEXT,
    
    -- Purchase details
    tier TEXT NOT NULL,
    minutes INTEGER NOT NULL,
    amount_cents INTEGER NOT NULL,
    currency TEXT DEFAULT 'usd',
    
    -- Status
    status TEXT NOT NULL DEFAULT 'pending'
        CHECK (status IN ('pending', 'completed', 'failed', 'refunded')),
    
    -- Type
    purchase_type TEXT DEFAULT 'one_time'
        CHECK (purchase_type IN ('one_time', 'subscription')),
    
    -- Timestamps
    created_at TIMESTAMPTZ DEFAULT NOW() NOT NULL,
    completed_at TIMESTAMPTZ,
    
    -- Prevent duplicate processing
    CONSTRAINT unique_payment_intent UNIQUE (stripe_payment_intent_id)
);

CREATE INDEX idx_purchases_user_id ON purchases(user_id);
CREATE INDEX idx_purchases_status ON purchases(status);
CREATE INDEX idx_purchases_stripe_session ON purchases(stripe_checkout_session_id);

-- RLS
ALTER TABLE purchases ENABLE ROW LEVEL SECURITY;

CREATE POLICY "Users can view own purchases"
    ON purchases FOR SELECT
    USING (auth.uid() = user_id);

-- =============================================
-- MINUTE TRANSACTIONS: Audit trail
-- =============================================
CREATE TABLE minute_transactions (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    user_id UUID NOT NULL REFERENCES auth.users(id) ON DELETE CASCADE,
    
    -- Transaction details
    amount NUMERIC(10,2) NOT NULL,  -- Positive = credit, Negative = debit
    balance_after NUMERIC(10,2) NOT NULL,
    
    -- Reference
    transaction_type TEXT NOT NULL
        CHECK (transaction_type IN ('purchase', 'usage', 'refund', 'adjustment', 'bonus')),
    reference_id UUID,  -- job_id or purchase_id
    reference_type TEXT,  -- 'video_job' or 'purchase'
    
    description TEXT,
    created_at TIMESTAMPTZ DEFAULT NOW() NOT NULL
);

CREATE INDEX idx_minute_transactions_user ON minute_transactions(user_id);
CREATE INDEX idx_minute_transactions_created ON minute_transactions(created_at DESC);

-- RLS
ALTER TABLE minute_transactions ENABLE ROW LEVEL SECURITY;

CREATE POLICY "Users can view own transactions"
    ON minute_transactions FOR SELECT
    USING (auth.uid() = user_id);
```

### Data Integrity Considerations

| Concern | Mitigation |
|---------|------------|
| Race condition on minutes deduction | Use database transaction with row lock |
| Duplicate payment processing | Unique constraint on `stripe_payment_intent_id` |
| Orphaned jobs | Foreign key with `ON DELETE CASCADE` |
| Missing profiles | Trigger creates profile on user signup |

**⚠️ Current gap:** Minutes deduction is not yet transactional. Need to implement:
```sql
BEGIN;
SELECT minutes_balance FROM profiles WHERE id = $1 FOR UPDATE;
-- Check if sufficient balance
UPDATE profiles SET minutes_balance = minutes_balance - $2 WHERE id = $1;
INSERT INTO minute_transactions (...);
COMMIT;
```

---

## Authentication & Authorization

### Auth Flow

```
┌─────────────────────────────────────────────────────────────────┐
│                      SUPABASE AUTH                              │
├─────────────────────────────────────────────────────────────────┤
│                                                                  │
│  ┌──────────┐    ┌──────────┐    ┌──────────┐                   │
│  │  Email/  │    │  Google  │    │  (Future)│                   │
│  │  Password│    │  OAuth   │    │  Apple   │                   │
│  └────┬─────┘    └────┬─────┘    └──────────┘                   │
│       │               │                                          │
│       └───────┬───────┘                                          │
│               ▼                                                  │
│       ┌──────────────┐                                           │
│       │ Supabase     │                                           │
│       │ Auth Server  │                                           │
│       └──────┬───────┘                                           │
│              │                                                   │
│              ▼                                                   │
│       ┌──────────────┐                                           │
│       │ JWT Token    │                                           │
│       │ (access +    │                                           │
│       │  refresh)    │                                           │
│       └──────────────┘                                           │
│                                                                  │
└─────────────────────────────────────────────────────────────────┘
```

### JWT Validation (Backend)

```python
# utils/auth.py
async def get_current_user(authorization: str = Header(...)):
    """
    Validates JWT token from Authorization header.
    Returns user payload or raises 401.
    """
    token = authorization.replace("Bearer ", "")
    
    # Verify with Supabase
    supabase = create_client(SUPABASE_URL, SUPABASE_SERVICE_KEY)
    user = supabase.auth.get_user(token)
    
    if not user:
        raise HTTPException(401, "Invalid token")
    
    return user.user
```

### Authorization Rules

| Resource | Rule |
|----------|------|
| Own profile | User can read/update |
| Own jobs | User can read |
| Own purchases | User can read |
| Other users' data | Blocked by RLS |
| Admin functions | Not implemented (⚠️ **TODO**) |

### Session Management

- **Access token:** 1 hour expiry
- **Refresh token:** 7 days expiry (configurable in Supabase)
- **Frontend:** Uses `onAuthStateChange` listener for auto-refresh
- **Backend:** Validates token on every request (stateless)

---

## Payment Processing

### Stripe Integration

**Products & Prices:**

| Tier | Minutes | One-time | Subscription |
|------|---------|----------|--------------|
| Starter | 10 | $2.00 | $1.50/mo |
| Standard | 50 | $8.00 | $6.00/mo |
| Pro | 120 | $15.00 | $12.00/mo |

### Checkout Flow

```
1. User clicks "Buy Now" in PricingModal
   │
   ▼
2. Frontend calls POST /api/payments/create-checkout
   ├── Includes: tier, mode (payment/subscription), success/cancel URLs
   └── Requires: JWT auth
   │
   ▼
3. API creates Stripe Checkout Session
   ├── Sets customer email from JWT
   ├── Sets metadata: user_id, tier, minutes
   └── Returns: checkout_url
   │
   ▼
4. Frontend redirects to Stripe Checkout
   │
   ▼
5. User completes payment on Stripe
   │
   ▼
6. Stripe redirects to success_url (/dashboard?success=true)
   │
   ▼
7. Stripe sends webhook to /api/payments/webhook
   ├── Event: checkout.session.completed
   ├── Verify signature with webhook secret
   ├── Extract metadata (user_id, minutes)
   ├── Credit minutes to user profile
   └── Create purchase record
```

### Webhook Security

```python
@router.post("/webhook")
async def stripe_webhook(request: Request):
    payload = await request.body()
    sig_header = request.headers.get("stripe-signature")
    
    try:
        event = stripe.Webhook.construct_event(
            payload, sig_header, STRIPE_WEBHOOK_SECRET
        )
    except ValueError:
        raise HTTPException(400, "Invalid payload")
    except stripe.error.SignatureVerificationError:
        raise HTTPException(400, "Invalid signature")
    
    # Process event...
```

### ⚠️ Current Webhook Status: NOT IMPLEMENTED

**Critical TODO:**
- [ ] Implement `/api/payments/webhook` endpoint
- [ ] Handle `checkout.session.completed` event
- [ ] Handle `invoice.paid` for subscriptions
- [ ] Handle `customer.subscription.deleted`
- [ ] Idempotency check (don't double-credit)

---

## Task Queue Architecture

### Celery Configuration

```python
# celery_app.py
celery_app.conf.update(
    # Serialization
    task_serializer="json",
    accept_content=["json"],
    result_serializer="json",
    
    # Reliability
    task_acks_late=True,              # ACK after completion
    task_reject_on_worker_lost=True,  # Re-queue on crash
    
    # Timeouts
    task_time_limit=600,              # 10 min hard limit
    task_soft_time_limit=540,         # 9 min soft limit
    
    # Concurrency
    worker_prefetch_multiplier=1,     # Grab 1 at a time
    worker_concurrency=2,             # 2 parallel tasks
    
    # Results
    result_expires=86400,             # 24 hour expiry
)
```

### Task Definition

```python
# tasks.py
@celery_app.task(bind=True, name="tasks.generate_video")
def generate_video(self, job_id: str, script_data: dict, voice: str, user_id: str):
    """
    Renders a video from parsed problem data.
    
    Progress updates via self.update_state().
    """
    try:
        self.update_state(state="PROCESSING", meta={"progress": 10})
        
        # ... render video ...
        
        return {"status": "complete", "video_url": url}
        
    except SoftTimeLimitExceeded:
        return {"status": "failed", "error": "Timeout"}
```

### Failure Modes

| Failure | Behavior |
|---------|----------|
| Worker crashes mid-task | Task re-queued (acks_late) |
| Task exceeds 10 min | Killed, marked failed |
| Redis connection lost | Workers retry connection |
| API can't reach Redis | Job queued locally (fallback) |

---

## Video Generation Pipeline

### Parser (DeepSeek/GPT-4)

**Input:**
```
"Solve for x: 2x + 5 = 11"
```

**Output:**
```json
{
  "meta": {
    "problem": "Solve for x: 2x + 5 = 11",
    "latex": "2x + 5 = 11",
    "type": "linear_equation"
  },
  "steps": [
    {
      "narration": "Let's solve this equation step by step. We start with 2x plus 5 equals 11.",
      "latex": "2x + 5 = 11",
      "action": "show"
    },
    {
      "narration": "First, subtract 5 from both sides.",
      "latex": "2x = 6",
      "action": "transform"
    },
    {
      "narration": "Now divide both sides by 2.",
      "latex": "x = 3",
      "action": "transform"
    },
    {
      "narration": "Therefore, x equals 3.",
      "latex": "x = 3",
      "action": "highlight"
    }
  ]
}
```

### Voice Generation (Fish Audio)

- **API:** Fish Audio TTS
- **Voices:** Multiple options (allison, etc.)
- **Format:** MP3
- **Rate:** ~150 words/minute

### Animation (Manim)

- **Library:** Manim Community Edition
- **Resolution:** 1080p (configurable)
- **FPS:** 30
- **Style:** Clean, educational

### Composition (FFmpeg)

```bash
ffmpeg -i animation.mp4 -i narration.mp3 \
  -c:v copy -c:a aac \
  -map 0:v:0 -map 1:a:0 \
  output.mp4
```

---

## API Specification

### Endpoints

| Method | Path | Auth | Description |
|--------|------|------|-------------|
| GET | `/health` | No | Health check |
| POST | `/parse` | Yes | Parse problem (free preview) |
| POST | `/solve` | Yes | Submit video job |
| GET | `/job/{job_id}` | Yes | Get job status |
| GET | `/jobs` | Yes | List user's jobs |
| POST | `/api/payments/create-checkout` | Yes | Create Stripe session |
| POST | `/api/payments/webhook` | No* | Stripe webhook |

*Webhook uses Stripe signature verification instead of JWT.

### Request/Response Examples

**POST /solve**
```json
// Request
{
  "problem": "Solve 2x + 5 = 11",
  "voice": "allison"
}

// Response (202 Accepted)
{
  "job_id": "abc12345",
  "status": "pending",
  "message": "Video queued: Solve 2x + 5 = 11..."
}
```

**GET /job/{job_id}**
```json
// Response (processing)
{
  "job_id": "abc12345",
  "status": "processing",
  "progress": 60,
  "progress_message": "Rendering video...",
  "created_at": "2026-02-14T08:00:00Z"
}

// Response (complete)
{
  "job_id": "abc12345",
  "status": "complete",
  "video_url": "https://r2.example.com/videos/abc12345.mp4",
  "created_at": "2026-02-14T08:00:00Z",
  "completed_at": "2026-02-14T08:01:30Z"
}
```

### Error Responses

```json
// 400 Bad Request
{
  "detail": "Must provide either 'problem' or 'image'"
}

// 401 Unauthorized
{
  "detail": "Invalid or expired token"
}

// 403 Forbidden
{
  "detail": "Not authorized to view this job"
}

// 500 Internal Server Error
{
  "detail": "Failed to parse problem: [error message]"
}
```

---

## Security Considerations

### Current Security Measures

| Measure | Status | Notes |
|---------|--------|-------|
| HTTPS | ✅ | Enforced by Vercel/Railway |
| JWT validation | ✅ | On all protected endpoints |
| CORS allowlist | ✅ | Only known origins |
| RLS on database | ✅ | Users see only own data |
| Stripe signature verification | ⚠️ | Endpoint not implemented |
| Input validation | ⚠️ | Basic (Pydantic models) |
| Rate limiting | ❌ | Not implemented |
| SQL injection prevention | ✅ | Supabase client parameterized |
| XSS prevention | ✅ | React auto-escapes |
| CSRF protection | ✅ | JWT-based (no cookies) |

### Security Gaps (TODO)

1. **Rate Limiting**
   - No rate limiting on any endpoint
   - Risk: DoS, cost abuse (AI API calls)
   - Recommendation: Add Redis-based rate limiting
   ```python
   # Example: 10 requests per minute per user
   @limiter.limit("10/minute")
   async def solve(...):
   ```

2. **Input Sanitization**
   - Problem text passed directly to AI
   - Risk: Prompt injection
   - Recommendation: Sanitize/validate input patterns

3. **API Key Exposure**
   - AI API keys in environment variables
   - Risk: If server compromised, keys exposed
   - Recommendation: Use secrets manager, rotate keys

4. **Admin Endpoints**
   - No admin authentication
   - Risk: Can't manage users/jobs
   - Recommendation: Add admin role + endpoints

5. **Webhook Idempotency**
   - Stripe webhooks can retry
   - Risk: Double-credit minutes
   - Recommendation: Check `stripe_payment_intent_id` uniqueness

---

## Error Handling

### Error Categories

| Category | Example | Handling |
|----------|---------|----------|
| Validation | Missing problem | 400 + clear message |
| Auth | Invalid token | 401 + redirect to login |
| Authorization | Wrong user's job | 403 |
| Not Found | Unknown job_id | 404 |
| External API | DeepSeek timeout | Retry with backoff |
| Render failure | Manim error | Mark job failed, notify user |
| Infra | Redis down | Fallback to sync processing |

### Retry Logic

```python
# AI API calls with retry
@retry(
    stop=stop_after_attempt(3),
    wait=wait_exponential(multiplier=1, min=2, max=10),
    retry=retry_if_exception_type(RateLimitError)
)
def call_deepseek(prompt):
    ...
```

### User-Facing Errors

- Failed jobs show error message in UI
- Polling continues even after failure (to get error details)
- No automatic retry from user perspective (must resubmit)

---

## Scalability & Performance

### Current Bottlenecks

| Component | Bottleneck | Impact | Solution |
|-----------|------------|--------|----------|
| API | Single instance | ~100 concurrent users | Horizontal scaling |
| Workers | CPU-bound rendering | ~2-4 videos/worker | Add more workers |
| Redis | Memory | Queue backup if workers slow | Monitor queue depth |
| AI APIs | Rate limits | Throttled requests | Request queuing |
| R2 | None | N/A | CDN handles load |

### Scaling Strategy

```
PHASE 1 (MVP): Single API + 1-2 workers
├── Handles: ~100 users/day, ~500 videos/day
└── Cost: ~$20-50/month

PHASE 2 (Growth): Multiple API + 4-8 workers  
├── Handles: ~1000 users/day, ~5000 videos/day
└── Cost: ~$100-300/month

PHASE 3 (Scale): Auto-scaling workers
├── Handles: 10K+ users/day
├── Workers scale based on queue depth
└── Cost: Variable based on usage
```

### Performance Targets

| Metric | Current | Target | Strategy |
|--------|---------|--------|----------|
| API response (submit) | <500ms | <200ms | Already fast |
| Queue wait | Varies | <5s | Scale workers |
| Video render | 30-90s | <20s | Pipeline optimization |
| Video delivery | N/A | <2s | CDN (R2) |

### Video Render Optimization Ideas

1. **Pre-render common elements** — Cache axes, grids, symbols
2. **Lower resolution** — 720p vs 1080p (2-4x faster)
3. **Simpler animations** — Reduce Manim complexity
4. **GPU rendering** — If Manim supports
5. **Audio streaming** — Don't wait for full TTS
6. **Problem caching** — Same problem = same video

---

## Monitoring & Observability

### Current State: Minimal

- Basic health endpoint
- Console logging
- No metrics, no alerts, no dashboards

### Recommended Additions

1. **Structured Logging**
   ```python
   import structlog
   logger = structlog.get_logger()
   logger.info("job_submitted", job_id=job_id, user_id=user_id)
   ```

2. **Metrics (Prometheus)**
   - `orbital_jobs_total` (counter, by status)
   - `orbital_job_duration_seconds` (histogram)
   - `orbital_queue_depth` (gauge)
   - `orbital_api_requests_total` (counter, by endpoint)

3. **Alerting**
   - Queue depth > 100 jobs
   - Error rate > 5%
   - API latency p99 > 1s
   - Worker down

4. **Dashboards (Grafana)**
   - Request rate
   - Error rate
   - Queue depth
   - Job processing time
   - Revenue (jobs * minutes)

5. **Celery Monitoring (Flower)**
   ```bash
   celery -A celery_app flower --port=5555
   ```

---

## Infrastructure & Deployment

### Current Deployment

| Component | Platform | Status |
|-----------|----------|--------|
| Frontend | Vercel | ✅ Live |
| API | Railway | ❌ Not deployed |
| Workers | Railway | ❌ Not deployed |
| Redis | Railway | ❌ Not provisioned |
| Database | Supabase | ✅ Live |
| Storage | R2 | ❌ Not configured |

### CI/CD

**Frontend (Vercel):**
- Auto-deploy on push to `main`
- Preview deploys on PRs
- No manual steps

**Backend (Railway):**
- Will auto-deploy on push (when configured)
- Procfile defines services:
  ```
  web: uvicorn main:app --host 0.0.0.0 --port $PORT
  worker: celery -A celery_app worker --loglevel=info
  ```

### Environment Variables Required

**Frontend:**
```
NEXT_PUBLIC_SUPABASE_URL
NEXT_PUBLIC_SUPABASE_ANON_KEY
NEXT_PUBLIC_API_URL
```

**Backend:**
```
# Supabase
SUPABASE_URL
SUPABASE_SERVICE_KEY

# AI
OPENAI_API_KEY (or DEEPSEEK_API_KEY)
FISH_AUDIO_API_KEY

# Stripe
STRIPE_SECRET_KEY
STRIPE_WEBHOOK_SECRET

# Queue
REDIS_URL
CELERY_ENABLED=true
USE_SUPABASE_JOBS=true

# Storage (future)
R2_ACCESS_KEY_ID
R2_SECRET_ACCESS_KEY
R2_BUCKET
R2_ENDPOINT
```

---

## Known Limitations & Technical Debt

### Critical

| Issue | Impact | Priority |
|-------|--------|----------|
| No Stripe webhook | Payments don't credit minutes | P0 |
| No rate limiting | DoS/cost risk | P0 |
| In-memory jobs (local) | Lost on restart | P1 (prod uses Supabase) |
| No admin panel | Can't manage users | P2 |

### Technical Debt

| Issue | Impact | Priority |
|-------|--------|----------|
| No tests | Regressions | P1 |
| No CI pipeline | Manual verification | P2 |
| Hardcoded config | Inflexible | P2 |
| No API versioning | Breaking changes | P2 |
| No input validation | Bad data | P2 |
| Single-region deploy | Latency for distant users | P3 |

### Missing Features

| Feature | Impact | Priority |
|---------|--------|----------|
| Video download | User requests | P1 |
| Video deletion | Storage costs | P2 |
| Subscription management | Churn handling | P2 |
| Usage analytics | Business insights | P3 |
| Multi-language | International users | P3 |

---

## Open Questions

### Architecture

1. **Webhook reliability** — What if webhook fails? Manual reconciliation?
2. **Video retention** — How long to keep videos? Auto-delete policy?
3. **Subscription billing** — What happens if payment fails mid-cycle?
4. **Multi-tenant** — Will we support teams/organizations?

### Performance

1. **Render optimization** — What's the realistic floor for video render time?
2. **Caching** — Should we cache identical problems?
3. **Geographic distribution** — Do we need multi-region workers?

### Security

1. **Prompt injection** — How do we prevent malicious problem inputs?
2. **Content moderation** — What if someone submits inappropriate content?
3. **Abuse prevention** — How do we handle accounts that abuse the system?

### Business

1. **Refund policy** — When do we refund minutes?
2. **Enterprise tier** — Different pricing for schools/institutions?
3. **Offline support** — iOS app needs connectivity?

---

## Appendix: Local Development

### Prerequisites
- Python 3.11+
- Node.js 18+
- Docker (for Redis)

### Frontend
```bash
cd ~/Desktop/Orbital/orbital_site
npm install
npm run dev  # http://localhost:3000
```

### Backend (Simple Mode)
```bash
cd ~/Desktop/Orbital/orbital_api
python -m venv venv
source venv/bin/activate
pip install -r requirements.txt
uvicorn main:app --reload --port 8002
```

### Backend (With Celery)
```bash
# Terminal 1: Redis
docker run -p 6379:6379 redis

# Terminal 2: API
CELERY_ENABLED=true uvicorn main:app --reload --port 8002

# Terminal 3: Worker
celery -A celery_app worker --loglevel=info
```

---

*Document prepared for senior developer review.*
*Questions: [contact info]*
