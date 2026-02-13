# Supabase Configuration Audit

**Project URL:** https://pqwhfiuvcsjfevjwljml.supabase.co  
**Audit Date:** 2026-02-12  
**Status:** ✅ PASS

---

## 1. Tables & Schemas

### `profiles` Table ✅
Links to `auth.users` via id (ON DELETE CASCADE)

| Column | Type | Default | Notes |
|--------|------|---------|-------|
| id | uuid | - | PK, references auth.users |
| email | text | - | Required |
| minutes_balance | decimal(10,2) | 0 | Current balance |
| total_minutes_purchased | decimal(10,2) | 0 | Lifetime total |
| total_spent_cents | integer | 0 | Lifetime spending |
| created_at | timestamptz | now() | - |
| updated_at | timestamptz | now() | - |
| stripe_customer_id | text | null | Stripe customer |
| stripe_subscription_id | text | null | Active subscription |
| subscription_tier | text | null | 'starter'/'standard'/'pro' |

**Current Data:** 2 users registered (test accounts)

### `videos` Table ✅
Stores generated math videos

| Column | Type | Default | Notes |
|--------|------|---------|-------|
| id | uuid | gen_random_uuid() | PK |
| user_id | uuid | - | FK → profiles.id |
| problem_text | text | - | Required |
| problem_type | text | null | 'algebra', 'calculus', etc. |
| minutes_used | decimal(10,2) | - | Required |
| character_count | integer | - | Required |
| steps_count | integer | null | - |
| video_url | text | null | R2 URL |
| video_key | text | null | R2 object key |
| thumbnail_url | text | null | - |
| status | text | 'generating' | 'generating'/'complete'/'failed'/'expired' |
| error_message | text | null | - |
| expires_at | timestamptz | - | Required (48h expiry) |
| emailed | boolean | false | - |
| emailed_at | timestamptz | null | - |
| created_at | timestamptz | now() | - |

**Current Data:** 0 videos (no generations yet)

### `purchases` Table ✅
Tracks minute purchases

| Column | Type | Default | Notes |
|--------|------|---------|-------|
| id | uuid | gen_random_uuid() | PK |
| user_id | uuid | - | FK → profiles.id |
| tier | text | - | Required |
| minutes_added | decimal(10,2) | - | Required |
| amount_cents | integer | - | Required |
| stripe_payment_intent_id | text | null | - |
| stripe_checkout_session_id | text | null | UNIQUE constraint (idempotency) |
| status | text | 'completed' | 'pending'/'completed'/'refunded' |
| created_at | timestamptz | now() | - |

**Current Data:** 0 purchases (no transactions yet)

---

## 2. Row Level Security (RLS) ✅

### RLS Verification Test
| Table | Anon Key | Service Key | Status |
|-------|----------|-------------|--------|
| profiles | `[]` (blocked) | Returns data | ✅ Working |
| videos | `[]` (blocked) | Returns data | ✅ Working |
| purchases | `[]` (blocked) | Returns data | ✅ Working |

### RLS Policies

#### profiles
- `Users can view own profile` - SELECT where `auth.uid() = id`
- `Users can update own profile` - UPDATE where `auth.uid() = id`

#### purchases
- `Users can view own purchases` - SELECT where `auth.uid() = user_id`

#### videos
- `Users can view own videos` - SELECT where `auth.uid() = user_id`
- `Users can insert own videos` - INSERT where `auth.uid() = user_id`

**Assessment:** All policies correctly restrict access to owned data only.

---

## 3. Authentication Settings ✅

### Enabled Providers
| Provider | Status |
|----------|--------|
| Email | ✅ Enabled |
| Google OAuth | ✅ Enabled |
| Phone | ❌ Disabled |
| Other OAuth | ❌ All disabled |

### Settings
- **Signup:** ✅ Enabled (`disable_signup: false`)
- **Email Confirmation:** ✅ Required (`mailer_autoconfirm: false`)
- **Anonymous Users:** ❌ Disabled (correct for paid service)

**Assessment:** Configuration appropriate for Orbital's use case (email/Google signup with confirmation required).

---

## 4. Database Functions ✅

### `handle_new_user()` - Trigger Function
- **Purpose:** Auto-creates profile when user signs up
- **Trigger:** Fires AFTER INSERT on `auth.users`
- **Security:** SECURITY DEFINER

### `deduct_minutes(p_user_id, p_minutes)` → BOOLEAN
- **Purpose:** Safely deduct minutes with balance check
- **Features:**
  - Row lock (`FOR UPDATE`) prevents race conditions
  - Returns `FALSE` if insufficient balance
  - Updates `updated_at` timestamp
- **Security:** SECURITY DEFINER
- **Exposed via:** `/rpc/deduct_minutes`

### `add_minutes(p_user_id, p_minutes, p_amount_cents, p_tier, p_stripe_session_id)` → UUID
- **Purpose:** Add minutes after successful purchase
- **Features:**
  - **Idempotent:** Checks for existing `stripe_checkout_session_id` first
  - Returns existing purchase ID if duplicate request
  - Creates purchase record
  - Updates profile totals
- **Security:** SECURITY DEFINER
- **Exposed via:** `/rpc/add_minutes`

**Assessment:** Functions correctly handle atomic operations with proper idempotency for payment processing.

---

## 5. Indexes ✅

| Table | Index | Purpose |
|-------|-------|---------|
| purchases | `idx_purchases_user_id` | User lookup |
| videos | `idx_videos_user_id` | User lookup |
| videos | `idx_videos_expires_at` | Cleanup queries |
| videos | `idx_videos_status` | Status filtering |

---

## 6. Schema Drift Note ⚠️

The `profiles` table in **production** has 3 columns not in `database/schema.sql`:
- `stripe_customer_id`
- `stripe_subscription_id`  
- `subscription_tier`

**Recommendation:** Update `schema.sql` to match production:

```sql
-- Add after total_spent_cents line:
stripe_customer_id TEXT,
stripe_subscription_id TEXT,
subscription_tier TEXT
```

---

## Summary

| Category | Status | Notes |
|----------|--------|-------|
| Tables | ✅ PASS | 3 tables, correct schemas |
| RLS | ✅ PASS | All tables protected, policies correct |
| Auth | ✅ PASS | Email + Google, confirmation required |
| Functions | ✅ PASS | add_minutes, deduct_minutes with idempotency |
| Indexes | ✅ PASS | Appropriate indexes exist |
| Schema Sync | ⚠️ WARN | schema.sql missing Stripe subscription columns |

**Overall: Supabase configuration is production-ready.**
