# React State Flow Investigation

**Date:** 2025-01-21  
**Bug:** User sees infinite spinner after `setUser(user)` is called, even though `setLoading(false)` should follow

---

## Executive Summary

**🔴 CRITICAL ISSUE FOUND:** `useAuth()` is a stateful hook, NOT a React Context. Each component using it creates isolated state. This causes loading state to reset on navigation.

**🟡 SECONDARY ISSUE:** Dashboard has double-spinner logic that shows spinner when `!user` even after `authLoading` is false.

---

## Issue 1: useAuth is NOT a Context (CRITICAL)

### Location: `src/lib/auth.ts`

```typescript
export function useAuth() {
  const [user, setUser] = useState<User | null>(null)
  const [loading, setLoading] = useState(true)  // ← NEW state each call!
  // ...
}
```

### Problem
Every component that calls `useAuth()` gets its **own separate state instance**:
- Dashboard's `loading` ≠ Login's `loading`
- When navigating login → dashboard, dashboard starts with `loading: true`
- Dashboard must wait for its own `onAuthStateChange` event

### What Happens
1. User logs in on `/login`
2. Login's `useAuth()` instance receives `SIGNED_IN` event
3. Login's instance sets `user` and `loading: false`
4. Navigation to `/dashboard` occurs
5. **Dashboard mounts with NEW `useAuth()` instance**
6. New instance starts with `loading: true`, `user: null`
7. New instance sets up fresh `onAuthStateChange` listener
8. Must wait for `INITIAL_SESSION` event (may or may not fire quickly)

### Fix Required
Convert `useAuth()` to a proper React Context:

```typescript
// auth-context.tsx
const AuthContext = createContext<AuthState | null>(null);

export function AuthProvider({ children }) {
  const [user, setUser] = useState<User | null>(null);
  const [loading, setLoading] = useState(true);
  // ... auth logic
  return (
    <AuthContext.Provider value={{ user, loading, ... }}>
      {children}
    </AuthContext.Provider>
  );
}

export function useAuth() {
  const ctx = useContext(AuthContext);
  if (!ctx) throw new Error('useAuth must be used within AuthProvider');
  return ctx;
}
```

Then wrap app in `layout.tsx`:
```tsx
<AuthProvider>
  {children}
</AuthProvider>
```

---

## Issue 2: setLoading(false) After await fetchProfile

### Location: `src/lib/auth.ts` lines 64-79

```typescript
if (event === 'INITIAL_SESSION' || event === 'SIGNED_IN') {
  if (session?.user) {
    setUser(session.user)
    await fetchProfile(session.user.id, supabase)  // ← BLOCKS HERE
  } else {
    setUser(null)
    setProfile(null)
  }
  setLoading(false)  // ← Only runs AFTER fetchProfile completes!
}
```

### Problem
- `setLoading(false)` is **after** `await fetchProfile()`
- If profile fetch is slow or hangs, loading stays true
- `fetchProfile` has try/catch so won't throw, but network issues could cause delays

### Fix Required
Set loading false immediately, fetch profile in background:

```typescript
if (event === 'INITIAL_SESSION' || event === 'SIGNED_IN') {
  if (session?.user) {
    setUser(session.user)
    setLoading(false)  // ← Set BEFORE async work
    fetchProfile(session.user.id, supabase)  // ← No await, runs in background
  } else {
    setUser(null)
    setProfile(null)
    setLoading(false)
  }
}
```

---

## Issue 3: Double Spinner in Dashboard

### Location: `src/app/dashboard/page.tsx` lines 268-285

```typescript
// Show loading while checking auth
if (authLoading) {
  return (<spinner />);
}

// If not logged in, show loading spinner
if (!user) {
  return (<spinner />);  // ← SAME SPINNER!
}
```

### Problem
If `setLoading(false)` executes but `user` is still null for any reason:
- User passes the first check (`authLoading` is false)
- User hits the second check (`!user` is true)
- **Shows spinner forever** - looks identical to loading state!

The comment says "Navigation is handled by middleware" but:
1. Middleware only works on server-side/hard navigation
2. Client-side navigation (React Router) doesn't trigger middleware
3. After `signOut()`, this becomes an infinite spinner

### Fix Required
Show different UI for "not authenticated" vs "loading":

```typescript
if (authLoading) {
  return <LoadingSpinner />;
}

if (!user) {
  // Redirect or show login prompt - NOT a spinner!
  router.push('/login');
  return null;  // Or show "Redirecting..." message
}
```

---

## Issue 4: Limited Event Coverage for setLoading(false)

### Location: `src/lib/auth.ts`

`setLoading(false)` is ONLY called for:
- `INITIAL_SESSION` (line 79)
- `SIGNED_IN` (line 79, same block)
- `SIGNED_OUT` (line 86)
- Safety timeout (line 101) - but only if **NO** event received

### Problem
If `TOKEN_REFRESHED` fires first (or any other event), `authEventReceived` becomes true, disabling the safety timeout, but `setLoading(false)` isn't called.

### Events Not Handled
- `TOKEN_REFRESHED` - sets user but not loading
- `PASSWORD_RECOVERY`
- `MFA_CHALLENGE_VERIFIED`
- `USER_UPDATED`

### Fix Required
Add fallback handling:

```typescript
const { data: { subscription } } = supabase.auth.onAuthStateChange(
  async (event, session) => {
    if (!mounted) return;
    authEventReceived = true;
    
    // Handle all session events
    if (session?.user) {
      setUser(session.user);
    } else {
      setUser(null);
      setProfile(null);
    }
    
    // Always set loading false after any event
    setLoading(false);
    
    // Then handle specific events...
    if (event === 'SIGNED_IN' || event === 'INITIAL_SESSION') {
      if (session?.user) fetchProfile(session.user.id, supabase);
    }
  }
);
```

---

## Issue 5: initializedRef Behavior

### Location: `src/lib/auth.ts` line 11, 31-32

```typescript
const initializedRef = useRef(false)

useEffect(() => {
  if (initializedRef.current) return
  initializedRef.current = true
  // ...
}, [fetchProfile])
```

### Analysis
This is **working correctly** - it prevents double-initialization within a single component instance. However, when the component unmounts and a new instance mounts, `initializedRef` is fresh (false), so initialization runs again.

This is **expected behavior** for a hook. The issue is that this is a hook, not a context.

---

## State Batching Analysis

### Question: Are setState calls batching correctly?

**Answer: YES.** React 18+ automatically batches all setState calls within event handlers and async functions. The sequence:

```typescript
setUser(session.user)
await fetchProfile(...)
setLoading(false)
```

Will batch `setUser` with `setLoading` after the await completes (they're in the same tick). This is NOT the issue.

---

## Dashboard useEffect Analysis

### Location: `src/app/dashboard/page.tsx`

| Line | useEffect Purpose | Interferes with Auth? |
|------|-------------------|----------------------|
| 174 | bfcache (pageshow event) | NO - Forces reload on back nav |
| 187 | Load theme/voice from localStorage | NO - Only touches localStorage |
| 196 | Fetch videos when user changes | NO - Depends on `user`, doesn't modify it |
| 234 | Close dropdowns on outside click | NO - UI state only |

**Conclusion:** None of these useEffects interfere with auth state.

---

## Summary of Required Fixes

### Priority 1 (Critical) - Convert to Context
Convert `useAuth()` from a stateful hook to a proper React Context. This is the root cause.

### Priority 2 (High) - Fix Loading Timing
Move `setLoading(false)` before `await fetchProfile()` so UI updates immediately.

### Priority 3 (High) - Fix Dashboard Double-Spinner
Replace second spinner with redirect or "Redirecting..." message.

### Priority 4 (Medium) - Expand Event Coverage
Ensure `setLoading(false)` is called for ALL auth events, not just specific ones.

---

## Quick Fix (Workaround)

If Context refactor is too large, a quick fix for the double-spinner:

```typescript
// In dashboard/page.tsx
if (authLoading) {
  return <LoadingSpinner />;
}

if (!user) {
  // Use useEffect to redirect, not during render
  useEffect(() => {
    if (!authLoading && !user) {
      router.push('/login');
    }
  }, [authLoading, user, router]);
  
  return <div>Redirecting to login...</div>;
}
```

But this is a band-aid. The proper fix is the Context pattern.
