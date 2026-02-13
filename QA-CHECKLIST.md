# Orbital QA Checklist

## Auth Flows

### Sign Up
- [ ] Email/password signup works
- [ ] Shows confirmation message
- [ ] Email verification link works
- [ ] Redirect to dashboard after verification

### Login
- [ ] Email/password login works
- [ ] Google OAuth login works  
- [ ] Apple OAuth login works (if enabled)
- [ ] "Forgot password" sends reset email
- [ ] Password reset link works
- [ ] Redirect to dashboard after login
- [ ] Redirect to intended page if came from protected route

### Logout
- [ ] Logout from dashboard works
- [ ] Logout from settings works
- [ ] Logout redirects to home page
- [ ] Cannot access dashboard after logout
- [ ] Cannot access settings after logout

### Session Persistence
- [ ] Stay logged in after page refresh
- [ ] Stay logged in after closing/reopening browser
- [ ] Stay logged in after navigating between pages

### Edge Cases
- [ ] Back button from Stripe → dashboard still works
- [ ] Back button from external site → dashboard still works
- [ ] Multiple tabs don't conflict
- [ ] Incognito mode works correctly
- [ ] Session timeout handled gracefully

---

## Protected Routes

### Dashboard `/dashboard`
- [ ] Shows loading spinner while checking auth
- [ ] Redirects to login if not authenticated
- [ ] Shows user email in menu
- [ ] Shows correct minutes balance
- [ ] Theme toggle works
- [ ] User menu opens/closes

### Settings `/settings`
- [ ] Accessible when logged in
- [ ] Redirects to login if not authenticated
- [ ] Displays user info correctly

### Purchases `/purchases`
- [ ] Accessible when logged in
- [ ] Redirects to login if not authenticated
- [ ] Shows purchase history (or empty state)

### Videos `/videos`
- [ ] Accessible when logged in
- [ ] Redirects to login if not authenticated
- [ ] Shows video list (or empty state)

---

## Stripe Checkout

### Pricing Modal
- [ ] Opens from "Buy More" button
- [ ] Shows all three tiers
- [ ] Toggle between one-time and subscription works
- [ ] Prices display correctly
- [ ] Close button works
- [ ] Click outside to close works

### Checkout Flow
- [ ] Starter one-time checkout → Stripe
- [ ] Standard one-time checkout → Stripe
- [ ] Pro one-time checkout → Stripe
- [ ] Starter subscription checkout → Stripe
- [ ] Standard subscription checkout → Stripe
- [ ] Pro subscription checkout → Stripe

### Post-Checkout
- [ ] Success redirect works
- [ ] Cancel redirect works
- [ ] Back button from Stripe works
- [ ] Minutes credited after payment (webhook)

---

## Public Pages

### Home `/`
- [ ] Loads correctly
- [ ] CTA buttons work
- [ ] Navigation works

### Login `/login`
- [ ] Form displays correctly
- [ ] Redirects to dashboard if already logged in

### Signup `/signup`
- [ ] Form displays correctly
- [ ] Redirects to dashboard if already logged in

### Terms `/terms`
- [ ] Page loads

### Privacy `/privacy`
- [ ] Page loads

---

## UI/UX

### Theme
- [ ] Dark mode default
- [ ] Light mode toggle works
- [ ] Theme persists across pages
- [ ] Theme persists across sessions

### Responsive
- [ ] Mobile layout works
- [ ] Tablet layout works
- [ ] Desktop layout works

### Loading States
- [ ] Auth loading shows spinner
- [ ] Checkout loading shows spinner
- [ ] No flash of wrong content

### Error States
- [ ] Invalid login shows error
- [ ] Network error handled gracefully
- [ ] API error handled gracefully

---

## Current Known Issues

1. **Black screen after Stripe back button** - CRITICAL
   - Steps: Login → Dashboard → Buy More → Go to Stripe → Back button → Try to sign out
   - Expected: Dashboard works normally
   - Actual: Black screen

---

## Test Environment

- Browser: Chrome Incognito
- Also test: Safari, Firefox
- Device: Desktop (also test mobile)
