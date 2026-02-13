# Routing & Middleware Audit

**Project:** Orbital Site  
**Date:** 2025-06-28  
**Auditor:** QA Subagent

---

## Executive Summary

The middleware and routing implementation is **solid overall**, with proper server-side auth validation. However, there are **redundant client-side auth checks** on some protected pages that create minor conflicts and could cause race conditions during sign-out flows.

| Area | Status | Notes |
|------|--------|-------|
| Middleware Auth | ✅ Good | Uses `getUser()` for server validation |
| Protected Routes | ✅ Good | Correctly defined |
| Auth Route Handling | ✅ Good | Redirects logged-in users away |
| Matcher Config | ✅ Good | Properly excludes static assets |
| Client-Side Checks | ⚠️ Concern | Redundant checks create conflicts |
| OAuth Flow | ✅ Good | PKCE implemented correctly |

---

## 1. Middleware Analysis (`src/middleware.ts`)

### Protected Routes
```typescript
const protectedPaths = ['/dashboard', '/settings', '/purchases', '/videos']
```

### Auth Routes (redirect if logged in)
```typescript
const authPaths = ['/login', '/signup']
```

### Auth Check Method
✅ **Uses `getUser()` for server-side validation** — This is the correct approach per Supabase best practices. The middleware properly validates sessions with the auth server rather than just trusting cookies.

### Redirect Logic
✅ **Properly preserves intended destination:**
```typescript
redirectUrl.searchParams.set('redirect', request.nextUrl.pathname)
```

### Error Handling
✅ **Graceful degradation** — If middleware errors (corrupted cookies, network issues), requests pass through and pages handle auth state. This prevents blocking users entirely.

### Matcher Config
```typescript
'/((?!_next/static|_next/image|favicon.ico|.*\\.(?:svg|png|jpg|jpeg|gif|webp)$).*)'
```
✅ **Correctly excludes:**
- `_next/static` — Static files
- `_next/image` — Image optimization
- `favicon.ico`
- Image file extensions (svg, png, jpg, jpeg, gif, webp)

---

## 2. Supabase Middleware Helper (`src/lib/supabase/middleware.ts`)

✅ **Excellent implementation:**
- Uses `createServerClient` from `@supabase/ssr`
- Properly handles cookie get/set operations
- **Uses `getUser()` not `getSession()`** — Critical for security
- Returns response with refreshed cookies

---

## 3. Client-Side Auth Conflicts ⚠️

### Problem: Redundant Auth Checks

Several protected pages implement **their own client-side redirect logic** despite middleware already handling this:

#### `/videos/page.tsx` — ❌ Conflicting
```typescript
useEffect(() => {
  if (!authLoading && !user) {
    router.push("/login");
  }
}, [user, authLoading, router]);
```

#### `/settings/page.tsx` — ❌ Conflicting  
```typescript
useEffect(() => {
  if (!authLoading && !user) {
    router.push("/login");
  }
}, [user, authLoading, router]);
```

#### `/dashboard/page.tsx` — ⚠️ Partially Conflicting
Has removed the redirect but still shows a spinner when `!user`:
```typescript
if (!user) {
  return (
    <div className="min-h-screen w-full flex items-center justify-center bg-black">
      <div className="w-8 h-8 border-2 border-violet-500 border-t-transparent rounded-full animate-spin" />
    </div>
  );
}
```
Comment says: *"Navigation is handled by: middleware (server-side) or signOut handler (client-side)"*

#### `/login/page.tsx` — ❌ Conflicting
```typescript
useEffect(() => {
  if (!authLoading && user) {
    router.push("/dashboard");
  }
}, [user, authLoading, router]);
```

### Why This Is Problematic

1. **Race conditions** — Client-side check fires while middleware has already handled redirect
2. **Double redirects** — User may see brief flash or multiple navigations
3. **Sign-out edge cases** — When signing out, client state clears before navigation, causing the redirect useEffect to fire
4. **Inconsistent behavior** — Dashboard has special handling while other pages don't

### Recommendation

**Remove redundant client-side redirects** from protected pages. The middleware handles this server-side before the page even loads. Pages should:
1. Show loading spinner while `authLoading` is true
2. Trust that if they rendered, the user is authenticated (middleware guarantees this)
3. Handle only the loading state, not redirect logic

---

## 4. OAuth/Auth Callback Flow

### `/auth/callback/route.ts`
✅ **Well implemented:**
- Properly exchanges code for session using PKCE
- Sets cookies on both cookie store and response
- Validates user with `getUser()` after exchange
- Redirects to `/auth/complete` for client-side session finalization
- Includes cache-busting headers

### `/auth/complete/page.tsx`
✅ **Proper fallback handler:**
- Handles hash fragment tokens (implicit flow fallback)
- Verifies session exists
- Redirects to dashboard on success

---

## 5. Routes Not Protected (by design)

| Route | Purpose | Status |
|-------|---------|--------|
| `/` | Landing page | ✅ Public |
| `/login` | Auth | ✅ Redirects if logged in |
| `/signup` | Auth | ✅ Redirects if logged in |
| `/forgot-password` | Password reset | ✅ Public |
| `/reset-password` | Password reset | ✅ Public |
| `/privacy` | Legal | ✅ Public |
| `/terms` | Legal | ✅ Public |
| `/auth/callback` | OAuth callback | ✅ Public (server-side only) |
| `/auth/complete` | OAuth completion | ✅ Public (client-side finalization) |
| `/debug` | Debug page | ⚠️ Should this be protected? |

---

## 6. Next.js Config (`next.config.ts`)

```typescript
const nextConfig: NextConfig = {
  /* config options here */
};
```

✅ **No routing conflicts** — Config is minimal with no rewrites or redirects that would conflict with middleware.

---

## 7. Action Items

### High Priority
1. **Remove redundant client-side auth redirects** from `/videos`, `/settings`, and `/login` pages
2. **Standardize protected page pattern** — Follow the dashboard's approach (spinner only, no redirect logic)

### Medium Priority
3. **Consider protecting `/debug` route** — Currently accessible without auth
4. **Add `redirect` param handling** to login success flow — The middleware sets it, but login page doesn't use it

### Low Priority
5. **Add rate limiting to auth callback** — Prevent abuse
6. **Consider adding CSP headers** in middleware for auth routes

---

## 8. Recommended Protected Page Pattern

```typescript
export default function ProtectedPage() {
  const { user, profile, loading } = useAuth();
  
  // Show loading while auth initializes
  if (loading) {
    return <LoadingSpinner />;
  }
  
  // If we got here without a user, middleware failed — show spinner
  // (Middleware should have redirected; this is just a safety fallback)
  if (!user) {
    return <LoadingSpinner />;
  }
  
  // Render page normally — user is guaranteed authenticated
  return <PageContent user={user} profile={profile} />;
}
```

**Key principle:** Trust the middleware. If the page renders, the user is authenticated.

---

## Summary

The middleware implementation is **well-designed and secure**. The main issue is **redundant client-side auth checks** that create unnecessary complexity and potential race conditions. Removing these checks will simplify the codebase and make auth behavior more predictable.
