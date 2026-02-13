# Stripe Webhook Setup for Orbital

## Overview

The webhook endpoint at `/api/stripe/webhook` handles:
- **checkout.session.completed** - Credits minutes after successful payment (one-time or first subscription)
- **invoice.paid** - Credits minutes for subscription renewals
- **customer.subscription.deleted** - Clears subscription info when cancelled

## Environment Variables Required

Add these to your `.env.local` (development) and production environment:

```bash
# Already should exist from checkout setup:
STRIPE_SECRET_KEY=sk_live_xxx  # or sk_test_xxx for testing

# NEW - Required for webhook:
STRIPE_WEBHOOK_SECRET=whsec_xxx

# Required for admin operations:
SUPABASE_SERVICE_KEY=eyJxxx...  # Service role key (NOT anon key)
```

## Stripe Dashboard Configuration

### 1. Create the Webhook Endpoint

1. Go to [Stripe Dashboard → Developers → Webhooks](https://dashboard.stripe.com/webhooks)
2. Click **"Add endpoint"**
3. Enter your endpoint URL:
   - **Production:** `https://your-domain.com/api/stripe/webhook`
   - **Local testing:** Use Stripe CLI (see below)
4. Select events to listen to:
   - `checkout.session.completed`
   - `invoice.paid`
   - `customer.subscription.deleted`
5. Click **"Add endpoint"**

### 2. Get the Webhook Secret

1. Click on your newly created webhook endpoint
2. Under **"Signing secret"**, click **"Reveal"**
3. Copy the `whsec_xxx` value
4. Add it to your environment as `STRIPE_WEBHOOK_SECRET`

## Local Development Testing

Use the Stripe CLI to forward webhooks to your local server:

```bash
# Install Stripe CLI (if not already installed)
brew install stripe/stripe-cli/stripe

# Login to Stripe
stripe login

# Forward webhooks to local server
stripe listen --forward-to localhost:3000/api/stripe/webhook

# The CLI will output a webhook signing secret (whsec_xxx)
# Use this for STRIPE_WEBHOOK_SECRET in local dev
```

### Trigger Test Events

```bash
# Trigger a checkout.session.completed event
stripe trigger checkout.session.completed

# Or test the full flow by completing a real test checkout
# Use card number: 4242 4242 4242 4242
```

## Database Requirements

The webhook uses a Supabase RPC function `add_minutes`. Make sure this exists:

```sql
-- Function to add minutes and log the purchase
CREATE OR REPLACE FUNCTION add_minutes(
  p_user_id UUID,
  p_minutes NUMERIC,
  p_amount_cents INTEGER,
  p_tier TEXT,
  p_stripe_session_id TEXT
)
RETURNS VOID AS $$
BEGIN
  -- Update the user's minutes balance
  UPDATE profiles 
  SET minutes_balance = COALESCE(minutes_balance, 0) + p_minutes
  WHERE id = p_user_id;
  
  -- Log the purchase
  INSERT INTO purchases (user_id, minutes, amount_cents, tier, stripe_session_id)
  VALUES (p_user_id, p_minutes, p_amount_cents, p_tier, p_stripe_session_id);
END;
$$ LANGUAGE plpgsql SECURITY DEFINER;
```

Also ensure the `profiles` table has these columns for subscriptions:
- `stripe_customer_id` (TEXT)
- `stripe_subscription_id` (TEXT)
- `subscription_tier` (TEXT)
- `minutes_balance` (NUMERIC)

## Verifying Webhook is Working

### Check Stripe Dashboard

1. Go to **Developers → Webhooks**
2. Click on your endpoint
3. Check the **"Attempts"** tab for delivery logs
4. Status should show `200 OK`

### Check Server Logs

Look for these log messages:
- `✅ Added X minutes to user Y` - Successful minute credit
- `❌ Failed to add minutes: ...` - Database error
- `❌ Webhook signature verification failed` - Invalid/wrong secret

## Troubleshooting

### "Webhook secret not configured"
- Ensure `STRIPE_WEBHOOK_SECRET` is set in your environment
- Restart your server after adding env vars

### "Missing stripe-signature header"
- The request is not coming from Stripe
- Check you're using the correct endpoint URL

### "Webhook signature verification failed"
- Wrong `STRIPE_WEBHOOK_SECRET` value
- Using test secret with production webhook or vice versa
- Request body was modified (ensure raw body is passed)

### Minutes not credited
- Check that `add_minutes` RPC function exists
- Check user_id in checkout session metadata
- Verify `SUPABASE_SERVICE_KEY` is set correctly

## Security Notes

1. **Never expose the webhook secret** - It's used to verify requests are from Stripe
2. **Use HTTPS in production** - Stripe requires HTTPS for production webhooks
3. **Service key is sensitive** - The `SUPABASE_SERVICE_KEY` has admin access; never expose to frontend
