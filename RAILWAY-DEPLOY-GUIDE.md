# Railway Deployment Guide — Orbital API

**Time estimate:** 10-15 minutes

## Prerequisites
- Railway account (railway.app)
- GitHub repo with API code (or we push it)

---

## Step 1: Push API to GitHub (if not already)

```bash
cd ~/Desktop/Orbital/orbital_api
git init
git add -A
git commit -m "Initial API commit"
gh repo create Claudio-Atlas/orbital-api --private --push
```

---

## Step 2: Create Railway Project

1. Go to [railway.app](https://railway.app)
2. Click **"New Project"**
3. Select **"Deploy from GitHub repo"**
4. Connect your GitHub and select `Claudio-Atlas/orbital-api`

---

## Step 3: Configure Environment Variables

In Railway dashboard → your project → **Variables** tab, add ALL of these:

### Required — Supabase
```
SUPABASE_URL=<copy from ~/Desktop/Orbital/orbital_api/.env>
SUPABASE_ANON_KEY=<copy from .env>
SUPABASE_SERVICE_KEY=<copy from .env>
```

### Required — AI Providers
```
DEEPSEEK_API_KEY=<copy from .env>
OPENAI_API_KEY=<your-openai-key>
```

### Required — Stripe
```
STRIPE_SECRET_KEY=<copy from ~/Desktop/Orbital/orbital_api/.env>
STRIPE_WEBHOOK_SECRET=<we'll get this after setting up webhook>
STRIPE_PRICE_STARTER=<copy from .env>
STRIPE_PRICE_STANDARD=<copy from .env>
STRIPE_PRICE_PRO=<copy from .env>
STRIPE_PRICE_STARTER_SUB=<copy from .env>
STRIPE_PRICE_STANDARD_SUB=<copy from .env>
STRIPE_PRICE_PRO_SUB=<copy from .env>
```

### Config
```
ORBITAL_PROVIDER=deepseek
TTS_PROVIDER=openai
```

### Optional — R2 (set up later for video storage)
```
R2_ACCOUNT_ID=
R2_ACCESS_KEY_ID=
R2_SECRET_ACCESS_KEY=
R2_BUCKET_NAME=orbital-videos
```

---

## Step 4: Configure Build Settings

Railway should auto-detect Python. If not, add these files:

**railway.json** (create in repo root):
```json
{
  "$schema": "https://railway.app/railway.schema.json",
  "build": {
    "builder": "NIXPACKS"
  },
  "deploy": {
    "startCommand": "uvicorn main:app --host 0.0.0.0 --port $PORT",
    "restartPolicyType": "ON_FAILURE"
  }
}
```

**Procfile** (alternative, create in repo root):
```
web: uvicorn main:app --host 0.0.0.0 --port $PORT
```

---

## Step 5: Deploy

1. Railway will auto-deploy when you push to GitHub
2. Watch the build logs for errors
3. Once deployed, get your public URL from Railway dashboard (e.g., `https://orbital-api-production.up.railway.app`)

---

## Step 6: Update Frontend

Update `orbital_site/.env.local` (and Vercel env vars):

```
NEXT_PUBLIC_API_URL=https://orbital-api-production.up.railway.app
```

Then redeploy frontend.

---

## Step 7: Set Up Stripe Webhook

1. Go to Stripe Dashboard → Developers → Webhooks
2. Add endpoint: `https://your-railway-url.up.railway.app/stripe/webhook`
3. Select events: `checkout.session.completed`, `customer.subscription.created`, etc.
4. Copy the webhook signing secret
5. Add to Railway env vars as `STRIPE_WEBHOOK_SECRET`

---

## Step 8: Test

```bash
# Health check
curl https://your-railway-url.up.railway.app/health

# Should return:
# {"status":"healthy","service":"orbital-solver","jobs_in_memory":0}
```

---

## Troubleshooting

**Build fails:**
- Check requirements.txt has all dependencies
- Look at build logs for missing packages

**App crashes on start:**
- Check env vars are all set
- Look at runtime logs

**Stripe webhook fails:**
- Verify webhook secret is correct
- Check Railway logs for the incoming request

---

## Cost Estimate

Railway Hobby plan: ~$5/month for low traffic
- Includes 500 hours runtime
- Auto-sleeps when idle
- Wakes on request (~1-2s cold start)

For production, consider Pro plan (~$20/month) for always-on.
