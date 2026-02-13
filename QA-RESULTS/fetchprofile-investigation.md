# fetchProfile Investigation

**Investigated:** 2025-01-27  
**File:** `src/lib/auth.ts`

---

## 1. What does fetchProfile do?

```typescript
const fetchProfile = useCallback(async (userId: string, client: ReturnType<typeof getSupabase>) => {
  try {
    const { data, error } = await client
      .from('profiles')
      .select('*')
      .eq('id', userId)
      .single()

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

**Summary:**
- Queries the `profiles` table in Supabase
- Selects all columns (`*`) where `id` matches the user ID
- Uses `.single()` expecting exactly one row
- Sets the profile state if data is returned

---

## 2. Does it have try/catch? What happens on error?

✅ **Yes, it has try/catch**

**Error handling:**
- Catches exceptions and logs them: `console.error('[Auth] Profile fetch error:', err)`
- Also checks for Supabase-level errors from the query
- **Ignores error code `PGRST116`** (PostgREST "no rows returned" - expected for new users)
- Logs other errors to console

**⚠️ ISSUE:** On error, it only logs. It does NOT:
- Set profile to null explicitly
- Set any error state
- Notify the user

---

## 3. Does it always call setLoading(false) even on error?

## ⛔ CRITICAL BUG FOUND

**No! fetchProfile does NOT call setLoading(false) at all.**

The loading state is managed in the caller (onAuthStateChange handler):

```typescript
if (event === 'INITIAL_SESSION' || event === 'SIGNED_IN') {
  if (session?.user) {
    setUser(session.user)
    await fetchProfile(session.user.id, supabase)  // ← If this hangs...
  }
  setLoading(false)  // ← ...this never runs!
}
```

**The problem:**
- `fetchProfile` is awaited before `setLoading(false)`
- If the Supabase query hangs (network issue, RLS timeout, etc.), loading stays `true` forever
- The user sees infinite loading spinner

---

## 4. Is there a timeout? Could it hang forever?

**Partial protection only:**

```typescript
// Safety timeout - only fires if NO auth event was received
const timeout = setTimeout(() => {
  if (mounted && !authEventReceived) {  // ← Only if NO event received
    console.warn('[Auth] No auth event received in 5s, assuming not logged in')
    setLoading(false)
  }
}, 5000)
```

**⚠️ PROBLEM:**
- The 5-second timeout only fires if `authEventReceived` is `false`
- Once `INITIAL_SESSION` or `SIGNED_IN` fires, `authEventReceived = true`
- If the auth event fires but `fetchProfile` hangs, **there's no timeout protection**
- The app could hang forever waiting for the profile query

---

## 5. Supabase Configuration Analysis

### Table Queried
- **Table:** `profiles`
- **Query:** `SELECT * WHERE id = userId`

### Key Usage
From `supabase.ts`:
```typescript
export function createClient() {
  return createBrowserClient(
    process.env.NEXT_PUBLIC_SUPABASE_URL!,
    process.env.NEXT_PUBLIC_SUPABASE_ANON_KEY!  // ← ANON key, not service key
  )
}
```

**This is correct for client-side.** The anon key means:
- RLS (Row Level Security) policies ARE enforced
- Users can only read their own profile (if RLS is set up correctly)

### RLS Consideration
If RLS policies on `profiles` table don't allow the user to read their own row, the query will:
1. Return empty (no error, just no data)
2. Or return an error depending on policy

**This could explain:**
- Profile not loading (RLS blocking)
- Infinite loading (if RLS check hangs)

---

## Summary of Issues Found

| Issue | Severity | Description |
|-------|----------|-------------|
| No timeout on fetchProfile | 🔴 Critical | If Supabase query hangs, loading stays true forever |
| Await blocks setLoading | 🔴 Critical | setLoading(false) waits for fetchProfile to complete |
| No error state | 🟡 Medium | Errors are logged but not surfaced to UI |
| RLS dependency | 🟡 Medium | Query relies on RLS being correctly configured |

---

## Recommended Fixes

### 1. Add timeout to fetchProfile
```typescript
const fetchProfile = useCallback(async (userId: string, client: ReturnType<typeof getSupabase>) => {
  const timeout = new Promise((_, reject) => 
    setTimeout(() => reject(new Error('Profile fetch timeout')), 5000)
  )
  
  try {
    const queryPromise = client
      .from('profiles')
      .select('*')
      .eq('id', userId)
      .single()
    
    const { data, error } = await Promise.race([queryPromise, timeout])
    // ... rest of handling
  } catch (err) {
    console.error('[Auth] Profile fetch error:', err)
  }
}, [])
```

### 2. Don't block loading on profile fetch
```typescript
if (session?.user) {
  setUser(session.user)
  setLoading(false)  // ← Set loading false BEFORE profile fetch
  fetchProfile(session.user.id, supabase)  // ← Don't await - let it load in background
}
```

### 3. Verify RLS policies
Check that `profiles` table has a policy like:
```sql
CREATE POLICY "Users can read own profile"
ON profiles FOR SELECT
USING (auth.uid() = id);
```

---

## Files Reviewed
- `src/lib/auth.ts` - Main auth hook with fetchProfile
- `src/lib/supabase.ts` - Supabase client configuration
