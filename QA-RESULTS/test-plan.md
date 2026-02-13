# Orbital Site - End-to-End Manual Test Plan

**Generated:** 2024-02-12  
**Site:** orbital_site (Next.js + Supabase + Stripe)  
**Test Environment:** Local (localhost:3000) or Production

---

## Table of Contents
1. [Auth Flows](#1-auth-flows)
2. [Stripe Flows](#2-stripe-flows)
3. [Navigation Flows](#3-navigation-flows)
4. [Edge Cases](#4-edge-cases)

---

## 1. Auth Flows

### 1.1 Sign Up with Email/Password

| Field | Value |
|-------|-------|
| **ID** | AUTH-001 |
| **Precondition** | User not logged in, no existing account with test email |
| **Steps** | 1. Navigate to `/signup`<br>2. Enter valid email (e.g., `test+${Date.now()}@example.com`)<br>3. Enter password meeting requirements (8+ chars, 1 uppercase, 1 number)<br>4. Enter matching password in confirm field<br>5. Click "Create Account" |
| **Expected Result** | Success message appears: "Account created. Check your email to confirm your account." |
| **Console Check** | No errors. Look for `[Auth]` logs showing signup attempt |

---

### 1.2 Sign Up - Invalid Password

| Field | Value |
|-------|-------|
| **ID** | AUTH-002 |
| **Precondition** | User not logged in |
| **Steps** | 1. Navigate to `/signup`<br>2. Enter valid email<br>3. Enter weak password (e.g., "password" - no uppercase/number)<br>4. Observe password requirement indicators<br>5. Try to submit |
| **Expected Result** | Submit button disabled. Password requirements show unmet criteria in gray |
| **Console Check** | No errors - form validation is client-side |

---

### 1.3 Sign Up - Passwords Don't Match

| Field | Value |
|-------|-------|
| **ID** | AUTH-003 |
| **Precondition** | User not logged in |
| **Steps** | 1. Navigate to `/signup`<br>2. Enter valid email<br>3. Enter valid password<br>4. Enter different password in confirm field<br>5. Try to submit |
| **Expected Result** | Confirm field shows ✕ icon and red border. Submit button disabled |
| **Console Check** | No errors |

---

### 1.4 Sign Up - Existing Email

| Field | Value |
|-------|-------|
| **ID** | AUTH-004 |
| **Precondition** | Account already exists for email |
| **Steps** | 1. Navigate to `/signup`<br>2. Enter existing user's email<br>3. Enter valid password + confirm<br>4. Click "Create Account" |
| **Expected Result** | Error message from Supabase (varies: may say "User already registered" or similar) |
| **Console Check** | Check for Supabase auth error in console |

---

### 1.5 Login with Email/Password - Success

| Field | Value |
|-------|-------|
| **ID** | AUTH-005 |
| **Precondition** | User has confirmed account (clicked email verification link) |
| **Steps** | 1. Navigate to `/login`<br>2. Enter valid email<br>3. Enter correct password<br>4. Click "Sign In" |
| **Expected Result** | Redirected to `/dashboard`. User sees their minutes balance and can access features |
| **Console Check** | Look for `[Auth] Session user: <email>` and `[Auth] Profile fetched, setting loading false` |

---

### 1.6 Login with Email/Password - Wrong Password

| Field | Value |
|-------|-------|
| **ID** | AUTH-006 |
| **Precondition** | User has confirmed account |
| **Steps** | 1. Navigate to `/login`<br>2. Enter valid email<br>3. Enter wrong password<br>4. Click "Sign In" |
| **Expected Result** | Error message appears: "Invalid login credentials" (or similar Supabase message) |
| **Console Check** | No console errors (error handled gracefully) |

---

### 1.7 Login with Email/Password - Unconfirmed Email

| Field | Value |
|-------|-------|
| **ID** | AUTH-007 |
| **Precondition** | User signed up but never clicked confirmation email |
| **Steps** | 1. Navigate to `/login`<br>2. Enter unconfirmed email<br>3. Enter password<br>4. Click "Sign In" |
| **Expected Result** | Error message (Supabase typically: "Email not confirmed") |
| **Console Check** | Supabase auth error logged |

---

### 1.8 Login with Google OAuth

| Field | Value |
|-------|-------|
| **ID** | AUTH-008 |
| **Precondition** | User not logged in, has Google account |
| **Steps** | 1. Navigate to `/login`<br>2. Click "Continue with Google"<br>3. Complete Google OAuth flow (select account, authorize)<br>4. Wait for redirect |
| **Expected Result** | Redirected through `/auth/callback` → `/auth/complete` → `/dashboard`. User is logged in |
| **Console Check** | `Auth callback hit: { code: true, error: undefined }` in server logs. Client shows `[Auth] Session user:` |

---

### 1.9 Login with Google OAuth - Cancel/Deny

| Field | Value |
|-------|-------|
| **ID** | AUTH-009 |
| **Precondition** | User not logged in |
| **Steps** | 1. Navigate to `/login`<br>2. Click "Continue with Google"<br>3. Cancel or deny access at Google prompt |
| **Expected Result** | Redirected back to `/login?error=access_denied` (or similar). Error displayed |
| **Console Check** | `OAuth error: access_denied` in server logs |

---

### 1.10 Forgot Password - Request Reset

| Field | Value |
|-------|-------|
| **ID** | AUTH-010 |
| **Precondition** | User has existing account |
| **Steps** | 1. Navigate to `/login`<br>2. Click "Forgot password?"<br>3. Enter registered email<br>4. Click "Send Reset Link" |
| **Expected Result** | Success message: "Check your email for a password reset link" |
| **Console Check** | No errors |

---

### 1.11 Forgot Password - Reset Flow

| Field | Value |
|-------|-------|
| **ID** | AUTH-011 |
| **Precondition** | User requested password reset |
| **Steps** | 1. Click link in password reset email<br>2. Land on `/reset-password` with token params<br>3. Enter new password (meeting requirements)<br>4. Click "Reset Password" |
| **Expected Result** | Password updated. User can now login with new password |
| **Console Check** | No errors. Check network tab for successful Supabase call |

---

### 1.12 Sign Out from Dashboard

| Field | Value |
|-------|-------|
| **ID** | AUTH-012 |
| **Precondition** | User logged in on `/dashboard` |
| **Steps** | 1. On dashboard, open user menu (user icon)<br>2. Click "Sign Out" |
| **Expected Result** | Redirected to `/login`. Trying to access `/dashboard` redirects to login |
| **Console Check** | `[Auth] SIGNED_OUT` event logged |

---

### 1.13 Sign Out from Settings

| Field | Value |
|-------|-------|
| **ID** | AUTH-013 |
| **Precondition** | User logged in on `/settings` |
| **Steps** | 1. Navigate to `/settings`<br>2. Click "Sign Out" button (bottom of page) |
| **Expected Result** | Redirected to `/login`. Session cleared |
| **Console Check** | Verify session cookies cleared in Application tab |

---

### 1.14 Sign Out from Purchases

| Field | Value |
|-------|-------|
| **ID** | AUTH-014 |
| **Precondition** | User logged in on `/purchases` |
| **Steps** | 1. Navigate to `/purchases`<br>2. Use navigation to sign out (back to dashboard → sign out, or direct if available) |
| **Expected Result** | User logged out, redirected to `/login` |
| **Console Check** | Session cleared |

---

### 1.15 Session Persistence - Page Refresh

| Field | Value |
|-------|-------|
| **ID** | AUTH-015 |
| **Precondition** | User logged in on `/dashboard` |
| **Steps** | 1. On `/dashboard`, press F5 or Cmd+R to refresh<br>2. Wait for page to reload |
| **Expected Result** | Still logged in. Dashboard shows user data. No redirect to login |
| **Console Check** | `[Auth] Session user: <email>` appears after refresh |

---

### 1.16 Session Persistence - Tab Close/Reopen

| Field | Value |
|-------|-------|
| **ID** | AUTH-016 |
| **Precondition** | User logged in |
| **Steps** | 1. Close browser tab<br>2. Open new tab<br>3. Navigate to site `/dashboard` |
| **Expected Result** | User still logged in (cookies persist) |
| **Console Check** | `[Auth] getSession returned` with valid session |

---

### 1.17 Session Persistence - Browser Close/Reopen

| Field | Value |
|-------|-------|
| **ID** | AUTH-017 |
| **Precondition** | User logged in, browser not in incognito mode |
| **Steps** | 1. Close entire browser<br>2. Reopen browser<br>3. Navigate to `/dashboard` |
| **Expected Result** | User still logged in (depends on cookie settings) |
| **Console Check** | Verify session cookies exist in Application → Cookies |

---

## 2. Stripe Flows

### 2.1 Open Pricing Modal

| Field | Value |
|-------|-------|
| **ID** | STRIPE-001 |
| **Precondition** | User logged in on `/dashboard` |
| **Steps** | 1. On dashboard, click "Buy Minutes" button (or equivalent CTA) |
| **Expected Result** | Pricing modal opens showing 3 tiers (Starter, Standard, Pro) with One-time/Monthly toggle |
| **Console Check** | No errors |

---

### 2.2 Close Pricing Modal

| Field | Value |
|-------|-------|
| **ID** | STRIPE-002 |
| **Precondition** | Pricing modal open |
| **Steps** | 1. Click X button<br>OR<br>2. Click backdrop (outside modal) |
| **Expected Result** | Modal closes. Dashboard visible |
| **Console Check** | No errors |

---

### 2.3 Starter Tier - One-time Purchase

| Field | Value |
|-------|-------|
| **ID** | STRIPE-003 |
| **Precondition** | User logged in, pricing modal open |
| **Steps** | 1. Ensure "One-time" billing mode selected<br>2. Click "Buy Now" on Starter tier ($2) |
| **Expected Result** | Redirected to Stripe Checkout. Product shows: Starter - 10 minutes, $2.00 |
| **Console Check** | `[Checkout] Getting session...` → `[Checkout] Calling API...` → `[Checkout] Success data: { checkout_url: "..." }` |

---

### 2.4 Standard Tier - One-time Purchase

| Field | Value |
|-------|-------|
| **ID** | STRIPE-004 |
| **Precondition** | User logged in, pricing modal open |
| **Steps** | 1. Ensure "One-time" billing mode selected<br>2. Click "Buy Now" on Standard tier ($8) |
| **Expected Result** | Redirected to Stripe Checkout. Product shows: Standard - 50 minutes, $8.00. "Best Value" badge visible |
| **Console Check** | No errors. API returns checkout_url |

---

### 2.5 Pro Tier - One-time Purchase

| Field | Value |
|-------|-------|
| **ID** | STRIPE-005 |
| **Precondition** | User logged in, pricing modal open |
| **Steps** | 1. Ensure "One-time" billing mode selected<br>2. Click "Buy Now" on Pro tier ($15) |
| **Expected Result** | Redirected to Stripe Checkout. Product shows: Pro - 120 minutes, $15.00 |
| **Console Check** | Successful API response |

---

### 2.6 Starter Tier - Subscription

| Field | Value |
|-------|-------|
| **ID** | STRIPE-006 |
| **Precondition** | User logged in, pricing modal open |
| **Steps** | 1. Toggle to "Monthly" billing mode<br>2. Note pricing updates (Starter: $1.50/mo)<br>3. Click "Buy Now" on Starter |
| **Expected Result** | Redirected to Stripe Checkout in subscription mode. Shows recurring billing |
| **Console Check** | API request body contains `mode: "subscription"` |

---

### 2.7 Standard Tier - Subscription

| Field | Value |
|-------|-------|
| **ID** | STRIPE-007 |
| **Precondition** | User logged in, pricing modal open |
| **Steps** | 1. Toggle to "Monthly"<br>2. Click "Buy Now" on Standard ($6/mo) |
| **Expected Result** | Stripe Checkout shows subscription for Standard plan |
| **Console Check** | Verify subscription mode in network request |

---

### 2.8 Pro Tier - Subscription

| Field | Value |
|-------|-------|
| **ID** | STRIPE-008 |
| **Precondition** | User logged in, pricing modal open |
| **Steps** | 1. Toggle to "Monthly"<br>2. Click "Buy Now" on Pro ($12/mo) |
| **Expected Result** | Stripe Checkout shows subscription for Pro plan |
| **Console Check** | Correct price_id used for subscription |

---

### 2.9 Stripe Checkout - Success Redirect

| Field | Value |
|-------|-------|
| **ID** | STRIPE-009 |
| **Precondition** | On Stripe Checkout page |
| **Steps** | 1. Enter test card: `4242 4242 4242 4242`<br>2. Any future expiry, any CVC<br>3. Enter required billing details<br>4. Click "Pay" |
| **Expected Result** | Redirected to `/dashboard?success=true&session_id=...`. Success toast/message shown. Minutes balance updated |
| **Console Check** | No errors. Profile refresh occurs |

---

### 2.10 Stripe Checkout - Cancel Redirect

| Field | Value |
|-------|-------|
| **ID** | STRIPE-010 |
| **Precondition** | On Stripe Checkout page |
| **Steps** | 1. Click back arrow or "< Back" link at top of Stripe page |
| **Expected Result** | Redirected to `/dashboard?canceled=true`. No purchase made. Minutes unchanged |
| **Console Check** | No errors |

---

### 🔴 2.11 Stripe Checkout - Browser BACK Button (THE PROBLEM!)

| Field | Value |
|-------|-------|
| **ID** | STRIPE-011 |
| **Precondition** | User on Stripe Checkout page (after clicking Buy Now) |
| **Steps** | 1. On Stripe Checkout, press browser BACK button (not Stripe's back link)<br>2. Observe what happens on return to site |
| **Expected Result** | **CURRENT BUG:** Page may be in broken state (loading spinner stuck, session stale, bfcache issues). **EXPECTED:** Should detect bfcache restore and show refresh banner OR automatically refresh |
| **Console Check** | 🔍 Look for:<br>- `pageshow` event with `persisted: true`<br>- Stale session errors<br>- `[Checkout] Getting session...` hanging<br>- Any React hydration errors |

**Specific things to test for STRIPE-011:**

1. **Safari (most common bfcache issue)**
   - Press back button
   - Does page show "Page needs refresh" banner?
   - Does clicking a tier button trigger refresh?
   
2. **Chrome**
   - Back button behavior
   - Is session still valid?
   
3. **Firefox**
   - Back button behavior
   - Check if `pageshow` event fires

---

### 2.12 Stripe - User Not Logged In Attempt

| Field | Value |
|-------|-------|
| **ID** | STRIPE-012 |
| **Precondition** | Session expired or user somehow on dashboard without auth |
| **Steps** | 1. (Hard to reproduce) Try to trigger checkout without valid session |
| **Expected Result** | Alert: "Please log in to purchase" |
| **Console Check** | `[Checkout] Session result: { hasSession: false }` |

---

### 2.13 Stripe - API Error Handling

| Field | Value |
|-------|-------|
| **ID** | STRIPE-013 |
| **Precondition** | User logged in |
| **Steps** | 1. (Simulate by breaking API - e.g., wrong price ID in env)<br>2. Click Buy Now |
| **Expected Result** | Error message shown to user. Loading spinner stops |
| **Console Check** | Error logged. Alert displayed with error details |

---

## 3. Navigation Flows

### 3.1 Direct URL Access - Logged Out - Protected Routes

| Field | Value |
|-------|-------|
| **ID** | NAV-001 |
| **Precondition** | User NOT logged in |
| **Steps** | Test each protected route by entering URL directly:<br>1. `/dashboard`<br>2. `/settings`<br>3. `/purchases`<br>4. `/videos` |
| **Expected Result** | Redirected to `/login?redirect=<original_path>`. Cannot access protected content |
| **Console Check** | Middleware redirect logged (server-side) |

---

### 3.2 Direct URL Access - Logged Out - Public Routes

| Field | Value |
|-------|-------|
| **ID** | NAV-002 |
| **Precondition** | User NOT logged in |
| **Steps** | Test each public route:<br>1. `/` (home)<br>2. `/login`<br>3. `/signup`<br>4. `/forgot-password`<br>5. `/privacy`<br>6. `/terms` |
| **Expected Result** | All pages accessible without redirect |
| **Console Check** | No auth errors |

---

### 3.3 Direct URL Access - Logged In - Protected Routes

| Field | Value |
|-------|-------|
| **ID** | NAV-003 |
| **Precondition** | User logged in |
| **Steps** | Enter each URL directly:<br>1. `/dashboard`<br>2. `/settings`<br>3. `/purchases`<br>4. `/videos` |
| **Expected Result** | All pages load correctly with user data |
| **Console Check** | `[Auth] Session user:` shows for each page |

---

### 3.4 Direct URL Access - Logged In - Auth Routes

| Field | Value |
|-------|-------|
| **ID** | NAV-004 |
| **Precondition** | User logged in |
| **Steps** | Try to access auth routes:<br>1. `/login`<br>2. `/signup` |
| **Expected Result** | Redirected to `/dashboard` (middleware prevents logged-in users from seeing login/signup) |
| **Console Check** | Middleware handles redirect |

---

### 3.5 Navigation - Dashboard → Settings

| Field | Value |
|-------|-------|
| **ID** | NAV-005 |
| **Precondition** | User logged in on `/dashboard` |
| **Steps** | 1. Click user icon / settings link<br>2. Navigate to settings |
| **Expected Result** | `/settings` loads with user preferences |
| **Console Check** | No errors |

---

### 3.6 Navigation - Settings → Dashboard

| Field | Value |
|-------|-------|
| **ID** | NAV-006 |
| **Precondition** | User on `/settings` |
| **Steps** | 1. Click back arrow or "Dashboard" link |
| **Expected Result** | Returns to `/dashboard` |
| **Console Check** | No errors |

---

### 3.7 Navigation - Dashboard → Purchases

| Field | Value |
|-------|-------|
| **ID** | NAV-007 |
| **Precondition** | User on `/dashboard` |
| **Steps** | 1. Navigate to purchases (via settings or direct link) |
| **Expected Result** | `/purchases` shows purchase history |
| **Console Check** | Purchase fetch query logged |

---

### 3.8 Navigation - Dashboard → Videos

| Field | Value |
|-------|-------|
| **ID** | NAV-008 |
| **Precondition** | User on `/dashboard` |
| **Steps** | 1. Click "Videos" or navigate via menu |
| **Expected Result** | `/videos` page loads |
| **Console Check** | No errors |

---

### 3.9 Navigation - Deep Link with Redirect

| Field | Value |
|-------|-------|
| **ID** | NAV-009 |
| **Precondition** | User NOT logged in |
| **Steps** | 1. Navigate to `/dashboard` (gets redirected to `/login?redirect=/dashboard`)<br>2. Log in successfully |
| **Expected Result** | After login, redirected to `/dashboard` (original intended destination) |
| **Console Check** | Check URL params preserved through login |

---

### 3.10 Navigation - Query Params Preservation

| Field | Value |
|-------|-------|
| **ID** | NAV-010 |
| **Precondition** | User logged in |
| **Steps** | 1. Navigate to `/dashboard?success=true`<br>2. Check if success message appears |
| **Expected Result** | Success query param detected and success UI shown |
| **Console Check** | No errors |

---

## 4. Edge Cases

### 4.1 Multiple Tabs - Same Session

| Field | Value |
|-------|-------|
| **ID** | EDGE-001 |
| **Precondition** | User logged in |
| **Steps** | 1. Open `/dashboard` in Tab 1<br>2. Open `/dashboard` in Tab 2<br>3. Verify both tabs work |
| **Expected Result** | Both tabs function correctly. Same session shared |
| **Console Check** | Both tabs show same user session |

---

### 4.2 Multiple Tabs - Sign Out in One Tab

| Field | Value |
|-------|-------|
| **ID** | EDGE-002 |
| **Precondition** | User logged in, 2 tabs open on `/dashboard` |
| **Steps** | 1. Sign out in Tab 1<br>2. Check Tab 2 (may need to interact/refresh) |
| **Expected Result** | Tab 2 should detect logout on next interaction. Auth state listener fires `SIGNED_OUT` |
| **Console Check** | `onAuthStateChange: SIGNED_OUT` in Tab 2 console |

---

### 4.3 Multiple Tabs - Sign In in Another Tab

| Field | Value |
|-------|-------|
| **ID** | EDGE-003 |
| **Precondition** | User NOT logged in, 2 tabs open |
| **Steps** | 1. Tab 1 on `/login`<br>2. Tab 2 on `/login`<br>3. Complete login in Tab 1<br>4. Check Tab 2 |
| **Expected Result** | Tab 2 may auto-detect login (auth state change listener) or will show logged-in state on refresh |
| **Console Check** | `onAuthStateChange: SIGNED_IN` event |

---

### 4.4 Incognito Mode - Fresh Session

| Field | Value |
|-------|-------|
| **ID** | EDGE-004 |
| **Precondition** | None |
| **Steps** | 1. Open incognito/private window<br>2. Navigate to site<br>3. Attempt to access `/dashboard` |
| **Expected Result** | Not logged in. Redirected to login. No previous session exists |
| **Console Check** | `[Auth] No session found` |

---

### 4.5 Incognito Mode - Complete Flow

| Field | Value |
|-------|-------|
| **ID** | EDGE-005 |
| **Precondition** | In incognito window |
| **Steps** | 1. Sign up with new email<br>2. (Skip email confirmation if testing locally)<br>3. Log in<br>4. Navigate around<br>5. Close incognito window<br>6. Open new incognito window<br>7. Navigate to site |
| **Expected Result** | Session does NOT persist after closing incognito window |
| **Console Check** | New window shows no session |

---

### 4.6 Incognito Mode - Stripe Checkout

| Field | Value |
|-------|-------|
| **ID** | EDGE-006 |
| **Precondition** | Logged in, in incognito mode |
| **Steps** | 1. Open pricing modal<br>2. Click "Buy Now"<br>3. Complete Stripe checkout<br>4. Observe redirect |
| **Expected Result** | Should work identically to normal mode. Minutes credited |
| **Console Check** | No cookie-related errors |

---

### 4.7 Refresh on Protected Page - Valid Session

| Field | Value |
|-------|-------|
| **ID** | EDGE-007 |
| **Precondition** | User logged in on `/dashboard` |
| **Steps** | 1. Press F5 / Cmd+R to hard refresh<br>2. Wait for page load |
| **Expected Result** | Page reloads, user still authenticated, all data loads correctly |
| **Console Check** | `[Auth] initAuth starting...` → Session found → Profile fetched |

---

### 4.8 Refresh on Protected Page - Expired Session

| Field | Value |
|-------|-------|
| **ID** | EDGE-008 |
| **Precondition** | User was logged in, session has expired (or manually clear cookies) |
| **Steps** | 1. Clear auth cookies via DevTools<br>2. Press F5 on `/dashboard` |
| **Expected Result** | Middleware detects no session, redirects to `/login` |
| **Console Check** | `[Auth] No session found` |

---

### 4.9 Token Refresh

| Field | Value |
|-------|-------|
| **ID** | EDGE-009 |
| **Precondition** | User logged in, session near expiry (hard to test manually) |
| **Steps** | 1. Keep page open for extended period<br>2. Interact with page after token should refresh |
| **Expected Result** | Supabase auto-refreshes token. User stays logged in |
| **Console Check** | `onAuthStateChange: TOKEN_REFRESHED` event |

---

### 4.10 Network Offline During Auth

| Field | Value |
|-------|-------|
| **ID** | EDGE-010 |
| **Precondition** | User on login page |
| **Steps** | 1. Open DevTools → Network tab → Offline mode<br>2. Try to login |
| **Expected Result** | Error message shown (network error). Form doesn't hang indefinitely |
| **Console Check** | Network error caught and handled |

---

### 4.11 Network Offline During Checkout

| Field | Value |
|-------|-------|
| **ID** | EDGE-011 |
| **Precondition** | User logged in, pricing modal open |
| **Steps** | 1. Enable offline mode<br>2. Click "Buy Now" |
| **Expected Result** | Error alert shown. Loading spinner clears |
| **Console Check** | Fetch error logged |

---

### 4.12 Rapid Navigation (Race Conditions)

| Field | Value |
|-------|-------|
| **ID** | EDGE-012 |
| **Precondition** | User logged in |
| **Steps** | 1. Navigate rapidly between pages<br>2. Click multiple links in quick succession |
| **Expected Result** | No race conditions. Last navigation wins. No duplicate renders |
| **Console Check** | No "Can't perform state update on unmounted component" warnings |

---

### 4.13 Back/Forward Browser History

| Field | Value |
|-------|-------|
| **ID** | EDGE-013 |
| **Precondition** | User logged in, has navigated through several pages |
| **Steps** | 1. Visit: `/dashboard` → `/settings` → `/purchases`<br>2. Press Back button twice<br>3. Press Forward button once |
| **Expected Result** | History navigation works. Pages load correctly. Auth state maintained |
| **Console Check** | No errors on navigation |

---

### 4.14 Theme Persistence

| Field | Value |
|-------|-------|
| **ID** | EDGE-014 |
| **Precondition** | User on any page |
| **Steps** | 1. Toggle theme to light mode<br>2. Navigate to different page<br>3. Refresh page<br>4. Close and reopen browser |
| **Expected Result** | Theme preference persists (stored in localStorage) |
| **Console Check** | `localStorage.getItem("orbital-theme")` returns saved value |

---

## Appendix: Console Debug Commands

Use these in DevTools console for debugging:

```javascript
// Check current auth state
const { data: { session } } = await supabase.auth.getSession()
console.log('Session:', session)

// Check profile
const { data: profile } = await supabase.from('profiles').select('*').single()
console.log('Profile:', profile)

// Force sign out
await supabase.auth.signOut()

// Check localStorage
console.log('Theme:', localStorage.getItem('orbital-theme'))
console.log('All localStorage:', {...localStorage})

// Check cookies (run in Application tab)
document.cookie
```

---

## Priority Test Matrix

| Priority | Tests | Focus |
|----------|-------|-------|
| 🔴 **P0 - Critical** | STRIPE-011, AUTH-005, AUTH-008, NAV-001 | Browser back from Stripe, core login flows |
| 🟠 **P1 - High** | STRIPE-009, STRIPE-010, AUTH-012, EDGE-001 | Payment flows, sign out, multi-tab |
| 🟡 **P2 - Medium** | All other auth tests, navigation tests | Full coverage |
| 🟢 **P3 - Low** | EDGE-009 through EDGE-014 | Edge cases, nice-to-have |

---

## Known Issues to Watch

1. **🔴 STRIPE-011**: Browser BACK from Stripe causes bfcache issues
   - Implemented `pageshow` handler with `persisted` check
   - Shows refresh banner when bfcache restore detected
   - Clicking tier button triggers reload
   
2. **Session loading**: Initial `[Auth] initAuth` can be slow
   - Optimized to use session.user instead of separate getUser() call
   
3. **Safari**: More aggressive bfcache behavior than Chrome
