# Stripe Integration Audit - Orbital

**Date:** 2025-02-13  
**Auditor:** QA Subagent

---

## Summary

| Area | Status | Issues |
|------|--------|--------|
| Checkout API (Next.js) | ✅ Solid | Minor - env vars need local setup |
| PricingModal (UI) | ⚠️ Concern | Hardcoded price IDs not used by API |
| Webhook Handling | ✅ Secure | Proper signature verification |
| Token Validation | ✅ Secure | Supabase JWT verification |
| Python API | ✅ Well-built | Comprehensive implementation |

**Overall:** Good implementation with proper security. A few cleanup items.

---

## 1. Next.js Checkout API

**File:** `src/app/api/payments/create-checkout/route.ts`

### ✅ What's Good

- **Lazy Stripe initialization** - Prevents build errors when env vars unavailable
- **Proper auth check** - Bearer token validation before processing
- **Supabase JWT verification** - Uses `getUser(token)` to validate user
- **Metadata tracking** - Includes user_id, tier, minutes, mode in session
- **Error handling** - Catches and sanitizes errors appropriately
- **Promotion codes** - Enabled for subscriptions

### ⚠️ Issues

1. **Missing env vars locally** - `.env.local` doesn't have any Stripe vars:
   ```
   # Current .env.local only has:
   NEXT_PUBLIC_SUPABASE_URL=<SET>
   NEXT_PUBLIC_SUPABASE_ANON_KEY=<SET>
   NEXT_PUBLIC_API_URL=<SET>
   
   # Missing for local dev:
   STRIPE_SECRET_KEY
   STRIPE_PRICE_STARTER / STANDARD / PRO
   STRIPE_PRICE_STARTER_SUB / STANDARD_SUB / PRO_SUB
   ```
   
   **Impact:** Local dev will fail if trying to use Next.js checkout route.  
   **Note:** These may be configured in Vercel dashboard for production.

2. **Non-null assertions (`!`)** - Price IDs use `!` which could crash at runtime:
   ```typescript
   priceId: process.env.STRIPE_PRICE_STARTER!
   ```
   Better to validate at checkout time (which it does with the `if (!priceConfig.priceId)` check).

---

## 2. PricingModal (UI)

**File:** `src/components/PricingModal.tsx`

### ⚠️ Hardcoded Price IDs

The frontend has price IDs hardcoded:
```typescript
const TIERS: Record<string, Tier> = {
  starter: {
    oneTime: { price: 2, priceId: "price_1SzmKKBDEgxKWlDL2k0V7nYG" },
    subscription: { price: 1.5, priceId: "price_1SzmKmBDEgxKWlDLlvmHBMPb" },
  },
  standard: {
    oneTime: { price: 8, priceId: "price_1SzmMWBDEgxKWlDLwy7yInQv" },
    subscription: { price: 6, priceId: "price_1SzmNOBDEgxKWlDLgRje5FeR" },
  },
  pro: {
    oneTime: { price: 15, priceId: "price_1SzmQpBDEgxKWlDLJnvwG9e1" },
    subscription: { price: 12, priceId: "price_1SzmRWBDEgxKWlDLiUwiNxPQ" },
  },
};
```

**Assessment:** 
- These price IDs are **NOT sent to the API** - the frontend only sends `tier` and `mode`
- The backend uses environment variables for actual price IDs
- The hardcoded IDs are essentially **dead code** (display-only, not functional)

**Recommendation:** Remove unused `priceId` from frontend types, or fetch prices from `/api/payments/prices` endpoint.

### ✅ What's Good

- **Session handling** - Gets fresh token before each request
- **Safari bfcache handling** - Detects back-button and prompts refresh
- **Loading states** - Proper UX during checkout
- **Success/cancel URLs** - Correctly use dashboard paths:
  ```typescript
  success_url: `${window.location.origin}/dashboard?success=true`,
  cancel_url: `${window.location.origin}/dashboard?canceled=true`,
  ```
- **Mode mapping** - Correctly maps `one_time` → `payment`, `subscription` → `subscription`

---

## 3. Python API (payments.py)

**File:** `routes/payments.py`

### ✅ Excellent Implementation

1. **Webhook Security** - Proper signature verification:
   ```python
   if not STRIPE_WEBHOOK_SECRET:
       raise HTTPException(
           status_code=500, 
           detail="Webhook secret not configured. Cannot process webhooks securely."
       )
   
   event = stripe.Webhook.construct_event(
       payload, sig_header, STRIPE_WEBHOOK_SECRET
   )
   ```

2. **Handled Events:**
   - `checkout.session.completed` - Initial payment (one-time & subscription)
   - `invoice.paid` - Subscription renewals
   - `customer.subscription.deleted` - Cancellations
   
3. **Subscription Logic:**
   - Prevents duplicate subscriptions
   - Stores `stripe_customer_id`, `stripe_subscription_id`, `subscription_tier`
   - Handles cancel-at-period-end properly

4. **Idempotency:** Uses `stripe_session_id` in `add_minutes` RPC (prevents double-crediting)

5. **Additional Endpoints:**
   - `/subscription-status` - Check active subscription
   - `/cancel-subscription` - Graceful cancellation
   - `/history` - Purchase history
   - `/balance` - Minutes balance
   - `/prices` - Public pricing info

### Environment Variables Configured

```
STRIPE_SECRET_KEY=<SET>
STRIPE_WEBHOOK_SECRET=<SET>
STRIPE_PRICE_STARTER=<SET>
STRIPE_PRICE_STANDARD=<SET>
STRIPE_PRICE_PRO=<SET>
STRIPE_PRICE_STARTER_SUB=<SET>
STRIPE_PRICE_STANDARD_SUB=<SET>
STRIPE_PRICE_PRO_SUB=<SET>
```

All required Stripe vars are properly configured in Python API's `.env`.

---

## 4. Price ID Verification

**Question:** Do the hardcoded frontend prices match the backend?

| Tier | Frontend One-time | Frontend Sub | Backend (env) |
|------|-------------------|--------------|---------------|
| Starter | `price_1SzmKK...` | `price_1SzmKm...` | From ENV |
| Standard | `price_1SzmMW...` | `price_1SzmNO...` | From ENV |
| Pro | `price_1SzmQp...` | `price_1SzmRW...` | From ENV |

**Cannot verify match** - Backend uses env vars, not hardcoded values. The frontend price IDs are unused in API calls, so any mismatch wouldn't affect functionality.

**Recommendation:** Verify in Stripe dashboard that the price IDs in Python `.env` match what's displayed in frontend (for consistency).

---

## 5. Security Assessment

### ✅ Token Validation

Both Next.js and Python APIs validate tokens securely:

**Next.js:**
```typescript
const { data: { user }, error } = await supabase.auth.getUser(token);
if (authError || !user) {
  return NextResponse.json({ detail: 'Invalid token' }, { status: 401 });
}
```

**Python:**
```python
user = supabase.auth.get_user(token)
if not user or not user.user:
    raise HTTPException(status_code=401, detail="Invalid token")
```

### ✅ Webhook Security

- Signature verification required
- Fails safely if secret not configured
- Uses Stripe's official SDK verification

### ⚠️ Minor Concerns

1. **Error message leakage** - Some errors pass through raw:
   ```python
   raise HTTPException(status_code=401, detail=str(e))
   ```
   Could potentially expose internal error details.

2. **No rate limiting** - Checkout endpoint has no rate limiting (could be abused to create many Stripe sessions)

---

## 6. Recommendations

### High Priority

1. **Add Stripe env vars to Next.js `.env.local`** for local development
2. **Remove unused `priceId` from PricingModal types** to avoid confusion
3. **Verify price IDs match** between Python `.env` and Stripe dashboard

### Medium Priority

4. **Add rate limiting** to checkout endpoints (e.g., 5 requests/minute/user)
5. **Sanitize error messages** in auth failures
6. **Consider using `/api/payments/prices`** endpoint to dynamically load prices in frontend

### Low Priority

7. **Create `.env.example`** for Next.js site documenting all required vars
8. **Add logging** for successful checkouts in Next.js route (currently only errors logged)

---

## Architecture Note

The system has **two** checkout endpoints:
1. **Next.js:** `/api/payments/create-checkout` (route.ts)
2. **Python:** `/payments/create-checkout` (payments.py)

The PricingModal calls the **Next.js** endpoint (relative `/api/payments/create-checkout`).

Both implementations are largely identical and properly secured. The Python API additionally handles webhooks and has more comprehensive subscription management.

**Consider:** Consolidating to use only the Python API for payments to avoid maintaining duplicate code.

---

## Conclusion

The Stripe integration is **well-implemented and secure**. The main issues are:
- Configuration (missing local env vars)
- Code cleanliness (unused hardcoded price IDs)
- Minor security hardening (rate limiting, error sanitization)

No critical security vulnerabilities found. Payment flows, webhook handling, and token validation are all properly implemented.
