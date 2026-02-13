# Spinner Bug Investigation

## Summary
**Root Cause Found:** `setLoading(false)` is gated behind `await fetchProfile()` completing. If profile fetch hangs, loading never becomes false, causing eternal spinner.

---

## The Exact Sequence

### In `src/lib/auth.ts` (lines 50-64):

```javascript
if (event === 'INITIAL_SESSION' || event === 'SIGNED_IN') {
  if (session?.user) {
    console.log('[Auth] Setting user:', session.user.email)  // ← LOG APPEARS
    setUser(session.user)                                    // ← User IS set
    await fetchProfile(session.user.id, supabase)            // ← BLOCKS HERE
  } else {
    console.log('[Auth] No user in session')
    setUser(null)
    setProfile(null)
  }
  setLoading(false)  // ← NEVER REACHED if fetchProfile hangs!
}
```

### What Happens:
1. ✅ Auth event fires (`INITIAL_SESSION` or `SIGNED_IN`)
2. ✅ `console.log('[Auth] Setting user: email@gmail.com')` — **this is the log we see**
3. ✅ `setUser(session.user)` — user state IS updated
4. ⏳ `await fetchProfile(...)` — **BLOCKS HERE**
5. ❌ `setLoading(false)` — **NEVER CALLED** if step 4 hangs

---

## Dashboard Rendering Logic

### In `src/app/dashboard/page.tsx` (lines 253-269):

```javascript
const { user, profile, loading: authLoading, signOut } = useAuth();

// ...

// Show loading while checking auth
if (authLoading) {
  return (
    <div className="min-h-screen w-full flex items-center justify-center bg-black">
      <div className="w-8 h-8 border-2 border-violet-500 border-t-transparent rounded-full animate-spin" />
    </div>
  );
}

// If not logged in, show loading spinner
if (!user) {
  return (
    <div className="min-h-screen w-full flex items-center justify-center bg-black">
      <div className="w-8 h-8 border-2 border-violet-500 border-t-transparent rounded-full animate-spin" />
    </div>
  );
}
```

### Why Spinner Shows:
- `authLoading` is **still `true`** because `setLoading(false)` was never called
- Dashboard hits the first `if (authLoading)` check → **returns spinner**
- Even though `user` is set, we never reach that check

---

## What `fetchProfile` Awaits

### In `src/lib/auth.ts` (lines 15-28):

```javascript
const fetchProfile = useCallback(async (userId: string, client: ...) => {
  try {
    const { data, error } = await client
      .from('profiles')
      .select('*')
      .eq('id', userId)
      .single()  // ← Supabase query - can hang on network issues

    if (error && error.code !== 'PGRST116') {
      console.error('[Auth] Profile fetch error:', error.message)
    }
    
    if (data) {
      setProfile(data as Profile)
    }
  } catch (err) {
    console.error('[Auth] Profile fetch error:', err)
  }
}, [])
```

**Potential hang points:**
1. Supabase client network request (no timeout configured)
2. DNS resolution issues
3. SSL handshake delays
4. Server-side query slowness

Note: Even if the query errors, the function completes. The issue is when the **network request itself hangs** (never resolves or rejects).

---

## The Disconnect

```
┌─────────────────────────────────────────────────────────────────┐
│ EXPECTED FLOW                                                    │
├─────────────────────────────────────────────────────────────────┤
│ Auth event → setUser() → fetchProfile() → setLoading(false)     │
│                                              ↓                   │
│                              Dashboard sees loading=false        │
│                                              ↓                   │
│                              Dashboard checks user (set) → RENDER│
└─────────────────────────────────────────────────────────────────┘

┌─────────────────────────────────────────────────────────────────┐
│ ACTUAL FLOW (BUG)                                                │
├─────────────────────────────────────────────────────────────────┤
│ Auth event → setUser() → fetchProfile() [HANGS...]              │
│                              ↓                                   │
│              setLoading(false) NEVER CALLED                      │
│                              ↓                                   │
│              Dashboard sees loading=true → SPINNER FOREVER       │
└─────────────────────────────────────────────────────────────────┘
```

---

## Evidence Supporting This Theory

1. **Log shows `[Auth] Setting user: email@gmail.com`** — proves auth event fired, user was set
2. **Spinner persists** — proves `authLoading` is still `true`
3. **No `[Auth] Profile fetch error:` log** — proves fetchProfile didn't error, it's just hanging

---

## Recommended Fix

### Option A: Set loading false BEFORE profile fetch (preferred)

```javascript
if (event === 'INITIAL_SESSION' || event === 'SIGNED_IN') {
  if (session?.user) {
    console.log('[Auth] Setting user:', session.user.email)
    setUser(session.user)
    setLoading(false)  // ← Move here - auth is resolved, profile is bonus
    fetchProfile(session.user.id, supabase)  // ← No await - fire and forget
  } else {
    setUser(null)
    setProfile(null)
    setLoading(false)
  }
}
```

**Why this works:** User can interact with dashboard immediately while profile loads in background.

### Option B: Add timeout to profile fetch

```javascript
const fetchWithTimeout = async (promise, ms) => {
  const timeout = new Promise((_, reject) => 
    setTimeout(() => reject(new Error('Timeout')), ms)
  );
  return Promise.race([promise, timeout]);
};

// In auth handler:
try {
  await fetchWithTimeout(fetchProfile(session.user.id, supabase), 5000);
} catch (e) {
  console.warn('[Auth] Profile fetch timed out');
}
setLoading(false);
```

### Option C: Separate loading states

```javascript
const [authLoading, setAuthLoading] = useState(true)
const [profileLoading, setProfileLoading] = useState(true)

// In handler:
setUser(session.user)
setAuthLoading(false)  // Auth is done
fetchProfile(...).finally(() => setProfileLoading(false))  // Profile is separate
```

---

## Other Loading States in Dashboard

The dashboard has one additional loading state for videos:

```javascript
const [loadingVideos, setLoadingVideos] = useState(true);
```

This is separate from auth and only affects the videos list, not the main spinner.

---

## Middleware Interaction

The middleware (`src/middleware.ts`) handles server-side auth checks:
- Redirects unauthenticated users to `/login` for protected routes
- This works correctly and doesn't cause the spinner issue
- The issue is purely client-side in the `useAuth` hook

---

## Conclusion

**The bug is clear:** `setLoading(false)` depends on `fetchProfile` completing, but profile fetch can hang indefinitely on network issues.

**The fix is simple:** Decouple auth completion from profile loading. Set `loading=false` as soon as we know the user's auth state, regardless of whether their profile has loaded.
