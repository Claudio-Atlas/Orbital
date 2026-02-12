# Google OAuth Branding Guide — Orbital

**Time estimate:** 5 minutes

This makes the Google sign-in screen show "Orbital" instead of the ugly Supabase project URL.

---

## Step 1: Access Google Cloud Console

1. Go to [console.cloud.google.com](https://console.cloud.google.com)
2. Make sure you're in the correct project (the one with your OAuth credentials)

---

## Step 2: Navigate to OAuth Consent Screen

1. In the left sidebar: **APIs & Services** → **OAuth consent screen**
2. You should see your existing consent screen config

---

## Step 3: Edit App Information

Click **"Edit App"** and update:

### App Information
- **App name:** `Orbital`
- **User support email:** `hello@orbitalsolver.io` (or your email)
- **App logo:** Upload the Orbital logo (512x512 PNG recommended)

### App Domain (optional but professional)
- **Application home page:** `https://orbitalsolver.io`
- **Application privacy policy:** `https://orbitalsolver.io/privacy`
- **Application terms of service:** `https://orbitalsolver.io/terms`

### Developer Contact
- **Email:** Your email address

---

## Step 4: Save Changes

Click **"Save and Continue"** through the screens.

---

## Step 5: Verify (Optional for Production)

For production with 100+ users, you may need to verify the app:
1. Go through Google's verification process
2. This removes the "unverified app" warning
3. Required for publishing to external users

For now (testing/early launch), unverified is fine.

---

## Result

After these changes, users will see:

```
Sign in with Google

Choose an account
to continue to Orbital

[Your accounts listed here]
```

Instead of:

```
to continue to pqwhfiuvcsjfevjwljml.supabase.co
```

---

## Notes

- Changes may take a few minutes to propagate
- The Supabase URL will still appear in the actual OAuth flow (this is normal)
- What changes is the **app name** shown to users
