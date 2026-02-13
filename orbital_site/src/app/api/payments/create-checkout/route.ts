import { NextRequest, NextResponse } from 'next/server';
import Stripe from 'stripe';
import { createClient } from '@supabase/supabase-js';

// Lazy init Stripe (avoid build-time errors when env vars not available)
function getStripe() {
  if (!process.env.STRIPE_SECRET_KEY) {
    throw new Error('STRIPE_SECRET_KEY not configured');
  }
  return new Stripe(process.env.STRIPE_SECRET_KEY);
}

// Pricing tiers with Stripe price IDs
const TIERS = {
  starter: {
    oneTime: { priceId: process.env.STRIPE_PRICE_STARTER!, minutes: 10 },
    subscription: { priceId: process.env.STRIPE_PRICE_STARTER_SUB!, minutes: 10 },
  },
  standard: {
    oneTime: { priceId: process.env.STRIPE_PRICE_STANDARD!, minutes: 50 },
    subscription: { priceId: process.env.STRIPE_PRICE_STANDARD_SUB!, minutes: 50 },
  },
  pro: {
    oneTime: { priceId: process.env.STRIPE_PRICE_PRO!, minutes: 120 },
    subscription: { priceId: process.env.STRIPE_PRICE_PRO_SUB!, minutes: 120 },
  },
};

export async function POST(request: NextRequest) {
  try {
    // Get auth token from header
    const authHeader = request.headers.get('Authorization');
    if (!authHeader?.startsWith('Bearer ')) {
      return NextResponse.json({ detail: 'Unauthorized' }, { status: 401 });
    }
    const token = authHeader.replace('Bearer ', '');

    // Verify user with Supabase
    const supabase = createClient(
      process.env.NEXT_PUBLIC_SUPABASE_URL!,
      process.env.NEXT_PUBLIC_SUPABASE_ANON_KEY!
    );
    
    const { data: { user }, error: authError } = await supabase.auth.getUser(token);
    if (authError || !user) {
      return NextResponse.json({ detail: 'Invalid token' }, { status: 401 });
    }

    // Parse request body
    const body = await request.json();
    const { tier, mode, success_url, cancel_url } = body;

    // Validate tier
    if (!tier || !TIERS[tier as keyof typeof TIERS]) {
      return NextResponse.json(
        { detail: `Invalid tier. Must be one of: ${Object.keys(TIERS).join(', ')}` },
        { status: 400 }
      );
    }

    const tierData = TIERS[tier as keyof typeof TIERS];
    const isSubscription = mode === 'subscription';
    const priceConfig = isSubscription ? tierData.subscription : tierData.oneTime;

    if (!priceConfig.priceId) {
      return NextResponse.json(
        { detail: 'Stripe prices not configured' },
        { status: 500 }
      );
    }

    // Create Stripe checkout session
    const sessionParams: Stripe.Checkout.SessionCreateParams = {
      payment_method_types: ['card'],
      line_items: [
        {
          price: priceConfig.priceId,
          quantity: 1,
        },
      ],
      mode: isSubscription ? 'subscription' : 'payment',
      success_url: `${success_url}?session_id={CHECKOUT_SESSION_ID}`,
      cancel_url: cancel_url,
      client_reference_id: user.id,
      metadata: {
        user_id: user.id,
        tier: tier,
        minutes: String(priceConfig.minutes),
        mode: mode,
      },
    };

    if (isSubscription) {
      sessionParams.allow_promotion_codes = true;
    }

    const stripe = getStripe();
    const session = await stripe.checkout.sessions.create(sessionParams);

    return NextResponse.json({
      checkout_url: session.url,
      session_id: session.id,
    });
  } catch (error) {
    console.error('Checkout error:', error);
    const message = error instanceof Error ? error.message : 'Unknown error';
    return NextResponse.json({ detail: message }, { status: 500 });
  }
}
