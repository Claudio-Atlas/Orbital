# Orbital Professional Audit

## Current State Assessment

### 🔴 Critical Issues

1. **Mock data in production** - Dashboard shows fake 47.5 minutes
2. **Stripe checkout** - Status unknown, needs testing
3. **No error boundaries** - JS errors cause blank screens
4. **No proper loading states** - Spinners but no context

### 🟡 Architecture Concerns

1. **Auth flow complexity** - Middleware + client-side checks = race conditions
2. **No centralized error handling**
3. **No logging/monitoring**
4. **Environment variables scattered**

---

## What a World-Class Builder Would Do

### Phase 1: Foundation Cleanup (Do First)

#### 1.1 Remove All Mock Data
- [ ] Remove MOCK_USER from dashboard
- [ ] Remove MOCK_VIDEOS from dashboard  
- [ ] Show real data or proper empty states
- [ ] 0 minutes = "0 minutes" not fake number

#### 1.2 Proper Loading States
- [ ] "Loading your dashboard..." not just spinner
- [ ] Skeleton loaders for content areas
- [ ] Clear feedback on what's happening

#### 1.3 Error Boundaries
- [ ] Global error boundary component
- [ ] Graceful error pages, not blank screens
- [ ] User-friendly error messages

#### 1.4 Environment Variable Audit
```
REQUIRED FOR FRONTEND (NEXT_PUBLIC_*):
- NEXT_PUBLIC_SUPABASE_URL
- NEXT_PUBLIC_SUPABASE_ANON_KEY

REQUIRED FOR API ROUTES (server-side):
- STRIPE_SECRET_KEY
- STRIPE_PRICE_STARTER
- STRIPE_PRICE_STANDARD
- STRIPE_PRICE_PRO
- STRIPE_PRICE_STARTER_SUB
- STRIPE_PRICE_STANDARD_SUB
- STRIPE_PRICE_PRO_SUB
```

### Phase 2: Auth Hardening

#### 2.1 Simplify Auth Flow
Current: Middleware + useAuth hook + component checks = confusion

Recommended:
- Middleware: ONLY check cookies, redirect if missing
- useAuth: ONLY provide user state to components
- Components: ONLY render UI based on state (no navigation logic)

#### 2.2 Session Handling
- [ ] Proper session refresh
- [ ] Handle expired sessions gracefully
- [ ] Clear error messages for auth failures

#### 2.3 Sign Out Flow
- [ ] Clear all cookies
- [ ] Clear local storage
- [ ] Redirect to home
- [ ] No race conditions

### Phase 3: Stripe Integration

#### 3.1 Checkout Flow
- [ ] Verify env vars are set in Vercel
- [ ] Test each tier (starter/standard/pro)
- [ ] Test one-time vs subscription
- [ ] Handle success redirect
- [ ] Handle cancel redirect
- [ ] Handle back button

#### 3.2 Webhook Setup
- [ ] Create webhook endpoint
- [ ] Configure in Stripe dashboard
- [ ] Handle checkout.session.completed
- [ ] Credit minutes to user account
- [ ] Handle subscription renewals
- [ ] Handle cancellations

#### 3.3 User Balance
- [ ] Create `profiles` table with `minutes_balance`
- [ ] RPC function to add minutes (atomic)
- [ ] Display real balance, not mock

### Phase 4: Database Schema

#### Required Tables
```sql
-- profiles (extends Supabase auth.users)
CREATE TABLE profiles (
  id UUID PRIMARY KEY REFERENCES auth.users(id),
  email TEXT,
  display_name TEXT,
  minutes_balance DECIMAL DEFAULT 0,
  stripe_customer_id TEXT,
  stripe_subscription_id TEXT,
  subscription_tier TEXT,
  created_at TIMESTAMPTZ DEFAULT NOW(),
  updated_at TIMESTAMPTZ DEFAULT NOW()
);

-- purchases (transaction log)
CREATE TABLE purchases (
  id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
  user_id UUID REFERENCES profiles(id),
  stripe_session_id TEXT UNIQUE,
  tier TEXT,
  minutes DECIMAL,
  amount_cents INTEGER,
  mode TEXT, -- 'payment' or 'subscription'
  created_at TIMESTAMPTZ DEFAULT NOW()
);

-- videos (user's generated videos)
CREATE TABLE videos (
  id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
  user_id UUID REFERENCES profiles(id),
  problem TEXT,
  problem_type TEXT, -- 'latex' or 'text'
  status TEXT, -- 'pending', 'processing', 'complete', 'error'
  video_url TEXT,
  thumbnail_url TEXT,
  minutes_used DECIMAL,
  created_at TIMESTAMPTZ DEFAULT NOW(),
  expires_at TIMESTAMPTZ
);
```

#### RPC Functions
```sql
-- Atomic minute addition (prevents race conditions)
CREATE OR REPLACE FUNCTION add_minutes(
  p_user_id UUID,
  p_minutes DECIMAL,
  p_amount_cents INTEGER,
  p_tier TEXT,
  p_stripe_session_id TEXT
) RETURNS void AS $$
BEGIN
  -- Update balance
  UPDATE profiles 
  SET minutes_balance = minutes_balance + p_minutes,
      updated_at = NOW()
  WHERE id = p_user_id;
  
  -- Log purchase
  INSERT INTO purchases (user_id, stripe_session_id, tier, minutes, amount_cents, mode)
  VALUES (p_user_id, p_stripe_session_id, p_tier, p_minutes, p_amount_cents, 'payment');
END;
$$ LANGUAGE plpgsql;
```

### Phase 5: Security Audit

#### 5.1 API Routes
- [ ] All routes validate auth token
- [ ] Rate limiting on sensitive endpoints
- [ ] Input validation on all endpoints
- [ ] No sensitive data in error messages

#### 5.2 Client-Side
- [ ] No secrets in client code
- [ ] No sensitive data in localStorage
- [ ] HTTPS only
- [ ] Proper CORS if needed

#### 5.3 Supabase RLS
- [ ] RLS enabled on all tables
- [ ] Users can only read their own data
- [ ] Users can only update their own profile
- [ ] Service role key only on server

### Phase 6: Testing Checklist

#### Auth Flows
- [ ] Sign up with email/password
- [ ] Sign up with Google OAuth
- [ ] Login with email/password
- [ ] Login with Google OAuth
- [ ] Forgot password flow
- [ ] Password reset flow
- [ ] Sign out from dashboard
- [ ] Sign out from other pages
- [ ] Session persists on refresh
- [ ] Protected routes redirect when not logged in

#### Stripe Flows
- [ ] Open pricing modal
- [ ] Select starter one-time → checkout → success
- [ ] Select standard one-time → checkout → success
- [ ] Select pro one-time → checkout → success
- [ ] Subscription checkout works
- [ ] Cancel on Stripe returns properly
- [ ] Back button from Stripe works
- [ ] Minutes credited after purchase

#### Edge Cases
- [ ] Multiple browser tabs
- [ ] Incognito mode
- [ ] Mobile browser
- [ ] Safari specific issues
- [ ] Network interruption during checkout

---

## Immediate Action Plan

### Today (30 minutes)
1. [ ] Remove mock data from dashboard
2. [ ] Verify Stripe env vars in Vercel
3. [ ] Test basic checkout flow
4. [ ] Fix any immediate blockers

### This Week
1. [ ] Implement proper error boundaries
2. [ ] Set up Stripe webhook
3. [ ] Create/verify database tables
4. [ ] Full auth flow testing

### Before Launch
1. [ ] Security audit complete
2. [ ] All test cases passing
3. [ ] Error monitoring set up
4. [ ] Performance check

---

## Questions to Answer

1. Is the Supabase `profiles` table created with `minutes_balance`?
2. Is the `add_minutes` RPC function created?
3. Are all Stripe env vars in Vercel?
4. Is the Stripe webhook configured?

Let's verify these one by one.
