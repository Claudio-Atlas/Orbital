# Orbital Database Setup

## Supabase Setup

1. Create a new Supabase project at https://supabase.com
2. Go to SQL Editor
3. Run `schema.sql` to create tables and functions

## Environment Variables

Add to your `.env`:

```bash
SUPABASE_URL=https://xxxxx.supabase.co
SUPABASE_ANON_KEY=eyJhbGciOiJIUzI1NiIs...
SUPABASE_SERVICE_KEY=eyJhbGciOiJIUzI1NiIs...  # For server-side operations
```

## Tables

| Table | Purpose |
|-------|---------|
| `profiles` | User data, minutes balance (extends auth.users) |
| `purchases` | Purchase history, Stripe records |
| `videos` | Generated videos, expiry tracking |

## Key Functions

| Function | Purpose |
|----------|---------|
| `handle_new_user()` | Auto-creates profile on signup |
| `deduct_minutes(user_id, minutes)` | Atomically deduct minutes (returns false if insufficient) |
| `add_minutes(user_id, minutes, amount, tier, stripe_id)` | Add minutes after purchase |

## Row Level Security (RLS)

All tables have RLS enabled. Users can only access their own data.

## Cloudflare R2 Setup

1. Create R2 bucket named `orbital-videos`
2. Add lifecycle rule: Delete objects with prefix `videos/` after 2 days
3. Get API credentials for the bucket

## Stripe Setup

1. Create products for each tier:
   - Starter: $2 (price_xxx)
   - Standard: $8 (price_xxx)
   - Pro: $15 (price_xxx)
2. Set up webhook for `checkout.session.completed`
3. Add to `.env`:
   ```
   STRIPE_SECRET_KEY=sk_live_xxx
   STRIPE_WEBHOOK_SECRET=whsec_xxx
   STRIPE_PRICE_STARTER=price_xxx
   STRIPE_PRICE_STANDARD=price_xxx
   STRIPE_PRICE_PRO=price_xxx
   ```
