# Auth Flow Audit - Orbital Site

**Audit Date:** 2025-01-21  
**Auditor:** QA Subagent  
**Scope:** All authentication-related code paths

---

## Executive Summary

The auth system uses a **dual-client architecture** with separate browser (localStorage) and server (cookie) Supabase clients. This was intentionally done to work around SSR issues with external redirects (Stripe), but creates complexity and potential sync issues.

**Critical Issues Found:** 2  
**Moderate Issues Found:** 4  
**Minor Issues/Improvements:** 5

---

## File-by-File Analysis

### 1. `src/lib/supabase.ts` - Browser Client

**Purpose:** Creates a singleton Supabase client for browser-side usage using localStorage for session storage.

```typescript
// Uses standard client (NOT SSR client)
import { createClient as createSupabaseClient } from '@supabase/supabase-js'
```

**What it does:**
- Creates a bare Supabase client using the standard JS library
- Uses singleton pattern for client-side (prevents multiple instances)
- Creates fresh client on server-side (SSR safety)
- Stores sessions in **localStorage** (default behavior)

**Key Comment (explains architecture decision):**
> SSR client's getSession() hangs after external navigation (Stripe)

**Issues:**
- ⚠️ **MODERATE: No custom auth configuration** - Client uses defaults, no session persistence options configured
- 📝 **NOTE:** The `!` non-null assertions on env vars will throw at runtime if not set (acceptable for env vars)

---

### 2. `src/lib/supabase/server.ts` - Server Client

**Purpose:** Creates cookie-based Supabase client for Server Components and Server Actions.

**What it does:**
- Uses `@supabase/ssr` for cookie-based auth
- Reads/writes auth tokens via `cookies()` from `next/headers`
- Silently ignores `setAll` errors in Server Components (expected behavior)

**Issues:**
- ✅ Correctly implemented per Supabase SSR docs
- 📝 **NOTE:** Silent catch in `setAll` is intentional - middleware handles session refresh

---

### 3. `src/lib/supabase/middleware.ts` - Session Handler

**Purpose:** Middleware helper that refreshes sessions and validates users.

**What it does:**
- Creates SSR client with cookie access
- Calls `getUser()` (NOT `getSession()`) - validates with auth server
- Returns updated response with refreshed cookies

**Excellent Comment:**
```typescript
// IMPORTANT: Do NOT use getSession() here.
// getSession() reads from cookies but doesn't validate with the server.
// Use getUser() which validates the session with the Supabase Auth server.
```

**Issues:**
- ✅ **CORRECT:** Uses `getUser()` for security (validates tokens server-side)
- ✅ Properly propagates cookies to response

---

### 4. `src/middleware.ts` - Route Protection

**Purpose:** Next.js middleware that protects routes and handles auth redirects.

**What it does:**
- Calls `updateSession()` to refresh/validate session
- Protects: `/dashboard`, `/settings`, `/purchases`, `/videos`
- Redirects unauthenticated users to `/login?redirect=<path>`
- Redirects authenticated users away from `/login`, `/signup`
- Returns supabaseResponse to persist cookies

**Issues:**
- ⚠️ **MODERATE: Catch-all error handling too permissive**
  ```typescript
  catch (e) {
    // If there's an error (corrupted cookies, network issues, etc.),
    // let the request through - the page can handle auth state
    console.error('Middleware error:', e)
    return NextResponse.next({ request })
  }
  ```
  This allows protected routes to be accessed if middleware fails. Consider redirecting to login instead.

- 📝 **NOTE:** The `redirect` param is correctly set for post-login return

---

### 5. `src/lib/auth.ts` - useAuth Hook

**Purpose:** React hook providing auth state and methods for client components.

**What it does:**
- Manages `user`, `profile`, and `loading` state
- Fetches profile from `profiles` table
- Listens for auth state changes (`onAuthStateChange`)
- Provides `signUp`, `signIn`, `signOut`, `refreshProfile` methods

**Issues:**

- 🔴 **CRITICAL: Inconsistent session validation**
  ```typescript
  const { data: { session }, error: sessionError } = await supabase.auth.getSession()
  // ... then uses session.user
  ```
  Uses `getSession()` which reads from storage without validating. The middleware uses `getUser()`. This inconsistency means:
  - Middleware validates tokens server-side ✅
  - Client hook trusts localStorage blindly ⚠️
  
  **Risk:** Expired/revoked tokens could appear valid client-side.

- 🔴 **CRITICAL: Race condition in signOut**
  ```typescript
  const signOut = async () => {
    setUser(null)        // State cleared BEFORE signOut
    setProfile(null)
    const { error } = await supabase.auth.signOut()  // What if this fails?
    if (error) console.error('SignOut error:', error.message)
    return { error }
  }
  ```
  If `signOut()` fails (network error), UI shows logged out but session persists. User might think they're logged out when they're not.
  
  **Fix:** Only clear state after successful signOut, or clear regardless but retry on error.

- ⚠️ **MODERATE: No error state exposed**
  - Errors are logged but not exposed to consumers
  - Components can't show "session expired" messages

- 📝 **Minor: `initializedRef` is good** - Prevents double-init in React Strict Mode

---

### 6. `src/app/login/page.tsx` - Login Page

**Purpose:** Email/password and Google OAuth login.

**What it does:**
- Form-based email/password login via `signIn()` from useAuth
- Google OAuth via server action `signInWithGoogle()`
- Redirects to dashboard if already authenticated
- Preserves theme in localStorage

**Issues:**

- ⚠️ **MODERATE: Duplicate redirect logic**
  ```typescript
  // In useEffect:
  if (!authLoading && user) {
    router.push("/dashboard");
  }
  
  // In handleSubmit:
  router.push("/dashboard");
  ```
  The useEffect redirect races with handleSubmit redirect. Both might fire.

- 📝 **Minor: Unused import**
  ```typescript
  const supabase = getSupabase();  // Never used in component
  ```
  
- 📝 **Minor: No redirect param handling**
  - Middleware sets `?redirect=/original-path`
  - Login page ignores this and always redirects to `/dashboard`
  - User loses their intended destination

- 📝 **Minor: Loading state not reset on success**
  ```typescript
  // setIsLoading(false) not called before redirect
  // Minor since page navigates away anyway
  ```

---

### 7. `src/app/signup/page.tsx` - Signup Page

**Purpose:** User registration with email/password or Google OAuth.

**What it does:**
- Email/password signup with validation
- Password requirements (8+ chars, uppercase, number)
- Shows success message prompting email confirmation
- Google OAuth via same server action

**Issues:**

- 📝 **Minor: Same unused import**
  ```typescript
  const supabase = getSupabase();  // Never used
  ```

- 📝 **Minor: Same redirect param issue**
  - Doesn't read `?redirect=` from URL

- ✅ **GOOD: Password validation is client-side AND displays requirements**

- ✅ **GOOD: Shows confirmation message** - Doesn't auto-login (requires email confirmation)

---

### 8. `src/app/auth/callback/route.ts` - OAuth Callback

**Purpose:** Handles OAuth redirect from Google, exchanges code for session.

**What it does:**
1. Receives authorization code from OAuth provider
2. Creates SSR client with cookie access
3. Exchanges code for session (`exchangeCodeForSession`)
4. Validates user with `getUser()`
5. Sets auth cookies on response
6. Redirects to `/auth/complete`

**Issues:**

- 🔴 **CRITICAL: Cookie/localStorage mismatch**
  ```typescript
  // Callback sets COOKIES via SSR client
  response.cookies.set(name, value, options)
  
  // But client-side uses LOCALSTORAGE client
  // See /auth/complete and useAuth hook
  ```
  The session is stored in cookies, but the browser client reads from localStorage. This might work because:
  - The `/auth/complete` page checks for hash fragments
  - The standard Supabase client might detect cookies on `getUser()` call
  
  **Risk:** If the localStorage client doesn't sync from cookies, OAuth users won't be authenticated client-side.

- 📝 **NOTE: `next` param ignored**
  ```typescript
  const next = searchParams.get('next') ?? '/dashboard'  // Captured but not used
  // Always redirects to /auth/complete
  ```

- ✅ **GOOD: Validates user after code exchange** - Security best practice
- ✅ **GOOD: No-cache headers** - Prevents caching issues
- ✅ **GOOD: Error handling with user-friendly redirects**

---

### 9. `src/app/auth/actions.ts` - Server Actions

**Purpose:** Server-side auth actions for OAuth initiation and signout.

**What it does:**
- `signInWithGoogle()`: Initiates OAuth flow with PKCE
- `signOut()`: Server-side logout with redirect

**Issues:**

- ✅ **GOOD: Uses server client** - PKCE verifier stored in cookies
- ✅ **GOOD: Dynamic origin detection** - Works in dev and production
- 📝 **NOTE:** `prompt: 'consent'` forces consent screen every time (intentional for refresh tokens)

---

### 10. `src/app/auth/complete/page.tsx` - OAuth Completion

**Purpose:** Client-side page that finalizes OAuth session.

**What it does:**
1. Checks for error in query params
2. Checks for hash fragment tokens (implicit flow fallback)
3. Calls `getUser()` to verify session
4. Redirects to dashboard or login

**Issues:**

- ⚠️ **MODERATE: Relies on hash fragment detection**
  ```typescript
  if (window.location.hash.includes('access_token')) {
    // The Supabase client auto-detects hash fragments on init
    await new Promise(r => setTimeout(r, 300))
  }
  ```
  The OAuth flow uses PKCE (code exchange), not implicit flow (hash fragments). This code path may never execute.

- 📝 **Minor: Magic delay**
  ```typescript
  await new Promise(r => setTimeout(r, 300))  // Why 300ms?
  ```
  Arbitrary delay; could be removed or explained.

- ✅ **GOOD: Cleans up hash fragments** - Security best practice
- ✅ **GOOD: Suspense boundary** - Proper Next.js 14 pattern

---

## Architecture Analysis

### Client Strategy Mismatch

```
┌─────────────────────────────────────────────────────────────────┐
│                        AUTH ARCHITECTURE                         │
├─────────────────────────────────────────────────────────────────┤
│                                                                  │
│  SERVER SIDE (SSR/Middleware/Actions)                           │
│  ┌──────────────────────────────────────────────────────────┐   │
│  │  @supabase/ssr (Cookie-based)                            │   │
│  │  - middleware.ts uses cookies                            │   │
│  │  - server.ts uses cookies                                │   │
│  │  - callback/route.ts sets cookies                        │   │
│  └──────────────────────────────────────────────────────────┘   │
│                            ↕ MISMATCH                            │
│  CLIENT SIDE (Browser)                                          │
│  ┌──────────────────────────────────────────────────────────┐   │
│  │  @supabase/supabase-js (localStorage-based)              │   │
│  │  - useAuth hook reads localStorage                       │   │
│  │  - login/signup pages use localStorage client            │   │
│  │  - /auth/complete uses localStorage client               │   │
│  └──────────────────────────────────────────────────────────┘   │
│                                                                  │
└─────────────────────────────────────────────────────────────────┘
```

**The Problem:**
- Email/password login: Works fine (client calls API, tokens stored in localStorage)
- OAuth login: Callback sets cookies, but client reads localStorage
- The `/auth/complete` page attempts to bridge this, but may not work reliably

**Why it might still work:**
1. Supabase's standard client might auto-detect auth cookies and sync to localStorage
2. The hash fragment fallback (though PKCE shouldn't use it)
3. The `getUser()` call might trigger session sync

**Recommendation:** Test OAuth flow end-to-end and verify session appears in both cookies AND localStorage after completion.

---

## Summary of Issues

### 🔴 Critical (Must Fix)

1. **Cookie/localStorage session mismatch** - OAuth sets cookies but client reads localStorage. Test thoroughly.

2. **signOut race condition** - State cleared before signOut completes. If signOut fails, UI shows logged out but session persists.

3. **getSession vs getUser inconsistency** - Middleware validates tokens server-side, but useAuth trusts localStorage blindly.

### ⚠️ Moderate (Should Fix)

1. **Middleware error handler too permissive** - Lets requests through on error; should redirect to login.

2. **Redirect param ignored** - Login/signup don't read `?redirect=` param from middleware.

3. **Duplicate redirect logic** - Login page has useEffect redirect AND handleSubmit redirect.

4. **Hash fragment reliance** - `/auth/complete` checks for hash fragments but PKCE flow doesn't use them.

### 📝 Minor (Nice to Fix)

1. **Unused `supabase` variable** in login/signup pages
2. **No error state** exposed from useAuth hook
3. **`next` param captured but unused** in callback
4. **Magic 300ms delay** in /auth/complete
5. **Loading state not reset** before redirect in login

---

## TODO/FIXME Comments Found

**None found** - The codebase is clean of TODO markers.

---

## Recommendations

### Immediate Actions

1. **Test OAuth flow end-to-end** - Verify user appears authenticated after Google login
2. **Fix signOut race condition** - Only clear state after successful signOut
3. **Add redirect param handling** - Read `?redirect=` and use it post-login

### Short-term Improvements

1. **Unify client strategy** - Either:
   - Use SSR client everywhere (might hit the Stripe navigation bug)
   - Configure browser client to use cookies
   - Add explicit cookie → localStorage sync after OAuth

2. **Consider using `getUser()` in useAuth** - For consistent validation (adds network call)

3. **Improve error handling** - Expose auth errors to components

### Long-term Considerations

1. **Add auth state machine** - Current flow has implicit states; a state machine (xstate) would make transitions explicit

2. **Add refresh token rotation** - Currently relies on Supabase defaults

3. **Add session activity tracking** - Detect idle sessions

---

## Test Cases to Verify

- [ ] Email/password signup → email confirmation → login
- [ ] Email/password login → dashboard access
- [ ] Google OAuth → callback → complete → dashboard
- [ ] Protected route access when logged out → redirect to login → login → return to original route
- [ ] Sign out → protected route access → redirect to login
- [ ] Sign out with network failure → verify session state
- [ ] Expired session → behavior on protected route
- [ ] Multiple tabs → sign out in one → state in others

---

*End of Audit*
